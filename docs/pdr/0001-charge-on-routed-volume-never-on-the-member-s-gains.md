# PDR-0001 — Charge a flat commission on routed volume, never a share of the member's gains

- **Status**: Accepted
- **Date**: 2026-09-21
- **Decision makers**: @napkinstack-admin, decider of the project
- **Modules affected**: none yet — no module exists; this constrains the first one

> The PDR describes **what the product must do and why**, never its implementation.
> The how belongs to an ADR.

---

## User problem

A member about to copy a trader for the first time cannot answer a question they will
certainly ask: *what does this cost me, and when do I pay it?* The field gives two
incompatible answers — pay on every trade, or pay only when you gain — and they are not
interchangeable: one is knowable in advance, the other is not, and only one of them requires
somebody to hold the member's capital and compute their gains. Today flet has neither answer
nor revenue.

## Goal

Before their first copy, a member can see exactly what flet costs them and when it is taken,
and the answer is the same whether they win or lose.

## Out of scope

- **Any share of the member's gains.** Ruled out by the decider on 2026-09-21.
- Subscriptions, per-member or per-community.
- Any charge to the administrator, and any listing fee paid by a trader to appear on a list.
- Differentiated pricing per community: the rate is one number for everybody.

---

## Prior art

**How is this problem solved elsewhere?**

