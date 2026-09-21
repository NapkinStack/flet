"""Read-only access to the venue's public endpoint.

An HTTP client, never an SDK that can sign (ADR-0002). Nothing here authenticates, and the
responses are typed by us, so a breaking change is ours to notice.
"""

from __future__ import annotations

import random
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any

import httpx

from screening.model import Fill, FillWindow

INFO_URL = "https://api.hyperliquid.xyz/info"
TIMEOUT_SECONDS = 20.0

#: The venue never returns more than this many fills in one answer.
PAGE_SIZE = 2000

#: How many heavy reads (`userFillsByTime`) one invocation will make. The venue meters by
#: weight rather than by call, so this is a budget for the venue's sake as much as for ours.
#: A trader busy enough to exhaust it is one whose window will be short, and
#: `FillWindow.complete` is how the answer says so.
MAX_PAGES = 20

#: Chunks are sized to come back about this fraction of a page full. The headroom is what
#: lets a trader's rate rise between one chunk and the next without costing a second read.
_CHUNK_LOAD = 2

#: How much a chunk may grow in one step. The probe measures the trader's *newest* fills,
#: which for anyone with a recent burst is the densest stretch of their month — so the first
#: chunk is cut for the spike, and without growth the whole window is walked at that step.
#: Capped so that one near-empty chunk cannot overshoot into a range needing many reads.
_MAX_GROWTH = 16

_MS_PER_DAY = 86_400_000


#: The one 4xx that means "come back later" rather than "this will fail identically".
TOO_MANY = 429


@dataclass(frozen=True)
class Retry:
    """When and how long to wait before asking again.

    `operations.md` E1 wants the side effects analysed before any retry, and they are, in
    `tests/test_retry.py`: the read is idempotent, only transient errors are retried, the
    backoff is exponential with jitter, and both a count and a total budget are set.
    """

    attempts: int = 4
    base_delay_s: float = 0.5
    budget_s: float = 60.0
    sleep: Callable[[float], None] = time.sleep
    monotonic: Callable[[], float] = time.monotonic


@dataclass
class _Waiting:
    """The budget for one invocation, and what it has spent."""

    retry: Retry
    started: float = field(default=0.0)
    waits: int = 0

    def __post_init__(self) -> None:
        self.started = self.retry.monotonic()

    def before_attempt(self, attempt: int) -> None:
        """Sleep before attempt `attempt`, or refuse if the budget will not cover it."""
        # Jittered inside [0.75, 1.25) of the nominal delay: enough that two commands started
        # together do not retry in lockstep, tight enough that the wait still grows.
        delay = self.retry.base_delay_s * (2 ** (attempt - 1)) * (0.75 + 0.5 * random.random())
        spent = self.retry.monotonic() - self.started
        if spent + delay > self.retry.budget_s:
            raise VenueUnavailable(
                f"gave up inside its {self.retry.budget_s:.0f}s budget after {self.waits} wait(s)"
            )
        self.retry.sleep(delay)
        self.waits += 1


class VenueUnavailable(RuntimeError):
    """The venue could not be read, or did not answer in the shape we type.

    No verdict follows from partial or stale data (AGENTS.md).
    """


