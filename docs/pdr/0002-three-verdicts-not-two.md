---
status: proposed
decider: "@napkinstack-admin"
---

# PDR-0002 — Three verdicts, not two

- **Status**: Proposed
- **Date**: 2026-09-21
- **Decision makers**: @napkinstack-admin, who delegated product decisions of this kind to the
  framer on 2026-09-21; recorded here rather than left in the conversation
- **Modules affected**: `screening`, and the copying module when it consumes this answer

> The PDR describes **what the product must do and why**, never its implementation.

---

## User problem

An administrator asks whether a trader can be copied by their members and gets **yes** or
**no**. Two independent verifiers, on two different commits, found the same thing: the yes is
not trustworthy.

Observed live, both times, on real traders:

- `COPYABLE`, exit **0**, with **71%** of the trader's fills unreproducible by a copier and a
  fee burden the command **itself** flags as *"the fees, not the strategy, will decide this
  member's result"*.
- `COPYABLE`, exit **0**, for a trader who placed a month's volume in **one day**, where the
  quoted monthly cost understates the next month by about thirty times.

The verdict turns on the venue's 10 USDC floor and on nothing else. The other three
measurements are printed underneath it, faithfully — and an administrator scanning a list of
candidates reads the headline, while a script reads the exit code and never sees a sentence.

This is not a display problem. **A two-state answer forces a grey case into the state that
says yes**, and yes is the state that puts a member's money somewhere.

## Goal

An administrator can tell at a glance, and a script can tell from the exit code, which of
three things is true: this trader can be copied; this trader can be copied but something about
them will cost the member; this trader cannot be copied at all.

## Out of scope

- **Ranking traders.** Copyability is arithmetic, not merit (ADR-0001 of the module). A grade
  is not a score, and nothing here orders traders against each other.
- **Deciding for the administrator.** The middle state exists to make them look, not to choose.
- Any change to what is measured. The four measurements stay exactly as they are.

---

## Prior art

**How is this problem solved elsewhere?**

| Product / reference | Solution chosen | What we keep from it |
|---|---|---|
| **Static analysis and security scanners** — linters, `gitleaks`, CI gates | Three outcomes — pass, warn, fail — each with its own exit code, so the human reading and the script reading agree | The shape, and the exit-code discipline. This is the closest analogue: a mechanical check whose middle state means "possible, and you should look" |
| **Credit decisioning** — approve, refer, decline | The middle state exists precisely because a binary forces an underwriter to guess on the marginal case, and the guess is systematically optimistic | The reason for having a middle state at all, and the name for what a binary does wrong |
| **Nutri-Score, EU energy labels** | One graded mark computed from several components, legible at a glance, components available underneath | The idea that a compound judgement can have one headline **and** stay auditable. Not the grade scale: five letters would imply a precision these four measurements do not have |
| **PRIIPs Key Information Document** — a 1–7 summary risk indicator | A single regulated number for a financial product's risk | Read and **rejected**: it compresses distinct risks onto one axis, and its weakness is exactly ours — a reader cannot tell which risk moved the number |

**The convention the user already knows:** where a mechanical check has a grey zone, the
answer has three states and the middle one names what to look at. Anyone who has read CI
output knows it.

**Why depart from it** — we do not. The current two-state answer is the deviation, and this
decision returns to the convention.

---

## Options considered

| Option | What the user experiences | Cost | Chosen? |
|---|---|---|---|
| Do nothing | `COPYABLE` on a trader whose fees the command itself calls decisive. Two verifiers found it; a third would too | 0 | No |
| Make the other three measurements **fail** the verdict | Fewer false yeses, and a flood of `NOT COPYABLE` on traders a member could follow with their eyes open. The bias swings from optimistic to useless | Small | No |
| **Three verdicts: copyable · copyable with reservations · not copyable** | The floor still decides possible from impossible. The middle state says possible, and here is what will cost you | Small: one enum, one exit code, the reasons already exist | **Yes** |
| A graded score, 1–5 | Comparable across traders, and invites ranking — which ADR-0001 rules out — while implying a precision four measurements do not carry | Moderate | No |

## Decision

**Three verdicts, and the exit code carries them.**

- **`COPYABLE`** — clears the venue's floor at this ticket, and none of the three reservations
  applies.
- **`COPYABLE WITH RESERVATIONS`** — clears the floor, and at least one of: the monthly fee
  burden is above the alert; more than half the trader's fills were posted and cannot be
  reproduced; the month's volume landed on a third or less of the window's days.
