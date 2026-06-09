# External Materialization Wave 2 - current702

Run: 2026-06-09T03:44:26Z

Wave 2 consumed the 2026-06-09 admission QA merged surface and import-ready preview, carrying forward already materialized rows while avoiding coordinate downloads because the run started below the 10 GiB disk floor.

## Summary

- Input rows: `845`
- Coordinate materialized new: `0`
- Coordinate reused from consumed preview: `333`
- Locator sidecars materialized new: `309`
- Locator sidecars reused from consumed preview: `333`
- Import-ready preview count: `333`
- Repair/continuation queue count: `512`
- Duplicate conflicts: `33`
- Disk free at start GiB: `7.1`

## Consumed Source Artifacts

- `external_bulk_ingestion_scaleout`: `origin/ce-external-bulk-pagination-scaleout-20260609:artifacts/v3_external_bulk_ingestion_scaleout_current702_20260609.json` (sha256 `3804f45dec32578ddab615abf78a8aadfc6d9591065bcd0ab19a1dbcf23e8592`)
- `external_bulk_ingestion_scaleout_provisional_import_preview`: `origin/ce-external-bulk-pagination-scaleout-20260609:artifacts/v3_external_bulk_ingestion_scaleout_provisional_import_preview_current702_20260609.json` (sha256 `5d37f102a095ee3dfa1a1bcd7fbc62b186232b60f71938499f0db665b4a43001`)
- `external_materialization_admission_batch`: `origin/ce-external-materialization-admission-batch-20260608:artifacts/v3_external_materialization_admission_batch_current702_20260608.json` (sha256 `ce0cd844c465fcd28181d087f6d807bc90f8b0f47df951572564acca9540f9a6`)
- `external_materialization_import_ready_preview`: `origin/ce-external-materialization-admission-batch-20260608:artifacts/v3_external_materialization_import_ready_preview_current702_20260608.json` (sha256 `b771d847359392ccc17c472906b8497012071ebc7b5c1d284f1d8fb2313b926e`)
- `previous_external_admission_qa_surface`: `origin/ce-external-admission-qa-merger-20260608:artifacts/v3_external_admission_merged_surface_current702_20260608.json` (sha256 `41f57a9d8c1f2fa317c3cdeb869b18d49c2530c6d9124666a2800266e0fa969a`)
- `wave2_import_ready_source_input`: `artifacts/v3_external_admission_import_ready_preview_current702_20260609.json` (sha256 `07dfa19f68822ffb3fd7a78bfc3b7c5645c6694ef55dc01d6ecdf7c9747bd713`)
- `wave2_merged_surface_input`: `artifacts/v3_external_admission_merged_surface_current702_20260609.json` (sha256 `ecf2103e9a95fc5ffa870de63c0faf88022c8cceeda34d4fe774b9c9380a211b`)

## Wave 2 Terminal Counts

| terminal state | count |
| --- | ---: |
| `blocked_duplicate_or_current_registry_conflict` | 33 |
| `import_ready_preview_carried_forward` | 333 |
| `locator_sidecar_materialized_coordinate_pending` | 309 |
| `repair_queue_coordinate_ready_pending_locator` | 120 |
| `repair_queue_coordinate_repair_candidate` | 3 |
| `repair_queue_hard_blocked_with_next_action` | 2 |
| `repair_queue_locator_repair_candidate` | 8 |
| `repair_queue_repairable_locator_blocker` | 37 |

## Repair Buckets

| repair bucket | count |
| --- | ---: |
| `coordinate_materialization_continuation_due_disk_floor` | 309 |
| `coordinate_repair` | 3 |
| `duplicate_conflict_no_import` | 33 |
| `hard_blocker` | 2 |
| `locator_repair` | 45 |
| `source_free_locator_materialization_needed` | 120 |

## Import-Ready Preview

- Rows: `333`
- Preview-only; no production import, registry, ontology, split, threshold, or model-weight edit was performed.

## Exact Next Continuation

- Restore disk free space above 10 GiB, then rerun coordinate materialization for the locator-sidecar continuation rows and the coordinate-ready pending-locator queue before expanding the controlled import-ready preview.
