# External Admission QA Merger - current702

Merged the durable external admission surfaces by upgrading the 16-row validated admission slice over the bulk scout baseline, auditing provenance/hash continuity, and separating repairable rows into an explicit queue without touching production registries or final import files.

## Summary

- Merged rows: 693
- Validation upgrades: 16
- Bulk-only rows: 677
- Import-ready preview rows: 0
- Repair-queue rows: 23
- Scaleout-overlap audit rows: 119
- Validation passed: True

## Producer Watch

- `ce-external-materialization-admission-batch`: `missing_in_current_main_state` (0 artifact(s))
- `ce-external-bulk-pagination-scaleout`: `missing_in_current_main_state` (0 artifact(s))

## Terminal State Counts

| terminal state | count |
| --- | ---: |
| `admission_ready_pending_coordinate_materialization` | 10 |
| `admission_ready_pending_locator_materialization` | 6 |
| `blocked_duplicate_or_current_registry_conflict` | 23 |
| `coordinate_ready_pending_locator` | 97 |
| `coordinate_repair_candidate` | 3 |
| `hard_blocked_with_next_action` | 2 |
| `locator_ready_candidate` | 194 |
| `locator_repair_candidate` | 4 |
| `provisional_external_countable_preflight_candidate` | 354 |

## Lane Counts

| family/lane | terminal state | count |
| --- | --- | ---: |
| PLP children | `admission_ready_pending_locator_materialization` | 3 |
| PLP children | `blocked_duplicate_or_current_registry_conflict` | 2 |
| PLP children | `locator_ready_candidate` | 5 |
| PLP children | `provisional_external_countable_preflight_candidate` | 89 |
| glycoside/nucleoside | `admission_ready_pending_coordinate_materialization` | 1 |
| glycoside/nucleoside | `admission_ready_pending_locator_materialization` | 1 |
| glycoside/nucleoside | `blocked_duplicate_or_current_registry_conflict` | 3 |
| glycoside/nucleoside | `coordinate_ready_pending_locator` | 28 |
| glycoside/nucleoside | `locator_ready_candidate` | 17 |
| glycoside/nucleoside | `provisional_external_countable_preflight_candidate` | 47 |
| metal hydrolase | `blocked_duplicate_or_current_registry_conflict` | 6 |
| metal hydrolase | `coordinate_ready_pending_locator` | 1 |
| metal hydrolase | `locator_ready_candidate` | 77 |
| metal hydrolase | `provisional_external_countable_preflight_candidate` | 16 |
| near-orphan/no-reliable-structure | `blocked_duplicate_or_current_registry_conflict` | 4 |
| near-orphan/no-reliable-structure | `coordinate_ready_pending_locator` | 53 |
| near-orphan/no-reliable-structure | `hard_blocked_with_next_action` | 2 |
| near-orphan/no-reliable-structure | `locator_ready_candidate` | 38 |
| near-orphan/no-reliable-structure | `locator_repair_candidate` | 2 |
| near-orphan/no-reliable-structure | `provisional_external_countable_preflight_candidate` | 1 |
| phosphoryl transfer | `admission_ready_pending_coordinate_materialization` | 2 |
| phosphoryl transfer | `admission_ready_pending_locator_materialization` | 2 |
| phosphoryl transfer | `blocked_duplicate_or_current_registry_conflict` | 2 |
| phosphoryl transfer | `coordinate_ready_pending_locator` | 5 |
| phosphoryl transfer | `locator_repair_candidate` | 1 |
| phosphoryl transfer | `provisional_external_countable_preflight_candidate` | 88 |
| radical-SAM/cobalamin | `admission_ready_pending_coordinate_materialization` | 3 |
| radical-SAM/cobalamin | `blocked_duplicate_or_current_registry_conflict` | 3 |
| radical-SAM/cobalamin | `coordinate_ready_pending_locator` | 7 |
| radical-SAM/cobalamin | `coordinate_repair_candidate` | 3 |
| radical-SAM/cobalamin | `locator_ready_candidate` | 29 |
| radical-SAM/cobalamin | `provisional_external_countable_preflight_candidate` | 52 |
| redox oxygen/sulfur | `admission_ready_pending_coordinate_materialization` | 4 |
| redox oxygen/sulfur | `blocked_duplicate_or_current_registry_conflict` | 3 |
| redox oxygen/sulfur | `coordinate_ready_pending_locator` | 3 |
| redox oxygen/sulfur | `locator_ready_candidate` | 28 |
| redox oxygen/sulfur | `locator_repair_candidate` | 1 |
| redox oxygen/sulfur | `provisional_external_countable_preflight_candidate` | 61 |

