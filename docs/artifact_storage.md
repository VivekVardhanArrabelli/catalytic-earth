# Artifact Storage Policy

Catalytic Earth keeps a research record, not a scratchpad dump. Generated
artifacts can be moved out of Git only after their conclusion and provenance are
preserved in a committed manifest or canonical summary.

## Current Inventory

The current storage inventory is:

```text
artifacts/v3_artifact_storage_inventory_1025.json
artifacts/v3_artifact_storage_policy_check_1025.json
artifacts/v3_artifact_producer_consumer_manifest_1025.json
artifacts/v3_artifact_migration_readiness_plan_1025.json
artifacts/v3_artifact_migration_execution_1025.json
artifacts/v3_artifact_admission_guard_1025.json
```

The refreshed inventory covers 2,580 artifact files and 2.5562 GiB, including
storage planning artifacts. The large-file surface remains 108 files above the
5 MiB threshold. The policy check passes with zero deletion authorization and
zero unclassified large artifacts. The producer/consumer manifest covers all
108 large `regenerable_intermediate` and `raw_cache` rows; the
migration-readiness plan ranks those rows for future review but authorizes no
migration; the Phase 1 execution manifest records exact current-Git target
URIs for the same 108 rows and keeps `migration_ready=false`,
`remote_sha256_verified=false`, `restore_test_passed=false`, and
`removal_allowed=false` for every row. The admission guard passes only because
every current large noncanonical row has a manifest row.

The execution manifest is explicit about the current-main scientific baseline:
`baseline=current_main_three_external_hard_negatives`, `slice_id=1025`, and
`canonical_countable_label_count=682`. The three external imported
out-of-scope hard negatives are exactly `uniprot:P06744`, `uniprot:P78549`,
and `uniprot:Q3LXA3`; there are 0 imported external seed-fingerprint labels.
Those hard negatives remain `label_type=out_of_scope`, `fingerprint_id=null`,
and `ontology_version_at_decision=label_factory_v1_8fp`.

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

Build producer/downstream provenance for current large noncanonical rows:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-artifact-producer-consumer-manifest \
  --inventory artifacts/v3_artifact_storage_inventory_1025.json \
  --out artifacts/v3_artifact_producer_consumer_manifest_1025.json
```

Build the migration-readiness plan without moving anything:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-artifact-migration-readiness-plan \
  --inventory artifacts/v3_artifact_storage_inventory_1025.json \
  --producer-consumer-manifest artifacts/v3_artifact_producer_consumer_manifest_1025.json \
  --out artifacts/v3_artifact_migration_readiness_plan_1025.json
```

Build and validate the Phase 1 execution manifest without upload or removal:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-artifact-migration-execution-manifest \
  --readiness-plan artifacts/v3_artifact_migration_readiness_plan_1025.json \
  --producer-consumer-manifest artifacts/v3_artifact_producer_consumer_manifest_1025.json \
  --out artifacts/v3_artifact_migration_execution_1025.json

PYTHONPATH=src python -m catalytic_earth.cli validate-artifact-migration \
  --manifest artifacts/v3_artifact_migration_execution_1025.json \
  --dry-run
```

Run a fail-closed restore smoke dry run:

```bash
PYTHONPATH=src python -m catalytic_earth.cli restore-artifacts \
  --manifest artifacts/v3_artifact_migration_execution_1025.json \
  --subset smoke \
  --dry-run
```

Run the future artifact admission guard:

```bash
PYTHONPATH=src python -m catalytic_earth.cli check-artifact-admission-guard \
  --inventory artifacts/v3_artifact_storage_inventory_1025.json \
  --producer-consumer-manifest artifacts/v3_artifact_producer_consumer_manifest_1025.json \
  --out artifacts/v3_artifact_admission_guard_1025.json
```

A source-only checkout can avoid the artifact payload while still validating
code imports:

```bash
export GIT_SSH_COMMAND='ssh -i /Users/vivekvardhanarrabelli/.ssh/catalytic_earth_deploy_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=accept-new'
git clone --filter=blob:none --sparse git@github.com:VivekVardhanArrabelli/catalytic-earth.git catalytic-earth-source
cd catalytic-earth-source
git sparse-checkout set src tests docs data
PYTHONPATH=src python -m catalytic_earth.cli validate
```

Automation using the repo deploy key should export the project SSH command for
the whole sparse-checkout session, not only the initial clone, because later
lazy blob fetches also use SSH. Do not add network-dependent clone checks to
the routine unit suite; keep source-only clone validation as an operator or CI
smoke test with explicit network access.

Source-only CI should run without restored large artifacts for package import,
CLI help, manifest validation, and unit tests that do not require restored
artifacts:

```bash
python -m compileall src
PYTHONPATH=src python -c "import catalytic_earth.transfer_scope"
PYTHONPATH=src python -m catalytic_earth.cli --help
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli validate-artifact-migration --dry-run
```

Restored-artifact CI is separate and heavier. It should call
`restore-artifacts` for the required subset, verify SHA-256 before use, and
then run the artifact-dependent scientific regressions.

## Migration Phases

Phase 1 is instrumentation only: manifest schema, validator, restore tooling,
pointer record format, docs, source-only reproducibility checks, and tests. No
artifact migration, deletion, Git LFS migration, external upload, or history
rewrite has been performed.

Phase 2 may upload approved artifacts only after a human authorizes the storage
target. Every uploaded artifact must have a target URI, independently verified
remote SHA-256, and a passing restore subset test before any Git tracking
change is considered.

Phase 3 is the only phase that may remove approved rows from Git tracking, and
only after the validator derives `removal_allowed=true`. Canonical artifacts
remain fail-closed, pointer records must preserve exact restore metadata, and
source-only plus restored-artifact CI must both pass.

## Immediate Migration Candidates

The first candidates for future external storage are:

- large `v1_graph_*` slice graphs;
- large `v3_geometry_features_*` and `v3_geometry_retrieval_*` slices;
- structure coordinate sidecars under `artifacts/v3_foldseek_coordinates_1000/`;
- backend TSV/FASTA/sequence-search sidecars.

Do not move these yet just because they are large. Move them only after the
manifest records producer commands, input dependencies, downstream consumers,
and a stable external location.
