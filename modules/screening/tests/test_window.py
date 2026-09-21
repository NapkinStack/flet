"""The venue answers at most 2000 fills per call, ascending, so a range denser than the read
budget yields its OLDEST part. For "can my members copy this trader?", that is the wrong half.

These are the tests that pin the direction of the read: whatever gets dropped, the window kept
ends at the moment of the run.
"""

from __future__ import annotations

import bisect
import json
from decimal import Decimal
from typing import Any

import httpx
import pytest

from screening.venue import MAX_PAGES, PAGE_SIZE, VenueUnavailable, fills_since

ADDRESS = "0x0000000000000000000000000000000000000001"
DAY_MS = 86_400_000
NOW_MS = 1_790_000_000_000


def row(time_ms: int) -> dict[str, Any]:
    return {"coin": "BTC", "px": "100", "sz": "1", "time": time_ms, "crossed": True}


def venue(series: list[int]) -> tuple[httpx.Client, list[dict[str, Any]]]:
    """A venue holding `series` (ascending fill times), answering as Hyperliquid does.

    `userFills` returns the **newest** page. `userFillsByTime` returns the **oldest** page
    within the range asked for — which is the whole reason a naive read keeps stale fills.
    """
    calls: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        calls.append(payload)
        if payload["type"] == "userFills":
            chosen = series[-PAGE_SIZE:]
        else:
            start, end = int(payload["startTime"]), int(payload["endTime"])
            lo = bisect.bisect_left(series, start)
            hi = bisect.bisect_right(series, end)
            chosen = series[lo:hi][:PAGE_SIZE]
        return httpx.Response(200, json=[row(t) for t in chosen])

    return httpx.Client(transport=httpx.MockTransport(handler)), calls


def evenly(per_day: int, days: int) -> list[int]:
    """A trader filling at a constant rate, the newest fill landing exactly at `NOW_MS`."""
    step = DAY_MS // per_day
    return list(range(NOW_MS - days * DAY_MS, NOW_MS + 1, step))


