"""The shapes this module reads and returns.

The venue's responses are typed here rather than by an SDK, because the SDK that would
type them can also sign (ADR-0002).
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

#: The venue refuses any order below this notional. Not ours to change (AGENTS.md).
MINIMUM_ORDER_USDC = Decimal(10)

#: What flet takes on a routed fill, capped by the venue (PDR-0001).
BUILDER_FEE_RATE = Decimal("0.001")

#: The venue's own taker fee at the base tier. A small copier pays no less than this.
VENUE_TAKER_FEE_RATE = Decimal("0.00045")

#: Share of a trader's orders a member should be able to place for the answer to be "yes".
COVERAGE_TARGET = Decimal("0.80")

#: Above this monthly cost, the fee burden is called out rather than merely stated.
FEE_BURDEN_ALERT = Decimal("0.05")


@dataclass(frozen=True)
class Fill:
    """One execution of the trader, as the venue reports it publicly."""

    coin: str
    price: Decimal
    size: Decimal
    time_ms: int
    took_liquidity: bool
    """The venue's `crossed`. False means the trader POSTED the order and the market came to
    it — a copier arriving afterwards cannot reproduce that fill at all."""

    @property
    def notional(self) -> Decimal:
        return self.price * self.size


@dataclass(frozen=True)
class Verdict:
    """The answer, with every figure it rests on. A verdict without its measurement is not
    an answer here (AGENTS.md)."""

    copyable: bool
    ticket: Decimal
    trader_account: Decimal
    fills_read: int
    days_observed: Decimal
    refused_share: Decimal
    """Share of the trader's orders that would fall under the venue's floor at this ticket."""
    unreproducible_share: Decimal
    """Share of fills where the trader posted liquidity. A copier cannot reproduce these."""
    monthly_turnover: Decimal
    """Monthly volume divided by the trader's account."""
    monthly_fee_burden: Decimal
    """What copying costs the member per month, as a share of their ticket."""
    minimum_ticket: Decimal
    """The ticket needed to place COVERAGE_TARGET of this trader's orders."""
    reasons: tuple[str, ...]
