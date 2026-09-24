---
goal: "Find out whether anyone wants this, and make the key a member hands flet safe to give and safe to take back"
status: accepted
appetite_weeks: 3
start: 2026-09-24
end: 2026-10-15
deliverables:
  - id: D1
    title: "Spike — does an administrator's vouching move anyone? Five private invitations, read at day 14"
    module: null
    state: ready
    acceptance:
      - "Given docs/project/link-test-protocol.md, private variant, when the cycle starts, then the five messages are sent within 3 days and the administrator's reason for choosing each member is recorded as the stated bias it is"
      - "Given day 14, when it is reached, then the number who actually started is read from their public addresses — refuted at 0 of 5, and no result confirms"
      - "Given any reading, when it is recorded, then each figure carries its grade: on-chain, or declarative"
  - id: D2
    title: "A member can hand flet a key that places orders and nothing else, and take it back"
    module: copying
    state: ready
    acceptance:
      - "Given a member who has authorised nothing, when they authorise flet on the venue, then one agent key exists for them, and its scope and expiry are read back from the venue rather than asserted by us"
      - "Given that key, when a withdrawal is attempted with it, then the venue refuses and the refusal is recorded — and the same for a transfer between accounts and for a change of the account's permissions, one test per action the key must not be able to perform"
      - "Given a member who revokes, when they revoke, then an order placed with that key afterwards is refused by the venue, verified by attempting one rather than by trusting our own state"
      - "Given a revoked or expired key, when anything in flet would act for that member, then it does not, and nothing retries — the absence is asserted, not assumed"
      - "Given the key at any point in its life, when the logs, the process output and the repository are searched for it, then it appears in none of them, and where it is held and for how long is stated"
  - id: D3
    title: "A member is told what they are getting into before they act, not after"
    module: copying
    state: ready
    acceptance:
      - "Given a member about to authorise for the first time, when they are asked, then the notice is shown before the authorisation and states all four: that flet is not authorised by any regulator, that the legal opinion is pending, that positions are leveraged, and that they can lose everything"
      - "Given that notice, when the member does not acknowledge it, then no key is created, nothing is authorised, and the member is not asked again in the same exchange"
      - "Given a member who has acknowledged, when the acknowledgement is recorded, then it carries the date and the notice's version, so that a later change to the wording cannot be mistaken for what they agreed to"
---

# Cycle 03 — A key given, and taken back

> One accepted cycle at a time; no automatic extension. The end date is a circuit breaker.

## Goal

Two questions again, and the same asymmetry as cycle 02: one costs five messages, the other is
the most dangerous code this project will write.

**Does anyone want this?** Still unanswered after a discovery, two challenges and two cycles. D1
has been deferred twice, so this is the third time it appears on a day one. The charter's five
phase-1 criteria all sit behind it, and the alternative is to build a `critical` module for a
demand nobody has observed.

**And can a member hand flet a key without handing it their money?** `copying` holds an agent key
and acts for someone. It is the first `critical` module in this project, and the two things that
are not negotiable about it are tests, not process: **the key can place orders and nothing else**,
and **revocation works**.

## Deliverables

**Order.** D1 on day one — it is somebody else's calendar and a fourteen-day clock, and it has
been the first casualty of two cycles. D2 before D3: the notice guards an action that must exist
before it can be guarded. D2 and D3 are both `copying`, so they are sequential, one pull request
per module.

**The module is created when this cycle is accepted**, not before:
`nstack new-module copying NapkinStack/maintainers critical`, declared `user_facing`, since a
member sees what it does.

**What the acceptance criteria are built to refuse.** Every criterion on D2 names the venue, not
our own state, as the thing that answers. A key we *believe* is scoped, a revocation we *record*
as done, a retry we *think* stopped — those are the three ways this module can be wrong while
every test we own is green. So the scope is read back from the venue, the revocation is checked by
attempting an order after it, and the absence of action is asserted rather than assumed.

**Verification.** `critical` means adversarial rounds without a cap, until the verifier signs
(ADR-0003). That is deliberate and it is not the cap cycle 02 was given: a wrong figure in a
screening report is visible to an administrator who can re-run it, while a wrong order here is a
member's money. The lesson cycle 02 paid six confirmation runs to learn applies to the briefs:
**state the general form first.** A guarantee written per-instance produces one refusal per round.

## Out of scope

- **Copying an order.** No fill of a trader's is reproduced in this cycle. That is the next
  cycle's deliverable and it is what produces the charter's *zero unchosen divergence* criterion.
  Said plainly because it is the obvious thing to reach for once a key exists, and reaching for it
  is how a three-week appetite becomes five.
- **The acquisition funnel, a landing page, a waiting list.** Phase 2, gated on the legal opinion
  and on every phase-1 criterion (PDR-0003).
- **Anything on Telegram.** §7 of its Bot Developer Terms closes the Mini App path for a non-TON
  venue, and the decider has accepted excluding it.
- **The `screening` follow-ups** recorded in #26, including input validation and the threshold
  calibration. They belong with an observability and hardening batch, or with the PDR's own
  success-criterion review.

## Later

- **The first copied order**, and with it *zero unchosen divergence* and the confrontation of
  `screening`'s predictions with a member's actual fills — the most valuable of the five phase-1
  criteria, and the one only a real pilot produces.
- **Observability**, carried from cycle 01 for the third time: the retry-rate metric, the
  unrecorded 429 deviation, and a 60-second budget that is per call where one invocation makes
  several. It is now carried by two modules instead of one.
- **The Discord application and its verification prerequisites**, at 75 servers.
- **The install-to-active ratio**, measured rather than judged.

## Open questions

**Blocking:** none once this cycle is accepted.

**Not blocking:**

- **The written legal opinion**, requested and pending. It gates phase 2, not this cycle. D3's
  notice says it is pending, which is the honest statement while it is.
- **Whether an agent key can register another agent**, and whether the venue's internal transfer
  actions accept an agent signature. The venue's documentation is silent, and D2's second
  criterion is written to find out by attempting it rather than by reading about it.
- **The date on the phase-2 commission criterion**, owed by the decider since PDR-0003 moved it
  "with a later date" and named none. Recorded in the charter's open questions.
- **Whether the administrator sends the five messages within three days.** Their calendar, for the
  third cycle running.

## A note the framer owes this cycle

The decider was offered three sizes and chose the middle one: **three weeks for the key, its
revocation and the notice, with no copied order.** The other two were two weeks for the key alone,
which would have left the pilot FAQ's pre-action notice unhonoured, and five weeks through to a
first copied order, which is a long appetite on `critical` code.

They also chose D1 in, on day one, for the third time. Recorded because cycle 02's closure said
that deferring it a third time would be the project's answer about what it is really doing — and
the answer given was the other one.

**What cycle 02 says to watch here.** Its appetite was sized for work cycle 01 had already done,
so both engineering deliverables landed in three days and nineteen days went unspent while the one
deliverable that needed somebody else's calendar did not move. Three weeks for a module that does
not exist yet is a different bet, but the failure mode is the same shape: **if D1's messages have
not gone out by day three, this cycle is already repeating both of its predecessors**, and that is
worth a look on day three rather than at the end.

## Closure

<Written at the end of the cycle.>
