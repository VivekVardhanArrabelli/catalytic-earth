# External Batch Import Approval Packet - current702

Created UTC: `2026-06-10T14:34:17Z`

This is a decision packet only. It performs no production import, registry edit, ontology edit, split edit, threshold change, or model change.

## Batch Decision

- Rows that can become countable after one controlled batch approval: 275
- Blocked rows remaining: 12220
- Production import authorized here: False

One final controlled batch approval can advance 275 machine-clean rows to countable import handling, provided the approval also records the label-factory gate and production registry-change authorization. This packet does not perform that import.

## Terminal State Counts

| terminal state | count |
| --- | ---: |
| `controlled_import_review_ready` | 275 |
| `needs_structural_duplicate_screen` | 1 |
| `needs_family_policy_review` | 0 |
| `repairable_locator_blocker` | 1096 |
| `repairable_coordinate_blocker` | 5179 |
| `duplicate_current702_conflict` | 203 |
| `duplicate_external_conflict` | 1275 |
| `reject/OOS_preserve_signal` | 1562 |
| `hard_blocked_with_next_action` | 2904 |

## Blocked Mechanical Gates

| gate | rows |
| --- | ---: |
| `coordinate_materialization_hash_or_path_reconciliation` | 5179 |
| `current702_duplicate_reconciliation_or_reject` | 203 |
| `current702_structural_duplicate_screen` | 1 |
| `external_duplicate_reconciliation_or_reject` | 1269 |
| `preserve_out_of_scope_or_hard_negative_signal` | 1562 |
| `preview_sequence_duplicate_reconciliation` | 6 |
| `source_free_locator_sidecar_materialization_or_linkage_repair` | 1096 |
| `source_retrieval_or_materialization_hard_blocker_clearance` | 2904 |

## Mechanical Reconciliation Audit

- `locator_sidecar_linked_repair_surface_rows`: `4931`
- `locator_sidecar_linked_but_coordinate_missing_rows`: `4931`
- `coordinate_hash_present_but_coordinate_path_unmaterialized_rows`: `4`
- `duplicate_status_reconciled_to_terminal_conflict_rows`: `1478`
- `terminal_state_normalization_total_rows`: `12495`
- `count_normalization_reconciles`: `True`

## Ready Lane Counts

| lane | ready rows |
| --- | ---: |
| PLP children | 6 |
| adjacent high-yield lyase/isomerase | 10 |
| glycoside hydrolase | 1 |
| glycoside/nucleoside | 39 |
| metal hydrolase | 105 |
| metal hydrolase Mg/Mn controls | 1 |
| metal hydrolase amidase/peptidase boundary | 4 |
| near-orphan/no-reliable-structure | 27 |
| nucleotide phosphoryl-transfer boundary | 1 |
| phosphoryl transfer | 6 |
| phosphoryl transfer/phosphatase | 1 |
| radical-SAM/cobalamin | 27 |
| redox oxygen/sulfur | 47 |

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
| `uniprot:P42694` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q68D91` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q5T1V6` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q9Y2E5` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:O14638` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:P49641` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:P00813` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q01433` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q8NDL9` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q9NZK5` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q9UPW5` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:O00754` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:P45381` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q01432` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:O76074` | metal hydrolase | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:P21912` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q8S7E1` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q9MBA1` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q9NZ45` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q9FYC2` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:O75306` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:O00217` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:O75251` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:P0AC47` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q1QYU7` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:P47985` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:P21913` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q3T189` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q9CQA3` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:A5PL98` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:P07014` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:P21801` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:P21914` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q09545` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q8LB02` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q8LBZ7` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q6H4G3` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q9FJP9` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:Q9ZR03` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| `uniprot:P77165` | redox oxygen/sulfur | `repairable_locator_blocker` | `source_free_locator_sidecar_materialization_or_linkage_repair` |
| ... | ... | ... | plus 12180 more rows |
