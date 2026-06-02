# Current Run Artifact Integrity Audit - current702

Run: 2026-06-02T02:18:32Z

Current automation-run integrity audit for fold-channel carryover resolution, mechanism-feature P0 refresh blocker, existing northstar carryovers, and docs-reference maintenance outputs.

## Status

- current_run_artifact_integrity_audit_passed
- JSON artifacts checked: 25
- JSON artifacts parse-passed: 25
- Work reports present: 25
- Repo JSON parse errors: 0

## Artifact Rows

| category | artifact status | JSON parse | report present |
| --- | --- | --- | --- |
| fold_channel_coordinate_provenance | coordinate_bundle_not_persisted_results_parseable | True | True |
| fold_channel_reproduction_manifest | fold_channel_reproduction_manifest_ready_missing_coordinates | True | True |
| fold_channel_carryover_resolution | fold_channel_carryover_resolved_no_rerun_needed | True | True |
| predicted_atlas_vs_fold_novelty_delta | predicted_atlas_vs_fold_novelty_delta_ready_review_only | True | True |
| mechanism_feature_schema | row_specific_bond_change_schema_staged_no_fit | True | True |
| mechanism_feature_gap_guardrail | row_specific_bond_change_gap_not_consumed_by_feature_contract | True | True |
| mechanism_feature_gap_priority | row_specific_bond_change_materialization_priority_ready_no_fit | True | True |
| mechanism_feature_p0_source_graph_readiness | p0_source_graph_context_ready_bond_events_not_structured | True | True |
| mechanism_feature_p0_extraction_work_package | p0_row_specific_bond_change_extraction_work_package_ready_manual_only | True | True |
| mechanism_feature_p0_extraction_strict_audit | p0_extraction_work_package_strict_audit_passed | True | True |
| mechanism_feature_p0_source_evidence_schema | p0_source_evidence_sidecar_schema_staged_no_fit | True | True |
| mechanism_feature_p0_source_evidence_sidecar | p0_source_evidence_sidecar_draft_review_required | True | True |
| mechanism_feature_p0_source_evidence_strict_audit | p0_source_evidence_sidecar_strict_audit_passed_draft_not_consumable | True | True |
| mechanism_feature_p0_source_evidence_review_queue | p0_source_evidence_review_queue_ready_manual_only | True | True |
| mechanism_feature_p0_rhea_lookup_resolution | p0_rhea_lookup_resolution_partial_review_only | True | True |
| mechanism_feature_p0_rhea_lookup_manifest | p0_rhea_lookup_manifest_ready_manual_only | True | True |
| mechanism_feature_p0_rhea_resolution_consumption_audit | p0_rhea_resolution_consumption_audit_passed_review_only | True | True |
| mechanism_feature_p0_rhea_unresolved_official_source_audit | p0_rhea_unresolved_official_source_audit_ready_review_only | True | True |
| mechanism_feature_p0_reviewer_decision_matrix | p0_reviewer_decision_matrix_ready_review_only | True | True |
| mechanism_feature_p0_feature_readiness_audit | p0_feature_readiness_audit_blocked_review_required | True | True |
| mechanism_feature_p0_refresh_blocker_audit | p0_no_template_feature_refresh_blocked_review_required | True | True |
| family_panel_readiness | glycyl_radical_panel_ready_as_oos_boundary_review_only | True | True |
| family_panel_no_template_feature_guardrail | glycyl_radical_panel_no_template_feature_guardrail_ready_review_only | True | True |
| source_free_locator_decision_matrix | source_free_locator_human_decision_matrix_ready_review_only | True | True |
| docs_reference_check | current_docs_artifact_references_passed | True | True |

## Validation

- catalytic_earth_cli_validate: passed; 12 source records, 8 fingerprints, 15 ontology families, 702 labels
- compileall: passed
- current_docs_artifact_reference_check: passed; 500 references checked, 0 missing
- disk_check: pending final wrap disk check
- focused_new_tests: passed; fold-channel carryover resolution, P0 refresh-blocker, current-count regressions, and CLI registration focused slices
- full_pytest: passed; 1139 tests, 50 subtests, 1 existing sklearn/scipy deprecation warning
- git_diff_check: passed
- repo_json_parse_sweep: passed; 3138 JSON and 26 JSONL files parsed with 0 errors
- touched_pytest_files: passed; 290 tests and 31 subtests
- unittest_discovery: passed; 1116 tests, 1 existing sklearn/scipy deprecation warning

## Next Action

- Do not rerun the predicted-structure fold channel; use the P0 reviewer decision matrix to record reviewer provenance before any no-template feature-contract refresh.
