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
from screening.model import FillWindow, Ruling, Verdict
from screening.verdict import assess

#: The window the command asks the venue for. Thirty days is what a monthly figure means.
WINDOW_DAYS = 30

#: Ordered by severity (PDR-0002). The renumbering is a breaking change to this command's
#: interface, made before anything consumes it: a script keeping the idiom it already has —
#: `if code == 0` — stops getting a zero for a trader the command was warning it about.
EXIT_COPYABLE = 0
EXIT_WITH_RESERVATIONS = 1
EXIT_NOT_COPYABLE = 2
EXIT_NO_VERDICT = 3


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


_EXIT = {
    Ruling.COPYABLE: EXIT_COPYABLE,
    Ruling.WITH_RESERVATIONS: EXIT_WITH_RESERVATIONS,
    Ruling.NOT_COPYABLE: EXIT_NOT_COPYABLE,
}


def _render(address: str, verdict: Verdict, window: FillWindow) -> str:
    head = str(verdict.ruling)
    if verdict.reservations:
        # Named in the headline, so the first line alone is actionable. A middle verdict that
        # does not say what it is reserving about would be read as noise, and it will be the
        # common one.
        head += f" ({', '.join(verdict.reservations)})"
    # The dates of the fills actually held, never the range that was requested.
    held_from = _date(window.first_fill_ms) if window.first_fill_ms is not None else "?"
    held_to = _date(window.last_fill_ms) if window.last_fill_ms is not None else "?"
    window_label = (
        f"{held_from} to {held_to}"
        if window.complete
        else (
            f"{held_from} to {held_to} — the most recent part of the "
            f"{window.days_requested:.0f} days asked for, not the oldest"
        )
    )
    lines = [
        f"{head} — {address} at a {verdict.ticket:,.0f} ticket",
        f"  read {verdict.fills_read} fills over {window_label}, "
        f"traded on {verdict.days_traded} of {verdict.calendar_days} days; "
        f"trader account {verdict.trader_account:,.0f}",
        f"  cost to the venue: {window.reads} heavy read(s) of a {venue.MAX_PAGES} budget",
    ]
    if window.waits:
        lines.append(
            f"  the venue asked us to slow down {window.waits} time(s)"
            + ("" if window.complete else ", and the read below stops where the budget did")
        )
    lines += [f"  · {reason}" for reason in verdict.reasons]
    return "\n".join(lines)


def main(
    argv: Sequence[str] | None = None,
    *,
    client: httpx.Client | None = None,
    retry: venue.Retry | None = None,
) -> int:
    try:
        args = _parser().parse_args(argv)
    except SystemExit as exit_code:
        # argparse exits 2 on a usage error, and 2 now means NOT COPYABLE. A script that
        # reads the code and never sees a sentence would record "this trader cannot be
        # copied" because of a typo in its own command line. A malformed invocation is the
        # same thing as an unreadable venue: no verdict.
        # `--help` exits 0 and has already printed. Returning it keeps `main` total, which
        # matters because the copying module will consume this through a contract.
        return EXIT_NO_VERDICT if exit_code.code not in (0, None) else EXIT_COPYABLE
    try:
        ticket = Decimal(args.ticket)
    except InvalidOperation:
        print(f"--ticket: {args.ticket!r} is not a number", file=sys.stderr)
        return EXIT_NO_VERDICT
    if not ticket.is_finite():
        # `nan` and `Infinity` parse as Decimals. Infinity printed a complete verdict headed
        # `at a Infinity ticket` saying every order clears the floor.
        print(f"--ticket: {args.ticket!r} is not a finite amount", file=sys.stderr)
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
            window_asked_days=window.days_requested,
        )
    except (ValueError, ArithmeticError) as error:
        # `ArithmeticError` is the backstop, and it was removed last round on the written
        # reason that `is_finite()` above "already stops every case". That was false:
        # `is_finite()` guards `--ticket` and nothing else, while every other number in
        # `assess` comes from the venue. A verifier walked `accountValue: "NaN"`,
        # `accountValue: "Infinity"`, a `px: "NaN"` fill and a zero-notional fill straight
        # through to an uncaught decimal error — which the process reports as exit 1, and
        # this deliverable is what made 1 mean COPYABLE WITH RESERVATIONS.
        #
        # The four shapes are refused in `assess` now, with reasons. This stays because the
        # fifth one has not been thought of yet, and the cost of missing it is a crash that
        # reads as a qualified yes.
        print(f"no verdict: {error}", file=sys.stderr)
        return EXIT_NO_VERDICT

    print(_render(args.address, verdict, window))
    return _EXIT[verdict.ruling]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
