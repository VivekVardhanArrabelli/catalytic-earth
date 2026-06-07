# Family Label Admission Pipeline - current702

Run: 2026-06-07T19:26:57Z

Small deterministic family-label admission pipeline for current702 family-panel rows. It normalizes existing family-panel gates into one row-level state, preserves mechanism/provenance signal, and does not import, promote, score heldout, refit, or change thresholds.

## Status

- family_label_admission_pipeline_ready_review_only
- Candidate rows evaluated: 22
- Family axes evaluated: 7
- Admission states: {'countable_candidate': 0, 'review_only_evidence': 0, 'oos_hard_negative': 11, 'blocked_locator': 2, 'blocked_coordinate': 3, 'blocked_family_decision': 6, 'reject_preserve_signal': 0}
- Import-preview rows: 0
- Review-packet rows: 11
- OOS/reject signal rows: 11
- Exact-one-state audit: passed (22/22 rows)
- Action-queue rows: 11
- Blockers: ['family_decisions_pending', 'source_free_locators_pending', 'coordinates_or_coordinate_policy_pending', 'no_countable_candidates_from_current_inputs']

## Machinery Applied

- family_set_expansion_targets
- family_panel_evidence_packets
- fold_augmented_family_panel_research_readout
- family_panel_countability_gate_preflight
- family_panel_import_preview_blocker_gate
- family_panel_expert_import_decision_packet
- family_panel_acceptance_scenario_plan
- family_panel_expert_import_decision_application
- family_panel_accepted_import_preview
- family_panel_label_factory_gate_readiness
- family_panel_source_free_locator_human_decision_matrix
- family_panel_source_free_predicted_geometry_retrieval

## Family Axes

| family axis | evaluated rows | states |
| --- | ---: | --- |
| cobalamin_and_radical_rearrangement_panel | 3 | {'blocked_coordinate': 1, 'oos_hard_negative': 2} |
| flavin_monooxygenase_and_flavin_oxygen_transfer | 4 | {'blocked_family_decision': 1, 'oos_hard_negative': 3} |
| glycyl_radical_or_thiamine_radical_lyase_boundary | 2 | {'blocked_family_decision': 2} |
| lipoamide_or_sulfur_transfer_redox_boundary | 2 | {'blocked_family_decision': 1, 'oos_hard_negative': 1} |
| near_orphan_glycoside_or_nucleoside_hydrolase_controls | 4 | {'blocked_coordinate': 1, 'blocked_family_decision': 1, 'oos_hard_negative': 2} |
| no_reliable_structure_metal_hydrolase_controls | 6 | {'blocked_coordinate': 1, 'blocked_locator': 2, 'oos_hard_negative': 3} |
| thiol_disulfide_oxidoreductase_isomerase_boundary | 1 | {'blocked_family_decision': 1} |

## Row Admission Table

| row | family axis | state | blocker | next action |
| --- | --- | --- | --- | --- |
| m_csa:10 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | blocked_family_decision | expert_family_admission_decision_required | record an explicit expert accept/reject/review-only decision with the preserved decision_context_sha256 |
| m_csa:30 | glycyl_radical_or_thiamine_radical_lyase_boundary | blocked_family_decision | expert_family_admission_decision_required | record an explicit expert accept/reject/review-only decision with the preserved decision_context_sha256 |
| m_csa:31 | glycyl_radical_or_thiamine_radical_lyase_boundary | blocked_family_decision | expert_family_admission_decision_required | record an explicit expert accept/reject/review-only decision with the preserved decision_context_sha256 |
| m_csa:116 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| m_csa:131 | flavin_monooxygenase_and_flavin_oxygen_transfer | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| m_csa:132 | flavin_monooxygenase_and_flavin_oxygen_transfer | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| m_csa:191 | thiol_disulfide_oxidoreductase_isomerase_boundary | blocked_family_decision | expert_family_admission_decision_required | record an explicit expert accept/reject/review-only decision with the preserved decision_context_sha256 |
| m_csa:267 | lipoamide_or_sulfur_transfer_redox_boundary | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| m_csa:448 | lipoamide_or_sulfur_transfer_redox_boundary | blocked_family_decision | expert_family_admission_decision_required | record an explicit expert accept/reject/review-only decision with the preserved decision_context_sha256 |
| m_csa:551 | flavin_monooxygenase_and_flavin_oxygen_transfer | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| m_csa:750 | cobalamin_and_radical_rearrangement_panel | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| m_csa:973 | flavin_monooxygenase_and_flavin_oxygen_transfer | blocked_family_decision | expert_family_admission_decision_required | record an explicit expert accept/reject/review-only decision with the preserved decision_context_sha256 |
| external_glycoside_panel | near_orphan_glycoside_or_nucleoside_hydrolase_controls | blocked_coordinate | coordinate_or_coordinate_policy_missing | No cached same-accession substrate-like coordinate clears external_glycoside_panel; provide an explicit substrate-complex coordinate or expert-approved non-glycan locator before rerunning schema/scoring. |
| mh_064 | no_reliable_structure_metal_hydrolase_controls | blocked_coordinate | coordinate_or_coordinate_policy_missing | Approve or reject fetching mh_064 frozen alternate coordinates 3RKJ/3RKK/3SBL/3SFP/3SPU. |
| mh_065 | no_reliable_structure_metal_hydrolase_controls | blocked_locator | source_free_locator_or_position_mapping_missing | No matching non-AFDB replacement coordinate is cached for mh_065/mh_072; provide matching frozen PDB/mmCIF coordinates or explicitly approve alignment/remapped locators before any raw representative-coordinate copy. |
| mh_066 | no_reliable_structure_metal_hydrolase_controls | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| mh_067 | no_reliable_structure_metal_hydrolase_controls | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| mh_068 | no_reliable_structure_metal_hydrolase_controls | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| mh_072 | no_reliable_structure_metal_hydrolase_controls | blocked_locator | source_free_locator_or_position_mapping_missing | No matching non-AFDB replacement coordinate is cached for mh_065/mh_072; provide matching frozen PDB/mmCIF coordinates or explicitly approve alignment/remapped locators before any raw representative-coordinate copy. |
| mh_073 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| secondary_probe::cobalamin_radical_rearrangement | cobalamin_and_radical_rearrangement_panel | blocked_coordinate | coordinate_or_coordinate_policy_missing | No eligible alternate source row is available for Q59490; authorize an alternate source row/coordinate or define an explicit nonlabel strategy with at least two source-free sequence-position locators. |
| secondary_probe::radical_sam_enzyme | cobalamin_and_radical_rearrangement_panel | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |

