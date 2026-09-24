"""D2 on the venue's testnet: the venue, not flet's state, answers every question here.

Needs FLET_TESTNET_MAIN_KEY — the decider's funded testnet wallet, standing in for a member.
Without it every test here is skipped, and a skipped test is *not run*, never a pass.
The member's own step — approving flet's agent on the venue's API page — is played by
`approve`, signed with the main key exactly as that page would; nothing in `src/` does this.
"""

import math
import os
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from cryptography.fernet import Fernet
from eth_account import Account
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils.constants import TESTNET_API_URL
from hyperliquid.utils.error import ClientError
from hyperliquid.utils.signing import get_timestamp_ms, sign_agent

from copying.guard import act_for
from copying.key import Agent, new_agent
from copying.store import KeyStore
from copying.venue import listed

MAIN_KEY = os.environ.get("FLET_TESTNET_MAIN_KEY", "")
pytestmark = [
    pytest.mark.venue,
    pytest.mark.skipif(not MAIN_KEY, reason="FLET_TESTNET_MAIN_KEY not set: NOT RUN"),
]
ELSEWHERE = "0x000000000000000000000000000000000000dEaD"
COIN = "BTC"


@pytest.fixture(scope="module")
def main() -> Any:
    return Account.from_key(MAIN_KEY)


@pytest.fixture(scope="module")
def info() -> Info:
    return Info(TESTNET_API_URL, skip_ws=True)


def approve(main: Any, address: str, name: str) -> Any:
    """What the member does on the venue's API page, signed with their main key."""
    nonce = get_timestamp_ms()
    action = {"type": "approveAgent", "agentAddress": address, "agentName": name, "nonce": nonce}
    signature = sign_agent(main, action, False)
    return Exchange(main, TESTNET_API_URL).post(
        "/exchange", {"action": action, "nonce": nonce, "signature": signature}
    )


def revoke(main: Any, agent: Agent) -> Any:
    """Replace the agent under its name — the venue's only documented deregistration."""
    return approve(main, new_agent(get_timestamp_ms()).address, agent.name)


def refused(call: Callable[[], Any]) -> str:
    """The venue's refusal, verbatim; fails if the venue accepted."""
    try:
        response = call()
    except ClientError as e:
        return f"HTTP {e.status_code}: {e.error_message}"
    assert isinstance(response, dict) and response.get("status") == "err", response
    return str(response.get("response"))


def funds(info: Info, main: Any) -> tuple[str, str]:
    perp = info.user_state(main.address)["marginSummary"]["accountValue"]
    spot = info.spot_user_state(main.address)["balances"]
    return perp, str(sorted((b["coin"], b["total"]) for b in spot))


def far_order(agent_exchange: Exchange, info: Info) -> Any:
    """A resting buy at half the mid: never fills, 12 USDC of notional, over the floor."""
    mid = float(info.all_mids()[COIN])
    decimals = next(a["szDecimals"] for a in info.meta()["universe"] if a["name"] == COIN)
    price = float(f"{mid / 2:.5g}")
    size = math.ceil(12 / price * 10**decimals) / 10**decimals
    return agent_exchange.order(COIN, True, size, price, {"limit": {"tif": "Gtc"}})


def placed(response: Any) -> int:
    assert response.get("status") == "ok", response
    status = response["response"]["data"]["statuses"][0]
    assert "resting" in status, status
    return int(status["resting"]["oid"])


@pytest.fixture
def agent(main: Any) -> Any:
    a = new_agent(get_timestamp_ms())
    assert approve(main, a.address, a.name).get("status") == "ok"
    yield a
    revoke(main, a)


def usdc(info: Info) -> str:
    token = next(t for t in info.spot_meta()["tokens"] if t["name"] == "USDC")
    return f"USDC:{token['tokenId']}"


def as_agent(agent: Agent, main: Any) -> Exchange:
    return Exchange(
        Account.from_key(agent.private_key), TESTNET_API_URL, account_address=main.address
    )


