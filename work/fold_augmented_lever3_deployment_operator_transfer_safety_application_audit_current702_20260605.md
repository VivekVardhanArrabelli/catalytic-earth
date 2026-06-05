# Fold-Augmented Lever 3 Deployment Operator Transfer-Safety Application Audit - current702

Run: 2026-06-05T14:21:04Z

Application audit for the reproducible Lever 3 operator transfer-safety matrix. It verifies the matrix source path, source hashes, rebuild stability, safe abstain/route actions, and fail-closed scoring behavior before operator use.

## Status

- fold_augmented_lever3_deployment_operator_transfer_safety_application_audit_passed
- Transfer-safety application ready: True
- Transfer-safety matrix reproducible: True
- Mechanism transfer disallowed for all rows: True
- Fixed-threshold scoring closure available now: False
- Application violations: []

## Counts

- Application operator rows safe-to-abstain/route: 21/21
- Transfer-safety matrix rows: 5
- Mechanism-transfer-allowed rows: 0
- Route-class stage-source links hash-current: 7/7
- Direct source hashes current: 2/2
- Matrix rebuild difference count: 0
- Calibration retention: 31/34
- Train/cal OOS abstain or route: 167/204
- Retained residual rows after all counteraxes: 0
- Route class counts: {'cofactor_or_same_family_confound': 11, 'fold_similarity_confound': 4, 'pocket_chemistry_confound': 1, 'pocket_geometry_confound': 3, 'protein_descriptor_counteraxis': 2}

## Application Checks

| check | passed |
| --- | ---: |
| transfer_safety_matrix_readout_passed | True |
| transfer_safety_matrix_reproducibility_audit_passed | True |
| direct_source_hashes_current | True |
| matrix_path_matches_reproducibility_source | True |
| matrix_rebuild_matches_stored | True |
| all_operator_rows_safe_to_apply_abstain_route | True |
| mechanism_transfer_disallowed_for_all_rows | True |
| no_scoring_forced_label_or_threshold_actions | True |
| route_class_and_provenance_metrics_stable | True |
| operating_point_metrics_stable | True |
| fixed_threshold_scoring_fail_closed | True |
| predicted_source_free_evidence_sufficient_for_safe_abstention | True |
| no_forbidden_guardrail_hits_in_sources | True |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Operator action: apply_reproducible_transfer_safety_matrix_for_abstain_route_only
- Next gate: Apply the reproducible transfer-safety matrix only for abstain/route novel-OOS decisions; keep mechanism transfer and fixed-threshold scoring closure fail-closed pending exact P07658 evidence.

## Guardrails

- Measured readout only. Existing transfer-safety matrix and reproducibility artifacts only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 transfer-safety application audit is ready.
- 21/21 operator rows remain safe-to-abstain/route with mechanism transfer allowed for 0 rows.
- Use the reproducible transfer-safety matrix only for abstain/route.
