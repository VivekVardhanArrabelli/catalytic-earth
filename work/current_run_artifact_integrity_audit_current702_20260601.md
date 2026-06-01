# Current Run Artifact Integrity Audit - current702

Run: 2026-06-01T20:13:09Z

Current automation-run integrity audit for fold reproduction, mechanism-feature bond-change source-evidence draft artifacts, Rhea lookup handoff, family-panel readiness, locator decision, and docs-reference maintenance outputs.

## Status

- current_run_artifact_integrity_audit_passed
- JSON artifacts checked: 16
- JSON artifacts parse-passed: 16
- Work reports present: 16
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
| mechanism_feature_p0_source_evidence_sidecar | p0_source_evidence_sidecar_draft_review_required | True | True |
| mechanism_feature_p0_source_evidence_strict_audit | p0_source_evidence_sidecar_strict_audit_passed_draft_not_consumable | True | True |
| mechanism_feature_p0_source_evidence_review_queue | p0_source_evidence_review_queue_ready_manual_only | True | True |
| mechanism_feature_p0_rhea_lookup_manifest | p0_rhea_lookup_manifest_ready_manual_only | True | True |
| family_panel_readiness | glycyl_radical_panel_ready_as_oos_boundary_review_only | True | True |
| source_free_locator_decision_matrix | source_free_locator_human_decision_matrix_ready_review_only | True | True |
| docs_reference_check | current_docs_artifact_references_passed | True | True |

## Validation

- focused source-evidence tests: passed
- full pytest: passed; 1119 tests, 40 subtests, 1 sklearn warning
- unittest discovery: passed; 1096 tests
- compileall: passed
- catalytic_earth CLI validate: passed; 702 curated mechanism labels
- current-docs artifact reference check: passed; 481 references checked, 0 missing
- repo JSON parse sweep: passed; 3123 JSON and 25 JSONL files parsed with 0 errors
- git diff check: passed
- disk check: passed; 28 GiB available

## Next Action

- Manually resolve the P0 Rhea lookup manifest in order (`m_csa:124`, `m_csa:11`, `m_csa:169`, `m_csa:5`), update the draft source-evidence sidecar, then rerun strict audit and review queue before any feature-contract refresh.
