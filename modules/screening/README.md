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

## Contracts

- Provided: see `provides` in the MANIFEST
- Consumed: see `consumes` in the MANIFEST

## Decisions

See `docs/adr/`.
