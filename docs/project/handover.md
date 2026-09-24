---
title: "Handover — where the project stands and how to resume"
updated_on: 2026-09-23
---

# Handover — where the project stands and how to resume

> Written so a session with no memory of the work can pick it up. Everything below is
> reconstructible from the repository; this file is the map, not the source. Where it
> disagrees with the charter, a cycle, an ADR or a PDR, **those win**.

## Where the project is, in one paragraph

flet is a bot that lets a community's administrator offer curated copy trading to its members on
Hyperliquid, taking a flat commission on routed volume and never custody. The discovery is done
and challenged (`go`). **Cycle 01 was stopped and reframed; cycle 02 closed `shipped` on
2026-09-23** with D2 and D3 accepted and D1 never started. The `screening` module answers whether
a trader is copyable, in three verdicts with four exit codes, and it is merged. **The module that
matters most — `copying` — does not exist, no member has been asked whether they want any of this,
and neither of the charter's success criteria has moved.** That is the honest headline, and the
closure of cycle 02 says it at more length.

## Repository state

| | |
|---|---|
| `main` | D3 (#26), cycle 02's closure and the charter correction (#27), cycle 03's framing (#28), NapkinStack v0.6.1 (#29) |
| **Cycle 03** | **accepted, running 2026-09-24 to 2026-10-15.** D1 a spike, D2 and D3 on `copying` |
| `screening` | 81 tests, `nstack check` 0, `nstack fitness` compliant, verified on `main` |
| `copying` | **does not exist yet.** It is created by the first task below |
| Framework | v0.6.1, project and CLI in step |

Older branches are merged or superseded and can be ignored. `nstack fitness` is compliant and
`nstack doctor` reports **0 gaps**; its 13 `NOT VERIFIED` lines are the GitHub settings, which need
a token to read — *what cannot be read is never reported as guarded*. `doctor` exits non-zero in
that state, so read the gap count, not the exit code.

## Next, in order

1. **D1, and it is day one.** Five private messages, sent within three days, read at day 14.
   Deferred by two cycles, in the cycle for the third time, and it gates every phase-1 criterion in
   the charter. **The framer's note says to look on day three, not at the end:** if the messages
   have not gone out by 2026-09-27, this cycle is already repeating both of its predecessors.
2. **Scaffold the module:** `nstack new-module copying NapkinStack/maintainers critical`, declared
   `user_facing` — a member sees what it does. Its own pull request, as `screening` had.
3. **D2, then D3**, sequentially: both are `copying`, and it is one pull request per module. D2 is
   the key a member gives and takes back; D3 is the notice shown before they act. Read the cycle
   for what the criteria are built to refuse — every one of them names **the venue** as the thing
   that answers, never our own state.
4. **`critical` means adversarial verification without a cap** (ADR-0003), unlike `screening`'s one
   round. Hold that line when it is inconvenient; the reason is in *What this project has learned
   about itself* below.

**Owed at the next boundary, not before:** check NapkinStack again. It moved 0.3.0 to 0.6.1 in
three days. Sequence, and only in this order: `uv tool install "napkinstack==X.Y.Z"
--with-executables-from pre-commit`, then `nstack update`, then `nstack doctor`. Upgrading the CLI
without `nstack update` turns doctor's L1 red. **And `nstack update` branches from the current HEAD
without saying so** — check out `main` first, or expect to replant the branch, as #29 had to.

## Decisions taken, and where they live

| Decision | Where |
|---|---|
| Two GitHub identities: the App commits, the token configures | `docs/adr/0001` |
| A delegated session may verify, signing as itself | `docs/adr/0002` |
| Verification budget follows criticality; no unasked change inside a fix | `docs/adr/0003` |
| Commission on routed volume, never a share of gains | `docs/pdr/0001` |
| Three verdicts, four reservations, the extrapolation ceiling — and four amendments | `docs/pdr/0002` |
| A closed pilot of 5–8 before any funnel; the count criterion replaced | `docs/pdr/0003` |
| The read is sized from one probe, and the trade that forces | `modules/screening/docs/adr/0003` |

**If the hook's "ADR-0004" confuses you, read `docs/adr/0001` before assuming it is missing.** The
hook that refuses a direct GitHub CLI call cites **NapkinStack's** ADR-0004, not this project's;
`docs/adr/` here stops at 0003 and that is correct. This project's ADR-0001 names it, explains the
mechanism it enforces — a token minted per call, one hour, never on disk — and builds on it. The
session that wrote this line briefly recorded it as a missing decision, which it is not.

## Open, and belonging to the decider

- **The legal opinion.** Requested, pending. Phase 2 is gated on it.
- **The five DMs.** Ten traders and twenty members are *reported* as wanting to test the bot —
  private, declarative, nobody has acted. D1 stays `deferred`.
- **The phase-2 date** on the commission criterion. PDR-0003 moved it there "with a later date" and
  named none, so the project currently has a viability criterion that cannot fail. In the charter's
  open questions.
- **`.claude/` project settings and hooks** are untracked and deliberately not gitignored: the team
  is meant to share them. They are masked as character devices inside the agent's sandbox, so the
  agent cannot read them and will not commit what it has not read. **A human needs to add them.**

## How to work in this repository

- **GitHub:** the agent CLI wrapper only — a project hook refuses the direct one. The App commits
  and pushes; the fine-grained token configures the repository and cannot push. Merging requires
  the decider's approval; the agent cannot self-approve. **A push dismisses an existing approval**
  (the ruleset says so), while editing a pull request's description re-runs the description checks
  on the same head and leaves the approval standing — so put the test sheet in last.
- **That hook matches the command text, not the process invoked.** A heredoc that merely mentions
  the forbidden command name is refused too. Write such a file with an editing tool instead of a
  shell redirection.
- **`git config`, remotes:** never `--global`. `GIT_CONFIG_GLOBAL` already points at
  `workspace/flet/.gitconfig`, which is workspace-scoped on purpose.
- **Reading a CI log needs a writable cache**: `XDG_CACHE_HOME="$TMPDIR"`, or it fails on a
  read-only `~/.cache`.
- **Check gates by their own exit status**, never by a command chained after a `tail`, and never
  read an exit code through a pipe — `cmd >log 2>&1; echo $?`. Both mistakes have shipped a failing
  commit here, and one of them recurred in the session that wrote this line.
- **A live venue run** needs `allowed_domains` including `api.hyperliquid.xyz`. Watch which side of
  that you are on: with egress denied the command takes its no-verdict path, which is a different
  measurement from a real answer, and confusing the two has already produced a wrong reading.
- **Mutation testing:** `PYTHONDONTWRITEBYTECODE=1`, clear `__pycache__` between mutants, and
  verify each patch actually applied before reading its result.
- **T4 costs a re-measurement.** Every sheet row carries the head commit, so any commit — including
  one that touches no module file — invalidates the whole sheet. Three of cycle 02's six
  confirmation runs were spent re-measuring 30-odd rows after a documentation-only commit. Land the
  prose before asking for the sheet.

## What this project has learned about itself

**Six adversarial rounds and six confirmation runs on one read-only module produced eleven real
defects and five refusals.** Three of the defects the author introduced in later rounds, inside
changes nobody had asked for. Three of the refusals were not about code at all: they were sentences
in a decision record asserting more than the code does.

Two things came out of that and they are worth carrying rather than re-deriving:

1. **A class closes; an instance does not.** Four refusals were spent on clauses that fixed the
   case just found. The one sentence that ended the sequence generalised — *the guarantees speak
   about what the command chooses to write* — and the verifier then bounded it by enumerating the
   two write sites. Write the general form first.
2. **A delegated verifier has no session identifier of its own.** `CLAUDE_CODE_SESSION_ID` in its
   shell is the parent's — the same value every `Agent-Session` trailer carries — so T2 cannot
   detect that a verifier is a child of the session that wrote the code. Each run established its
   identity from the harness's subagent records and said so unprompted. ADR-0002 records this as
   owed; the mitigation is social, and it worked here only because the briefs asked for failure and
   the verifier refused five heads.
