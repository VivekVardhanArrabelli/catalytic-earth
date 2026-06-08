# Family Label Admission Pipeline - current702

Run: 2026-06-08T03:51:18Z

Small deterministic family-label admission pipeline for current702 family-panel rows. It normalizes existing family-panel gates into one row-level state, preserves mechanism/provenance signal, and does not import, promote, score heldout, refit, or change thresholds.

## Status

- family_label_admission_pipeline_ready_review_only
- Candidate rows evaluated: 22
- Family axes evaluated: 7
- Admission states: {'countable_candidate': 0, 'review_only_evidence': 2, 'oos_hard_negative': 11, 'blocked_locator': 2, 'blocked_coordinate': 3, 'blocked_family_decision': 0, 'reject_preserve_signal': 4}
- Import-preview rows: 0
- Accepted decisions waiting for import preview: 0
- Review-packet rows: 5
- Expert decision template rows: 0
- Expert decision review-file rows: 0
- Architecture decision proposals: 0 ({})
- Human family-decision rows after architecture defaults: 0
- OOS/reject signal rows: 15
- Exact-one-state audit: passed (22/22 rows)
- Action-queue rows: 5
- Blockers: ['source_free_locators_pending', 'coordinates_or_coordinate_policy_pending', 'no_countable_candidates_from_current_inputs']

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
| flavin_monooxygenase_and_flavin_oxygen_transfer | 4 | {'oos_hard_negative': 3, 'review_only_evidence': 1} |
| glycyl_radical_or_thiamine_radical_lyase_boundary | 2 | {'reject_preserve_signal': 2} |
| lipoamide_or_sulfur_transfer_redox_boundary | 2 | {'oos_hard_negative': 1, 'review_only_evidence': 1} |
| near_orphan_glycoside_or_nucleoside_hydrolase_controls | 4 | {'blocked_coordinate': 1, 'oos_hard_negative': 2, 'reject_preserve_signal': 1} |
| no_reliable_structure_metal_hydrolase_controls | 6 | {'blocked_coordinate': 1, 'blocked_locator': 2, 'oos_hard_negative': 3} |
| thiol_disulfide_oxidoreductase_isomerase_boundary | 1 | {'reject_preserve_signal': 1} |

## Row Admission Table

| row | family axis | state | blocker | next action |
| --- | --- | --- | --- | --- |
| m_csa:10 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | reject_preserve_signal | explicit_expert_reject | preserve the reviewed rejection/OOS signal and do not import |
| m_csa:30 | glycyl_radical_or_thiamine_radical_lyase_boundary | reject_preserve_signal | explicit_expert_reject | preserve the reviewed rejection/OOS signal and do not import |
| m_csa:31 | glycyl_radical_or_thiamine_radical_lyase_boundary | reject_preserve_signal | explicit_expert_reject | preserve the reviewed rejection/OOS signal and do not import |
| m_csa:116 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| m_csa:131 | flavin_monooxygenase_and_flavin_oxygen_transfer | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| m_csa:132 | flavin_monooxygenase_and_flavin_oxygen_transfer | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| m_csa:191 | thiol_disulfide_oxidoreductase_isomerase_boundary | reject_preserve_signal | explicit_expert_reject | preserve the reviewed rejection/OOS signal and do not import |
| m_csa:267 | lipoamide_or_sulfur_transfer_redox_boundary | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| m_csa:448 | lipoamide_or_sulfur_transfer_redox_boundary | review_only_evidence | explicit_review_only_decision | preserve the reviewed evidence outside import preview unless new family-promotion evidence is added |
| m_csa:551 | flavin_monooxygenase_and_flavin_oxygen_transfer | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| m_csa:750 | cobalamin_and_radical_rearrangement_panel | oos_hard_negative | completed_source_check_no_family_promotion | preserve as OOS/boundary signal unless a separate family-promotion override is explicitly reviewed |
| m_csa:973 | flavin_monooxygenase_and_flavin_oxygen_transfer | review_only_evidence | explicit_review_only_decision | preserve the reviewed evidence outside import preview unless new family-promotion evidence is added |
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

## Architecture Decision Proposals

| row | proposed decision | confidence | human required for default | rationale |
| --- | --- | --- | --- | --- |
| n/a | n/a | n/a | 0 | no architecture proposal rows |

## Outputs

- Review packet: 5 unresolved family/locator/coordinate rows.
- Expert decision intake packet: 0 family-decision templates.
- Expert decision review-file template: 0 pending rows.
- Import preview: 0 rows from current inputs.
- Rejects/OOS signal packet: 15 preserved signal rows.

## Expert Decision Intake

| rank | row | decision context | preview if accepted | allowed decisions |
| ---: | --- | --- | --- | --- |
| n/a | n/a | n/a | 0 | no pending expert decision templates |

Decision review-file template:
`artifacts/v3_family_label_admission_expert_decision_template_current702_20260607.json`

## Action Queue

| rank | row | action class | state | next action |
| ---: | --- | --- | --- | --- |
| 1 | mh_065 | source_free_locator_or_position_mapping_resolution | blocked_locator | No matching non-AFDB replacement coordinate is cached for mh_065/mh_072; provide matching frozen PDB/mmCIF coordinates or explicitly approve alignment/remapped locators before any raw representative-coordinate copy. |
| 2 | mh_072 | source_free_locator_or_position_mapping_resolution | blocked_locator | No matching non-AFDB replacement coordinate is cached for mh_065/mh_072; provide matching frozen PDB/mmCIF coordinates or explicitly approve alignment/remapped locators before any raw representative-coordinate copy. |
| 3 | external_glycoside_panel | coordinate_or_coordinate_policy_resolution | blocked_coordinate | No cached same-accession substrate-like coordinate clears external_glycoside_panel; provide an explicit substrate-complex coordinate or expert-approved non-glycan locator before rerunning schema/scoring. |
| 4 | mh_064 | coordinate_or_coordinate_policy_resolution | blocked_coordinate | Approve or reject fetching mh_064 frozen alternate coordinates 3RKJ/3RKK/3SBL/3SFP/3SPU. |
| 5 | secondary_probe::cobalamin_radical_rearrangement | coordinate_or_coordinate_policy_resolution | blocked_coordinate | No eligible alternate source row is available for Q59490; authorize an alternate source row/coordinate or define an explicit nonlabel strategy with at least two source-free sequence-position locators. |

## Next Task

- Resolve the highest-priority blocked locator row mh_065: No matching non-AFDB replacement coordinate is cached for mh_065/mh_072; provide matching frozen PDB/mmCIF coordinates or explicitly approve alignment/remapped locators before any raw representative-coordinate copy.
- Human decision needed: source-free locator or position-mapping approval
