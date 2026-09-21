# Architecture Decision Records

A structuring **technical or architectural** decision — costly to reverse, or one that
will constrain the decisions after it.

- Template: [`_TEMPLATE.md`](./_TEMPLATE.md)
- Naming: `NNNN-verb-phrase-title.md`, e.g. `0001-adopt-postgres.md`
- A replaced decision is **superseded**, never rewritten quietly.

## Mandatory sections

| Section | Check |
|---|---|
| **Prior art** — ≥ 2 named references + the convention identified | Review; to automate |
| **Deviation** — when departing from the convention | Review; to automate |
| **Dated success criterion** — when building something bespoke | Review; to automate |
| **Rule to automate** — which fitness function follows from it | Review |

See `docs/os/06-decisions.md`.

## Index

| No. | Title | Status | Criterion to check on |
|---|---|---|---|
| [0001](./0001-split-the-agent-github-identity-in-two.md) | Split the agent's forge identity in two: the App commits, the administration token configures | Accepted | 2027-03-20 |
| [0002](./0002-a-delegated-session-may-verify-and-signs-as-itself.md) | A delegated session may verify, and signs under its own identifier | Accepted |
