---
goal: "Receive one contribution from outside the organisation, made from a fork without write access"
status: accepted
appetite_days: 20
start: 2026-11-25
end: 2026-12-15
deliverables:
  - id: D1
    title: "The step that sizes the next slice of a long read is pinned by tests: `_resize` is covered on each of its three branches"
    module: screening
    state: ready
    acceptance:
      - "Given a slice that needed more than one read (`spent` above 1), when `_resize` is asked for the next span, then it returns the span divided by the reads spent, and never less than 1 millisecond"
      - "Given a slice that held at least half a page of fills (`got` at or above `PAGE_SIZE // 2`) after a single read, when `_resize` is asked, then the span is returned unchanged"
      - "Given a slice that held fewer than that, when `_resize` is asked, then the span grows by the target divided by the fills held, at least 2 times and at most 16 times, and an empty slice grows it by exactly 16 times"
      - "Given the new tests, when `uv run pytest` runs in `modules/screening`, then they pass, no other test changes, and `src/` is untouched"
---

# Cycle 04 — A contribution from a fork

> One accepted cycle at a time; no automatic extension. The end date is a circuit breaker.

## Goal

Rehearse contributing without write access: a person outside the organisation forks the
repository, makes one small change, and opens a pull request from the fork. The change itself
matters little; the path is what is being tried, and every friction met on it is what the cycle
is for.

## Deliverables

### D1

`_resize` in `modules/screening/src/screening/venue.py` is a pure function (three integers in,
one integer out) with three branches and no test of its own: `grep -rn resize modules/screening/tests`
finds nothing. It suits an outsider because it needs no secret, no credential, no network and no
knowledge of the venue; its docstring states the behaviour, and the constants it reads
(`PAGE_SIZE`, `_CHUNK_LOAD`, `_MAX_GROWTH`) are in the same file. About an hour.

The tests go in a new file under `modules/screening/tests/`. They import the private name
directly; that is the point, since the function is only reachable through a long read otherwise.
This deliverable changes tests only: a behaviour the tests disagree with is reported, not fixed
in the same pull request.

## What needs a person

| Deliverable | Who | The literal gesture |
|---|---|---|
| D1 | The outside contributor | Fork the repository on the forge with an account that has no write access, clone the fork, branch, add the tests, run `uv run pytest` in `modules/screening`, push to the fork and open a pull request against the upstream default branch |

## Out of scope

- Any change under `modules/screening/src/`, and any other module.
- Granting the contributor write access, a label or a role.

## Later

- What the rehearsal shows about the contribution path, for the next framing.

## Open questions

**Blocking:** none.

**Not blocking:**

- Whether the checks that need a secret or a label run for a pull request from a fork; this is
  what the rehearsal observes.

## Closure

<Written at the end of the cycle.>

**Documents brought current:** <none yet>
