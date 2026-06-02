# Fold-Augmented Family-Panel Import-Preview Blocker Gate - current702

Run: 2026-06-02T19:37:51Z

Lever 4 import-preview blocker gate for the review-only family-panel packets. It consumes the countability preflight and records exactly why no family-panel row can enter an import preview or label-factory countability gate yet.

## Status

- family_panel_import_preview_blocker_gate_ready_blocked
- Review rows evaluated: 22
- Rows blocked before import preview: 22
- Import-preview-ready rows: 0
- Label-factory-ready rows: 0
- Countable label candidates: 0
- Primary blocker classes: {'completed_source_check_review_only_no_promotion': 11, 'expert_family_admission_decision_required': 6, 'source_free_locator_or_primary_channel_missing': 5}
- Priority rows with locator decision class: 5
- Priority rows mechanically clearable now: 0

## Decision

- Source checks fully reconciled: True
- Import preview can run: False
- New countable labels authorized: False
- All priority rows human/policy blocked: True
- Priority next rows: ['secondary_probe::cobalamin_radical_rearrangement', 'external_glycoside_panel', 'mh_064', 'mh_065', 'mh_072']
- Next gate: Pick one locator decision class from the joined human decision matrix and record an explicit approval/rejection; then rerun this blocker gate before any family-panel import preview.

## Panel Blockers

| panel | rows | primary blocker counts |
| --- | ---: | --- |
| cobalamin_and_radical_rearrangement_panel | 3 | {'completed_source_check_review_only_no_promotion': 2, 'source_free_locator_or_primary_channel_missing': 1} |
| flavin_monooxygenase_and_flavin_oxygen_transfer | 4 | {'completed_source_check_review_only_no_promotion': 3, 'expert_family_admission_decision_required': 1} |
| glycyl_radical_or_thiamine_radical_lyase_boundary | 2 | {'expert_family_admission_decision_required': 2} |
| lipoamide_or_sulfur_transfer_redox_boundary | 2 | {'completed_source_check_review_only_no_promotion': 1, 'expert_family_admission_decision_required': 1} |
| near_orphan_glycoside_or_nucleoside_hydrolase_controls | 4 | {'completed_source_check_review_only_no_promotion': 2, 'expert_family_admission_decision_required': 1, 'source_free_locator_or_primary_channel_missing': 1} |
| no_reliable_structure_metal_hydrolase_controls | 6 | {'completed_source_check_review_only_no_promotion': 3, 'source_free_locator_or_primary_channel_missing': 3} |
| thiol_disulfide_oxidoreductase_isomerase_boundary | 1 | {'expert_family_admission_decision_required': 1} |

## Row Blockers

