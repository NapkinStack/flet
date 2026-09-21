"""The oracle for D3, written before the implementation and read against the cycle's
acceptance criteria (01-is-a-trader-copyable.md)."""

from __future__ import annotations

import time
from decimal import Decimal

import pytest

from screening.model import (
    EXTRAPOLATION_ALERT,
    FEE_BURDEN_ALERT,
    UNREPRODUCIBLE_ALERT,
    Fill,
    Ruling,
    Verdict,
)
from screening.verdict import assess

NOW_MS = int(time.time() * 1000)

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


# --- PDR-0002: three verdicts, not two ------------------------------------------------


def _fills(n: int, px: str = "1000", crossed: bool = True, day_span: int = 30) -> list[Fill]:
    """`n` fills spread evenly over `day_span` days, ending now."""
    step = max((day_span * 86_400_000) // max(n - 1, 1), 1)
    return [
        Fill(
            coin="BTC",
            price=Decimal(px),
            size=Decimal(1),
            time_ms=NOW_MS - (n - 1 - i) * step,
            took_liquidity=crossed,
        )
        for i in range(n)
    ]


def test_a_trader_who_clears_the_floor_and_trips_nothing_is_simply_copyable() -> None:
    v = assess(
        _fills(60), trader_account=Decimal(100_000), ticket=Decimal(50_000), window_days=Decimal(30)
    )
    assert v.ruling is Ruling.COPYABLE
    assert v.reservations == ()


def test_a_fee_burden_above_the_alert_is_a_reservation_not_a_refusal() -> None:
    """The defect PDR-0002 exists for: live, the command printed COPYABLE and exited 0
    directly above a line saying the fees would decide the member's result."""
    v = assess(
        _fills(4000),
        trader_account=Decimal(100_000),
        ticket=Decimal(50_000),
        window_days=Decimal(30),
    )
    assert v.monthly_fee_burden > FEE_BURDEN_ALERT
    assert v.ruling is Ruling.WITH_RESERVATIONS
    assert "fees" in v.reservations
    assert v.copyable is True, "a reservation is expensive, never impossible"


def test_more_than_half_the_fills_posted_is_a_reproducibility_reservation() -> None:
    fills = _fills(30, crossed=True) + _fills(40, crossed=False)
    v = assess(
        fills, trader_account=Decimal(100_000), ticket=Decimal(50_000), window_days=Decimal(30)
    )
    assert v.ruling is Ruling.WITH_RESERVATIONS
    assert "reproducibility" in v.reservations


def test_volume_on_a_third_of_the_days_or_fewer_is_a_concentration_reservation() -> None:
    v = assess(
        _fills(60, day_span=3),
        trader_account=Decimal(100_000),
        ticket=Decimal(50_000),
        window_days=Decimal(30),
    )
    assert v.days_traded <= 10
    assert v.ruling is Ruling.WITH_RESERVATIONS
    assert "concentration" in v.reservations


def test_the_floor_beats_every_reservation() -> None:
    """Impossible beats expensive: a trader whose orders cannot be placed is NOT COPYABLE
    whatever else is true, and the reservations are still printed below."""
    v = assess(
        _fills(4000),
        trader_account=Decimal(100_000),
        ticket=Decimal(100),
        window_days=Decimal(30),
    )
    assert v.refused_share > Decimal("0.2")
    assert v.ruling is Ruling.NOT_COPYABLE
    assert v.copyable is False
    assert v.reservations, "still named, so the administrator learns it twice over"


def test_a_window_stretched_past_the_ceiling_is_no_verdict_at_all() -> None:
    """A read of 2.4 hours extrapolated to a month by 319 has the shape of a measurement and
    the content of a guess. Past the ceiling the command refuses rather than answering."""
    with pytest.raises(ValueError, match="guess, not a figure"):
        assess(
            _fills(60, day_span=0),
            trader_account=Decimal(100_000),
            ticket=Decimal(50_000),
            window_days=Decimal(30),
            window_complete=False,
        )


def test_a_window_stretched_past_the_alert_is_only_a_reservation() -> None:
    v = assess(
        _fills(60, day_span=5),
        trader_account=Decimal(100_000),
        ticket=Decimal(50_000),
        window_days=Decimal(30),
        window_complete=False,
    )
    assert "extrapolation" in v.reservations
    assert v.ruling is Ruling.WITH_RESERVATIONS, "short is a caveat, absurd is no verdict"


# --- the thresholds, defended ---------------------------------------------------------


def test_each_threshold_falls_on_the_side_the_decision_says() -> None:
    """A verifier checked all five boundaries by hand, found the code right, and found six
    mutants flipping `>` to `>=` that the suite let through. The wording is the contract:
    fees *above* the alert, *more than half* posted, a third *or less* of the days, *more
    than* 3x stretched."""
    from screening.verdict import _reservations

    tiny = Decimal("0.0000001")

    def at(
        *,
        fee: Decimal = FEE_BURDEN_ALERT,
        posted: Decimal = UNREPRODUCIBLE_ALERT,
        traded: int = 11,
        stretch: Decimal = EXTRAPOLATION_ALERT,
    ) -> tuple[str, ...]:
        return _reservations(
            monthly_fee_burden=fee,
            unreproducible_share=posted,
            days_traded=traded,
            calendar_days=30,
            stretch=stretch,
        )

    assert at() == (), "exactly at every threshold trips nothing"
    assert "fees" in at(fee=FEE_BURDEN_ALERT + tiny)
    assert "reproducibility" in at(posted=UNREPRODUCIBLE_ALERT + tiny)
    assert "extrapolation" in at(stretch=EXTRAPOLATION_ALERT + tiny)
    # Concentration is the one stated the other way round — `a third OR LESS` — so exactly a
    # third fires, and one day more does not.
    assert "concentration" in at(traded=10)
    assert at(traded=11) == ()


def test_the_ceiling_is_past_thirty_not_at_it() -> None:
    """`Past 30x` in the amendment. Exactly a day of a thirty-day window is a reservation;
    a hair less is no verdict."""
    day = 86_400_000
    at = [
        Fill(coin="BTC", price=Decimal(1000), size=Decimal(1), time_ms=t, took_liquidity=True)
        for t in (NOW_MS - day, NOW_MS)
    ]
    v = assess(
        at,
        trader_account=Decimal(100_000),
        ticket=Decimal(50_000),
        window_complete=False,
        window_asked_days=Decimal(30),
    )
    assert "extrapolation" in v.reservations
    assert v.ruling is Ruling.WITH_RESERVATIONS, "exactly 30x is still an answer"

    past = [
        Fill(coin="BTC", price=Decimal(1000), size=Decimal(1), time_ms=t, took_liquidity=True)
        for t in (NOW_MS - day + 1, NOW_MS)
    ]
    with pytest.raises(ValueError, match="guess, not a figure"):
        assess(
            past,
            trader_account=Decimal(100_000),
            ticket=Decimal(50_000),
            window_complete=False,
            window_asked_days=Decimal(30),
        )


def test_days_traded_is_clamped_to_the_window_it_is_counted_against() -> None:
    """UTC day buckets: fills every twelve hours across exactly thirty days fall into
    thirty-one buckets, and the command printed `traded on 31 of the 30 days read`."""
    half = 43_200_000
    fills = [
        Fill(
            coin="BTC",
            price=Decimal(1000),
            size=Decimal(1),
            time_ms=NOW_MS - i * half,
            took_liquidity=True,
        )
        for i in range(61)
    ]
    v = assess(
        fills, trader_account=Decimal(100_000), ticket=Decimal(50_000), window_days=Decimal(30)
    )
    assert v.days_traded <= v.calendar_days, "an impossible sentence, and it was printed"
    assert f"{v.days_traded} of the {v.calendar_days}" in " ".join(v.reasons)


def test_the_reservations_come_out_in_the_order_the_decision_fixes() -> None:
    """`all are named, in the order fees, reproducibility, concentration` (PDR-0002), plus
    extrapolation from the amendment. Swapping two of them, or moving fees to the end, left
    all sixty-five tests green — and the test named for the first line was satisfied by any
    order, because its fixture tripped only one reservation."""
    from screening.verdict import _reservations

    assert _reservations(
        monthly_fee_burden=Decimal("0.9"),
        unreproducible_share=Decimal("0.9"),
        days_traded=1,
        calendar_days=30,
        stretch=Decimal(20),
    ) == ("fees", "reproducibility", "concentration", "extrapolation")


def test_the_floor_boundary_is_the_coverage_target_exactly() -> None:
    """D3 made this line the sole gate for `NOT COPYABLE` and for exit 2, and nothing pinned
    which side of it exactly-20%-refused falls on."""
    trader_account, ticket = Decimal(100_000), Decimal(1_000)
    # scale 1/100: a 900 notional becomes 9 USDC (refused), a 2000 becomes 20 (placed)
    at_target = spread([fill("900")] * 2 + [fill("2000")] * 8)
    assert assess(at_target, trader_account=trader_account, ticket=ticket).copyable is True

    past = spread([fill("900")] * 3 + [fill("2000")] * 7)
    assert assess(past, trader_account=trader_account, ticket=ticket).copyable is False
