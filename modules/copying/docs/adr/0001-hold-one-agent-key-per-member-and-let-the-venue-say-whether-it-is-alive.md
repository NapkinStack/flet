# ADR-0001 — Hold one agent key per member, and let the venue say whether it is alive

- **Status**: Proposed
- **Date**: 2026-09-24
- **Decision makers**: @napkinstack-admin, on the author's proposal
- **Scope**: module `copying`
- **Reversibility**: costly — once members have authorised keys, changing how they are held
  means asking every member to authorise again

---

## Context

Cycle 03 was accepted on 2026-09-24. Its D2 asks that a member can hand flet a key that places
orders and nothing else, and take it back, with every criterion answered by the venue rather than
by our own state. The charter already fixes the shape: **no custody, ever**. flet holds one
revocable, expirable agent key per member, able to place and cancel orders and nothing else.

Nothing in the project signs today. `screening` holds no key by construction (its ADR-0002), and
that ADR names the official SDK as "the expected choice for the copying module, which will sign".

What the venue documents, read on 2026-09-24 from its own pages and its SDK's source:

- **An agent (API wallet) is approved by the account's main key** through `approveAgent`, an
  EIP-712 user-signed action carrying `agentAddress`, an optional `agentName` and a nonce. The SDK
  generates the agent's private key locally and signs the approval with the main key. *Primary:
  `exchange-endpoint`; SDK `exchange.py:approve_agent`, `utils/signing.py:sign_agent`.*
- **An account may hold one unnamed agent and up to three named ones.** "A custom expiration can
  be set by appending `valid_until {timestamp}` after the name. The expiration can be at most 180
  days in the future." *Primary: `exchange-endpoint`.*
- **There is no revoke action.** An agent is deregistered when a new one is approved under the
  same name, when it expires, or when the account no longer has funds. "Once an agent is
  deregistered, its used nonce state may be pruned … previously signed actions can be replayed";
  the venue advises never reusing an agent's address. *Primary: `nonces-and-api-wallets`.*
- **The agents of an account can be read back**: `{"type":"extraAgents","user":<main address>}`
  returns `name`, `address` and `validUntil`. *SDK `info.py:extra_agents`; absent from the
  documentation page — reported by the SDK, not by the docs.*
- **What an agent can sign is not listed anywhere.** The SDK's agent example states "the agent
  does not have permission to transfer or withdraw funds"; the builder-code page says
  `ApproveBuilderFee` must be signed by the main wallet. That every *user-signed* action is
  refused to an agent is an **inference**, and D2's second criterion exists to replace it with
  observations.

## Problem

How does flet obtain, hold, check and lose a member's agent key, so that the key can only trade,
its revocation is real, and nothing in flet can act on a key the venue no longer honours?

## Constraints

- **No custody.** flet never sees a member's main key or their funds (charter).
- **The member signs with their main wallet, outside a chat** (charter, from the builder-code
  constraint). Nothing in this cycle builds a wallet-connection page.
- **A solo, half-time project on one Hetzner server.** No vault, no KMS, no second machine.
- **`critical`.** A leaked key cannot take a member's money but can lose it, with leverage.
- **Decided by the decider on 2026-09-24:** the member authorises on the venue's own API page;
  keys expire after **30 days**; tests run against the venue's testnet with a wallet the decider
  funds.

---

## Prior art

**Dominant convention of the field:** a trading application on this venue generates an API
wallet, has the user approve it with their main wallet, and trades with it on the user's behalf —
one agent per trading process. It is the mechanism the venue documents for exactly this purpose.

**References examined:**

