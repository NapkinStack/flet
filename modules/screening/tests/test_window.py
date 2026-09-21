"""The venue returns at most 2000 fills per call, so the observation window is whatever that
cap happens to cover. These are the tests that stop a monthly figure being an artefact of it.
"""

from __future__ import annotations

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


def paging_client(pages: list[list[dict[str, Any]]]) -> tuple[httpx.Client, list[int]]:
    """Answers each call with the next page, and records the startTime it was asked for."""
    asked: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        asked.append(int(payload["startTime"]))
        page = pages[len(asked) - 1] if len(asked) <= len(pages) else []
        return httpx.Response(200, json=page)

    return httpx.Client(transport=httpx.MockTransport(handler)), asked


def test_it_asks_for_the_window_it_wants_not_the_one_the_cap_gives() -> None:
    client, asked = paging_client([[row(NOW_MS - 29 * DAY_MS), row(NOW_MS - DAY_MS)]])
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert asked == [NOW_MS - 30 * DAY_MS], "the first call must start 30 days back"
    assert window.complete is True
    assert len(window.fills) == 2


def test_it_pages_until_the_venue_stops_filling_the_page() -> None:
    """A full page means there is more behind it."""
    first = [row(NOW_MS - (30 - i // 100) * DAY_MS) for i in range(PAGE_SIZE)]
    second = [row(NOW_MS - DAY_MS)] * 3
    client, asked = paging_client([first, second])
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert len(asked) == 2, "a full page must be followed by another call"
    assert asked[1] == first[-1]["time"] + 1, "the next page starts after the last fill read"
    assert len(window.fills) == PAGE_SIZE + 3
    assert window.complete is True


def test_it_stops_at_the_page_cap_and_says_the_window_is_incomplete() -> None:
    """A trader busy enough to fill every page is exactly the one whose monthly figure
    would otherwise be invented."""
    full = [row(NOW_MS - 30 * DAY_MS + i) for i in range(PAGE_SIZE)]
    client, asked = paging_client([full] * (2 * MAX_PAGES + 4))
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    # Two passes at most: the window asked for, then a recent window sized to what that got
    # through. Neither pages forever.
    assert len(asked) <= 2 * MAX_PAGES, "it must not page forever"
    assert window.complete is False, "an incomplete window must say so"
    assert len(window.fills) == PAGE_SIZE * MAX_PAGES, "what it kept is one full pass"


def test_it_reports_the_window_it_actually_covered() -> None:
    client, _ = paging_client([[row(NOW_MS - 10 * DAY_MS), row(NOW_MS - 2 * DAY_MS)]])
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert window.days_covered == Decimal(8), "the span of the fills actually read"
    assert window.days_requested == Decimal(30)


def test_it_says_so_when_a_page_cannot_be_read() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("no route to host")

    with pytest.raises(VenueUnavailable):
        fills_since(ADDRESS, days=30, client=httpx.Client(transport=httpx.MockTransport(handler)))


def test_a_cut_short_read_keeps_the_recent_end_not_the_stale_one() -> None:
    """Paging ascends from the start of a range, so stopping at the cap keeps the OLDEST part
    and throws away the newest. For "can my members copy this trader?", the half worth keeping
    is the recent one — a trader who stopped a fortnight ago must not read as current."""
    calls: list[tuple[int, int]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        start, end = int(payload["startTime"]), int(payload["endTime"])
        calls.append((start, end))
        span = end - start
        # the trader fills a page every half-day, so a 30-day window cannot fit
        if span > 10 * DAY_MS:
            return httpx.Response(200, json=[row(start + i) for i in range(PAGE_SIZE)])
        return httpx.Response(200, json=[row(start), row(end - 1)])

    window = fills_since(
        ADDRESS, days=30, client=httpx.Client(transport=httpx.MockTransport(handler)), now_ms=NOW_MS
    )
    assert window.complete is False, "30 days did not fit and the answer must say so"
    assert window.ends_at_ms == NOW_MS, "the window kept must end now, not a fortnight ago"
    assert window.starts_at_ms > NOW_MS - 30 * DAY_MS, "it is a shorter, recent window"
    assert calls[-1][1] == NOW_MS, "the last read must reach up to now"


def test_it_reports_the_dates_it_read_so_a_truncated_answer_can_be_judged() -> None:
    client, _ = paging_client([[row(NOW_MS - 10 * DAY_MS), row(NOW_MS - 2 * DAY_MS)]])
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert window.starts_at_ms == NOW_MS - 30 * DAY_MS, "what it asked for"
    assert window.ends_at_ms == NOW_MS
    assert window.calendar_days == 8, "and, separately, what it holds — the two are not the same"


def test_it_reports_the_fills_it_holds_not_the_range_it_asked_for() -> None:
    """Every defect on this branch has been the same one: a number derived from what was
    ASKED FOR, printed as a fact about what was READ. The window carries the timestamps it
    actually holds, so the two cannot be confused again."""
    client, _ = paging_client([[row(NOW_MS - 22 * DAY_MS), row(NOW_MS - 9 * DAY_MS)]])
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert window.first_fill_ms == NOW_MS - 22 * DAY_MS
    assert window.last_fill_ms == NOW_MS - 9 * DAY_MS
    assert window.calendar_days == 13, "the days it holds, not the 30 it asked for"


def test_a_second_pass_that_also_overflows_is_still_incomplete() -> None:
    """The narrowed window can overflow too. Saying `complete` then is the failure the
    narrowing was written to prevent, wearing different clothes."""
    full = [row(NOW_MS - 30 * DAY_MS + i) for i in range(PAGE_SIZE)]
    client, _ = paging_client([full] * (2 * MAX_PAGES + 4))
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert window.complete is False, "neither pass reached the end of its range"


def test_an_empty_read_has_no_dates_to_report() -> None:
    client, _ = paging_client([[]])
    window = fills_since(ADDRESS, days=30, client=client, now_ms=NOW_MS)
    assert window.first_fill_ms is None
    assert window.calendar_days == 0
