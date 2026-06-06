# Fold-Augmented Lever 3 Deployment Contract Readiness Audit - current702

Run: 2026-06-05T11:08:29Z

Deployment-contract readiness audit for the current Lever 3 abstain/route operating point. It consumes the accepted row-level application audit and verifies that the operating-point contract is source-current, threshold-locked, row-action complete, guardrail-clean, and fail-closed for fixed-threshold scoring.

## Status

- fold_augmented_lever3_deployment_contract_readiness_audit_passed
- Deployment contract ready: True
- Safe abstention route remains current: True
- Fixed-threshold scoring closure available now: False
- Readiness violations: []

## Operating Point

- Route ID: fixed_baseline_plus_accepted_counteraxes_plus_descriptor_plus_channel_margin_fold_pressure_plus_pocket_chemistry_plus_geometry_mismatch
- Baseline threshold: 0.44155
- Accepted threshold: 0.44155
- Threshold selection source: train_calibration_only
- Threshold/value changed now: False
- Calibration retained: 31/34 (0.911765)
- Train/cal OOS abstained or routed: 167/204 (0.818627)
- Retained residual rows after all counteraxes: 0

## Counts

- Application rows abstain/route: 21/21
- Application rows with stage source: 21/21
- Source hashes current: 2/2
- Route stages with rows: 8
- Forced mechanism-label rows: 0
- Unsafe non-abstain residual action rows: 0

## Readiness Checks

| check | passed |
| --- | ---: |
| application_audit_passed | True |
| application_checks_all_pass | True |
| application_source_hashes_current | True |
| hard_residual_rows_present | True |
| all_hard_residual_rows_abstain_or_route | True |
| all_hard_residual_rows_have_stage_source | True |
| route_stage_counts_match_application_audit | True |
| no_forced_mechanism_labels | True |
| no_unsafe_non_abstain_actions | True |
| application_rows_not_used_for_rule_selection | True |
| zero_retained_residual_rows | True |
| zero_residual_rows_without_final_route | True |
| true_in_scope_retention_above_90_percent | True |
| train_cal_oos_operating_point_measured | True |
| accepted_threshold_locked_to_0_44155 | True |
| threshold_selected_on_train_cal_only | True |
| threshold_not_changed | True |
| fixed_threshold_scoring_fail_closed | True |
| safe_abstention_evidence_sufficient | True |
| exact_missing_scoring_evidence_named | True |
| measured_non_blocker_artifact | True |
| no_new_rule_or_threshold_selection | True |
| no_row_scoring_provider_or_coordinate_changes | True |
| no_heldout_metadata_or_forbidden_feature_shortcuts | True |
| no_label_registry_ontology_import_changes | True |

## Route Stages

| route stage | rows | entry ids |
| --- | ---: | --- |
| accepted_cofactor_or_same_family_bandpass | 10 | m_csa:135, m_csa:223, m_csa:289, m_csa:451, m_csa:463, m_csa:464, m_csa:488, m_csa:502, m_csa:503, m_csa:646 |
| channel_margin_counteraxis | 2 | m_csa:89, m_csa:229 |
| descriptor_generalization_counteraxis | 1 | m_csa:25 |
| fold_cofactor_pressure_counteraxis | 1 | m_csa:638 |
| fold_tm_bandpass_counteraxis | 4 | m_csa:52, m_csa:74, m_csa:190, m_csa:256 |
| geometry_mismatch_counteraxis | 1 | m_csa:308 |
| pairwise_descriptor_counteraxis | 1 | m_csa:84 |
| pocket_chemistry_counteraxis | 1 | m_csa:468 |

## Source Hashes

| source | hash current | path |
| --- | ---: | --- |
| closure_reproducibility_audit | True | artifacts/v3_fold_augmented_lever3_closure_reproducibility_audit_current702_20260605.json |
| operating_point_closure_readout | True | artifacts/v3_fold_augmented_lever3_operating_point_closure_readout_current702_20260605.json |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Operator contract action: abstain_or_route_novel_oos_for_all_hard_confounded_residual_rows
- Operator contract prohibitions: ['do_not_force_mechanism_labels', 'do_not_change_threshold_0.44155', 'do_not_claim_fixed_threshold_scoring_closure', 'do_not_use_heldout_or_experimental_pdb_metadata_shortcuts']
- Exact missing evidence for scoring closure: ['one credentialed provider route or local predictor that accepts the exact 715-aa P07658 FASTA', 'returned full-length coordinate file at the preferred staging path', 'filled provenance with provider/model/version/path/checksum, input sequence hash, and documented U140 handling', 'P07658 acceptance preflight with all required checks passing']
- Next gate: Use this deployment contract as the current Lever 3 operating-point readout; fixed-threshold scoring closure remains fail-closed pending the separate exact P07658 coordinate/provenance route and acceptance preflight.

## Guardrails

- Measured readout only. Existing application audit only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 deployment contract is ready at the operating point.
- 21/21 hard residual rows abstain or route novel/OOS, 31/34 calibration in-scope rows are retained, and 167/204 train/cal OOS rows abstain or route at threshold 0.44155.
- Use this as the operator-facing Lever 3 abstain/route contract; keep scoring closure fail-closed until the exact P07658 coordinate/provenance route exists.
