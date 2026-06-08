# Targeted Expansion Factory Batch

Run: `2026-06-08T04:21:01Z`

Non-importing targeted expansion artifact. No labels, registries, ontologies, splits, model weights, production thresholds, or imports were changed.

## Summary

- Status: `target_volume_reached`
- Candidate rows: `816`
- Exact-one-state audit: `True`

## Admission Counts

- `countable_candidate`: 0
- `review_only_evidence`: 391
- `reject/OOS_preserve_signal`: 205
- `blocked_locator`: 90
- `blocked_coordinate`: 44
- `blocked_family_decision`: 0
- `acquisition_needed`: 86

## Family Axes

| Family axis | Candidates | Admission mix |
| --- | ---: | --- |
| `glycoside_or_nucleoside_hydrolase_controls` | 80 | acquisition_needed=11, blocked_coordinate=12, blocked_locator=7, reject/OOS_preserve_signal=42, review_only_evidence=8 |
| `metal_hydrolase_subclasses` | 394 | blocked_coordinate=10, blocked_locator=34, reject/OOS_preserve_signal=97, review_only_evidence=253 |
| `near_orphan_or_unrepresented_mechanism_tail` | 43 | acquisition_needed=37, reject/OOS_preserve_signal=3, review_only_evidence=3 |
| `no_reliable_structure_or_locator_gap` | 23 | blocked_coordinate=4, blocked_locator=19 |
| `phosphoryl_transfer_boundary` | 25 | acquisition_needed=25 |
| `plp_child_subclasses` | 56 | acquisition_needed=2, blocked_coordinate=2, blocked_locator=4, reject/OOS_preserve_signal=15, review_only_evidence=33 |
| `radical_cobalamin_sam_like_probes` | 22 | blocked_coordinate=2, reject/OOS_preserve_signal=9, review_only_evidence=11 |
| `redox_oxygen_transfer_and_sulfur_lipoamide` | 173 | acquisition_needed=11, blocked_coordinate=14, blocked_locator=26, reject/OOS_preserve_signal=39, review_only_evidence=83 |

## Source Counts

- `active_learning_1025_preview`: 436
- `architecture_default_decisions`: 6
- `coordinate_readiness_1000`: 213
- `external_hard_negative_new_sourcing`: 71
- `external_hard_negative_next_sourcing`: 139
- `external_panel_router_queue`: 273
- `label_expansion_candidates_1025`: 324
- `local_evidence_gap_audit_1025`: 93

## Evidence Coverage

- `candidate_rows`: 816
- `coordinate_or_structure_provenance_available`: 676
- `active_site_or_locator_evidence_present`: 470
- `cofactor_or_metal_evidence_present`: 681
- `fold_or_near_neighbor_signal_present`: 537
- `row_context_hash_present`: 816
- `source_hashes_present`: 816

## Validation Checks

- Passed: `True`
- `candidate_volume_within_requested_bounds`: True
- `required_row_fields_present`: True
- `row_source_hashes_match_declared_sources`: True
- `all_rows_have_source_hashes`: True
- `all_rows_have_row_context_hashes`: True
- `row_context_hashes_recompute`: True
- `forbidden_raw_predictive_fields_absent`: True

## Architecture Defaults Reused

- Expected default rows: `6`
- Present default rows: `6`
- Default row states:
  - `reject/OOS_preserve_signal`: 4
  - `review_only_evidence`: 2
- Default row IDs:
  - `m_csa:10`: `reject/OOS_preserve_signal` via `glycoside_or_nucleoside_hydrolase_controls`
  - `m_csa:191`: `reject/OOS_preserve_signal` via `redox_oxygen_transfer_and_sulfur_lipoamide`
  - `m_csa:30`: `reject/OOS_preserve_signal` via `radical_cobalamin_sam_like_probes`
  - `m_csa:31`: `reject/OOS_preserve_signal` via `radical_cobalamin_sam_like_probes`
  - `m_csa:448`: `review_only_evidence` via `redox_oxygen_transfer_and_sulfur_lipoamide`
  - `m_csa:973`: `review_only_evidence` via `redox_oxygen_transfer_and_sulfur_lipoamide`

## Blockers And Acquisition

- Target floor gap: `0`
- Acquisition-needed rows: `86`
- Acquisition rows with explicit screen lists: `16`
- Acquisition rows missing explicit screen lists: `70`
- Locator/coordinate blocked rows: `134`
- Required screen counts:
  - `current_countable_foldseek_structural_screen`: 16
  - `current_reference_backend_sequence_search`: 16
  - `external_all_vs_all_structural_cluster_assignment`: 16
  - `full_label_factory_gate`: 16
  - `terminal_review_decision`: 16
  - `uniref_wide_duplicate_screening`: 16
