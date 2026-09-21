"""The venue layer answers from the public endpoint, or says it cannot."""

from __future__ import annotations

import json
from decimal import Decimal

import httpx
import pytest

from screening.venue import Retry, VenueUnavailable, account_value, fills

ADDRESS = "0x0000000000000000000000000000000000000001"

#: These tests assert what happens when a read fails, not how long it waits first.
NO_WAITING = Retry(attempts=1)


def client_returning(payload: object, status: int = 200) -> httpx.Client:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(status, content=json.dumps(payload))

    return httpx.Client(transport=httpx.MockTransport(handler))


def client_that_fails() -> httpx.Client:
    def handler(_: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("no route to host")

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_it_reads_public_fills() -> None:
    payload = [
        {"coin": "BTC", "px": "81058.0", "sz": "0.26", "time": 1789920498800, "crossed": True},
        {"coin": "BTC", "px": "81100.0", "sz": "0.10", "time": 1789920499900, "crossed": False},
    ]
    got = fills(ADDRESS, client_returning(payload))
    assert [f.took_liquidity for f in got] == [True, False]
    assert got[0].notional == Decimal("81058.0") * Decimal("0.26")


def test_it_reads_the_account_value() -> None:
    payload = {"marginSummary": {"accountValue": "316746.42"}}
    assert account_value(ADDRESS, client_returning(payload)) == Decimal("316746.42")


def test_it_says_so_when_the_venue_is_unreachable() -> None:
    """No verdict from stale or partial data — it says so and returns nothing."""
    with pytest.raises(VenueUnavailable):
        fills(ADDRESS, client_that_fails(), retry=NO_WAITING)
    with pytest.raises(VenueUnavailable):
        account_value(ADDRESS, client_that_fails(), retry=NO_WAITING)


def test_it_says_so_when_the_venue_answers_with_an_error() -> None:
    with pytest.raises(VenueUnavailable):
        fills(ADDRESS, client_returning({"error": "nope"}, status=500), retry=NO_WAITING)


def test_it_says_so_when_the_shape_is_not_what_we_typed() -> None:
    """The responses are typed by us, so a breaking change is ours to notice (ADR-0002)."""
    with pytest.raises(VenueUnavailable):
        account_value(ADDRESS, client_returning({"unexpected": True}))
