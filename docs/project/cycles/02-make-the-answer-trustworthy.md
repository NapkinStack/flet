---
goal: "Find out whether vouching moves anyone, and make the screening answer one an administrator can act on"
status: accepted
appetite_weeks: 3
start: 2026-09-21
end: 2026-10-12
deliverables:
  - id: D1
    title: "Spike — does an administrator's vouching move anyone? Five private invitations, read at day 14"
    module: null
    state: deferred
    acceptance:
      - "Given docs/project/link-test-protocol.md, private variant, when the cycle starts, then the five messages are sent within 3 days and Karim's reason for choosing each member is recorded as the stated bias it is"
      - "Given day 14, when it is reached, then the number who actually started is read from their public addresses — refuted at 0 of 5, and no result confirms"
      - "Given any reading, when it is recorded, then each figure carries its grade: on-chain, or declarative"
  - id: D2
    title: "The screening answer is read from a window that ends now, and the venue does not refuse it"
    module: screening
    state: ready
    acceptance:
      - "Given a trader whose 30 days of fills exceed the page bound, when the command runs, then the window it keeps ends at or near the moment of the run — never a window that ended days before the question"
      - "Given the same trader, when the command runs, then it completes without exhausting the venue's rate limit, and the number of heavy reads it made is stated"
      - "Given the venue throttles it anyway, when that happens, then it says so and returns no verdict, rather than a verdict from stale or partial data"
      - "Given a trader whose orders fall under the venue's floor once scaled, when the command runs, then the share that would be refused is stated"
      - "Given any trader, when the command runs, then the monthly fee cost is stated as a percentage per month, and the share of fills a copier could not reproduce is stated"
  - id: D3
    title: "Three verdicts instead of two, so the headline cannot say yes to a trader the answer is warning about"
    module: screening
    state: ready
    acceptance:
      - "Given a trader who clears the floor and trips no reservation, when the command runs, then the verdict is COPYABLE and the exit code is 0"
      - "Given a trader who clears the floor with a fee burden above the alert, when the command runs, then the verdict is COPYABLE WITH RESERVATIONS, the fee reservation is named on the first line, and the exit code is 1"
      - "Given a trader who clears the floor with more than half their fills posted, when the command runs, then the verdict is COPYABLE WITH RESERVATIONS and the reproducibility reservation is named"
      - "Given a trader who clears the floor whose volume landed on a third or less of the days, when the command runs, then the verdict is COPYABLE WITH RESERVATIONS and the concentration reservation is named"
      - "Given a trader who does not clear the floor, when the command runs, then the verdict is NOT COPYABLE and the exit code is 2, whatever the reservations say"
      - "Given the venue cannot be read, when the command runs, then the verdict is NO VERDICT and the exit code is 3"
---

# Cycle 02 — Make the answer trustworthy

> One accepted cycle at a time; no automatic extension. The end date is a circuit breaker.

## Goal

Two questions, and only one of them is about code.

**Does anyone want this?** After a discovery, two independent challenges and a whole cycle,
nobody has asked a member. Five private messages answer it — or kill the project for the price
of five messages, which is the cheapest outcome available.

**And can an administrator act on what the screening command tells them?** Today it can return a
verdict from a window that ended eleven days earlier, and it can say `COPYABLE` about a trader
whose fees it is simultaneously warning will decide the member's result.

## Deliverables

**Order.** D1 first and on day one — it is somebody else's calendar and a fourteen-day clock.
D2 before D3, because both touch `screening` and D3's verdict rests on figures D2 makes
trustworthy. One pull request per module, so they are sequential, not parallel.

**D2 absorbs the unmerged branch.** `d3/the-command` carries the command, five fixes and a
failed S8. D2 finishes it and merges it whole; it does not start again.

**D2 is one change under two names.** S8 fails because a cut-short read keeps the stale front;
the venue's weight-based limiter refuses up to 40 heavy reads. Both are answered by reading
**fewer, better-targeted pages** — read backwards from now, or size the window to the trader's
rate before reading. Fixing one fixes the other, and the cycle-01 closure says so.

