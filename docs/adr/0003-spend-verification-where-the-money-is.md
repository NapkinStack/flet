# ADR-0003 — Spend verification where the money is, and stop tidying inside fixes

- **Status**: Accepted
- **Date**: 2026-09-22
- **Complements** [ADR-0002](./0002-a-delegated-session-may-verify-and-signs-as-itself.md)

## Context

Cycle 02 spent **six independent verification rounds** on `screening`'s window read. The
module is `high`, read-only, holds no key and places no order. The rounds were not wasted —
they found eleven real defects — but the decider named the cost plainly: *too many constraints
become a real brake on progress*, and the project is at half-time against a 2026-12-31 kill
date with the `critical` module not yet started.

Reading the eleven defects by origin tells a second story:

| Origin | Count |
|---|---|
| Defects in the original implementation | 4 |
| Defects the author **introduced in a later round**, in changes nobody asked for | 3 |
| Fixtures of the author's that proved nothing | 9 across the cycle |

Three of the round-six blockers did not exist before round five. Each came from tidying
inside a fix: a guard removed as "unreachable" on a reason that was false, an assertion
deleted while rewriting the test around it, a reorder made because the code read better that
way. The verification rounds were not finding a module that resisted being fixed; they were
finding a fixer who kept changing more than was asked.

## Decision

**Two rules, one about where to spend and one about what not to do.**

### 1. The verification budget follows criticality

| Criticality | Budget |
|---|---|
| `high` or below, read-only | **One round.** Blockers are fixed; everything else becomes a recorded follow-up. No second adversarial round — a confirmation run at the head for T4 is not a round |
| `critical` — holds a key, places an order, moves money | **Adversarial rounds without a cap**, until the verifier signs |

The module's criticality is already declared in its MANIFEST, so this needs no new field and
no judgement in the moment.

### 2. A fix changes only what the finding names

No unasked change inside a correction. Something that looks worth cleaning becomes a line in
the follow-up list, not an edit in the same commit. This is free, and it would have prevented
three of cycle 02's blockers.

## Consequences

**Accepted.** Less verification on read-only modules means some defects ship there. That is
the trade, taken deliberately: a wrong figure in a screening report is visible to an
administrator who can re-run it, while a wrong order in the copying module is a member's
money.

**Accepted.** "No unasked change" will sometimes leave code the author knows is untidy. The
follow-up list is where that goes, and a follow-up list nobody reads is the failure mode to
watch.

**Not accepted.** This does not reduce what a `critical` module must show. Two things are not
negotiable there and they are tests, not process: the agent key can place orders and nothing
else, and revocation works. They cost an hour; not having them costs the project.

## Success criterion

By **2026-12-31**: no deliverable of a `high` module has taken more than one adversarial
verification round, and no blocker on any module has been traced to a change the finding did
not name. If either happens, the rules did not bind and this ADR needs teeth rather than
restating.

## Removal condition

If a `high` module ships a defect that reaches a member's money, the first rule is wrong and
the budget goes back up. That is the event to watch for, and it is worth more than any
argument about proportion.

## Alternatives considered

- **Keep the same depth everywhere.** What cycle 02 did. It produced a well-tested read
  function and no copying module, which is the wrong artefact to have polished.
- **Cap rounds by count on every module.** A cap on `critical` work is a promise to stop
  looking before the answer arrives, on the code that holds the key.
- **Drop independent verification on `high` modules entirely.** Four of the eleven defects
  were in the first round. The first round is the one that pays.
