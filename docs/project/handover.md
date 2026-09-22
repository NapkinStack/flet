---
title: "Handover — where the project stands and how to resume"
updated_on: 2026-09-22
---

# Handover — where the project stands and how to resume

> Written so a session with no memory of the work can pick it up. Everything below is
> reconstructible from the repository; this file is the map, not the source. Where it
> disagrees with the charter, a cycle, an ADR or a PDR, **those win**.

## Where the project is, in one paragraph

flet is a bot that lets a community's administrator offer curated copy trading to its members
on Hyperliquid, taking a flat commission on routed volume and never custody. The discovery is
done and challenged (`go`). Cycle 01 was stopped and reframed. **Cycle 02 runs 2026-09-21 to
2026-10-12**: D1 is `deferred`, D2 is `accepted` and merged, D3 is built and in verification.
The module that matters most — copying — **does not exist yet**, and that is the honest
headline.

## Repository state

| | |
|---|---|
| `main` | `9f1135c` — D2 merged (#20), ADR-0002 (#22), pilot FAQ and declared demand (#23) |
| `d3/three-verdicts` | `b41e6f6` — 75 tests, `nstack check` green, **no PR open yet** |
| `pdr/revise-the-pilot-criterion` | `11e1905` — pushed, PR to open |
| `ops/how-we-verify` | this branch — ADR-0003 and this file |

Older branches are merged or superseded and can be ignored. `nstack doctor` reports compliant;
`nstack plan` and `nstack fitness` are compliant.

## What is in flight

**D3 — three verdicts.** `COPYABLE` / `COPYABLE WITH RESERVATIONS (…)` / `NOT COPYABLE (…)`,
exit codes 0/1/2/3 by severity, four reservations (fees, reproducibility, concentration,
extrapolation) and a ceiling past 30× that refuses to answer at all.

It has been through **six verification rounds**. The last one returned `failed` with three
blockers; all three are fixed at `b41e6f6` and five mutants re-checked as caught, **but that
re-check was done by the author**. What it still needs:

1. A **confirmation run** by a delegated verifier at the head — not a seventh adversarial
   round (ADR-0003 caps `high` modules at one, and this module is long past it). T4 requires
   the sheet to be dated at the head commit, and it has refused that argument before.
2. The PR opened with that sheet, signed under the verifier's own agent identifier
   (ADR-0002), and the over-budget label with its justification: ~700 lines, indivisible
   because every intermediate point is an exit-code scheme that means two things at once.

## Decisions taken, and where they live

| Decision | Where |
|---|---|
| Two GitHub identities: the App commits, the token configures | `docs/adr/0001` |
| A delegated session may verify, signing as itself | `docs/adr/0002` |
| Verification budget follows criticality; no unasked change inside a fix | `docs/adr/0003` |
| Commission on routed volume, never a share of gains | `docs/pdr/0001` |
| Three verdicts, four reservations, the extrapolation ceiling | `docs/pdr/0002` + its amendment |
| Closed pilot of 5–8 before any funnel; criterion 1 replaced | `docs/pdr/0003` |
| The read is sized from one probe, and the trade that forces | `modules/screening/docs/adr/0003` |

## Open, and belonging to the decider

- **The legal opinion.** Requested, pending. Phase 2 is gated on it.
- **The five (or fifteen) DMs.** Ten traders and twenty members have said they want to test
  the bot — *reported*, private, not observed. Nobody has acted. D1 stays `deferred`.
- **`.claude/` project settings and hooks** are untracked and deliberately not gitignored: the
  team is meant to share them. They are masked as character devices inside the agent's
  sandbox, so the agent cannot read them and will not commit what it has not read. **A human
  needs to add them.**

## Next, in order

1. Confirmation run on `d3/three-verdicts` → open its PR → merge.
2. Open and merge `pdr/revise-the-pilot-criterion` and `ops/how-we-verify`.
3. **Close cycle 02.** Its closure owes one sentence, already promised: *the project built a
   tool for choosing traders with no evidence that any member wants to copy one, and that was
   a decision rather than an oversight.*
4. **Upgrade the framework at the cycle boundary, not before.** NapkinStack 0.6.1 exists;
   it changes only two `nstack init` error messages and no template file, so it cannot affect
   this project mid-cycle. Upgrading the CLI without `nstack update` would turn doctor's L1
   red. Sequence: `uv tool install napkinstack --force`, then `nstack update`, then
   `nstack doctor`. **The framework moved 0.3.0 → 0.6.1 in three days: re-check this at every
   cycle boundary rather than when someone remembers.**
5. **Frame cycle 03 around the copying module.** It is `critical`. Two things are not
   negotiable and they are tests, not process: the agent key can place orders and nothing
   else, and revocation works. Two commitments from `pilot-faq.md` must be framed *with* the
   module rather than around it: the notice shown **before** a member acts, and revocation as
   a first-class path.

## How to work in this repository

- **GitHub:** `gh-agent` only — a project hook refuses the direct CLI. The App commits and
  pushes; the fine-grained token configures the repository and cannot push. Merging requires
  the decider's approval; the agent cannot self-approve.
- **`git config`, remotes:** never `--global`. `GIT_CONFIG_GLOBAL` already points at
  `workspace/flet/.gitconfig`, which is workspace-scoped on purpose; `~/.gitconfig` is
  untouched and shared with other projects.
- **Mutation testing:** `PYTHONDONTWRITEBYTECODE=1`, clear `__pycache__` between mutants, and
  **verify each patch actually applied before reading its result** — a `sed` that silently
  matched nothing has already been read as "survived".
- **Exit codes:** measure without a pipe (`cmd >/dev/null 2>&1; echo $?`). A pipe reports the
  last command's status and has misled in this project.
- **Live runs** need `allowed_domains` including `api.hyperliquid.xyz`; the venue answers 429
  under repeated hammering, which is itself a scenario.
- **Check gates by their own exit status**, not by a command chained after a `tail`. A gate
  whose output is printed and not read is the same as no gate, and that has shipped a failing
  commit once.

## What this project has learned about itself

Six verification rounds on one read-only function produced eleven real defects. **Three of
them the author introduced in later rounds**, in changes nobody had asked for, and **nine
fixtures written by the author proved nothing** — one of them passing against the very commit
it was written to fail against.

That is why ADR-0002 exists, why ADR-0003 exists, and why the copying module gets adversarial
verification without a cap while `screening` gets one round. It is not ceremony. It is the
measured behaviour of the thing writing the code.
