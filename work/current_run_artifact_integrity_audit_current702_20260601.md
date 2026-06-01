# Current Run Artifact Integrity Audit - current702

Run: 2026-06-01T22:11:01Z

Current automation-run integrity audit for fold reproduction, mechanism-feature bond/proton/electron readiness, Rhea lookup handoff, family-panel guardrails, locator decision, and docs-reference maintenance outputs.

## Status

- current_run_artifact_integrity_audit_passed
- JSON artifacts checked: 18
- JSON artifacts parse-passed: 18
- Work reports present: 18
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
| mechanism_feature_p0_feature_readiness_audit | p0_feature_readiness_audit_blocked_review_required | True | True |
| family_panel_readiness | glycyl_radical_panel_ready_as_oos_boundary_review_only | True | True |
| family_panel_no_template_feature_guardrail | glycyl_radical_panel_no_template_feature_guardrail_ready_review_only | True | True |
| source_free_locator_decision_matrix | source_free_locator_human_decision_matrix_ready_review_only | True | True |
| docs_reference_check | current_docs_artifact_references_passed | True | True |

## Validation

- focused new tests: passed; 5 tests and 17 subtests
- changed file pytest: passed; 275 tests and 24 subtests
- full pytest: passed; 1124 tests, 43 subtests, 1 sklearn/scipy deprecation warning
- unittest discovery: passed; 1101 tests, 1 sklearn/scipy deprecation warning
- compileall: passed
- catalytic earth cli validate: passed; 702 curated mechanism labels
- current docs artifact reference check: passed; 489 references checked, 0 missing
- repo json parse sweep: passed; 3131 JSON and 26 JSONL files parsed with 0 errors
- git diff check: passed
- disk check: passed; 27 GiB available

## Next Action

- Resolve the four P0 Rhea lookup rows and reviewer provenance, rerun strict/readiness audits, then refresh only train/cal no-template feature contracts if the gate passes; keep m_csa:30/m_csa:31 as review-only heldout controls.
