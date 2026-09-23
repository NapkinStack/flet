---
status: accepted
decider: "@napkinstack-admin"
success_criteria:
  - "Phase 1: a closed pilot of 5-8 members answers all five criteria of PDR-0003, before 2026-12-31"
  - "Phase 2, gated on the legal opinion and on phase 1: commission above 500 € in a calendar month"
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

**Revised on 2026-09-22 by [PDR-0003](../pdr/0003-prove-the-machine-on-a-few-before-opening-the-tap.md)**,
which replaced a count with evidence of quality and moved the commission criterion behind a
gate. This section states what that decision says; where the two disagree, the PDR wins. It is
written out here because the PDR was merged with this section left as it was, and the open
questions below claimed a revision the criteria above did not carry.

**Phase 1 — a closed pilot, 5 to 8 members and 2 to 3 traders, before 2026-12-31.** Five
criteria, every one observed rather than asserted:

1. **Zero unchosen divergence** between the member's position and the vouched trader's: the copy
   is faithful, or it refuses and says so. It is the product's whole promise — if it drifts
   silently, nothing else counts.
2. **Zero key incident.** The agent key can place orders and nothing else, throughout. A decider
   no-go, verified rather than asserted.
3. **Every member revokes at least once, deliberately, and it works.** An exit that has never
   been used is not an exit.
4. **At least 60% of members choose to continue past day 14.** The only desire signal a pilot can
   honestly produce.
5. **`screening`'s predictions confronted with reality** — fees actually incurred, share of
   orders refused, slippage between the trader's fill and the member's. The most valuable of the
   five, and only a small pilot produces it: it makes falsifiable everything that module has been
   asserting.

**Why the count went.** The earlier criterion — twenty members still copying at day 30 — was not
excused, it was arithmetically out of reach at pilot size: this project's own binomial model
showed five invitations returning *refuted* **47% of the time while the product was exactly as
good as forecast**. A criterion that fires on noise is worse than none, because it will be
believed. PDR-0003 carries the model.

**Phase 2 — the acquisition funnel, gated on two conditions**, not one: the written legal opinion
received *and acted on*, **and** every phase-1 criterion met. The funnel may be built meanwhile —
a landing page and a waiting list cost nothing and expose nothing. The tap does not open.

**The commission criterion lives there now**: more than 500 € in a calendar month, testing
viability, needing roughly 98,000 € of member capital under copy, observed from the builder fee
credited on-chain. **Its date is owed by the decider** — PDR-0003 moved it to phase 2 "with a
later date" and named none, so the old *before 2027-03-21* is not restated here as though it had
survived. See the open questions.

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
  at **75** — an email arrives at 75 with the link to apply. Corroborated across Discord's own
  developer support articles; **the Developer Policy page itself has now refused four
  independent sessions with HTTP 403**, so the clause on financial information is still
  *unread*, not merely *excerpt*. Verification needs a live privacy policy and terms of service,
  identity verification, and a justification of each privileged intent — so the app uses **slash
  commands only** and never reads message content.
- **Telegram: read on the primary source, and it decides more than it looked like it would.**
  Bot Developer Terms **§7**: *"all Mini Apps which implement cryptocurrency functionality,
  either within the Mini App itself **or within its connected bot**, are required to be based
  exclusively on [TON]"*. **§7.3** permits multichain wallets *"provided that such actions are
  performed directly within the interface of the Mini App"*, with external interactions through
  TON Connect only.

  Hyperliquid is not TON, so **a Mini App is closed to this product**. What §7 does not reach is
  a **bot with no Mini App at all**: the restriction is written about Mini Apps and the bots
  connected to them. That leaves one possible shape on Telegram — a bot whose wallet step sends
  the member to an ordinary web page in their browser, outside Telegram. Whether that survives
  contact with Telegram's review is **untested**, and it is a narrower path than Discord's.
  *The decider has already said that excluding Telegram is acceptable.*

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

**Answered 2026-09-22 — success criterion 1 is revised, by [PDR-0003](../pdr/0003-prove-the-machine-on-a-few-before-opening-the-tap.md).**

The question was: twenty interested members yield 3.5 to 8.4 still copying at day 30, against
a criterion of 20. Widen to 48-114 interested, or restate the criterion.

The decider chose to restate, and gave the reason: onboarding many users prematurely is
dangerous for a product where a defect produces a liquidation rather than a bad page, and
where the legal opinion has not arrived. The framer agrees, and PDR-0003 carries why, what
replaces the criterion, what it costs, and the one illusion to avoid — a small pilot proves
the system does not harm, not that it scales.

**A count is replaced by evidence of quality**, because at five to eight members a threshold
on a number is noise: this project's own model showed five invitations returning *refuted*
47% of the time while the product was exactly as good as forecast.

The pilot size is a **launch** parameter. It gates no deliverable and no module.

**Previously blocking, answered when this charter was accepted:** the **criticality**
(`critical`) and **success criterion 2** (the 500 € restatement proposed for PDR-0001).

**Owed by the decider, since 2026-09-22:** the **date** on the phase-2 commission criterion.
PDR-0003 moved it there "with a later date" and named none. Until it has one, the project has a
viability criterion with no deadline, which is a criterion that cannot fail.

**Not blocking:**

- The written legal opinion, requested and pending.
- Discord's 75/100 thresholds and Telegram's §7 clause, both *excerpt* after three sessions
  were refused by the primary pages.
- The install-to-active ratio, 15%, which is the decider's judgement and not a measurement.
- Whether an agent key can register another agent, and whether the venue's internal transfer
  actions accept an agent signature. The docs are silent.
- Hyperliquid's Restricted Persons clause, unverified on the primary source after three
  attempts.
