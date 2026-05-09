# V0 Protocol

## Objective

Create an executable foundation for a mechanism-first enzyme atlas.

## Research Questions

1. Can public enzyme knowledge sources be represented as a provenance-aware
   source registry?
2. Can common catalytic mechanisms be represented in a structured fingerprint
   language?
3. Can validation tooling detect incomplete or weak records before downstream
   modeling begins?

## Inputs

V0 uses hand-curated seed registries:

- `data/registries/source_registry.json`
- `data/registries/mechanism_fingerprints.json`

These files are intentionally small. They define the schema and assumptions
before large-scale ingestion.

## Commands

```bash
python -m catalytic_earth.cli validate
python -m catalytic_earth.cli build-ledger --out artifacts/source_ledger.json
python -m catalytic_earth.cli fingerprint-demo --out artifacts/mechanism_demo.json
```

## Expected Artifacts

- `artifacts/source_ledger.json`
- `artifacts/mechanism_demo.json`

## Evaluation

V0 passes if:

- every source record has role, access, license, and caveat fields
- every fingerprint has active-site, reaction-center, evidence, and uncertainty
  fields
- the CLI can create artifacts from the registries
- tests pass with only standard-library Python

## Next Milestone

Add ingestion adapters for Rhea and M-CSA first. They are smaller and more
mechanism-centered than broad sequence repositories, so they are the right
starting point for graph design.
