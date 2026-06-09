# External Import Review Preflight - current702

Controlled import-review preflight over the 333 external import-ready preview rows. No production registry, import file, ontology, split, threshold, or model artifact was edited.

## Summary

- Preview rows: 333
- Controlled import-review ready rows: 317
- Repair/conflict queue rows: 16
- Final human batch approval: A final controlled human batch approval could cover 317 machine-clean rows at once rather than row-by-row; production registry authorization and label-factory gates remain outside this preflight.
- Production import authorized here: False

## Terminal State Counts

| terminal state | count |
| --- | ---: |
| `controlled_import_review_ready` | 317 |
| `needs_structural_duplicate_screen` | 0 |
| `needs_family_policy_review` | 1 |
| `repairable_locator_blocker` | 0 |
| `repairable_coordinate_blocker` | 0 |
| `duplicate_current702_conflict` | 0 |
| `duplicate_external_conflict` | 15 |
| `reject/OOS_preserve_signal` | 0 |
| `hard_blocked_with_next_action` | 0 |

## Lane Counts

| lane | count |
| --- | ---: |
| PLP children | 72 |
| glycoside/nucleoside | 43 |
| metal hydrolase | 15 |
| near-orphan/no-reliable-structure | 1 |
| phosphoryl transfer | 88 |
| radical-SAM/cobalamin | 50 |
| redox oxygen/sulfur | 64 |

## Policy Blockers

| blocker | scope | ready rows affected |
| --- | --- | ---: |
| `production_registry_change_authorization_not_present` | `production_import` | 317 |
| `label_factory_gate_and_explicit_review_decision_not_run_here` | `production_import` | 317 |
| `full_foldseek_tm_current702_structural_duplicate_screen_not_computed` | `caveat` | 317 |

## Validation

- JSON/count reconciliation passed: True
- Source provenance present for all preview rows: True
- Source hashes present for all preview rows: True
- Source-free locators present for all preview rows: True
- Coordinate hashes present for all preview rows: True
- Sequence hashes unique across preview: True
- Exact current702 coordinate/structure-ID overlaps: 0

## Review Queue

| candidate | lane | terminal state | blockers | next action |
| --- | --- | --- | --- | --- |
| `uniprot:P09601` | redox oxygen/sulfur | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:P30519` | redox oxygen/sulfur | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:P29082` | redox oxygen/sulfur | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:Q9UGB7` | redox oxygen/sulfur | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:P04181` | PLP children | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:Q96255` | PLP children | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:P04062` | glycoside/nucleoside | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:O60502` | glycoside/nucleoside | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:Q969G6` | phosphoryl transfer | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:P32189` | phosphoryl transfer | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:Q3T906` | phosphoryl transfer | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:Q9Y6K0` | phosphoryl transfer | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:Q99707` | radical-SAM/cobalamin | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:A6H5Y3` | radical-SAM/cobalamin | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:Q9Z2Q4` | radical-SAM/cobalamin | `duplicate_external_conflict` | `external_duplicate_accession_or_sequence_conflict` | Resolve external duplicate provenance before any batch approval. |
| `uniprot:P0C264` | near-orphan/no-reliable-structure | `needs_family_policy_review` | `singleton_near_orphan_lane_needs_family_policy_review` | Record family/lane policy before batch import approval. |

## Outputs

- Preflight artifact: `artifacts/v3_external_import_review_preflight_current702_20260609.json`
- Ready preview: `artifacts/v3_external_import_review_ready_preview_current702_20260609.json`
- Repair/conflict queue: `artifacts/v3_external_import_review_repair_queue_current702_20260609.json`
