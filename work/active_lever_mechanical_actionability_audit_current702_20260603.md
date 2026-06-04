# Active Lever Mechanical Actionability Audit - current702

Run: 2026-06-04T00:28:30Z

Review-only actionability audit across active Lever 2/3/4 gates. It distinguishes mechanical gates that can run now from explicit review or policy decisions that must remain fail-closed.

## Status

- active_lever_mechanical_actionability_blocked_external_decisions
- Decision items: 131
- External decisions required: 23
- Automation-action-allowed-now items: 0
- Mechanical gates ready now: 1
- Source-decision follow-on gate-ready rows: 0
- Source-decision pending rows: 23
- Source-decision invalid rows: 0
- Lever 2 pending locator approvals: 0
- Lever 2 pending event-axis signoffs: 0
- Lever 2 event-axis linker rows: 14
- Lever 2 event-axis signoff draft rows: 53
- Lever 2 event-axis pending signoff rows: 0
- Lever 2 event-axis explicit approved rows: 14
- Lever 2 event-axis gate-consumable signoff rows: 14
- Lever 2 event-axis priority 1/2/insufficient signoff rows: 3/11/33
- Lever 2 partial-surface policy ready: True
- Lever 2 partial-surface threshold read accepted: False
- Lever 2 partial-surface pair-feature rows: 53
- Lever 2 partial-surface missing-locator abstain rows: 87
- Lever 2 partial-surface operating-contract decision required: True
- Lever 2 partial-surface operating-contract blockers: 2
- Lever 3 structural proxy abstained: 10/55
- Lever 3 retained proxy gap rows: 48
- Lever 3 proxy stress blockers: 2
- Lever 3 proxy evidence request rows: 48
- Lever 3 high-cofactor min new abstained rows for 80%: 16
- Lever 3 structural min new abstained rows for 80%: 170
- Lever 3 proxy evidence-extension blockers: 6
- Lever 3 proxy acquisition family-panel eligible rows: 0
- Lever 3 proxy acquisition high-cofactor shortfall: 16
- Lever 3 proxy acquisition structural shortfall: 170
- Lever 3 proxy acquisition heldout-guardrail rows: 4
- Lever 3 proxy acquisition blockers: 6
- Lever 3 proxy candidate-pool unscored rows: 170
- Lever 3 proxy candidate-pool high-axis rows: 0
- Lever 3 proxy candidate-pool structural-axis rows: 0
- Lever 3 proxy scoring-tranche rows: 0
- Lever 3 proxy scoring-tranche high/structural rows: 0/0
- Lever 3 proxy scoring-tranche ready for plan: False
- Lever 3 proxy background-only rows: 170
- Lever 3 proxy background-axis exhausted: True
- Lever 3 proxy background-axis scout ready axes: 0/3
- Lever 3 unsupported-geometry coordinates observed/missing: 8/0
- Lever 3 unsupported-geometry locus evidence files: 0/8
- Lever 3 unsupported-geometry protein-only files: 8
- Lever 3 new proxy axis registered: True
- Lever 3 new proxy-axis contracted rows: 6
- Lever 3 new proxy-axis full-channel rows: 6
- Lever 3 new proxy-axis missing full-score rows: 0
- Lever 4 acceptance scenario rows: 6
- Lever 4 acceptance scenario panels: 5
- Lever 4 label-factory candidates if scenario accepted: 6
- Lever 4 label-factory gate input rows: 0
- Blockers: ['p10746_policy_decision_missing', 'lever3_confounded_structural_proxy_calibration_gap', 'lever3_confounded_proxy_threshold_stress_retention_cost', 'lever3_confounded_proxy_evidence_extension_scale_gap', 'lever3_confounded_proxy_acquisition_shortfall', 'lever3_confounded_proxy_train_cal_scoring_tranche_not_run', 'lever3_confounded_proxy_background_axis_exhausted', 'lever3_confounded_proxy_unsupported_geometry_locus_scan_no_axis', 'family_panel_expert_import_decisions_missing', 'family_panel_label_factory_gate_inputs_missing', 'lever2_partial_surface_operating_contract_decision_required', 'lever2_pre_threshold_readiness_not_ready']

## Decision

- Apply any decision gate now: False
- Copy locator sidecars now: False
- Apply frozen residual threshold now: False
- Run label-factory gate now: False
- Next gate: Record explicit decisions in the source packets with hashes unchanged. Then rerun only the matching application or materialization gates; do not read heldout or apply the frozen Lever 2 threshold until pre-threshold readiness passes.

## Gate Checks

