# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Expanded Calibration Comparison - current702

Run: 2026-06-02T11:18:35Z

Calibration-only comparison between the coarse OOS-augmented row-specific feature surface and the expanded retained-OOS target surface. It compares already-written rerun artifacts only; it does not fit new models, tune thresholds, or read heldout.

## Status

- p0_oos_augmented_expanded_calibration_comparison_ready
- Coarse dimensions: 17
- Expanded dimensions: 560
- Calibration rows: 32
- Calibration OOS rows: 28
- Critical violations: 0

## Residual Operating Point

| surface | threshold | OOS abstain recall | residual AUC |
| --- | ---: | ---: | ---: |
| coarse | 3.21469422 | 0.5 | 0.669643 |
| expanded | 19.31389136 | 0.035714 | 0.285714 |

## Deltas

- Expanded minus coarse residual OOS abstain recall: -0.464286
- Expanded minus coarse residual AUC: -0.383929

## Decision

- Expanded surface replaces frozen residual contract: False
- Recommended surface: coarse_oos_augmented_residual_contract
- Keep existing residual threshold: True
- Next gate: Do not promote the all-family expanded surface. Use the retained-OOS target artifact for a narrower ablation or regularized feature-family pass, and keep the coarse residual threshold frozen until a calibration contract beats it.

## Interpretation

- The expanded retained-OOS feature surface underperforms the coarse surface at the calibration operating point: residual OOS abstain recall delta is -0.464286 and residual AUC delta is -0.383929.
- Keep the coarse residual operating-point contract as the deployable candidate and run a narrower expanded-family ablation before any heldout read.
