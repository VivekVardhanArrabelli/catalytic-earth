# External Materialization Wave 2 - current702

Run: 2026-06-09T13:05:58Z

Wave 2 consumed the 2026-06-09 admission QA surface plus landed broad bulk, metal/phosphoryl/glycoside, near-orphan/diversity, PLP/radical/cobalamin, and redox/cofactor shard previews. It deduped the surfaces into one review surface, carried only controlled-review-ready rows into the import-ready preview, and avoided coordinate downloads while producing source-free locator sidecars for coordinate-continuation rows.

## Summary

- Source surface rows consumed: `18235`
- Unique input candidates: `12495`
- Import-ready source preview rows consumed: `3504`
- Supplemental review shard rows referenced: `4378`
- Coordinate materialized new: `0`
- Coordinate reused from consumed preview metadata: `318`
- Local coordinate paths present from consumed preview: `13`
- Locator sidecars materialized new: `2934`
- Locator sidecars reused from this Wave 2 directory: `2279`
- Local locator paths present from consumed preview: `0`
- Source import-ready previews kept in coordinate continuation: `2811`
- Import-ready preview count: `318`
- Repair/continuation queue count: `12177`
- Duplicate conflicts: `1420`
- Cross-source duplicates collapsed: `4818`
- Disk free at start GiB: `None`

## Consumed Source Artifacts

- `v3_external_admission_import_ready_preview_current702_20260609`: `artifacts/v3_external_admission_import_ready_preview_current702_20260609.json` (sha256 `07dfa19f68822ffb3fd7a78bfc3b7c5645c6694ef55dc01d6ecdf7c9747bd713`)
- `v3_external_admission_merged_surface_current702_20260609`: `artifacts/v3_external_admission_merged_surface_current702_20260609.json` (sha256 `ecf2103e9a95fc5ffa870de63c0faf88022c8cceeda34d4fe774b9c9380a211b`)
- `v3_external_bulk_ingestion_scaleout_wave2_current702_20260609`: `artifacts/v3_external_bulk_ingestion_scaleout_wave2_current702_20260609.json` (sha256 `6ccfbc94adab00c626ae7ec4f23028bda04b4505b570614f9d45bdd23662ed45`)
- `v3_external_bulk_ingestion_scaleout_wave2_provisional_import_preview_current702_20260609`: `artifacts/v3_external_bulk_ingestion_scaleout_wave2_provisional_import_preview_current702_20260609.json` (sha256 `49d89388aa52db8f5d9a1a4895d47f430d5ff765ef3eaad92d5d5b5e90ca24a3`)
- `v3_external_scaleout_shard_metal_phosphoryl_glycoside_current702_20260609`: `artifacts/v3_external_scaleout_shard_metal_phosphoryl_glycoside_current702_20260609.json` (sha256 `7539db610432a53786502eae4c0e7ffb2f521460543558c77c48bdec977c9ac5`)
- `v3_external_scaleout_shard_metal_phosphoryl_glycoside_import_ready_preview_current702_20260609`: `artifacts/v3_external_scaleout_shard_metal_phosphoryl_glycoside_import_ready_preview_current702_20260609.json` (sha256 `74acbe56373f7c89e341fc54f2a94209615e2f2728174d24ce9920cf5c339088`)
- `v3_external_scaleout_shard_near_orphan_diversity_current702_20260609`: `artifacts/v3_external_scaleout_shard_near_orphan_diversity_current702_20260609.json` (sha256 `28561b355f6759217170a6193e5a436cad0f0a34553a0a58067d28fb59056149`)
- `v3_external_scaleout_shard_near_orphan_diversity_import_ready_preview_current702_20260609`: `artifacts/v3_external_scaleout_shard_near_orphan_diversity_import_ready_preview_current702_20260609.json` (sha256 `348f6bd434a1eb0e1bad98e961a370d9a2b294345cfc581c0d8427e17dac8819`)
- `v3_external_scaleout_shard_plp_radical_cobalamin_current702_20260609`: `artifacts/v3_external_scaleout_shard_plp_radical_cobalamin_current702_20260609.json` (sha256 `3fb1e2d021ded6eb6848a8ff13083cd61ad4490ee7d282e7c333762735c947c7`)
- `v3_external_scaleout_shard_plp_radical_cobalamin_import_ready_preview_current702_20260609`: `artifacts/v3_external_scaleout_shard_plp_radical_cobalamin_import_ready_preview_current702_20260609.json` (sha256 `8b7730538ce3dad06ddb38bc84e116e6a95d50ba86ae697d32b081754c983005`)
- `v3_external_scaleout_shard_redox_cofactor_confounded_current702_20260609`: `artifacts/v3_external_scaleout_shard_redox_cofactor_confounded_current702_20260609.json` (sha256 `0554dee0f8b810d3fa161eb357dd2fcb3c30dc8fa530cf22829d336de554e98f`)
- `v3_external_scaleout_shard_redox_cofactor_confounded_import_ready_preview_current702_20260609`: `artifacts/v3_external_scaleout_shard_redox_cofactor_confounded_import_ready_preview_current702_20260609.json` (sha256 `56a68ddefb8478af61118372ddee1b46104330692f931bf5a169e61890f13489`)
- `v3_scaleout_glycoside_nucleoside_shard_current702_20260608`: `artifacts/v3_scaleout_glycoside_nucleoside_shard_current702_20260608.json` (sha256 `1835fa174e43b171c5335b4b7268a99c3619b3f675fbfc19c47b881762c341be`)
- `v3_scaleout_metal_hydrolase_shard_current702_20260608`: `artifacts/v3_scaleout_metal_hydrolase_shard_current702_20260608.json` (sha256 `96ed2f0ea671e257d006669228281b2b2482c87fdf0a7284039e36e3fa6fb465`)
- `v3_scaleout_near_orphan_tail_shard_current702_20260608`: `artifacts/v3_scaleout_near_orphan_tail_shard_current702_20260608.json` (sha256 `ad52ab2c99fbf5065baca18e3c89cf3fe50d8fc91bcc5fca4e93ddbd40ea733d`)
- `v3_scaleout_phosphoryl_transfer_shard_current702_20260608`: `artifacts/v3_scaleout_phosphoryl_transfer_shard_current702_20260608.json` (sha256 `7db4ef6fdf747ac66226d1bf8fb7f13efb881c4e69d925eb0ac3dc6d13b80848`)
- `v3_scaleout_plp_children_shard_current702_20260608`: `artifacts/v3_scaleout_plp_children_shard_current702_20260608.json` (sha256 `360e8453a6c89c60ddc0789610bdbbb8419c73ba1adfaece282abd545999b701`)
- `v3_scaleout_radical_sam_cobalamin_shard_current702_20260608`: `artifacts/v3_scaleout_radical_sam_cobalamin_shard_current702_20260608.json` (sha256 `302c47fb5ff0fbd74d1be2a38dff5c47a26428ccc418aeb2427a20864c4ffaa5`)
- `v3_scaleout_redox_oxygen_sulfur_shard_current702_20260608`: `artifacts/v3_scaleout_redox_oxygen_sulfur_shard_current702_20260608.json` (sha256 `23c602dee83d76d46e2e555e68b7fdd4ba222019063e855430d72ca9f15f3267`)

