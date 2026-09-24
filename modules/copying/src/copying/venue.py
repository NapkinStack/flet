"""What the venue says about a member's agents. It is the record; flet's state is a cache."""

from dataclasses import dataclass
from typing import Any, Protocol


class NoAnswer(Exception):
    """The venue did not answer usably. Never to be read as "not listed"."""


class Venue(Protocol):
    def extra_agents(self, user: str) -> Any: ...


@dataclass(frozen=True)
class Listing:
    address: str
    name: str
    valid_until_ms: int


def listed(venue: Venue, member: str, agent_address: str) -> Listing | None:
    """Our agent as the venue lists it under the member's main address, or None."""
    try:
        answer = venue.extra_agents(member)
    except Exception as e:  # any failure to hear the venue is no answer, never an absence
        raise NoAnswer(type(e).__name__) from None
    if not isinstance(answer, list):
        raise NoAnswer("malformed answer")
    for entry in answer:
        if not (
            isinstance(entry, dict)
            and isinstance(entry.get("address"), str)
            and isinstance(entry.get("name"), str)
            and isinstance(entry.get("validUntil"), int)
        ):
            raise NoAnswer("malformed answer")
        if entry["address"].lower() == agent_address.lower():
            return Listing(entry["address"], entry["name"], entry["validUntil"])
    return None
