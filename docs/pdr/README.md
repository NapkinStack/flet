# Product Decision Records

An important **product** decision: a user goal, an expected behaviour, a trade-off, a
structuring business rule, a UX or business decision.

The PDR describes **what the product must do and why**, never its implementation.

- Template: [`_TEMPLATE.md`](./_TEMPLATE.md)
- Naming: `NNNN-user-oriented-title.md`

## Mandatory sections

| Section | Why |
|---|---|
| **Prior art** — ≥ 2 references | On an interface, a convention's value comes from the user already knowing it |
| **Dated success criterion** | Makes the decision falsifiable, and therefore useful |
| **Removal condition** | Without it, a feature is permanent by default, even unused |

> The **FDR** format does not exist in this OS. For genuinely complex features, the
> *Detailed functional design* section of the PDR is enough
> (`docs/os/06-decisions.md` §4).

## Index

| No. | Title | Status | Criterion to check on |
|---|---|---|---|
| [0001](./0001-charge-on-routed-volume-never-on-the-member-s-gains.md) | Charge a flat commission on routed volume, never a share of the member's gains | Accepted | 2027-03-21 |
| [0002](./0002-three-verdicts-not-two.md) | Three verdicts, not two: copyable, copyable with reservations, not copyable | Accepted | 2026-12-31 |
