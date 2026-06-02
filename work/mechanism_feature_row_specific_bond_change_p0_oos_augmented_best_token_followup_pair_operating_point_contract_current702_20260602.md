# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Operating-Point Contract - current702

Run: 2026-06-02T12:28:24Z

Calibration-only operating-point contract for the best-token follow-up pair row-specific feature surface. It freezes thresholds on calibration rows only and leaves heldout unread.

## Status

- p0_oos_augmented_best_token_followup_pair_operating_point_contract_ready_calibration_only
- Feature rows: 43
- Train rows: 11
- Calibration rows: 32
- Calibration OOS rows: 28

## Calibration Contract

- Centroid similarity threshold: 0.23726514
- Centroid OOS abstain recall: 0.857143
- Residual distance threshold: 3.21469422
- Residual OOS abstain recall: 0.857143
- Preferred contract: residual_distance_threshold

## Interpretation

- The OOS-augmented train/cal surface has a calibration-only operating point: both centroid similarity and residual distance retain all calibration primaries and abstain on 24/28 OOS rows.
- Use this follow-up pair residual-distance contract only after a heldout-safe application surface is materialized; do not retune on heldout.