## Wave 2 Terminal Counts

| terminal state | count |
| --- | ---: |
| `blocked_duplicate_or_current_registry_conflict` | 1420 |
| `import_ready_preview_carried_forward` | 318 |
| `locator_sidecar_materialized_coordinate_pending` | 1032 |
| `locator_sidecar_reused_coordinate_pending` | 1370 |
| `repair_queue_coordinate_ready_pending_locator` | 676 |
| `repair_queue_coordinate_repair_candidate` | 237 |
| `repair_queue_hard_blocked_with_next_action` | 2956 |
| `repair_queue_locator_repair_candidate` | 57 |
| `repair_queue_reject/OOS_preserve_signal` | 1562 |
| `repair_queue_repairable_coordinate_blocker` | 11 |
| `repair_queue_repairable_locator_blocker` | 45 |
| `shard_import_ready_preview_locator_sidecar_materialized_coordinate_pending` | 1902 |
| `shard_import_ready_preview_locator_sidecar_reused_coordinate_pending` | 909 |

## Repair Buckets

| repair bucket | count |
| --- | ---: |
| `coordinate_materialization_continuation_due_disk_floor` | 5213 |
| `coordinate_repair` | 248 |
| `duplicate_conflict_no_import` | 1420 |
| `hard_blocker` | 2956 |
| `locator_repair` | 102 |
| `reject_or_oos_preserve_signal_no_import` | 1562 |
| `source_free_locator_materialization_needed` | 676 |

## Import-Ready Preview

- Rows: `318`
- Preview-only; no production import, registry, ontology, split, threshold, or model-weight edit was performed.

## Exact Next Continuation

- Restore disk free space above 10 GiB, then rerun coordinate materialization for the shard-preview and locator-sidecar continuation rows, then rerun the controlled import-review preflight before any production registry/import action.
