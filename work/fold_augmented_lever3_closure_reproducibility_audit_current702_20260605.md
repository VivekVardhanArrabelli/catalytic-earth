# Fold-Augmented Lever 3 Closure Reproducibility Audit - current702

Run: 2026-06-05T10:10:38Z

Deployment-valid reproducibility and source-hash audit for the Lever 3 operating-point closure readout. It rebuilds the closure from its recorded source artifacts, normalizes only created_utc, and checks that the current abstain/route operating point remains hash-current, guardrail-clean, and safe against forced mechanism transfer without selecting rules or changing thresholds.

## Status

- fold_augmented_lever3_closure_reproducibility_audit_passed
- Deployment-valid reproducible operating point available: True
- Safe abstention route remains current: True
- Fixed-threshold scoring closure available now: False
- Audit violations: []

## Reproducibility

- Closure artifact: v3_fold_augmented_lever3_operating_point_closure_readout_current702_20260605
- Normalized rebuild matches stored closure: True
- Stored normalized SHA-256: 764bd8314cec1505e1733491d18826e6b2c7c48dbd0ecf837f02a40a922c8a14
- Rebuilt normalized SHA-256: 764bd8314cec1505e1733491d18826e6b2c7c48dbd0ecf837f02a40a922c8a14
- Rebuild error: None

## Operating Point

- Route ID: fixed_baseline_plus_accepted_counteraxes_plus_descriptor_plus_channel_margin_fold_pressure_plus_pocket_chemistry_plus_geometry_mismatch
- Baseline threshold: 0.44155
- Threshold selection source: train_calibration_only
- Calibration retained: 31/34 (0.911765)
- Train/cal OOS abstained or routed: 167/204 (0.818627)
- Retained residual rows after all counteraxes: 0

## Counts

- Direct source records hash-current: 5/5
- Nested source records hash-current: 34/34
- Closure rebuild difference count: 0
- Forced mechanism-label rows: 0
- Unsafe non-abstain residual action rows: 0

## Closure Checks

| check | passed |
| --- | ---: |
| closure_source_hashes_current | True |
| nested_source_hashes_current | True |
| closure_rebuild_matches_stored_after_created_utc_normalization | True |
| closure_status_closed | True |
| closure_guardrail_violations_absent | True |
| closure_guardrail_checks_pass | True |
| closure_source_status_checks_pass | True |
| zero_residual_retained_rows | True |
| all_hard_residual_rows_routed | True |
| no_forced_mechanism_labels | True |
| residual_application_rows_not_rule_selection | True |
| calibration_retention_above_90_percent | True |
| train_cal_oos_abstention_operating_point_present | True |
| fixed_threshold_scoring_closure_remains_fail_closed | True |
| threshold_unchanged | True |
| no_row_scoring_or_provider_calls | True |
| no_coordinate_generation_or_staging | True |
| no_heldout_or_metadata_shortcuts | True |
| no_label_registry_ontology_or_import_changes | True |
| no_forbidden_predictive_feature_flags | True |

## Direct Source Hashes

| source | current | path |
| --- | ---: | --- |
| deployment_action_readout | True | artifacts/v3_fold_augmented_lever3_deployment_action_readout_current702_20260604.json |
| retained_channel_margin_counteraxis_readout | True | artifacts/v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604.json |
| retained_geometry_mismatch_counteraxis_readout | True | artifacts/v3_fold_augmented_lever3_retained_geometry_mismatch_counteraxis_readout_current702_20260605.json |
| retained_pairwise_descriptor_counteraxis_readout | True | artifacts/v3_fold_augmented_lever3_retained_pairwise_descriptor_counteraxis_readout_current702_20260604.json |
| retained_pocket_chemistry_counteraxis_readout | True | artifacts/v3_fold_augmented_lever3_retained_pocket_chemistry_counteraxis_readout_current702_20260605.json |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Exact missing evidence for scoring closure: ['one credentialed provider route or local predictor that accepts the exact 715-aa P07658 FASTA', 'returned full-length coordinate file at the preferred staging path', 'filled provenance with provider/model/version/path/checksum, input sequence hash, and documented U140 handling', 'P07658 acceptance preflight with all required checks passing']
- Next gate: Keep using the closure readout as the current Lever 3 abstain/route operating point; do not change threshold 0.44155 or force mechanism labels. Fixed-threshold scoring closure remains a separate exact P07658 coordinate/provenance preflight task.

## Guardrails

- Measured readout only. Existing source-free closure/source artifacts only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 closure is reproducible and source-hash current.
- The stored closure rebuilds with only created_utc normalized, keeps 31/34 calibration in-scope rows, routes 167/204 train/cal OOS rows, and leaves 0 retained hard residual rows.
- Use the closure as the current deployment-valid abstain/route readout; keep fixed-threshold scoring fail-closed pending the separate exact P07658 coordinate/provenance route.
