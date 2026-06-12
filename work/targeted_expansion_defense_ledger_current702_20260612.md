# Targeted Expansion Defense Ledger - current702

Created UTC: `2026-06-12T20:14:14Z`

This ledger refreshes the targeted expansion review story after the Wave 2 import-review preflight. It is not an import artifact.

## Count Ledger

| surface | count | note |
| --- | ---: | --- |
| Current countable labels | 702 | Frozen current702 benchmark reference; unchanged by this packet. |
| Wave 2 review surface | 12495 | 600 preview rows plus 11,895 repair-surface rows. |
| Controlled import-review ready | 275 | Can move together after one final controlled batch approval. |
| Blocked rows remaining | 12220 | Routed to concrete duplicate, locator, coordinate, OOS, structural, or hard-blocker gates. |
| Projected count after approval | 977 | Projection only; no import performed here. |

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

## Family And Lane Rationale

| family/lane | why targeted | current Wave 2 ready rows | current Wave 2 rows |
| --- | --- | ---: | ---: |
| `metal_hydrolase` | Metal coordination and hydrolase-like folds are a known cofactor/fold confounding axis; the atlas needs subclass breadth and hard duplicate screens rather than one broad metal bucket. | 110 | 1610 |
| `redox oxygen/sulfur` | Predicted geometry failure analysis showed missing cofactor context can dominate deployment loss; oxygen/sulfur redox lanes are the clearest place to test cofactor reconstruction and electron-flow guardrails. | 47 | 810 |
| `PLP children` | PLP mechanism children are useful only if the ledger keeps child mechanisms separate from broad PLP family evidence and locator gaps. | 6 | 102 |
| `radical-SAM/cobalamin` | Radical-SAM and cobalamin were secondary/OOD probes and cofactor-locus sidecars; they stress active-site cofactor evidence, not just fold similarity. | 27 | 121 |
| `glycoside/nucleoside` | This lane supplies hydrolase controls, carbohydrate/nucleoside boundary rows, and source-free locator pressure from prior external glycoside panels. | 39 | 554 |
| `phosphoryl transfer` | Earlier ePK and ATP/substrate-role work showed phosphorylation-like rows are especially vulnerable to ligand/protein-substrate confounding. | 8 | 1064 |
| `near-orphan/no-reliable-structure` | Near-orphan and no-reliable-structure rows are the explicit atlas-growth lane for mechanisms not well represented in current702. | 27 | 350 |
| `adjacent high-yield amidase/deaminase` | The pagination scaleout added high-yield adjacent external lanes to test whether the Swiss-Prot/AFDB/Rhea pattern can broaden without becoming random. | 0 | 12 |
| `adjacent high-yield lyase/isomerase` | This external-only lane tests adjacent mechanism space while keeping exact current702 conflicts and coordinate/locator blockers visible. | 10 | 14 |
| `glycoside hydrolase` | Wave 2 preflight found machine-clean, source-provenanced rows in this lane after duplicate, locator, and coordinate checks. | 1 | 179 |

## Guardrails

- `label_import_performed`: `False`
- `production_registry_edited`: `False`
- `final_import_files_edited`: `False`
- `ontology_edited`: `False`
- `heldout_splits_edited`: `False`
- `production_thresholds_edited`: `False`
- `model_weights_edited`: `False`
- `preview_not_import`: `True`
- `source_free_coordinate_locator_requirements_preserved`: `True`

## Review Narrative

### Honest Claims

- Current main has a full Wave 2 materialization/preflight surface of 12,495 unique external candidates.
- 275 rows are machine-clean for one controlled batch approval; they are not imported by this artifact.
- The selected lanes are targeted by prior mechanism failure modes and by lane-specific duplicate/locator/coordinate gates, not random sampling.

### Still Preview Or Provisional

- Production import still requires an explicit controlled batch approval, label-factory gate, and registry-change authorization.
- 12220 rows remain blocked behind concrete mechanical or policy gates.
- Exact coordinate/structure-ID screening is not a full Foldseek/TM structural duplicate screen.

## Validation

- `preflight_validation_passed`: `True`
- `approval_packet_validation_passed`: `True`
- `terminal_counts_reconcile`: `True`
- `batch_ready_count_matches_preflight`: `True`
- `family_rationale_present`: `True`
- `passed`: `True`