| row | panel | primary blocker | locator decision | required actions |
| --- | --- | --- | --- | --- |
| m_csa:750 | cobalamin_and_radical_rearrangement_panel | completed_source_check_review_only_no_promotion | None | expert_import_decision_required, family_promotion_decision_required, label_factory_gate_required_after_import_preview |
| secondary_probe::radical_sam_enzyme | cobalamin_and_radical_rearrangement_panel | completed_source_check_review_only_no_promotion | None | expert_import_decision_required, family_promotion_decision_required, label_factory_gate_required_after_import_preview |
| m_csa:131 | flavin_monooxygenase_and_flavin_oxygen_transfer | completed_source_check_review_only_no_promotion | None | expert_import_decision_required, family_promotion_decision_required, label_factory_gate_required_after_import_preview |
| m_csa:132 | flavin_monooxygenase_and_flavin_oxygen_transfer | completed_source_check_review_only_no_promotion | None | expert_import_decision_required, family_promotion_decision_required, label_factory_gate_required_after_import_preview |
| m_csa:551 | flavin_monooxygenase_and_flavin_oxygen_transfer | completed_source_check_review_only_no_promotion | None | expert_import_decision_required, family_promotion_decision_required, label_factory_gate_required_after_import_preview |
| m_csa:267 | lipoamide_or_sulfur_transfer_redox_boundary | completed_source_check_review_only_no_promotion | None | expert_import_decision_required, family_promotion_decision_required, label_factory_gate_required_after_import_preview |
| m_csa:116 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | completed_source_check_review_only_no_promotion | None | expert_import_decision_required, family_promotion_decision_required, label_factory_gate_required_after_import_preview |
| mh_073 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | completed_source_check_review_only_no_promotion | None | expert_import_decision_required, family_promotion_decision_required, label_factory_gate_required_after_import_preview |
| mh_066 | no_reliable_structure_metal_hydrolase_controls | completed_source_check_review_only_no_promotion | None | expert_import_decision_required, family_promotion_decision_required, label_factory_gate_required_after_import_preview |
| mh_067 | no_reliable_structure_metal_hydrolase_controls | completed_source_check_review_only_no_promotion | None | expert_import_decision_required, family_promotion_decision_required, label_factory_gate_required_after_import_preview |
| mh_068 | no_reliable_structure_metal_hydrolase_controls | completed_source_check_review_only_no_promotion | None | expert_import_decision_required, family_promotion_decision_required, label_factory_gate_required_after_import_preview |
| m_csa:973 | flavin_monooxygenase_and_flavin_oxygen_transfer | expert_family_admission_decision_required | None | expert_import_decision_required, label_factory_gate_required_after_import_preview |
| m_csa:30 | glycyl_radical_or_thiamine_radical_lyase_boundary | expert_family_admission_decision_required | None | expert_import_decision_required, label_factory_gate_required_after_import_preview |
| m_csa:31 | glycyl_radical_or_thiamine_radical_lyase_boundary | expert_family_admission_decision_required | None | expert_import_decision_required, label_factory_gate_required_after_import_preview |
| m_csa:448 | lipoamide_or_sulfur_transfer_redox_boundary | expert_family_admission_decision_required | None | expert_import_decision_required, label_factory_gate_required_after_import_preview |
| m_csa:10 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | expert_family_admission_decision_required | None | expert_import_decision_required, label_factory_gate_required_after_import_preview |
| m_csa:191 | thiol_disulfide_oxidoreductase_isomerase_boundary | expert_family_admission_decision_required | None | expert_import_decision_required, label_factory_gate_required_after_import_preview |
| secondary_probe::cobalamin_radical_rearrangement | cobalamin_and_radical_rearrangement_panel | source_free_locator_or_primary_channel_missing | nonlabel_locator_strategy_or_alternate_source_required | expert_import_decision_required, label_factory_gate_required_after_import_preview, materialize_primary_channel_score, resolve_source_free_locator_or_coordinate_policy |
| external_glycoside_panel | near_orphan_glycoside_or_nucleoside_hydrolase_controls | source_free_locator_or_primary_channel_missing | ligand_specificity_validator_or_substrate_coordinate_required | expert_import_decision_required, label_factory_gate_required_after_import_preview, materialize_primary_channel_score, resolve_source_free_locator_or_coordinate_policy |
| mh_064 | no_reliable_structure_metal_hydrolase_controls | source_free_locator_or_primary_channel_missing | alternate_coordinate_fetch_approval_required | expert_import_decision_required, label_factory_gate_required_after_import_preview, materialize_primary_channel_score, resolve_source_free_locator_or_coordinate_policy |
| mh_065 | no_reliable_structure_metal_hydrolase_controls | source_free_locator_or_primary_channel_missing | accession_equivalence_or_matching_coordinate_required | expert_import_decision_required, label_factory_gate_required_after_import_preview, materialize_primary_channel_score, resolve_source_free_locator_or_coordinate_policy |
| mh_072 | no_reliable_structure_metal_hydrolase_controls | source_free_locator_or_primary_channel_missing | accession_equivalence_or_matching_coordinate_required | expert_import_decision_required, label_factory_gate_required_after_import_preview, materialize_primary_channel_score, resolve_source_free_locator_or_coordinate_policy |

## Interpretation

- 0/22 family-panel review rows can enter an import preview.
- The source-check queue is reconciled, but countability is still blocked by expert import decisions, label-factory gate absence, completed source checks that explicitly remain review-only, and source-free locator/primary-channel gaps. The priority locator rows are all joined to human or policy decision classes.
- Start with the highest-priority locator decision class: Provide matching frozen coordinates for mh_065/mh_072 or explicitly approve alignment/remapped locators before any raw representative-coordinate copy. Then rerun the relevant locator schema or candidate audit before scoring.
