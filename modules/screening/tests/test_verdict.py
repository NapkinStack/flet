"""The oracle for D3, written before the implementation and read against the cycle's
acceptance criteria (01-is-a-trader-copyable.md)."""

from __future__ import annotations

from decimal import Decimal

import pytest

from screening.model import Fill, Verdict
from screening.verdict import assess

DAY_MS = 86_400_000


def fill(notional: str, *, took_liquidity: bool = True, day: int = 0) -> Fill:
    return Fill(
        coin="BTC",
        price=Decimal(notional),
        size=Decimal(1),
        time_ms=day * DAY_MS,
        took_liquidity=took_liquidity,
    )


def spread(fills: list[Fill], days: int = 30) -> list[Fill]:
    """Stamp fills across a window so turnover is defined."""
    return [
        Fill(f.coin, f.price, f.size, i * DAY_MS * days // max(len(fills) - 1, 1), f.took_liquidity)
        for i, f in enumerate(fills)
    ]


def test_it_answers_from_the_traders_real_fills() -> None:
    """Given a trader's fills and a member ticket, the answer states whether the trader is
    copyable and carries the figures it rests on."""
    trader = spread([fill("2000")] * 20)
    v = assess(trader, trader_account=Decimal(20_000), ticket=Decimal(2_000))
    assert isinstance(v, Verdict)
    assert v.copyable is True
    assert v.fills_read == 20
    assert v.reasons, "a verdict without a stated reason is not an answer"


def test_it_refuses_a_trader_whose_orders_fall_under_the_floor() -> None:
    """A member at 500 EUR copying a 300k account scales every order by 1/600. A typical
    2,000 USDC order becomes 3.33 USDC, under the venue's 10 USDC floor."""
    trader = spread([fill("2000")] * 20)
    v = assess(trader, trader_account=Decimal(300_000), ticket=Decimal(500))
    assert v.copyable is False
    assert v.refused_share == Decimal(1), "every order is under the floor at this ticket"
    assert any("10" in r for r in v.reasons), "the reason must name the floor"


def test_it_states_the_refused_share_when_only_some_orders_are_too_small() -> None:
    trader = spread([fill("100")] * 10 + [fill("10000")] * 10)
    v = assess(trader, trader_account=Decimal(100_000), ticket=Decimal(1_000))
    # scale 1/100: the 100 USDC orders become 1 USDC (refused), the 10k become 100 (placed)
    assert v.refused_share == Decimal("0.5")


def test_it_states_the_fee_burden_as_a_monthly_percentage() -> None:
    """Turnover 10x a month at 0.1% builder + 0.045% venue costs the member 1.45% a month."""
    trader = spread([fill("10000")] * 10)  # 100k of volume on a 10k account over 30 days
    v = assess(trader, trader_account=Decimal(10_000), ticket=Decimal(2_000))
    assert v.monthly_turnover == pytest.approx(Decimal(10), rel=Decimal("0.01"))
    assert v.monthly_fee_burden == pytest.approx(Decimal("0.0145"), rel=Decimal("0.01"))


def test_it_calls_out_a_fee_burden_above_five_percent() -> None:
    trader = spread([fill("100000")] * 10)  # 1M of volume on a 10k account: turnover 100x
    v = assess(trader, trader_account=Decimal(10_000), ticket=Decimal(2_000))
    assert v.monthly_fee_burden > Decimal("0.05")
    assert any("%" in r for r in v.reasons), "the cost must be stated, not hidden behind a verdict"


def test_it_states_the_share_a_copier_could_not_reproduce() -> None:
    """A fill the trader POSTED was executed when the market reached it. A copier arriving
    afterwards cannot reproduce it."""
    trader = spread([fill("2000", took_liquidity=False)] * 6 + [fill("2000")] * 4)
    v = assess(trader, trader_account=Decimal(20_000), ticket=Decimal(2_000))
    assert v.unreproducible_share == Decimal("0.6")


def test_it_reports_the_minimum_ticket_that_would_work() -> None:
    """The ticket needed to place 80% of this trader's orders."""
    trader = spread([fill("1000")] * 2 + [fill("5000")] * 8)
    v = assess(trader, trader_account=Decimal(100_000), ticket=Decimal(500))
    # 80% coverage means clearing the floor on the 8 orders of 5,000: 10 / (5000/100000)
    assert v.minimum_ticket == pytest.approx(Decimal(200), rel=Decimal("0.01"))


def test_it_refuses_to_answer_without_fills() -> None:
    """No verdict from partial data (AGENTS.md)."""
    with pytest.raises(ValueError):
        assess([], trader_account=Decimal(20_000), ticket=Decimal(2_000))
