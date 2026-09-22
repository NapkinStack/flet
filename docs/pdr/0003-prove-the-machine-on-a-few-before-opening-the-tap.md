---
status: proposed
decider: "@napkinstack-admin"
---

# PDR-0003 — Prove the machine on a few, before opening the tap

- **Status**: Proposed
- **Date**: 2026-09-22
- **Decision makers**: @napkinstack-admin, who decided the direction on 2026-09-22; the framer
  proposed the numbers and the shape
- **Modules affected**: the copying module, which does not exist yet, and every launch
  decision after it
- **Supersedes**: success criterion 1 of the charter

## Context

The charter's first success criterion — *at least 20 members still copying 30 days after they
started, observed on 2026-12-31* — was set before the project had a single datum. It now has
one, and the criterion is arithmetically out of reach:

```
20 members interested (reported 2026-09-21)
  × 35–60 %   connect and place a first copied order
  × 50–70 %   are still copying at day 30
  ─────────
  = 3.5 to 8.4 members        the criterion requires 20
```

Reaching 20 would need 48 to 114 interested members. The decider chose to revise rather than
widen, and gave the reason: **onboarding many users prematurely is dangerous for this
product.**

That reason is right, and for reasons more specific than caution:

- **A defect here does not produce a bad page, it produces a liquidation.** The blast radius
  is linear in user count. Five affected members can be made whole out of pocket; two hundred
  cannot, on an 8,000 € budget.
- **The regulatory exposure scales the same way.** ESMA's supervisory briefing places copy
  trading under portfolio management or investment advice, and in France providing the service
  unauthorised carries two years and 30,000 €. The legal opinion is requested and pending. A
  closed pilot with informed participants is materially different from an acquisition funnel
  taking strangers.
- **The defect density is measured, not assumed.** Six verification rounds on one read
  function produced eleven real defects, two of which the author would have shipped and three
  of which the author introduced while believing he was fixing something. That is the module
  that holds no key and places no order. The copying module is `critical`.

## Decision

**Replace a count with evidence of quality, because a count is what a pilot cannot produce.**

At five to eight members, a threshold on a number is noise-dominated: the project's own
binomial model showed five invitations returning *refuted* 47% of the time while the product
was exactly as good as forecast. A criterion that fires on noise is worse than none, because
it will be believed.

### Phase 1 — closed pilot, 5 to 8 members, 2 to 3 traders, before 2026-12-31

| Criterion | Why this one |
|---|---|
| **Zero unchosen divergence** between the member's position and the vouched trader's: the copy is faithful, or it refuses and says so | It is the product's whole promise. If it drifts silently, nothing else counts |
| **Zero key incident**: the agent key can place orders and nothing else, throughout | A decider no-go, verified rather than asserted |
| **Every member revokes at least once, deliberately, and it works** | An exit that has never been used is not an exit |
| **≥ 60% of members choose to continue past day 14** | The only desire signal a pilot can honestly produce |
| **`screening`'s predictions confronted with reality**: fees actually incurred, share of orders refused, slippage between the trader's fill and the member's | The most valuable of the five, and only a small pilot produces it — it makes falsifiable everything the module has been asserting |

### Phase 2 — the acquisition funnel, gated on **two** conditions, not one

1. The written legal opinion received, and acted on.
2. Every phase-1 criterion met.

Build the funnel meanwhile — a landing page and a waiting list cost nothing and expose
nothing. **Do not open the tap.**

### What moves out

The commission criterion — *more than 500 € in a calendar month* — moves to phase 2 with a
later date. Five members cannot produce it, and keeping a criterion a pilot cannot reach is
the same mistake this PDR is correcting, in reverse.

## Expected behaviour

**Nominal:** the pilot runs with named members who have read `pilot-faq.md` and accepted that
nobody is authorised and that they can lose everything. Each phase-1 criterion is measured and
written down as it is observed, not reconstructed at the end.

**Degraded:** any key incident, or any unchosen divergence, stops the pilot the same day. Not
"is investigated" — stops.

**Business rules:** the pilot size is a **launch** parameter. It gates no deliverable and no
module. Nothing in the build waits on it.

## What this does not change

- The no-gos: never custody of funds or keys, never a promise of return.
- PDR-0001: a flat commission on routed volume, never a share of gains.
- The 2026-12-31 horizon. The date stays; what is observed on it changes.

## Success criterion

By **2026-12-31**, phase 1 has run with at least five members and all five criteria above are
answered — including with a "no". A pilot that produces five honest noes is a success of this
decision; a pilot that produces nothing because it never started is its failure.

## Removal condition

If phase 1 passes and phase 2 opens, this PDR is spent and the criteria that replace it are
the funnel's. If phase 1 cannot be run before 2026-12-31 — no copying module, or no members —
that is the kill signal the original criterion existed to give, and it must be read as one
rather than extended.

## Prior art

Two references, and no more, because this decision rests on the arithmetic above rather than
on precedent:

- **pvp.trade**, the one measured comparable in the discovery: same venue, same builder-code
  rail, 50,000+ monthly users claimed, $14,899 earned in its last 30 days — *excerpt*. It did
  not begin at that size, and neither can this.
- **ESMA supervisory briefing ESMA35-42-1428**, 30 March 2023 — *primary*. It places copy
  trading under MiFID II investment services, which is why the number of people exposed before
  the legal opinion arrives is a decision and not a detail.

## The cost, stated

**The commercial signal is lost for now.** Five people will teach nothing about willingness to
pay or unit economics, and 2026-12-31 will arrive without knowing whether the model holds.
That is a real cost. It is smaller than learning it at the same moment as an incident across
two hundred people.

**And a small pilot does not prove the system scales.** It proves it does not harm. Those are
different claims, and conflating them is how people ship. Five members will never reach the
concurrency and rate-limit paths two hundred will — the venue already answered 429 against the
read-only module. Phase 2 is a graduated ramp, not a switch.
