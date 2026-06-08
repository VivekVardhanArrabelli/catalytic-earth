# Targeted Expansion Acquisition Conversion Screens

Run: `2026-06-08T13:01:52Z`

Non-importing conversion/screening artifact for the first targeted expansion factory batch. No labels, registries, ontologies, splits, model weights, thresholds, or imports were changed.

## Summary

- Acquisition rows screened: `86`
- Priority screen-ready rows: `16`
- Expanded non-priority rows: `70`
- Validation passed: `True`

## Terminal States

- `review_only_evidence`: 1
- `reject/OOS_preserve_signal`: 27
- `blocked_locator`: 7
- `blocked_coordinate`: 0
- `blocked_family_decision`: 50
- `countable_candidate_preflight_only`: 1

## Priority Rows

- `countable_candidate_preflight_only`: 1
- `reject/OOS_preserve_signal`: 14
- `review_only_evidence`: 1

## Priority Row Outcome Matrix

| Candidate | Terminal state | Current-reference sequence | Current-countable structure | Broad sequence | Route basis |
| --- | --- | --- | --- | --- | --- |
| `uniprot:P04424` | `reject/OOS_preserve_signal` | `no_near_duplicate_signal` | `current_countable_structural_duplicate_signal` | `not_available` | `current_countable_structural_duplicate` |
| `uniprot:P22830` | `reject/OOS_preserve_signal` | `exact_reference_or_sequence_holdout` | `no_current_countable_structural_duplicate_signal` | `targeted_uniref_current_reference_no_overlap` | `current_reference_sequence_duplicate_or_holdout` |
| `uniprot:P30566` | `reject/OOS_preserve_signal` | `no_near_duplicate_signal` | `current_countable_structural_duplicate_signal` | `not_available` | `current_countable_structural_duplicate` |
| `uniprot:P78549` | `countable_candidate_preflight_only` | `no_near_duplicate_signal` | `no_current_countable_structural_duplicate_signal` | `targeted_uniref_current_reference_no_overlap` | `factory_preflight_passed_import_not_performed` |
| `uniprot:Q04760` | `reject/OOS_preserve_signal` | `exact_reference_or_sequence_holdout` | `not_available` | `not_available` | `current_reference_sequence_duplicate_or_holdout` |
| `uniprot:Q13087` | `reject/OOS_preserve_signal` | `no_near_duplicate_signal` | `current_countable_structural_duplicate_signal` | `not_available` | `current_countable_structural_duplicate` |
| `uniprot:Q3LXA3` | `review_only_evidence` | `no_near_duplicate_signal` | `no_current_countable_structural_duplicate_signal` | `targeted_uniref_current_reference_no_overlap` | `screened_review_only_no_promotion_authority` |
| `uniprot:Q8N0X4` | `reject/OOS_preserve_signal` | `no_near_duplicate_signal` | `current_countable_structural_duplicate_signal` | `not_available` | `current_countable_structural_duplicate` |
| `uniprot:Q8TB92` | `reject/OOS_preserve_signal` | `no_near_duplicate_signal` | `current_countable_structural_duplicate_signal` | `external_all_vs_all_no_near_duplicate_signal` | `current_countable_structural_duplicate` |
| `uniprot:Q9GZT4` | `reject/OOS_preserve_signal` | `no_near_duplicate_signal` | `current_countable_structural_duplicate_signal` | `external_all_vs_all_no_near_duplicate_signal` | `current_countable_structural_duplicate` |
| `uniprot:O75828` | `reject/OOS_preserve_signal` | `no_near_duplicate_signal` | `current_countable_structural_duplicate_signal` | `not_available` | `current_countable_structural_duplicate` |
| `uniprot:O95154` | `reject/OOS_preserve_signal` | `no_near_duplicate_signal` | `current_countable_structural_duplicate_signal` | `not_available` | `current_countable_structural_duplicate` |
| `uniprot:O95479` | `reject/OOS_preserve_signal` | `no_near_duplicate_signal` | `current_countable_structural_duplicate_signal` | `not_available` | `current_countable_structural_duplicate` |
| `uniprot:P00338` | `reject/OOS_preserve_signal` | `no_near_duplicate_signal` | `current_countable_structural_duplicate_signal` | `external_all_vs_all_no_near_duplicate_signal` | `current_countable_structural_duplicate` |
| `uniprot:P04406` | `reject/OOS_preserve_signal` | `no_near_duplicate_signal` | `current_countable_structural_duplicate_signal` | `external_all_vs_all_no_near_duplicate_signal` | `current_countable_structural_duplicate` |
| `uniprot:P14060` | `reject/OOS_preserve_signal` | `no_near_duplicate_signal` | `current_countable_structural_duplicate_signal` | `external_all_vs_all_no_near_duplicate_signal` | `current_countable_structural_duplicate` |

