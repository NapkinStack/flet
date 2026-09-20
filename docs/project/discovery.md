---
decision: clarify           # proposed | go | clarify | kill — the decider decides
decider: "@napkinstack-admin"  # the human who decides, recorded at intake
decided_on: 2026-09-20      # YYYY-MM-DD, with the decision
challenger: "agent session (challenger), 2026-09-20; independent agent session (challenger), 2026-09-21"  # stage 5, one per round
idea: "docs/project/inputs/idea.md"         # the idea as given, kept in docs/project/inputs/
round: 3
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

---

### Round 2 — can the product run without holding members' funds, and be paid only on transactions?

Asked by the decider at the round-1 decision, against flaw **F2**. Same marking as above;
*primary-negative* means the source is silent where a statement was looked for, which is not
the same as the source denying it.

| Question | What the sources say | Mark |
|---|---|---|
| **Can a third party place orders for a member without holding their funds?** | Yes. An API wallet — also called an agent wallet — is "an alternate signing key that a master account can authorize to sign transactions on behalf of itself or any sub-accounts". The member's funds never leave the member's own account. The delegation expires if an expiry was set, is deregistered when a new unnamed API wallet is registered, and lapses when the registering account no longer has funds. | [Hyperliquid docs, nonces and API wallets](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets) — *primary* |
| **Can that agent key withdraw or move the member's money?** | **No — and the reason is structural, not a policy that could change.** `withdraw3` signs over exactly `hyperliquidChain`, `signatureChainId`, `amount`, `time`, `destination`; `usdSend` over `hyperliquidChain`, `signatureChainId`, `destination`, `amount`, `time`. **Neither payload has any field naming an account to act on behalf of** — no `vaultAddress`, no master address, nothing. Order actions do have that field, which is how they act for a sub-account or a vault. So the account debited by a withdrawal is simply whoever signed it: an agent key signing `withdraw3` withdraws from the agent key's own empty address. The action format cannot express "withdraw from the account that authorised me". | [Exchange endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint) — *primary, structural*. Corroborating: [Privy](https://docs.privy.io/recipes/hyperliquid/agents-and-subaccounts) calls agent wallets "permissioned signers that **do not hold funds**" — *secondary*. Note: the docs still never state the prohibition as a sentence — *primary-negative* — so this is an argument from the documented payload shape, and it is only as complete as the documentation. |
| **What the venue does say about who must sign what** | USDC transfers and spot sends are "user-signed actions", signed over the real chain id with a human-readable typed struct so a wallet can display them — a different signing path from ordinary L1 trading actions. And, stated outright for one action: `ApproveBuilderFee` "must be signed by the user's main wallet, **not an agent/API wallet**". | [Exchange endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint), [builder codes](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/builder-codes) — *primary* |
| **Can the product be paid purely on transactions, touching no member money?** | **Yes, and this part is fully verified.** A builder fee is taken on-chain as part of the venue's own fee logic and credited to the builder, who claims it through the standard referral reward process. No member funds pass through the product at any point. Cap: 0.1% on perps, 1% on spot. The builder must hold at least 100 USDC of perps account value and use `standard` account abstraction; a member may hold at most 10 active builder approvals. | [Builder codes](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/builder-codes) — *primary* |
| **Sub-accounts, as a risk primitive** | A sub-account is an isolated margin sandbox spawned by the master account. "Subaccounts and vaults do not have private keys" — the master account signs for them, naming the sub-account in the `vaultAddress` field. Cross-margin does not bleed between sub-accounts: a liquidation in one leaves the others untouched. | [Exchange endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint) — *primary*; the isolation property — *excerpt* |
| **Which vault rail carries the 10k USDC fee** | The fee is on the **legacy** rail. Current vaults are built on HyperEVM with "fully customizable accounting"; legacy vaults were "introduced in 2023 and do not support HIP-3 or spot trading". The overview page states **no fee at all**, for either rail — so "the new rail is free" is *not* established; what is established is that the 10k figure belongs to the page Hyperliquid titles "(legacy)". | [Vaults overview](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults) — *primary* for the two rails, *primary-negative* on fees |

**What this settles, and what it does not.**

The architecture the decider asked about **exists**: the member keeps their funds and their
main key, approves a revocable, expirable agent key that the product holds, and the product
is paid by the venue itself on the flow it routes, never out of the member's balance. On the
second question — payment purely on transactions — the answer is an unqualified yes, from
primary sources.

On the first question the answer is **yes with one hole**: the product would hold **a**
private key. Not the member's, not one that can move money out — but a key. So no-go 1
("never hold a member's funds or private keys", line 188) does not resolve itself; it has to
be read. Under "no custody of funds" the agent-wallet design satisfies it. Under "no key of
any kind" it does not, and automated copying becomes impossible — leaving signal relay,
which Skadden's analysis (section 5.3) places under investment advice rather than outside
regulation.

And a distinction the sources make that the product must not blur: an agent key **cannot
take** the member's money, but it **can lose** it. Liquidating a leveraged position is not a
withdrawal. Pre-mortem item 10 survives this finding intact.

### Round 2 — the feasibility shadow run, actually run

Test **5.2 — feasibility** was run on 2026-09-20, read-only, no keys, no orders, no money.
It is the only one of the four tests that needed nobody else.

**Method, so it can be repeated.** Hyperliquid's public leaderboard
(`stats-data.hyperliquid.xyz/Mainnet/leaderboard`) was filtered to accounts between 20k and
400k USDC with more than 2M USDC of 30-day volume and a positive month — the size a
community trader plausibly has. Three were taken. Their last 2,000 fills came from
`api.hyperliquid.xyz/info` (`userFills`), cut to the **last 3 days** so the three are
compared on equal ground. Entry slippage was measured against 1-minute candles
(`candleSnapshot`): for each fill where the trader **took** liquidity, the adverse move
between their fill price and the close of the minute containing it — a proxy for a copier
reacting within the same minute, and no finer than one minute. Fees are **not modelled**:
they are the `fee` field of the trader's own fills, scaled to the copier's account.

**The slippage is fine. That is not where this breaks.**

| Trader | Fills / day | Median slippage | p90 | Over the proposed 15 bps threshold |
|---|---|---|---|---|
| `0x102d1d1a…` | 522 | **+0.0 bps** | +5.8 | 0% |
| `0x7c36139b…` | 443 | −0.4 bps | +23.1 | 15% |
| `0xe7795fce…` | 5 | −6.1 bps | −5.4 | 0% |

The threshold the challenger proposed — *median entry slippage above 15 bps* — **is not
breached by any of the three**. On this criterion the test passes. It measured the wrong
thing, and that is itself the finding: three other constraints decide feasibility, and none
of them was in the test as designed.

**What actually breaks it.**

| Finding | Measurement | What it means |
|---|---|---|
| **Half to two-thirds of the fills are not copyable at all.** | Liquidity *posted*, not taken: 0%, **54.1%**, **60.0%** of the three traders' fills. | A resting limit order is filled when the market comes to it. A copier reacting *after* that fill cannot reproduce it — the price has already traded there. They take liquidity at a worse price, or post and may never fill. For two of three traders, most of the strategy is structurally out of reach. |
| **Most orders are too small to place once scaled down.** | Hyperliquid's floor is **10 USDC of notional**, confirmed empirically: **the smallest of 2,912 observed fills is 10.10 USDC, and not one is below 10**. For a 500 USDC member, **38%, 85% and 87%** of the three traders' orders fall under it. | Copying a 316k account with 500 USDC means a scale of 0.0016. Most orders become dust the venue refuses. The product has a **minimum member ticket**, and it is not a few hundred USDC. |
| **The fees destroy the account before the strategy can help it.** | Copying trader `0x102d…` costs a member **28.5% of their account in 3 days — 285% a month** — whatever their account size, since it scales. Trader `0x7c36…`: 28.8% a month. | That trader turns their account over 72 times a day. A copier turns theirs over 72 times a day too, and pays on every turn. No edge survives this. |
| **flet's own commission is the larger half of that burden.** | On trader `0x102d…`, over 3 days: platform fees **33.21 USDC**, flet's builder fee **109.18 USDC**. The trader's own realised fee rate is **0.0304%** of notional; the cap flet may take is **0.1%** — **3.3× what the venue itself charges**. | The idea says "a small commission". At the cap it is not small: it is the dominant cost the member pays, and more than three times the exchange's. |

**The minimum member ticket, per trader, to be able to place…**

| Trader | 50% of their orders | 80% | 95% |
|---|---|---|---|
| `0x102d1d1a…` | 340 USDC | **4,896** | 42,953 |
| `0x7c36139b…` | 2,414 USDC | **6,013** | 16,376 |
| `0xe7795fce…` | 2,753 USDC | **51,367** | 245,792 |

**Corrected the same day: the three traders were unrepresentative, and the correction
reverses the conclusion.** They were picked by 30-day ROI, which selects scalpers. Screening
the **whole** leaderboard instead — 13,536 accounts above 5k USDC active over 30 days — the
median monthly turnover is **8.4×** the account, which costs a copier **1.2% a month** in
total fees, not 285%. **68.6%** of active accounts stay under a 5%-a-month fee burden, and
**7,635** of them also closed the month positive. *The fee problem is a selection problem,
not a structural one.*

**The 10 USDC floor, however, survives the correction — and yields the product's real
constraint.** Sampling 14 traders from the copyable-and-winning population: the ticket a
member needs to place 80% of a trader's orders has a **median of 6,583 USDC**; none of the
14 is reachable with 1,000 USDC and two with 2,000. The rule behind it, measured across the
sample: **a member needs roughly one twentieth of the trader's account**, the ratio ranging
from 8 to 80. So the administrator's list must be matched to the members' wallets, not only
to the members' trust.

**Supply exists at every size**, once the rule is applied — copyable, winning traders whose
account is at most 20× the member's ticket:

| Member ticket | Trader accounts in range | Copyable **and** winning |
|---|---|---|
| 500 € | 5k–10k | 210 |
| 1,000 € | 5k–20k | 557 |
| 2,000 € | 5k–40k | 966 |
| 5,000 € | 5k–100k | 1,666 |

### Round 2 — the revenue forecast, on minimal stated assumptions

Requested by the decider in the absence of the real figures. **Every input below is an
assumption of the framer, not a measurement**, except the turnover band and the fee cap,
which are measured above. Revenue = copiers × ticket × monthly turnover × 0.1%.

| Scenario | Members | Trade perps | Adopt | Active copiers | Ticket | Turnover | **Revenue / month** |
|---|---|---|---|---|---|---|---|
| Minimal | 150 | 8% | 25% | 3 | 1,000 € | 10× | **30 €** |
| Base | 400 | 12% | 35% | 17 | 1,500 € | 15× | **378 €** |
| High | 1,000 | 15% | 40% | 60 | 2,500 € | 25× | **3,750 €** |

**What 2,000 €/month from a single community would require:** 200 simultaneous active
copiers at 1,000 € and 10× turnover; or 67 at 2,000 € and 15×; or 27 at 3,000 € and 25×.

**Cross-check against the one measured comparable.** pvp.trade — same venue, same
builder-code rail, 50,000+ monthly users claimed — earned **$14,899** in its last 30 days
(section 5.3, read from DefiLlama). The high scenario for *one* community is a quarter of
that. The base scenario is 2.5% of it.

**What the forecast says, plainly.** One community does not pay for a build. The base case
covers a subscription, not an engineer. The product is therefore either a **multi-community
play** — which multiplies the regulatory exposure of section 5.3 and needs not one unpaid
Karim but dozens — or it needs a different take than 0.1% of notional. Worth noting for that
second branch, from section 2 round 1: the venue's **vault** rail natively supports a **10%
profit share**, which pays only when the member gains, and is a different promise to make.

None of this is a recommendation. It is the arithmetic the decider asked for, on assumptions
the decider has not yet replaced with facts.

---

**Honest limits of this run.** Three traders, three days, chosen from the top of a public
leaderboard — not a sample of the traders an administrator would actually vouch for, and
selected for recent success. The slippage proxy has one-minute resolution. The fee figures
are **optimistic**: they scale the *leader's* fee tier onto a small copier, who would sit in
a worse tier. And proportional copying is assumed; copying at a fixed size, or only
replicating position changes above a threshold, would dodge the 10 USDC floor — at the cost
of no longer running the leader's strategy.

**What it changes for the product**, stated as questions the round must now answer rather
than as conclusions:

1. **Is there a minimum member ticket, and is it above what a community member will risk?**
   The numbers say the ticket is in the thousands, not the hundreds.
2. **Must the authorised traders be selected for being copyable** — low frequency, taker
   fills, large orders — and not only for being trustworthy? That is a new criterion on
   Karim's list, and it is technical, not social.
3. **Is 0.1% the right take, when it is 3.3× the venue's own fee?** The cap is a maximum,
   not a rate. Lowering it eases the member's burden and shrinks a revenue that the
   counter-evidence already found thin.

---

**The empirical confirmation is blocked, and the structural finding largely replaces it.**

The plan was: register an agent wallet on testnet, attempt `withdraw3` and `usdSend` with it,
record the refusal. It cannot be run from here. Hyperliquid's own faucet page states that to
receive the 1,000 mock USDC "you need to have deposited on mainnet with the same address"
(*primary*), and the documentation describes no other route to testnet balance. A throwaway
address cannot be funded without a real mainnet deposit, which is the decider's money and was
not spent.

What replaced it is arguably stronger: the payload analysis above shows *why* an agent cannot
withdraw, rather than merely observing that one attempt failed. Its weakness is different —
it assumes the documented payload list is complete.

**What is still not established**, and would need either the testnet run or a statement from
the venue:

- Whether an agent key can call `approveAgent` and register a further agent.
- Whether `usdClassTransfer` and `subAccountTransfer` accept an agent signature; the docs do
  not say, and `subAccountTransfer` is not documented on the page read.

Neither lets an agent move money to a stranger's address on the evidence above, but neither
is closed. **Round-2 item, for whoever holds a mainnet-activated address** — an hour of their
time, not a purchase.

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

## 5. Challenge — round 1

**Challenger:** agent session (challenger), independent of the session that wrote stages 1
to 4 · 2026-09-20

> **Line references in this section are to the document as at commit `b77915b`** — the
> revision the challenger read. Round-2 material was later added to section 2, which shifted
> every line after it; resolve a citation against that commit, not against the current file.
> Nothing in this section has been edited since it was written.

> Section 1 is confirmed (line 17), so this challenge is against the document as written.
> `docs/tooling-profile.md` declares no research tool, so — as in stage 2 — this round used
> the tools at hand: the agent's web search and page fetch, named at each finding. Same
> marking: *primary* — read on the source's own site; *reported* — a figure a company
> states about itself; *excerpt* — seen only in a search result; *assumption* — unsourced.
> Arithmetic done here from sourced figures is marked *derived*.

### 5.1 Pre-mortem

It is September 2027. flet shipped. It is being wound down. The plausible reasons:

1. **Nobody clicked copy.** Thirty members connected a wallet over the year, four started a
   copy, one was still copying at day 60. The commission for the whole year did not cover a
   month of the build. The community liked the idea and did not use it. *(value)*
2. **Onboarding broke the promise at step one.** Before a member could copy anything they
   had to leave Discord, open a wallet, and sign `ApproveBuilderFee` with their main wallet,
   then approve an agent wallet. Most people stopped at the wallet screen. The product that
   shipped was "a Discord link to a web page", which is what the press release said it was
   not. *(usability)*
3. **The copies did not track.** Members entered behind the leader, at worse prices, with
   position sizes scaled to smaller accounts. On leveraged perps, several copiers were
   liquidated in weeks where the leader was not. The community blamed the administrator who
   had vouched for the trader. *(feasibility → value)*
4. **The administrator stopped curating.** They took no share (line 114), the work was
   unpaid, and after three weeks the list went stale. What remained was pvp.trade with fewer
   features. *(value / viability)*
5. **Voting turned curation into a leaderboard.** Members had no basis to vote on but
   screenshots of P&L, so they voted on P&L. The differentiator — an administrator's
   vouching (line 154) — was replaced by the ranking it was supposed to beat, and no-go 2
   (line 189) was broken in the channel, by members, where it could not be enforced. *(value)*
6. **A member lost money and asked who was responsible.** The operator was an unauthorised
   natural person, the members were EU residents, the instrument was perpetual futures, and
   the central act was a curated list of traders to copy. There was no good answer, and the
   cheapest response was to shut down. *(viability)*
7. **The administrator was told they were exposed too.** Nobody had ever explained that
   selecting the traders — for free, for someone else's commission — is the act regulators
   look at. They removed the bot the same week. *(viability)*
8. **The alternatives were already there and cheaper.** Copin routes non-custodial
   Hyperliquid copy trades at a reported 0.05% of trade size; HyperMirror at 0.1%. The
   community used a link. *(value)*
9. **The arithmetic never worked.** At the venue's 0.1% cap, the community had to generate
   €2,000,000 of notional a month to pay €2,000 a month. It generated a fraction of that.
   *(viability)*
10. **"Non-custodial" did not survive contact.** To copy automatically, flet held an agent
    key able to trade the member's account. One scare — a bug, a bad fill loop, a rumour of
    a leak — and the trust the whole product was built on was gone. *(feasibility / viability)*

### 5.2 The four risks

Thresholds below are **proposed by the challenger**. They are the decider's to set.

| Risk | Riskiest assumption | Cheapest test — and the result that refutes it |
|---|---|---|
| **Value** | Lines 154-156: a member copies **because a trusted administrator vouched**, not because of a track record — and enough of them do it, and keep doing it, to matter. Nothing in stages 1 to 4 tests this; stage 3 concedes the problem is not quoted from users (line 98). | **The link test. No code, one Discord message, 30 days.** The administrator posts, in their own name, a shortlist of 3 traders they vouch for, with a link to an existing non-custodial Hyperliquid copy tool (Copin, HyperMirror). That is flet minus the Discord integration. Count at day 14 and day 30: clicks, wallets connected, copies started, copies still open. **Refuted if** the endorsement moves too few people. *Proposed threshold: fewer than 10 members start a copy within 14 days, or fewer than 5 still copying at day 30.* This also settles stage 4's own falsifier (line 159): if they copy through the existing tool, they would have copied through the existing tool. |
| **Usability** | Line 24 and lines 172-174: the member copies **"without leaving Discord"**. Refuted on its face by the source stage 2 itself cites: `ApproveBuilderFee` "must be signed by the user's main wallet, not an agent/API wallet" (*primary*, Hyperliquid builder-codes docs, also recorded at line 56). A Discord bot cannot produce that signature. | **Walkthrough of the real onboarding path, one week, no backend.** A throwaway page: Discord message → browser → connect wallet → sign `ApproveBuilderFee` on testnet → approve an agent wallet → back to Discord. Sit with 5 members of the target community, 30 minutes each, unaided, screen shared. **Refuted if** they cannot get through it. *Proposed threshold: 2 or more of 5 fail to complete unaided in under 10 minutes.* If refuted, the press release (lines 165-180) is describing a product that cannot be built as described, and must be rewritten **before** any go. |
| **Feasibility** | That a copy can be mirrored faithfully enough to be worth paying for, **and** that it can be done without flet holding a key that can lose the member's money — while budget and time are still unknown (line 129). | **Two-week shadow run, read-only, no keys, no orders.** Watch the fills of 3 traders the administrator would authorise; simulate a proportional copy for a 1,000 USDC account; record entry slippage against the leader's fill and whether the simulated copier would have been liquidated in a window where the leader was not. **Refuted if** the copy diverges enough to harm the copier. *Proposed threshold: median entry slippage above 15 bps, or any simulated liquidation the leader did not suffer.* **And, separately, before any code:** write down who holds the agent-wallet key. See flaw F2 — as no-go 1 is written (line 188), the answer may be that nobody can, which means there is no product. |
| **Viability** | Lines 121-122 and 140: a flat commission the venue caps at **0.1% of notional** pays for this. And lines 123-127: an unauthorised operator can serve EU residents perpetual futures with a curated trader list. | **(A) Economics, one afternoon, no code.** Get from the administrator the member count and the number who trade Hyperliquid today; get from the candidate traders their real monthly notional (they are community members — a read-only address is enough). Compute month-6 revenue = 0.001 × copiers × notional per copier. **Refuted if** the honest optimistic number is trivial. *Proposed threshold: below €1,000/month at month 6.* Calibration, verified below: pvp.trade — same venue, same builder-code rail, 50k+ monthly users claimed — earned **$14,899 in the trailing 30 days**. **(B) Law, two weeks, one bill.** A written scoping opinion from a lawyer qualified in **the one named member state** where most members live, on one question: does an unauthorised natural person operating a Discord bot that lets residents of that state pick a curated trader and routes their perps orders to Hyperliquid for a fee on notional provide an investment service requiring authorisation — **and does the administrator who curates the list provide one?** **Refuted if** the answer is yes for either party. *Proposed threshold: any "authorisation required" that cannot be structured around inside the decider's own budget and deadline is a kill, not a clarify.* The question cannot be asked yet: line 116 says only "majority EU" and names no country. |

**One honest complication with test A above (value):** the link test has the administrator
publicly recommend traders. That is the act ESMA's briefing points at (line 58). The
cheapest value test therefore carries the exposure the legal test is meant to size. Test
**(B)** should start first, or at the same time — not after.

### 5.3 Counter-evidence

Tools: the agent's web search and page fetch.

| Finding | What it contradicts | Mark / source |
|---|---|---|
| **pvp.trade's revenue has collapsed.** Trailing 24h **$180**, 7d **$1,412**, 30d **$14,899**, 12 months **$502,489**, all-time **$8,005,840**. Daily series 7–18 Sept 2026: $31 to $761. | The closest comparable — same venue, same builder-code rail, same "trade in the group chat" act, VC-backed, 50k+ monthly users claimed (line 57) — earns about **$500/day averaged over a year and about $180 on a recent day**. 94% of everything it ever earned was earned before the last twelve months. Stage 2 cites pvp.trade as the competitor to beat; the readable number says the category it competes in is not currently paying. A single Discord community is a small fraction of 50k users. | *primary* — read directly from the DefiLlama API, `https://api.llama.fi/summary/fees/pvp.trade`. DefiLlama is an aggregator, not the company; figure is what DefiLlama reports. |
| **Non-custodial Hyperliquid copy trading already ships, at or below the cap.** **Copin**: "0.05% fee on trade size when opening copy trade positions", executed via an API wallet. **HyperMirror**: mirrors a basket of up to 10 Hyperliquid traders in isolated sub-accounts, non-custodial, "a 0.1% builder fee". **HyperX** and **HyperDash** named alongside them. | Directly contradicts stage 2's open assumption (lines 66-67) that Copin's fees are "not found", and undercuts the differentiator at line 157: a trader does **not** need a 10k USDC vault to be copied non-custodially — three or more shipped products already provide that. flet's only remaining difference is the curated list and the Discord surface. It also fixes the price ceiling: a competitor charges **half** the cap. | Copin fee — *excerpt*, `hyperliquidguide.com/guides/trading/copy-trading-guide`, third-party guide, not Copin's own site. HyperMirror — *excerpt*, search result; `hypermirror.io` refused the connection from this sandbox and could not be read. |
| **Hyperliquid's own copy-trading mechanism cited at line 55 is labelled legacy.** The page stage 2 cites is titled "For vault leaders **(legacy)**"; its figures verify exactly (10% profit share, 100 USDC minimum leader deposit, "Creating a vault requires a 10k USDC gas fee", "maintain ≥5% of the vault at all times"). But the vaults overview says current HyperEVM vaults are "a strict improvement over the 'legacy' HyperCore vaults, which were introduced in 2023" and states **no 10k fee** for them. | The 10k USDC figure is real but attached to a deprecated rail. Stage 4 leans on it — "it is why the trader does not need the 10k USDC a Hyperliquid vault costs to open" (line 157) — as if it were a durable barrier. It is not: the replacement path is a deployable contract, and competitors have already routed around it. | *primary* — both Hyperliquid docs pages read directly. The claim that the new path carries no comparable fee is *primary-negative* (the page states none), not a positive finding. |
| **Promoting an unregistered crypto service in France is itself restricted.** Advertising digital-asset services is prohibited unless the provider is registered or approved with the AMF; the 2023 influencer law (n° 2023-451, 9 June 2023) extended this to social-media promotion; intermediaries — media, YouTubers, influencers — can be caught in the infringement; penalties cited up to €100,000, and up to €300,000 and two years for influencer breaches. | Stages 1 to 4 analyse whether the **operator** may provide the service (lines 123-127). They never ask whether the **administrator may promote it to their own members**. If the community is French, the administrator's post announcing flet may be the offence, and the administrator is the unpaid party (line 114). This is a new exposure, on the person whose participation the whole product depends on. | Law-firm analysis read directly: `orwl.fr/en/how-to-lawfully-promote-crypto-services-in-france/` — *primary for ORWL's statement, secondary for the law*. Influencer-law penalties — *excerpt*. Not verified against Légifrance; do not rely on the figures without counsel. |
| **Copy trading with discretion is portfolio management; without it, advice.** "services that provide the service provider with investment discretion by automatically executing the trade signals of third parties will regularly qualify as portfolio management"; "services that require client action prior to the execution of a transaction may qualify as investment advice or investment brokerage". | Corroborates line 58 from an independent source and closes the escape hatch: **both** designs are regulated. A version where the member confirms each trade does not escape MiFID II — it just moves from portfolio management to advice. There is no "make it manual and it's fine" fallback. | *primary* — Skadden, `skadden.com/insights/publications/2025/05/update-on-mica-implementation`, read directly. Law-firm analysis, not a regulator's text. |
| **Unauthorised signal/copy operations in chat apps do get named by regulators.** FCA warning list entry for **Signals2Trades** (published 09/03/2026, updated 10/03/2026): "This firm may be providing or promoting financial services or products without our permission", operating via website, Facebook, TikTok and Telegram. CySEC has added Telegram "forex signals" channels to its warning list; the FSCA (South Africa) brought an enforcement action over forex signals published via Telegram; a Hong Kong court convicted the operator of a subscription Telegram group. | The failure mode in pre-mortem item 6 is not hypothetical, and the cheapest regulatory outcome is not a fine — it is being named on a public warning list, which ends distribution instantly. | FCA entry — *primary*, read directly. CySEC / FSCA / Hong Kong — *excerpt*. |
| **Discord's Developer Policy restricts financial handling by apps.** Developers may not use applications to obtain or transmit financial information or other sensitive information under applicable law except as specifically allowed, and apps monetising through Discord's services must follow its Monetization Terms. | A platform risk absent from stages 1 to 4: the distribution channel is a third party with its own rules, and flet's whole surface is a Discord app that routes financial transactions. Whether this clause bites is unknown — but the document treats Discord as neutral ground, and it is not. | *excerpt* — search result quoting `support-dev.discord.com` Developer Policy; the page returned HTTP 403 to this session's fetch and could **not** be read directly. **Must be read on the primary source before any go.** |
| **Hyperliquid's Restricted Persons clause could not be verified — again.** The definition circulating (US residents/citizens, Ontario, sanctioned territories) matches line 60, but `app.hyperliquid.xyz/terms` renders in JavaScript and returned only the page header to this session too. | Line 60's own caveat stands, independently confirmed. It is still *excerpt* after two sessions tried. A Discord server has no reliable geography and flet proposes no KYC; "majority EU" (line 116) concedes a minority that is not. | *excerpt*, and an explicit **not verified**. |
| **Copy trading's base rate is poor, and regulators say so.** IOSCO notes users rely heavily on historical performance when selecting traders and may underestimate leverage and strategy-change risk; the FCA warns retail investors use copy trading to reach high-risk leveraged products without understanding them. | Bears on retention, which is success signal 1 (line 139). If copiers lose money at the usual rate, the 60-day retention number will be bad for reasons that have nothing to do with whether the administrator's endorsement works — and the value test will read as refuted when the hypothesis was never the problem. Design the value test to record P&L alongside retention. | *excerpt* — both seen only in search results; neither IOSCO's nor the FCA's own document was read. Treat as directional, not as a figure. |

**Explicitly not found:**

- No shut-down, insolvency or regulatory closure of a named copy-trading platform was found.
  Searches on ayondo, ZuluTrade and Darwinex returned operating businesses. One *excerpt*
  claims FxPro closed its SuperTrader service in 2017; not verified. **The "failed
  competitor" evidence the playbook asks for does not exist in readable form** — the
  counter-evidence here is a live competitor's collapsing revenue, not a graveyard.
- No ESMA or national enforcement action against a firm specifically for unauthorised **copy
  trading** was found in 2024-2026. Absence of enforcement is not absence of exposure, and
  it is also not evidence of tolerance.
- **Still nothing, either way, on an administrator-curated list restricted to one community**
  (stage 2, lines 68-69). The claimed novelty remains unverified after a second independent
  search. *Assumption.*

**Derived, from sourced figures — not a finding:**

- At the verified 0.1% cap, **€1,000/month of commission requires €1,000,000 of member
  notional per month**; €2,000 requires €2,000,000. *derived* from the builder-code cap.
- pvp.trade's $14,899 over 30 days implies **at most ~$14.9M of notional** in that window if
  it charges the full cap, and more if it charges less. *derived.*
- Stage 2's own line 62 — a signal subscription at $30-300/month — means an administrator
  with 100 paying members earns $3,000-30,000/month from the alternative, against a flet
  commission pool that pre-mortem item 9 suggests will be in the hundreds. *derived* from an
  *excerpt*-grade figure; the conclusion is only as good as that row.

### 5.4 Flaws in stages 1 to 4

**F1 — Line 157 rests the differentiator on a deprecated fee.** "it is why the trader does
not need the 10k USDC a Hyperliquid vault costs to open". The 10k figure verifies, on a page
Hyperliquid titles "For vault leaders **(legacy)**". The current vault rail is described as
"a strict improvement over the 'legacy' HyperCore vaults" and no such fee is stated for it.
And whatever the vault costs, **Copin, HyperMirror, HyperX and HyperDash already copy
Hyperliquid traders non-custodially without one**. The 10k USDC is not a moat. Remove it
from the value hypothesis and what remains is: *curation by a trusted administrator, inside
Discord*. That is the real claim and it should stand alone. (Minor, same line-55 row: "minimum
deposit 100 USDC" is the **leader's** minimum deposit per the source, not the member's.)

**F2 — Line 188 (no-go 1) may forbid the product. This is the most important flaw here.**
"Never hold a member's funds or private keys" is adopted. Lines 117-120 say flet "routes
orders the member's own wallet signs". Both cannot be true of automated copy trading on
Hyperliquid. Placing orders without the member present requires an approved **agent / API
wallet** — "A master account can approve API wallets to sign on behalf of the master
account" (*primary*, Hyperliquid docs). Someone holds that key. If flet holds it, no-go 1 is
broken from the first copy. If the member holds it, they sign every trade and it is signal
relay, not copy trading — and per Skadden that version is still regulated, as advice. The
third-party evidence points the same way: Copin's model is described as "requires sharing
private key with platform" (*excerpt*). **The document does not notice this.** It should be
resolved before anything else, because the answer determines whether there is a product.
Note also, verified: the docs I read do **not** state what an agent wallet may not do — I
could not confirm that it cannot withdraw. *Not verified.*

**F3 — Line 24 and lines 172-174 promise something the document's own source rules out.**
"without leaving Discord". Line 56 of the same document records that `ApproveBuilderFee`
"is signed by the user's **main wallet**". Stage 2 found it, stage 4 wrote the press release
as if it had not. The press release convinced the decider (line 182) partly on a promise
that cannot be kept, which makes that "yes" worth less than it looks.

**F4 — Line 116, "majority resident in the EU", is not an answer to line 76.** MiFID II
authorisation is granted by a member state; the analysis at lines 58-59 draws on ESMA and on
**French** sources for a country the document never names. Nothing can be asked of a lawyer
until one country is named. And "majority" concedes a minority who are not EU — some of whom
may be Restricted Persons under line 60. Line 76 called this "the most decision-changing
question open" and stage 3 closed it with a word that does not close it.

**F5 — Lines 112-114 put the regulated act on the unpaid party.** The administrator curates
"explicitly to filter out scammers" and "takes no share of the commission". Line 58 records
that ESMA's expectations cover "the qualifications of the traders being copied" — the
selecting is the act. Stage 3's regulatory paragraph (lines 123-127) reasons only about the
operator: "the commission, the product and the relationship with the member are the
decider's". True, and beside the point. The person choosing the traders is the administrator,
for free, and nobody has told them. This is simultaneously the viability risk and the reason
success signal 3 (line 141) will come back negative.

**F6 — Lines 137-142: not one success signal can be run before the money is spent.** All four
begin at install. A discovery whose only tests require the product to exist has not tested
the idea; it has scheduled a post-mortem. Section 5.2 above proposes four tests that all run
without code. If the decider keeps only one thing from this section, keep that.

**F7 — Line 189 (adopted), lines 196-198 (not adopted) and line 203 (adopted) cannot all
hold.** No-go 2 forbids past performance as a sales argument. No-go 3, which would have
forbidden a leaderboard, was declined. Voting is in v1. Members voting on traders will vote
on the only evidence they have, which is performance, posted by the traders themselves in
the channel where no-go 2 cannot be enforced. Stage 4 describes this tension at lines 205-213
and then files it as an open question (line 217). It is not an open question. It is a
contradiction between an adopted no-go and an adopted scope change, and one of them has to
go before a charter can be written.

**F8 — Line 62 is the most decision-relevant row in stage 2 and the worst-sourced.** The
administrator's real alternative — paid signal subscriptions at "$30-300+ per month" — is
marked "Review sites only — *excerpt*, no primary source found". If that row is right, the
administrator earns more from the status quo than flet's entire commission pool and has a
positive reason not to install. Everything downstream of "the administrator will do this for
nothing" depends on a figure nobody sourced.

**F9 — Line 133, keeping all four signals, is not a decision.** Stage 3 says so itself at
lines 144-146 and moves on. The playbook requires each round to end with a decision; an
unranked set of four post-hoc signals, none of which is a stopping condition, is the absence
of one. Line 220 re-asks the question. It should have been answered before stage 4 was
written.

**F10 — Lines 129-131 and line 203: scope grew while feasibility was unknown.** Budget and
time "were not established in this round", and in the same round member voting was pulled
into v1 against the framer's advice. Adding scope before the budget is known is how the
feasibility risk becomes unmeasurable rather than merely unmeasured.

**F11 — Line 57 sizes the competitor with the wrong number.** "reported 50k+ monthly users"
is an *excerpt* from a members-only post. A readable figure exists and it is far more
decision-changing: DefiLlama reports pvp.trade's trailing-30-day revenue at **$14,899**.
Stage 2 measured the competitor's popularity when the question was whether the business
model pays.

**F12 — Lines 117-120 answer the decider's question in the decider's place.** Line 41 asks
"Who holds the members' funds and their keys while the copying runs?" — stage 1's own first
open question. Stage 3 closes it with "*Assumption stated by the framer, not contradicted by
the decider*". The playbook is explicit: when the decider cannot answer, write the question
down and go on — "never answer it in their place". Silence is not confirmation, and per F2
this is the question the product turns on.

### 5.5 Open items — questions the challenger would have asked

Not answerable from here; they are objections until the decider answers them.

1. **Which single country do most members live in?** Nothing can be asked of a lawyer, and
   no legal finding in this document can be applied, until this is one word.
2. **How many members does the server have, and how many of them trade Hyperliquid today?**
   The viability arithmetic is one multiplication and this is its only missing input.
3. **Who holds the agent-wallet key — flet, or the member?** See F2.
4. **What is the budget, and by when?** (Line 129, still open, and now with added scope.)
5. **Has anyone told the administrator that selecting the traders may be a regulated act
   they perform for free, and that promoting flet to their members may be separately
   restricted?** Would they still install it?
6. **Does voting replace the administrator's curation or sit under it?** Seconding line 217 —
   with the addition that under F7 the answer also decides no-go 2.
7. **Which signal, negative, stops the project?** Seconding line 220.

### 5.6 The challenger's verdict on the value hypothesis

Stated plainly, because the playbook forbids blunting it.

**The hypothesis at lines 154-161 cannot survive as written.** Its second sentence — the 10k
USDC vault fee as the reason a trader needs flet — is false as a differentiator (F1), and
the clause should be struck. Its operating premise — that the administrator will do the
curation for nothing (line 114) — is the assumption most likely to fail, and it fails harder
once anyone explains the exposure to them (F5, counter-evidence on promotion). And the
architecture that would deliver it appears to be forbidden by the product's own first no-go
(F2).

**The core claim underneath it can survive, and is worth testing.** That a member copies
because someone they know vouched, rather than because a ranking said so, is a real
hypothesis, it is not obviously wrong, and — unlike everything else in this document — it
can be refuted in fourteen days for the price of one Discord message and no code (5.2,
value). Nothing in the counter-evidence disproves it. What the counter-evidence disproves is
the *business* around it: the venue caps the take at 0.1%, competitors already charge half
that, and the nearest comparable with 50k+ claimed monthly users made $14,899 last month.

**Recommendation — the decider's call, not the challenger's:** not a go. The four tests in
5.2 cost roughly one week of somebody's attention plus one legal bill, and three of the four
can refute the project before a line of code is written. Run the legal scoping (viability B)
and the link test (value) first, and in that order, since the link test performs the act the
legal test sizes.

### Round 2 challenge — 2026-09-21

**Challenger:** independent agent session, dispatched as challenger · 2026-09-21. This
session did not write any of the round-2 material and had no access to the session that did.

> **Scope.** Round 1's challenge above is not revisited. This subsection challenges only what
> round 2 produced: the feasibility shadow run and its correction, the minimum-ticket rule,
> the revenue forecast, the round-2 entries at the end of the document, `docs/pdr/0001-…`, and
> `docs/project/legal-scoping-request.md` version 2.
>
> **Line references resolve against commit `56189f5`**, the revision this session read.
> Inserting this subsection shifts every line of the round-2 entries that follow it; resolve a
> citation against that commit, not against the current file. Nothing above is edited.
>
> **Tools.** `docs/tooling-profile.md` still declares no research tool, so this round used the
> tools at hand, named at each finding: the agent's web search and page fetch, and — for the
> numbers — direct HTTP reads of `stats-data.hyperliquid.xyz`, `api.hyperliquid.xyz` and
> `api.llama.fi` from this sandbox, all read-only, no keys, no orders, no money.
>
> **Marking**, as in section 2: *primary* — read on the source's own site or endpoint;
> *reported* — a figure a party states about itself; *excerpt* — seen only in a search result;
> *primary-negative* — the source is silent where a statement was looked for; *assumption* —
> unsourced; *derived* — arithmetic done here from sourced figures.

#### R2.0 What was re-measured first, and what held

A challenger who only argues is cheap. Round 2's central measurements were re-run here from
the same public endpoints before anything below was written.

| Round 2 claim | Re-measured 2026-09-21 | Verdict |
|---|---|---|
| "13,536 accounts above 5k USDC active over 30 days" (line 172) | 13,524, from a fresh leaderboard snapshot of 46,312 rows (`accountValue > 5000`, 30-day volume > 0) | **holds** |
| "median monthly turnover is **8.4×**" (line 173) | 8.5× | **holds** |
| "**68.6%** … stay under a 5%-a-month fee burden" (line 174) | 68.5%, using 0.1% builder + 0.045% venue taker per turn | **holds** |
| "**7,635** of them also closed the month positive" (line 175) | 7,589 | **holds** |
| The supply table, 210 / 557 / 966 / 1,666 (lines 189-192) | 214 / 559 / 971 / 1,674 | **holds** |
| Maker share of fills: 0% / 54.1% / 60.0% (line 156) | 0% / 50.6% / 67.2%, from 2,000 `userFills` each | **holds** |
| Minimum ticket for 80% of orders (lines 178-184) | 4,534 / 6,308 / 36,019 USDC against the document's 4,896 / 6,013 / 51,367 | **holds for two of three**; the third differs because this session's 2,000 fills span 15 days where the run cut to 3 |
| pvp.trade: $180 / $1,412 / $14,899 / $502,489 / $8,005,840 (5.3) | identical, re-read today. DefiLlama's own `methodology` field reads "builder code revenue from Hyperliquid Perps Trades" — the same rail and the same fee flet would use | **holds**, and is a closer comparable than 5.3 claimed |

*primary* — `stats-data.hyperliquid.xyz/Mainnet/leaderboard`, `api.hyperliquid.xyz/info`
(`userFills`) and `api.llama.fi/summary/fees/pvp.trade`, all read directly from this sandbox
on 2026-09-21.

One correction to round 1's framing while the data is open: pvp.trade's revenue is no longer
collapsing, it has bottomed. The 30 days before the ones 5.3 recorded came to **$14,366**
against $14,899 — flat month on month, at about a third of its trailing-year monthly average
($41,874). *derived*, from the same series.

**So the arithmetic of round 2's correction is sound.** What follows is not a dispute about
whether those sums were done right. It is that the one number the revenue depends on was
taken from the wrong population, and that everything built on top of it inherits the error.

#### R2.1 Pre-mortem — the platform, one year on

It is September 2027. flet shipped as a self-serve bot on any Discord server or Telegram
channel, paid on routed volume. It is being wound down.

1. **It never got past a hundred servers.** The app was never verified by Discord — an
   unverified app cannot join a 101st server — and the model needed hundreds. Nobody had
   checked whether an app that routes leveraged derivatives orders gets verified. *(viability)*
2. **It got the installs and not the copiers.** Three hundred servers installed it in the
   launch month. The median server produced zero active copiers, which is precisely what the
   median builder-code interface on this venue produces in revenue. The long tail of line 776
   was not a risk to the model; it was the model. *(value)*
3. **The commission was real and trivial.** Eleven communities went active. At the turnover
   the trader-selection rule actually yields, the whole year's commission was under €2,000,
   and the rate could not be raised because somebody else sets the cap. *(viability)*
4. **The minimum ticket priced out the members.** The members who wanted to copy had €300.
   The traders their administrators vouched for needed €6,000 behind them. The ones who
   copied anyway received a third of the leader's orders. *(value)*
5. **The copy was flet's strategy, not the trader's.** Half the leader's fills were posted,
   not taken; most of the rest were dust once scaled. flet chose which orders to reproduce,
   at what size, under what leverage cap. The tracking error *was* the product, and the
   traders publicly disowned the results their names were attached to. *(feasibility → value)*
6. **A key store leaked — or was rumoured to have leaked.** flet held one agent key per
   member across every server. No withdrawal was possible and none was needed: maximum
   leverage on thin perps zeroed several hundred accounts inside one block. The leverage
   ceiling was in the same cycle as the incident. *(feasibility / viability)*
7. **The copying stopped by itself and nobody noticed.** Members registered an agent wallet
   with another Hyperliquid tool, which deregistered flet's unnamed one — the document quotes
   exactly this mechanism at line 97 — or an expiry lapsed. The day-60 retention number was a
   bug report read as a signal. *(usability / feasibility)*
8. **An administrator listed themselves and drained their own members.** A server built to
   farm the product; a curated list that was a scam by design. flet took 0.1% of it and
   appeared in the complaint as the party that routed the orders and was paid for them.
   Round 2 named this surface at line 801 and addressed none of it. *(viability)*
9. **The administrators stopped, and the platform had nothing to offer them.** PDR-0001
   forbids paying them. With one friend that was a risk. With four hundred strangers doing the
   only work that differentiates the product, it was the growth model. *(value / viability)*
10. **The written opinion came back favourable on Q1 and reserved on Q4.** Q1 had been asked
    on facts that changed before the answer arrived; Q4 said an open platform must know where
    its members are, and the remedy was geoblocking and identity checks the product had no way
    to perform, at a cost nobody had a budget to compare against. *(viability)*
11. **An administrator's launch post was the offence, not the operator's service.** The
    volunteer had never been told. They removed the bot and told the other admins. *(viability)*
12. **A warning-list entry ended distribution in a day.** Not a fine — a line on a regulator's
    page, and a delisting the same week. *(viability)*
13. **Telegram never shipped.** The main-wallet signature needed a browser hop that the Mini
    App rules made awkward, and half the forecast's communities were Telegram. *(feasibility)*

#### R2.2 The four risks, restated for the platform

Thresholds are **proposed by the challenger**. They are the decider's to set, and the decider
has now been asked to set thresholds twice without doing so (line 746).

| Risk | The riskiest assumption as round 2 leaves it | The cheapest test that could refute it |
|---|---|---|
| **Value** | No longer only "a member copies because a trusted admin vouched". It is now: **enough servers, installed self-serve by strangers, contain enough members holding roughly €5,000 who will route it through a bot belonging to someone they have never heard of.** Line 776-780 calls the install→active ratio "the load-bearing and untested assumption", says "nothing here estimates that ratio", and then estimates nothing. | **The install test. One landing page, no bot, 21 days.** Publish the product where server administrators gather, with an "install" button that instead collects: the server, its member count, and the admin's own estimate of how many members trade perps and with how much. Count admin sign-ups, and count how many describe a server that could actually produce copiers. **Refuted if** administrators do not come, or their servers are too small. *Proposed threshold: fewer than 20 admin sign-ups in 21 days, or fewer than 4 of those describing a server with 10 or more members trading perps at €2,000 or above.* This test also produces the operand the forecast has been missing since round 1. Run it **alongside** the link test of 5.2, which stands as written — and which now needs the second reading 5.3's last row asked for: **record the copiers' P&L next to their retention**, or a bad retention number will be read as a refutation of the wrong hypothesis. |
| **Usability** | That a member of *any* server, with no relationship to the operator, completes a flow requiring a main-wallet `ApproveBuilderFee` signature (*primary*, and flet cannot produce it — round 1's F3 is unresolved), a separate `ApproveAgent` registration, and, on Telegram, either a Mini App inside TON Connect rules or a hop out to a browser. Round 1's threshold was set for members of a community that trusts its administrator; the platform removes the trust and adds a channel. | **The same walkthrough, twice, with strangers, one week, no backend.** Five members of a server the operator has no relationship with, on Discord; five on Telegram. Thirty minutes each, unaided, testnet, screen shared. Record completion, time, and the step they stop at. **Refuted if** they cannot get through it. *Proposed threshold: on either channel, 3 or more of 5 fail to complete unaided in under 10 minutes; or, on Telegram, 2 or more of 5 leave the app to sign and do not come back.* Refuted on Telegram alone halves the forecast's community count. **And before the test, write down what the product does when an agent registration silently lapses** (line 97). If the answer is "the member finds out from their P&L", the usability risk is not onboarding — it is silent failure. |
| **Feasibility** | Two assumptions, neither tested. First, that "replication" is a thing flet can do at all — section 2 establishes that most of a typical leader's fills are not reproducible and most scaled orders are refused, and then the product is still described to a lawyer as replication. Second, that **one agent key per member, across an open set of servers, held by one unauthorised natural person**, is an operable design. | **(A) Tracking error, two weeks, read-only, no keys.** Take the ticket-matched supply of lines 186-192 — copyable, winning traders at most 20× a €2,000 ticket — and simulate the copy flet will actually implement: skip sub-floor orders, take liquidity where the leader posted, apply the leverage ceiling of line 725. Report the copier's monthly return against the leader's, per trader. **Refuted if** the copy does not reproduce the leader. *Proposed threshold: median absolute tracking error above 25% of the leader's monthly return, or more than 1 in 10 simulated copiers finishing a month negative that the leader finished positive.* This is what test 5.2 was for; the slippage proxy measured the wrong thing and section 2 says so at line 154. **(B) Blast radius, one afternoon, on paper.** Write the incident: every agent key flet holds is disclosed at 02:00. Enumerate what the holder can do, how long before every member can revoke, and what flet can do centrally without the member. **Refuted if** no answer bounds the loss. *Proposed threshold: if flet cannot bring every member to zero exposure within 60 minutes without the member acting, the design is not shippable at platform scale.* Still open, and now three sessions old: whether an agent may register another agent, and whether `usdClassTransfer` / `subAccountTransfer` accept an agent signature. The docs remain silent — *primary-negative*, re-confirmed today. |
| **Viability** | That a rate fixed at 0.1% (PDR-0001) pays for a service an unauthorised natural person provides to members in jurisdictions it does not know — in a category whose median participant on this exact rail earns **$1,689 a month** and where both named comparables charge **half** the rate flet intends. | **(A) Economics, half a day, no code — the same multiplication as round 1, with the right multiplicand.** Re-run the forecast on the turnover of the population the document's own selection rule produces (measured below: 5.4× a month for a €1,500 ticket), not on 15×, and at 0.05% as well as 0.1%. **Refuted if** the honest optimistic case cannot pay for the build. *Proposed threshold: if clearing €2,000/month needs more than 20 active communities at the rate the decider intends to charge, that is a kill and not a clarify.* On the restatement below it needs **15** at 0.1% and **30** at 0.05%. **(B) The written opinion — unchanged, and not yet ready to send.** Before it goes: correct the facts (R2-F15), add the third party it promises and omits (R2-F16), state the budget and the deadline the threshold is defined against (R2-F17), and record the lawyer's field (R2-F18). *Threshold unchanged and now completed: any "authorisation required" for the operator **or** for the administrators whose remedy costs more than €X or takes longer than date Y is a kill. The decider writes X and Y before the letter is sent* — otherwise the opinion cannot be read against its own threshold, which is the only reason it is being bought. **(C) The platform gate, one week, free.** Apply for Discord app verification describing what the app actually does, and read Telegram's Mini App rules against the intended onboarding. **Refuted if** the distribution channel will not carry the product. *Proposed threshold: verification refused, or not granted within 30 days, on either channel.* This costs nothing and sits upstream of every number in the forecast. |

#### R2.3 Counter-evidence

Researched this session with the tools named above. An explicit "not found" is recorded as a
result.

| Finding | What it contradicts | Mark / source |
|---|---|---|
| **The long tail is measurable, it is on this exact rail, and it is bleak.** DefiLlama's fee overview for chain "Hyperliquid L1" lists **116 protocols in the `Interface` category** — the builder-code frontends, methodology "builder code revenue from Hyperliquid Perps Trades". Trailing 30 days: category total **$15,050,782**, of which the **top 5 take 79%** and the top 10 take 89%. **Median: $1,689.** 45% earn under $1,000 a month; 34% under $100; **18 (16%) earned exactly $0**. Of those 18, ten had trailing-year revenue above $1,000 — **Dreamcash Markets** ($1,701,446 over the year → $0 last month), **Felix Perps** ($813,636 → $0), **Ventuals** ($255,991 → $0), **HyperSignals** ($203,505 → $0), **VibeLiquid Perps** ($182,324 → $0), **SuperX** ($141,345 → $0), **Ranger Finance Perps**, **HyperSwap Terminal**, **FlowBot Perps**, **Superstack**. Of the 80 protocols with over $10,000 of trailing-year revenue, **48 now run below one twelfth of it**. | Line 776-780: "**The load-bearing and untested assumption is the long tail** … Nothing here estimates that ratio, and it decides everything." A close proxy is one API call away and the call was not made. It also answers round 1's explicit not-found ("the 'failed competitor' evidence the playbook asks for does not exist in readable form"): on this rail, in this category, **the modal outcome of shipping is zero**, and products that earned six figures in a year are at zero this month. Note the honest counterweight: the category *aggregate* is up 31% on its trailing-year monthly average — but that growth sits in wallets (tradeXYZ, MetaMask, Trust Wallet, Phantom), not in copy-trading products. And line 769's base case of 382 € (≈$410) would place an entire active community at roughly the **40th percentile** of this category. | *primary* — `api.llama.fi/overview/fees/Hyperliquid%20L1`, read directly 2026-09-21. DefiLlama is an aggregator, not the companies; a protocol at $0 may have moved off builder codes rather than shut down. |
| **Both named comparables charge 0.05%, not the cap.** pvp.trade's fee is reported at **0.05% on futures**. Copin was already recorded at 0.05% in 5.3. | PDR-0001 fixes the model at "at most 0.1%" and argues it is cheap because Telegram bots charge 1% (PDR lines 61-63). The relevant convention is not Telegram bots; it is the builder-code frontends on this venue, and they charge half. Every revenue figure in the document assumes the cap. | pvp.trade fee — *excerpt*, third-party guides, not pvp.trade's own site. Copin — *excerpt*, as in 5.3. |
| **The nearest comparable routes about $596 of notional per claimed monthly user.** $14,899 at 0.05% implies ≈$29.8M of notional over 30 days; against pvp.trade's claimed 50,000+ monthly users that is ≈$596 per user per month. | The forecast's base case assumes **22,500 € of notional per copier per month** (1,500 € × 15×) — about **38×** the comparable, or about 14× at the restated 5.4× turnover. Copiers are not counter-traders and the comparison is not like for like, but the order of magnitude is a reality check the document never performs. | *derived*, from two *excerpt*-grade figures ($14,899 is *primary*; the 0.05% rate and the 50k user count are not). Directional, not a figure. |
| **Telegram has a specific clause pointing at flet's Telegram onboarding.** Telegram's Bot Developer Terms, section 7: "all **Mini Apps** which implement cryptocurrency functionality … are required to be based exclusively on [TON]"; 7.2 requires Mini Apps with wallet functionality to use "only … TON Connect SDK"; 7.4 prohibits promoting non-TON cryptoassets; 7.3 carves out multichain wallets "provided that such actions are performed directly within the interface of the Mini App". Also, for the operator: "It is your responsibility to ensure that any TPA … operate within all applicable laws", with a full indemnity to Telegram. | Line 792-795: "the Discord Developer Policy question of section 5.3 now has a **Telegram twin that nobody has looked at**." Somebody has now, and there is a named clause. Hyperliquid is not TON and flet's onboarding needs an EVM main-wallet signature; whether 7.3 covers it is unresolved. The counterweight is real: pvp.trade operates on Telegram against Hyperliquid, so this is not an absolute bar — it may simply mean flet must be a bot and not a Mini App, which pushes the signature back into a browser and makes the usability risk worse, not better. | *primary* — `telegram.org/tos/bot-developers`, read via page fetch. The fetch returns quoted fragments with section numbers; the full surrounding text was **not** read. Confirm on the page before relying on 7.3. |
| **An unverified Discord app cannot exceed 100 servers.** "A bot that is currently in under 100 servers cannot join a 101st without getting verified." | The multi-community economics need hundreds of installations — 390 on the document's own 10% activation figure (line 780), about 1,090 on the restatement below. The first ceiling is not demand; it is a platform review flet has not been through, for an app that routes leveraged derivatives orders, and nothing establishes that such an app is verified. This belongs above the revenue table, not in a footnote. | *excerpt* — search results only. Discord's own pages defeated this session as they defeated round 1: `docs.discord.com/developers/tutorials/…/app-verification-and-approval` returned **404**, `support-dev.discord.com` Developer Policy returned **403**. **Must be read on the primary source before any go.** |
| **IOSCO's final report exists, is dated, and is about exactly this intersection.** IOSCO **FR/06/2025**, *Online Imitative Trading Practices: Copy Trading, Mirror Trading and Social Trading*, published **19 May 2025**, alongside a separate final report on finfluencers. It flags a "growing overlap between imitative trading and finfluencer activity", which "can obscure the distinction between regulated advice and general information". | 5.3 carried IOSCO as a bare *excerpt*. The reference and date now verify, and the content points at **the selector**, not the operator — a second international body after ESMA aiming at the person who picks the traders. That strengthens F5 rather than dissolving it, and it lands on an administrator nobody has told. | *reported* — A&O Shearman's FinReg summary, read directly. **IOSCO's own PDF returned 403 to this session and was not read.** |
| **Hyperliquid's terms are still unreadable — a third session, a third failure.** `app.hyperliquid.xyz/terms` fetched today returns 6,845 bytes containing 581 characters of text, all of it a build-tooling comment. No terms. | Round 2 makes the Restricted Persons clause something **flet must enforce** (line 787) and the legal request asks a paid question about it (Q5). The project is buying an opinion on a document that no session has read. | *primary-negative* and an explicit **not verified**. An *excerpt* seen today claims the licence is "for your own, or your internal use only"; unverified, and nothing here relies on it. |

**Explicitly not found:**

- **No public figure for the install→active rate of a self-serve Discord or Telegram bot** —
  not from Discord, not from a bot directory, not from a developer write-up. The category
  distribution above is the nearest proxy and it is a proxy, not the ratio. *Not found.*
- **Nothing, still, on an administrator-curated list restricted to one community.** Third
  independent search across three sessions. The claimed novelty remains unverified.
  *Assumption.*
- **No enforcement action against a copy-trading operator specifically** was found for
  2024-2026, as in round 1. Absence of enforcement is not absence of exposure.

#### R2.4 Flaws in the round-2 material

**R2-F1 — Line 198-199 calls the forecast's turnover a measurement. It is not, and the only
measurement in the document points the other way. This is the flaw that moves the most money.**

The forecast states: "Every input below is an assumption of the framer, not a measurement,
except **the turnover band** and the fee cap, **which are measured above**." The turnover band
— 10× / 15× / 25× — is measured nowhere. The only turnover measured above is the **8.4×**
median of line 173, which sits *below* the entire band.

And 8.4× is the median of **all** active accounts, including the scalpers the same paragraph
excludes as uncopyable. Apply the document's own selection rule from line 174-175 — positive
month, fee burden under 5% — to a fresh snapshot of the same leaderboard, and the median
monthly turnover of the surviving population is **2.06×** (n = 7,589). Apply the
ticket-matching rule of line 186-192 as well, and the medians for the three scenarios' tickets
are **5.10× / 5.40× / 5.60×**.

Restated on the ticket-matched median — every other input left exactly as the framer wrote it:

| Scenario | Ticket | Doc's turnover | Doc's revenue | Measured median turnover | Restated | Overstated |
|---|---|---|---|---|---|---|
| Minimal | 1,000 € | 10× | 30 € | 5.10× | **15 €** | 2.0× |
| Base | 1,500 € | 15× | 378 € | 5.40× | **136 €** | 2.8× |
| High | 2,500 € | 25× | 3,750 € | 5.60× | **840 €** | 4.5× |

Which carries straight into the multi-community table at lines 766-774:

- 2,000 €/month needs about **15** active base-case communities, not 5.
- Matching pvp.trade's last month needs about **109**, not 39.
- At the 10% activation rate the document itself posits (line 780), that is about **1,090
  installations** — above Discord's unverified ceiling by an order of magnitude.

*derived*, from a leaderboard snapshot read 2026-09-21 and the document's own assumptions.

**And the structural point the document never states: revenue and the member's fee burden are
the same variable.** Revenue = ticket × turnover × 0.1%. Burden = turnover × ≈0.145%. Every
euro flet earns costs the member €1.45. The correction at line 175 fixes the member's problem
by selecting *away* from flet's revenue. Lines 174-175 and lines 204-206 optimise the same
number in opposite directions, in the same section, and neither mentions the other. At the
base case's own 15×, flet takes **18% of every member's capital per year**; at the high case's
25×, **30% a year**. Against a copy-trading base rate that 5.3's own last row calls poor, that
is the number the value test has to beat.

**R2-F2 — The two forecast tables disagree, and the "5 communities" claim is arithmetically
false.**

Line 205 gives the base case as **378 €**. Line 769's table gives one community at **382 €**
and five at 1,912 € — that is 5 × 382.5. The difference is that the first table rounds the
copier count up to 17 and computes the revenue on 16.8. Pick one.

Line 773: "To reach 2,000 €/month: **5 communities in the base case**." 5 × 382.5 = 1,912.50.
It is six, on the document's own figures.

Line 774: "the **$14,899** that pvp.trade earned last month: 39 base-case communities."
39 × 382.5 = 14,917.5 **euros** compared against a **dollar** figure, with no rate stated
anywhere. The builder fee is credited in USDC and every ticket in the model is in euros; the
document silently treats them as the same unit throughout, including in the supply table at
lines 189-192, which pairs "500 €" tickets with "5k–10k" USDC accounts.

**R2-F3 — The 285%/month headline is a three-day window multiplied by ten, and the same
endpoint serves the number that would have caught it.**

Line 159: "Copying trader `0x102d…` costs a member **28.5% of their account in 3 days — 285% a
month**", and "That trader turns their account over **72 times a day**."

Resolved on today's leaderboard, that account is
`0x102d1d1a6240581a809bac9b9b4dff2eafe8c058`: account value 272,805 USDC, 30-day volume
196,252,428 USDC — **719× a month, or 24× a day**, with the most recent 24 hours at 8.9×. Same
fee arithmetic on the trader's own 30-day figure gives roughly **104% a month**, not 285%.

The finding survives — this trader is uncopyable by a wide margin — but the number does not,
and the number is what carried the section. The `windowPerformances` field on the very
endpoint the run used returns the 30-day figure next to the account value; the run took a
three-day slice of the same trader and multiplied by ten without looking at it. *primary*,
re-measured today.

**R2-F4 — The shadow run says it can be repeated and then withholds what repeating it needs.**

Line 126: "**Method, so it can be repeated.**" The three addresses are truncated to eight hex
characters (lines 148-152). This session resolved all three against today's leaderboard, but
that is luck: an account that drops off the leaderboard is unrecoverable from eight
characters. Record the full addresses and the snapshot timestamp, or the section's central
measurements are unauditable by anyone including its author.

**R2-F5 — "Not one is below 10" is false, and the run measures fills where it reasons about
orders.**

Line 158: "confirmed empirically: **the smallest of 2,912 observed fills is 10.10 USDC, and
not one is below 10**." In 2,000 fills of `0x7c36139b…` read today there is one of **4.23
USDC** (NEAR, "Open Long", crossed). One in six thousand — so the floor is real and the
conclusion stands. But the floor is on the **order**, not the fill: Hyperliquid's own error
text carries an exception for reduce-only closes, and partial fills of a compliant order
produce sub-floor fills. The observed fill distribution is therefore smaller than the order
distribution it is used as a proxy for, which biases the minimum-ticket figures of lines
178-184 **upward** by an unmeasured amount. The "roughly one twentieth of the trader's
account" rule of line 182 is directional, not a measurement, and the document presents it as
"the product's real constraint". *primary*, re-measured today.

**R2-F6 — The supply table applies a median as if it were a guarantee.**

Lines 186-192 count "copyable **and** winning traders whose account is **at most 20×** the
member's ticket". Line 182-183 says that 20× is the median of a ratio "ranging from 8 to 80",
on a sample of **14**. By construction, roughly half the traders counted inside the band still
need a bigger ticket than the member has. The counts reproduce (214 / 559 / 971 / 1,674 today
against 210 / 557 / 966 / 1,666); what they count does not mean what the heading says.
"Supply exists at every size" is, at best, half of it, from a rule fitted on fourteen points
with a tenfold spread.

**R2-F7 — The screen is survivorship-filtered, and "7,635 closed the month positive" is largely
the filter.**

Line 174-175. On today's snapshot, **75.2%** of the screened population closed the month
positive — an implausible base rate for leveraged perps, and a sign that the filter is doing
the work. Among the active accounts the screen discards, those at or below 5,000 USDC,
**62.2%** closed the month negative, against 24.1% of those kept. The 5k threshold is applied
to the account value *after* the month, so losing accounts fall out of the sample. This does
not overturn the correction; it means the positive-supply figure cannot be read as a base rate,
and the administrator picks for *next* month, which one snapshot cannot measure. Two snapshots
thirty days apart can, and would cost an hour.

**R2-F8 — "The economics become plausible for the first time" (line 766) is the strongest
claim in round 2 and the least supported.**

It multiplies a per-community figure that is 2.8× too high (R2-F1) by a count of active
communities that the same entry says nothing estimates (lines 776-780), and nets off no cost
of serving them. Multiplying an untested number by an unknown number does not make economics
plausible; it makes them unfalsifiable. The honest sentence is the one three paragraphs later
— "it decides everything" — and it should lead, not follow.

**R2-F9 — Line 808 understates what the platform changes.**

"**What this does not change:** the minimum member ticket and the trader-selection rule …
apply per member and per trader regardless of how many communities exist." True, and that is
the problem. The trader-selection rule is technical, measured in this document, and must now
be applied either by hundreds of volunteer administrators who have never seen it, or by flet.
If flet applies it, the legal request's central factual claim becomes false — see R2-F15.

**R2-F10 — PDR-0001's success criterion is not the conservative half of the base case. It is
2.2× harder per member.**

PDR lines 144-150: "at least **20 members**, across at least 5 communities … and the
commission collected over that month exceeds **1,000 €**", justified as "deliberately below
the forecast: `discovery.md` puts five base-case communities at about 1,900 € a month, so
1,000 € is the conservative half".

Five base-case communities is **85 copiers**, not 20. The criterion halves the money and cuts
the members by 76%, which means **50 € of commission per member per month** against the base
case's **22.5 €** — 2.2× the revenue per member of the scenario it calls itself a discount of.
In notional that is 50,000 € routed per member per month: at the base case's own 15× turnover,
a **3,333 €** ticket each; at the ticket-matched median measured here, **9,259 €**; at the
selected-population median, **24,272 €**. A criterion that quietly requires every one of
twenty members to sit at or above the top of the measured ticket range is not conservative.
(Minor, same criterion: "1,000 €" against a fee the venue credits in USDC.)

**R2-F11 — PDR-0001's removal condition cites the wrong question.**

PDR lines 169-170: "it is **question 7** of `docs/project/legal-scoping-request.md`". Q7 is
*Les aménagements*. The remuneration question is **Q8** (legal request lines 130-135), as
line 831 of the discovery itself says: "a removal condition that points at **question 8**".
The live removal condition of an Accepted PDR points at the wrong paragraph of the document it
depends on.

**R2-F12 — PDR-0001 treats two distinct venue approvals as one, and one of the two cases is a
safety case.**

PDR line 107: "**The member revokes the approval** — copying stops; no charge survives the
revocation." The venue has two separate approvals, both recorded in this document:
`ApproveAgent`, which lets flet trade, and `ApproveBuilderFee`, which lets flet be paid
(*primary*, builder-codes docs; the latter signed by the main wallet, section 2 line 56).

- Revoke the builder fee and leave the agent: **flet keeps trading a member's leveraged
  account, for nothing, and no rule anywhere says it must stop.**
- Revoke the agent and leave the builder approval: it keeps occupying one of the member's
  ten (*primary*, builder-codes docs).

Neither is in the edge-case list. Nor is the case the venue's own design makes inevitable: the
member signs a **maximum** builder fee, so a member whose signed maximum is below the
configured rate is a state the product will meet, and PDR line 115 — "One rate, the same for
every member and every community" — is not enforceable against a per-user signed maximum.

**R2-F13 — Acceptance criterion 3 has no oracle, and the criteria omit the constraint the
discovery measured.**

PDR lines 131-132: "Given a member who lost money over a month, **when they ask what they owe
flet**, then the answer is nothing". "When they ask" is not an observable event; there is
nothing to assert against. The kernel's Law 2 requires the criterion to be executable before
any code. Rewrite it as a system assertion — no balance record exists, no invoice object can
be constructed — or drop it.

And nothing in the criteria addresses the **minimum member ticket**, which section 2 calls the
product's real constraint, nor what a member is shown or charged when their scaled order is
refused under the 10 USDC floor. PDR line 110 has an edge case for the ten-approval limit and
none for the one the discovery actually measured.

**R2-F14 — PDR-0001 makes the unpaid administrator structural, and never considers the obvious
alternative.**

PDR line 31, Out of scope: "**Any charge to the administrator**, and any listing fee paid by a
trader to appear on a list." Fine as far as it goes — but the options table at PDR lines 74-81
contains **no option for sharing the commission with the administrator**, which is the single
lever that answers pre-mortem item 4, and which the idea file asks for in as many words:
"permettant à une communauté de proposer du copy trading à ses membres et de **monétiser
l'activité générée**" (`inputs/idea.md`). With one friendly volunteer, unpaid curation is a
risk. With an open set of strangers "que nous ne choisissons pas et ne contrôlons pas", unpaid
curation *is* the growth model, and it contains no incentive. The PDR forecloses the fix on the
same day the platform pivot created the need for it, under a heading that carries no argument.

The Prior Art Gate (kernel §6) is also incompletely applied: the table at PDR lines 40-45 has
no row for the direct price comparables on the same rail — Copin at 0.05%, already recorded in
5.3, and pvp.trade at 0.05%. The PDR's stated reason for 0.1% is that it is "a tenth of the
flat-fee convention" of Telegram bots at 1% (lines 61-63), and it skips the competitors
charging half.

**R2-F15 — The legal request describes a product the discovery has already established cannot
be built. This is the most expensive flaw here, because it is what the money buys.**

Legal request line 74: the operator "**Ne choisit aucun trader.**" Q1, lines 94-97: "alors que
nous ne sélectionnons aucun trader". Lines 39-41: "Les ordres de ce trader sont ensuite
**répliqués automatiquement** sur le compte du membre".

Section 2 of this document establishes that replication in that sense is not available:

- 50–67% of a typical leader's fills are **posted**, not taken, and a copier reacting after
  the fact cannot reproduce them (line 156);
- most scaled orders fall under the venue's floor and are refused (line 158);
- the run's own limits paragraph says the ways around it — fixed-size copying, threshold
  replication — mean "**no longer running the leader's strategy**" (lines 232-234);
- and the decider has put "**position sizing, a leverage ceiling and a kill switch**" into the
  first cycle (line 725).

So the product that ships will decide **which of the leader's orders to reproduce, at what
size, and under what leverage cap**. That is discretion exercised by the operator over a
member's leveraged account, and it is precisely the fact Q1 asks the lawyer to rule on — and
precisely the fact that, per the Skadden source in 5.3, moves a service into portfolio
management. A favourable answer to Q1 on these facts would be favourable on facts the document
has already ruled out. Fix the facts before the letter is sent; it costs nothing and it is the
difference between an opinion and a receipt.

**R2-F16 — The request promises three qualifications and asks eight questions about two.**

Legal request line 71: "Trois, et nous avons besoin d'une réponse distincte pour **chacune**",
listing the copied traders as party 3 at lines 77-78. **No question asks about party 3.** A
trader whose orders are replicated for strangers, on a list they consented to be on, generating
a fee for a third party, is a plausible unauthorised provider — and if they are, flet and the
administrators are distributing them. The letter names the party and then does not ask.

**R2-F17 — The request never states the budget or the deadline, and the kill threshold is
defined against exactly those two numbers.**

The threshold in 5.2 (viability B) is: any "authorisation required" that **cannot be structured
around inside the decider's own budget and deadline** is a kill. Q7 (legal request lines
125-128) asks the lawyer for "un ordre de grandeur de coût et de délai". Line 745 records that
the budget and the deadline are **still open** — for the third round running. The project is
buying the one number the decision turns on and has not decided what number is too large. Two
values, written down, before the letter goes out.

**R2-F18 — Nothing records that the lawyer is qualified for the question.**

5.2 (viability B) asks for "a lawyer qualified in the one named member state". Line 837 records
a verbal impression from "the lawyer"; nothing anywhere records their field. A MiFID II
investment-services question on leveraged derivatives is not a generalist's and not a
crypto-tax practitioner's. Ask, and record the answer, before the bill.

**R2-F19 — The legal signal is recorded correctly and then acted on two lines later.**

Lines 837-846 state, carefully and correctly, that a verbal impression does not clear the
threshold and is an assumption rather than a finding. Lines 851-852 then conclude: "**The link
test (5.2, value) is no longer blocked.**"

The ordering constraint round 1 set is genuinely satisfied — the legal work had to start before
or alongside the value test, and it has started. The objection is to the placement: the release
of the test that performs the regulated act sits in the same entry as, and immediately after,
a favourable impression that the same entry says decides nothing. If the following sentence is
true, write it down: **the link test is released because the legal work has started, and it
would be released identically had the impression been unfavourable.** If it is not true, the
test is still blocked, and the entry should say so.

#### R2.5 Open items — questions the challenger would have asked

Not answerable from here. They are objections until the decider answers them.

1. **What is the budget, and by when?** Asked at line 129, carried into round 2 at line 745,
   still open. Two numbers. Until they exist, the opinion the project is paying for cannot be
   read against its own kill threshold (R2-F17).
2. **How many members does the first server have, and how many trade perps, at what size?**
   Round 1's open item 2, still the only missing operand of the entire forecast.
3. **What install→active ratio does the decider believe, and what ratio would stop the
   project?** Line 780 names it load-bearing and leaves it blank.
4. **At what rate does flet intend to charge — 0.1%, or 0.05% like both comparables?**
   PDR-0001 fixes the cap, not the rate, and every revenue figure in the document assumes the
   cap.
5. **Is the administrator paid, at platform scale?** If the answer stays no (PDR line 31),
   what stops four hundred volunteers from stopping (R2-F14)?
6. **What is the lawyer's field, and has the letter been sent — with which version of the
   facts?** (R2-F15, R2-F18.)
7. **Which signal, coming back negative, stops the project?** Third time of asking: line 220,
   round 1's F9, line 746.
8. **Who is liable, and as what legal person?** The operator is an unauthorised natural person.
   The platform pivot multiplies the counterparties, and the legal request excludes "montage de
   structure" from its scope. That exclusion was reasonable for one community and is not for an
   open platform.

#### R2.6 The challenger's verdict

**Round 2 did real work, and two of its three pieces hold up.** The structural argument that an
agent key cannot withdraw is the strongest research in the document. The whole-leaderboard
correction of the shadow run was the right instinct, honestly flagged, and it reproduces to
within 0.1% on an independent snapshot. The framing correction to a multi-community platform
is almost certainly right about what the product is, and it was recorded rather than
retrofitted.

**But round 2 has made the project less likely to work, not more, and the document now says
the opposite.** Line 766 — "the economics become plausible for the first time" — is the only
optimistic sentence in eight hundred lines, and it is the one that does not survive
measurement. Correct the turnover to the population the document's own selection rule produces
and the base case falls from 382 € to 136 €; the five communities needed for 2,000 € become
fifteen; the thirty-nine needed to match a competitor become a hundred and nine; and the
installations needed to get there exceed the ceiling Discord puts on an unverified app. The
pivot did not improve the economics. It replaced one known-small number with a large number of
unknown ones, and the unknown that decides everything — how many installed servers ever produce
a copier — has a measurable proxy on this exact rail whose median is $1,689 a month and whose
modal value is zero.

**Meanwhile the one thing that could still refute the project cheaply has been put behind two
avoidable errors.** The legal request describes replication by an operator who selects nothing;
the discovery has established that the product must select, size and cap. And the threshold the
opinion is to be read against depends on a budget and a deadline that have now gone unanswered
for three rounds.

**Recommendation — the decider's call, not the challenger's:** still not a go, and not a third
clarify on the same questions. Do four things, none of which needs code or costs more than the
legal bill already committed:

1. **Write the budget and the deadline.** One line. Everything downstream is blocked on it.
2. **Fix the legal request before it is sent** — the facts (R2-F15), the third party (R2-F16),
   the two numbers (R2-F17), the lawyer's field (R2-F18).
3. **Apply for Discord verification** and read Telegram's Mini App rules. Free, one week,
   upstream of every revenue figure.
4. **Run the install test and the link test together**, with the P&L recorded next to the
   retention.

If the install test comes back empty, the platform pivot is the answer to a question nobody
asked, and the honest outcome is the one the playbook calls cheapest.

## 6. Decision

### Round 1 — **clarify**, 2026-09-20, by @napkinstack-admin

The challenge was presented unchanged and the decider chose **clarify**: no charter, no
module, no code until the round-2 questions are answered and the cheap tests have run.

**The reasons.**

- **F2 is the question the product turns on, and it was answerable for free.** Rather than
  decide around it, the decider asked for it to be settled on the venue's own documentation
  first. That research is in section 2, "Round 2", and it changes the shape of the question:
  the non-custodial architecture exists, so what remains is a reading of no-go 1, not an
  architectural impossibility.
- **The four tests in 5.2 cost about a week and one legal bill, and three of them can refute
  the project before a line of code exists.** Against that, a go would have spent a build to
  learn the same thing later. The playbook calls the cheap outcome the cheapest for a reason.
- **Two inputs that everything else waits on are still missing**: one named country, without
  which no legal question can even be asked, and the member count, without which the
  viability arithmetic has no operand.
- **The decider did not accept the challenger's premise that the idea is dead.** The core
  claim — a member copies because someone they know vouched — was not refuted by anything in
  section 5.3, and the link test can settle it in fourteen days.

**What round 2 carries.**

1. The testnet check on agent-wallet permissions (section 2, round 2) — one hour, converts
   the load-bearing claim to primary.
2. The reading of no-go 1: "no custody of funds", or "no key of any kind". The answer decides
   whether there is an automated product at all.
3. One named member state; the server's member count and how many trade Hyperliquid today;
   the budget and the deadline.
4. The legal scoping opinion (5.2, viability B), started **before** the link test, since the
   link test performs the act the opinion must qualify.
5. The link test (5.2, value), and the thresholds the decider sets on all four tests.

Still open and unanswered from round 1: whether voting replaces or sits under the
administrator's curation (F7 makes this also decide no-go 2), and which signal, coming back
negative, stops the project.

---

### Round 2 — the decider's answers, 2026-09-20

**1. Version B: automated copying, accepted.** flet holds **one agent key per member** — a
second key, registered by the member's own main wallet, able to place and cancel orders on
that member's account and nothing else, revocable by the member at any time and able to
carry an expiry. The **traders' side needs no key at all**: their positions are public
on-chain, and flet reads their address.

- **No-go 1 is reworded by the decider** to *never hold a member's funds or a member's main
  key*. The round-1 wording ("funds or private keys", section 4) stands above as adopted and
  is superseded here, not deleted.
- **The testnet check was made blocking by the decider, and the evidence has since moved.**
  The empirical run is blocked: the faucet requires a prior mainnet deposit from the same
  address (*primary*), so a throwaway address cannot be funded without spending real money.
  In its place, the payload analysis in section 2 establishes structurally, from primary
  documentation, that a withdrawal or transfer signed by an agent key debits that agent's own
  address — the action format has no field for acting on behalf of the account that
  authorised it. **Whether that satisfies the blocking condition is the decider's to say.**
  Two narrower questions remain open there: whether an agent may register another agent, and
  whether the two internal-transfer actions accept an agent signature.
- **What this does not change:** an agent key cannot *take* a member's money but can *lose*
  it. Pre-mortem item 10 stands, and it is now a design constraint rather than a worry:
  position sizing, a leverage ceiling and a kill switch belong to the first cycle, not later.

**2. France is the launch country.** The legal scoping (5.2, viability B) is on French law
and must cover **both parties** — the operator and the administrator who curates — plus the
separate question of whether the administrator's announcement post is restricted promotion of
an unregistered service. The decider foresees extending abroad; that is **re-asked country by
country**, since nothing found for France transposes automatically. F4 is closed for round 2
only.

**3. Voting sits under the administrator, who keeps a veto.** Members propose and vote; the
administrator validates or refuses. The vouching stays theirs, so the value hypothesis
survives, and F7's contradiction is resolved in favour of no-go 2 — **on paper only**:
members will still argue from displayed performance in the channel, where no-go 2 cannot be
enforced. Recorded as a residual, not as closed. Unchanged either way: the administrator
still performs the act ESMA's briefing points at, and still takes no share of the commission
(F5).

**Still open after this pass:** the server's member count and how many of them trade
Hyperliquid today; the budget and the deadline; the thresholds on all four tests; and which
signal, coming back negative, stops the project.

---

### Round 2 — the decider corrects the framing, 2026-09-21

**flet is a multi-community, multi-channel product, and was meant to be from the start.**
The bot is installable on **any** Discord server or Telegram channel, and administered by
the admin of that server or channel. Karim's server was an example, never the product.

*How the framing narrowed.* The idea file says "permettant à **une** communauté de proposer
du copy trading à ses membres" — which reads as *any* community, generically. The framer's
stage-1 restatement turned it into *the* community's existing channel, the decider confirmed
that restatement, and every stage-3 question after it asked about *the* administrator and
*the* members' country. The narrowing is the framer's, and it propagated into the legal
work. It is corrected here rather than rewritten above.

**What it changes.**

**1. The economics become plausible for the first time.** Per-community figures from the
forecast above, multiplied by the number of **active** communities:

| Active communities | Minimal | Base | High |
|---|---|---|---|
| 1 | 30 € | 382 € | 3,750 € |
| 5 | 150 € | 1,912 € | 18,750 € |
| 20 | 600 € | 7,650 € | 75,000 € |
| 50 | 1,500 € | 19,125 € | 187,500 € |

To reach 2,000 €/month: 5 communities in the base case, 67 in the minimal one. To reach the
$14,899 that pvp.trade earned last month: 39 base-case communities.

**The load-bearing and untested assumption is the long tail.** Those tables count *active*
communities, not installations. The normal shape of a self-serve product is that most
servers install it and never produce a single active copier. Nothing here estimates that
ratio, and it decides everything: at a 10% activation rate, 39 active communities means 390
installations.

**2. The legal question changes shape, and `legal-scoping-request.md` as written on
2026-09-20 is wrong.** It asks whether *the operator* may serve *one French community*. The
real question is whether an unauthorised operator may run an **open platform** that any
administrator installs, serving members in **uncontrolled jurisdictions**, on perpetual
futures. Three things follow that the first version never raised: the members' countries are
no longer knowable in advance; Hyperliquid's Restricted Persons clause becomes something
**flet must enforce** rather than something it can assume about one server; and the admins
are no longer one identified volunteer but an open set the operator neither selects nor
controls. The request is rewritten in the same commit as this entry.

**3. Telegram re-enters the scope.** Stage 3 fixed on Discord because that is where the
example community lives. The product needs both channels: two integrations, two platform
policy regimes, and the Discord Developer Policy question of section 5.3 now has a Telegram
twin that nobody has looked at.

**4. Flaw F5 multiplies.** Not one unpaid curator performing the act ESMA's briefing points
at, but one per community — an open set the operator does not choose. And flet becomes
responsible, in fact if not in law, for what those administrators list.

**5. A surface the discovery has never addressed: self-serve installation.** An
administrator who lists themselves as a copyable trader; a server created to farm the
product; a curated list that is a scam by design. Karim's trustworthiness was an assumption
the whole product rested on, and it does not generalise to strangers.

**6. The comparable stops being approximate.** pvp.trade is precisely a multi-group Telegram
product on the same venue with the same fee rail. Its measured $14,899 over 30 days is now
the direct read of what this category currently pays, not a distant analogy.

**What this does not change:** the minimum member ticket and the trader-selection rule
(section 2), both of which apply per member and per trader regardless of how many
communities exist.

### Round 2 — the revenue model is settled, 2026-09-21

**No profit share.** The decider rules it out. flet is paid a flat commission on the notional
it routes, capped by the venue at 0.1%, and never takes a share of a member's gains.

This closes the third question the feasibility run put to the decider, and it closes more
than a pricing choice: the only native way to take a profit share on this venue is the
**vault** rail, which pools members' capital. Ruling out the profit share therefore also
rules out vaults and settles the architecture — the member keeps their funds, flet holds a
revocable agent key, and the venue pays flet on routed volume. Every mention of the vault
rail in sections 2 and 5 is now background, not an option.

Recorded as **PDR-0001**, with its prior art, the trade-off owned — a member who loses still
pays — its acceptance criteria, a success criterion dated 2027-03-21 and a removal condition
that points at question 8 of the legal scoping request.

**Consequence the decider should hold in view:** the revenue model is now fixed *and* capped
by somebody else. flet cannot raise its take; it can only lower it. Everything therefore
rests on the number of **active** communities, which is the untested long-tail assumption
recorded above.

### Round 2 — first legal signal, 2026-09-21

**The decider reports that the lawyer "seems favourable".** Recorded for what it is, and no
more: a **preliminary verbal impression relayed by the decider**, not the written opinion
that test 5.2 (viability B) asks for, and not attributed to any of the eight questions. No
document was received. *Assumption, not finding.*

**What it does not do.** The threshold the challenger set, and the decider did not replace,
is explicit: *any "authorisation required" for either party, that cannot be structured around
inside the budget, is a kill and not a clarify*. A favourable impression does not clear that
threshold, because the threshold is about **which** party and **which** question. Favourable
on Q1 — the operator, who selects no trader — while reserved on Q4 — the territoriality of an
open platform whose members' countries are unknown — describes a different product from the
reverse.

**What it does do.** The challenger's ordering constraint is satisfied: the legal work had to
start **before or alongside** the value test, never after. It has started. **The link test
(5.2, value) is no longer blocked** and is the cheapest remaining test of the one claim
nothing has yet refuted.

**Still owed before this section can be marked as an answer:** the written opinion, and the
lawyer's position question by question — at minimum Q1 (the operator), Q2 (the administrators,
and our responsibility for them), and Q4 (territoriality).

### Round 2 — **clarify**, 2026-09-21, by @napkinstack-admin

**A second `clarify`, chosen explicitly.** The playbook requires this to be recorded as the
decider's deliberate choice and never as a default, and it is: the decider was presented with
kill, go and clarify, and with the challenger's own recommendation of neither go nor a third
round on the same questions.

**The reasons.**

- **Round 3 does not replay round 2's questions.** It carries what the round-2 challenge
  showed to be missing or wrong, not what round 1 left open.
- **The legal request was describing a product that cannot be built**, and it had already been
  sent. That is the objection that could not wait: a favourable opinion given on those facts
  would have been worthless, and worse, reassuring. Corrected the same day as **version 3**.
- **The framer's forecast was wrong in the direction of optimism**, and the decider chose to
  keep going with the corrected numbers rather than with the ones that flattered the project.
- **The core claim is still standing.** After two rounds and two independent challenges,
  nothing has refuted the belief that a member copies because someone they know vouched. It is
  also still untested, which is the anomaly round 3 exists to end.

**What round 3 carries.**

1. **The budget and the deadline, written down.** Open since round 1, open through two
   challenges, and the kill threshold is defined against them. Nothing else in round 3 can be
   weighed without them.
2. **The legal request, version 3, re-sent.** It now states the discretion: which orders are
   reproduced, at what size, under what risk limits. Question 1 asks whether that discretion
   alone moves the service into portfolio management.
3. **Discord verification.** Free, about a week, and upstream of every number in the forecast
   — an unverified application is reported to be capped at 100 servers, which the round-2
   challenge marks *excerpt* and which must be confirmed on the primary source.
4. **The link test, with P&L recorded beside retention** — so that a bad retention number can
   be told apart from a bad market.
5. **The install→active ratio**, explicitly *not found* by the challenger. Without it the
   multi-community forecast has no operand.

**Corrected in this round, not deferred:** the forecast's turnover band, which the framer had
labelled measured when it was assumed. On the document's own selection rule the median is
2.06×, and 5.10× once matched to the member's ticket — against the 15× assumed. The base case
falls from 382 € to between 53 € and 130 € a month, and 2,000 €/month needs 15 to 38 active
communities rather than 5.

**Not accepted as settled:** the first legal signal. It stays recorded as a verbal impression,
and it was given on the facts of version 2.

### Round 3 — the budget, the deadline and the stopping condition, 2026-09-21

**The decider, verbatim:** *"J'ai 8 000 € et trois mois à mi-temps. Si au 31 décembre il n'y a
pas 20 membres qui copient encore après 30 jours, j'arrête."*

Budget **8,000 €**, three months half-time, deadline **2026-12-31** — 101 days from today.
Kill condition: **fewer than 20 members still copying at day 30, by 31 December.**

This closes the input that stayed open through round 1, round 2 and both challenges.

> **One caveat the framer must record.** These figures reproduce, word for word, the
> *illustrative example* the framer wrote when asking the question. They may well be the
> decider's real numbers — but the framer invented them first, and this document has already
> been burned once by a framer's assumption travelling as a measurement (the turnover band).
> **Flagged for the decider's confirmation**; every threshold below inherits it.

**What the threshold is worth, tested against the measured economics.** Twenty members
copying, at the turnovers measured in section 2:

| Average member ticket | at 2.06× (copyable median) | at 5.10× (matched to ticket) |
|---|---|---|
| 1,000 € | 41 €/month | 102 €/month |
| 1,500 € | 62 €/month | 153 €/month |
| 3,000 € | 124 €/month | 306 €/month |
| 6,583 € *(the measured median minimum ticket)* | 271 €/month | 671 €/month |

**The decider's success condition, met exactly, repays the 8,000 € in 12 to 52 months.** It
is a threshold that can be *achieved* and still leave the project not working. A stopping
rule should separate the world where you continue from the world where you stop; this one, at
its most favourable reading, describes a world where you have spent three months and 8,000 €
to build something that earns 671 € a month — and it says continue.

**And it makes PDR-0001's success criterion unreachable as written.** That criterion asks for
20 members and more than 1,000 €/month. At the measured turnover of 5.10× that needs an
average ticket of **9,804 € per member**; at 2.06×, **24,272 €**. The PDR calls itself "the
conservative half" of a forecast that has since been corrected downward by a factor of three.
**PDR-0001 must be superseded or its criterion restated** — an open item of round 3, not a
detail.

**What the framer puts to the decider, without deciding it:** a stopping rule made of members
alone cannot fail in the way that matters. Pairing it with a revenue figure — *"…and at least
X € collected in the month"* — is what would make 31 December a real date rather than a
counting exercise.