| Reference | What it does | Applicable here? |
|---|---|---|
| The venue's [API wallets](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets) and [`approveAgent`](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint) | Main key approves an agent address; the agent signs trading actions; expiry by `valid_until`; deregistration by name replacement or expiry | **Yes — it is the only non-custodial mechanism the venue offers.** |
| [`hyperliquid-python-sdk`](https://github.com/hyperliquid-dex/hyperliquid-python-sdk) 0.24.0, `examples/basic_agent.py` | Creates an agent with the main key, then trades through `Exchange(agent, url, account_address=main)` | **Yes for trading.** Its `approve_agent` needs the main key, which flet never holds, so flet generates the agent itself and the member approves it on the venue. |
| The venue's own API page (`app.hyperliquid.xyz/API`) | Lets the account owner approve and remove API wallets with their main wallet | **Yes — it is where the member authorises and revokes.** *Assumption to observe on the test sheet: that it accepts a name carrying `valid_until`.* |
| [`cryptography` Fernet](https://cryptography.io/en/latest/fernet/) | Authenticated symmetric encryption, the Python ecosystem's standard answer to "encrypt this blob at rest" | **Yes, for the key at rest** (security rule S5: never our own crypto). |
| HashiCorp Vault, a cloud KMS | Keys held by a dedicated service, never on the application's disk | Not at this size: a second service to run and secure on one server, for a pilot of 5–8 members. The exit if the pilot grows. |

**Why the convention is not enough:** it is enough. The one departure is that flet does not call
the SDK's `approve_agent`, because that call signs with the main key; the member performs that
step on the venue instead.

---

## Options considered

### Option 1 — Agent key generated by flet, approved by the member on the venue's page, encrypted at rest *(chosen)*
- Description: flet generates a fresh key pair per member, shows the address and the name
  `flet valid_until <now + 30 days>`; the member approves it on the venue's API page. flet stores
  the private key encrypted with Fernet under a secret taken from the environment, in a file only
  its owner can read. Before any action for a member, flet reads `extraAgents` and acts only if
  its agent is listed and not expired.
- Advantages: the venue's own convention; no page of ours ever touches a wallet; the venue, not
  flet, is the record of whether a key lives; revocation is the venue's, so it works even if flet
  is down or wrong.
- Drawbacks: the member copies an address into a web page — one manual step, and a wrong paste
  approves nothing rather than something else. The encryption secret sits on the same machine as
  the ciphertext: it protects against a leaked file or backup, not against a compromised server.
- Cost of setup / maintenance / **getting out**: low / one dependency pair to track / move the
  ciphertext to a vault; members need not re-authorise.

### Option 2 — A flet web page that asks the member's wallet to sign `approveAgent`
- Advantages: no copied address; the name and expiry cannot be mistyped.
- Drawbacks: a web surface that talks to wallets, to build and secure inside a three-week cycle
  that also carries D1 and D3. Rejected by the decider on 2026-09-24.

### Option 3 — Keys in clear on disk, or only in memory
- In clear: one leaked backup is every member's trading key. Refused on S1.
- Only in memory: every restart silently loses every key, and each member must re-authorise —
  which also burns the venue's named-agent slots and forbids reusing addresses.

### Option 4 — Do nothing: members copy by hand
- What the discovery found members already do, and why the project exists.

---

## Decision

**Option 1.** Concretely, and each line is a test in D2:

1. **One named agent per member**, name `flet valid_until <ms timestamp>`, 30 days out. Named, not
   unnamed, so that flet occupies one of the member's three named slots and never displaces an
   unnamed agent another tool of theirs may use. *The unit of the timestamp is not documented;
   the first venue test establishes it by reading `validUntil` back.*
2. **A fresh address every time.** An address that has ever been approved is never approved again
   (the venue's replay warning).
3. **The venue is the truth.** Before any action for a member, flet reads `extraAgents`; not
   listed, or `validUntil` past, means flet does nothing for that member and does not retry.
4. **Revocation is the member's act on the venue** — removing the agent, or letting it expire.
   flet also offers to forget its copy on request, which stops flet even before the venue is
   told, but it never presents that as a revocation.
5. **At rest, Fernet-encrypted**, secret from the environment, file mode 0600. A key is deleted
   once the venue no longer lists it. It never appears in a log, in process output or in the
   repository.
6. **Dependencies:** `hyperliquid-python-sdk` (signing trading actions as the agent) and
   `cryptography` (Fernet), each declared in the manifest with its exit.

### Deviation from the convention

None on the mechanism. Not calling `approve_agent` follows from the charter's no-custody rule.

---

## Success criterion

> We will consider this was the right call if **D2 is accepted by 2026-10-15 with every venue
> test green on testnet — scope read back, each forbidden action refused by the venue, an order
> refused after revocation — and no key found in the logs, the process output or the
> repository**, observed at cycle 03's closure.

What we do if it is not: if the venue accepts a user-signed action from an agent, the no-custody
promise does not hold with this mechanism and the pilot does not start — that is a finding for the
charter, not a bug to patch here.

---

## Consequences

**Positive:**

- flet can never move a member's funds by construction of the venue, not of our code — provided
  D2's second criterion confirms it.
- A revocation works even if flet is down, wrong or compromised.

**Negative and accepted debt:**

- The encryption secret lives beside the ciphertext. Recorded in the runbook as the reason a
  server compromise is a key incident for every member, to be answered by rotating: every member
  approves a new agent.
- One read of `extraAgents` before each action costs a request per member per action; the copy
  engine of the next cycle has to budget for it.
- Two ways to reach the venue in the project — `screening`'s plain HTTP client and this SDK — as
  `screening`'s ADR-0002 anticipated, with the boundary between them exactly the boundary between
  signing and not signing.

**Impacts on other modules or contracts:** none. `screening` is untouched and no contract exists.

**Rule to automate:** a test that runs every path of the module with a known key and asserts its
hex appears in no captured log line and no output — D2's fifth criterion, made permanent.

---

## Rejected alternatives

**Option 2, our own signing page** — rejected by the decider for this cycle, on appetite.
**Option 3, clear or memory-only keys** — rejected on S1 and on the replay rule.
**A vault or KMS** — deferred, not rejected: the exit when the member count outgrows one server.
