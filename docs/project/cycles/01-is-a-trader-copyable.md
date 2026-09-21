---
goal: "An administrator can tell whether a trader is copyable by their members, and Karim's community has been asked whether vouching moves anyone"
status: accepted
appetite_weeks: 2
start: 2026-09-21
end: 2026-10-05
deliverables:
  - id: D1
    title: "Spike — does an administrator's vouching move members to copy? The link test, launched and read at day 14"
    module: null
    state: ready
    acceptance:
      - "Given the protocol in docs/project/link-test-protocol.md, when the cycle starts, then the administrator's post is live within 3 days and the server's member count and the shortened link are recorded"
      - "Given a 500-member server, when day 14 is reached, then the number of members who started copying is recorded from the public addresses posted in the thread — refuted below 4, confirmed at 9 or more"
      - "Given any reading, when it is recorded, then each figure carries how it was obtained: on-chain, or self-declared"
  - id: D2
    title: "Spike — what Discord and Telegram actually allow, read on their own pages"
    module: null
    state: ready
    acceptance:
      - "Given the developer portal opened by the decider, when the verification page is read, then the eligibility and requirement thresholds are recorded with their source, replacing the excerpt-grade 75 and 100"
      - "Given Discord's Developer Policy, when the clause on financial information is read, then it is quoted in the charter's constraints or recorded as absent"
      - "Given Telegram's Bot Developer Terms, when §7 and §7.3 are read, then whether a crypto Mini App is restricted to TON is recorded, with the exact wording"
  - id: D3
    title: "An administrator asks whether a trader is copyable for a given member ticket, and gets a grounded answer"
    module: screening
    state: in-progress
    acceptance:
      - "Given a trader's public address and a member ticket in euros, when the administrator runs the command, then the answer states whether the trader is copyable and why, from that trader's real fills"
      - "Given a trader whose typical order falls under 10 USDC once scaled to the ticket, when the command runs, then it is reported as not copyable at that ticket, with the share of orders that would be refused"
      - "Given a trader whose monthly turnover would cost the member more than 5% of their capital in fees, when the command runs, then that cost is stated as a percentage per month, not hidden behind a verdict"
      - "Given a trader who posts more liquidity than they take, when the command runs, then the share of their fills a copier could not reproduce is stated"
      - "Given the venue's public API is unreachable, when the command runs, then it says so and returns no verdict, rather than a verdict from stale or partial data"
---

# Cycle 01 — Is a trader copyable?

> One accepted cycle at a time; no automatic extension. The end date is a circuit breaker.

## Goal

Two weeks, and the two things that carry the most risk reduction per hour.

The first is **not code**: Karim's community has never been asked. Three rounds and two
independent challenges have failed to refute the claim that a member copies because someone
they know vouched — and have equally failed to find any evidence for it. One Discord message
ends that, and its clock is the only one already running.

The second is the one piece of the product that the discovery **measured into existence**:
an administrator cannot pick copyable traders by trusting them. Copyability is arithmetic —
the venue's 10 USDC floor, the trader's turnover, the share of their fills that rest on the
book rather than take from it. Nobody can do that by eye, and today nobody is doing it at all.

Both run on **public data only**. No key, no order, no member's money.

## Deliverables

**Order and dependencies.** D1 first and on day one: it is somebody else's calendar and a
30-day window that must start before it can end. D2 is the decider's, needs a logged-in
browser, and unblocks nothing in this cycle — it removes three *excerpt*-grade figures the
charter currently rests on. D3 is the only build, and it depends on neither.

**D3 is deliberately the module that touches nothing.** The charter sets `critical` for this
project, and it is right for the module that will hold agent keys and place orders. That
module is not this one: `screening` reads public addresses and answers a question. It is
declared **`high`** and **user-facing** — an administrator reads its answer and changes who
their members can copy, so a wrong answer has consequences, but it cannot move a euro.

**What D1 can do to this cycle.** If the link test is refuted at day 14 — fewer than 4 of 500
members starting — the charter's first success criterion is dead and the decider should be
presented with stopping the project, as the framing playbook requires when a spike refutes
what the charter rests on. D3 would still be a useful tool; it would just have no product
around it.

## Out of scope

Not done in this cycle, even if time remains:

- **Anything that holds a key or places an order.** No agent-key onboarding, no copying, no
  risk limits, no kill switch. That is the `critical` module and it gets its own cycle.
- The Discord application itself, its verification, its privacy policy and terms of service.
- Telegram, in any form.
- The onboarding notice, which belongs with the onboarding.
- The day-30 reading of the link test, which falls outside this cycle's window by
  construction.

## Later

Candidates for the next framing, in the order the discovery makes them urgent:

- The copying module: agent-key onboarding, the curated list, a member copying — `critical`,
  with position sizing, a leverage ceiling, a kill switch and a verified rollback.
- The honest onboarding notice: not authorised, opinion pending, leveraged, you can lose
  everything.
- The Discord application and its verification prerequisites, needed at 75 servers.
- Trader-to-ticket matching turned from an answer into a behaviour: the bot proposing only
  the traders a given member can actually copy.
