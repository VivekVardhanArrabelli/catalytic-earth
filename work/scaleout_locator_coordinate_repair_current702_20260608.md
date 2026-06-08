# Scale-out Locator/Coordinate Repair - current702

- Artifact: `artifacts/v3_scaleout_locator_coordinate_repair_current702_20260608.json`
- Created UTC: `2026-06-08T14:27:57Z`
- Automation ID: `ce-expansion-merger-qa`
- STARTED_AT_UTC: `2026-06-08T14:17:14Z`
- STARTED_AT_LOCAL: `2026-06-08T09:17:14-0500`
- Source branch/head: `ce-expansion-merger-qa-20260608` / `fcee1b768934da05f9fc24ac8cc303fe8897b21a`
- Shard artifacts available: `0`
- Merger surface built: `false` (`fewer_than_three_shard_artifacts_available`)

## Repair Summary

- Input conversion rows: `86`
- Input `blocked_locator` rows audited: `7`
- Coordinate files materialized and hash-matched: `7/7`
- Source-free locator sidecars materialized now: `0`
- Mechanical reject/OOS recommendations for future consolidated surface: `1`
- Source-backed locator mapping preflight candidates: `1`
- Remaining locator-blocked recommendations: `6`
- Import-preview rows: `0`

## Row Decisions

| Candidate | Family axis | Coordinate status | External structural signal | Locator preflight | Repair decision | Future surface recommendation | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `uniprot:O60568` | `glycoside_or_nucleoside_hydrolase_controls` | `coordinate_materialized_for_external_screen` | `external_structural_cluster_assigned_no_neighbor_above_threshold; nearest Q9Y5N5 TM 0.4844` | `binding_context_only_active_site_sourcing_required (active=0, binding=13)` | `coordinate_gap_cleared_locator_still_blocked` | `blocked_locator` via `source_free_active_site_locator_not_ready` | source explicit active-site residues or build a source-free locator packet |
| `uniprot:P29372` | `glycoside_or_nucleoside_hydrolase_controls` | `coordinate_materialized_for_external_screen` | `external_structural_cluster_assigned_no_neighbor_above_threshold; nearest Q969G6 TM 0.4322` | `no_active_site_feature_candidate_found (active=0, binding=0)` | `coordinate_gap_cleared_locator_still_blocked` | `blocked_locator` via `source_free_active_site_locator_not_ready` | source explicit active-site residues or build a source-free locator packet |
| `uniprot:P60174` | `glycoside_or_nucleoside_hydrolase_controls` | `coordinate_materialized_for_external_screen` | `external_structural_cluster_assigned_no_neighbor_above_threshold; nearest Q9BXD5 TM 0.6714` | `source_backed_active_site_position_mapping_preflight_candidate (active=2, binding=2)` | `source_backed_locator_mapping_preflight_candidate` | `blocked_locator` via `source_free_active_site_locator_not_ready` | map explicit active-site positions to the candidate structure, then run review-gated locator copy preflight; do not import |
| `uniprot:Q9BXS1` | `glycoside_or_nucleoside_hydrolase_controls` | `coordinate_materialized_for_external_screen` | `external_structural_cluster_neighbor_at_or_above_threshold; nearest Q13907 TM 0.9843` | `terminal_duplicate_repair_supersedes_locator_preflight (active=2, binding=8)` | `mechanical_reject_oos_recommendation` | `reject/OOS_preserve_signal` via `source_free_external_structural_cluster_transitive_current_countable_duplicate` | preserve duplicate/OOS signal; do not retry accession without new evidence |
| `uniprot:Q96I15` | `plp_child_subclasses` | `coordinate_materialized_for_external_screen` | `external_structural_cluster_assigned_no_neighbor_above_threshold; nearest Q9Y5N5 TM 0.5138` | `active_site_feature_singleton_insufficient_for_locator_schema (active=1, binding=0)` | `coordinate_gap_cleared_locator_still_blocked` | `blocked_locator` via `source_free_active_site_locator_not_ready` | source explicit active-site residues or build a source-free locator packet |
| `uniprot:A2RUC4` | `redox_oxygen_transfer_and_sulfur_lipoamide` | `coordinate_materialized_for_external_screen` | `external_structural_cluster_assigned_no_neighbor_above_threshold; nearest P34949 TM 0.4168` | `binding_context_only_active_site_sourcing_required (active=0, binding=6)` | `coordinate_gap_cleared_locator_still_blocked` | `blocked_locator` via `source_free_active_site_locator_not_ready` | source explicit active-site residues or build a source-free locator packet |
| `uniprot:A5PLL7` | `redox_oxygen_transfer_and_sulfur_lipoamide` | `coordinate_materialized_for_external_screen` | `external_structural_cluster_assigned_no_neighbor_above_threshold; nearest P27144 TM 0.3945` | `no_active_site_feature_candidate_found (active=0, binding=0)` | `coordinate_gap_cleared_locator_still_blocked` | `blocked_locator` via `source_free_active_site_locator_not_ready` | source explicit active-site residues or build a source-free locator packet |

## Mechanical Duplicate Repair

- `uniprot:Q9BXS1`: external structural cluster neighbor `uniprot:Q13907` at TM `0.9843`; that neighbor is `reject/OOS_preserve_signal` via `current_countable_structural_duplicate` with current-countable hit `m_csa:190` at TM `0.8686`. Recommendation: preserve as reject/OOS signal in the future consolidated surface, with no import.

