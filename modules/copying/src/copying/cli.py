"""copying authorise | status | forget MEMBER — the member's key, as the venue sees it.

Exit codes: 0 done or alive · 1 flet holds no live key · 2 refused input or setup ·
3 no answer from the venue, nothing done.
"""

import argparse
import os
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

from copying.guard import alive
from copying.key import member_address, new_agent
from copying.store import KeyStore
from copying.venue import NoAnswer, Venue

PAGES = {False: "https://app.hyperliquid.xyz/API", True: "https://app.hyperliquid-testnet.xyz/API"}


def venue_for(testnet: bool) -> Venue:
    from hyperliquid.info import Info
    from hyperliquid.utils.constants import MAINNET_API_URL, TESTNET_API_URL

    return Info(TESTNET_API_URL if testnet else MAINNET_API_URL, skip_ws=True)  # type: ignore[no-any-return]


def _now_ms() -> int:
    return int(time.time() * 1000)


def _day(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, UTC).strftime("%Y-%m-%d %H:%M UTC")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="copying")
    parser.add_argument("command", choices=["authorise", "status", "forget"])
    parser.add_argument("member", help="the member's main address on the venue")
    parser.add_argument("--testnet", action="store_true")
    args = parser.parse_args(argv)

    try:
        member = member_address(args.member)
        store = KeyStore(Path(os.environ["FLET_KEY_DIR"]), os.environ["FLET_KEY_SECRET"].encode())
    except (ValueError, KeyError):
        print(
            "Refused: a member address and FLET_KEY_DIR, FLET_KEY_SECRET are needed.",
            file=sys.stderr,
        )
        return 2

    if args.command == "authorise":
        agent = new_agent(_now_ms())
        store.put(member, agent)
        print(f"Approve this agent with your main wallet at {PAGES[args.testnet]}")
        print(f"  Address: {agent.address}")
        print(f"  Name:    {agent.name}")
        print(f"It expires on {_day(agent.valid_until_ms)}. It can place and cancel orders,")
        print("nothing else. Remove it on the same page to take it back at any time.")
        return 0

    if args.command == "forget":
        store.forget(member)
        print("flet no longer holds a key for this member.")
        print(f"This does not revoke it on the venue: remove it at {PAGES[args.testnet]}")
        return 0

    if store.get(member) is None:
        print("flet holds no key for this member.")
        return 1
    try:
        try:
            venue = venue_for(args.testnet)
        except Exception as e:  # the SDK reads the venue while being built
            raise NoAnswer(type(e).__name__) from None
        found = alive(member, store, venue, _now_ms())
    except NoAnswer:
        print("No answer from the venue: nothing was done, nothing is known.", file=sys.stderr)
        return 3
    if found is None:
        print("Not listed on the venue, or expired: flet will not act for this member.")
        return 1
    listing = found[1]
    print(f"alive: {listing.address}, until {_day(listing.valid_until_ms)} per the venue.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
