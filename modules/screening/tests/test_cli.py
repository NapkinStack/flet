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
