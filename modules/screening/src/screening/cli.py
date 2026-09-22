"""`screening <address> --ticket <eur>` — the command an administrator runs.

Read-only. It carries no credential and cannot sign (ADR-0002).
"""

from __future__ import annotations

import argparse
import contextlib
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from typing import NoReturn

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

#: argparse's own status for a usage error. It never reaches the caller — `_decide` reads it
#: as no verdict — but `2` is NOT COPYABLE here, and an unnamed 2 in this file invites the
#: reader to think a typo produces a verdict.
EXIT_USAGE = 2


def _say(reason: str) -> None:
    """The reason, on stderr, or nowhere at all — never on stdout, and never fatally.

    Two ways this line used to decide the exit code by itself, both found by a confirmation
    run and both reachable through the installed command:

    `... 2>&1 >/dev/null | true` with an unbuffered stderr raises `BrokenPipeError` out of
    `print`. It escaped `main` — including out of `main`'s own backstop, which is where this
    lands when everything else has already failed — and CPython exits **1**, which this
    deliverable is what made mean COPYABLE WITH RESERVATIONS. A reader that consumes nothing
    is not an opinion about a trader.

    `... 2>&-` closes fd 2, so CPython sets `sys.stderr` to `None`, and `print(file=None)`
    writes to **stdout**. The reason for having no verdict was landing where the verdict
    goes, which is what the amendment of 2026-09-22 says never happens. An exit code of 3
    with 59 bytes on stdout is exactly the shape a script cannot read.

    Neither was introduced by the backstop above; both were in every one of these prints
    since the command existed, and being one line from closed is not a reason to leave a
    fourth one open.
    """
    stream = sys.stderr
    if stream is None:
        return
    # A broken or closed stderr. There is nowhere left to say it, and stdout is not a
    # fallback: silence, and the exit code carries the answer on its own.
    #
    # `Exception`, not `(OSError, ValueError)`: a confirmation run reached exit 1 — which
    # names a verdict — through a `sys.stderr` whose `write` raised `RuntimeError`. It found
    # no route to that through a shell, and one character closes it. `KeyboardInterrupt` and
    # `SystemExit` are `BaseException` and still leave.
    with contextlib.suppress(Exception):
        print(reason, file=stream)


def _date(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=UTC).strftime("%Y-%m-%d")


class _Parser(argparse.ArgumentParser):
    """`argparse` reports a usage error itself, and it does not go through `_say`.

    `ArgumentParser.error` calls `print_usage(sys.stderr)`. With fd 2 closed `sys.stderr` is
    `None`, and `print_usage` substitutes **stdout** for it — so six ordinary malformed
    command lines put 46 bytes of `usage: ...` where the verdict goes, under exit 3. A
    confirmation run measured it, and it is the same shape as the leak closed one commit
    earlier: that guard covered every write in this file, and argparse is not in this file.

    Reporting the error through `_say` and exiting with no message of argparse's own keeps
    `--help` on stdout, where it belongs, and leaves the mapping in `_decide` untouched:
    `SystemExit(2)` from a usage error is already read there as no verdict.
    """

    def error(self, message: str) -> NoReturn:
        _say(f"{self.format_usage().rstrip()}\n{self.prog}: error: {message}")
        self.exit(EXIT_USAGE)


def _parser() -> argparse.ArgumentParser:
    parser = _Parser(
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


def _decide(
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
        _say(f"--ticket: {args.ticket!r} is not a number")
        return EXIT_NO_VERDICT
    if not ticket.is_finite():
        # `nan` and `Infinity` parse as Decimals. Infinity printed a complete verdict headed
        # `at a Infinity ticket` saying every order clears the floor.
        _say(f"--ticket: {args.ticket!r} is not a finite amount")
        return EXIT_NO_VERDICT

    owned = client is None
    http = client or venue.client()
    try:
        window = venue.fills_since(args.address, days=WINDOW_DAYS, client=http, retry=retry)
        account = venue.account_value(args.address, http, retry=retry)
    except venue.VenueUnavailable as error:
        _say(f"venue unavailable — no verdict: {error}")
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
        _say(f"no verdict: {error}")
        return EXIT_NO_VERDICT

    print(_render(args.address, verdict, window))
    return _EXIT[verdict.ruling]


def main(
    argv: Sequence[str] | None = None,
    *,
    client: httpx.Client | None = None,
    retry: venue.Retry | None = None,
) -> int:
    """`_decide`, with a backstop under the whole of it.

    A verifier reached exit 1 — which this deliverable is what made mean COPYABLE WITH
    RESERVATIONS — from two ordinary environment variables: `https_proxy=socks5://...`
    without `socksio` installed, and `SSL_CERT_FILE` naming a file that is not there. Both
    raise while `httpx.Client` is being built, one line before the `try` that guards the
    reads, so the process died with an empty stdout and a code that reads as a qualified yes
    about a trader whose fills were never read. `venue`'s handlers are narrower than they
    look as well: they catch `httpx.HTTPError`, and `httpx.StreamError` is a `RuntimeError`.

    Nothing caught it because every test of the command passes `client=`, so `venue.client()`
    — the one line the administrator's own invocation runs — was run by no test at all.

    This is the reasoning behind the `ArithmeticError` backstop in `_decide`, applied to the
    command rather than to `assess`: no unhandled exception may leave this process carrying a
    code that names a verdict.
    """
    try:
        return _decide(argv, client=client, retry=retry)
    except Exception as error:
        _say(f"no verdict: {type(error).__name__}: {error}")
        return EXIT_NO_VERDICT


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
