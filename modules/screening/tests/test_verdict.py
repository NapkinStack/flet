"""The oracle for D3, written before the implementation and read against the cycle's
acceptance criteria (01-is-a-trader-copyable.md)."""

from __future__ import annotations

from decimal import Decimal

import pytest

from screening.model import Fill, Verdict
from screening.verdict import assess

DAY_MS = 86_400_000


def fill(notional: str, *, took_liquidity: bool = True, day: int = 0) -> Fill:
    """A fill of `notional`, stamped on `day` of the window."""
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


def test_it_marks_a_monthly_figure_extrapolated_from_an_incomplete_window() -> None:
    """When the venue's page cap stopped us short, the monthly figure is an extrapolation and
    the answer must say so rather than present it as a measurement."""
    trader = spread([fill("10000")] * 10, days=3)
    v = assess(trader, trader_account=Decimal(10_000), ticket=Decimal(2_000), window_complete=False)
    assert v.window_complete is False
    assert any("extrapolat" in r.lower() for r in v.reasons), (
        "an extrapolated figure must be named as one"
    )


def test_it_counts_the_days_the_trader_actually_traded() -> None:
    """A month's volume in one burst is not a month of trading, and the difference is what
    decides whether the monthly cost above means anything about tomorrow."""
    burst = [fill("10000", day=0) for _ in range(20)]
    v = assess(
        [*burst, fill("10000", day=29)],
        trader_account=Decimal(100_000),
        ticket=Decimal(5_000),
    )
    assert v.days_traded == 2, "two calendar days carried the whole window"


def test_it_says_when_a_month_of_volume_landed_in_a_handful_of_days() -> None:
    """The figure is right about the past and understates the future. Say so, with the factor."""
    burst = [fill("50000", day=0) for _ in range(30)]
    v = assess(
        burst, trader_account=Decimal(100_000), ticket=Decimal(5_000), window_days=Decimal(30)
    )
    assert v.days_traded == 1
    joined = " ".join(v.reasons).lower()
    assert "1 of the 30" in joined or "1 day" in joined, "the concentration must be stated"
    assert "understate" in joined, "and named as an understatement, since it runs toward yes"


def test_it_does_not_cry_concentration_for_a_trader_spread_across_the_month() -> None:
    spread_out = [fill("10000", day=d) for d in range(0, 30)]
    v = assess(
        spread_out, trader_account=Decimal(100_000), ticket=Decimal(5_000), window_days=Decimal(30)
    )
    assert v.days_traded == 30
    assert not any("understate" in r.lower() for r in v.reasons)


def test_days_traded_never_exceeds_the_days_it_is_counted_against() -> None:
    """`traded on 18 of the 17 days read` is an impossible sentence, and it was printed."""
    fills = [fill("10000", day=d) for d in range(0, 18)]
    v = assess(fills, trader_account=Decimal(100_000), ticket=Decimal(5_000))
    said = " ".join(v.reasons)
    assert v.days_traded <= v.calendar_days, "a day traded is a day in the window"
    assert f"{v.days_traded} of the {v.calendar_days}" in said


def test_it_always_states_the_concentration_factor_without_a_cliff() -> None:
    """A threshold on a continuous quantity is a cliff: 10 days of 30 warned, 11 did not, and
    a 2.7x understatement passed unnamed."""
    eleven = [fill("10000", day=d) for d in range(0, 11)] + [fill("1", day=29)]
    v = assess(
        eleven, trader_account=Decimal(100_000), ticket=Decimal(5_000), window_days=Decimal(30)
    )
    assert any("x" in r and "understate" in r.lower() for r in v.reasons), (
        "the factor is stated for every trader, not only past a threshold"
    )
