"""Turn a trader's public fills into an answer about one member's ticket.

Copyability is arithmetic, not merit (ADR-0001). Nothing here ranks a trader.
"""

from __future__ import annotations

from collections.abc import Sequence
from decimal import Decimal

from screening.model import (
    BUILDER_FEE_RATE,
    COVERAGE_TARGET,
    FEE_BURDEN_ALERT,
    MINIMUM_ORDER_USDC,
    VENUE_TAKER_FEE_RATE,
    Fill,
    Verdict,
)

_MS_PER_DAY = Decimal(86_400_000)
_DAYS_PER_MONTH = Decimal(30)


def assess(fills: Sequence[Fill], trader_account: Decimal, ticket: Decimal) -> Verdict:
    """Can a member holding `ticket` copy this trader, and at what cost?

    Raises:
        ValueError: when the fills cannot support a verdict. No verdict from partial data.
    """
    if not fills:
        raise ValueError("no fills: a verdict cannot be given without the trader's executions")
    if trader_account <= 0:
        raise ValueError("the trader's account value must be positive")
    if ticket <= 0:
        raise ValueError("the member's ticket must be positive")

    days = (Decimal(max(f.time_ms for f in fills) - min(f.time_ms for f in fills))) / _MS_PER_DAY
    if days <= 0:
        raise ValueError("the fills span no time: a monthly turnover cannot be computed from them")

    count = Decimal(len(fills))
    scale = ticket / trader_account
    notionals = sorted(f.notional for f in fills)

    refused = sum(1 for n in notionals if n * scale < MINIMUM_ORDER_USDC)
    refused_share = Decimal(refused) / count
    posted = sum(1 for f in fills if not f.took_liquidity)
    unreproducible_share = Decimal(posted) / count

    monthly_volume = sum(notionals, Decimal(0)) * _DAYS_PER_MONTH / days
    monthly_turnover = monthly_volume / trader_account
    monthly_fee_burden = monthly_turnover * (BUILDER_FEE_RATE + VENUE_TAKER_FEE_RATE)

    # The ticket that clears the floor on COVERAGE_TARGET of the orders: the smallest
    # (1 - COVERAGE_TARGET) may be refused.
    cutoff = notionals[int((Decimal(1) - COVERAGE_TARGET) * count)]
    minimum_ticket = MINIMUM_ORDER_USDC / (cutoff / trader_account)

    copyable = refused_share <= Decimal(1) - COVERAGE_TARGET

    return Verdict(
        copyable=copyable,
        ticket=ticket,
        trader_account=trader_account,
        fills_read=len(fills),
        days_observed=days,
        refused_share=refused_share,
        unreproducible_share=unreproducible_share,
        monthly_turnover=monthly_turnover,
        monthly_fee_burden=monthly_fee_burden,
        minimum_ticket=minimum_ticket,
        reasons=_reasons(
            copyable=copyable,
            ticket=ticket,
            refused_share=refused_share,
            unreproducible_share=unreproducible_share,
            monthly_turnover=monthly_turnover,
            monthly_fee_burden=monthly_fee_burden,
            minimum_ticket=minimum_ticket,
        ),
    )


def _reasons(
    *,
    copyable: bool,
    ticket: Decimal,
    refused_share: Decimal,
    unreproducible_share: Decimal,
    monthly_turnover: Decimal,
    monthly_fee_burden: Decimal,
    minimum_ticket: Decimal,
) -> tuple[str, ...]:
    """Every figure the verdict rests on, stated. A verdict without its measurement is not
    an answer here (AGENTS.md)."""
    said: list[str] = []

    if refused_share > 0:
        said.append(
            f"{refused_share:.0%} of this trader's orders fall under the venue's "
            f"{MINIMUM_ORDER_USDC} USDC floor once scaled to a {ticket:,.0f} ticket, "
            f"and cannot be placed at all"
        )
    else:
        said.append(
            f"every order clears the venue's {MINIMUM_ORDER_USDC} USDC floor at this ticket"
        )

    if not copyable:
        said.append(
            f"a ticket of about {minimum_ticket:,.0f} would place {COVERAGE_TARGET:.0%} of them"
        )

    said.append(
        f"turnover {monthly_turnover:,.1f}x a month costs the member {monthly_fee_burden:.2%} "
        f"of their ticket per month in fees, of which flet takes "
        f"{monthly_turnover * BUILDER_FEE_RATE:.2%}"
    )
    if monthly_fee_burden > FEE_BURDEN_ALERT:
        said.append(
            f"that is above {FEE_BURDEN_ALERT:.0%} a month: the fees, not the strategy, "
            f"will decide this member's result"
        )

    if unreproducible_share > 0:
        said.append(
            f"{unreproducible_share:.0%} of the fills were posted rather than taken: a copier "
            f"arriving afterwards cannot reproduce them"
        )

    return tuple(said)