## Import-Ready Preview

- Candidate rows: `0`
- No row is import-ready yet. The validated rows still need coordinate and/or locator materialization, and bulk-only rows still need scaled admission validation plus downstream duplicate and review gates.

## Repair Queue

| candidate | lane | terminal state | repair bucket | next action |
| --- | --- | --- | --- | --- |
| `uniprot:Q8TB37` | redox oxygen/sulfur | `locator_repair_candidate` | `locator_repair` | Repair range/ambiguous locators to exact residue positions before preflight. |
| `uniprot:P09601` | redox oxygen/sulfur | `admission_ready_pending_coordinate_materialization` | `coordinate_materialization` |  |
| `uniprot:P30519` | redox oxygen/sulfur | `admission_ready_pending_coordinate_materialization` | `coordinate_materialization` |  |
| `uniprot:P29082` | redox oxygen/sulfur | `admission_ready_pending_coordinate_materialization` | `coordinate_materialization` |  |
| `uniprot:Q9UGB7` | redox oxygen/sulfur | `admission_ready_pending_coordinate_materialization` | `coordinate_materialization` |  |
| `uniprot:Q9Y617` | PLP children | `admission_ready_pending_locator_materialization` | `locator_materialization` |  |
| `uniprot:P04181` | PLP children | `admission_ready_pending_locator_materialization` | `locator_materialization` |  |
| `uniprot:Q96255` | PLP children | `admission_ready_pending_locator_materialization` | `locator_materialization` |  |
| `uniprot:P04062` | glycoside/nucleoside | `admission_ready_pending_locator_materialization` | `locator_materialization` |  |
| `uniprot:O60502` | glycoside/nucleoside | `admission_ready_pending_coordinate_materialization` | `coordinate_materialization` |  |
| `uniprot:Q969G6` | phosphoryl transfer | `admission_ready_pending_locator_materialization` | `locator_materialization` |  |
| `uniprot:P32189` | phosphoryl transfer | `admission_ready_pending_locator_materialization` | `locator_materialization` |  |
| `uniprot:Q3T906` | phosphoryl transfer | `admission_ready_pending_coordinate_materialization` | `coordinate_materialization` |  |
| `uniprot:Q9Y6K0` | phosphoryl transfer | `admission_ready_pending_coordinate_materialization` | `coordinate_materialization` |  |
| `uniprot:Q96PC2` | phosphoryl transfer | `locator_repair_candidate` | `locator_repair` | Repair range/ambiguous locators to exact residue positions before preflight. |
| `uniprot:Q99707` | radical-SAM/cobalamin | `admission_ready_pending_coordinate_materialization` | `coordinate_materialization` |  |
| `uniprot:A6H5Y3` | radical-SAM/cobalamin | `admission_ready_pending_coordinate_materialization` | `coordinate_materialization` |  |
| `uniprot:Q9Z2Q4` | radical-SAM/cobalamin | `admission_ready_pending_coordinate_materialization` | `coordinate_materialization` |  |
| `uniprot:Q9JLB4` | radical-SAM/cobalamin | `coordinate_repair_candidate` | `coordinate_repair` | Find AFDB/PDB or alternate coordinate provenance for the exact locators. |
| `uniprot:O70244` | radical-SAM/cobalamin | `coordinate_repair_candidate` | `coordinate_repair` | Find AFDB/PDB or alternate coordinate provenance for the exact locators. |
| `uniprot:F1RWC3` | radical-SAM/cobalamin | `coordinate_repair_candidate` | `coordinate_repair` | Find AFDB/PDB or alternate coordinate provenance for the exact locators. |
| `uniprot:P43610` | near-orphan/no-reliable-structure | `locator_repair_candidate` | `locator_repair` | Repair range/ambiguous locators to exact residue positions before preflight. |
| `uniprot:O94387` | near-orphan/no-reliable-structure | `locator_repair_candidate` | `locator_repair` | Repair range/ambiguous locators to exact residue positions before preflight. |
