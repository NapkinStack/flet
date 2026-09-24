# copying — local instructions

> Only what is **specific to this module**.
> Never duplicate a kernel rule (`/AGENTS.md`).

## Responsibility

Holds each member's trade-only agent key on the venue, acting with it solely while the venue
still honours it.

## What this module does not do

- **It never holds, asks for or signs with a member's main key.** The member approves flet's
  agent on the venue's own API page (ADR-0001). A task that needs the main key has the boundary
  wrong — stop and say so. The SDK's `approve_agent` signs with the main key: never call it here.
- **It never moves funds.** No withdrawal, transfer, builder-fee approval or agent approval is
  ever built here, even as a helper. The only place such calls appear is the venue tests that
  prove the venue refuses them.
- **It does not judge whether a trader is copyable.** That is `screening`.
- **It does not copy orders yet.** Cycle 03 is the key, its revocation and the notice; the first
  copied order is the next cycle's.

## Internal conventions nobody could guess

- **The venue is the record, flet's state is a cache.** Whether a key is alive is read from
  `extraAgents` before acting, never from what flet stored or remembers doing.
- **A test that the venue refuses something must reach the venue.** A mocked refusal proves
  nothing about the key. Venue tests run on testnet, marked `venue`, and need the decider's
  funded wallet in the environment; without it they are skipped *and reported as not run*, never
  counted as passing.

## Business invariants

- **An agent can place and cancel orders and nothing else** — established by attempting each
  forbidden action on the venue, one test per action.
- **Not listed, or expired, means nothing happens**, with no retry.
- **An agent address is never approved twice.** The venue may prune a deregistered agent's
  nonces, which makes its old signatures replayable.
- **A key never appears in a log line, in process output or in the repository.** At rest it is
  Fernet-encrypted, mode 0600, and deleted once the venue no longer lists it.
- **Expiry is 30 days** (the decider, 2026-09-24), well under the venue's 180-day ceiling.

## Known traps

- **`extraAgents` is documented by the SDK, not by the venue's pages**, and the unit of
  `valid_until` is documented nowhere. Establish both on the venue; do not assume.
- **Queries must use the member's main address.** Querying with the agent's address returns an
  empty result, which reads exactly like "revoked".
- **Egress denied looks like "not listed".** A sandboxed session without `allowed_domains`
  including the venue's testnet host gets a network error: that is *no answer*, and must never be
  recorded as a refusal or a revocation.

## Areas not to change without approval

The 30-day expiry, the named-agent choice and the encryption at rest are the decider's and
ADR-0001's. Changing any of them is a new ADR.

## Non-standard commands

None yet. `commands.check` and `commands.test` are declared with the first file of code.
