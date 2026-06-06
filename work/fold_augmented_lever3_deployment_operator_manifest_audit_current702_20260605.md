# Fold-Augmented Lever 3 Deployment Operator Manifest Audit - current702

Run: 2026-06-05T12:09:33Z

Operator-manifest audit for the current Lever 3 abstain/route contract. It packages the accepted contract into a minimal row-action table and verifies threshold lock, source currency, safe abstain-only actions, and removal of leakage-prone fields.

## Status

- fold_augmented_lever3_deployment_operator_manifest_audit_passed
- Operator manifest ready: True
- Safe abstention route remains current: True
- Fixed-threshold scoring closure available now: False
- Manifest violations: []

## Operating Point

- Route ID: fixed_baseline_plus_accepted_counteraxes_plus_descriptor_plus_channel_margin_fold_pressure_plus_pocket_chemistry_plus_geometry_mismatch
- Baseline threshold: 0.44155
- Accepted threshold: 0.44155
- Threshold selection source: train_calibration_only
- Threshold/value changed now: False
- Calibration retained: 31/34
- Train/cal OOS abstained or routed: 167/204
- Retained residual rows after all counteraxes: 0

## Manifest Counts

- Manifest rows abstain/route: 21/21
- Source hashes current: 5/5
- Route stages with rows: 8
- Unsafe action rows: 0
- Forced mechanism-label rows: 0
- Rule-selection rows: 0
- Forbidden-field rows: 0
- Manifest SHA-256: e3de25919052c16e5a139ebd950885d3ca8bbc1cbafaa58ba37df5d346578fdf

## Operator Manifest Checks

| check | passed |
| --- | ---: |
| deployment_contract_reproducibility_audit_passed | True |
| deployment_contract_readiness_audit_passed | True |
| readiness_path_matches_reproducibility_source | True |
| all_source_hashes_current | True |
| manifest_row_count_matches_readiness | True |
| all_manifest_rows_abstain_or_route_novel_oos | True |
| no_manifest_rows_force_mechanism_labels | True |
| no_manifest_rows_used_for_rule_selection | True |
| all_manifest_rows_have_route_stage | True |
| all_manifest_rows_have_stage_source | True |
| all_manifest_rows_have_entry_id | True |
| manifest_route_stage_counts_match_readiness | True |
| manifest_contains_only_allowed_row_fields | True |
| manifest_strips_forbidden_predictive_fields | True |
| threshold_locked_to_train_cal_0_44155 | True |
| threshold_not_changed | True |
| fixed_threshold_scoring_fail_closed | True |
| safe_abstention_evidence_sufficient | True |
| no_heldout_metadata_or_forbidden_feature_shortcuts | True |

## Route Stages

| route_stage | rows |
| --- | ---: |
| accepted_cofactor_or_same_family_bandpass | 10 |
| channel_margin_counteraxis | 2 |
| descriptor_generalization_counteraxis | 1 |
| fold_cofactor_pressure_counteraxis | 1 |
| fold_tm_bandpass_counteraxis | 4 |
| geometry_mismatch_counteraxis | 1 |
| pairwise_descriptor_counteraxis | 1 |
| pocket_chemistry_counteraxis | 1 |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Exact missing evidence for scoring closure: ['one credentialed provider route or local predictor that accepts the exact 715-aa P07658 FASTA', 'returned full-length coordinate file at the preferred staging path', 'filled provenance with provider/model/version/path/checksum, input sequence hash, and documented U140 handling', 'P07658 acceptance preflight with all required checks passing']
- Next gate: Use this manifest only as the operator-facing abstain/route table; keep fixed-threshold scoring closure fail-closed pending exact P07658 coordinate/provenance evidence.

## Guardrails

- Measured readout only. Existing contract artifacts only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 operator manifest is ready for abstain/route use.
- 21 manifest rows, 0 unsafe non-abstain actions, 0 forced-label rows, and 0 forbidden-field rows.
- Apply only the manifest abstain/route actions; keep scoring closure fail-closed until the exact P07658 route passes.