- The install-to-active ratio, measured rather than judged.

## Open questions

**Blocking:** none once this cycle is accepted.

**Not blocking:**

- Whether Karim posts within three days. His calendar, not the decider's, and D1's acceptance
  says three days for that reason.
- Whether members will post a public address rather than self-declare. The protocol says the
  count falls back to self-declaration and drops a grade if they will not.
- The written legal opinion, still pending, and the decision to launch without it — neither
  bears on this cycle, which touches no money.
- **Found by running D3 against the live venue, 2026-09-21.** Two real traders come back
  `COPYABLE` while costing the member **14.31%** and **5.64%** of their ticket per month in
  fees. The acceptance criteria are met — the cost is stated and not hidden — but the one-word
  headline still reads as approval. An independent verifier raised the same thing from the
  other side: `copyable` rests on **one** of the four measurements, so a trader can be
  `COPYABLE` with 70% of their fills unreproducible. **Not changed in this cycle**: it moves an
  accepted acceptance criterion, which is the decider's to do.
- **Also found by running it:** the public leaderboard and the live account state disagree.
  Several leaderboard accounts now hold nothing, and the command correctly returns no verdict
  for them. The module reads the live state, which is the right source; the leaderboard is a
  snapshot, and the discovery's figures inherit that.
- **Raised by the verifier, and both are real.** The fee burden is computed on the trader's
  **whole** volume, including the fills a copier cannot reproduce — so it errs *pessimistic* on
  fees inside the same verdict that says that volume is unreachable, while the fee *tier* errs
  optimistic. Two unbounded biases in opposite directions. And the cycle says "5% of their
  **capital**" where the code computes a share of the **ticket**; they coincide only when the
  ticket is the member's whole allocation. **Words to settle before the command states them to
  an administrator.**
- **`days_observed` was unbounded — found, then fixed before merging.** The venue returns at
  most 2,000 fills per call, so the observation window was whatever that cap covered, and the
  monthly figures were extrapolated from it. The second verifier showed this is the **normal
  path for any active trader**, not an edge case: one real trader read 2,000 fills over 0.6
  days and was told his copier would pay **1,371% of their ticket per month**. Fixed by paging
  `userFillsByTime` over a requested 30-day window; the same trader now reads 8,186 fills over
  30.0 days and 85.49% — still high, but a measurement of a genuinely hyperactive trader rather
  than an artefact of a cap. When the page limit does stop the read short, the answer says so
  and names its figures as extrapolated.
- **And the mirror of that defect, found by the same verifier and addressed before merging.**
  Reading the 30 days correctly still averages over them, so a trader who placed **15,243 fills
  in two hours** and nothing else reads as `0.17% of their ticket per month` — right about the
  past, roughly **360× too low** as a forward cost. The first defect over-stated, which errs
  toward refusing a trader; this one under-stated, **which errs toward `COPYABLE`**. The command
  now states **how many of the window's days the trader actually traded on**, and names the
  understatement with its factor when the volume is concentrated. It does not divide by those
  days — that would swing the bias straight back — it shows both and lets the administrator
  see a trader who did a month in a day.

## Closure

<Written at the end of the cycle.>

### D3 — what the fourth verification found, and where it was stopped

**Two defects, both fixed here, both in the branch no earlier pass had reached.** The verifier
got there by changing how it sampled: earlier passes looked at the highest *monthly volume*,
which finds burst traders; the population that crosses the 40,000-fill bound is the sustained
market maker, and the cheap signature is one mid-window day that is itself page-capped. Four
funded addresses crossed on the first attempt. **The bound is a normal Tuesday for a market
maker, not an exotic case.**

1. **`traded on 18 of the 17 days read`** — an impossible sentence, printed to an
   administrator. Two numbers on different bases. Now counted against the same base.
2. **A cut-short read kept the *stalest* part of the window.** Paging ascends, so stopping at
   the cap discarded the most recent 13 of 30 days and reported the rest as current. A trader
   who stopped, resized or blew up a fortnight ago was invisible. The read now retries over a
   **recent** window sized to what the first pass got through, and the command states the
   **dates** it read — complete or not.
3. **The concentration threshold was a cliff.** 0.34 warned at 10 days of 30 and not at 11,
   leaving a 2.7× understatement unnamed. The constant is gone; the factor is arithmetic and is
   stated for every trader.

**Where this stops, and why it stops rather than continues.** Up to 40 heavy reads per
invocation trip the venue's rate limiter. A retry with exponential backoff, jitter, a maximum
count and a total budget is in place (`operations.md`), and the command now **says** it was
throttled instead of hanging or inventing an answer — but on the over-bound traders it still
returns `no verdict`. Measured: 25 rapid *light* calls pass untouched, so the limiter is
**weight-based**, and a 2,000-row page is what costs. The fix is pacing, not retrying.

**It is not written, deliberately.** This session's own bursts have left the limiter hot, so a
pacing change could not be observed here — and writing code that cannot be verified is the one
thing four verification passes have made indefensible. Recorded as an operational gap with its
measurement, for a batch that can watch it work.