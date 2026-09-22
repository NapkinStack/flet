# screening

Tells an administrator whether a trader is copyable by their members, and at what cost — arithmetic they cannot do by eye.

- **Owner**: NapkinStack/maintainers
- **Criticality**: high
- **Manifest**: [MANIFEST.yaml](./MANIFEST.yaml)

## Getting started

```bash
nstack bootstrap screening    # from a fresh clone, when declared
nstack check screening        # format, lint, types - under 2 min
nstack test screening         # never starts another module
nstack run screening          # locally, with doubles for the dependencies
```

Commands: the `commands` section of the MANIFEST, to declare for this module's stack.

## What the command answers

```
screening <address> --ticket <amount>
```

One of four verdicts on the first line, then every figure it rests on. A verdict without its
measurement is not an answer here.

| Verdict | Exit | Means |
|---|---|---|
| `COPYABLE` | **0** | At least **80%** of the trader's orders clear the venue's 10 USDC floor at this ticket, and nothing else is worth reserving about. The share that would still be refused is printed. |
| `COPYABLE WITH RESERVATIONS (…)` | **1** | Clears the floor, and at least one reservation applies. The reservations are **named in the headline**, so the first line alone is actionable. |
| `NOT COPYABLE (…)` | **2** | More than 20% of the orders fall under the floor. The member cannot place this trader's orders at this ticket, whatever else is true — impossible beats expensive. Any reservations are still printed below. |
| *(nothing on stdout)* | **3** | **No verdict.** The venue could not be read or answered with something that is not a number, the command line was malformed, or the data cannot support an answer. |

`--help` prints the usage and exits **0**, as a command should. It is the one exit 0 that is not a verdict.

**The codes run by severity**, so a script keeping the idiom it already has — `if code == 0` —
stops getting a zero for a trader the command was warning it about.

**No verdict outranks every verdict, including `NOT COPYABLE`.** If the window the venue
returned is stretched to a month by more than **30×**, the command refuses before forming any
verdict at all — because at that point the floor share and the minimum ticket are inferences
from half an hour, and printing them as facts about a trader is the thing this module exists
to not do.

### The four reservations

| Named | Applies when |
|---|---|
| `fees` | The monthly fee burden is **above 5%** of the member's ticket. The fees, not the strategy, will decide their result. |
| `reproducibility` | **More than half** the trader's fills were posted rather than taken. A copier arriving afterwards cannot reproduce them. |
| `concentration` | The volume landed on **a third or fewer** of the days read. A month's volume in one burst is not a month of trading. |
| `extrapolation` | The venue could not return the whole window, and the monthly figures are stretched by **more than 3×**. |

Thresholds are one set of numbers for every administrator and every community. An
administrator cannot tune them and a trader cannot be exempted
([PDR-0002](../../docs/pdr/0002-three-verdicts-not-two.md)).

## Contracts

- Provided: see `provides` in the MANIFEST
- Consumed: see `consumes` in the MANIFEST

## Decisions

See `docs/adr/`.
