---
decision: clarify           # proposed | go | clarify | kill — the decider decides
decider: "@napkinstack-admin"  # the human who decides, recorded at intake
decided_on: 2026-09-20      # YYYY-MM-DD, with the decision
challenger: "agent session (challenger), 2026-09-20"  # stage 5
idea: "docs/project/inputs/idea.md"         # the idea as given, kept in docs/project/inputs/
round: 2
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
