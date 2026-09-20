# ADR-0001 — Split the agent's GitHub identity in two: the App commits, the administration token configures

- **Status**: Accepted
- **Date**: 2026-09-20
- **Decision makers**: @napkinstack-admin, decider of the project
- **Scope**: project
- **Reversibility**: easy — revoking the administration token restores the single-identity
  setup, and the repository keeps the settings already applied

---

## Context

This project's guardrails do not live in the repository. Rulesets, push protection, private
vulnerability reporting and the exception labels live in GitHub's settings, and
`nstack doctor` only ever *reads* them: it answers `guarded` or `unguarded`, and closes
nothing.

The skeleton's installation checklist asks for a GitHub App as "the identity your agents
work under", and fixes its permissions: Contents, Pull requests and Issues read and write,
Actions and Checks read — and **never Administration**. It adds a line that settles more
than it looks: "The agent's session reaches no human credential." The kernel says the same
in §0: "You work under your own GitHub identity, never with a human's credentials."

The workstation enforces this rather than trusting it. A hook refuses a direct call to the
GitHub CLI and requires the `gh-agent` wrapper, which mints an installation token of the
`napkinstack-agent` App on each call — valid one hour, never written to disk, with its own
config directory so the machine's default account is never read, and `auth` refused
outright. That hook names NapkinStack's ADR-0004 as its reason.

At the same time, the skeleton's README documents that `nstack doctor` reads a token from
`GH_TOKEN` with the Administration **read** permission. So the framework already expects two
credentials to exist on the workstation. What it does not settle is whether the agent may
*write* with the second one.

The question arose on the project's first day: the repository was created and pushed, and
thirteen settings stood between it and a forge that refuses anything at all.

## Problem

Which identity may change this repository's settings — and may an agent use it?

## Constraints

- The kernel and the skeleton's checklist both forbid the agent reaching a human credential.
- The same checklist forbids Administration on the agents' App.
- **A GitHub App cannot widen its own installation scope.** Verified in session:
  `GET /user/installations` answers `403 Resource not accessible by integration` to an
  installation token, because adding a repository to an installation goes through
  `PUT /user/installations/{id}/repositories/{id}`, which requires a *user* access token.
- The administration credential available here is a fine-grained token limited to this
  repository: Administration write, Issues write, and **Contents: No access** — it cannot
  create a commit.
- Nothing in the toolchain applies settings. `nstack doctor` reads them; no command writes
  them.

---

## Prior art

**Dominant convention of the field:** one automation identity — a GitHub App — for
everything an agent does on the forge, with personal access tokens reserved for throwaway
use.

**References examined:**

| Reference | What it does | Applicable here? |
|---|---|---|
| GitHub Docs, ["Deciding when to build a GitHub App"](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/deciding-when-to-build-a-github-app) | Recommends Apps over personal access tokens for any long-lived integration: "fine-grained permissions" instead of broad scopes, the ability to "act independently of a user", no seat consumed. Personal access tokens are for "API testing or short-lived scripts". | Yes — it is why the code path goes through the App and through nothing else. |
| NapkinStack's ADR-0004, as enforced on this workstation by the `gh-agent` wrapper and the hook that names it | Routes every GitHub call an agent makes through the `napkinstack-agent` App: a token minted per call, one hour, never on disk, its own config directory, `auth` refused. | Yes — it is the mechanism this decision builds on, and the one the hook makes non-optional. |
| The skeleton's own installation checklist (`README.md`, "To do once on GitHub") | Fixes the agents' App permissions and forbids Administration among them; requires that the agent's session reach no human credential. | Yes — it is precisely what rules out the single-identity answer. |

**Why the convention is not enough:**

The convention says "one App for the agent". Applied literally here it leaves thirteen
settings to a human hand for ever, because that same convention forbids giving the App the
Administration permission needed to apply them. The gap is not comfort. A repository whose
settings drift is one where `nstack doctor` can name the drift and never close it, and every
drift then waits on somebody noticing a report.

---

## Options considered

### Option 1 — One App, granted Administration
- Description: the `napkinstack-agent` App receives Administration write; the agent does
  everything under it.
- Advantages: a single identity, nothing to arbitrate, nothing to explain in a summary.
- Drawbacks: the agents' App can then rewrite the rulesets that judge its own pull requests.
  The skeleton's checklist forbids Administration for that exact reason.
