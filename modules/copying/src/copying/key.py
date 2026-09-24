"""A member's agent: a fresh key pair flet generates, which the member approves on the venue."""

import re
from dataclasses import dataclass, field

from eth_account import Account

# The decider, 2026-09-24: 30 days, well under the venue's 180-day ceiling (ADR-0001).
LIFETIME_MS = 30 * 24 * 3600 * 1000

_ADDRESS = re.compile(r"0x[0-9a-f]{40}")


@dataclass(frozen=True)
class Agent:
    address: str
    valid_until_ms: int
    private_key: str = field(repr=False)

    @property
    def name(self) -> str:
        """What the member types on the venue's API page; the venue reads the expiry from it."""
        return f"flet valid_until {self.valid_until_ms}"


def new_agent(now_ms: int, lifetime_ms: int = LIFETIME_MS) -> Agent:
    """Always a fresh address: a deregistered agent's old signatures may be replayable."""
    account = Account.create()
    return Agent(account.address, now_ms + lifetime_ms, account.key.hex())


def member_address(raw: str) -> str:
    """A member's main address, lower-cased; anything else is refused before any use."""
    address = raw.lower()
    if not _ADDRESS.fullmatch(address):
        raise ValueError("not an address")
    return address