## Family Routing

| Family axis | Terminal mix |
| --- | --- |
| `glycoside_or_nucleoside_hydrolase_controls` | blocked_family_decision=1, blocked_locator=4, reject/OOS_preserve_signal=6 |
| `near_orphan_or_unrepresented_mechanism_tail` | blocked_family_decision=24, countable_candidate_preflight_only=1, reject/OOS_preserve_signal=11, review_only_evidence=1 |
| `phosphoryl_transfer_boundary` | blocked_family_decision=24, reject/OOS_preserve_signal=1 |
| `plp_child_subclasses` | blocked_locator=1, reject/OOS_preserve_signal=1 |
| `redox_oxygen_transfer_and_sulfur_lipoamide` | blocked_family_decision=1, blocked_locator=2, reject/OOS_preserve_signal=8 |

## Screen Axis Coverage

| Axis | Status mix |
| --- | --- |
| `current_reference_sequence_duplicate_screen` | exact_reference_or_sequence_holdout=5, no_exact_current_reference_accession_proxy=39, no_near_duplicate_signal=42 |
| `current_countable_structural_screen` | current_countable_structural_duplicate_signal=15, no_current_countable_structural_duplicate_signal=3, not_available=68 |
| `external_all_vs_all_structural_cluster_assignment` | external_structural_cluster_assigned_no_neighbor_above_threshold=38, external_structural_cluster_neighbor_at_or_above_threshold=8, not_available=40 |
| `broad_sequence_neighborhood_duplicate_screen` | broad_sequence_near_duplicate_or_holdout=2, external_all_vs_all_no_near_duplicate_signal=33, not_available=48, targeted_uniref_current_reference_no_overlap=3 |
| `locator_coordinate_readiness` | blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen=30, blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending=40, source_free_locator_ready_explicit_active_site_source\|coordinate_materialized_for_external_screen=16 |
| `label_factory_pre_promotion_readiness` | blocked_by_active_site_sourcing=7, countable_candidate_preflight_passed_import_not_performed=1, not_available=41, pre_promotion_review_only_or_gate_incomplete=27, terminal_review_blocked_locator_active_site_missing=3, terminal_review_reject_or_oos_preserve_signal=7 |

## Countable Preflight Only

- `uniprot:P78549` via `near_orphan_or_unrepresented_mechanism_tail`: factory preflight/import-ready evidence exists, but no import was performed.

## Remaining Blockers

- `blocked_locator`: 7
  - `uniprot:O60568`: source explicit active-site residues or build a source-free locator packet
  - `uniprot:P29372`: source explicit active-site residues or build a source-free locator packet
  - `uniprot:P60174`: source explicit active-site residues or build a source-free locator packet
  - `uniprot:Q9BXS1`: source explicit active-site residues or build a source-free locator packet
  - `uniprot:Q96I15`: source explicit active-site residues or build a source-free locator packet
  - `uniprot:A2RUC4`: source explicit active-site residues or build a source-free locator packet
  - `uniprot:A5PLL7`: source explicit active-site residues or build a source-free locator packet
- `blocked_coordinate`: 0
- `blocked_family_decision`: 50
  - `uniprot:P30176`: resolve the family/lane decision before promotion or import discussion
  - `uniprot:A6NJ78`: resolve the family/lane decision before promotion or import discussion
  - `uniprot:O95050`: resolve the family/lane decision before promotion or import discussion
  - `uniprot:P40261`: resolve the family/lane decision before promotion or import discussion
  - `uniprot:P46597`: resolve the family/lane decision before promotion or import discussion
  - `uniprot:P51580`: resolve the family/lane decision before promotion or import discussion
  - `uniprot:Q32P41`: resolve the family/lane decision before promotion or import discussion
  - `uniprot:Q5JPI9`: resolve the family/lane decision before promotion or import discussion
  - `uniprot:Q5T8I9`: resolve the family/lane decision before promotion or import discussion
  - `uniprot:Q5VZV1`: resolve the family/lane decision before promotion or import discussion
  - `uniprot:Q6UX53`: resolve the family/lane decision before promotion or import discussion
  - `uniprot:Q86X55`: resolve the family/lane decision before promotion or import discussion
  - ... 38 more

## Locator Blocker Queue

| Family axis | Candidate | Current-reference sequence | Structure | Locator/coordinate |
| --- | --- | --- | --- | --- |
| `glycoside_or_nucleoside_hydrolase_controls` | `uniprot:O60568` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `glycoside_or_nucleoside_hydrolase_controls` | `uniprot:P29372` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `glycoside_or_nucleoside_hydrolase_controls` | `uniprot:P60174` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `glycoside_or_nucleoside_hydrolase_controls` | `uniprot:Q9BXS1` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `plp_child_subclasses` | `uniprot:Q96I15` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `redox_oxygen_transfer_and_sulfur_lipoamide` | `uniprot:A2RUC4` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `redox_oxygen_transfer_and_sulfur_lipoamide` | `uniprot:A5PLL7` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |

