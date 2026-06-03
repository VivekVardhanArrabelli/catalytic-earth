# Active Lever Reviewer Decision Queue - current702

Run: 2026-06-03T10:22:00Z

Review-only consolidated decision queue across the active Lever 2/3/4 blockers. It composes existing decision packets so reviewer actions are visible and hash-verifiable; it does not apply decisions, copy locator sidecars, write imports, edit labels, change registries, train models, or tune thresholds.

## Status

- active_lever_reviewer_decision_queue_ready_review_only
- Decision items: 78
- Lever counts: {'Lever 2': 55, 'Lever 3': 1, 'Lever 4': 22}
- Decision classes: {'family_panel_expert_import_decision': 22, 'p10746_fold_only_deployment_caveat': 1, 'source_free_locator_rewrite_approval': 55}
- Lever 4 import-preview candidates if accepted: 6
- Lever 4 accepted import-preview rows: 0
- Lever 4 label-factory gate input rows: 0
- Lever 2 clean locator rewrite items: 49
- Automation-action-allowed-now items: 0
- Blockers: []

## Decision

- Queue ready for review: True
- Apply decisions now: False
- Lever 4 label-factory gate inputs ready: False
- Next gate: Review priority-1/2 items first: P10746 caveat decision for Lever 3 deployment closure, then the six Lever 4 expert-import rows that can become import-preview candidates if accepted. Only after explicit decisions are recorded should the matching application gates be rerun.

## Queue

| priority | lever | row | decision class | scope | status | next gate |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Lever 3 | m_csa:204 | p10746_fold_only_deployment_caveat | confounded_deployment_closure | pending_explicit_decision | apply-fold-augmented-p10746-deployment-caveat-decision |
| 2 | Lever 4 | m_csa:10 | family_panel_expert_import_decision | near_orphan_glycoside_or_nucleoside_hydrolase_controls | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 2 | Lever 4 | m_csa:30 | family_panel_expert_import_decision | glycyl_radical_or_thiamine_radical_lyase_boundary | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 2 | Lever 4 | m_csa:31 | family_panel_expert_import_decision | glycyl_radical_or_thiamine_radical_lyase_boundary | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 2 | Lever 4 | m_csa:191 | family_panel_expert_import_decision | thiol_disulfide_oxidoreductase_isomerase_boundary | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 2 | Lever 4 | m_csa:448 | family_panel_expert_import_decision | lipoamide_or_sulfur_transfer_redox_boundary | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 2 | Lever 4 | m_csa:973 | family_panel_expert_import_decision | flavin_monooxygenase_and_flavin_oxygen_transfer | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 3 | Lever 2 | m_csa:3 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:9 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:32 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:43 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:44 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:45 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:46 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:97 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:109 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:115 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:121 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:131 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:159 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:163 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:171 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:180 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:188 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:211 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:220 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:239 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:242 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:250 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:311 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:321 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:323 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:333 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:352 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:370 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:384 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:392 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:397 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:403 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:418 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:419 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:497 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:517 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:526 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:545 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:551 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:709 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:710 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:714 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:723 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:750 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:853 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:854 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:916 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:990 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 3 | Lever 2 | m_csa:994 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 4 | Lever 4 | m_csa:116 | family_panel_expert_import_decision | near_orphan_glycoside_or_nucleoside_hydrolase_controls | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 4 | Lever 4 | m_csa:131 | family_panel_expert_import_decision | flavin_monooxygenase_and_flavin_oxygen_transfer | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 4 | Lever 4 | m_csa:132 | family_panel_expert_import_decision | flavin_monooxygenase_and_flavin_oxygen_transfer | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 4 | Lever 4 | m_csa:267 | family_panel_expert_import_decision | lipoamide_or_sulfur_transfer_redox_boundary | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 4 | Lever 4 | m_csa:551 | family_panel_expert_import_decision | flavin_monooxygenase_and_flavin_oxygen_transfer | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 4 | Lever 4 | m_csa:750 | family_panel_expert_import_decision | cobalamin_and_radical_rearrangement_panel | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 4 | Lever 4 | mh_066 | family_panel_expert_import_decision | no_reliable_structure_metal_hydrolase_controls | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 4 | Lever 4 | mh_067 | family_panel_expert_import_decision | no_reliable_structure_metal_hydrolase_controls | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 4 | Lever 4 | mh_068 | family_panel_expert_import_decision | no_reliable_structure_metal_hydrolase_controls | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 4 | Lever 4 | mh_073 | family_panel_expert_import_decision | near_orphan_glycoside_or_nucleoside_hydrolase_controls | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 4 | Lever 4 | secondary_probe::radical_sam_enzyme | family_panel_expert_import_decision | cobalamin_and_radical_rearrangement_panel | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 5 | Lever 4 | external_glycoside_panel | family_panel_expert_import_decision | near_orphan_glycoside_or_nucleoside_hydrolase_controls | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 5 | Lever 4 | mh_064 | family_panel_expert_import_decision | no_reliable_structure_metal_hydrolase_controls | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 5 | Lever 4 | mh_065 | family_panel_expert_import_decision | no_reliable_structure_metal_hydrolase_controls | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 5 | Lever 4 | mh_072 | family_panel_expert_import_decision | no_reliable_structure_metal_hydrolase_controls | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 5 | Lever 4 | secondary_probe::cobalamin_radical_rearrangement | family_panel_expert_import_decision | cobalamin_and_radical_rearrangement_panel | pending_expert_import_decision | apply-fold-augmented-family-panel-expert-import-decision |
| 6 | Lever 2 | m_csa:56 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 6 | Lever 2 | m_csa:199 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 6 | Lever 2 | m_csa:356 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 6 | Lever 2 | m_csa:480 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 6 | Lever 2 | m_csa:541 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| 6 | Lever 2 | m_csa:599 | source_free_locator_rewrite_approval | heldout_source_free_locator_surface | pending_reviewer_decision | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |

## Interpretation

- 78 active Lever 2/3/4 reviewer decisions are queued; none are applied automatically.
- The active lever blockers are now organized by unblock effect: one P10746 policy caveat, six Lever 4 rows that could enter import preview if accepted, and 55 Lever 2 locator rewrites that still require explicit approval before materialization.
- Record reviewed decisions in the source packet formats with hashes unchanged, then rerun only the relevant application or materialization gate.
