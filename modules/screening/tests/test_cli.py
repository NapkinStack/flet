"""The command an administrator actually runs."""

from __future__ import annotations

import json
import time
from typing import Any

import httpx
import pytest

from screening.cli import main
from screening.venue import Retry

ADDRESS = "0x102d1d1a6240581a809bac9b9b4dff2eafe8c058"
DAY_MS = 86_400_000
NOW_MS = int(time.time() * 1000)


def venue(fills: list[dict[str, Any]], account: str) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        kind = json.loads(request.content)["type"]
        if kind.startswith("userFills"):
            return httpx.Response(200, json=fills)
        return httpx.Response(200, json={"marginSummary": {"accountValue": account}})

    return httpx.Client(transport=httpx.MockTransport(handler))


def a_fill(px: str, day: int, crossed: bool = True) -> dict[str, Any]:
    """`day` 0 is twenty-nine days ago, `day` 29 is today.

    Dated against the clock the command reads, not against the epoch: the read now keeps only
    what falls inside the window it was asked for, so a fill stamped 1970 is correctly thrown
    away — and a fixture that relies on it being kept is testing nothing.
    """
    return {
        "coin": "BTC",
        "px": px,
        "sz": "1",
        "time": NOW_MS - (29 - day) * DAY_MS,
        "crossed": crossed,
    }


def test_it_answers_for_a_copyable_trader(capsys: pytest.CaptureFixture[str]) -> None:
    rows = [a_fill("2000", day) for day in range(0, 30)]
    code = main([ADDRESS, "--ticket", "2000"], client=venue(rows, "20000"))
    out = capsys.readouterr().out
    assert code == 0
    assert "copyable" in out.lower()
    assert "%" in out, "the figures must be shown, not just the verdict"


def test_it_refuses_and_says_what_ticket_would_work(capsys: pytest.CaptureFixture[str]) -> None:
    rows = [a_fill("2000", day) for day in range(0, 30)]
    code = main([ADDRESS, "--ticket", "500"], client=venue(rows, "300000"))
    out = capsys.readouterr().out
    assert code == 2, "not copyable is 2 now: the codes run by severity (PDR-0002)"
    assert "10" in out, "the floor must be named"


