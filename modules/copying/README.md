# copying

Lets a member hand flet a key that can place orders and nothing else on the venue, and take it
back — the venue, not flet, saying whether the key is alive.

- **Owner**: NapkinStack/maintainers
- **Criticality**: critical
- **Manifest**: [MANIFEST.yaml](./MANIFEST.yaml)

## Getting started

```bash
nstack bootstrap copying    # from a fresh clone, when declared
nstack check copying        # format, lint, types - under 2 min
nstack test copying         # never starts another module
nstack run copying          # locally, with doubles for the dependencies
```

Commands: the `commands` section of the MANIFEST.

```bash
uv run copying authorise <member main address> [--testnet]   # a fresh agent, to approve on the venue
uv run copying status    <member main address> [--testnet]   # alive, per the venue — or no answer
uv run copying forget    <member main address>               # flet drops its copy; not a revocation
```

## Contracts

- Provided: see `provides` in the MANIFEST
- Consumed: see `consumes` in the MANIFEST

## Decisions

See `docs/adr/`.
