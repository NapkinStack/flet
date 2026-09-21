# ADR-0001 — Answer copyability from the venue's public fills, in a module that holds no key

- **Status**: Accepted
- **Date**: 2026-09-21
- **Decision makers**: @napkinstack-admin, on the framer's proposal
- **Scope**: module `screening`
- **Reversibility**: easy — the module holds no key, no state and no contract

---

## Context

The discovery measured something nobody had asked for: whether a trader can be copied at all
by a small member is **arithmetic**, not trust. The venue refuses orders under 10 USDC of
notional, so a member needs roughly one twentieth of a trader's account to place 80% of their
orders; a trader's monthly turnover sets the member's fee burden — 2.06× costs about 1.2% a
month, 72× destroys the account; and between 0% and 67% of a trader's fills are posted
liquidity that a copier arriving afterwards cannot reproduce at all.

An administrator curating a list today has no way to see any of this. The charter therefore
carries "matching traders to the members' ticket" as a product requirement, and cycle 01 makes
it the first thing built.

## Problem

Where does the capability "is this trader copyable, and at what cost" live, and what may it
touch?

## Constraints

- The charter sets the project's copying module at `critical` — it will hold an agent key per
  member and place orders on leveraged accounts.
- The appetite for cycle 01 is **two weeks**. A `critical` module's definition of done adds
  end-to-end tests, observability and a verified rollback.
- Every input this capability needs — fills, account values, order sizes — is **public** on
  the venue and requires no authentication.

---

## Prior art

**Dominant convention of the field:** copy-trading products expose a trader's **track record**
— return, drawdown, win rate — and let the follower choose on it.

**References examined:**

| Reference | What it does | Applicable here? |
|---|---|---|
| Hyperliquid's own leaderboard, and the third-party dashboards built on it | Rank traders by return over a window; the leaderboard is what the framer used, and it selected scalpers | **No, and it is the trap.** Ranking by performance selects traders that are uncopyable at small size. |
| Copin, HyperMirror, HyperX — shipped non-custodial copy trading on this venue | Let a follower copy a chosen trader; none was found to warn that a trader is unsuitable for a given account size | Partly: they prove the copying is feasible, not that the selection is informed. |
| The venue's own order rules — the 10 USDC floor, the builder-fee cap, the maker/taker distinction on a fill | Impose what is arithmetically possible, independently of anyone's opinion | **Yes.** These are the inputs; everything else is derived from them. |

**Why the convention is not enough:** a track record answers *is this trader good*. It cannot
answer *can my member follow this trader at all*, which is the question that decides whether
38% or 87% of the orders will simply be refused. The two questions are independent, and only
the second has an arithmetic answer.

---

## Options considered

### Option 1 — Put the capability in the copying module
- Description: the module that holds agent keys also answers the copyability question.
- Advantages: one module, no boundary to define.
- Drawbacks: a read-only question inherits `critical`, its verified rollback and its
  end-to-end weight, for code that cannot move a euro. And nothing could be built in cycle 01
  without opening the key-holding module first.
- Cost of setup / maintenance / **getting out**: low / high / splitting it later, once the
  key-holding code is entangled with it.

### Option 2 — A separate module, read-only, no key *(chosen)*
- Description: `screening` reads public addresses and answers the question. It authenticates
  to nothing and holds nothing.
- Advantages: a blast radius of zero, so `high` rather than `critical` is honest. Buildable in
  two weeks. Usable by an administrator before any copying exists, which also improves the
  curated list feeding the link test.
- Drawbacks: a boundary to maintain, and the copying module will later consume this answer —
  through a contract, not by reaching into it.
- Cost of setup / maintenance / **getting out**: low / low / delete it; nothing depends on it
  yet.

### Option 3 — Do nothing, and let administrators judge by eye
- Description: no tool. Administrators pick traders they trust, as Karim does today.
- Advantages: free.
- Drawbacks: the discovery measured what this produces — a 500 € member copying a 300k account
  has 38% to 87% of orders refused, and a high-turnover trader costs them 28% of their capital
  a month. Nobody sees any of that by eye, and the member pays for it.
- Cost of setup / maintenance / **getting out**: none / none / none.

---

## Decision

**Option 2.** The capability is real, it is measurable from public data, and it needs no
credential — so it belongs in a module that has none. That keeps the first thing built at a
criticality its actual risk justifies, and keeps the key-holding module closed until it gets
the cycle its `critical` rating deserves.

Option 3 was not dismissed lightly: it is what every shipped competitor does today. It was
rejected because the discovery **measured** the cost of judging by eye, and that cost lands on
the member.

### Deviation from the convention

- **Expected user value**: an administrator stops recommending traders their members cannot
  actually follow, and a member stops paying a fee burden nobody quoted them.
- **How we will observe it**: at least one trader that Karim would have listed is reported as
  not copyable at his members' ticket, with the share of orders that would be refused.

---

## Success criterion

> We will consider this was the right call if **at least one trader an administrator intended
> to list is shown to be uncopyable at their members' ticket, and the administrator changes
> the list because of it** is observed before **2026-12-31**.

What we do if it is not: if every trader an administrator picks turns out copyable anyway, the
module solves a problem that does not occur, and it is removed rather than maintained.

---

## Consequences

**Positive:**

- The first module built holds no key, so nothing in cycle 01 can lose anyone's money.
- The copying module inherits an answer instead of re-deriving it.
- An administrator gets something usable before the product exists.

**Negative and accepted debt:**

- A second module to own, and a contract to define when copying consumes this.
- The answers depend on a live snapshot of a public leaderboard: two runs a day apart differ.
  Recorded as a trap in the module's `AGENTS.md`.

**Impacts on other modules or contracts:** none today. The copying module will consume this
through a declared contract, never by reading this module's code.

**Rule to automate:** that this module never authenticates. A check that its source contains
no credential read, no signing call and no private-key handling would make the boundary
enforced rather than stated. It does not exist yet; until it does, this is a review-time check
and the omission is recorded here rather than assumed away.

---

## Rejected alternatives

**Option 1, inside the copying module** — rejected because it would give `critical` weight to
code that cannot move a euro, and would force the key-holding module open in a two-week cycle
that was scoped to touch no money.

**Option 3, judging by eye** — rejected on measurement, not on principle. It remains what the
field does, and if the success criterion above is missed it is the state this module returns to.
