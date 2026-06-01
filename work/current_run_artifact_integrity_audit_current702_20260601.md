# Current Run Artifact Integrity Audit - current702

Run: 2026-06-01T19:11:20Z

Current automation-run integrity audit for fold reproduction, mechanism-feature bond-change gap closure artifacts, family-panel readiness, locator decision, and docs-reference maintenance outputs.

## Status

- current_run_artifact_integrity_audit_passed
- JSON artifacts checked: 12
- JSON artifacts parse-passed: 12
- Work reports present: 12
- Repo JSON parse errors: 0

## Artifact Rows

| category | artifact status | JSON parse | report present |
| --- | --- | --- | --- |
| fold_channel_coordinate_provenance | coordinate_bundle_not_persisted_results_parseable | True | True |
| fold_channel_reproduction_manifest | fold_channel_reproduction_manifest_ready_missing_coordinates | True | True |
| mechanism_feature_schema | row_specific_bond_change_schema_staged_no_fit | True | True |
| mechanism_feature_gap_guardrail | row_specific_bond_change_gap_not_consumed_by_feature_contract | True | True |
| mechanism_feature_gap_priority | row_specific_bond_change_materialization_priority_ready_no_fit | True | True |
| mechanism_feature_p0_source_graph_readiness | p0_source_graph_context_ready_bond_events_not_structured | True | True |
| mechanism_feature_p0_extraction_work_package | p0_row_specific_bond_change_extraction_work_package_ready_manual_only | True | True |
| mechanism_feature_p0_extraction_strict_audit | p0_extraction_work_package_strict_audit_passed | True | True |
| mechanism_feature_p0_source_evidence_schema | p0_source_evidence_sidecar_schema_staged_no_fit | True | True |
| family_panel_readiness | glycyl_radical_panel_ready_as_oos_boundary_review_only | True | True |
| source_free_locator_decision_matrix | source_free_locator_human_decision_matrix_ready_review_only | True | True |
| docs_reference_check | current_docs_artifact_references_passed | True | True |

## Validation

- catalytic_earth_cli_validate: passed; 702 curated mechanism labels
- compileall: passed
- current_docs_artifact_reference_check: passed; 469 references checked, 0 missing
- full_pytest: passed; 1110 tests, 36 subtests, 1 sklearn deprecation warning
- git_diff_check: passed
- repo_json_parse_sweep: passed; 3123 JSON and 26 JSONL files parsed with 0 errors
- unittest_discovery: passed; 1087 tests

## Next Action

- Fill the P0 row-specific bond-change extraction worksheet from source-backed M-CSA/Rhea/mechanism evidence, emit a sidecar conforming to the staged schema, and run a strict source-evidence sidecar audit before any no-fit feature-contract refresh.