def _post(payload: dict[str, Any], client: httpx.Client, waiting: _Waiting) -> Any:
    for attempt in range(1, waiting.retry.attempts + 1):
        try:
            response = client.post(INFO_URL, json=payload, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as error:
            transient = error.response.status_code == TOO_MANY or error.response.status_code >= 500
            if not transient or attempt == waiting.retry.attempts:
                raise VenueUnavailable(f"{payload['type']}: {error}") from error
        except httpx.TransportError as error:
            if attempt == waiting.retry.attempts:
                raise VenueUnavailable(f"{payload['type']}: {error}") from error
        except httpx.HTTPError as error:
            raise VenueUnavailable(f"{payload['type']}: {error}") from error
        except ValueError as error:  # the body was not JSON
            raise VenueUnavailable(f"{payload['type']}: response was not JSON") from error
        waiting.before_attempt(attempt)
    raise VenueUnavailable(f"{payload['type']}: out of attempts")


def fills(address: str, client: httpx.Client, *, retry: Retry | None = None) -> list[Fill]:
    """The trader's recent public fills, oldest first as the venue returns them."""
    return _recent(address, client, _Waiting(retry or Retry()))


def _recent(address: str, client: httpx.Client, waiting: _Waiting) -> list[Fill]:
    """The venue's own most recent page: at most `PAGE_SIZE` fills, ending now.

    This is the cheap read. It answers the question outright for a sparse trader, and for a
    dense one it measures the rate that sizes every heavy read that follows.
    """
    body = _post({"type": "userFills", "user": address}, client, waiting)
    if not isinstance(body, list):
        raise VenueUnavailable("userFills: expected a list of fills")
    return _as_fills(body, "userFills")


def _as_fills(rows: list[Any], what: str) -> list[Fill]:
    try:
        return [
            Fill(
                coin=str(row["coin"]),
                price=Decimal(str(row["px"])),
                size=Decimal(str(row["sz"])),
                time_ms=int(row["time"]),
                took_liquidity=bool(row["crossed"]),
            )
            for row in rows
        ]
    except (KeyError, TypeError, ValueError, InvalidOperation) as error:
        raise VenueUnavailable(f"{what}: unexpected shape ({error})") from error


def fills_since(
    address: str,
    days: int,
    client: httpx.Client,
    *,
    now_ms: int | None = None,
    retry: Retry | None = None,
) -> FillWindow:
    """The trader's public fills over the last `days`, read **backwards from now**.

    The venue answers ascending and at most a page at a time, so a range denser than the read
    budget yields its *oldest* part — the half that cannot answer "can my members copy this
    trader now". Reading backwards inverts what a cut-short read loses: it drops the oldest
    fills, and **the window it keeps always ends at `now`**. That is the property, not the
    report of it.
    """
    now = now_ms if now_ms is not None else int(time.time() * 1000)
    asked_from = now - days * _MS_PER_DAY
    waiting = _Waiting(retry or Retry())

    probe = _recent(address, client, waiting)
    oldest_probed = min((f.time_ms for f in probe), default=now)

    # The venue's own page already reaches past the start of the window: the question is
    # answered outright, and not one heavy read was spent on it.
    if len(probe) < PAGE_SIZE or oldest_probed <= asked_from:
        kept = tuple(f for f in probe if f.time_ms >= asked_from)
        return FillWindow(kept, Decimal(days), True, asked_from, now, waiting.waits, 0)

    # Dense enough that a page does not reach back far. A page spans `now - oldest_probed`, so
    # that is the trader's recent rate, and chunks are cut from it.
    chunk_ms = max((now - oldest_probed) // _CHUNK_LOAD, 1)
    held: list[Fill] = []
    covered_from = now
    budget = MAX_PAGES
    end = now

    while end >= asked_from and budget > 0:
        start = max(asked_from, end - chunk_ms + 1)
        chunk, whole, spent = _read_range(address, start, end, client, waiting, budget)
        budget -= spent
        if not whole:
            # The chunk ran out of budget part way, so its newest end is missing. Joining it
            # to what is already held would leave a hole in the middle of the window and no
            # figure drawn from it would mean anything. Dropped, and the window stops here.
            break
        held = chunk + held
        covered_from = start
        end = start - 1
        chunk_ms = _resize(chunk_ms, len(chunk), spent)

    return FillWindow(
        tuple(held),
        Decimal(days),
        covered_from <= asked_from,
        covered_from,
        now,
        waiting.waits,
        MAX_PAGES - budget,
    )


def _resize(chunk_ms: int, got: int, spent: int) -> int:
    """The next chunk's span, from what this one actually held.

    A chunk that came back near-empty means the read has walked past the burst the probe
    measured and is now crossing quiet ground at a step cut for the spike — which is how a
    budget gets spent on hours. A chunk that needed more than one read means the opposite,
    and is cut back by what it overran.
    """
    if spent > 1:
        return max(chunk_ms // spent, 1)
    target = PAGE_SIZE // _CHUNK_LOAD
    if got >= target:
        return chunk_ms
    return chunk_ms * min(_MAX_GROWTH, max(2, target // max(got, 1)))


def _read_range(
    address: str,
    start_ms: int,
    end_ms: int,
    client: httpx.Client,
    waiting: _Waiting,
    budget: int,
) -> tuple[list[Fill], bool, int]:
    """Pages ascending through `[start_ms, end_ms]` until the range is exhausted.

    Returns the fills, whether the range was read **to its end**, and how many heavy reads it
    spent. A caller that gets `False` holds a prefix of the range, never the whole of it.
    """
    read: list[Fill] = []
    cursor = start_ms
    spent = 0
    while spent < budget:
        page = _fills_page(address, cursor, end_ms, client, waiting)
        spent += 1
        read.extend(page)
        if len(page) < PAGE_SIZE:
            return read, True, spent
        if page[0].time_ms == page[-1].time_ms:
            # A whole page inside one millisecond. Stepping to the next millisecond would
            # silently drop whatever else the venue holds at this one, leaving a hole in the
            # middle of a window reported as contiguous — and every rate drawn across it
            # would be wrong. No verdict from partial data (AGENTS.md).
            raise VenueUnavailable(
                f"userFillsByTime: {PAGE_SIZE} fills share millisecond {page[-1].time_ms}; "
                "the read cannot step past it without dropping some"
            )
        cursor = page[-1].time_ms + 1
    return read, False, spent


def _fills_page(
    address: str, start_ms: int, end_ms: int, client: httpx.Client, waiting: _Waiting
) -> list[Fill]:
    body = _post(
        {"type": "userFillsByTime", "user": address, "startTime": start_ms, "endTime": end_ms},
        client,
        waiting,
    )
    if not isinstance(body, list):
        raise VenueUnavailable("userFillsByTime: expected a list of fills")
    return _as_fills(body, "userFillsByTime")


def account_value(address: str, client: httpx.Client, *, retry: Retry | None = None) -> Decimal:
    """The trader's account value, from their public clearinghouse state."""
    body = _post(
        {"type": "clearinghouseState", "user": address}, client, _Waiting(retry or Retry())
    )
    try:
        return Decimal(str(body["marginSummary"]["accountValue"]))
    except (KeyError, TypeError, InvalidOperation) as error:
        raise VenueUnavailable(f"clearinghouseState: unexpected shape ({error})") from error


def client() -> httpx.Client:
    """An HTTP client for the venue. It carries no credential and cannot sign."""
    return httpx.Client(headers={"Content-Type": "application/json"})
