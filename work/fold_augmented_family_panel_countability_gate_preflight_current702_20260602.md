# Fold-Augmented Family-Panel Countability Gate Preflight - current702

Run: 2026-06-02T19:37:50Z

Lever 4 countability preflight for the existing review-only family-panel packets. It maps packet rows to the import-preview and label-factory gates without creating labels, importing rows, changing registries, or treating research readout scores as countable evidence.

## Status

- family_panel_countability_gate_preflight_ready_no_countable_rows
- Readout candidate rows: 22
- Primary score-complete rows: 17
- Non-abstained review rows: 11
- Missing primary-channel rows: 5
- Source-check queue rows joined: 11
- Source-check completed rows joined: 11
- Source-check pending rows joined: 0
- Completed source checks still not promotion-ready: 11
- Locator human/policy blocked rows joined: 5
- Countable label candidates: 0
- Blocker counts: {'completed_source_check_not_family_promotion_ready': 11, 'countable_import_preview_missing': 22, 'label_factory_gate_not_run_for_family_panel_row': 22, 'primary_channel_score_missing': 5, 'review_packet_not_expert_import_decision': 22, 'source_free_locator_human_or_policy_decision_required': 5}

## Decision

- New countable labels authorized: False
- Import ready: False
- Label-factory gate ready: False
- Next gate: Source checks are fully reconciled. Clear source-free geometry/locator blockers for missing-primary-channel rows, then run an explicit import-preview blocker gate before any label-factory countability action.

## Panel Gates

| panel | rows | complete | non-abstained | geometry/locator blocked | countable | next gate |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| cobalamin_and_radical_rearrangement_panel | 3 | 2 | 2 | 1 | 0 | source_check_non_abstained_rows_then_import_preview |
| flavin_monooxygenase_and_flavin_oxygen_transfer | 4 | 4 | 3 | 0 | 0 | source_check_non_abstained_rows_then_import_preview |
| glycyl_radical_or_thiamine_radical_lyase_boundary | 2 | 2 | 0 | 0 | 0 | expert_family_decision_before_import_preview |
| lipoamide_or_sulfur_transfer_redox_boundary | 2 | 2 | 1 | 0 | 0 | source_check_non_abstained_rows_then_import_preview |
| near_orphan_glycoside_or_nucleoside_hydrolase_controls | 4 | 3 | 2 | 1 | 0 | source_check_non_abstained_rows_then_import_preview |
| no_reliable_structure_metal_hydrolase_controls | 6 | 3 | 3 | 3 | 0 | source_check_non_abstained_rows_then_import_preview |
| thiol_disulfide_oxidoreductase_isomerase_boundary | 1 | 1 | 0 | 0 | 0 | expert_family_decision_before_import_preview |

## Row Gates

