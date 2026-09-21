"""`screening <address> --ticket <eur>` — the command an administrator runs.

Read-only. It carries no credential and cannot sign (ADR-0002).
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation

import httpx

from screening import venue
from screening.model import FillWindow, Verdict
from screening.verdict import assess

#: The window the command asks the venue for. Thirty days is what a monthly figure means.
WINDOW_DAYS = 30

EXIT_COPYABLE = 0
EXIT_NOT_COPYABLE = 1
EXIT_NO_VERDICT = 2


def _date(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=UTC).strftime("%Y-%m-%d")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="screening",
        description=(
            "Can a member of a given ticket copy this trader? Answers from the trader's "
            "public fills. Copyability is arithmetic, not merit: this never ranks a trader."
        ),
    )
    parser.add_argument("address", help="the trader's public address on the venue")
    parser.add_argument(
        "--ticket",
        required=True,
        help="what one member would put under copy, in the venue's quote currency",
    )
    return parser


def _render(address: str, verdict: Verdict, window: FillWindow) -> str:
    head = "COPYABLE" if verdict.copyable else "NOT COPYABLE"
    read_from = _date(window.starts_at_ms)
    read_to = _date(window.ends_at_ms)
    window_label = (
        f"{read_from} to {read_to}"
        if window.complete
        else f"{read_from} to {read_to} only — the venue could not return the 30 days asked for"
    )
    lines = [
        f"{head} — {address} at a {verdict.ticket:,.0f} ticket",
        f"  read {verdict.fills_read} fills over {window_label}, "
        f"traded on {verdict.days_traded} of {verdict.calendar_days} days; "
        f"trader account {verdict.trader_account:,.0f}",
    ]
    if window.waits:
        lines.append(
            f"  the venue asked us to slow down {window.waits} time(s); the answer below is "
            f"complete but the read was throttled"
        )
    lines += [f"  · {reason}" for reason in verdict.reasons]
    return "\n".join(lines)


def main(
    argv: Sequence[str] | None = None,
    *,
    client: httpx.Client | None = None,
    retry: venue.Retry | None = None,
) -> int:
    args = _parser().parse_args(argv)
    try:
        ticket = Decimal(args.ticket)
    except InvalidOperation:
        print(f"--ticket: {args.ticket!r} is not a number", file=sys.stderr)
        return EXIT_NO_VERDICT

    owned = client is None
    http = client or venue.client()
    try:
        window = venue.fills_since(args.address, days=WINDOW_DAYS, client=http, retry=retry)
        account = venue.account_value(args.address, http, retry=retry)
    except venue.VenueUnavailable as error:
        print(f"venue unavailable — no verdict: {error}", file=sys.stderr)
        return EXIT_NO_VERDICT
    finally:
        if owned:
            http.close()

    try:
        verdict = assess(
            window.fills,
            trader_account=account,
            ticket=ticket,
            window_days=window.days_requested if window.complete else None,
            window_complete=window.complete,
        )
    except ValueError as error:
        print(f"no verdict: {error}", file=sys.stderr)
        return EXIT_NO_VERDICT

    print(_render(args.address, verdict, window))
    return EXIT_COPYABLE if verdict.copyable else EXIT_NOT_COPYABLE


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
