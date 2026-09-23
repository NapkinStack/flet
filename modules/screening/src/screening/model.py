"""The shapes this module reads and returns.

The venue's responses are typed here rather than by an SDK, because the SDK that would
type them can also sign (ADR-0002).
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

#: The venue refuses any order below this notional. Not ours to change (AGENTS.md).
MINIMUM_ORDER_USDC = Decimal(10)

#: What flet takes on a routed fill, capped by the venue (PDR-0001).
BUILDER_FEE_RATE = Decimal("0.001")

#: The venue's own taker fee at the base tier. A small copier pays no less than this.
VENUE_TAKER_FEE_RATE = Decimal("0.00045")

#: Share of a trader's orders a member should be able to place for the answer to be "yes".
COVERAGE_TARGET = Decimal("0.80")

#: More than this share of fills posted rather than taken and a copier arriving afterwards
#: reproduces less than half of what they are copying (PDR-0002).
UNREPRODUCIBLE_ALERT = Decimal("0.5")

#: Volume landing on this share of the window's days or fewer is a burst, not a month
#: (PDR-0002).
CONCENTRATION_ALERT = Decimal(1) / Decimal(3)

#: A cut-short window is extrapolated to a month by this factor before the answer says so.
EXTRAPOLATION_ALERT = Decimal(3)

#: And past this factor it stops being an answer. Live, a read of 2.4 hours was extrapolated
#: by 319 — a number with the shape of a measurement and the content of a guess (PDR-0002,
#: amended 2026-09-21).
EXTRAPOLATION_CEILING = Decimal(30)

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


class Ruling(StrEnum):
    """What the answer says on its first line. `NO VERDICT` is not here: it is the absence of
    a verdict, raised rather than returned (PDR-0002)."""

    COPYABLE = "COPYABLE"
    WITH_RESERVATIONS = "COPYABLE WITH RESERVATIONS"
    NOT_COPYABLE = "NOT COPYABLE"


@dataclass(frozen=True)
class Verdict:
    """The answer, with every figure it rests on. A verdict without its measurement is not
    an answer here (AGENTS.md)."""

    ruling: Ruling
    reservations: tuple[str, ...]
    """Named in the headline, in the order fees, reproducibility, concentration,
    extrapolation. Empty when the ruling is `COPYABLE`; still printed in full below when the
    ruling is `NOT_COPYABLE`, so an administrator learns why a trader is unsuitable twice
    over."""
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

    @property
    def copyable(self) -> bool:
        """Clears the venue's floor at this ticket. Reservations never make it false — a
        reservation is expensive, not impossible."""
        return self.ruling is not Ruling.NOT_COPYABLE


@dataclass(frozen=True)
class FillWindow:
    """What was actually read, and whether it is the window that was asked for.

    The venue returns at most a page of fills per call, so without this the observation window
    is whatever the cap happened to cover — and every monthly figure derived from it is an
    artefact of that cap rather than of the trader.

    **It always ends at the moment of the run.** The read walks backwards from now, so a
    window cut short by the read budget is missing its oldest days, never its newest: a
    trader who stopped a fortnight ago cannot read as current.
    """

    fills: tuple[Fill, ...]
    days_requested: Decimal
    complete: bool
    starts_at_ms: int
    ends_at_ms: int
    waits: int = 0
    """How many times the read backed off. A retry that succeeds hides a degradation unless
    it is counted (`operations.md` E4)."""

    reads: int = 0
    """How many heavy reads the venue was asked for. The venue meters by weight, so a figure
    the operator cannot see is a cost nobody is watching."""

    @property
    def first_fill_ms(self) -> int | None:
        """The oldest fill actually held. `starts_at_ms` is what was *asked for*, and the two
        diverge the moment a read is cut short — which is where every defect on this branch
        has lived."""
        return min((f.time_ms for f in self.fills), default=None)

    @property
    def last_fill_ms(self) -> int | None:
        return max((f.time_ms for f in self.fills), default=None)

    @property
    def calendar_days(self) -> int:
        """Whole days the fills it holds actually span. Never the range it requested."""
        if self.first_fill_ms is None or self.last_fill_ms is None:
            return 0
        return -(-(self.last_fill_ms - self.first_fill_ms) // 86_400_000)

    @property
    def days_covered(self) -> Decimal:
        """The span of the fills actually read. Zero when there are fewer than two."""
        if len(self.fills) < 2:
            return Decimal(0)
        span = max(f.time_ms for f in self.fills) - min(f.time_ms for f in self.fills)
        return Decimal(span) / Decimal(86_400_000)