| lever | gate | ready now | blocker | next command after decision |
| --- | --- | --- | --- | --- |
| Lever 2/3/4 | source_decision_intake_preflight | False | source_decision_follow_on_rows_already_consumed | build-active-lever-source-decision-intake-preflight |
| Lever 3 | p10746_post_decision_deployment_closure | False | p10746_policy_decision_missing | apply-fold-augmented-p10746-deployment-caveat-decision |
| Lever 3 | confounded_proxy_train_calibration | False | confounded_proxy_train_calibration_gap | build-fold-augmented-confounded-proxy-threshold-stress |
| Lever 3 | confounded_proxy_evidence_extension | False | confounded_proxy_evidence_extension_scale_gap | build-fold-augmented-confounded-proxy-evidence-extension-plan |
| Lever 3 | confounded_proxy_acquisition_queue | False | confounded_proxy_acquisition_shortfall | build-fold-augmented-confounded-proxy-acquisition-queue |
| Lever 3 | confounded_proxy_train_cal_candidate_pool | False | confounded_proxy_candidate_pool_not_scored | build-fold-augmented-confounded-proxy-train-cal-candidate-pool |
| Lever 3 | confounded_proxy_train_cal_scoring_tranche | False | confounded_proxy_scoring_tranche_not_run | build-fold-augmented-confounded-proxy-train-cal-scoring-tranche-plan |
| Lever 3 | confounded_proxy_train_cal_background_axis_blocker | False | confounded_proxy_remaining_rows_background_only | build-fold-augmented-confounded-proxy-train-cal-background-axis-blocker |
| Lever 3 | confounded_proxy_train_cal_background_axis_scout | False | current_scout_axis_scored_no_ready_followup_axis | build-fold-augmented-confounded-proxy-train-cal-background-axis-scout |
| Lever 3 | confounded_proxy_train_cal_unsupported_geometry_locus_scan | False | unsupported_geometry_afdb_coordinates_protein_only_no_locus_evidence | scan-fold-augmented-confounded-proxy-train-cal-unsupported-geometry-coordinate-loci |
| Lever 3 | confounded_proxy_train_cal_new_proxy_axis_contract | False | contracted_proxy_axis_fully_scored_surface_still_blocked | build-fold-augmented-confounded-proxy-train-cal-background-axis-scout |
| Lever 4 | family_panel_label_factory_gate_readiness | False | family_panel_expert_import_decisions_missing | apply-fold-augmented-family-panel-expert-import-decision |
| Lever 2 | source_free_partial_surface_operating_contract | False | deterministic_missing_locator_abstention_operating_contract_decision_required | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-partial-surface-operating-contract-preflight |
| Lever 2 | source_free_locator_materialization_and_pre_threshold_readiness | False | source_free_pre_threshold_readiness_blocked | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-locator-rewrite-materialization-gate |
| Lever 2 | source_free_event_axis_linkers | True | source_free_event_axis_linkers_materialized | build-mechanism-feature-row-specific-bond-change-p0-oos-augmented-best-token-followup-pair-source-free-event-axis-linker-materialization-gate |

## Next Review Items

| priority | lever | row | decision class | status | decision field |
| ---: | --- | --- | --- | --- | --- |
| 1 | Lever 3 | m_csa:204 | p10746_fold_only_deployment_caveat | pending_explicit_decision | decision |
| 2 | Lever 4 | m_csa:10 | family_panel_expert_import_decision | pending_expert_import_decision | decision |
| 2 | Lever 4 | m_csa:30 | family_panel_expert_import_decision | pending_expert_import_decision | decision |
| 2 | Lever 4 | m_csa:31 | family_panel_expert_import_decision | pending_expert_import_decision | decision |
| 2 | Lever 4 | m_csa:191 | family_panel_expert_import_decision | pending_expert_import_decision | decision |
| 2 | Lever 4 | m_csa:448 | family_panel_expert_import_decision | pending_expert_import_decision | decision |
| 2 | Lever 4 | m_csa:973 | family_panel_expert_import_decision | pending_expert_import_decision | decision |
| 4 | Lever 4 | m_csa:116 | family_panel_expert_import_decision | pending_expert_import_decision | decision |
| 4 | Lever 4 | m_csa:131 | family_panel_expert_import_decision | pending_expert_import_decision | decision |
| 4 | Lever 4 | m_csa:132 | family_panel_expert_import_decision | pending_expert_import_decision | decision |
| 4 | Lever 4 | m_csa:267 | family_panel_expert_import_decision | pending_expert_import_decision | decision |
| 4 | Lever 4 | m_csa:551 | family_panel_expert_import_decision | pending_expert_import_decision | decision |
| 2 | Lever 2 | current702_partial_surface | source_free_partial_surface_operating_contract | pending_explicit_policy_decision | decision |

## Interpretation

- 1 active Lever 2/3/4 gate mechanically ready on the current decision state.
- Lever 3 has a pre-registered source-free proxy-axis contract with 6 train/cal rows and 6 full-channel scores; the new tranche is complete, but calibration remains blocked by the existing fixed-threshold proxy and prior/base-surface gaps. The unsupported-geometry coordinate repair path scanned 8 AFDB-v6 train/cal files and found zero source-free inorganic/cofactor locus evidence. Lever 4 is blocked before import preview by expert import decisions, and Lever 2 locator approvals and event-axis signoffs are cleared. The partial policy has 53 source-free pair-feature rows and 87 missing-locator abstention rows, but the frozen threshold read remains blocked until complete locator coverage or an accepted missing-locator abstention operating contract exists.
- Review the next queued pending rows: P10746 policy decision; 6 Lever 4 import-preview candidates; Lever 2 partial-surface operating-contract decision. For Lever 3, the new proxy-axis tranche is fully scored. Do not rerun the fixed-threshold audit on a partial/base-blocked surface; clear the remaining prior/base full-channel and policy/calibration blockers first. Do not score or register the unsupported-geometry proxy from those AFDB files; use a different source-free protein-only structural proxy or reviewed P10746/Lever 4 decisions.
