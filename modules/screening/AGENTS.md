# screening — local instructions

> Only what is **specific to this module**.
> Never duplicate a kernel rule (`/AGENTS.md`).

## Responsibility

Answers whether a given trader can be copied by a member of a given ticket size, from that
trader's public fills on the venue.

## What this module does not do

- **It does not place, size or cancel an order, and holds no key.** That is the copying
  module, which does not exist yet and will be `critical`. If a task here needs a key, the
  boundary is wrong — stop and say so.
- **It does not decide who may be copied.** Each administrator owns their list. This module
  answers a question about a trader; it never curates.
- **It does not rank traders by performance.** Copyability is not merit, and the charter's
  differentiator is an administrator's vouching, not a leaderboard.

## Internal conventions nobody could guess

- **Every figure carries how it was obtained.** The discovery grades each claim *primary*,
  *reported*, *excerpt* or *assumption*, and this module's answers follow the same rule: a
  verdict without its measurement is not an answer here.
- **Rates, never absolutes.** A server's size and a member's ticket both vary; anything
  reported as a count is unusable one community later.
- **Read-only against the venue.** Public endpoints only. This module never authenticates.

## Business invariants

- **An order under 10 USDC of notional is refused by the venue.** Any verdict that ignores
  the floor is wrong, not approximate.
- **A trader's turnover sets both the member's fee burden and flet's revenue** — they are the
  same variable. A verdict that reports one without the other hides the trade-off.
- **A fill where the trader posted liquidity cannot be reproduced by a copier** arriving
  afterwards. Counting it as copyable overstates every other figure.
- **No verdict from stale or partial data.** If the venue is unreachable, say so and return
  nothing.

## Known traps

- **Selecting traders by performance selects scalpers.** The framer did exactly this and
  produced a fee figure 200 times too high, corrected only by screening the whole population.
  Any sampling here states its selection rule.
- **The median turnover of *all* active accounts is not the median of the *copyable* ones** —
  8.5× against 2.06×. Applying the wrong one moves the project's forecast by a factor of three.
- **The leaderboard is a live snapshot.** Two runs a day apart give different minimum-ticket
  figures. Record the addresses so a result can be reproduced.

## Areas not to change without approval

The 10 USDC floor and the 0.1% fee cap are the venue's, not ours. If either appears to have
changed, that is a finding for the charter's constraints, not a constant to edit.

## Non-standard commands

None. The MANIFEST verbs apply, and `commands.check` and `commands.test` are declared before
this module's first file of code.
