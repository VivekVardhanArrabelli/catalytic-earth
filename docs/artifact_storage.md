# Artifact Storage Policy

Catalytic Earth keeps a research record, not a scratchpad dump. Generated
artifacts can be moved out of Git only after their conclusion and provenance are
preserved in a committed manifest or canonical summary.

## Current Inventory

The current storage inventory is:

```text
artifacts/v3_artifact_storage_inventory_1025.json
artifacts/v3_artifact_storage_policy_check_1025.json
```

At creation, the inventory covered 2,574 artifact files and 2.55 GiB of
artifact payload, with 108 files above the 5 MiB large-file threshold. The
policy check passed with zero deletion authorization and zero unclassified large
artifacts.

## Categories

- `canonical_evidence`: decision, gate, policy, regression, or terminal-review
  artifacts. Keep these in Git unless a future migration preserves the exact
  artifact hash, conclusion, and downstream references.
- `regenerable_intermediate`: generated slice artifacts such as graph,
  geometry, retrieval, and repeated label-factory outputs. These may be
  externalized only after recording producer command, input artifacts,
  downstream consumers, and SHA-256.
- `raw_cache`: structure sidecars, sequence-search exports, backend TSV/FASTA
  files, and other bulky caches. These are the strongest candidates for
  external object storage, but not for silent deletion.
- `compact_artifact`: small artifacts that are not currently worth migrating.
- `large_unclassified`: blocker category. Do not commit a new large artifact in
  this category; classify it or add a specific policy rule first.

## Non-Loss Rule

No artifact may be deleted or removed from Git unless all of the following are
true:

1. A committed manifest row records its path, size, SHA-256, category, and
   storage decision.
2. A committed canonical artifact or document preserves the scientific
   conclusion that artifact supported.
3. The producer command, source inputs, and downstream consumers are recorded or
   explicitly marked unavailable with a reason.
4. The replacement storage location is recorded for raw caches or large
   intermediates.
5. A regression or policy check confirms the migration did not weaken label,
   import, leakage, or benchmark guarantees.

This policy does not authorize history rewriting. Any history rewrite or Git LFS
migration needs an explicit manual decision because it changes collaborator and
automation assumptions.

## Commands

Build the inventory:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-artifact-storage-inventory \
  --artifact-dir artifacts \
  --large-file-threshold-mb 5 \
  --top-n 75 \
  --out artifacts/v3_artifact_storage_inventory_1025.json
```

Check the inventory:

```bash
PYTHONPATH=src python -m catalytic_earth.cli check-artifact-storage-policy \
  --inventory artifacts/v3_artifact_storage_inventory_1025.json \
  --out artifacts/v3_artifact_storage_policy_check_1025.json
```

A source-only checkout can avoid the artifact payload while still validating
code imports:

```bash
git clone --filter=blob:none --sparse git@github.com:VivekVardhanArrabelli/catalytic-earth.git catalytic-earth-source
cd catalytic-earth-source
git sparse-checkout set src tests docs data
PYTHONPATH=src python -m catalytic_earth.cli validate
```

Automation using the repo deploy key should export the project SSH command for
the whole sparse-checkout session, not only the initial clone.

## Immediate Migration Candidates

The first candidates for future external storage are:

- large `v1_graph_*` slice graphs;
- large `v3_geometry_features_*` and `v3_geometry_retrieval_*` slices;
- structure coordinate sidecars under `artifacts/v3_foldseek_coordinates_1000/`;
- backend TSV/FASTA/sequence-search sidecars.

Do not move these yet just because they are large. Move them only after the
manifest records producer commands, input dependencies, downstream consumers,
and a stable external location.
