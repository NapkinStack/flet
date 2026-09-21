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

from screening.model import Fill
from screening.venue import (
    MAX_PAGES,
    PAGE_SIZE,
    VenueUnavailable,
    fills_since,
)

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


def venue_read_range(
    client: httpx.Client, start_ms: int, end_ms: int, budget: int = MAX_PAGES
) -> tuple[list[Fill], bool, int]:
    """One range, read to its end. Private in the module; reached here because one defect
    lives at the page boundary and arranging that boundary through the chunked walk is a
    coincidence rather than a test."""
    from screening.venue import Retry, _read_range, _Waiting

    return _read_range(ADDRESS, start_ms, end_ms, client, _Waiting(Retry()), budget)


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


def test_a_crowded_millisecond_inside_the_window_leaves_no_hole() -> None:
    """A page that ENDS inside a group of fills sharing one millisecond used to step to the
    next millisecond and drop the rest of that group — a silent gap in the middle of a window
    reported as contiguous. A verifier built this case twice; the second time it lost 1250 of
    2500 fills, and the guard written for it missed it entirely because that guard only looked
    at whether the WHOLE page sat in one millisecond."""
    # Smaller than a page: a page that ends inside it can back off to its start and read it
    # whole next time. More than a page at one millisecond is a different case, below.
    clump_at = NOW_MS - 6 * 3600 * 1000
    series = sorted(
        [clump_at] * 1500 + list(range(NOW_MS - 2 * DAY_MS, NOW_MS + 1, (2 * DAY_MS) // 3000))
    )
    client, _ = venue(series)
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)

    first, last = window.first_fill_ms, window.last_fill_ms
    assert first is not None and last is not None
    assert first <= clump_at <= last, "the crowded millisecond must be inside what was kept"
    expected = series[bisect.bisect_left(series, first) : bisect.bisect_right(series, last)]
    assert len(window.fills) == len(expected), (
        "every fill between the two ends is held, the crowded millisecond included"
    )
    assert sum(1 for f in window.fills if f.time_ms == clump_at) == series.count(clump_at), (
        "every fill at that millisecond, counted from the series rather than from a constant "
        "that would quietly encode where the fixture happens to land"
    )


# --- what the read costs ----------------------------------------------------------------


def test_it_never_exceeds_the_read_budget() -> None:
    client, calls = venue(evenly(per_day=4000, days=40))
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert len(heavy(calls)) <= MAX_PAGES, "the venue meters by weight; this is the ceiling"
    assert window.reads == len(heavy(calls)), "and the answer states what it actually spent"


def test_a_trader_whose_month_fits_is_read_in_a_few_reads_not_the_whole_budget() -> None:
    """Chunks aim at half a page, so a complete read costs about twice the pages the fills
    occupy — a bounded multiple, not the ceiling regardless."""
    series = evenly(per_day=200, days=40)
    client, calls = venue(series)
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert window.complete is True
    pages_the_fills_occupy = -(-(30 * 200) // PAGE_SIZE)
    assert len(heavy(calls)) <= 2 * pages_the_fills_occupy + 2, (
        "the name of this test used to promise 'far fewer' while asserting only 'not more "
        "than twenty', which is not a claim about anything"
    )


def test_a_quiet_month_behind_a_busy_week_is_still_read_whole() -> None:
    """The probe measures the trader's NEWEST fills, which for anyone with a burst is the
    densest stretch of their month. Cutting every chunk to that step walks the quiet weeks in
    spike-sized paces and spends the budget on hours: a verifier measured 0.07 of a day
    returned where the previous implementation returned all thirty. Chunks grow when one
    comes back near-empty, which is what leaves the burst behind."""
    burst = list(range(NOW_MS - 10 * 60 * 1000, NOW_MS + 1, (10 * 60 * 1000) // 2000))
    series = sorted(evenly(per_day=50, days=40) + burst)
    client, calls = venue(series)
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)

    assert window.complete is True, "thirty days of a mostly quiet trader must fit"
    assert window.calendar_days == 30, "and all thirty must actually be held"
    assert len(heavy(calls)) < MAX_PAGES, "without spending the whole budget to get there"


def test_a_chunk_the_budget_cannot_finish_is_dropped_whole() -> None:
    """The branch that carries the no-hole invariant. A wall of fills behind quiet ground:
    chunks grow across the quiet part, then one lands on the wall, cannot be finished inside
    what is left of the budget, and must be dropped rather than joined with a gap in it."""
    # Busy enough at the front that the probe fills, then quiet ground so the chunks grow,
    # then a wall far enough back that a grown chunk lands on it with little budget left.
    front = list(range(NOW_MS - 2 * DAY_MS, NOW_MS + 1, (2 * DAY_MS) // 3000))
    quiet = list(range(NOW_MS - 10 * DAY_MS, NOW_MS - 2 * DAY_MS, DAY_MS // 10))
    wall_at = NOW_MS - 12 * DAY_MS
    wall = list(range(wall_at, wall_at + 200_000, 2))
    series = sorted(front + quiet + wall)
    client, _ = venue(series)
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)

    first, last = window.first_fill_ms, window.last_fill_ms
    assert first is not None and last is not None
    assert window.complete is False
    assert last >= NOW_MS - DAY_MS, "and what survives still ends at the run"
    expected = series[bisect.bisect_left(series, first) : bisect.bisect_right(series, last)]
    assert len(window.fills) == len(expected), (
        "every fill between the two ends is held: the unfinished chunk was dropped, not "
        "joined with a hole in the middle"
    )


def test_a_page_wholly_inside_one_millisecond_stops_the_read_without_blaming_the_venue() -> None:
    """More than a page of fills at one millisecond leaves the cursor nowhere to go: it cannot
    step past without dropping some, and there is no earlier boundary to back off to. The read
    stops there and says the window is incomplete.

    It must NOT report a venue outage. That would be false — the venue answered every call —
    and it would throw away the recent days already in hand, which are the ones the question
    is about."""
    crowded = [NOW_MS - 20 * DAY_MS] * (PAGE_SIZE + 500)
    recent = list(range(NOW_MS - 2 * DAY_MS, NOW_MS + 1, (2 * DAY_MS) // 3000))
    client, _ = venue(sorted(crowded + recent))

    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert window.complete is False, "it could not reach the far edge, and must say so"
    assert window.last_fill_ms is not None
    assert window.last_fill_ms >= NOW_MS - DAY_MS, "what it did reach still ends at the run"


def test_a_page_exactly_filled_by_one_millisecond_does_not_cost_the_whole_answer() -> None:
    """Exactly `PAGE_SIZE` fills at one millisecond, with nothing more there: stepping past
    would drop nothing. We cannot tell that from the venue's answer, so the read stops — but
    stopping must cost only the ground beyond, never the command."""
    crowded = [NOW_MS - 20 * DAY_MS] * PAGE_SIZE
    recent = list(range(NOW_MS - 2 * DAY_MS, NOW_MS + 1, (2 * DAY_MS) // 3000))
    client, _ = venue(sorted(crowded + recent))

    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert window.fills, "the recent days are still answered"
    assert window.last_fill_ms is not None
    assert window.last_fill_ms >= NOW_MS - DAY_MS


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


def test_a_chunk_that_overran_cuts_the_next_one_back() -> None:
    """Growth has to have a brake. A chunk that grew across quiet ground and then needed
    several reads to clear a busy patch must not hand the same span to the next chunk, or one
    dense stretch turns every later read into a multi-page one."""
    front = list(range(NOW_MS - 2 * DAY_MS, NOW_MS + 1, (2 * DAY_MS) // 3000))
    quiet = list(range(NOW_MS - 30 * DAY_MS, NOW_MS - 2 * DAY_MS, DAY_MS // 10))
    patch_at = NOW_MS - 11 * DAY_MS
    patch = list(range(patch_at, patch_at + 50_000, 10))
    client, calls = venue(sorted(front + quiet + patch))
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)

    assert window.complete is True, "the month still fits once the brake is applied"
    assert window.calendar_days == 30
    assert len(heavy(calls)) < MAX_PAGES, "and it is not paid for with the whole budget"


def test_an_overshooting_chunk_is_cut_and_the_same_ground_tried_again() -> None:
    """Growth needs a way back. A trader with quiet ground in front of a dense stretch makes
    the chunks grow, and one then lands on the dense part and cannot be finished. Ending the
    read there spends the whole remaining budget on nothing: a verifier measured four days
    held where the implementation being replaced held twelve.

    The span is cut and the same ground is tried again instead."""
    front = list(range(NOW_MS - 2 * DAY_MS, NOW_MS + 1, (2 * DAY_MS) // 3000))
    quiet = list(range(NOW_MS - 11 * DAY_MS, NOW_MS - 2 * DAY_MS, DAY_MS // 10))
    wall_at = NOW_MS - 12 * DAY_MS
    wall = list(range(wall_at, wall_at + 120_000, 2))
    client, calls = venue(sorted(front + quiet + wall))

    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)

    assert window.complete is False, "the wall is not readable inside the budget"
    assert window.calendar_days >= 9, (
        "but the quiet ground in front of it is, and must not be thrown away with the chunk "
        "that overshot — without the retry this holds about four days"
    )
    assert window.last_fill_ms is not None
    assert window.last_fill_ms >= NOW_MS - DAY_MS, "and what is held still ends at the run"
    assert len(heavy(calls)) <= MAX_PAGES


def test_ground_known_too_dense_is_never_grown_back_into() -> None:
    """The cut and the growth used to fight each other: a chunk overshoots and is cut, the
    next one comes back near-empty, growth puts it straight back into the same dense ground.
    A verifier measured three full cut-grow-overshoot cycles over one day, fourteen of twenty
    reads wasted, and thirteen times fewer fills held than the implementation before it."""
    series = sorted(
        evenly(per_day=300, days=40)
        + list(range(NOW_MS - 10 * DAY_MS, NOW_MS - 10 * DAY_MS + 60_000, 2))
    )
    client, calls = venue(series)
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)

    assert window.days_covered >= Decimal("9.5"), (
        "the quiet ground down to the dense day must be read. Measured: 10.00 days with the "
        "memory, 8.74 without it. Asserted on `days_covered` and not on `calendar_days`, "
        "which rounds up — 8.74 becomes 9 there, and this assertion passed against the very "
        "commit it was written to fail against"
    )
    wide = [c for c in heavy(calls) if int(c["endTime"]) - int(c["startTime"]) >= 4 * DAY_MS]
    assert len(wide) <= 2, (
        "a span already known to overshoot is not launched at again and again: the "
        "oscillation ran three full cut-grow-overshoot cycles over the same day"
    )


def test_a_page_ending_on_one_member_of_a_crowded_millisecond_leaves_no_hole() -> None:
    """The alignment a verifier found by sweeping the page boundary across a crowded
    millisecond: when exactly ONE member of the group is the page's last fill, the previous
    guard — which compared the last two fills — did not fire, the cursor stepped past, and
    2499 of 2500 fills were dropped while the range still reported itself completely read.

    Read at the level the defect lives at, because arranging that alignment through the
    chunked walk is a coincidence rather than a test."""
    clump_at = NOW_MS - 5 * DAY_MS
    before = [clump_at - (PAGE_SIZE - i) for i in range(PAGE_SIZE - 1)]
    series = sorted(before + [clump_at] * 2500 + [clump_at + 1000])
    client, _ = venue(series)

    from screening.venue import _Unsteppable

    try:
        read, whole, _ = venue_read_range(client, series[0], NOW_MS)
    except _Unsteppable:
        return  # it stopped rather than stepping over: nothing was dropped silently

    held_at_clump = sum(1 for f in read if f.time_ms == clump_at)
    assert held_at_clump in (0, 2500), (
        f"all of the crowded millisecond or none of it, never {held_at_clump} of 2500 — "
        "the alignment that dropped 2499 reported the range as completely read"
    )
    if whole:
        assert len(read) == len(series), "a range reported as read whole must hold all of it"