# Criterion 1 — the scope and the expiry are read back from the venue.


def test_the_venue_lists_the_agent_with_the_expiry_we_asked_for(
    agent: Agent, main: Any, info: Info
) -> None:
    listing = listed(info, main.address, agent.address)
    assert listing is not None
    assert listing.valid_until_ms == agent.valid_until_ms
    assert info.user_role(agent.address) == {
        "role": "agent",
        "data": {"user": main.address.lower()},
    }


def test_the_agent_can_place_and_cancel_an_order(agent: Agent, main: Any, info: Info) -> None:
    exchange = as_agent(agent, main)
    oid = placed(far_order(exchange, info))
    assert exchange.cancel(COIN, oid).get("status") == "ok"


# Criterion 2 — every action the key must not perform, attempted, refused, funds unmoved.
# A user-signed action is attributed to whoever signed it; the refusal alone could be the
# agent's own empty account refusing. So each test also reads the member's funds.

FORBIDDEN: dict[str, Callable[[Exchange, Any], Any]] = {
    "withdraw3": lambda x, m: x.withdraw_from_bridge(2, m.address),
    "usdSend": lambda x, m: x.usd_transfer(1, ELSEWHERE),
    "spotSend": lambda x, m: x.spot_transfer(1, ELSEWHERE, usdc(x.info)),
    "usdClassTransfer": lambda x, m: x.usd_class_transfer(1, to_perp=False),
    "sendAsset": lambda x, m: x.send_asset(ELSEWHERE, "", "", "USDC", 1),
    "approveAgent": lambda x, m: x.approve_agent("intruder")[0],
    "approveBuilderFee": lambda x, m: x.approve_builder_fee(ELSEWHERE, "0.1%"),
}


@pytest.mark.parametrize("action", sorted(FORBIDDEN))
def test_the_venue_refuses_the_agent(
    action: str, agent: Agent, main: Any, info: Info, record_property: Any
) -> None:
    before = funds(info, main)
    agents_before = info.extra_agents(main.address)
    refusal = refused(lambda: FORBIDDEN[action](as_agent(agent, main), main))
    record_property("refusal", refusal)
    assert funds(info, main) == before
    assert info.extra_agents(main.address) == agents_before


# Criteria 3 and 4 — after revocation or expiry, the venue refuses and flet does nothing.


def test_after_revocation_the_venue_refuses_an_order(main: Any, info: Info) -> None:
    agent = new_agent(get_timestamp_ms())
    approve(main, agent.address, agent.name)
    exchange = as_agent(agent, main)
    exchange.cancel(COIN, placed(far_order(exchange, info)))  # it worked before
    assert revoke(main, agent).get("status") == "ok"
    assert listed(info, main.address, agent.address) is None
    refused(lambda: placed(far_order(exchange, info)))


def test_after_expiry_the_venue_refuses_an_order(main: Any, info: Info) -> None:
    agent = new_agent(get_timestamp_ms(), lifetime_ms=60_000)
    approve(main, agent.address, agent.name)
    time.sleep(max(0, agent.valid_until_ms - get_timestamp_ms()) / 1000 + 10)
    refused(lambda: placed(far_order(as_agent(agent, main), info)))


def test_after_revocation_flet_does_nothing(main: Any, info: Info, tmp_path: Path) -> None:
    store = KeyStore(tmp_path, Fernet.generate_key())
    agent = new_agent(get_timestamp_ms())
    store.put(main.address.lower(), agent)
    approve(main, agent.address, agent.name)
    assert act_for(main.address.lower(), store, info, get_timestamp_ms(), lambda a: "acted")
    revoke(main, agent)
    calls: list[Any] = []
    assert act_for(main.address.lower(), store, info, get_timestamp_ms(), calls.append) is None
    assert calls == []
    assert store.get(main.address.lower()) is None
