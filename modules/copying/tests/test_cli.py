import logging
from pathlib import Path
from typing import Any

import pytest
from cryptography.fernet import Fernet

from copying import cli
from copying.key import Agent, new_agent
from tests.fakes import FakeVenue, listing

MEMBER = "0x" + "1" * 40


@pytest.fixture
def env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("FLET_KEY_DIR", str(tmp_path))
    monkeypatch.setenv("FLET_KEY_SECRET", Fernet.generate_key().decode())
    return tmp_path


@pytest.fixture
def made(monkeypatch: pytest.MonkeyPatch) -> list[Agent]:
    """Records every agent the command creates, so its key can be searched for."""
    agents: list[Agent] = []

    def recording(now_ms: int) -> Agent:
        agent = new_agent(now_ms)
        agents.append(agent)
        return agent

    monkeypatch.setattr(cli, "new_agent", recording)
    return agents


def use_venue(monkeypatch: pytest.MonkeyPatch, venue: FakeVenue) -> None:
    monkeypatch.setattr(cli, "venue_for", lambda testnet: venue)


def test_authorise_shows_what_to_approve_and_where(
    env: Path, made: list[Agent], capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main(["authorise", MEMBER]) == 0
    out = capsys.readouterr().out
    (agent,) = made
    assert agent.address in out
    assert agent.name in out
    assert "https://app.hyperliquid.xyz/API" in out


def test_authorise_on_testnet_points_at_the_testnet_page(
    env: Path, made: list[Agent], capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main(["authorise", MEMBER, "--testnet"]) == 0
    assert "https://app.hyperliquid-testnet.xyz/API" in capsys.readouterr().out


def test_status_of_a_listed_agent_is_alive(
    env: Path,
    made: list[Agent],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    cli.main(["authorise", MEMBER])
    (agent,) = made
    use_venue(monkeypatch, FakeVenue([listing(agent.address, agent.name, agent.valid_until_ms)]))
    capsys.readouterr()
    assert cli.main(["status", MEMBER]) == 0
    assert "alive" in capsys.readouterr().out


def test_status_of_an_unlisted_agent_says_flet_will_not_act(
    env: Path,
    made: list[Agent],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    cli.main(["authorise", MEMBER])
    use_venue(monkeypatch, FakeVenue([]))
    capsys.readouterr()
    assert cli.main(["status", MEMBER]) == 1
    assert "will not act" in capsys.readouterr().out


def test_no_answer_is_said_as_such_and_is_not_a_status(
    env: Path,
    made: list[Agent],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    cli.main(["authorise", MEMBER])
    use_venue(monkeypatch, FakeVenue(fail=True))
    capsys.readouterr()
    assert cli.main(["status", MEMBER]) == 3
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "no answer" in captured.err.lower()


def test_forget_says_it_is_not_a_revocation(
    env: Path, made: list[Agent], capsys: pytest.CaptureFixture[str]
) -> None:
    cli.main(["authorise", MEMBER])
    capsys.readouterr()
    assert cli.main(["forget", MEMBER]) == 0
    out = capsys.readouterr().out
    assert "not revoke" in out.lower()
    assert list(env.iterdir()) == []


def test_a_hostile_member_address_is_refused(env: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["authorise", "../../x"]) == 2


def test_without_its_secret_the_command_refuses(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FLET_KEY_DIR", str(tmp_path))
    monkeypatch.delenv("FLET_KEY_SECRET", raising=False)
    assert cli.main(["authorise", MEMBER]) == 2
    assert list(tmp_path.iterdir()) == []


def test_the_key_appears_in_no_output_and_no_log_on_any_path(
    env: Path,
    made: list[Agent],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.DEBUG)
    cli.main(["authorise", MEMBER])
    (agent,) = made
    for venue in (
        FakeVenue([listing(agent.address, agent.name, agent.valid_until_ms)]),
        FakeVenue(fail=True),
        FakeVenue([]),
    ):
        use_venue(monkeypatch, venue)
        cli.main(["status", MEMBER])
    cli.main(["forget", MEMBER])
    captured = capsys.readouterr()
    seen: list[Any] = [captured.out, captured.err, caplog.text]
    secret = agent.private_key.removeprefix("0x").lower()
    assert all(secret not in str(s).lower() for s in seen)
