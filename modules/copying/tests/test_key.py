import pytest
from eth_account import Account

from copying.key import LIFETIME_MS, member_address, new_agent

NOW = 1_790_000_000_000


def test_a_new_agent_expires_thirty_days_out() -> None:
    assert new_agent(NOW).valid_until_ms == NOW + 30 * 24 * 3600 * 1000 == NOW + LIFETIME_MS


def test_its_name_carries_the_expiry_the_venue_reads() -> None:
    agent = new_agent(NOW)
    assert agent.name == f"flet valid_until {agent.valid_until_ms}"


def test_its_address_is_the_one_its_key_signs_as() -> None:
    agent = new_agent(NOW)
    assert Account.from_key(agent.private_key).address == agent.address


def test_every_agent_is_a_fresh_address() -> None:
    assert len({new_agent(NOW).address for _ in range(20)}) == 20


def test_the_key_never_shows_in_its_representation() -> None:
    agent = new_agent(NOW)
    assert agent.private_key.removeprefix("0x") not in repr(agent)
    assert agent.private_key.removeprefix("0x") not in str(agent)


def test_a_member_address_is_normalised() -> None:
    raw = "0x" + "AB" * 20
    assert member_address(raw) == raw.lower()


@pytest.mark.parametrize(
    "raw",
    ["", "0x", "0x" + "a" * 39, "0x" + "a" * 41, "0x" + "g" * 40, "../../etc/passwd", "a" * 42],
)
def test_anything_else_is_refused_as_a_member_address(raw: str) -> None:
    with pytest.raises(ValueError):
        member_address(raw)