- Cost of setup / of maintenance / **of getting out**: none / none / removing a permission
  an agent's routines have come to depend on, which is when it gets noticed.

### Option 2 — Two identities, split by capability *(chosen)*
- Description: the App holds Contents and Pull requests write and no Administration — it
  commits, pushes and opens pull requests. The fine-grained token holds Administration and
  Issues write and Contents "No access" — it configures and cannot commit.
- Advantages: neither credential can do the other's job, and the split is enforced by the
  credentials themselves rather than by the agent's discipline or by a prompt.
- Drawbacks: two things to rotate and revoke; an agent must say which identity each action
  used, and nothing enforces that it says so.
- Cost of setup / of maintenance / **of getting out**: none, both already existed /
  rotating a fine-grained token / revoke the token — the repository keeps its settings.

### Option 3 — Do nothing: a human applies the settings by hand
- Description: the agent reports what `nstack doctor` finds; a human opens GitHub's settings
  and applies each item.
- Advantages: the cheapest option, and the strictest reading of the kernel. No second
  credential exists, so none can be misused.
- Drawbacks: thirteen settings at creation, then a human pass at every drift.
  `nstack doctor` becomes a report that nobody closes, which is how guardrails quietly stop
  guarding.
- Cost of setup / of maintenance / **of getting out**: none / a recurring human pass /
  nothing to undo.

---

## Decision

**Option 2.** What settled it is not convenience.

The property the kernel protects is that an agent cannot put code into the repository under
a credential that is not its own. Here that property is enforced by the token's own scope
rather than by trust: Contents "No access" means no commit can ever carry that token —
whatever an agent intends, whatever a future prompt suggests, whatever a summary claims. A
rule a credential enforces outranks a rule a kernel states, and option 1 would have replaced
an enforced rule with a stated one.

Option 3 was the honest runner-up and remains the fallback. It was set aside because a
guardrail that depends on somebody reading a report is the kind of goodwill
`docs/os/07-governance.md` exists to remove.

The contradiction with the kernel's "never with a human's credentials" was raised before the
token was used for anything, and settled by the decider — reported, not resolved in silence,
as §9 requires.

### Deviation from the convention

- **Expected user value**: the repository reaches `guarded` and stays there without a human
  hand-applying settings, while no agent can ever commit under the administration
  credential.
- **How we will observe it**: `nstack doctor` reports `guarded`; every commit on the default
  branch is authored by the App or by a human. The second observation is structural rather
  than hopeful — Contents "No access" makes the alternative impossible.

---

## Success criterion

> We will consider this was the right call if **`nstack doctor` still reports `guarded` and
> no commit in this repository was authored under the administration token** is observed
> before **2027-03-20**.

What we do if it is not: correct — narrow the token further, or fall back to option 3 and
apply the settings by hand.

---

## Consequences

**Positive:**

- The thirteen settings were applied on day one; the repository went from `unguarded` to
  `guarded` in one pass.
- Each credential is useless for the other's job, so a mistake in either direction fails
  rather than succeeding quietly.
- An agent can close the loop `nstack doctor` opens, instead of only reporting it.

**Negative and accepted debt:**

- Two credentials to rotate and revoke instead of one.
- An agent must state which identity each action used. Nothing enforces that today; it is a
  convention held by the closing summary.
- The administration token is scoped to this repository only. A second project needs its
  own, and nothing here generalises.

**Impacts on other modules or contracts:** none. No module exists yet, and no contract
touches the forge.

**Rule to automate:** the check that matters most — "the administration token never wrote a
commit" — needs no automation, because Contents "No access" makes it impossible. The reverse
is *not* covered: nothing verifies that the agents' App has not been granted Administration
later, since `nstack doctor` reads the repository's settings and not the App's permissions.
Proposed fitness function: assert that the `napkinstack-agent` installation on this
repository holds no Administration permission. Until it exists, this is a review-time check,
and that gap is recorded here rather than assumed away.

---

## Rejected alternatives

**Option 1, one App with Administration** — rejected because an agent able to change the
rules that judge its own pull requests is not governed by them. The skeleton's checklist
says as much by forbidding the permission outright, and no argument was found that the
checklist had not already weighed.

**Option 3, everything by hand** — rejected, though it was the cheapest and the strictest.
It makes every settings drift wait on human attention and turns a diagnosis into a report
nobody closes. It stays the documented fallback if the success criterion above is missed.
