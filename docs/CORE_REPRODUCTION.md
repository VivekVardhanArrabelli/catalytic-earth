# Locked core reproduction

The canonical core is deliberately small: standard-library Python, no network,
no accelerator, no external binary, no current-working-directory assumption,
and no third-party data bundle.

From a wheel:

```bash
python -m venv .venv
. .venv/bin/activate              # Windows: .venv\Scripts\activate
python -m pip install --no-deps catalytic_earth-0.1.0-py3-none-any.whl
catalytic-earth reproduce
```

Expected result SHA-256:

```text
a2374c6530dfd3b4681db5c3db691fdcdedbf645604c6e7dfe0b95ab7e89ea98
```

The command loads four project-authored fixture records through the versioned
typed mechanism schema, counts exact object/evidence types, retains one
synthetic negative observation, and checks the canonical result hash. It is a
packaging, schema, determinism, and negative-record-retention result.

It is not a biological benchmark, mechanism prediction, external validation,
or evidence that any real enzyme record is correct. Those stronger claims need
licensed source snapshots, exact tool/model environments, independent review,
and prospective evidence.

The old research command surface remains available as
`catalytic-earth-legacy`, is outside the locked core guarantee, and is frozen
pending decomposition.

## First biological kernel

The same dependency-free wheel also packages the compiled Atlas-3 records and
one local SQLite query:

```bash
catalytic-earth atlas3
```

Expected runtime-result SHA-256:

```text
1c21a74b09b5812f27c18d49e891cbe9cad6030364a4b6a41a895cdccb1f1921
```

This command loads three real biological cases and nine separately counted
Tier-0/Tier-1/Tier-2 objects, validates their internal provenance bindings,
materializes an in-memory database, executes the frozen query, and checks the
expected result. The wheel contains the compiled records and source hashes,
not the 1.2 MB raw source package; source-level re-audit remains a repository
operation described in [`ATLAS3_KERNEL.md`](ATLAS3_KERNEL.md).

This is deterministic reproduction of useful compiled knowledge. It is not
independent review, biological validation, a coverage or accuracy estimate,
prospective discovery, or a completed assay.

## Ten-case relationship-query surface

The wheel also packages the immutable Atlas-3 kernel plus the seven-case
Atlas-10 extension and its two frozen queries:

```bash
catalytic-earth atlas10
```

Expected runtime-result SHA-256:

```text
57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb
```

The command reproduces 10 cases and 30 typed truth objects, three documented
Rhea query gaps, one mandatory non-detailed abstention, 21 source steps, and 61
source electron-flow objects. It executes the convergent-strategy and
shared-fold/divergent-chemistry queries without network, accelerator, external
binary, or current-working-directory dependence.

The wheel contains compiled fields, source hashes, query expectations, and
attribution—not the raw Atlas-10 upstream snapshots. See
[`ATLAS10_KERNEL.md`](ATLAS10_KERNEL.md) for repository audit commands and the
still-pending external review-attempt gate. Reproduction is not independent
review, biological accuracy, representative coverage, discovery, design
readiness, or an assay result.
