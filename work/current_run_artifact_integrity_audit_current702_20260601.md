# Current Run Artifact Integrity Audit - current702

Run: 2026-06-02T01:06:58Z

Current automation-run integrity audit for fold reproduction, predicted-atlas/fold novelty delta, mechanism-feature bond/proton/electron readiness, P0 Rhea official-source and reviewer-decision outputs, family-panel guardrails, locator decision, and docs-reference maintenance outputs.

## Status

- current_run_artifact_integrity_audit_passed
- JSON artifacts checked: 23
- JSON artifacts parse-passed: 23
- Work reports present: 23
- Repo JSON parse errors: 0

## Artifact Rows

| category | artifact status | JSON parse | report present |
| --- | --- | --- | --- |
| fold_channel_coordinate_provenance | coordinate_bundle_not_persisted_results_parseable | True | True |
| fold_channel_reproduction_manifest | fold_channel_reproduction_manifest_ready_missing_coordinates | True | True |
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
| family_panel_readiness | glycyl_radical_panel_ready_as_oos_boundary_review_only | True | True |
| family_panel_no_template_feature_guardrail | glycyl_radical_panel_no_template_feature_guardrail_ready_review_only | True | True |
| source_free_locator_decision_matrix | source_free_locator_human_decision_matrix_ready_review_only | True | True |
| docs_reference_check | current_docs_artifact_references_passed | True | True |

## Validation

- focused_new_tests: passed; unresolved-Rhea official-source audit, reviewer decision matrix, Rhea resolution/consumption, artifact regressions, and CLI registration focused slices
- compileall: passed
- catalytic_earth_cli_validate: passed; 12 source records, 8 fingerprints, 15 ontology families, 702 labels
- current_docs_artifact_reference_check: passed; 494 references checked, 0 missing
- repo_json_parse_sweep: passed; 3136 JSON and 26 JSONL files parsed with 0 errors
- unittest_discovery: passed; 1112 tests, 1 existing sklearn/scipy deprecation warning
- full_pytest: passed; 1135 tests, 1 existing sklearn/scipy deprecation warning
- git_diff_check: passed
- disk_check: passed; 28 GiB available
- validation_soak: passed; 22 clean initial iterations through 41.9 minutes, timestamp file overwrite detected/restored from active lock, then 7 guarded iterations through 50.9 minutes

## Next Action

- Use the P0 reviewer decision matrix for m_csa:11, m_csa:169, and m_csa:5; record reviewer provenance before any train/cal no-template feature-contract refresh.
