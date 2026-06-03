# Active Lever Mechanical Actionability Audit - current702

Run: 2026-06-03T09:52:42Z

Review-only actionability audit across active Lever 2/3/4 gates. It distinguishes mechanical gates that can run now from explicit review or policy decisions that must remain fail-closed.

## Status

- active_lever_mechanical_actionability_blocked_external_decisions
- Decision items: 78
- External decisions required: 78
- Automation-action-allowed-now items: 0
- Mechanical gates ready now: 0
- Lever 2 pending locator approvals: 55
- Lever 2 event-axis linker rows: 0
- Lever 4 label-factory gate input rows: 0
- Blockers: ['no_active_lever_mechanical_gate_ready', 'p10746_policy_decision_missing', 'family_panel_expert_import_decisions_missing', 'source_free_locator_rewrite_approvals_missing', 'source_free_event_axis_linker_gate_blocked', 'source_free_event_axis_linkers_missing', 'family_panel_label_factory_gate_inputs_missing', 'lever2_pre_threshold_readiness_not_ready']

## Decision

- Apply any decision gate now: False
- Copy locator sidecars now: False
- Apply frozen residual threshold now: False
- Run label-factory gate now: False
- Next gate: Record explicit decisions in the source packets with hashes unchanged. Then rerun only the matching application or materialization gates; do not read heldout or apply the frozen Lever 2 threshold until pre-threshold readiness passes.

## Gate Checks

| lever | gate | ready now | blocker | next command after decision |
| --- | --- | --- | --- | --- |
| Lever 3 | p10746_post_decision_deployment_closure | False | p10746_policy_decision_missing | apply-fold-augmented-p10746-deployment-caveat-decision |
| Lever 4 | family_panel_label_factory_gate_readiness | False | family_panel_expert_import_decisions_missing | apply-fold-augmented-family-panel-expert-import-decision |
| Lever 2 | source_free_locator_materialization_and_pre_threshold_readiness | False | source_free_locator_rewrite_approvals_missing | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| Lever 2 | source_free_event_axis_linkers | False | source_free_event_axis_linker_gate_blocked | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-event-axis-linker-materialization-gate |

## Next Review Items

| priority | lever | row | decision class | status |
| ---: | --- | --- | --- | --- |
| 1 | Lever 3 | m_csa:204 | p10746_fold_only_deployment_caveat | pending_explicit_decision |
| 2 | Lever 4 | m_csa:10 | family_panel_expert_import_decision | pending_expert_import_decision |
| 2 | Lever 4 | m_csa:30 | family_panel_expert_import_decision | pending_expert_import_decision |
| 2 | Lever 4 | m_csa:31 | family_panel_expert_import_decision | pending_expert_import_decision |
| 2 | Lever 4 | m_csa:191 | family_panel_expert_import_decision | pending_expert_import_decision |
| 2 | Lever 4 | m_csa:448 | family_panel_expert_import_decision | pending_expert_import_decision |
| 2 | Lever 4 | m_csa:973 | family_panel_expert_import_decision | pending_expert_import_decision |
| 3 | Lever 2 | m_csa:3 | source_free_locator_rewrite_approval | pending_reviewer_decision |
| 3 | Lever 2 | m_csa:9 | source_free_locator_rewrite_approval | pending_reviewer_decision |
| 3 | Lever 2 | m_csa:32 | source_free_locator_rewrite_approval | pending_reviewer_decision |
| 3 | Lever 2 | m_csa:43 | source_free_locator_rewrite_approval | pending_reviewer_decision |
| 3 | Lever 2 | m_csa:44 | source_free_locator_rewrite_approval | pending_reviewer_decision |

## Interpretation

- No active Lever 2/3/4 gate is mechanically runnable on the current decision state.
- Lever 3 is blocked by the P10746 policy caveat, Lever 4 is blocked before import preview by expert import decisions, and Lever 2 is blocked by locator approvals plus source-free event-axis linkers.
- Review the first twelve queued rows here, starting with P10746 and the six Lever 4 import-preview candidates. After decisions land, regenerate this audit to verify a mechanical gate is actually open.
