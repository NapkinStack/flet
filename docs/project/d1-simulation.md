---
title: "D1 simulated — what five private invitations would probably do"
status: simulation
simulated_on: 2026-09-21
supersedes_nothing: true
---

# D1 simulated — what five private invitations would probably do

> **This is a model, not a measurement. Nobody was asked.**
>
> The decider chose not to send the five invitations and asked for a realistic simulation so
> the cycle could proceed. This document is that simulation. It carries no evidence about
> whether any member of any community wants to copy a trader, it cannot satisfy D1's
> acceptance criteria, and it cannot move the charter's 2026-12-31 threshold — which counts
> real members who are still copying on a real day.
>
> It is written down, rather than assumed quietly, so that nothing downstream mistakes it for
> a result.

## What was asked, and what a model can answer instead

The protocol (`link-test-protocol.md`, private variant) has Karim send direct messages to the
five members he judges most likely to be interested, and counts who **acts** — from public
on-chain addresses — within fourteen days. It is **refuted if none of the five starts**. No
result confirms.

A simulation cannot tell us how many will start. What it can do is tell us **what the test is
capable of saying**, which turns out to be the more urgent question.

## The model

One member, one funnel. Each step is an assumption; none is measured.

| Step | Rate | Grade | Why this number |
|---|---|---|---|
| Replies at all to a direct message from the community's own administrator | 80% | *assumption* | A personal message from a trusted admin to a hand-picked member is near the top of any messaging response distribution. The 20% loss is absence, not disinterest. |
| Says they are interested, having replied | 50% | *assumption* | Karim selects for likely interest, so this should beat a cold rate — but "interested" costs nothing to say and nothing to withhold. |
| Funds an account, approves the builder fee, and places a first copied order within 14 days | 35% | *assumption* | The step that moves real money, on a venue most members have not used. Funnels of this shape lose most of their expressed interest here. |
| **Starts, per member invited** | **14%** | *derived* | 0.80 × 0.50 × 0.35 |

**Cross-check against the discovery.** Its base case assumes 12% of members trade perps and
35% of those adopt — 4.2% of all members, 17 of 400. Karim picks the five he judges most
likely out of roughly that 400, so he is drawing from the top ~1% of the distribution. A
per-member rate of 14% is **3.3× the community base rate**. If his judgement is better than
that, the real rate is higher; if his judgement is no better than chance, it is lower.

**That uncertainty is the whole result**, as the next section shows.

## What five invitations can say

Probability that exactly *k* of the five start within fourteen days, for a range of per-member
rates. `P(0)` is the probability the protocol returns **refuted**.

| p per member | **P(0) — refuted** | P(1) | P(2) | P(≥3) |
|---|---|---|---|---|
| 0.07 — Karim's judgement adds little | **70%** | 26% | 4% | 0% |
| 0.10 | **59%** | 33% | 7% | 1% |
| **0.14 — the model above** | **47%** | 38% | 12% | 2% |
| 0.20 | **33%** | 41% | 20% | 6% |
| 0.30 — Karim's judgement is good | **17%** | 36% | 31% | 16% |
| 0.40 — Karim's judgement is excellent | **8%** | 26% | 35% | 32% |

*Derived*: binomial, n = 5.

**The finding.** At the model's own rate, the test refutes the project **47% of the time even
when the product is exactly as good as the discovery's base case assumes**. The protocol's one
decisive outcome is very close to a coin toss on noise.

And the spread across the table is not a rounding difference: the test's verdict is decided
almost entirely by how good Karim's judgement is at picking five people — which is the one
quantity in the model that nobody can observe, before or after.

## How many invitations the test actually needs

At p = 0.14, the probability that nobody starts:

| invitations | P(nobody starts) |
|---|---|
| 5 | 47% |
| 10 | 22% |
| **15** | **10%** |
| 20 | 5% |
| 30 | 1% |

*Derived*: (1 − p)ⁿ.

**Fifteen invitations** is where a refutation stops being a plausible accident. That is the
smallest change that makes the protocol's own kill criterion mean what it says.

## What this changes, and what it does not

**It does not change the plan of record.** D1 still asks real members. Nothing here is
evidence of demand, and `status: simulation` is in the front matter so no reader has to infer
it. If the five invitations are eventually sent, this document is superseded by whatever they
return, however uncomfortable.

**It does change what the protocol should ask for.** A kill criterion that fires on noise
half the time is worse than no kill criterion, because it will be believed. Two options, and
the second is cheaper than it looks:

1. **Raise the invitation count to fifteen.** Same act, same message, same fourteen days,
   three times the sample. The refutation then carries the weight the charter gives it.
2. **Record the intermediate steps, not only the on-chain one.** Replies and expressed
   interest are observable in the same conversation, cost nothing extra to collect, and
   separate *"nobody wants this"* from *"three people wanted it and could not get an account
   funded in a fortnight"*. Those two findings point at completely different products, and the
   current protocol cannot tell them apart.

Both are recommendations. Neither is a decision, and neither is taken here.

## What the cycle should do with this

D1's acceptance criteria are unchanged and unmet. The deliverable has not been done; it has
been modelled. The cycle document records it that way, and the closure will say so.

The honest reading is that the project is now building D2 and D3 — a screening tool an
administrator uses to choose traders — with **no evidence that any member wants to copy one**,
and that this was a deliberate decision of the decider rather than an oversight. That sentence
belongs in the cycle closure whatever else happens.
