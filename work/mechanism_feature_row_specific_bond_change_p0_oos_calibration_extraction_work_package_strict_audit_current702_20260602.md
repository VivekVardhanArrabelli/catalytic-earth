# Mechanism Feature Row-Specific Bond-Change P0 OOS Calibration Extraction Work Package Strict Audit - current702

Run: 2026-06-02T09:49:45Z

Validation-only audit for the P0 OOS calibration extraction work package. It confirms the packet stays manual-only, train/cal-only, OOS-only, and template-complete before any reviewer extraction work.

## Status

- p0_oos_calibration_extraction_work_package_strict_audit_passed
- Manual extraction rows: 30
- Required fields: 9
- Critical violations: 0

## Critical Counts

- rows_not_train_or_calibration: 0
- heldout_rows: 0
- non_oos_rows: 0
- missing_manual_template_fields: 0
- rows_allowed_for_feature_contract_consumption_now: 0
- rows_allowed_for_model_training_now: 0
- rows_with_materialized_source_evidence_status: 0

## Interpretation

- The P0 OOS calibration extraction package is valid as a manual-only review packet.
- Use the packet only for source-evidence extraction; do not materialize features until approved rows pass the sidecar guardrails.