## Outputs

- Review packet: 11 unresolved family/locator/coordinate rows.
- Import preview: 0 rows from current inputs.
- Rejects/OOS signal packet: 11 preserved signal rows.

## Action Queue

| rank | row | action class | state | next action |
| ---: | --- | --- | --- | --- |
| 1 | m_csa:10 | expert_family_admission_decision | blocked_family_decision | record an explicit expert accept/reject/review-only decision with the preserved decision_context_sha256 |
| 2 | m_csa:30 | expert_family_admission_decision | blocked_family_decision | record an explicit expert accept/reject/review-only decision with the preserved decision_context_sha256 |
| 3 | m_csa:31 | expert_family_admission_decision | blocked_family_decision | record an explicit expert accept/reject/review-only decision with the preserved decision_context_sha256 |
| 4 | m_csa:191 | expert_family_admission_decision | blocked_family_decision | record an explicit expert accept/reject/review-only decision with the preserved decision_context_sha256 |
| 5 | m_csa:448 | expert_family_admission_decision | blocked_family_decision | record an explicit expert accept/reject/review-only decision with the preserved decision_context_sha256 |
| 6 | m_csa:973 | expert_family_admission_decision | blocked_family_decision | record an explicit expert accept/reject/review-only decision with the preserved decision_context_sha256 |
| 7 | mh_065 | source_free_locator_or_position_mapping_resolution | blocked_locator | No matching non-AFDB replacement coordinate is cached for mh_065/mh_072; provide matching frozen PDB/mmCIF coordinates or explicitly approve alignment/remapped locators before any raw representative-coordinate copy. |
| 8 | mh_072 | source_free_locator_or_position_mapping_resolution | blocked_locator | No matching non-AFDB replacement coordinate is cached for mh_065/mh_072; provide matching frozen PDB/mmCIF coordinates or explicitly approve alignment/remapped locators before any raw representative-coordinate copy. |
| 9 | external_glycoside_panel | coordinate_or_coordinate_policy_resolution | blocked_coordinate | No cached same-accession substrate-like coordinate clears external_glycoside_panel; provide an explicit substrate-complex coordinate or expert-approved non-glycan locator before rerunning schema/scoring. |
| 10 | mh_064 | coordinate_or_coordinate_policy_resolution | blocked_coordinate | Approve or reject fetching mh_064 frozen alternate coordinates 3RKJ/3RKK/3SBL/3SFP/3SPU. |
| 11 | secondary_probe::cobalamin_radical_rearrangement | coordinate_or_coordinate_policy_resolution | blocked_coordinate | No eligible alternate source row is available for Q59490; authorize an alternate source row/coordinate or define an explicit nonlabel strategy with at least two source-free sequence-position locators. |

## Next Task

- Adjudicate the blocked family-decision rows with preserved decision_context_sha256 values, starting with m_csa:10, m_csa:30, m_csa:31, m_csa:191, m_csa:448, m_csa:973; then rerun the expert-decision application and accepted import-preview builders.
- Human decision needed: explicit accept/reject/review-only expert decisions for 6 family-panel rows
