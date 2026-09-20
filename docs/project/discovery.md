---
decision: proposed          # proposed | go | clarify | kill — the decider decides
decider: "@napkinstack-admin"  # the human who decides, recorded at intake
decided_on:                 # YYYY-MM-DD, with the decision
challenger: ""              # stage 5: @human, or the agent session — required for a go
idea: "docs/project/inputs/idea.md"         # the idea as given, kept in docs/project/inputs/
round: 1
---

# Discovery

> Started by the engine's `discover` command, run by your agent (`playbooks/discovery.md`).
> One document, a decision at the end of each round.

## 1. Intake

*Confirmed by the decider, 2026-09-20, as written — including the three inferences below.*

flet is a bot that lives inside an online community's existing channel — Discord or
Telegram. It serves two people at once: the community's administrator, who wants to earn
from the activity their community already generates, and the member, who wants to copy a
trader without leaving the place where that community talks. The administrator curates the
list of traders the community may copy; a member picks one or several of them from that
list; the copying then runs on Hyperliquid from inside that same experience, and a small
commission is taken on the transactions it generates. The selection stays under the
community's control — the administrator alone decides who may be proposed. The first
version aims at the simplest experience that works: the admin selects, the member chooses,
the platform takes its commission. A later one may let members vote on the list.

**Inferred by the framer, absent from the idea file, and confirmed by the decider:**

- The experience lives inside the community's channel, rather than in a separate
  application the channel links to.
- "Monetise the activity generated" means the commission accrues to whoever operates the
  product; how it is shared with the community is not stated.
- The traders being copied trade on Hyperliquid themselves — the idea names Hyperliquid
  only as where the member's copying happens.

**Open questions:**

- Who holds the members' funds and their keys while the copying runs?
- Does a first community already exist, and is its administrator reachable?
- Is the operator of the product the same person as the community's administrator, or two
  different parties?

## 2. Research

> `docs/tooling-profile.md` has no tool in the "Reliable documentary research" row, so this
> round used the tools at hand: the agent's web search and page fetch. Marked below:
> *primary* — read on the source's own site; *reported* — a figure a company states about
> itself; *excerpt* — seen only in a search result, the primary source not read.

