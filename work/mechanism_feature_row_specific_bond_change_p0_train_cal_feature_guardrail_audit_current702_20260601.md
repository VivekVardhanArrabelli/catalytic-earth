# Mechanism Feature Row-Specific Bond-Change P0 Train/Cal Feature Guardrail Audit - current702

Run: 2026-06-02T07:11:47Z

Strict leakage and split-contract audit for the partial P0 row-specific train/cal feature sidecar. Only `row_specific_event_features` is treated as predictive payload; entry IDs, splits, guardrails, source text, source IDs, reviewer metadata, labels, and heldout outcomes are excluded.

## Status

- p0_train_cal_feature_guardrail_audit_passed_partial_no_fit
- Feature rows: 3
- Train rows: 3
- Calibration rows: 0
- Feature value types: {'bool': 12, 'int': 39}
- Critical violations: 0

## Decision

- Partial feature surface guardrail passed: True
- Safe to run no-template methods now: False
- Reason: Only a partial approved P0 surface is materialized; continue review until train and calibration rows cover the intended no-template feature pilot.

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
- Use the calibration review packet to decide the four calibration-assigned draft rows, then rerun the strict sidecar, readiness, materialization, and this guardrail audit before any no-template centroid or residual rerun.
