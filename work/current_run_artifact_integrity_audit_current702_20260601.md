# Current Run Artifact Integrity Audit - current702

Run: 2026-06-01T17:34:10Z

Current automation-run integrity audit for new/updated JSON artifacts and matching work reports from fold provenance, mechanism-feature schema/gap guards, family-panel readiness, locator decision matrix, and docs-reference maintenance outputs.

## Status

- current_run_artifact_integrity_audit_passed
- JSON artifacts checked: 6
- JSON artifacts parse-passed: 6
- Work reports present: 6
- Repo JSON parse errors: 0

## Artifact Rows

| category | artifact status | JSON parse | report present |
| --- | --- | --- | --- |
| fold_channel_coordinate_provenance | coordinate_bundle_not_persisted_results_parseable | True | True |
| mechanism_feature_schema | row_specific_bond_change_schema_staged_no_fit | True | True |
| mechanism_feature_gap_guardrail | row_specific_bond_change_gap_not_consumed_by_feature_contract | True | True |
| family_panel_readiness | glycyl_radical_panel_ready_as_oos_boundary_review_only | True | True |
| source_free_locator_decision_matrix | source_free_locator_human_decision_matrix_ready_review_only | True | True |
| docs_reference_check | current_docs_artifact_references_passed | True | True |

## Validation

- focused_northstar_tests: 45 passed
- focused_geometry_artifact_regression: 86 passed, 7 subtests passed
- full_pytest: 1098 passed, 31 subtests passed, 1 sklearn deprecation warning
- unittest_discovery: 1075 tests passed
- compileall: passed
- catalytic_earth_cli_validate: passed; 702 curated mechanism labels
- git_diff_check: passed
- repo_json_parse_sweep: 3113 JSON and 25 JSONL files parsed with 0 errors
- current_docs_artifact_reference_check: passed; 440 references checked, 0 missing

## Next Action

- Use the locator human-decision matrix to pick one policy decision, preferably mh_067/mh_068 locator-copy approval or rejection, before any further source-free geometry scoring.
