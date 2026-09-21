# Link test — protocol

> Test **5.2 — value** of `discovery.md`, the cheapest test of the one claim two independent
> challenges failed to refute: **a member copies because someone they know vouched for the
> trader, not because a ranking said so.**
>
> No code, no product, no money. One message and thirty days.
>
> **The thresholds in section 5 are fixed before the test runs.** That is the whole point of
> writing this down: on the closing date we read a verdict, not a mood.

---

## 1. What is being tested, and what would refute it

An administrator the members already trust publishes a vouched shortlist, with a link to a
copy-trading tool that **already exists**. That is flet minus the integration. If members
follow, flet has a reason to exist. If they do not, flet would have changed nothing — and, as
`discovery.md` §4 already states, if they copy through the existing tool then they would have
copied through the existing tool.

## 2. What is deliberately not done

- **flet is not mentioned, built, or announced.** Nothing is installed anywhere.
- **No performance figures, no returns, no past track record** are published — no-go 2 of
  section 4 applies to this test as it applies to the product.
- **No promise that the traders are good.** The administrator vouches that they are *known*
  and *not scammers*. That is the claim under test; anything stronger contaminates it.

## 3. What the administrator does — D0

Karim posts once, in his own words. A template in French, since the community is
French-speaking:

> **J'ai regardé trois traders du serveur.** Ce sont des gens que vous connaissez, qui postent
> ici depuis des mois, et j'ai vérifié qu'ils tradent bien leur propre argent. Je ne vous dis
> pas qu'ils vont gagner — je vous dis que je sais qui ils sont.
>
> — @trader1 · @trader2 · @trader3
>
> Si vous voulez suivre l'un d'eux, ça se fait avec un outil existant, sans que personne
> d'autre ne touche à vos fonds : <lien>
>
> **Si vous vous lancez, postez votre adresse publique dans ce fil.** Elle est déjà visible
> par tout le monde sur la chaîne ; ça me permet juste de voir ce que ça donne pour vous dans
> un mois, et de vous le dire honnêtement.

The link is shortened through any counter, so clicks are measurable. The tool linked to is an
existing non-custodial Hyperliquid copy-trading product (Copin or HyperMirror, from section
5.3); the administrator picks one and links only to that one.

## 4. What is counted, and how

| Measure | How | Grade |
|---|---|---|
| Server members at D0 | The server's member count, noted the day of the post | fact |
| Clicks | The link counter | fact |
| Copies started, by D14 | **Public addresses posted in the thread**, read on the venue's public API | fact, verifiable |
| Still copying at D30 | The same addresses, re-read at D30 | fact, verifiable |
| Each copier's P&L over the window | The same addresses, read on the venue's public API | fact, verifiable |

Asking for the public address is what makes this test **verifiable rather than declarative**.
Self-declaration — a reaction, a "yes I started" — is the fallback if members will not post an
address, and it must then be marked as such: it over-reports enthusiasm and under-reports
losses.

**Everything is expressed as a rate**, never as an absolute, because the server's size is not
known in advance and the result has to be comparable to any other community:

- **start rate** = copies started ÷ members at D0
- **retention** = still copying at D30 ÷ copies started

## 5. The thresholds — fixed before the test

Anchored on the framer's three scenarios (`discovery.md`, round 3), whose start rates are
`members × trade × adopt`:

| Scenario | Implied start rate | Retention |
|---|---|---|
| prudent | 0.8 % | 45 % |
| central | 1.8 % | 50 % |
| ambitious | 3.0 % | 55 % |

**Refuted if** the start rate at D14 is **below 0.8 %** — the prudent scenario is then already
optimistic, and every downstream number with it.

**Confirmed if** the start rate is **at or above 1.8 %** and retention at D30 is **at or above
40 %**.

**Between the two**: not a verdict. The measured rate replaces the estimate, the three
scenarios are rebuilt on it, and the decider chooses again with real numbers.

**Retention is refuted on its own if it falls below 30 %**, whatever the start rate: people
who try once and leave are not a business.

## 6. The market caveat, which decides whether the result is readable at all