- Screen-ready acquisition rows:
  - `uniprot:P04424` via `near_orphan_or_unrepresented_mechanism_tail`
  - `uniprot:P22830` via `near_orphan_or_unrepresented_mechanism_tail`
  - `uniprot:P30566` via `near_orphan_or_unrepresented_mechanism_tail`
  - `uniprot:P78549` via `near_orphan_or_unrepresented_mechanism_tail`
  - `uniprot:Q04760` via `near_orphan_or_unrepresented_mechanism_tail`
  - `uniprot:Q13087` via `near_orphan_or_unrepresented_mechanism_tail`
  - `uniprot:Q3LXA3` via `near_orphan_or_unrepresented_mechanism_tail`
  - `uniprot:Q8N0X4` via `near_orphan_or_unrepresented_mechanism_tail`
  - `uniprot:Q8TB92` via `near_orphan_or_unrepresented_mechanism_tail`
  - `uniprot:Q9GZT4` via `near_orphan_or_unrepresented_mechanism_tail`
  - `uniprot:O75828` via `redox_oxygen_transfer_and_sulfur_lipoamide`
  - `uniprot:O95154` via `redox_oxygen_transfer_and_sulfur_lipoamide`
  - `uniprot:O95479` via `redox_oxygen_transfer_and_sulfur_lipoamide`
  - `uniprot:P00338` via `redox_oxygen_transfer_and_sulfur_lipoamide`
  - `uniprot:P04406` via `redox_oxygen_transfer_and_sulfur_lipoamide`
  - `uniprot:P14060` via `redox_oxygen_transfer_and_sulfur_lipoamide`
- First unblock actions:
  - run current-reference sequence search and current-countable structural screen for external sourced rows
  - materialize source-free active-site locators for blocked M-CSA rows
  - promote no row until a separate label-factory gate and human countable-promotion review pass
- Priority unblock candidate IDs:
  - `uniprot:O15527`
  - `uniprot:O60568`
  - `uniprot:P06746`
  - `uniprot:P29372`
  - `uniprot:P30176`
  - `uniprot:P33025`
  - `uniprot:P34949`
  - `uniprot:P60174`
  - `uniprot:Q13907`
  - `uniprot:Q6NSJ0`
  - `uniprot:Q9BXS1`
  - `uniprot:A6NJ78`
  - `uniprot:O95050`
  - `uniprot:P04424`
  - `uniprot:P11086`
  - `uniprot:P22830`
  - `uniprot:P30566`
  - `uniprot:P35914`
  - `uniprot:P40261`
  - `uniprot:P42126`
  - `uniprot:P46597`
  - `uniprot:P51580`
  - `uniprot:P78549`
  - `uniprot:Q04760`
  - `uniprot:Q13087`

## Largest Action Queues

| Admission state | Family axis | Rows | Next action |
| --- | --- | ---: | --- |
| `review_only_evidence` | `metal_hydrolase_subclasses` | 253 | preserve as review-only family evidence until explicit promotion gates pass |
| `reject/OOS_preserve_signal` | `metal_hydrolase_subclasses` | 97 | preserve as non-counting OOS or hard-negative evidence |
| `review_only_evidence` | `redox_oxygen_transfer_and_sulfur_lipoamide` | 81 | preserve as review-only family evidence until explicit promotion gates pass |
| `reject/OOS_preserve_signal` | `glycoside_or_nucleoside_hydrolase_controls` | 41 | preserve as non-counting OOS or hard-negative evidence |
| `reject/OOS_preserve_signal` | `redox_oxygen_transfer_and_sulfur_lipoamide` | 38 | preserve as non-counting OOS or hard-negative evidence |
| `acquisition_needed` | `near_orphan_or_unrepresented_mechanism_tail` | 37 | run the named source, sequence, structure, and duplicate screens |
| `blocked_locator` | `metal_hydrolase_subclasses` | 34 | repair source-free residue mapping or active-site locator evidence |
| `review_only_evidence` | `plp_child_subclasses` | 33 | preserve as review-only family evidence until explicit promotion gates pass |
| `blocked_locator` | `redox_oxygen_transfer_and_sulfur_lipoamide` | 26 | repair source-free residue mapping or active-site locator evidence |
| `acquisition_needed` | `phosphoryl_transfer_boundary` | 25 | run the named source, sequence, structure, and duplicate screens |
| `blocked_locator` | `no_reliable_structure_or_locator_gap` | 19 | repair source-free residue mapping or active-site locator evidence |
| `reject/OOS_preserve_signal` | `plp_child_subclasses` | 15 | preserve as non-counting OOS or hard-negative evidence |

## Next Batch Recommendation

`external_sourced_rows_sequence_structure_distance_screens`: The first batch already clears the 500-row target locally. The largest actionable next lift is converting acquisition_needed external rows into review_only_evidence with source-free locator, sequence-distance, and structural duplicate screens.
