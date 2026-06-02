# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Source-Evidence Sidecar - current702

Run: 2026-06-02T10:28:18Z

Union source-evidence sidecar for approved P0 primary rows plus strict-audited OOS calibration rows. It is used only for split-filtered train/cal feature materialization.

## Status

- p0_oos_augmented_source_evidence_sidecar_ready
- P0 source rows: 15
- OOS source rows: 28
- Sidecar rows: 43
- Feature-contract consumable rows: 43
- OOS strict audit passed: True

## Interpretation

- Combined 15 P0 rows with 28 approved OOS calibration rows for a train/cal-only feature rerun.
- Materialize label-stripped row-specific event features from approved/consumable rows only.