| Product / reference | Solution chosen | What we keep from it |
|---|---|---|
| [Hyperliquid builder codes](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/builder-codes) | A fee taken on-chain as part of the venue's own fee logic on each routed fill, credited to the builder; capped at 0.1% on perpetuals, 1% on spot | The entire mechanism. The venue collects and credits; nothing flows through flet, and flet issues no invoice |
| [Hyperliquid vaults](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults/for-vault-leaders-legacy) | A 10% share of profits, native to the venue, with a 5% permanent leader stake and — on the legacy rail — a 10k USDC creation fee | Nothing. It is the option rejected here, and the reason is below |
| [Bitget](https://www.bitget.com/support/articles/12560603892733), OKX, [Bybit](https://www.bybit.com/en/help-center/article/Copy-Trading-Profit-Sharing-Explained) copy trading | 10–20% of realised profit, set per lead trader, on a high-water mark | The convention a copy-trading user already knows |
| Telegram trading bots — Trojan, Maestro, BonkBot, BullX | A flat fee of about 1% on every trade | The convention a chat-bot user already knows |

**The convention the user already knows:** two of them, and which one they expect depends on
where they arrive from. Someone who has used Bitget or Bybit copy trading expects a profit
share. Someone who has used a Telegram trading bot expects a flat per-trade fee of around 1%.
flet's members arrive through the second door.

**Why depart from it** — meaning, why depart from the copy-trading convention of a profit
share:

1. **A profit share requires knowing the member's gains, which requires holding their
   capital or their accounting.** On this venue, the native way to take a profit share is the
   vault rail: pooled capital, a leader stake, and depositors who no longer hold their own
   position. That is custody, and the product's first adopted no-go forbids it. The
   alternative — computing each member's realised gains off-chain and billing them — makes
   flet a creditor of its members and gives it a P&L ledger it otherwise never needs.
2. **The flat fee here is a tenth of the flat-fee convention.** The venue caps it at 0.1% of
   notional where chat bots charge about 1%. A member coming from that world pays ten times
   less than the number they have in their head.
3. **It is knowable before signing.** A profit share cannot be quoted as a cost in advance;
   0.1% of each order can.

The cost of the deviation is owned: the member pays on losing trades too, which a profit
share would not charge them. That is the trade the decider took.

---

## Options considered

| Option | What the user experiences | Cost | Chosen? |
|---|---|---|---|
| Do nothing | Nothing to pay, and no service — flet has no revenue and cannot exist | 0 | No |
| **Flat commission on routed notional, at most 0.1%, via builder codes** | One signature at onboarding, then a fee taken by the venue on each copied order; nothing to pay flet directly, ever | Nothing to build: the venue already does it | **Yes** |
| Profit share via the venue's vault rail | Deposit into a pooled vault; 10% of gains to the leader; the member no longer holds their own position | Custody, a 5% leader stake, the legacy rail's 10k USDC creation fee, and the first no-go broken | No |
| Profit share billed off-chain | Pay flet a share of gains after the fact | An accounting ledger, a billing relationship, a debt the member can refuse | No |
| Subscription per member | A fixed monthly charge whether they trade or not | Payment rails, churn, and a charge on members who copied nothing | No |

## Decision

**flet is paid a flat commission on the notional it routes, at most 0.1%, taken by the venue
itself and credited to flet. It never takes a share of a member's gains, and never bills a
member directly.**

The member's cost is one number they can be shown before they sign anything. flet's revenue
is proportional to activity and to nothing else — not to the member's success, not to their
balance, not to their tenure. The trade-off owned: a member who loses still pays, and flet
earns from a losing month. The counterweight is that flet never has a reason to hold the
member's money, never computes their gains, and never has anything to invoice.

---

## Expected behaviour

**Nominal journey:** a member starts the copy flow. Before any signature is requested, the
rate is shown as a percentage **and** as a worked example on a concrete order. The member
signs the venue's builder-fee approval once, with their own main wallet. From then on, each
copied order carries the fee, taken by the venue at execution. The member never receives a
bill from flet.

**Edge cases and degraded states:**

- **No orders routed in a period** — the member is charged nothing at all.
- **The member revokes the approval** — copying stops; no charge survives the revocation.
- **The venue lowers its cap below the configured rate** — the lower figure applies, and the
  displayed rate is corrected before the next order is routed.
- **A member already holds ten builder approvals**, the venue's maximum — onboarding fails
  with an explanation naming the limit, not a generic error.

**Business rules:**

- One rate, the same for every member and every community.
- At most 0.1% of notional on perpetuals; it may be set lower, never higher.
- Taken by the venue on each routed fill and credited to flet. flet holds no member balance
  and issues no invoice.
- The administrator receives nothing, and no trader pays to appear on a list.

**Permissions:** only the operator may set or change the rate. An administrator has no
setting that changes, adds to, or waives it for their community.

**Acceptance criteria** *(testable — this is the task's oracle)*:

- [ ] Given a member who has not yet approved a builder fee, when they begin the copy flow,
      then the rate is displayed as a percentage and as a worked example on a concrete order
      amount, **before** any signature is requested.
- [ ] Given a member who is copying, when an order is routed on their behalf, then the only
      charge attributable to flet is the published rate applied to that order's notional.
- [ ] Given a member who lost money over a month, when they ask what they owe flet, then the
      answer is nothing beyond the per-order fees already taken at execution.
- [ ] Given an administrator configuring their server, when they open every available
      setting, then none of them changes, adds to, or waives the rate.
- [ ] Given a member for whom no order was routed during a period, when that period ends,
      then flet has taken nothing from them.
- [ ] Given a member who revokes their agent approval, when they check afterwards, then no
      further charge has been taken.

---

## Success criterion

> We will consider this was the right call if **at least 20 members, across at least 5
> communities, have been copying continuously for 30 days, and the commission collected over
> that month exceeds 1,000 €** is observed before **2027-03-21**.

The figure is deliberately below the forecast: `discovery.md` puts five base-case communities
at about 1,900 € a month, so 1,000 € is the conservative half of an assumption that has not
yet been tested.

How it is observed: the builder fee credited on-chain to flet's address over the month, and
the count of members holding an active agent approval throughout it.

If the criterion is not met: first establish whether the shortfall is **adoption** or
**rate** — they call for opposite corrections. Adjust the rate only if the member's cost is
shown to be what stopped them. Supersede this PDR if a flat commission cannot fund the
service at any reachable number of communities.

---

## Removal condition

> This decision will be removed if **the venue withdraws builder codes, or caps them below a
> rate at which the service can be funded** — or if **the legal opinion finds that taking a
> fee on routed volume is itself what makes the operator a regulated provider, where another
> model would not**.

The second condition is live, not hypothetical: it is question 8 of
`docs/project/legal-scoping-request.md`.

---

## Impacts

- **Existing users**: none. No user exists, and no migration is owed.
- **Modules and contracts**: no module exists yet. When the first one is created, the rate is
  a single configuration value of the product, never a per-community setting, and the
  acceptance criteria above are its oracle.
- **Support and documentation**: the rate belongs on the screen before the signature, not in
  a terms page. A member who discovers the cost after signing is a support failure, not a
  documentation gap.
- **Data**: this decision **removes** a data need. Because flet is never paid on gains, it
  needs no position history, no realised-profit accounting and no billing records for any
  member. That is worth defending against future convenience: the moment flet starts
  computing a member's P&L for its own revenue, it has acquired both the ledger and the
  relationship this decision exists to avoid.
