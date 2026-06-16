# External Materialization Wave 2 - current702

Run: 2026-06-16T14:03:01Z

Wave 2 consumed the 2026-06-09 admission QA surface plus landed broad bulk, metal/phosphoryl/glycoside, near-orphan/diversity, PLP/radical/cobalamin, and redox/cofactor shard previews. It deduped the surfaces into one review surface, carried only controlled-review-ready rows into the import-ready preview, and avoided coordinate downloads while producing source-free locator sidecars for coordinate-continuation rows.

## Summary

- Source surface rows consumed: `833`
- Unique input candidates: `833`
- Import-ready source preview rows consumed: `431`
- Supplemental review shard rows referenced: `0`
- Coordinate download budget: `0`
- Coordinate downloads attempted: `0`
- Coordinate downloads performed: `0`
- Coordinate downloads performed this invocation: `0`
- Coordinate materialized new: `0`
- Coordinate materialized new this invocation: `0`
- Wave 2 coordinate files present: `0`
- Coordinate reused from local artifacts for Wave 2: `204`
- Coordinate reused from consumed preview metadata: `0`
- Local coordinate paths present from consumed preview: `0`
- Locator sidecars materialized new: `667`
- Locator sidecars reused from this Wave 2 directory: `0`
- Coordinate-identity locator sidecars reused: `0`
- Local locator paths present from consumed preview: `0`
- Coordinate-ready rows promoted into preview: `197`
- Coordinate-ready materialized preview rows: `197`
- Source import-ready previews kept in coordinate continuation: `0`
- Import-ready preview count: `197`
- Repair/continuation queue count: `636`
- Duplicate conflicts: `40`
- Cross-source duplicates collapsed: `0`
- Disk free at start GiB: `None`
- Disk free at end GiB: `8.573`

## Consumed Source Artifacts

- `v3_external_bulk_ingestion_scout_current702_20260608`: `artifacts/v3_external_bulk_ingestion_scout_current702_20260616_run1403_size120.json` (sha256 `7463085bd6665e46872b7626573908e7598f1b3b7fb436be615559f8fe70edb7`)
- `v3_external_source_admission_ready_preview_current702_20260608`: `artifacts/v3_external_source_admission_ready_preview_431_current702_20260616_run1403_bulk_size120.json` (sha256 `96e675fea90dc93c93a6c9e43e3deac2455b1ef4452f02aa44da6bc9a9eb65f6`)

## Wave 2 Terminal Counts

| terminal state | count |
| --- | ---: |
| `blocked_duplicate_or_current_registry_conflict` | 40 |
| `import_ready_preview_materialized_coordinate_locator` | 197 |
| `locator_sidecar_materialized_coordinate_pending` | 470 |
| `repair_queue_coordinate_ready_pending_locator` | 117 |
| `repair_queue_coordinate_repair_candidate` | 3 |
| `repair_queue_hard_blocked_with_next_action` | 2 |
| `repair_queue_locator_repair_candidate` | 4 |

## Repair Buckets

| repair bucket | count |
| --- | ---: |
| `coordinate_materialization_continuation_due_disk_floor` | 470 |
| `coordinate_repair` | 3 |
| `duplicate_conflict_no_import` | 40 |
| `hard_blocker` | 2 |
| `locator_repair` | 4 |
| `source_free_locator_materialization_needed` | 117 |

## Import-Ready Preview

- Rows: `197`
- Preview-only; no production import, registry, ontology, split, threshold, or model-weight edit was performed.

## Exact Next Continuation

- Restore disk free space above 10 GiB, then rerun coordinate materialization for the shard-preview and locator-sidecar continuation rows, then rerun the controlled import-review preflight before any production registry/import action.