**Its sheet must name the criteria cycle 01's sheet missed.** Two verifiers reported that three
of D3's acceptance criteria were covered by tests and named by no scenario, so a green sheet
proved the window machinery rather than the deliverable. D2's last two acceptance criteria exist
to close that.

## Out of scope

- The retry-rate metric, the unrecorded 429 deviation, and the per-call rather than
  per-invocation budget. Recorded in cycle 01, and they belong with an observability batch.
- The copying module — agent keys, orders, risk limits. That is `critical`, and it gets its own
  cycle.
- Anything on Telegram. §7 of its Bot Developer Terms closes the Mini App path for a non-TON
  venue, and the decider has accepted excluding it.

## Later

- The honest onboarding notice: not authorised, opinion pending, leveraged, you can lose
  everything.
- The Discord application and its verification prerequisites, at 75 servers.
- The install-to-active ratio, measured rather than judged.
- Discord's Developer Policy clause on financial information — four sessions refused; it needs
  someone logged in.
- The wording preferences two verifiers raised: `of which flet takes …` invites a 20×
  misreading, and a complete window pairs a one-day date range with a thirty-day base.

## Open questions

**Blocking:** none once this cycle is accepted.

**Not blocking:**

- The written legal opinion, requested and pending, and the decision to launch without it.
- Whether Karim sends the five messages within three days. His calendar.
- Whether a Telegram bot with no Mini App escapes §7. A reading of a sentence, untested, and out
  of scope here.

## A note the framer owes this cycle

The decider was offered **one week on D1 alone**, two weeks on D1 and the window fix, or three
weeks on everything, and was told plainly that the third option has **the same shape as cycle
01** — which consumed a two-week appetite on one of three deliverables and accepted none of
them. The decider chose three weeks and everything.

Recorded here rather than left to be reconstructed, so that if this cycle ends the way the last
one did, the reason is already written down and nobody has to be persuaded of it.

## D1 has a declarative answer, and it is short of the charter

On 2026-09-21, after the simulation below was written, the decider reported **10 traders and
20 members** who have said they want to test the bot. The conversations are private and were
not disclosed; the result is *reported*, not observed. `pilot-faq.md` carries the exchanges
the decider confirms are representative of them.

**This answers D1's question and fails D1's criteria.** "Does an administrator's vouching move
anyone?" — yes, thirty people said so, which is more than nothing and more than this project
had an hour earlier. But D1 counts who **acts**, read from public addresses, and nobody has
acted: the members are waiting for the bot rather than mirroring a trader by hand. D1 stays
`deferred`.

The useful finding is arithmetic and it is now a blocking question on the charter: twenty
interested members yield **3.5 to 8.4** still copying at day 30, against a threshold of
**20**. The pool needed is 48 to 114. The ten traders are ample; the entire shortfall is on
the member side.

## D1 was simulated, not run

On 2026-09-21 the decider chose not to send the five invitations and asked for a realistic
simulation instead. `docs/project/d1-simulation.md` is that model, and it is marked
`status: simulation` in its own front matter.

**D1's acceptance criteria are unchanged and unmet.** No member of any community has been
asked. The deliverable's state is `deferred` — the framing vocabulary has no word for
"simulated", and `deferred` is the honest one: the work was not done in this cycle. Calling it
anything else would put a model where a measurement belongs.

The model's one useful output is about the protocol rather than the product: at the rate the
model itself assumes, five invitations return **refuted** 47% of the time even when the
product is exactly as good as the discovery's base case. The kill criterion fires on noise
roughly as often as on signal. Fifteen invitations would bring that to 10%.

The closure will record that D2 and D3 were built with no evidence that any member wants to
copy a trader, and that this was a decision rather than an oversight.

## Closure

<Written at the end of the cycle.>
