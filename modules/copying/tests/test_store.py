import stat
from pathlib import Path

import pytest
from cryptography.fernet import Fernet

from copying.key import new_agent
from copying.store import KeyStore

NOW = 1_790_000_000_000
MEMBER = "0x" + "1" * 40


@pytest.fixture
def store(tmp_path: Path) -> KeyStore:
    return KeyStore(tmp_path, Fernet.generate_key())


def test_a_held_key_comes_back_unconfirmed(store: KeyStore) -> None:
    agent = new_agent(NOW)
    store.put(MEMBER, agent)
    held = store.get(MEMBER)
    assert held is not None
    assert held.agent == agent
    assert held.confirmed is False


def test_a_confirmed_key_stays_confirmed(store: KeyStore) -> None:
    store.put(MEMBER, new_agent(NOW))
    store.confirm(MEMBER)
    held = store.get(MEMBER)
    assert held is not None and held.confirmed


def test_an_unknown_member_holds_nothing(store: KeyStore) -> None:
    assert store.get(MEMBER) is None


def test_authorising_again_replaces_the_old_key(store: KeyStore) -> None:
    store.put(MEMBER, new_agent(NOW))
    store.confirm(MEMBER)
    second = new_agent(NOW)
    store.put(MEMBER, second)
    held = store.get(MEMBER)
    assert held is not None and held.agent == second and not held.confirmed


def test_forgetting_deletes_the_file(store: KeyStore, tmp_path: Path) -> None:
    store.put(MEMBER, new_agent(NOW))
    assert store.forget(MEMBER) is True
    assert store.get(MEMBER) is None
    assert list(tmp_path.iterdir()) == []
    assert store.forget(MEMBER) is False


def test_the_file_is_readable_by_its_owner_only(store: KeyStore, tmp_path: Path) -> None:
    store.put(MEMBER, new_agent(NOW))
    (path,) = tmp_path.iterdir()
    assert stat.S_IMODE(path.stat().st_mode) == 0o600


def test_the_key_is_not_on_disk_in_clear(store: KeyStore, tmp_path: Path) -> None:
    agent = new_agent(NOW)
    store.put(MEMBER, agent)
    (path,) = tmp_path.iterdir()
    raw = path.read_bytes().lower()
    assert agent.private_key.removeprefix("0x").lower().encode() not in raw


def test_another_secret_cannot_read_it(tmp_path: Path) -> None:
    KeyStore(tmp_path, Fernet.generate_key()).put(MEMBER, new_agent(NOW))
    with pytest.raises(ValueError):
        KeyStore(tmp_path, Fernet.generate_key()).get(MEMBER)


def test_a_hostile_member_address_never_reaches_the_filesystem(store: KeyStore) -> None:
    with pytest.raises(ValueError):
        store.put("../../escape", new_agent(NOW))
