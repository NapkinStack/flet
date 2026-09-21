# ADR-0002 — Run on Python, and reach the venue with a client that cannot sign

- **Status**: Accepted
- **Date**: 2026-09-21
- **Decision makers**: @napkinstack-admin, on the framer's proposal
- **Scope**: module `screening`
- **Reversibility**: easy — the module is a few hundred lines against a public HTTP endpoint

---

## Context

`screening` must declare `commands.check` and `commands.test` before its first file of code
(fitness M7), and neither can be written without knowing what it runs on. The skeleton imposes
no stack: "the **names** never change, the **content** is yours."

What the module actually does is narrow. It reads a trader's public fills, a public
leaderboard and public candles, and computes four things from them: the share of orders that
would fall under the venue's 10 USDC floor once scaled to a member's ticket, the monthly
turnover and the fee burden it implies, the share of fills that rested on the book, and the
minimum ticket that makes the trader followable. **It authenticates to nothing, signs nothing
and holds nothing** — that is ADR-0001's boundary and this module's first invariant.

## Problem

What does this module run on, and what does it use to reach the venue?

## Constraints

- The project's toolchain is already **uv**, declared in `docs/tooling-profile.md` as the
  foundation's way of running commands and tests. A second package manager would be a second
  thing to install on the Hetzner box and in CI.
- `nstack` itself requires Python ≥ 3.12, so a Python runtime is present wherever this project
  is worked on.
- The module's invariant — never authenticate — must survive a future session that does not
  read this file.
- Two weeks of appetite, of which this module is one of three deliverables.

---

## Prior art

**Dominant convention of the field:** use the venue's official SDK.

**References examined:**

| Reference | What it does | Applicable here? |
|---|---|---|
| [`hyperliquid-python-sdk`](https://github.com/hyperliquid-dex/hyperliquid-python-sdk), v0.24.0, published by the venue's own org `hyperliquid-dex` | The official SDK. Its distinguishing work is **EIP-712 signing**, typed request objects and helpers for placing orders; it also wraps the public `info` endpoint. | **Partly, and that is the finding.** Everything this module needs from it is a JSON POST. Everything that makes it worth depending on is signing — which this module must never do. |
| [`nktkas/hyperliquid`](https://github.com/nktkas/hyperliquid), [`nomeida/hyperliquid`](https://github.com/nomeida/hyperliquid) — TypeScript | Community SDKs with full REST and WebSocket coverage and typed responses. Not published by the venue. | Only if the module were TypeScript, which would add a second toolchain beside uv for no measured gain. |
| The venue's [public `info` endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api) | A single unauthenticated JSON POST: `userFills`, `candleSnapshot`, `meta`. Used directly, without any SDK, for every measurement in `docs/project/discovery.md`. | **Yes.** The discovery's entire feasibility run — 2,912 fills, 13,524 accounts, the turnover distribution — was produced against it with nothing but an HTTP client. |

**Why the convention is not enough** *(and it is a narrow deviation, not a rejection)*: the
official SDK is the right dependency for the **copying** module, which will sign. Here, its
one distinguishing capability is the one thing forbidden. Taking it would put a signing
function one import away from a module whose first invariant is that it never signs.

---

## Options considered

### Option 1 — Python with the official SDK
- Description: `uv`, Python, `hyperliquid-python-sdk` for every call.
- Advantages: the convention; typed responses; one dependency to learn for this module and the
  next.
- Drawbacks: the module gains the ability to sign and place orders, which it must never use.
  The invariant stays a sentence in `AGENTS.md` that a future session can walk past.
- Cost of setup / maintenance / **getting out**: low / tracking an SDK whose surface is mostly
  unused / trivial.

### Option 2 — Python with a plain HTTP client *(chosen)*
- Description: `uv`, Python ≥ 3.12, `httpx` for the JSON POST, `pytest`, `ruff`, `mypy`.
- Advantages: the same toolchain as the rest of the project. **The client physically cannot
  sign**, so "this module never authenticates" is enforced by what is installed rather than by
  what is written. The endpoint is three call shapes and was already exercised throughout the
  discovery.
- Drawbacks: response shapes are typed by us, not by the venue; a breaking change to the
  endpoint is ours to notice.
- Cost of setup / maintenance / **getting out**: low / typing three response shapes / adopt the
  SDK, which stays available.

### Option 3 — TypeScript with a community SDK
- Description: Node, `nktkas/hyperliquid` or `nomeida/hyperliquid`.
- Advantages: the most-used Discord library lives in this ecosystem, so a later bot module
  might share it.
- Drawbacks: a second toolchain beside uv, on the workstation, on the Hetzner box and in CI,
  decided now for a module that is not the bot — and both SDKs are community, not the venue's.
- Cost of setup / maintenance / **getting out**: a second runtime everywhere / two ecosystems
  to keep current / rewriting the module.

### Option 4 — Do nothing: no stack, no module
- Described and rejected in ADR-0001. Judging copyability by eye is what every shipped
  competitor does, and the discovery measured what it costs the member.

---

## Decision

**Option 2.** Python on uv, reaching the venue with an HTTP client.

What settles it is not language preference — option 1 is the same language. It is that
**the dependency chosen cannot perform the act the module forbids**. This is the same
reasoning as ADR-0001 at the project level, where the administration token's `Contents: No
access` makes "the agent never commits with it" structural rather than trusted. A rule an
installed dependency cannot break outranks a rule an `AGENTS.md` states.

The official SDK is not rejected for the project: it is the expected choice for the copying
module, which will sign, and this ADR does not decide for it.

### Deviation from the convention

- **Expected user value**: none directly — a member never sees this. The value is that a wrong
  answer from this module can mislead an administrator, and a *signed* action from it could
  lose a member's money. The second failure is removed by construction.
- **How we will observe it**: the module's dependency list contains nothing capable of signing
  or of holding a key. That is checkable by reading one file.

---

## Success criterion

> We will consider this was the right call if **the module ships D3 within cycle 01's appetite
> and its dependency list still contains nothing that can sign**, observed on **2026-10-05**,
> the cycle's end date.

What we do if it is not: if typing the responses by hand turns out to cost more than it saves,
adopt the official SDK and replace this ADR — with a check that forbids importing its
signing surface from this module.

---

## Consequences

**Positive:**

- One toolchain for the whole project: uv, already the foundation.
- The module's first invariant is enforced by its dependencies rather than by its prose.
- `commands.check`, `commands.test` and `commands.bootstrap` can now be declared, which fitness
  M7 requires before the first file of code.

**Negative and accepted debt:**

- Three response shapes typed by us. A breaking change at the venue is ours to notice, and the
  module's "no verdict from stale or partial data" invariant is what limits the damage.
- The copying module will likely depend on the official SDK, so the project will hold both a
  hand-rolled client and an SDK. That is acceptable while the boundary between them is exactly
  the boundary between signing and not signing.

**Impacts on other modules or contracts:** none. No contract exists, and this ADR binds only
`screening`.

**Rule to automate:** ADR-0001 already names the check this module wants — that its source
performs no credential read, no signing call and no private-key handling. This decision makes
half of it mechanical: **assert that the module's declared dependencies contain no signing
library**. That is a check against one file and it should exist before the copying module does.

---

## Rejected alternatives

**Option 1, the official SDK here** — rejected on the boundary, not on quality. It is the right
dependency one module over.

**Option 3, TypeScript** — rejected because it decides the project's second toolchain from a
module that is not the one that would benefit. If the bot module later wants that ecosystem,
it argues for it then, with its own reasons.
