"""Backing off when the venue says "too many".

`operations.md` E1: never an automatic retry without analysing the side effects. Here they
are. **Idempotent** — a read of public fills over a fixed range; running it twice returns the
same fills and changes nothing at the venue. **Transient** — 429 is the one 4xx that says
"come back later" rather than "this will fail identically", and it is the only 4xx retried.
**Amplification** — one command, one user, and jitter so that two of them do not synchronise.
**Masking** — the number of waits is reported, so a retry that succeeds does not hide a
degradation (E4).
"""

from __future__ import annotations

import httpx
import pytest

from screening.venue import Retry, VenueUnavailable, account_value, fills_since

ADDRESS = "0x0000000000000000000000000000000000000001"


def recording_retry(**kwargs: object) -> tuple[Retry, list[float]]:
    slept: list[float] = []
    clock = [0.0]

    def sleep(seconds: float) -> None:
        slept.append(seconds)
        clock[0] += seconds

    return Retry(sleep=sleep, monotonic=lambda: clock[0], **kwargs), slept  # type: ignore[arg-type]


def answering(statuses: list[int], body: object) -> httpx.Client:
    def handler(_: httpx.Request) -> httpx.Response:
        status = statuses.pop(0) if statuses else 200
        return httpx.Response(status, json=body if status == 200 else {"error": "nope"})

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_it_waits_and_tries_again_when_the_venue_says_too_many() -> None:
    retry, slept = recording_retry()
    value = account_value(
        ADDRESS, answering([429, 429], {"marginSummary": {"accountValue": "10"}}), retry=retry
    )
    assert str(value) == "10"
    assert len(slept) == 2, "one wait per refusal"
    assert slept[1] > slept[0], "the wait grows"


def test_the_waits_are_not_all_the_same_length() -> None:
    """Jitter. Two commands started together must not retry in lockstep."""
    seen = set()
    for _ in range(8):
        retry, slept = recording_retry()
        account_value(
            ADDRESS, answering([429], {"marginSummary": {"accountValue": "10"}}), retry=retry
        )
        seen.add(round(slept[0], 6))
    assert len(seen) > 1, "every wait was identical: there is no jitter"


def test_it_does_not_retry_an_error_that_will_fail_identically() -> None:
    """A 400 is not transient. Retrying it is load with no chance of success."""
    retry, slept = recording_retry()
    with pytest.raises(VenueUnavailable):
        account_value(ADDRESS, answering([400, 400, 400, 400], {}), retry=retry)
    assert slept == [], "a 4xx that is not 429 must not be retried"


def test_it_gives_up_inside_its_budget_rather_than_hanging() -> None:
    retry, slept = recording_retry(attempts=99, budget_s=5.0)
    with pytest.raises(VenueUnavailable) as raised:
        account_value(ADDRESS, answering([429] * 99, {}), retry=retry)
    assert sum(slept) <= 5.0, "the total wait must stay inside the budget"
    assert "budget" in str(raised.value).lower(), "and say that is why it stopped"


def test_it_reports_how_many_times_it_waited() -> None:
    """A retry that succeeds hides a degradation unless it is counted (E4)."""
    retry, _ = recording_retry()
    body = [{"coin": "BTC", "px": "100", "sz": "1", "time": 1, "crossed": True}]
    window = fills_since(ADDRESS, days=30, client=answering([429, 429], body), retry=retry)
    assert window.waits == 2
