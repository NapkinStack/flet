---
status: accepted
decider: "@napkinstack-admin"
success_criteria:
  - "At least 20 members are still copying 30 days after they started, observed on 2026-12-31"
  - "The commission collected in a single calendar month exceeds 500 €, observed before 2027-03-21"
---

# Charter — flet

> Written once, at the first framing (`playbooks/framing.md`). Changed only through a PDR.
> Every agent session reads it.
>
> It reuses `docs/project/discovery.md`, decided **go** on 2026-09-21 after three rounds and
> two independent challenges. Where the discovery marks something as an assumption rather
> than a finding, this charter says so too.

## Users and their problem

Three parties, and only one of them pays.

- **The member** of a trading community follows the same handful of traders in the channel
  for months, and copies them by retyping each trade or not at all. **This problem is an
  assumption of the decider, not a finding:** no member's words were ever quoted, no count of
  people spoken to was ever given. The link test (`link-test-protocol.md`) exists to end that.
- **The administrator** of a Discord server or Telegram channel wants to offer their
  community something useful. They curate the list of traders that may be copied — explicitly
  to keep scammers out — and **take no share of the commission**.
- **The traders** are members of the same community. They trade their own account and receive
  nothing; flet reads their public positions.

flet is installable by **any** administrator on **any** Discord server or Telegram channel.
Karim's 500-member server is the first one, not the product.

## Success criteria

**1. Twenty members still copying at day 30, on 2026-12-31.** This is the decider's own
stopping rule, and it tests the one claim two independent challenges failed to refute: that a
member copies because someone they know vouched, not because a ranking said so. It is observed
from the members' public addresses on the venue.

**Recorded honestly, because it is written in the discovery and must not be lost here:** this
criterion decides **interest, not viability**. Twenty copiers produce between 41 € and 671 € a
month at the measured turnover. The decider chose it deliberately over a revenue condition:
the first proof sought is use.

**2. More than 500 € of commission in a calendar month, before 2027-03-21.** *(framer, to
confirm — it is the restatement proposed for PDR-0001, whose current criterion is unreachable
at the measured turnover.)* This is the one that tests viability. It needs roughly 98,000 € of
member capital under copy. Observed from the builder fee credited on-chain.

## Constraints

**Product, decided:**

- **No custody, ever.** flet never holds a member's funds or their main key. It holds one
  revocable, expirable agent key per member, able to place and cancel orders and nothing else.
- **No promised, projected or advertised returns**, and no past performance used as a sales
  argument.
- **A flat commission on routed volume**, capped by the venue at **0.1% of notional**, taken
  on-chain and credited to flet. Never a share of a member's gains (PDR-0001).

**Imposed by the venue, measured:**

- Orders under **10 USDC of notional are refused**. A member therefore needs roughly **one
  twentieth of a trader's account** to place 80% of their orders, which makes matching traders
  to members' tickets a product requirement rather than a nicety.
- A member signs `ApproveBuilderFee` with their **main wallet**, not from inside a chat. A
  member holds at most **10** builder approvals.
- Hyperliquid excludes **Restricted Persons** — US and Ontario residents, US citizens
  anywhere. *Excerpt: the primary terms page defeated three sessions.*

**Distribution:**

- A Discord app is capped at **100 servers** unverified and becomes eligible for verification
  at **75**. *Excerpt.* Verification needs a live privacy policy and terms of service, identity
  verification, and a justification of each privileged intent — so the app uses **slash
  commands only** and never reads message content.
- Telegram's Bot Developer Terms **§7** restricts Mini Apps with crypto or wallet
  functionality to TON, with a §7.3 multichain carve-out. *Excerpt, and unread.*

**Legal:** the members are majority EU residents, the venue trades perpetual futures, and the
operator holds no authorisation. A written scoping opinion has been requested
(`legal-scoping-request.md`, version 3) and **the decider has chosen to launch without waiting
for it**. That choice, and what it means, is recorded in the discovery's section 6.

**Money and time:** 8,000 €, three months half-time, deadline **2026-12-31**. The application
runs on a Hetzner server already paid for by other projects, so the marginal running cost is
near zero and break-even is about three active installs.

## Risks

**Criticality: `critical`** *(framer, to confirm)*. This project **acts on someone else's
money, with leverage, while they are asleep**. The playbook raises criticality for a domain
that moves money or acts on someone's behalf; this does both. `security.md` applies from the
first cycle, to the code and to whatever a spike collects.

What that costs, said plainly so the decider chooses knowingly: at `critical`, the definition
of done adds end-to-end tests on the critical journeys, observability, and a **verified
rollback**. For a solo half-time project that is real weight. The alternative — `high` — drops
the rollback requirement.

The risks themselves:

1. **An agent key cannot take a member's money but can lose it.** A sizing bug, a runaway copy
   loop, or a leverage mistake liquidates a real account. This is the risk that sets the
   criticality.
2. **The regulatory risk is live and unresolved**, and the service will launch before the
   opinion arrives. If the answer is "authorisation required", what is unwound is open
   positions belonging to real people.
3. **The administrator performs the act regulators look at, for free.** Karim knows and
   accepts. No future administrator does, and flet neither selects nor controls them.
4. **The economics are thin and measured.** Across 284 builder-code protocols on this venue the
   trailing-30-day median is $2,436 and 61 earn exactly zero.
5. **Self-serve installation is an unaddressed surface**: an administrator who lists themselves,
   a server built to farm the product, a curated list that is a scam by design.

## Vocabulary

| Term | Meaning |
|---|---|
| **Administrator** | Whoever installs flet on a server or channel and curates its list of copyable traders. Unpaid. |
| **Member** | Someone in that community who copies a trader through flet. Keeps their own funds and main key. |
| **Trader** | Someone on the administrator's list. Trades their own account, receives nothing, is read from their public address. |
| **Agent key** | The second key a member authorises, held by flet, able to place and cancel orders on their account and nothing else. Revocable, expirable. |
| **Builder code** | The venue's mechanism that takes flet's fee on-chain from a routed fill and credits it to flet. Capped at 0.1% on perpetuals. |
| **Notional** | The size of an order in USDC. The commission is a share of it, not of any gain. |
| **Turnover** | A trader's monthly volume divided by their account. It sets both flet's revenue and the member's fee burden — they are the same variable. |
| **Ticket** | What a member puts under copy. Governs which traders they can follow at all, because of the 10 USDC floor. |
| **Copyable** | A trader whose turnover keeps the member's fee burden tolerable and whose orders stay above the floor once scaled. Distinct from trustworthy. |
| **Active community** | A server where at least one member is copying. Distinct from an install. |

## Out of scope

- **Any share of a member's gains**, and with it the venue's vault rail (PDR-0001).
- **Holding a member's funds or main key**, in any form, including temporarily.
- **Selecting traders on flet's behalf.** The list belongs to each administrator.
- **Serving Restricted Persons** as the venue defines them.

## Open questions

**Blocking:** none once this charter is accepted. The two questions below must be answered by
the decider *in accepting it*: the **criticality** (`critical` proposed) and **success
criterion 2** (the 500 € restatement proposed for PDR-0001).

**Not blocking:**

- The written legal opinion, requested and pending.
- Discord's 75/100 thresholds and Telegram's §7 clause, both *excerpt* after three sessions
  were refused by the primary pages.
- The install-to-active ratio, 15%, which is the decider's judgement and not a measurement.
- Whether an agent key can register another agent, and whether the venue's internal transfer
  actions accept an agent signature. The docs are silent.
- Hyperliquid's Restricted Persons clause, unverified on the primary source after three
  attempts.
