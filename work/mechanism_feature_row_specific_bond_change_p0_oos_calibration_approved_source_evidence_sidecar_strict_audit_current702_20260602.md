# Mechanism Feature Row-Specific Bond-Change P0 OOS Calibration Approved Source-Evidence Sidecar Strict Audit - current702

Run: 2026-06-02T10:28:17Z

Strict audit for approved OOS calibration source-evidence rows. It verifies OOS train/cal split safety, source spans, Rhea spans, review provenance, and non-training guardrails.

## Status

- p0_oos_calibration_approved_source_evidence_sidecar_strict_audit_passed
- Sidecar rows: 28
- Approved rows: 28
- Feature-contract consumable rows: 28
- Critical violations: 0
- Violation counts: {}

## Interpretation

- The approved OOS calibration rows pass source-evidence and split-safety audit.
- Merge audited OOS rows with approved P0 rows, materialize label-stripped train/cal event features, and rerun no-template centroid/residual calibration.
