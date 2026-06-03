# Fold-Augmented Family-Panel Expert Import Decision Packet - current702

Run: 2026-06-03T08:09:20Z

Review-only expert-decision intake packet for Lever 4 family-panel rows blocked before import preview. It stages explicit accept/reject/keep-review-only decisions with row-context hashes; it does not write an import preview, run the label-factory gate, edit labels, change registries, or make any row countable.

## Status

- family_panel_expert_import_decision_packet_ready_review_only
- Decision stubs: 22
- Panels represented: 7
- Import-preview candidates if accepted: 6
- Family-promotion override needed rows: 11
- Locator/primary-channel blocked rows: 5
- Primary blocker classes: {'completed_source_check_review_only_no_promotion': 11, 'expert_family_admission_decision_required': 6, 'source_free_locator_or_primary_channel_missing': 5}
- Blockers: ['expert_import_decisions_not_recorded', 'family_promotion_override_decisions_missing', 'locator_or_primary_channel_blockers_remain']

## Decision

- Expert import packet ready for review: True
- Explicit expert decisions recorded: False
- Import preview can run now: False
- Label-factory gate ready: False
- New countable labels authorized: False
- Next gate: Record explicit expert decisions using the unchanged decision_context_sha256 values. Only accepted rows whose remaining blockers are import-preview/label-factory gates can move to a separate import-preview artifact; rows with locator, primary-channel, or family-promotion blockers remain review-only until those blockers clear.

## Decision Stubs

| row | panel | primary blocker | candidate if accepted | decision context sha |
| --- | --- | --- | ---: | --- |
| m_csa:750 | cobalamin_and_radical_rearrangement_panel | completed_source_check_review_only_no_promotion | 0 | 93a25d123a99 |
| secondary_probe::cobalamin_radical_rearrangement | cobalamin_and_radical_rearrangement_panel | source_free_locator_or_primary_channel_missing | 0 | 76e4d014d615 |
| secondary_probe::radical_sam_enzyme | cobalamin_and_radical_rearrangement_panel | completed_source_check_review_only_no_promotion | 0 | c5e1512a334f |
| m_csa:131 | flavin_monooxygenase_and_flavin_oxygen_transfer | completed_source_check_review_only_no_promotion | 0 | 2df2367c794c |
| m_csa:132 | flavin_monooxygenase_and_flavin_oxygen_transfer | completed_source_check_review_only_no_promotion | 0 | bf6fd180920d |
| m_csa:551 | flavin_monooxygenase_and_flavin_oxygen_transfer | completed_source_check_review_only_no_promotion | 0 | 8652136523d5 |
| m_csa:973 | flavin_monooxygenase_and_flavin_oxygen_transfer | expert_family_admission_decision_required | 1 | 1dabc7673a19 |
| m_csa:30 | glycyl_radical_or_thiamine_radical_lyase_boundary | expert_family_admission_decision_required | 1 | 053f26507363 |
| m_csa:31 | glycyl_radical_or_thiamine_radical_lyase_boundary | expert_family_admission_decision_required | 1 | 53c1ef64975b |
| m_csa:267 | lipoamide_or_sulfur_transfer_redox_boundary | completed_source_check_review_only_no_promotion | 0 | 319241624874 |
| m_csa:448 | lipoamide_or_sulfur_transfer_redox_boundary | expert_family_admission_decision_required | 1 | 5b858c3589a6 |
| external_glycoside_panel | near_orphan_glycoside_or_nucleoside_hydrolase_controls | source_free_locator_or_primary_channel_missing | 0 | 60e499d3cc40 |
| m_csa:10 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | expert_family_admission_decision_required | 1 | 7ed5f5d914a8 |
| m_csa:116 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | completed_source_check_review_only_no_promotion | 0 | cea2ee2a2180 |
| mh_073 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | completed_source_check_review_only_no_promotion | 0 | e75dde48da5a |
| mh_064 | no_reliable_structure_metal_hydrolase_controls | source_free_locator_or_primary_channel_missing | 0 | 40080da23147 |
| mh_065 | no_reliable_structure_metal_hydrolase_controls | source_free_locator_or_primary_channel_missing | 0 | c705b3e334a6 |
| mh_066 | no_reliable_structure_metal_hydrolase_controls | completed_source_check_review_only_no_promotion | 0 | ae915cfe306e |
| mh_067 | no_reliable_structure_metal_hydrolase_controls | completed_source_check_review_only_no_promotion | 0 | 23e7a8e70a90 |
| mh_068 | no_reliable_structure_metal_hydrolase_controls | completed_source_check_review_only_no_promotion | 0 | 83ab515e63be |
| mh_072 | no_reliable_structure_metal_hydrolase_controls | source_free_locator_or_primary_channel_missing | 0 | 02378e497c32 |
| m_csa:191 | thiol_disulfide_oxidoreductase_isomerase_boundary | expert_family_admission_decision_required | 1 | ec8b364f55c8 |

## Interpretation

- 6/22 family-panel rows could become import-preview candidates after explicit expert accept decisions.
- The packet makes Lever 4 reviewer decisions countable by a future gate while keeping current rows fail-closed: accepted decisions alone do not override source-free locator, primary channel, family-promotion, import-preview, or label-factory requirements.
- Review the expert import stubs, set accepted/rejected/review-only decisions with hashes unchanged, then add or run a separate import-preview application gate before any label-factory countability action.
