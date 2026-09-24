from pathlib import Path
from typing import Any

import pytest
from cryptography.fernet import Fernet

from copying.guard import act_for
from copying.key import Agent, new_agent
from copying.store import KeyStore
from copying.venue import NoAnswer
from tests.fakes import FakeVenue, listing

NOW = 1_790_000_000_000
MEMBER = "0x" + "1" * 40


class Recorder:
    def __init__(self) -> None:
        self.signers: list[str] = []

    def __call__(self, account: Any) -> str:
        self.signers.append(account.address)
        return "done"


@pytest.fixture
def store(tmp_path: Path) -> KeyStore:
    return KeyStore(tmp_path, Fernet.generate_key())


@pytest.fixture
def agent(store: KeyStore) -> Agent:
    a = new_agent(NOW)
    store.put(MEMBER, a)
    return a


def test_a_listed_agent_acts_as_itself(store: KeyStore, agent: Agent) -> None:
    venue = FakeVenue([listing(agent.address, agent.name, agent.valid_until_ms)])
    action = Recorder()
    assert act_for(MEMBER, store, venue, NOW, action) == "done"
    assert action.signers == [agent.address]
    assert venue.calls == [MEMBER]


def test_the_first_listing_confirms_the_key(store: KeyStore, agent: Agent) -> None:
    venue = FakeVenue([listing(agent.address, agent.name, agent.valid_until_ms)])
    act_for(MEMBER, store, venue, NOW, Recorder())
    held = store.get(MEMBER)
    assert held is not None and held.confirmed


def test_no_key_held_means_nothing_happens_and_nothing_is_asked(store: KeyStore) -> None:
    venue, action = FakeVenue(), Recorder()
    assert act_for(MEMBER, store, venue, NOW, action) is None
    assert action.signers == [] and venue.calls == []


def test_an_agent_not_yet_approved_does_nothing_and_is_kept(store: KeyStore, agent: Agent) -> None:
    venue, action = FakeVenue([]), Recorder()
    assert act_for(MEMBER, store, venue, NOW, action) is None
    assert action.signers == []
    assert store.get(MEMBER) is not None


def test_a_revoked_agent_does_nothing_asks_once_and_is_deleted(
    store: KeyStore, agent: Agent
) -> None:
    store.confirm(MEMBER)
    venue, action = FakeVenue([]), Recorder()
    assert act_for(MEMBER, store, venue, NOW, action) is None
    assert action.signers == []
    assert venue.calls == [MEMBER]
    assert store.get(MEMBER) is None


def test_an_agent_the_venue_lists_as_expired_does_nothing(store: KeyStore, agent: Agent) -> None:
    store.confirm(MEMBER)
    venue = FakeVenue([listing(agent.address, agent.name, NOW - 1)])
    action = Recorder()
    assert act_for(MEMBER, store, venue, NOW, action) is None
    assert action.signers == []
    assert store.get(MEMBER) is None


def test_the_venue_s_expiry_wins_over_ours(store: KeyStore, agent: Agent) -> None:
    venue = FakeVenue([listing(agent.address, agent.name, NOW)])
    action = Recorder()
    assert act_for(MEMBER, store, venue, NOW, action) is None
    assert action.signers == []
    assert store.get(MEMBER) is None  # listed dead is dead, even if never seen alive


def test_another_agent_listed_under_the_member_is_not_ours(store: KeyStore, agent: Agent) -> None:
    store.confirm(MEMBER)
    other = new_agent(NOW)
    venue = FakeVenue([listing(other.address, agent.name, agent.valid_until_ms)])
    action = Recorder()
    assert act_for(MEMBER, store, venue, NOW, action) is None
    assert action.signers == []


def test_an_unapproved_key_past_its_expiry_is_deleted(store: KeyStore, agent: Agent) -> None:
    assert act_for(MEMBER, store, FakeVenue([]), agent.valid_until_ms, Recorder()) is None
    assert store.get(MEMBER) is None


def test_no_answer_does_nothing_retries_nothing_and_keeps_the_key(
    store: KeyStore, agent: Agent
) -> None:
    store.confirm(MEMBER)
    venue, action = FakeVenue(fail=True), Recorder()
    with pytest.raises(NoAnswer):
        act_for(MEMBER, store, venue, NOW, action)
    assert action.signers == []
    assert venue.calls == [MEMBER]
    assert store.get(MEMBER) is not None


@pytest.mark.parametrize("answer", [None, {"agents": []}, [{"address": 1}], ["x"]])
def test_a_malformed_answer_is_no_answer(store: KeyStore, agent: Agent, answer: Any) -> None:
    venue = FakeVenue()
    venue.agents = answer
    action = Recorder()
    with pytest.raises(NoAnswer):
        act_for(MEMBER, store, venue, NOW, action)
    assert action.signers == []
