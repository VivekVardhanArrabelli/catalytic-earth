# External Admission QA Merger - current702

Merged the completed producer outputs by overlaying the 370-row materialization admission batch onto the 845-row bulk pagination scaleout surface, preserving preview-only guardrails and leaving all production registries, imports, ontologies, heldout splits, thresholds, and model weights untouched.

## Summary

- Merged candidate count: 845
- Import-ready preview count: 333
- Repair queue count: 48
- Blocked duplicate/current702 conflict rows: 33
- Exact current702 conflict rows: 22
- Rows newly added by scaleout vs 20260608 QA surface: 152
- Rows materialized from validated queue: 16
- Rows materialized from provisional queue: 354
- Controlled import-review lane ready: True

## Source Artifact Hashes

- `external_materialization_admission_batch`: `origin/ce-external-materialization-admission-batch-20260608:artifacts/v3_external_materialization_admission_batch_current702_20260608.json` @ `1f61a2dc` (sha256 `ce0cd844c465fcd28181d087f6d807bc90f8b0f47df951572564acca9540f9a6`)
- `external_materialization_import_ready_preview`: `origin/ce-external-materialization-admission-batch-20260608:artifacts/v3_external_materialization_import_ready_preview_current702_20260608.json` @ `1f61a2dc` (sha256 `b771d847359392ccc17c472906b8497012071ebc7b5c1d284f1d8fb2313b926e`)
- `external_bulk_ingestion_scaleout`: `origin/ce-external-bulk-pagination-scaleout-20260609:artifacts/v3_external_bulk_ingestion_scaleout_current702_20260609.json` @ `595c7ac8` (sha256 `3804f45dec32578ddab615abf78a8aadfc6d9591065bcd0ab19a1dbcf23e8592`)
- `external_bulk_ingestion_scaleout_provisional_import_preview`: `origin/ce-external-bulk-pagination-scaleout-20260609:artifacts/v3_external_bulk_ingestion_scaleout_provisional_import_preview_current702_20260609.json` @ `595c7ac8` (sha256 `5d37f102a095ee3dfa1a1bcd7fbc62b186232b60f71938499f0db665b4a43001`)
- `previous_external_admission_qa_surface`: `origin/ce-external-admission-qa-merger-20260608:artifacts/v3_external_admission_merged_surface_current702_20260608.json` @ `cac2d937` (sha256 `41f57a9d8c1f2fa317c3cdeb869b18d49c2530c6d9124666a2800266e0fa969a`)

## Terminal State Counts

| terminal state | count |
| --- | ---: |
| `blocked_duplicate_or_current_registry_conflict` | 33 |
| `coordinate_ready_pending_locator` | 120 |
| `coordinate_repair_candidate` | 3 |
| `hard_blocked_with_next_action` | 2 |
| `import_ready_preview` | 333 |
| `locator_ready_candidate` | 221 |
| `locator_repair_candidate` | 8 |
| `provisional_external_countable_preflight_candidate` | 88 |
| `repairable_locator_blocker` | 37 |

## Lane Counts

