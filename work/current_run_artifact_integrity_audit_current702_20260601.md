# Current Run Artifact Integrity Audit - current702

Run: 2026-06-02T07:27:52Z

Current automation-run integrity audit for P0 train/cal row-specific feature materialization, its calibration review gate, existing northstar carryovers, and docs-reference maintenance outputs.

## Status

- current_run_artifact_integrity_audit_passed
- JSON artifacts checked: 30
- JSON artifacts parse-passed: 30
- Work reports present: 30
- Repo JSON parse errors: 0

## Artifact Rows

| category | artifact status | JSON parse | report present |
| --- | --- | --- | --- |
| fold_channel_coordinate_provenance | coordinate_bundle_not_persisted_results_parseable | True | True |
| fold_channel_reproduction_manifest | fold_channel_reproduction_manifest_ready_missing_coordinates | True | True |
| fold_channel_carryover_resolution | fold_channel_carryover_resolved_no_rerun_needed | True | True |
| fold_augmented_confounded_deployment_closure_audit | confounded_fold_channel_research_ready_production_blocked | True | True |
| predicted_atlas_vs_fold_novelty_delta | predicted_atlas_vs_fold_novelty_delta_ready_review_only | True | True |
| mechanism_feature_schema | row_specific_bond_change_schema_staged_no_fit | True | True |
| mechanism_feature_gap_guardrail | row_specific_bond_change_gap_not_consumed_by_feature_contract | True | True |
| mechanism_feature_gap_priority | row_specific_bond_change_materialization_priority_ready_no_fit | True | True |
| mechanism_feature_p0_source_graph_readiness | p0_source_graph_context_ready_bond_events_not_structured | True | True |
| mechanism_feature_p0_extraction_work_package | p0_row_specific_bond_change_extraction_work_package_ready_manual_only | True | True |
| mechanism_feature_p0_extraction_strict_audit | p0_extraction_work_package_strict_audit_passed | True | True |
| mechanism_feature_p0_source_evidence_schema | p0_source_evidence_sidecar_schema_staged_no_fit | True | True |
| mechanism_feature_p0_source_evidence_sidecar | p0_source_evidence_sidecar_partially_approved_review_required | True | True |
| mechanism_feature_p0_source_evidence_strict_audit | p0_source_evidence_sidecar_strict_audit_passed_reviewed_consumable | True | True |
| mechanism_feature_p0_source_evidence_review_queue | p0_source_evidence_review_queue_ready_manual_only | True | True |
| mechanism_feature_p0_rhea_lookup_resolution | p0_rhea_lookup_resolution_partial_review_only | True | True |
| mechanism_feature_p0_rhea_lookup_manifest | p0_rhea_lookup_manifest_ready_manual_only | True | True |
| mechanism_feature_p0_rhea_resolution_consumption_audit | p0_rhea_resolution_consumption_audit_passed_review_only | True | True |
| mechanism_feature_p0_rhea_unresolved_official_source_audit | p0_rhea_unresolved_official_source_audit_ready_review_only | True | True |
| mechanism_feature_p0_reviewer_decision_matrix | p0_reviewer_decision_matrix_copy_ready_reviewed | True | True |
| mechanism_feature_p0_feature_readiness_audit | p0_feature_readiness_audit_blocked_review_required | True | True |
| mechanism_feature_p0_refresh_blocker_audit | p0_no_template_feature_refresh_partially_unblocked_review_remaining | True | True |
| mechanism_feature_p0_train_cal_feature_sidecar | p0_train_cal_row_specific_feature_sidecar_ready_partial_no_fit | True | True |
| mechanism_feature_p0_train_cal_coverage_gap | p0_train_cal_feature_coverage_gap_ready_review_queue | True | True |
| mechanism_feature_p0_calibration_review_packet | p0_calibration_review_packet_ready_manual_only | True | True |
| mechanism_feature_p0_train_cal_feature_guardrail_audit | p0_train_cal_feature_guardrail_audit_passed_partial_no_fit | True | True |
| family_panel_readiness | glycyl_radical_panel_ready_as_oos_boundary_review_only | True | True |
| family_panel_no_template_feature_guardrail | glycyl_radical_panel_no_template_feature_guardrail_ready_review_only | True | True |
| source_free_locator_decision_matrix | source_free_locator_human_decision_matrix_ready_review_only | True | True |
| docs_reference_check | current_docs_artifact_references_passed | True | True |

## Validation

- catalytic_earth_cli_validate: passed; 12 source records, 8 fingerprints, 15 ontology families, 702 labels
- compileall: passed
- current_docs_artifact_reference_check: passed; 552 references checked, 0 missing
- disk_check: passed; 26Gi available on /System/Volumes/Data
- focused_new_tests: passed; 35 P0 row-specific train/cal tests and current-count regressions
- full_pytest: passed; 1167 tests, 50 subtests, 1 existing sklearn/scipy deprecation warning
- git_diff_check: passed
- repo_json_parse_sweep: passed; 3142 JSON and 26 JSONL artifact files parsed with 0 errors
- touched_pytest_files: passed; 178 tests and 7 subtests
- unittest_discovery: passed; 1122 tests, 1 existing sklearn/scipy deprecation warning

## Next Action

- Review m_csa:186, m_csa:147, m_csa:6, and m_csa:133 in the calibration packet; record approve/rewrite/reject decisions before rerunning no-template methods.