- **`NOT COPYABLE`** — does not clear the floor. The member cannot place this trader's orders
  at this ticket, whatever else is true.
- **`NO VERDICT`** — the venue could not be read, or the data cannot support an answer.

**Exit codes are renumbered to run by severity**: `0` copyable, `1` with reservations, `2` not
copyable, `3` no verdict. A script keeps the idiom it already has — `if code == 0` — and stops
getting a zero for a trader the command was warning it about. The renumbering is a breaking
change to the command's interface, and it is made now, before anything consumes it.

**The trade-off owned:** the middle state will be common. Most real traders sampled so far land
in it. A state that applies to most cases risks being read as noise — which is why it must name
its reservation in the same breath, and why the reservations are three specific tests rather
than a vague caution.

---

## Expected behaviour

**Nominal journey:** an administrator runs the command for a trader and a member ticket. The
first line states one of the four verdicts. The lines below state every measurement, as they do
today. When the verdict is `COPYABLE WITH RESERVATIONS`, the first line names which reservation
applies, so the headline alone is actionable.

**Edge cases and degraded states:**

- **Several reservations at once** — all are named, in the order fees, reproducibility,
  concentration. The verdict is the same.
- **The floor fails and a reservation would also apply** — `NOT COPYABLE` wins. Impossible
  beats expensive, and the reservations are still printed so the administrator learns why the
  trader is unsuitable twice over.
- **The window was cut short** — unchanged: the figures are named as extrapolated, and the
  reservation thresholds are applied to them as they stand.

**Business rules:**

- The floor alone decides `NOT COPYABLE`. It is the venue's rule, not ours.
- A reservation never turns into a refusal on its own, and never disappears from the output.
- The thresholds are one set of numbers for every administrator and every community. An
  administrator cannot tune them; a trader cannot be exempted.

**Permissions:** none. The command reads public data and takes no argument that changes a
verdict other than the ticket.

**Acceptance criteria** *(testable — this replaces the cycle's first criterion for D3, and the
change is recorded here as the framing playbook requires)*:

- [ ] Given a trader who clears the floor and trips no reservation, when the command runs, then
      the verdict is `COPYABLE` and the exit code is 0
- [ ] Given a trader who clears the floor with a monthly fee burden above the alert, when the
      command runs, then the verdict is `COPYABLE WITH RESERVATIONS`, the fee reservation is
      named on the first line, and the exit code is 1
- [ ] Given a trader who clears the floor with more than half their fills posted, when the
      command runs, then the verdict is `COPYABLE WITH RESERVATIONS` and the reproducibility
      reservation is named
- [ ] Given a trader who clears the floor whose volume landed on a third or less of the days,
      when the command runs, then the verdict is `COPYABLE WITH RESERVATIONS` and the
      concentration reservation is named
- [ ] Given a trader who does not clear the floor, when the command runs, then the verdict is
      `NOT COPYABLE` and the exit code is 2, whatever the reservations say
- [ ] Given the venue cannot be read, when the command runs, then the verdict is `NO VERDICT`
      and the exit code is 3

---

## Success criterion

> We will consider this was the right call if **an administrator, shown a trader that returns
> `COPYABLE WITH RESERVATIONS`, can say without reading past the first line what the
> reservation is** — observed on at least three administrators before **2026-12-31**, the
> decider's own deadline.

How it is observed: ask them. Three questions, no product.

If the criterion is not met: the middle state is not carrying its meaning. Correct by naming
the reservation more plainly, or supersede this PDR with the graded scale rejected above.

---

## Removal condition

> This decision will be removed if **the middle state applies to substantially every trader an
> administrator screens**, measured over the first fifty real screenings.

A state that is always on is not information, and at that point the reservations belong in the
measurements rather than in the verdict.

---

## Impacts

- **Existing users**: none — nothing consumes this command yet, which is exactly why the exit
  codes are renumbered now rather than later.
- **Modules and contracts**: the copying module will consume this verdict through a contract.
  That contract carries four states from its first version; adding one later would be a
  breaking change to a version someone relies on, and the expand/contract sequence that goes
  with it.
- **Support and documentation**: the module's `README.md` states the four verdicts and their
  exit codes. An exit code is an interface and is documented as one.
- **Data**: no change. The same four measurements, from the same public reads.
