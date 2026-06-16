# External Batch Import Approval Packet - current702

Created UTC: `2026-06-16T15:03:49Z`

This is a decision packet only. It performs no production import, registry edit, ontology edit, split edit, threshold change, or model change.

## Batch Decision

- Rows that can become countable after one controlled batch approval: 197
- Blocked rows remaining: 636
- Production import authorized here: False

One final controlled batch approval can advance 197 machine-clean rows to countable import handling, provided the approval also records the label-factory gate and production registry-change authorization. This packet does not perform that import.

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

## Blocked Mechanical Gates

| gate | rows |
| --- | ---: |
| `coordinate_materialization_hash_or_path_reconciliation` | 473 |
| `current702_duplicate_reconciliation_or_reject` | 13 |
| `external_duplicate_reconciliation_or_reject` | 27 |
| `source_free_locator_sidecar_materialization_or_linkage_repair` | 121 |
| `source_retrieval_or_materialization_hard_blocker_clearance` | 2 |

## Mechanical Reconciliation Audit

- `locator_sidecar_linked_repair_surface_rows`: `470`
- `locator_sidecar_linked_but_coordinate_missing_rows`: `470`
- `coordinate_hash_present_but_coordinate_path_unmaterialized_rows`: `0`
- `duplicate_status_reconciled_to_terminal_conflict_rows`: `40`
- `terminal_state_normalization_total_rows`: `833`
- `count_normalization_reconciles`: `True`

## Ready Lane Counts

| lane | ready rows |
| --- | ---: |
| PLP children | 7 |
| glycoside/nucleoside | 19 |
| metal hydrolase | 82 |
| near-orphan/no-reliable-structure | 22 |
| phosphoryl transfer | 3 |
| radical-SAM/cobalamin | 30 |
| redox oxygen/sulfur | 34 |

## Validation

- `source_preflight_passed`: `True`
- `ready_rows_match_preflight_count`: `True`
- `blocked_rows_match_preflight_count`: `True`
- `terminal_counts_reconcile`: `True`
- `all_ready_rows_have_coordinate_hash`: `True`
- `all_ready_rows_have_locator_sidecar`: `True`
- `all_ready_rows_have_source_hashes`: `True`
- `all_ready_rows_have_source_provenance`: `True`
- `all_blocked_rows_have_mechanical_gate`: `True`
- `passed`: `True`

## Blocked Row Sample

| candidate | lane | terminal state | gate |
| --- | --- | --- | --- |
| `uniprot:Q495T6` | metal hydrolase | `duplicate_external_conflict` | `external_duplicate_reconciliation_or_reject` |
| `uniprot:A4D2B0` | metal hydrolase | `duplicate_external_conflict` | `external_duplicate_reconciliation_or_reject` |
| `uniprot:Q6GQQ9` | metal hydrolase | `duplicate_external_conflict` | `external_duplicate_reconciliation_or_reject` |
| `uniprot:Q9H8Y5` | metal hydrolase | `duplicate_external_conflict` | `external_duplicate_reconciliation_or_reject` |
| `uniprot:P42694` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q68D91` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q5T1V6` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:A2A288` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q6NVH7` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q9P2E3` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q9Y2E5` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q9BYK8` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:O14638` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:P49641` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q8NDL9` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q9UPW5` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:O76074` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:O00754` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:P08473` | metal hydrolase | `duplicate_current702_conflict` | `current702_duplicate_reconciliation_or_reject` |
| `uniprot:P45381` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q01432` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q9BQ52` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:O15072` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:O43462` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:O75173` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:O75439` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:O75900` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:P23109` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:P52888` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:P55786` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q13219` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q13444` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q6DHV7` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q8N6M6` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q8NEM8` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q92878` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q9H324` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q9Y2T3` | metal hydrolase | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:P21912` | redox oxygen/sulfur | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| `uniprot:Q8S7E1` | redox oxygen/sulfur | `repairable_coordinate_blocker` | `coordinate_materialization_hash_or_path_reconciliation` |
| ... | ... | ... | plus 596 more rows |
