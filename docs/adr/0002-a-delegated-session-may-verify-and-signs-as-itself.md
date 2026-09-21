# ADR-0002 — A delegated session may verify, and signs under its own identifier

- **Status**: Accepted
- **Date**: 2026-09-21
- **Supersedes nothing. Complements** [ADR-0001](./0001-split-the-agent-github-identity-in-two.md).

## Context

T2 requires that the verifier of a change is not one of its authors, and checks it
mechanically: the verifier named in the test sheet must not appear in the `Agent-Session`
trailer of any commit in the pull request.

On cycle 02's D2 the check refused a sheet, and it was right to by its own rule. The
verification had run as a **delegated session** — a separate agent, spawned for the purpose,
with its own context. All commits are written by the parent session, because a delegated
session cannot commit. So the sheet was signed with the parent's identifier and T2 saw the
author verifying their own work.

What the rule is for was nevertheless satisfied, and the record shows it. Across five rounds
that verification:

- found **eight defects**, two of which the author would have shipped;
- refused to merge **three times**;
- showed **five of the author's test fixtures** to prove nothing — including one that passed
  against the very commit it was written to fail against;
- disproved **four of the author's measurements**, one of which the author had already
  written into a commit message as fact.

Every one of those went against the author's interest. That is the independence T2 exists to
buy, and the check was refusing it on an identifier rather than on substance.

## Decision

**A delegated verifier session is a valid verifier, and signs the sheet with its own agent
identifier** — the one the harness assigns it, never the parent's, and never an invented one.

Three conditions, all of which must hold:

1. **It starts fresh.** A session that inherits the author's context is the author. The
   verifier reads the repository, the playbooks and the deliverable's acceptance criteria for
   itself.
2. **Its brief asks it to attack.** The author writes the brief, which is the real weakness of
   this arrangement — a brief can be written to find nothing. So the brief must ask for
   failure, name the scenarios from the acceptance criteria rather than from the
   implementation, and say that a `failed` verdict is a successful verification.
3. **Its refusals are recorded.** What it found goes into the pull request whether or not it
   flatters the change, and a verdict of "I would not merge" stops the merge.

## Consequences

**Accepted.** The author chooses the verifier's brief, so a lazy brief produces a lazy
verification and nothing in the machinery detects it. This is a real hole and the mitigation is
social, not mechanical: the sheet carries what the verifier found, and a sheet with no findings
across a large change is itself a signal.

**Accepted.** Two agents of the same model share blind spots. A delegated verifier is weaker
than a human reviewer and weaker than a different model. It is not weaker than no verifier,
which was the alternative on offer.

**Not accepted.** This does not licence signing a sheet with any identifier that makes the
check pass. The identifier written is the verifier's actual one; if no verification ran, the
sheet says `not verified`.

**Owed.** When the harness gives delegated sessions their own `Agent-Session` trailer, this ADR
becomes unnecessary and T2 works as written.

## Success criterion

By **2026-12-31**, every pull request in this project that changed a module carries a sheet
signed by a session other than its author's, and at least one of them records a refusal that
changed the code. If no verification ever refuses anything, the arrangement is decorative and
this ADR should be revisited rather than trusted.

## Removal condition

If a delegated verifier signs a sheet for a change that a later reader finds defective in a way
the scenarios covered, this ADR is suspended and verification goes to a human or a different
model until the cause is understood.

## Alternatives considered

- **The decider verifies each change themselves.** Correct, and unaffordable: 1402 lines for
  one deliverable, at half-time, with a 31 December kill date.
- **Waive T2 case by case.** A rule waived when inconvenient is not a rule. This ADR states
  when the rule is satisfied, which is a different thing from setting it aside.
- **Sign with the parent identifier and let CI fail on every module change.** A check that
  always fails is a check nobody reads, and it would have hidden the next real T2 violation.
