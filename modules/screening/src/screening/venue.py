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

#: How many pages we are willing to ask for. A trader busy enough to fill them all is one
#: whose window will be short, and `FillWindow.complete` is how the answer says so.
MAX_PAGES = 20

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
    body = _post({"type": "userFills", "user": address}, client, _Waiting(retry or Retry()))
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
    """The trader's public fills over the last `days`, paged.

    `userFills` returns only the most recent page, so the window it covers is set by the
    venue's cap rather than by the question — which makes any monthly figure derived from it
    an artefact. This asks for a window instead, and reports whether it reached the end of it.
    """
    now = now_ms if now_ms is not None else int(time.time() * 1000)
    asked_from = now - days * _MS_PER_DAY
    waiting = _Waiting(retry or Retry())

    read, complete, covered_ms = _read_ascending(address, asked_from, now, client, waiting)
    if complete:
        return FillWindow(tuple(read), Decimal(days), True, asked_from, now, waiting.waits)

    # The read was cut short. Paging ascends, so what it kept is the OLDEST part of the window
    # and what it dropped is the newest — the half that answers "can my members copy this
    # trader *now*". Read again over a window that ends now, sized to what the first pass got
    # through at this trader's rate.
    # The narrowed window can overflow too, for a trader dense enough. Its own completeness
    # flag is kept: dropping it is how a second-pass truncation came back as "complete".
    recent_from = now - max(covered_ms, _MS_PER_DAY)
    read, _, _ = _read_ascending(address, recent_from, now, client, waiting)
    # Incomplete either way: the window asked for was never covered. Whether the narrowed one
    # was is no longer load-bearing, because the answer now reports the dates of the fills it
    # actually holds rather than the range it requested.
    return FillWindow(tuple(read), Decimal(days), False, recent_from, now, waiting.waits)


def _read_ascending(
    address: str, start_ms: int, end_ms: int, client: httpx.Client, waiting: _Waiting
) -> tuple[list[Fill], bool, int]:
    """Pages forward from `start_ms`. Returns the fills, whether it reached the end of the
    range, and how much of it the read got through."""
    read: list[Fill] = []
    cursor = start_ms
    for _ in range(MAX_PAGES):
        page = _fills_page(address, cursor, end_ms, client, waiting)
        read.extend(page)
        if len(page) < PAGE_SIZE:
            return read, True, end_ms - start_ms
        cursor = page[-1].time_ms + 1
    return read, False, cursor - start_ms


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