If the **median copier is down more than 20 %** over the window, retention is not
interpretable: people stopped because they lost money, which says nothing about whether the
vouching works. In that case the retention figure is **discarded**, the start rate is kept —
it is measured before anyone has lost anything — and the retention measurement is re-run on a
later window.

This is why the P&L is collected. Without it, a bad month reads as a refuted idea.

## 7. Dates

| | |
|---|---|
| **D0** | The post. Record the member count and start the clock. |
| **D14** | Start rate. This is the number that can already refute. |
| **D30** | Retention and P&L. |

D30 must land **before 2026-12-31**, the decider's deadline, so D0 is **2026-12-01 at the
latest** — and every week earlier is a week of margin.

## 8. What each outcome means for the project

- **Refuted (start rate below 0.8 %)** — the vouching does not move people, in the one
  community where the administrator is known and willing. It will not move them in a stranger's
  server. That is a kill, and it cost one message.
- **Confirmed** — the only untested claim in the document becomes a measurement. The project's
  open question is no longer *whether anyone wants this* but *whether it can be funded*, which
  is a question the decider has explicitly deferred to a second date.
- **Between** — the estimate is replaced by a fact, and the forecast is rebuilt on it. That is
  worth the thirty days on its own.

## 9. Who does what

- **The administrator** posts, and asks again at D30. Nothing else.
- **The decider** records the member count at D0 and the click count.
- **The agent** reads the posted addresses on the venue's public API at D14 and D30, computes
  the rates and the P&L, and writes the result into `discovery.md` — with the measurement
  method next to each figure, as everything else in that document carries it.

---

# The private variant — chosen by the decider, 2026-09-21

The decider prefers not to post in the server. Recorded, with what it costs.

## What changes, and what must not

**Karim invites five members privately, and we count who acts.** Not "would you copy a trader I
vouched for?" — a stated intention is close to worthless, and five stated intentions are worth
less. He sends the same three vouched traders and the same link to an existing tool, in a direct
message, to **five members he judges most likely to be interested**, and we count how many
**actually start**.

Everything else holds: flet is never named, no performance is quoted, the count comes from the
public addresses of those who start, and the P&L is read beside the retention.

## What this test can and cannot do

**It can refute. It cannot confirm.** The sample is five, and Karim chooses it for likelihood of
interest — the most favourable conditions the project will ever get. So:

- **Refuted if none of the five starts within 14 days.** If the five members most likely to
  want this, invited personally by someone they trust, with a working tool one click away, all
  decline — the claim that vouching moves people is dead, and it died cheaply.
- **Not confirmed by any result.** Three of five starting would move the claim from *untested*
  to *not refuted under the best available conditions*. That is genuinely worth having, and it
  is not evidence that a stranger's server behaves the same way.

The charter's first success criterion — twenty members still copying at day 30, on 2026-12-31 —
is **not** measured by this and is unchanged. This is a refutation gate placed in front of it,
not a substitute for it.

## What Karim sends

> Je t'écris en direct parce que je sais que tu suis @trader1, @trader2 et @trader3 dans le
> serveur. J'ai vérifié qu'ils tradent bien leur propre argent, et je me porte garant de qui
> ils sont — pas de ce qu'ils vont gagner.
>
> Si tu veux en suivre un, ça se fait avec un outil qui existe déjà, sans que personne d'autre
> ne touche à tes fonds : `<lien>`
>
> Si tu te lances, dis-le-moi et donne-moi ton adresse publique — elle est déjà visible de tous
> sur la chaîne. Ça me permet de voir ce que ça donne pour toi dans un mois et de te le dire
> honnêtement.

## What is recorded

| Measure | How | Grade |
|---|---|---|
| The five invited, and **why Karim chose them** | His own words, recorded at D0 | fact, and a stated bias |
| How many started, by D14 | Their public addresses, read on the venue | fact, verifiable |
| Still copying at D30, and each one's P&L | The same addresses | fact, verifiable |
| Anyone who declined, and what they said | Karim's report | **declarative** — it carries that grade |

**D0 is the day the five messages are sent.** D30 must land before 2026-12-31.