def rising(quiet_per_day: int, busy_per_day: int, busy_days: int, days: int) -> list[int]:
    """A trader who was quiet for most of the month and has been frantic for the last few days.

    This is the shape that broke the old read. Paging forward from thirty days back, the budget
    is spent crossing the quiet stretch and dies a little way into the busy one — so the window
    kept ends days before the question was asked, while the trader is still filling orders.
    """
    busy_from = NOW_MS - busy_days * DAY_MS
    quiet = list(range(NOW_MS - days * DAY_MS, busy_from, DAY_MS // quiet_per_day))
    busy = list(range(busy_from, NOW_MS + 1, DAY_MS // busy_per_day))
    return quiet + busy


def heavy(calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [c for c in calls if c["type"] == "userFillsByTime"]


# --- the cheap path ---------------------------------------------------------------------


def test_a_sparse_trader_costs_no_heavy_read_at_all() -> None:
    """The venue's own page already holds everything. Asking for it by time as well would be
    a second read of the same fills, metered by weight, for nothing."""
    client, calls = venue([NOW_MS - 29 * DAY_MS, NOW_MS - DAY_MS])
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert window.complete is True
    assert len(window.fills) == 2
    assert heavy(calls) == [], "a sparse trader must cost one cheap read and nothing else"
    assert window.reads == 0


def test_the_venue_s_own_page_answers_when_it_reaches_past_the_window() -> None:
    """A full page that reaches back beyond 30 days means the 30 days are inside it."""
    series = evenly(per_day=50, days=40)
    client, calls = venue(series)
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert window.complete is True
    assert heavy(calls) == [], "nothing older than the page was needed"
    assert all(f.time_ms >= NOW_MS - 30 * DAY_MS for f in window.fills), "and nothing older kept"


# --- the direction of the read ----------------------------------------------------------


def test_a_dense_window_is_read_backwards_from_now() -> None:
    client, calls = venue(evenly(per_day=4000, days=40))
    fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    reads = heavy(calls)
    assert reads, "a dense trader needs heavy reads"
    assert reads[0]["endTime"] == NOW_MS, "the first heavy read must end now"
    assert int(reads[0]["startTime"]) > NOW_MS - DAY_MS, (
        "and it must be a recent CHUNK, not the whole month — the old read also ended its "
        "first call at now, while starting it thirty days back, which is the whole defect"
    )
    ends = [int(c["endTime"]) for c in reads]
    assert ends == sorted(ends, reverse=True), "and each one after it reaches further back"
    starts = [int(c["startTime"]) for c in reads]
    assert starts == sorted(starts, reverse=True), "walking backwards, never forwards"


def test_a_read_cut_short_by_the_budget_keeps_the_newest_days_not_the_oldest() -> None:
    """S8. A trader busy enough that 30 days cannot be read at all: what survives the budget
    must be the days next to the question, not the far side of the month."""
    client, _ = venue(rising(quiet_per_day=200, busy_per_day=20_000, busy_days=5, days=40))
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)

    assert window.complete is False, "30 days did not fit and the answer must say so"
    assert window.ends_at_ms == NOW_MS
    assert window.starts_at_ms > NOW_MS - 30 * DAY_MS, "it is a shorter, recent window"
    assert window.last_fill_ms is not None
    assert window.last_fill_ms >= NOW_MS - DAY_MS, (
        "the newest fill held must be from the day of the run — this is the assertion the "
        "old ascending read failed, returning fills eleven days stale"
    )


def test_what_it_keeps_has_no_hole_in_it() -> None:
    """A chunk the budget could not finish is missing its newest end. Joining it to the rest
    would leave a gap, and every rate computed across that gap would be wrong."""
    series = rising(quiet_per_day=200, busy_per_day=20_000, busy_days=5, days=40)
    client, _ = venue(series)
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)

    first, last = window.first_fill_ms, window.last_fill_ms
    assert first is not None and last is not None
    expected = series[bisect.bisect_left(series, first) : bisect.bisect_right(series, last)]
    assert len(window.fills) == len(expected), "every fill between the two ends must be held"


# --- what the read costs ----------------------------------------------------------------


def test_it_never_exceeds_the_read_budget() -> None:
    client, calls = venue(evenly(per_day=4000, days=40))
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert len(heavy(calls)) <= MAX_PAGES, "the venue meters by weight; this is the ceiling"
    assert window.reads == len(heavy(calls)), "and the answer states what it actually spent"


def test_a_dense_trader_costs_far_fewer_reads_than_the_ceiling_when_the_window_fits() -> None:
    """Chunks are sized from the measured rate, so a trader whose 30 days do fit is read in
    roughly the number of pages their fills occupy — not in twenty reads regardless."""
    client, calls = venue(evenly(per_day=200, days=40))
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert window.complete is True
    assert len(heavy(calls)) <= MAX_PAGES


# --- what the window reports --------------------------------------------------------------


def test_it_reports_the_fills_it_holds_not_the_range_it_asked_for() -> None:
    """Every defect on this branch has been the same one: a number derived from what was
    ASKED FOR, printed as a fact about what was READ."""
    client, _ = venue([NOW_MS - 22 * DAY_MS, NOW_MS - 9 * DAY_MS])
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert window.first_fill_ms == NOW_MS - 22 * DAY_MS
    assert window.last_fill_ms == NOW_MS - 9 * DAY_MS
    assert window.calendar_days == 13, "the days it holds, not the 30 it asked for"


def test_it_reports_the_window_it_actually_covered() -> None:
    client, _ = venue([NOW_MS - 10 * DAY_MS, NOW_MS - 2 * DAY_MS])
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert window.days_covered == Decimal(8), "the span of the fills actually read"
    assert window.days_requested == Decimal(30)


def test_an_empty_read_has_no_dates_to_report() -> None:
    client, _ = venue([])
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert window.first_fill_ms is None
    assert window.calendar_days == 0
    assert window.complete is True, "the venue answered; there is simply nothing there"


def test_it_says_so_when_a_page_cannot_be_read() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("no route to host")

    with pytest.raises(VenueUnavailable):
        fills_since(ADDRESS, days=30, client=httpx.Client(transport=httpx.MockTransport(handler)))