## Family Decision Blocker Queue

| Family axis | Candidate | Current-reference sequence | Structure | Locator/coordinate |
| --- | --- | --- | --- | --- |
| `glycoside_or_nucleoside_hydrolase_controls` | `uniprot:P30176` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:A6NJ78` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:O95050` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:P40261` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:P46597` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:P51580` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q32P41` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q5JPI9` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q5T8I9` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q5VZV1` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q6UX53` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q86X55` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q86XA0` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q8N4J0` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q8N6R0` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q8WZ04` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q9H2M3` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q9H867` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q9H8H3` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q9HBK9` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q9NZJ6` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q9UBM1` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q9UBP6` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q9UIC8` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `near_orphan_or_unrepresented_mechanism_tail` | `uniprot:Q9Y5N5` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `phosphoryl_transfer_boundary` | `uniprot:A2RU49` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `phosphoryl_transfer_boundary` | `uniprot:O43252` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:O95340` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:O95819` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:P00568` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:P0A7B1` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:P20485` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:P27144` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `phosphoryl_transfer_boundary` | `uniprot:P32189` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `phosphoryl_transfer_boundary` | `uniprot:P54819` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:Q12851` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:Q13233` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:Q14410` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:Q16774` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:Q3T906` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:Q5TCX8` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:Q8IVH8` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:Q8N4C8` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:Q92918` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:Q969G6` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |
| `phosphoryl_transfer_boundary` | `uniprot:Q99759` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:Q9UIJ7` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:Q9Y4K4` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `phosphoryl_transfer_boundary` | `uniprot:Q9Y6R4` | `no_exact_current_reference_accession_proxy` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_provenance_ready_materialization_pending` |
| `redox_oxygen_transfer_and_sulfur_lipoamide` | `uniprot:O15247` | `no_near_duplicate_signal` | `not_available` | `blocked_locator_active_site_not_sampled\|coordinate_materialized_for_external_screen` |

## Representative Converted Rows

