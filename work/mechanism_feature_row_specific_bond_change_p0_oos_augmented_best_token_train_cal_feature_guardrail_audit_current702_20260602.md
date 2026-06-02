# Mechanism Feature Row-Specific Bond-Change P0 Train/Cal Feature Guardrail Audit - current702

Run: 2026-06-02T11:35:00Z

Strict leakage and split-contract audit for the best-token OOS-augmented P0 train/cal row-specific feature sidecar.

## Status

- p0_oos_augmented_best_token_train_cal_feature_guardrail_audit_passed
- Feature rows: 43
- Train rows: 11
- Calibration rows: 32
- Feature value types: {'bool': 185, 'int': 559}
- Critical violations: 0

## Decision

- Partial feature surface guardrail passed: True
- Safe to run no-template methods now: True

## Predictive Feature Contract

- Payload: feature_rows[].row_specific_event_features
- Allowed value types: bool, int, float
- Forbidden inputs: entry_id, assigned_embedding_split, source text, source IDs, reviewer metadata, accession, fingerprint or labels, heldout outcomes, target names, EC/Rhea IDs

## Critical Counts

- feature_rows_missing_entry_id: 0
- duplicate_feature_entry_ids: 0
- unexpected_feature_row_keys: 0
- feature_rows_not_in_source_sidecar: 0
- feature_rows_source_not_approved: 0
- feature_rows_source_not_consumable: 0
- feature_rows_label_manifest_heldout: 0
- feature_rows_not_train_or_calibration: 0
- feature_rows_marked_heldout: 0
- feature_rows_missing_feature_payload: 0
- feature_payload_forbidden_keys: 0
- feature_payload_non_scalar_or_string_values: 0
- feature_guardrail_mismatches: 0

## Interpretation

- The partial P0 train/cal feature sidecar passes leakage and split guardrails for train-only feature materialization.
- Run the best-token no-template centroid/residual rerun on this guardrail-passing train/cal-only surface.
