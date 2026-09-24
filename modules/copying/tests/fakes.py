from typing import Any


class FakeVenue:
    """Answers `extraAgents` from a fixed list, or fails like an unreachable venue."""

    def __init__(self, agents: list[dict[str, Any]] | None = None, fail: bool = False) -> None:
        self.agents = agents or []
        self.fail = fail
        self.calls: list[str] = []

    def extra_agents(self, user: str) -> Any:
        self.calls.append(user)
        if self.fail:
            raise ConnectionError("egress denied")
        return self.agents


def listing(address: str, name: str, valid_until_ms: int) -> dict[str, Any]:
    return {"address": address, "name": name, "validUntil": valid_until_ms}
