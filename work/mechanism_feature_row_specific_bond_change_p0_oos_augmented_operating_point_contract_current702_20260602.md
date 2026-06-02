# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Operating-Point Contract - current702

Run: 2026-06-02T10:28:18Z

Deployable calibration contract for the OOS-augmented P0 row-specific no-template centroid and residual diagnostics. It records train/cal-selected thresholds and does not read heldout.

## Status

- p0_oos_augmented_operating_point_contract_ready_calibration_only
- Feature rows: 43
- Train rows: 11
- Calibration rows: 32
- Calibration OOS rows: 28

## Calibration Contract

- Centroid similarity threshold: 0.23726514
- Centroid OOS abstain recall: 0.5
- Residual distance threshold: 3.21469422
- Residual OOS abstain recall: 0.5
- Preferred contract: residual_distance_threshold

## Interpretation

- The OOS-augmented train/cal surface has a calibration-only operating point: both centroid similarity and residual distance retain all calibration primaries and abstain on 14/28 OOS rows.
- Use the residual-distance contract as the heldout-safe frozen threshold candidate; do not tune it on heldout rows.
