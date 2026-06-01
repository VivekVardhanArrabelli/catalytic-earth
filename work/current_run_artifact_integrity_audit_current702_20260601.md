# Current Run Artifact Integrity Audit - current702

Run: 2026-06-01T23:19:09Z

Current automation-run integrity audit for fold reproduction, predicted-atlas/fold novelty delta, mechanism-feature bond/proton/electron readiness, Rhea lookup resolution/consumption, family-panel guardrails, locator decision, and docs-reference maintenance outputs.

## Status

- current_run_artifact_integrity_audit_passed
- JSON artifacts checked: 21
- JSON artifacts parse-passed: 21
- Work reports present: 21
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
| mechanism_feature_p0_feature_readiness_audit | p0_feature_readiness_audit_blocked_review_required | True | True |
| family_panel_readiness | glycyl_radical_panel_ready_as_oos_boundary_review_only | True | True |
| family_panel_no_template_feature_guardrail | glycyl_radical_panel_no_template_feature_guardrail_ready_review_only | True | True |
| source_free_locator_decision_matrix | source_free_locator_human_decision_matrix_ready_review_only | True | True |
| docs_reference_check | current_docs_artifact_references_passed | True | True |

## Validation

- focused_new_tests: passed; Rhea resolution/consumption, predicted-atlas-vs-fold delta, current-run integrity, and CLI registration focused slices
- validation_soak: passed; 21 iterations of JSON parse, focused pytest, cli validate, and git diff --check through 50.1 elapsed minutes
- compileall: passed
- catalytic_earth_cli_validate: passed; 12 source records, 8 fingerprints, 15 ontology families, 702 labels
- current_docs_artifact_reference_check: passed; 492 references checked, 0 missing
- repo_json_parse_sweep: passed; 3134 JSON and 26 JSONL files parsed with 0 errors
- unittest_discovery: passed; 1108 tests, 1 existing sklearn/scipy deprecation warning
- full_pytest: passed; 1131 tests, 1 existing sklearn/scipy deprecation warning
- git_diff_check: passed
- disk_check: passed; 27 GiB available

## Next Action

- Resolve remaining P0 Rhea lookup rows m_csa:11, m_csa:169, and m_csa:5; add reviewer provenance before any train/cal no-template feature-contract refresh.
