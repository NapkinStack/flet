"""The command an administrator actually runs."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

from screening.cli import main

ADDRESS = "0x102d1d1a6240581a809bac9b9b4dff2eafe8c058"
DAY_MS = 86_400_000


def venue(fills: list[dict[str, Any]], account: str) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        kind = json.loads(request.content)["type"]
        if kind == "userFills":
            return httpx.Response(200, json=fills)
        return httpx.Response(200, json={"marginSummary": {"accountValue": account}})

    return httpx.Client(transport=httpx.MockTransport(handler))


def a_fill(px: str, day: int, crossed: bool = True) -> dict[str, Any]:
    return {"coin": "BTC", "px": px, "sz": "1", "time": day * DAY_MS, "crossed": crossed}


def test_it_answers_for_a_copyable_trader(capsys: pytest.CaptureFixture[str]) -> None:
    rows = [a_fill("2000", day) for day in range(0, 30)]
    code = main([ADDRESS, "--ticket", "2000"], client=venue(rows, "20000"))
    out = capsys.readouterr().out
    assert code == 0
    assert "copyable" in out.lower()
    assert "%" in out, "the figures must be shown, not just the verdict"


def test_it_refuses_and_says_what_ticket_would_work(capsys: pytest.CaptureFixture[str]) -> None:
    rows = [a_fill("2000", day) for day in range(0, 30)]
    code = main([ADDRESS, "--ticket", "500"], client=venue(rows, "300000"))
    out = capsys.readouterr().out
    assert code == 1, "a trader the member cannot follow is a non-zero exit"
    assert "10" in out, "the floor must be named"


def test_it_returns_no_verdict_when_the_venue_is_unreachable(
    capsys: pytest.CaptureFixture[str],
) -> None:
    def down(_: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("no route to host")

    code = main(
        [ADDRESS, "--ticket", "2000"], client=httpx.Client(transport=httpx.MockTransport(down))
    )
    captured = capsys.readouterr()
    assert code == 2, "unreachable is not the same answer as not copyable"
    assert "unavailable" in (captured.out + captured.err).lower()
    assert "copyable" not in captured.out.lower(), "no verdict from partial data"
