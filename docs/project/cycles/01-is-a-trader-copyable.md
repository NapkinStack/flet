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

## Closure

<Written at the end of the cycle.>
