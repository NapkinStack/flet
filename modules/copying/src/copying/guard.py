"""The only way anything in flet acts for a member: after the venue says the agent lives."""

from collections.abc import Callable
from typing import Any

from eth_account import Account

from copying.store import Held, KeyStore
from copying.venue import Listing, Venue, listed


def alive(member: str, store: KeyStore, venue: Venue, now_ms: int) -> tuple[Held, Listing] | None:
    """The member's agent and the venue's listing of it, if listed and unexpired; else None.

    One question to the venue, no retry. NoAnswer propagates with the key kept: an unheard
    venue is not a revocation. A key the venue has stopped honouring is deleted.
    """
    held = store.get(member)
    if held is None:
        return None
    listing = listed(venue, member, held.agent.address)
    if listing is None or listing.valid_until_ms <= now_ms:
        if held.confirmed or held.agent.valid_until_ms <= now_ms or listing is not None:
            store.forget(member)
        return None
    if not held.confirmed:
        store.confirm(member)
    return held, listing


def act_for[T](
    member: str, store: KeyStore, venue: Venue, now_ms: int, action: Callable[[Any], T]
) -> T | None:
    """Runs `action` with the member's agent only if `alive` says so; otherwise nothing."""
    found = alive(member, store, venue, now_ms)
    if found is None:
        return None
    return action(Account.from_key(found[0].agent.private_key))
