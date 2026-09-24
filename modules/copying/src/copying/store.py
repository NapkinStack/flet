"""Agent keys at rest: one Fernet-encrypted file per member, readable by its owner only."""

import json
import os
from dataclasses import dataclass
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken

from copying.key import Agent, member_address


@dataclass(frozen=True)
class Held:
    agent: Agent
    # Seen listed by the venue at least once: absent afterwards means revoked, not pending.
    confirmed: bool


class KeyStore:
    def __init__(self, directory: Path, secret: bytes) -> None:
        self._directory = directory
        self._fernet = Fernet(secret)

    def _path(self, member: str) -> Path:
        return self._directory / f"{member_address(member)}.key"

    def _write(self, member: str, agent: Agent, confirmed: bool) -> None:
        path = self._path(member)
        plain = json.dumps(
            {
                "address": agent.address,
                "valid_until_ms": agent.valid_until_ms,
                "private_key": agent.private_key,
                "confirmed": confirmed,
            }
        ).encode()
        staged = path.with_suffix(".tmp")
        fd = os.open(staged, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "wb") as f:
            f.write(self._fernet.encrypt(plain))
        os.replace(staged, path)

    def put(self, member: str, agent: Agent) -> None:
        self._write(member, agent, confirmed=False)

    def get(self, member: str) -> Held | None:
        path = self._path(member)
        if not path.exists():
            return None
        try:
            data = json.loads(self._fernet.decrypt(path.read_bytes()))
        except InvalidToken:
            raise ValueError("the key file cannot be read with this secret") from None
        agent = Agent(data["address"], data["valid_until_ms"], data["private_key"])
        return Held(agent, data["confirmed"])

    def confirm(self, member: str) -> None:
        held = self.get(member)
        if held is not None:
            self._write(member, held.agent, confirmed=True)

    def forget(self, member: str) -> bool:
        path = self._path(member)
        if not path.exists():
            return False
        path.unlink()
        return True
