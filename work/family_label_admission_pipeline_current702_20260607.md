# Family Label Admission Pipeline - current702

Run: 2026-06-07T20:56:09Z

Deterministic family-label admission adapter for current family-panel candidate rows. It classifies row states, preserves mechanism/provenance signal, and emits review/import/reject packets without editing labels, registries, ontology, thresholds, splits, or model weights.

## Outcome

- Status: family_label_admission_pipeline_ready_no_countable_candidates
- Candidate axes evaluated: 7
- Candidate rows evaluated: 22
- State counts: {'blocked_coordinate': 3, 'blocked_family_decision': 6, 'blocked_locator': 2, 'review_only_evidence': 11}
- Import-preview rows: 0
- Review packet rows: 22
- Reject/OOS-signal rows: 11

## Row Admission Table

| Panel | Row | State | Blocker class | Allowed next action |
| --- | --- | --- | --- | --- |
| glycyl_radical_or_thiamine_radical_lyase_boundary | m_csa:30 | blocked_family_decision | expert_family_admission_decision_required | Record an explicit expert family admission decision with the row context hash. |
| glycyl_radical_or_thiamine_radical_lyase_boundary | m_csa:31 | blocked_family_decision | expert_family_admission_decision_required | Record an explicit expert family admission decision with the row context hash. |
| thiol_disulfide_oxidoreductase_isomerase_boundary | m_csa:191 | blocked_family_decision | expert_family_admission_decision_required | Record an explicit expert family admission decision with the row context hash. |
| lipoamide_or_sulfur_transfer_redox_boundary | m_csa:267 | review_only_evidence | completed_source_check_review_only_no_promotion | Keep as review-only evidence unless an explicit family-promotion override is recorded. |
| lipoamide_or_sulfur_transfer_redox_boundary | m_csa:448 | blocked_family_decision | expert_family_admission_decision_required | Record an explicit expert family admission decision with the row context hash. |
| flavin_monooxygenase_and_flavin_oxygen_transfer | m_csa:131 | review_only_evidence | completed_source_check_review_only_no_promotion | Keep as review-only evidence unless an explicit family-promotion override is recorded. |
| flavin_monooxygenase_and_flavin_oxygen_transfer | m_csa:132 | review_only_evidence | completed_source_check_review_only_no_promotion | Keep as review-only evidence unless an explicit family-promotion override is recorded. |
| flavin_monooxygenase_and_flavin_oxygen_transfer | m_csa:551 | review_only_evidence | completed_source_check_review_only_no_promotion | Keep as review-only evidence unless an explicit family-promotion override is recorded. |
| flavin_monooxygenase_and_flavin_oxygen_transfer | m_csa:973 | blocked_family_decision | expert_family_admission_decision_required | Record an explicit expert family admission decision with the row context hash. |
| cobalamin_and_radical_rearrangement_panel | secondary_probe::cobalamin_radical_rearrangement | blocked_locator | source_free_locator_or_primary_channel_missing | Resolve the source-free locator policy/locator decision, then rerun locator validation. |
| cobalamin_and_radical_rearrangement_panel | secondary_probe::radical_sam_enzyme | review_only_evidence | completed_source_check_review_only_no_promotion | Keep as review-only evidence unless an explicit family-promotion override is recorded. |
| cobalamin_and_radical_rearrangement_panel | m_csa:750 | review_only_evidence | completed_source_check_review_only_no_promotion | Keep as review-only evidence unless an explicit family-promotion override is recorded. |
| no_reliable_structure_metal_hydrolase_controls | mh_064 | blocked_coordinate | source_free_locator_or_primary_channel_missing | Provide matching frozen coordinates or approve the coordinate fetch/remap, then rerun the primary-channel gate. |
| no_reliable_structure_metal_hydrolase_controls | mh_065 | blocked_coordinate | source_free_locator_or_primary_channel_missing | Provide matching frozen coordinates or approve the coordinate fetch/remap, then rerun the primary-channel gate. |
| no_reliable_structure_metal_hydrolase_controls | mh_066 | review_only_evidence | completed_source_check_review_only_no_promotion | Keep as review-only evidence unless an explicit family-promotion override is recorded. |
| no_reliable_structure_metal_hydrolase_controls | mh_067 | review_only_evidence | completed_source_check_review_only_no_promotion | Keep as review-only evidence unless an explicit family-promotion override is recorded. |
| no_reliable_structure_metal_hydrolase_controls | mh_068 | review_only_evidence | completed_source_check_review_only_no_promotion | Keep as review-only evidence unless an explicit family-promotion override is recorded. |
| no_reliable_structure_metal_hydrolase_controls | mh_072 | blocked_coordinate | source_free_locator_or_primary_channel_missing | Provide matching frozen coordinates or approve the coordinate fetch/remap, then rerun the primary-channel gate. |
| near_orphan_glycoside_or_nucleoside_hydrolase_controls | m_csa:10 | blocked_family_decision | expert_family_admission_decision_required | Record an explicit expert family admission decision with the row context hash. |
| near_orphan_glycoside_or_nucleoside_hydrolase_controls | m_csa:116 | review_only_evidence | completed_source_check_review_only_no_promotion | Keep as review-only evidence unless an explicit family-promotion override is recorded. |
| near_orphan_glycoside_or_nucleoside_hydrolase_controls | mh_073 | review_only_evidence | completed_source_check_review_only_no_promotion | Keep as review-only evidence unless an explicit family-promotion override is recorded. |
| near_orphan_glycoside_or_nucleoside_hydrolase_controls | external_glycoside_panel | blocked_locator | source_free_locator_or_primary_channel_missing | Resolve the source-free locator policy/locator decision, then rerun locator validation. |

## Outputs

- Review packet: family_label_admission_review_packet_ready (22 rows)
- Import preview: family_label_admission_import_preview_empty (0 rows)
- Reject/OOS-signal packet: family_label_admission_rejects_oos_signal_packet_ready (11 rows)

## Next Task

Start with the highest-priority locator decision class: No matching non-AFDB replacement coordinate is cached for mh_065/mh_072; provide matching frozen PDB/mmCIF coordinates or explicitly approve alignment/remapped locators before any raw representative-coordinate copy. Then rerun the relevant locator schema or candidate audit before scoring.