## Locator Evidence Preflight

- `uniprot:P60174` has two local active-site feature positions in `artifacts/v3_external_source_active_site_evidence_sample_1025.json`; both map cleanly onto the local AFDB residue table (`96/HIS` and `166/GLU`). A candidate payload is recorded inside the repair JSON, but it is not copied to the audited locator directory and is not scoring-ready.
- `uniprot:Q96I15` has one active-site feature position, below the locator schema minimum of two residue locators.
- `uniprot:O60568` and `uniprot:A2RUC4` have binding-context positions only; these do not clear the active-site locator blocker.
- `uniprot:P29372` and `uniprot:A5PLL7` have no local active-site feature candidate in the sample artifact.
- All seven local AFDB coordinate files are protein-only (`ATOM` records only; no nonstandard ligand/metal components), so the structure-local ligand-contact source-free locator route is not available from these coordinates.
- Feature descriptions, source IDs, EC/Rhea IDs, labels, and source prose were not used as predictive scoring features; no locator sidecar was copied.

## Remaining Locator Queue

| Candidate | Locator status | Label-factory status | Locator preflight status | Remaining blockers |
| --- | --- | --- | --- | --- |
| `uniprot:O60568` | `blocked_locator_active_site_not_sampled` | `terminal_review_blocked_locator_active_site_missing` | `binding_positions_found_no_explicit_active_site_positions` | `active_site_gap_source_request:binding_context_mapped_ready_for_active_site_sourcing`, `active_site_or_locator_evidence_missing`, `broader_duplicate_screening_required`, `explicit_active_site_residue_sources_absent`, `explicit_active_site_residue_sources_not_collected`, `external_active_site_feature_gap`, ... |
| `uniprot:P29372` | `blocked_locator_active_site_not_sampled` | `blocked_by_active_site_sourcing` | `no_local_active_site_or_binding_feature_positions` | `active_site_gap_source_request:reaction_text_only_needs_curated_residue_source`, `active_site_or_locator_evidence_missing`, `explicit_active_site_residue_sources_absent`, `explicit_active_site_residue_sources_not_collected`, `external_active_site_feature_gap`, `external_review_decision_artifact_not_built`, ... |
| `uniprot:P60174` | `blocked_locator_active_site_not_sampled` | `pre_promotion_review_only_or_gate_incomplete` | `candidate_positions_found_mapping_and_review_required` | `active_site_or_locator_evidence_missing`, `active_site_positions_not_mapped_to_candidate_structure`, `external_embeddings_not_computed`, `external_review_decision_artifact_not_built`, `full_label_factory_gate_not_run`, `heuristic_metal_hydrolase_collapse`, ... |
| `uniprot:Q96I15` | `blocked_locator_active_site_not_sampled` | `pre_promotion_review_only_or_gate_incomplete` | `single_position_found_minimum_two_required` | `active_site_or_locator_evidence_missing`, `external_embeddings_not_computed`, `external_review_decision_artifact_not_built`, `full_label_factory_gate_not_run`, `heuristic_metal_hydrolase_collapse`, `heuristic_scope_top1_mismatch`, ... |
| `uniprot:A2RUC4` | `blocked_locator_active_site_not_sampled` | `blocked_by_active_site_sourcing` | `binding_positions_found_no_explicit_active_site_positions` | `active_site_gap_source_request:binding_context_mapped_ready_for_active_site_sourcing`, `active_site_or_locator_evidence_missing`, `explicit_active_site_residue_sources_absent`, `explicit_active_site_residue_sources_not_collected`, `external_active_site_feature_gap`, `external_review_decision_artifact_not_built`, ... |
| `uniprot:A5PLL7` | `blocked_locator_active_site_not_sampled` | `blocked_by_active_site_sourcing` | `no_local_active_site_or_binding_feature_positions` | `active_site_gap_source_request:reaction_text_only_needs_curated_residue_source`, `active_site_or_locator_evidence_missing`, `explicit_active_site_residue_sources_absent`, `explicit_active_site_residue_sources_not_collected`, `external_active_site_feature_gap`, `external_review_decision_artifact_not_built`, ... |

## Family Diversity

| Family axis | Future recommendation counts |
| --- | --- |
| `glycoside_or_nucleoside_hydrolase_controls` | blocked_locator=3, reject/OOS_preserve_signal=1 |
| `plp_child_subclasses` | blocked_locator=1 |
| `redox_oxygen_transfer_and_sulfur_lipoamide` | blocked_locator=2 |

## Guardrails

- No label registry, ontology, split, model, threshold, or production import edit was made.
- No heldout row was used for training/tuning and no mechanism text, EC/Rhea IDs, labels, target names, source IDs, or source prose were used as predictive scoring features.
- Reject/OOS and review-only signal is preserved; this artifact is a future-surface repair recommendation and locator-preflight queue, not a production registry edit.
- Disk available at creation: `10.533` GiB; guardrail above 10 GiB: `True`.

## Validation

- JSON validation passed: `True`
- All seven blocked-locator coordinate files exist and match recorded structural-screen hashes: `True`
- `P60174` source-backed locator mapping preflight recorded: `True`
- `P60174` active-site positions mapped to AFDB residues: `True`
- All local AFDB coordinates are protein-only, with no ligand-contact locator route: `True`
- Existing acquisition conversion artifact was not rewritten.
