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
    calendar_days: int
    """Whole days the window covers. `days_traded` is counted against this so the two cannot
    contradict each other — `traded on 18 of the 17 days read` was printed before they did."""
    days_traded: int
    """Calendar days on which the trader actually traded. A month's volume in one burst is
    not a month of trading, and the monthly figures below average over the window either
    way — which understates what the next month would cost."""
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
    window_complete: bool
    """False when the venue's page cap stopped the read short of the window asked for, so the
    monthly figures above are extrapolated from less than that window."""
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class FillWindow:
    """What was actually read, and whether it is the window that was asked for.

    The venue returns at most a page of fills per call, so without this the observation window
    is whatever the cap happened to cover — and every monthly figure derived from it is an
    artefact of that cap rather than of the trader.
    """

    fills: tuple[Fill, ...]
    days_requested: Decimal
    complete: bool
    starts_at_ms: int
    ends_at_ms: int
    waits: int = 0
    """How many times the read backed off. A retry that succeeds hides a degradation unless
    it is counted (`operations.md` E4)."""
    """The window actually read. When the read is cut short this is a **recent** window, not
    the stale front of the one asked for — a trader who stopped a fortnight ago must not read
    as current."""

    @property
    def calendar_days(self) -> int:
        return -(-(self.ends_at_ms - self.starts_at_ms) // 86_400_000)

    @property
    def days_covered(self) -> Decimal:
        """The span of the fills actually read. Zero when there are fewer than two."""
        if len(self.fills) < 2:
            return Decimal(0)
        span = max(f.time_ms for f in self.fills) - min(f.time_ms for f in self.fills)
        return Decimal(span) / Decimal(86_400_000)