| Candidate | Family axis | Terminal state | Route basis |
| --- | --- | --- | --- |
| `uniprot:P04424` | `near_orphan_or_unrepresented_mechanism_tail` | `reject/OOS_preserve_signal` | `current_countable_structural_duplicate` |
| `uniprot:P22830` | `near_orphan_or_unrepresented_mechanism_tail` | `reject/OOS_preserve_signal` | `current_reference_sequence_duplicate_or_holdout` |
| `uniprot:P30566` | `near_orphan_or_unrepresented_mechanism_tail` | `reject/OOS_preserve_signal` | `current_countable_structural_duplicate` |
| `uniprot:P78549` | `near_orphan_or_unrepresented_mechanism_tail` | `countable_candidate_preflight_only` | `factory_preflight_passed_import_not_performed` |
| `uniprot:Q04760` | `near_orphan_or_unrepresented_mechanism_tail` | `reject/OOS_preserve_signal` | `current_reference_sequence_duplicate_or_holdout` |
| `uniprot:Q13087` | `near_orphan_or_unrepresented_mechanism_tail` | `reject/OOS_preserve_signal` | `current_countable_structural_duplicate` |
| `uniprot:Q3LXA3` | `near_orphan_or_unrepresented_mechanism_tail` | `review_only_evidence` | `screened_review_only_no_promotion_authority` |
| `uniprot:Q8N0X4` | `near_orphan_or_unrepresented_mechanism_tail` | `reject/OOS_preserve_signal` | `current_countable_structural_duplicate` |
| `uniprot:Q8TB92` | `near_orphan_or_unrepresented_mechanism_tail` | `reject/OOS_preserve_signal` | `current_countable_structural_duplicate` |
| `uniprot:Q9GZT4` | `near_orphan_or_unrepresented_mechanism_tail` | `reject/OOS_preserve_signal` | `current_countable_structural_duplicate` |
| `uniprot:O75828` | `redox_oxygen_transfer_and_sulfur_lipoamide` | `reject/OOS_preserve_signal` | `current_countable_structural_duplicate` |
| `uniprot:O95154` | `redox_oxygen_transfer_and_sulfur_lipoamide` | `reject/OOS_preserve_signal` | `current_countable_structural_duplicate` |
| `uniprot:O95479` | `redox_oxygen_transfer_and_sulfur_lipoamide` | `reject/OOS_preserve_signal` | `current_countable_structural_duplicate` |
| `uniprot:P00338` | `redox_oxygen_transfer_and_sulfur_lipoamide` | `reject/OOS_preserve_signal` | `current_countable_structural_duplicate` |
| `uniprot:P04406` | `redox_oxygen_transfer_and_sulfur_lipoamide` | `reject/OOS_preserve_signal` | `current_countable_structural_duplicate` |
| `uniprot:P14060` | `redox_oxygen_transfer_and_sulfur_lipoamide` | `reject/OOS_preserve_signal` | `current_countable_structural_duplicate` |
| `uniprot:O15527` | `glycoside_or_nucleoside_hydrolase_controls` | `reject/OOS_preserve_signal` | `current_reference_sequence_duplicate_or_holdout` |
| `uniprot:O60568` | `glycoside_or_nucleoside_hydrolase_controls` | `blocked_locator` | `source_free_active_site_locator_not_ready` |
| `uniprot:P06746` | `glycoside_or_nucleoside_hydrolase_controls` | `reject/OOS_preserve_signal` | `terminal_review_reject_or_oos` |
| `uniprot:P29372` | `glycoside_or_nucleoside_hydrolase_controls` | `blocked_locator` | `source_free_active_site_locator_not_ready` |
| `uniprot:P30176` | `glycoside_or_nucleoside_hydrolase_controls` | `blocked_family_decision` | `source_context_or_family_lane_decision_required` |
| `uniprot:P33025` | `glycoside_or_nucleoside_hydrolase_controls` | `reject/OOS_preserve_signal` | `current_countable_structural_duplicate` |
| `uniprot:P34949` | `glycoside_or_nucleoside_hydrolase_controls` | `reject/OOS_preserve_signal` | `terminal_review_reject_or_oos` |
| `uniprot:P60174` | `glycoside_or_nucleoside_hydrolase_controls` | `blocked_locator` | `source_free_active_site_locator_not_ready` |
| `uniprot:Q13907` | `glycoside_or_nucleoside_hydrolase_controls` | `reject/OOS_preserve_signal` | `current_countable_structural_duplicate` |
| `uniprot:Q6NSJ0` | `glycoside_or_nucleoside_hydrolase_controls` | `reject/OOS_preserve_signal` | `terminal_review_reject_or_oos` |
| `uniprot:Q9BXS1` | `glycoside_or_nucleoside_hydrolase_controls` | `blocked_locator` | `source_free_active_site_locator_not_ready` |
| `uniprot:A6NJ78` | `near_orphan_or_unrepresented_mechanism_tail` | `blocked_family_decision` | `source_context_or_family_lane_decision_required` |
| `uniprot:O95050` | `near_orphan_or_unrepresented_mechanism_tail` | `blocked_family_decision` | `source_context_or_family_lane_decision_required` |
| `uniprot:P11086` | `near_orphan_or_unrepresented_mechanism_tail` | `reject/OOS_preserve_signal` | `current_reference_sequence_duplicate_or_holdout` |
| `uniprot:P35914` | `near_orphan_or_unrepresented_mechanism_tail` | `reject/OOS_preserve_signal` | `current_countable_structural_duplicate` |
| `uniprot:P40261` | `near_orphan_or_unrepresented_mechanism_tail` | `blocked_family_decision` | `source_context_or_family_lane_decision_required` |
| `uniprot:P42126` | `near_orphan_or_unrepresented_mechanism_tail` | `reject/OOS_preserve_signal` | `current_reference_sequence_duplicate_or_holdout` |
| `uniprot:P46597` | `near_orphan_or_unrepresented_mechanism_tail` | `blocked_family_decision` | `source_context_or_family_lane_decision_required` |
| `uniprot:P51580` | `near_orphan_or_unrepresented_mechanism_tail` | `blocked_family_decision` | `source_context_or_family_lane_decision_required` |
| `uniprot:Q32P41` | `near_orphan_or_unrepresented_mechanism_tail` | `blocked_family_decision` | `source_context_or_family_lane_decision_required` |
| `uniprot:Q5JPI9` | `near_orphan_or_unrepresented_mechanism_tail` | `blocked_family_decision` | `source_context_or_family_lane_decision_required` |
| `uniprot:Q5T8I9` | `near_orphan_or_unrepresented_mechanism_tail` | `blocked_family_decision` | `source_context_or_family_lane_decision_required` |
| `uniprot:Q5VZV1` | `near_orphan_or_unrepresented_mechanism_tail` | `blocked_family_decision` | `source_context_or_family_lane_decision_required` |
| `uniprot:Q6UX53` | `near_orphan_or_unrepresented_mechanism_tail` | `blocked_family_decision` | `source_context_or_family_lane_decision_required` |

## Controlled Promotion Recommendation

Do not import or promote labels from this artifact automatically. The next controlled action is human review of the preflight-only and review-only rows, with duplicate/OOS rows preserved as non-counting evidence and blocker rows repaired mechanically first.