| lane | terminal state | count |
| --- | --- | ---: |
| PLP children | `blocked_duplicate_or_current_registry_conflict` | 2 |
| PLP children | `import_ready_preview` | 72 |
| PLP children | `locator_ready_candidate` | 5 |
| PLP children | `provisional_external_countable_preflight_candidate` | 3 |
| PLP children | `repairable_locator_blocker` | 20 |
| adjacent high-yield amidase/deaminase | `locator_ready_candidate` | 1 |
| adjacent high-yield amidase/deaminase | `provisional_external_countable_preflight_candidate` | 11 |
| adjacent high-yield lyase/isomerase | `blocked_duplicate_or_current_registry_conflict` | 1 |
| adjacent high-yield lyase/isomerase | `coordinate_ready_pending_locator` | 1 |
| adjacent high-yield lyase/isomerase | `provisional_external_countable_preflight_candidate` | 12 |
| glycoside/nucleoside | `blocked_duplicate_or_current_registry_conflict` | 6 |
| glycoside/nucleoside | `coordinate_ready_pending_locator` | 32 |
| glycoside/nucleoside | `import_ready_preview` | 43 |
| glycoside/nucleoside | `locator_ready_candidate` | 22 |
| glycoside/nucleoside | `provisional_external_countable_preflight_candidate` | 20 |
| glycoside/nucleoside | `repairable_locator_blocker` | 6 |
| metal hydrolase | `blocked_duplicate_or_current_registry_conflict` | 9 |
| metal hydrolase | `coordinate_ready_pending_locator` | 3 |
| metal hydrolase | `import_ready_preview` | 15 |
| metal hydrolase | `locator_ready_candidate` | 91 |
| metal hydrolase | `provisional_external_countable_preflight_candidate` | 13 |
| metal hydrolase | `repairable_locator_blocker` | 1 |
| near-orphan/no-reliable-structure | `blocked_duplicate_or_current_registry_conflict` | 4 |
| near-orphan/no-reliable-structure | `coordinate_ready_pending_locator` | 67 |
| near-orphan/no-reliable-structure | `hard_blocked_with_next_action` | 2 |
| near-orphan/no-reliable-structure | `import_ready_preview` | 1 |
| near-orphan/no-reliable-structure | `locator_ready_candidate` | 39 |
| near-orphan/no-reliable-structure | `locator_repair_candidate` | 2 |
| phosphoryl transfer | `blocked_duplicate_or_current_registry_conflict` | 3 |
| phosphoryl transfer | `coordinate_ready_pending_locator` | 6 |
| phosphoryl transfer | `import_ready_preview` | 88 |
| phosphoryl transfer | `locator_ready_candidate` | 4 |
| phosphoryl transfer | `locator_repair_candidate` | 1 |
| phosphoryl transfer | `provisional_external_countable_preflight_candidate` | 7 |
| phosphoryl transfer | `repairable_locator_blocker` | 4 |
| radical-SAM/cobalamin | `blocked_duplicate_or_current_registry_conflict` | 3 |
| radical-SAM/cobalamin | `coordinate_ready_pending_locator` | 7 |
| radical-SAM/cobalamin | `coordinate_repair_candidate` | 3 |
| radical-SAM/cobalamin | `import_ready_preview` | 50 |
| radical-SAM/cobalamin | `locator_ready_candidate` | 30 |
| radical-SAM/cobalamin | `provisional_external_countable_preflight_candidate` | 1 |
| radical-SAM/cobalamin | `repairable_locator_blocker` | 5 |
| redox oxygen/sulfur | `blocked_duplicate_or_current_registry_conflict` | 5 |
| redox oxygen/sulfur | `coordinate_ready_pending_locator` | 4 |
| redox oxygen/sulfur | `import_ready_preview` | 64 |
| redox oxygen/sulfur | `locator_ready_candidate` | 29 |
| redox oxygen/sulfur | `locator_repair_candidate` | 5 |
| redox oxygen/sulfur | `provisional_external_countable_preflight_candidate` | 21 |
| redox oxygen/sulfur | `repairable_locator_blocker` | 1 |

## Import Review Readiness

- Import-ready rows have source provenance: `True`
- Import-ready rows clear exact current702 non-overlap: `True`
- Production import authorized here: `False`
- Lane basis: preview-only external import lane is populated with materialized rows that carry source provenance and clear exact current702 non-overlap checks

## Repair Queue

| candidate | lane | terminal state | repair bucket | next action |
| --- | --- | --- | --- | --- |
| `uniprot:Q9BYK8` | metal hydrolase | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:Q8TB37` | redox oxygen/sulfur | `locator_repair_candidate` | `locator_repair` | Repair range/ambiguous locators to exact residue positions before preflight. |
| `uniprot:O60673` | redox oxygen/sulfur | `repairable_locator_blocker` | `locator_repair` | Resolve coordinate-to-sequence residue code mapping or choose an alternate coordinate, then rerun sidecar materialization. |
| `uniprot:Q9Y617` | PLP children | `repairable_locator_blocker` | `locator_repair` | Resolve coordinate-to-sequence residue code mapping or choose an alternate coordinate, then rerun sidecar materialization. |
| `uniprot:Q9Y600` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:Q6ZQY3` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:Q8TBG4` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:Q8IUZ5` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:Q9DBE0` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:Q64611` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:Q10G56` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:Q95ZS2` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:Q9LR30` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:Q9S7E9` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:Q80WP8` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:Q93703` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:P53090` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:P0A9H3` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:P28629` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:P21170` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:P52095` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:Q9LDV4` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:P77434` | PLP children | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:Q04179` | glycoside/nucleoside | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| `uniprot:P06865` | glycoside/nucleoside | `repairable_locator_blocker` | `locator_repair` | Expand to at least two source-free locators via coordinate-local review before any import-ready preview. |
| ... | ... | ... | ... | plus 23 more repair rows |