def test_it_returns_no_verdict_when_the_venue_is_unreachable(
    capsys: pytest.CaptureFixture[str],
) -> None:
    def down(_: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("no route to host")

    code = main(
        [ADDRESS, "--ticket", "2000"],
        client=httpx.Client(transport=httpx.MockTransport(down)),
        retry=Retry(attempts=1),
    )
    captured = capsys.readouterr()
    assert code == 3, "no verdict is the most severe: worse than not copyable (PDR-0002)"
    assert "unavailable" in (captured.out + captured.err).lower()
    assert "copyable" not in captured.out.lower(), "no verdict from partial data"


def test_it_never_calls_an_incomplete_answer_complete(capsys: pytest.CaptureFixture[str]) -> None:
    """`the answer below is complete` was printed three lines after `the venue could not
    return the 30 days asked for`, to an administrator."""
    page = [a_fill("2000", day) for day in range(0, 30)]
    refusals = [True]

    def handler(request: httpx.Request) -> httpx.Response:
        kind = json.loads(request.content)["type"]
        if not kind.startswith("userFills"):
            return httpx.Response(200, json={"marginSummary": {"accountValue": "20000"}})
        if refusals:
            refusals.pop()
            return httpx.Response(429, json={"error": "slow down"})
        return httpx.Response(200, json=page)

    main(
        [ADDRESS, "--ticket", "2000"],
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        retry=Retry(attempts=3, sleep=lambda _: None),
    )
    out = capsys.readouterr().out.lower()
    assert "slow down 1 time" in out, "the throttling is reported"
    assert "complete" not in out, "and nothing claims completeness it does not have"


def test_it_states_what_the_read_cost_the_venue(capsys: pytest.CaptureFixture[str]) -> None:
    """The venue meters by weight. A cost the administrator cannot see is a cost nobody is
    watching, and D2's second acceptance criterion asks for it in so many words."""
    rows = [a_fill("2000", day) for day in range(0, 30)]
    main([ADDRESS, "--ticket", "2000"], client=venue(rows, "20000"))
    out = capsys.readouterr().out
    assert "heavy read(s)" in out, "the number of heavy reads must be stated"
    assert "0 heavy read(s)" in out, "and this trader fits in the cheap probe, so it is zero"


def test_the_headline_names_the_extrapolation_when_the_window_was_cut_short(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The reservation existed only in unit tests until this was written: the command passed
    `window_days=None` for a cut-short window, so the extrapolation was measured against
    itself and could never fire in production."""
    import bisect

    from screening.venue import PAGE_SIZE

    # Dense enough over two days that thirty cannot be read, so the window is cut short and
    # the monthly figures are stretched by about fifteen.
    series = list(range(NOW_MS - 2 * DAY_MS, NOW_MS + 1, (2 * DAY_MS) // 60_000))

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        if payload["type"] == "clearinghouseState":
            return httpx.Response(200, json={"marginSummary": {"accountValue": "20000"}})
        if payload["type"] == "userFills":
            chosen = series[-PAGE_SIZE:]
        else:
            lo = bisect.bisect_left(series, int(payload["startTime"]))
            hi = bisect.bisect_right(series, int(payload["endTime"]))
            chosen = series[lo:hi][:PAGE_SIZE]
        return httpx.Response(
            200,
            json=[
                {"coin": "BTC", "px": "2000", "sz": "1", "time": t, "crossed": True} for t in chosen
            ],
        )

    code = main(
        [ADDRESS, "--ticket", "2000"],
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    out = capsys.readouterr().out
    assert "RESERVATIONS" in out or "NOT COPYABLE" in out
    assert "extrapolation" in out, "a window stretched past the alert is named in the headline"
    assert code in (1, 2)


def dense_venue(series: list[int], account: str = "20000", px: str = "2000") -> httpx.Client:
    """A venue holding `series` (ascending fill times), answering as Hyperliquid does."""
    import bisect

    from screening.venue import PAGE_SIZE

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        if payload["type"] == "clearinghouseState":
            return httpx.Response(200, json={"marginSummary": {"accountValue": account}})
        if payload["type"] == "userFills":
            chosen = series[-PAGE_SIZE:]
        else:
            lo = bisect.bisect_left(series, int(payload["startTime"]))
            hi = bisect.bisect_right(series, int(payload["endTime"]))
            chosen = series[lo:hi][:PAGE_SIZE]
        return httpx.Response(
            200,
            json=[{"coin": "BTC", "px": px, "sz": "1", "time": t, "crossed": True} for t in chosen],
        )

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_the_middle_verdict_has_its_own_exit_code(capsys: pytest.CaptureFixture[str]) -> None:
    """The distinction this whole decision exists to create, and nothing pinned it: setting
    `EXIT_WITH_RESERVATIONS = 2` — collapsing the middle verdict onto NOT COPYABLE's code —
    left the entire suite green."""
    rows = [a_fill("100000", day) for day in range(0, 30)]
    code = main([ADDRESS, "--ticket", "2000"], client=venue(rows, "20000"))
    out = capsys.readouterr().out

    assert out.splitlines()[0].startswith("COPYABLE WITH RESERVATIONS")
    assert code == 1, "the middle verdict is 1: not 0, and above all not 2"


def test_the_reservation_is_named_on_the_first_line_not_merely_somewhere(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`the headline alone is actionable` is the point of naming it. Asserting the word
    appears anywhere in the output proves nothing — the body already says it."""
    rows = [a_fill("100000", day) for day in range(0, 30)]
    main([ADDRESS, "--ticket", "2000"], client=venue(rows, "20000"))
    first = capsys.readouterr().out.splitlines()[0]
    assert "fees" in first, "the reservation must be on the headline"


def test_a_window_stretched_past_the_ceiling_gives_no_verdict_through_the_command(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The ceiling had no CLI test. Its unit test passes `window_days` with
    `window_complete=False`, a combination `main` never produces — so the production path to
    the ceiling was unpinned, which is the exact shape of the defect D3 was written to fix."""
    # Everything inside three hours, far too dense to read inside the budget.
    series = list(range(NOW_MS - 3 * 3600 * 1000, NOW_MS + 1, 90))
    code = main([ADDRESS, "--ticket", "2000"], client=dense_venue(series))

    assert capsys.readouterr().out == "", "no verdict means nothing on stdout"
    assert code == 3, "past the ceiling there is no verdict, not a weak one"


def test_no_verdict_outranks_every_verdict_including_not_copyable(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """An earlier version of this branch let the floor win over the ceiling, reasoning that
    whether orders clear 10 USDC is read straight off the notionals. The reasoning was wrong:
    those notionals are the ones inside the window we actually got, so `refused_share` and
    `minimum_ticket` become inferences from half an hour printed as facts about a trader.

    A verifier measured what it produced — `NOT COPYABLE` above
    `8352.24% of their ticket per month in fees`, `extrapolated ... by a factor of 823.3` —
    which is precisely what the amendment's success criterion says must never be shown."""
    series = list(range(NOW_MS - 3 * 3600 * 1000, NOW_MS + 1, 90))
    code = main([ADDRESS, "--ticket", "1"], client=dense_venue(series, account="1000000"))

    assert capsys.readouterr().out == "", "no verdict prints no verdict, not a refusal"
    assert code == 3, "the ceiling is reached before any verdict is formed"


def test_help_returns_rather_than_escaping(capsys: pytest.CaptureFixture[str]) -> None:
    """`main` is typed `-> int` and the copying module will consume it through a contract.
    `--help` raised SystemExit through it."""
    assert main(["--help"]) == 0
    assert "--ticket" in capsys.readouterr().out


def test_a_malformed_command_line_is_no_verdict_not_a_verdict(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """argparse exits 2 on a usage error, and 2 now means NOT COPYABLE. A script reading the
    code and never seeing a sentence would record `this trader cannot be copied` because of a
    typo in its own command line."""
    assert main([ADDRESS]) == 3, "a missing --ticket is no verdict"
    assert main([ADDRESS, "--ticket", "2000", "--window", "30"]) == 3, "so is a bad flag"


def test_a_ticket_that_is_not_a_finite_amount_is_no_verdict() -> None:
    """`nan` and `Infinity` parse as Decimals. `nan` escaped as an uncaught exception, which
    Python exits 1 for — and 1 now means COPYABLE WITH RESERVATIONS. A crash must never read
    as a qualified yes."""
    rows = [a_fill("2000", day) for day in range(0, 30)]
    for bad in ("nan", "Infinity", "-Infinity"):
        assert main([ADDRESS, "--ticket", bad], client=venue(rows, "20000")) == 3, bad


def test_the_headline_names_two_reservations_in_the_order_the_decision_fixes(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The order was asserted on the private helper, one layer below the surface the decision
    is about. PDR-0002 fixes the order of what is **named in the headline**, and sorting the
    tuple inside `_render` passed all sixty-eight tests — `fees` would have stopped being
    first and nothing would have said so."""
    # `fees` and `concentration`, chosen because the decision's order and alphabetical order
    # disagree on them. A fixture of `fees, reproducibility` is already alphabetical, so
    # sorting the tuple leaves it identical and the assertion proves nothing — which is what
    # the first attempt at this test did.
    rows = [a_fill("300000", day) for day in range(0, 10)]
    main([ADDRESS, "--ticket", "2000"], client=venue(rows, "20000"))
    first = capsys.readouterr().out.splitlines()[0]

    assert "(fees, concentration)" in first, (
        "both named, in the decision's order — sorted() would give (concentration, fees)"
    )


def test_a_refused_trader_says_not_copyable_in_those_words(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Rewriting the floor-versus-ceiling test deleted the only assertion of this literal, and
    nothing replaced it: renaming the verdict to `NOT-COPYABLE` passed all sixty-eight tests.
    Fixing a blocker should not cost the coverage that was already there."""
    rows = [a_fill("2000", day) for day in range(0, 30)]
    code = main([ADDRESS, "--ticket", "500"], client=venue(rows, "300000"))
    assert capsys.readouterr().out.splitlines()[0].startswith("NOT COPYABLE")
    assert code == 2


def test_a_venue_number_that_is_not_a_number_is_no_verdict() -> None:
    """`is_finite()` guards `--ticket` and nothing else. Every other number in `assess` comes
    from the venue, and a verifier walked four shapes straight through to an uncaught decimal
    error — which the process reports as exit 1, the code this deliverable made mean
    COPYABLE WITH RESERVATIONS. A crash must never read as a qualified yes."""
    rows = [a_fill("2000", day) for day in range(0, 30)]
    for account in ("NaN", "Infinity"):
        assert main([ADDRESS, "--ticket", "2000"], client=venue(rows, account)) == 3, account

    # The one that needs no exotic input at all: enough zero-notional fills to reach the
    # coverage target, so the cutoff itself is zero and the minimum ticket divides by it.
    # One zero alone is not a crash — it is simply refused under the floor, correctly.
    with_zeros = [a_fill("0", day) for day in range(0, 9)] + [
        a_fill("2000", day) for day in range(9, 30)
    ]
    assert main([ADDRESS, "--ticket", "2000"], client=venue(with_zeros, "20000")) == 3

    nan_price = [a_fill("NaN", 0), *(a_fill("2000", day) for day in range(1, 30))]
    assert main([ADDRESS, "--ticket", "2000"], client=venue(nan_price, "20000")) == 3


def test_a_complete_window_is_not_reported_as_extrapolated(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """One line in `main` decides whether the monthly figures are measured or extrapolated.
    Inverting it passed the whole suite: a complete month would report `traded on 1 of 1 days`
    — losing `concentration` — and inflate turnover thirtyfold."""
    # The fills must span FEWER days than the window, or both wirings agree and the test
    # proves nothing — the first attempt used fills on day 0 and day 29, which span 30.
    rows = [a_fill("2000", day) for day in range(20, 30)]
    main([ADDRESS, "--ticket", "2000"], client=venue(rows, "20000"))
    out = capsys.readouterr().out
    assert "extrapolat" not in out, "the window asked for was returned whole"
    assert "of the 30 days read" in out, (
        "counted against the 30 days asked for, not the 10 the fills happen to span"
    )


def test_any_failure_inside_assess_is_no_verdict(monkeypatch: pytest.MonkeyPatch) -> None:
    """The `ArithmeticError` backstop cannot be reached through any input `assess` now
    refuses, so nothing would show it does anything — which is the criticism that got it
    removed once already, with the four escapes that followed. Forced here instead."""
    import screening.cli as cli

    def boom(*args: object, **kwargs: object) -> None:
        raise ArithmeticError("something nobody thought of")

    monkeypatch.setattr(cli, "assess", boom)
    rows = [a_fill("2000", day) for day in range(0, 30)]
    assert main([ADDRESS, "--ticket", "2000"], client=venue(rows, "20000")) == 3


def test_a_client_the_environment_refuses_to_build_is_no_verdict(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Every other test here passes `client=`, so `venue.client()` — the only line the
    administrator's own invocation runs — was run by no test at all. A verifier ran it, with
    `SSL_CERT_FILE` naming a file that is not there, and got exit 1: COPYABLE WITH
    RESERVATIONS, about a trader whose fills were never read.

    No `client=` here on purpose. The client is built for real."""
    monkeypatch.setenv("SSL_CERT_FILE", "/nonexistent/ca.pem")
    assert main([ADDRESS, "--ticket", "500"]) == 3
    assert capsys.readouterr().out == "", "no verdict means nothing on stdout"


def test_a_read_that_raises_what_venue_does_not_catch_is_no_verdict() -> None:
    """`venue` catches `httpx.HTTPError`, and `httpx.StreamError` is a `RuntimeError` —
    as are the `OSError`s a broken socket raises. They escaped as exit 1."""

    def handler(request: httpx.Request) -> httpx.Response:
        raise RuntimeError("the socket went away mid-read")

    client = httpx.Client(transport=httpx.MockTransport(handler))
    assert main([ADDRESS, "--ticket", "500"], client=client) == 3


def _refusing_client() -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, json={})

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_a_broken_stderr_does_not_become_a_verdict(monkeypatch: pytest.MonkeyPatch) -> None:
    """`... 2>&1 >/dev/null | true` with an unbuffered stderr: the reason cannot be written,
    `BrokenPipeError` escapes the print, and the process exits 1 — COPYABLE WITH RESERVATIONS,
    decided by a reader that consumed nothing. Measured at exit 1 through the installed
    command before this guard."""
    import sys

    class Broken:
        def write(self, text: str) -> int:
            raise BrokenPipeError(32, "Broken pipe")

        def flush(self) -> None:
            raise BrokenPipeError(32, "Broken pipe")

    monkeypatch.setattr(sys, "stderr", Broken())
    # The venue's own refusal, and the backstop under everything else. Both used to report
    # through an unguarded print, and the second one is where a failure lands last.
    assert main([ADDRESS, "--ticket", "500"], client=_refusing_client()) == 3

    def explode(request: httpx.Request) -> httpx.Response:
        raise RuntimeError("nothing catches this one")

    assert (
        main(
            [ADDRESS, "--ticket", "500"],
            client=httpx.Client(transport=httpx.MockTransport(explode)),
        )
        == 3
    )


def test_no_verdict_never_falls_through_to_stdout(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """`... 2>&-` closes fd 2, CPython sets `sys.stderr` to None, and `print(file=None)` writes
    to stdout: 59 bytes of reason where the verdict goes, under exit 3. The amendment of
    2026-09-22 says stdout is empty when there is no answer, so nothing read back can be
    mistaken for one."""
    import sys

    monkeypatch.setattr(sys, "stderr", None)
    assert main([ADDRESS, "--ticket", "500"], client=_refusing_client()) == 3
    assert capsys.readouterr().out == "", "the reason landed on stdout"
