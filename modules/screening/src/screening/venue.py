"""Read-only access to the venue's public endpoint.

An HTTP client, never an SDK that can sign (ADR-0002). Nothing here authenticates, and the
responses are typed by us, so a breaking change is ours to notice.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

import httpx

from screening.model import Fill

INFO_URL = "https://api.hyperliquid.xyz/info"
TIMEOUT_SECONDS = 20.0


class VenueUnavailable(RuntimeError):
    """The venue could not be read, or did not answer in the shape we type.

    No verdict follows from partial or stale data (AGENTS.md).
    """


def _post(payload: dict[str, str], client: httpx.Client) -> Any:
    try:
        response = client.post(INFO_URL, json=payload, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as error:
        raise VenueUnavailable(f"{payload['type']}: {error}") from error
    except ValueError as error:  # the body was not JSON
        raise VenueUnavailable(f"{payload['type']}: response was not JSON") from error


def fills(address: str, client: httpx.Client) -> list[Fill]:
    """The trader's recent public fills, oldest first as the venue returns them."""
    body = _post({"type": "userFills", "user": address}, client)
    if not isinstance(body, list):
        raise VenueUnavailable("userFills: expected a list of fills")
    try:
        return [
            Fill(
                coin=str(row["coin"]),
                price=Decimal(str(row["px"])),
                size=Decimal(str(row["sz"])),
                time_ms=int(row["time"]),
                took_liquidity=bool(row["crossed"]),
            )
            for row in body
        ]
    except (KeyError, TypeError, ValueError, InvalidOperation) as error:
        raise VenueUnavailable(f"userFills: unexpected shape ({error})") from error


def account_value(address: str, client: httpx.Client) -> Decimal:
    """The trader's account value, from their public clearinghouse state."""
    body = _post({"type": "clearinghouseState", "user": address}, client)
    try:
        return Decimal(str(body["marginSummary"]["accountValue"]))
    except (KeyError, TypeError, InvalidOperation) as error:
        raise VenueUnavailable(f"clearinghouseState: unexpected shape ({error})") from error


def client() -> httpx.Client:
    """An HTTP client for the venue. It carries no credential and cannot sign."""
    return httpx.Client(headers={"Content-Type": "application/json"})