| row | panel | status | source-check | locator status | blockers |
| --- | --- | --- | --- | --- | --- |
| m_csa:750 | cobalamin_and_radical_rearrangement_panel | non_abstained_at_research_threshold | completed_review_only_no_label_change | None | completed_source_check_not_family_promotion_ready, countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| secondary_probe::cobalamin_radical_rearrangement | cobalamin_and_radical_rearrangement_panel | not_score_complete_for_primary_channel | None | blocked_no_coordinate_anchor_nonlabel_strategy_required | countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, primary_channel_score_missing, review_packet_not_expert_import_decision, source_free_locator_human_or_policy_decision_required |
| secondary_probe::radical_sam_enzyme | cobalamin_and_radical_rearrangement_panel | non_abstained_at_research_threshold | completed_review_only_no_label_change | None | completed_source_check_not_family_promotion_ready, countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| m_csa:131 | flavin_monooxygenase_and_flavin_oxygen_transfer | non_abstained_at_research_threshold | completed_review_only_no_label_change | None | completed_source_check_not_family_promotion_ready, countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| m_csa:132 | flavin_monooxygenase_and_flavin_oxygen_transfer | non_abstained_at_research_threshold | completed_review_only_no_label_change | None | completed_source_check_not_family_promotion_ready, countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| m_csa:551 | flavin_monooxygenase_and_flavin_oxygen_transfer | non_abstained_at_research_threshold | completed_review_only_no_label_change | None | completed_source_check_not_family_promotion_ready, countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| m_csa:973 | flavin_monooxygenase_and_flavin_oxygen_transfer | abstained_at_research_threshold | None | None | countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| m_csa:30 | glycyl_radical_or_thiamine_radical_lyase_boundary | abstained_at_research_threshold | None | None | countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| m_csa:31 | glycyl_radical_or_thiamine_radical_lyase_boundary | abstained_at_research_threshold | None | None | countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| m_csa:267 | lipoamide_or_sulfur_transfer_redox_boundary | non_abstained_at_research_threshold | completed_review_only_no_label_change | None | completed_source_check_not_family_promotion_ready, countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| m_csa:448 | lipoamide_or_sulfur_transfer_redox_boundary | abstained_at_research_threshold | None | None | countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| external_glycoside_panel | near_orphan_glycoside_or_nucleoside_hydrolase_controls | not_score_complete_for_primary_channel | None | selected_acetate_and_nag_glycan_validator_rejected | countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, primary_channel_score_missing, review_packet_not_expert_import_decision, source_free_locator_human_or_policy_decision_required |
| m_csa:10 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | abstained_at_research_threshold | None | None | countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| m_csa:116 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | non_abstained_at_research_threshold | completed_review_only_no_label_change | None | completed_source_check_not_family_promotion_ready, countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| mh_073 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | non_abstained_at_research_threshold | completed_review_only_no_label_change | None | completed_source_check_not_family_promotion_ready, countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| mh_064 | no_reliable_structure_metal_hydrolase_controls | not_score_complete_for_primary_channel | None | blocked_pending_fetch_policy_no_local_alternates_cached | countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, primary_channel_score_missing, review_packet_not_expert_import_decision, source_free_locator_human_or_policy_decision_required |
| mh_065 | no_reliable_structure_metal_hydrolase_controls | not_score_complete_for_primary_channel | None | blocked_accession_mismatch_requested_afdb_position_mismatch | countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, primary_channel_score_missing, review_packet_not_expert_import_decision, source_free_locator_human_or_policy_decision_required |
| mh_066 | no_reliable_structure_metal_hydrolase_controls | non_abstained_at_research_threshold | completed_review_only_no_label_change | None | completed_source_check_not_family_promotion_ready, countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| mh_067 | no_reliable_structure_metal_hydrolase_controls | non_abstained_at_research_threshold | completed_review_only_no_label_change | None | completed_source_check_not_family_promotion_ready, countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| mh_068 | no_reliable_structure_metal_hydrolase_controls | non_abstained_at_research_threshold | completed_review_only_no_label_change | None | completed_source_check_not_family_promotion_ready, countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |
| mh_072 | no_reliable_structure_metal_hydrolase_controls | not_score_complete_for_primary_channel | None | blocked_accession_mismatch_requested_afdb_position_mismatch | countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, primary_channel_score_missing, review_packet_not_expert_import_decision, source_free_locator_human_or_policy_decision_required |
| m_csa:191 | thiol_disulfide_oxidoreductase_isomerase_boundary | abstained_at_research_threshold | None | None | countable_import_preview_missing, label_factory_gate_not_run_for_family_panel_row, review_packet_not_expert_import_decision |

## Interpretation

- 0/22 family-panel review rows are countable label candidates under the import/label-factory gate.
- The family-panel packets widen review evidence, but every row is still blocked before countability by missing expert import decisions and label-factory gates; the remaining mechanical blockers are source-free locator/geometry decisions for missing-primary-channel rows.
- Use this preflight as the Lever 4 gate: choose one panel, clear its source-check or locator blockers, then generate an explicit import preview before any label can count.
