# External Import Review Preflight - current702

Controlled import-review preflight over the Wave 2 external materialization review surface: the carried-forward import-ready preview rows plus the expanded repair queue. No production registry, import file, ontology, split, threshold, or model artifact was edited.

## Summary

- Preview rows: 197
- Repair-surface rows: 636
- Total review-surface rows: 833
- Controlled import-review ready rows: 197
- Repair/conflict queue rows: 636
- Final human batch approval: A final controlled human batch approval could cover 197 machine-clean rows at once rather than row-by-row; production registry authorization and label-factory gates remain outside this preflight.
- Production import authorized here: False

## Terminal State Counts

| terminal state | count |
| --- | ---: |
| `controlled_import_review_ready` | 197 |
| `needs_structural_duplicate_screen` | 0 |
| `needs_family_policy_review` | 0 |
| `repairable_locator_blocker` | 121 |
| `repairable_coordinate_blocker` | 473 |
| `duplicate_current702_conflict` | 13 |
| `duplicate_external_conflict` | 27 |
| `reject/OOS_preserve_signal` | 0 |
| `hard_blocked_with_next_action` | 2 |

## Review Scope Counts

| scope | count |
| --- | ---: |
| `import_ready_preview` | 197 |
| `materialization_repair_surface` | 636 |

## Lane Counts

| lane | count |
| --- | ---: |
| PLP children | 119 |
| glycoside/nucleoside | 117 |
| metal hydrolase | 120 |
| near-orphan/no-reliable-structure | 120 |
| phosphoryl transfer | 120 |
| radical-SAM/cobalamin | 117 |
| redox oxygen/sulfur | 120 |

## Lane Terminal Counts

| lane | terminal counts |
| --- | --- |
| PLP children | `{'controlled_import_review_ready': 7, 'duplicate_current702_conflict': 3, 'duplicate_external_conflict': 3, 'repairable_coordinate_blocker': 106}` |
| glycoside/nucleoside | `{'controlled_import_review_ready': 19, 'duplicate_current702_conflict': 2, 'duplicate_external_conflict': 4, 'repairable_coordinate_blocker': 60, 'repairable_locator_blocker': 32}` |
| metal hydrolase | `{'controlled_import_review_ready': 82, 'duplicate_current702_conflict': 1, 'duplicate_external_conflict': 4, 'repairable_coordinate_blocker': 31, 'repairable_locator_blocker': 2}` |
| near-orphan/no-reliable-structure | `{'controlled_import_review_ready': 22, 'duplicate_external_conflict': 4, 'hard_blocked_with_next_action': 2, 'repairable_coordinate_blocker': 22, 'repairable_locator_blocker': 70}` |
| phosphoryl transfer | `{'controlled_import_review_ready': 3, 'duplicate_current702_conflict': 2, 'duplicate_external_conflict': 4, 'repairable_coordinate_blocker': 105, 'repairable_locator_blocker': 6}` |
| radical-SAM/cobalamin | `{'controlled_import_review_ready': 30, 'duplicate_current702_conflict': 2, 'duplicate_external_conflict': 4, 'repairable_coordinate_blocker': 73, 'repairable_locator_blocker': 8}` |
| redox oxygen/sulfur | `{'controlled_import_review_ready': 34, 'duplicate_current702_conflict': 3, 'duplicate_external_conflict': 4, 'repairable_coordinate_blocker': 76, 'repairable_locator_blocker': 3}` |

## Policy Blockers

| blocker | scope | ready rows affected |
| --- | --- | ---: |
| `production_registry_change_authorization_not_present` | `production_import` | 197 |
| `label_factory_gate_and_explicit_review_decision_not_run_here` | `production_import` | 197 |
| `full_foldseek_tm_current702_structural_duplicate_screen_not_computed` | `caveat` | 197 |

## Validation

- Validation passed: True
- JSON/count reconciliation passed: True
- Source provenance present for all preview rows: True
- Source provenance present for all review rows: True
- Source hashes present for all preview rows: True
- Source hashes present for all review rows: True
- Source-free locators present for all preview rows: True
- Coordinate hashes present for all preview rows: True
- Sequence hashes unique across preview: True
- Exact current702 coordinate/structure-ID overlaps: 9

## Review Queue

| candidate | lane | terminal state | blockers | next action |
| --- | --- | --- | --- | --- |
| `uniprot:Q495T6` | metal hydrolase | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:A4D2B0` | metal hydrolase | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:Q6GQQ9` | metal hydrolase | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:Q9H8Y5` | metal hydrolase | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:P42694` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q68D91` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q5T1V6` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:A2A288` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q6NVH7` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q9P2E3` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q9Y2E5` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q9BYK8` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:O14638` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:P49641` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q8NDL9` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q9UPW5` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:O76074` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:O00754` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:P08473` | metal hydrolase | `duplicate_current702_conflict` | `exact_current702_accession_or_sequence_conflict` | Reject as current702 duplicate unless a reviewer records a distinct mechanism. |
| `uniprot:P45381` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q01432` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q9BQ52` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:O15072` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:O43462` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:O75173` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:O75439` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:O75900` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:P23109` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:P52888` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:P55786` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q13219` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q13444` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q6DHV7` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q8N6M6` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q8NEM8` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q92878` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q9H324` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q9Y2T3` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:P21912` | redox oxygen/sulfur | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| `uniprot:Q8S7E1` | redox oxygen/sulfur | `repairable_coordinate_blocker` | `coordinate_materialization_or_hash_missing` | Repair coordinate materialization or coordinate hash provenance. |
| ... | ... | ... | ... | plus 596 more rows |

## Outputs

- Preflight artifact: `artifacts/v3_external_import_review_preflight_current702_20260616.json`
- Ready preview: `artifacts/v3_external_import_review_ready_preview_current702_20260616.json`
- Repair/conflict queue: `artifacts/v3_external_import_review_repair_queue_current702_20260616.json`