| Claim | What it changes for the idea | Source |
|---|---|---|
| Hyperliquid already ships copy trading: a **vault** lets a trader run depositors' capital for a **10% profit share**, minimum deposit 100 USDC, **10k USDC creation fee**, and the leader must hold **≥5% of the vault at all times**. | The core act — a member follows a trader on Hyperliquid — exists on the venue itself, at no cost to the member. flet has to justify what it adds over "here is the vault link". But the 10k USDC fee prices small community traders out of vaults, and that is the opening. | [Hyperliquid docs, vault leaders](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults/for-vault-leaders-legacy) — *primary* |
| Hyperliquid pays third-party frontends natively: **builder codes** take a fee on fills routed through an app, capped at **0.1% perps / 1% spot**, in tenths of a basis point. The user signs an `ApproveBuilderFee` with their **main wallet**; a builder needs ≥100 USDC of perps account value and `standard` account abstraction; a user holds at most **10 builder approvals**. | The "small commission on transactions generated" needs no bespoke billing — it is a platform primitive, taken on-chain. It also sets a hard revenue ceiling: 0.1% of notional on perps, and not a basis point more. The main-wallet signature is a step in every member's onboarding. | [Hyperliquid docs, builder codes](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/builder-codes) — *primary* |
| A Telegram bot that trades Hyperliquid **inside an existing group** already exists: **pvp.trade** — members see each other's positions and can copy or countertrade them in the group; reported 50k+ monthly users, backed by Alliance DAO. | This is the idea minus the admin-curated list: same channel, same venue, same act. It is the direct competitor, and the difference flet is betting on is *curation by the administrator*, not *trading in Telegram*. | [Delphi Digital](https://members.delphidigital.io/feed/hyperliquids-social-trading-arena) — *excerpt* |
| ESMA's supervisory briefing (ESMA35-42-1428, **30 March 2023**) states that copy trading services fall under **portfolio management or investment advice** — both MiFID II investment services. Expectations cover costs and charges, product governance, suitability, inducements, and **the qualifications of the traders being copied**. | An administrator who selects which traders may be copied is doing the selecting — the act ESMA points at. This is the finding most likely to decide whether the product can serve EU members at all without an authorised firm behind it. | [ESMA](https://www.esma.europa.eu/press-news/esma-news/esma-provides-guidance-supervision-copy-trading-services) — *primary* |
| MiCA does not cover perpetual futures; they fall under MiFID II, and offering them to EU retail requires **both** a CASP licence and MiFID II authorisation. In France the AMF's transitional period for existing providers ended **1 July 2026**; providing the service unauthorised carries up to two years' imprisonment and a €30,000 fine. | The venue is a perps venue. If the members are in the EU, the regulatory question is not MiCA's but MiFID II's, and it is not a paperwork question. | [AMF](https://www.amf-france.org/en/news-publications/news/amf-reminds-digital-asset-service-providers-transitional-period-allowing-them-continue-providing) — *primary*; [CoinDesk](https://www.coindesk.com/opinion/2026/07/01/europe-is-closing-the-door-on-offshore-crypto-but-it-s-leaving-the-riskiest-window-open) — *excerpt*, opinion piece |
| Hyperliquid's own terms exclude **Restricted Persons**: residents of the United States and of Ontario, Canada, sanctioned jurisdictions, and US citizens wherever they are; the front end blocks them. | Who may be a member is already bounded by the venue. A community's geography stops being a marketing question and becomes a product constraint. | [Datawallet](https://www.datawallet.com/crypto/is-hyperliquid-available-in-the-usa) — *excerpt*. The primary page `app.hyperliquid.xyz/terms` renders in JavaScript and could not be read; **to be confirmed on the primary source before any go**. |
| The field runs on two distinct models: **profit share on realised gains** — Hyperliquid vaults 10%, Bitget 10–20% (up to 50% on private programmes), OKX ~10% (max ~30%), Bybit set per master trader on a high-water mark — or a **flat per-trade fee**: Telegram bots charge ~1% (Trojan, Maestro, BONKbot, BullX), Banana Gun 0.5% on Ethereum. | The idea says "a commission on the transactions generated" — the flat model. It earns on losing trades too, which is a different promise to the member than a profit share, and a different conversation with a regulator. | [Bitget](https://www.bitget.com/support/articles/12560603892733), [Bybit](https://www.bybit.com/en/help-center/article/Copy-Trading-Profit-Sharing-Explained) — *reported*; bot fees — *excerpt* |
| What a community monetising trading does today: paid signal subscriptions, tiered, roughly **$30–$300+ per month**. | This is the administrator's real alternative, and it pays whether or not a member trades. flet's commission only pays when members trade — better aligned, more volatile. | Review sites only — *excerpt*, no primary source found |

**Assumptions** — what could not be sourced:

- **Copin's actual fees.** It is named as a non-custodial Hyperliquid copy-trading platform
  with free and pro tiers, but no price was found. Explicitly **not found**.
- **Whether any existing product offers an administrator-curated list restricted to one
  community.** Nothing found either way — this is the claimed novelty and it is unverified.
- **CopyLiquid**, announced August 2026 as "the first copy trading platform on Hyperliquid",
  is known only through its own press releases and a token presale. Treated as an
  announcement, not as a shipped competitor.

**Open questions:**

- **Which countries are the members in?** Nothing in the idea says. Every legal finding
  above changes answer depending on it, and it is the most decision-changing question open.
- **Does the product ever hold members' funds or keys, or does it only route orders the
  member's own wallet signs?** Builder codes work on the second model; custody would change
  the licensing question, the security surface and the shape of the first module.
- **Flat commission or profit share?** The idea says flat; the venue caps it at 0.1% on
  perps; the alternatives mostly charge on gains.

*Answered in stage 3:* the members are majority EU; the product takes no custody; the
decider operates and collects, the administrator curates for free.

## 3. Define

**Users and their problem:**

Three parties, not two:

- **The administrator** of a Discord community — identified, reachable, and willing to
  install the bot in their server *once it is built*.
- **The traders** the administrator would authorise — some are available to test.
- **The members** who would copy them — some are available to test.

**Status: the problem is not quoted from users.** The decider reports willingness to test;
no member's words, no size of the community, no count of people spoken to. Under this
playbook that makes the members' problem an **assumption held by the decider**, not a
finding — and the commitment obtained ("yes, after the development") is the one that costs
its giver nothing, since it is made once the build is already paid for.

What *is* established, and it is not nothing: distribution for a first release and a panel
willing to try it. That removes the cold-start problem, not the value question.

**Constraints:**

- **Who operates the service:** the decider, in their own name, with no authorisation. They
  take the commission and are who a member would turn to when something goes wrong.
- **What the administrator does:** installs the bot on their Discord server and curates the
  authorised traders — explicitly to filter out scammers — and **takes no share of the
  commission**. They are providing a feature to their community, not running a business on
  it. The traders are members of that same community.
- **Where:** Discord, the community's existing server. The venue is Hyperliquid perpetuals.
- **Who the members are:** majority resident in the EU.
- **Custody:** none. flet never holds members' funds or keys; it routes orders the member's
  own wallet signs. *Assumption stated by the framer, not contradicted by the decider* —
  it follows the venue's own mechanism, where `ApproveBuilderFee` is signed by the member's
  main wallet.
- **Revenue model:** a flat commission on the transactions generated, which the venue caps
  at 0.1% of notional on perpetuals.
- **Regulation: unresolved, and it is the binding constraint.** The service is provided by
  an unauthorised operator to EU residents, on perpetuals, and its central act — a curated
  list of traders that members copy — is what ESMA's briefing points at. The
  administrator taking no fee does not move the service provision: the commission, the
  product and the relationship with the member are the decider's.

**Open question, to be answered before the charter:** the budget and the time available —
neither was established in this round, and the feasibility risk cannot be weighed without
them.

**Success signals:** the decider kept all four proposed, each testing a different claim.
The windows below are the framer's proposal; **the thresholds are the decider's to set and
are not set yet.**

| Signal | Window | What it would prove | Threshold |
|---|---|---|---|
| Members start a copy, and are still copying later | 30 days after install, measured again at 60 | Value for the member — retention is the one thing that cannot be talked into existence | *to set* |
| Notional generated, and commission actually collected | first month | Viability: at a cap of 0.1% of notional, this says immediately whether the economics exist | *to set* |
| The administrator updates the list unprompted | several weeks | The most fragile assumption here: that they do the differentiating work for nothing | *to set* |
| A trader brings members who were not copying before | first month | Whether curation *creates* demand or merely channels demand that already existed | *to set* |

Keeping all four means none is ranked. Four signals for a first release is a lot, and the
question the decider has not yet answered is the useful one: **which of them, if it came
back negative, would stop the project?**

**Open questions:**

## 4. Shape

**Value hypothesis:**

A member copies a trader **because the community already knows that trader and an
administrator they trust has vouched for them** — not because a ranking says the trader is
good. That is what would make someone click copy who never clicked it on a leaderboard, and
it is why the trader does not need the 10k USDC a Hyperliquid vault costs to open.

It is **wrong** if members pick by past performance anyway, if they would have copied the
same traders through pvp.trade or a plain vault link, or if the administrator's endorsement
turns out to be worth less to them than a public track record.

**Press release** — *imagined; launch day not set, placeholder below.*

> **flet brings copy trading into the Discord servers that already talk about it**
> — <launch day>
>
> Members of trading communities on Discord have watched the same handful of traders post
> their entries for months. Copying them meant retyping each trade by hand, or leaving for
> a platform neither they nor their community chose. flet puts the act where the
> conversation already is: the server's administrator marks which traders may be copied —
> the ones the community knows, and has vetted against scammers — and a member picks one
> and copies them on Hyperliquid without leaving Discord, with their own wallet and their
> own keys.
>
> *"I'd been following three people in the server for months. I never trusted a ranking
> enough to click copy on a stranger."* — a member, **imagined quote**
>
> flet never holds members' funds or keys. It takes a small fee on the trades it routes,
> capped by Hyperliquid at 0.1% of notional.

**Convinces the decider?** **Yes**, as written — recorded 2026-09-20.

**No-gos:**

*The decider's, **adopted** 2026-09-20:*

1. **Never hold a member's funds or private keys.** As a no-go rather than a constraint, it
   also forbids the "just for convenience" version of it six months later.
2. **No promised, projected or advertised returns, and no past performance used as a sales
   argument.** A product stance, and the cheapest distance to keep from what ESMA's
   briefing scrutinises.

*The framer's, **proposed and not adopted** — they remain open, not decided:*

3. **No leaderboard ranking the authorised traders by performance.** Not taken. A ranking
   therefore stays possible, and with it the risk that the product's differentiator —
   community trust — is quietly replaced by the ranking it was meant to beat.
4. **No trader from outside the community in version 1.** Not taken.

*The decider's change of scope, recorded:*

5. **Member voting on traders is envisaged in version 1** — explicitly against the framer's
   proposal to defer it, and beyond the idea file, which placed voting "in time". This is
   the decider's call and it is recorded as such.

   **It is not a neutral addition.** The value hypothesis of stage 4 rests on *an
   administrator the members trust having vouched for a trader*. A vote moves the vouching
   from that administrator to the crowd — which is a **different hypothesis**, closer to
   the performance ranking that no-go 3 would have forbidden, and it loosens the one thing
   that distinguishes flet from pvp.trade. It also reopens a regulatory question that
   stage 3 had narrowed: if the members collectively select, who is providing the
   selection?

**Open questions:**

- **Does voting replace the administrator's curation, or sit under it** — the administrator
  keeping a veto? The two answers are different products, and the value hypothesis only
  survives the second.
- Which of the four success signals, coming back negative, would stop the project?
- Budget and time available — still unanswered, and needed before the charter.
**Open questions:**

## 5. Challenge

**Challenger:** <@human, or the agent session> · <date>

**Pre-mortem:** <the reasons, each tagged with its risk>

**The four risks:**

| Risk | Riskiest assumption | Cheapest test — and the result that refutes it |
|---|---|---|
| Value | | |
| Usability | | |
| Feasibility | | |
| Viability | | |

**Counter-evidence:**

**Flaws in stages 1 to 4:** <each citing its line>

## 6. Decision

<go · clarify · kill; the reasons; for a go, why each objection does not block it, and what
the first cycle carries: spikes, no-gos.>
