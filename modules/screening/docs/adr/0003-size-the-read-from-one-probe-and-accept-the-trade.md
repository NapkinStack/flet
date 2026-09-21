# ADR-0003 — Size the window read from one probe, and accept the trade it forces

- **Status**: Accepted
- **Date**: 2026-09-21
- **Deliverable**: cycle 02, D2

## Context

The venue answers at most 2000 fills per call, ascending, and meters by weight. To read a
trader's last thirty days we walk backwards from now in chunks, and each chunk's span is
guessed from a single cheap probe — the venue's own most recent page.

That guess is the problem. **The probe measures the trader's newest fills, which for anyone
with a recent burst is the densest stretch of their month.** Size every chunk from it and the
quiet weeks are walked at spike-sized paces; size them generously and a chunk lands on dense
ground it cannot finish, and the work it did is thrown away.

Four rounds of independent verification went into this one heuristic. Each round moved the
loss rather than removing it:

| round | what it fixed | what it broke |
|---|---|---|
| 1 | the read direction — S8, a window eleven days stale | quiet-month-then-burst traders: 0.07 of a day where the previous read held 30 |
| 2 | chunk growth | quiet-ground-then-wall traders: 4 days where the previous read held 12 |
| 3 | a retry when a chunk overshoots | the cut and the growth oscillated over the same ground |
| 4 | a memory of spans known to overshoot | the author's claim of live parity: 1.68× and 2.00× behind the previous head at two of three sampled timestamps, and one shape behind **both** predecessors |

The kernel says three consecutive attempts on one fix means the problem is in the framing
(`AGENTS.md` §3). This is the fourth.

## Decision

**Keep the single-probe heuristic, and stop tuning it inside this deliverable.**

`_CHUNK_READS = 3`. The constant is a genuine trade and the file now says so with both sides
measured: three wins the shapes where dense ground sits behind quiet ground, ten wins a dense
trader with a recent burst at some timestamps and is identical at others. Three is chosen
because its advantage is systematic and ten's is intermittent.

**Record the structural answer rather than attempt it.** A chunk that overshoots has read its
older part completely; only its newest slice is missing. Stashing that prefix and retrying
only the gap would waste nothing and remove the trade entirely. It is not taken here because
it makes the no-hole invariant span two loop iterations, and this deliverable has already
traded one defect for another three times.

## Consequences

**Accepted.** On some traders the window is shorter than the read this replaces would have
given — up to 2× at some timestamps on the live address. That figure is a ratio on purpose:
pinning `now_ms` does not make the comparison reproducible, because the probe reads the
trader's newest fills as of the request rather than as of the pinned instant, so absolute day
counts drift within the hour while the ratio holds. The answer states the dates it
holds and the factor it extrapolated by, so a short window is visible rather than silent.
That is the property the module's rules require; it is not a reason to call the trade
acceptable forever.

**Guarded.** Nineteen tests pin the read's behaviour, and the shapes that broke each round are
among them. Any future change to the heuristic has to keep them.

**Owed.** The prefix-stashing read is a deliverable of its own, with its own ADR and a fixed
shape set as its dated success criterion. Until it exists, the trade above is the module's
known limit and should be quoted whenever the window is short.

## Success criterion

By **2026-12-31**, either the prefix-stashing read is built and every shape in the fixed set
is read at least as deeply as the best of `81050b7` and `c8a8227`, or this ADR is revisited
and the trade is re-decided with whatever traders real administrators have actually curated
by then — which is better evidence than any shape we can invent.

## Removal condition

If the venue ever offers a descending read, or a count of fills in a range, the probe and
every constant here become unnecessary and this ADR is superseded outright.

## Alternatives considered

- **Raise `_CHUNK_READS` to 10.** Measured: closes the live gap completely at the timestamps
  where it appears, costs 6.0 → 4.0 days on one wall shape and 13k → 1k fills on another.
  Rejected because the cost is systematic and the benefit is not.
- **Drop the budget and read until done.** This is what the code before D2 did. It made up to
  40 heavy reads and was refused by the venue with 429 on a live trader.
- **Ask for a smaller window than thirty days.** Moves the arbitrariness into the question
  instead of the answer, and every monthly figure would still be an artefact of it.
