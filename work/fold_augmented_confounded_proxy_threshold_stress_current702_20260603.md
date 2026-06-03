# Fold-Augmented Confounded Proxy Threshold Stress - current702

Run: 2026-06-03T12:20:58Z

Train/cal-only counterfactual threshold stress for Lever 3 confounded proxy rows. It reports the in-scope retention cost of forcing proxy abstention targets, without changing the fixed operating threshold or reading heldout rows.

## Status

- fold_augmented_confounded_proxy_threshold_stress_ready
- Blockers: ['structural_proxy_80pct_abstain_breaks_85pct_in_scope_retention', 'high_cofactor_proxy_80pct_abstain_breaks_90pct_in_scope_retention']
- Fixed channel: combined_mean_geometry_fold
- Fixed threshold: 0.44155
- Calibration in-scope rows: 34

## Stress

| subset | rows | fixed abstain | target | counterfactual threshold | proxy abstain | in-scope retain |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| high_cofactor_signature_proxy | 1 | 0.0 | 0.5 | 0.4682 | 1.0 | 0.8824 |
| high_cofactor_signature_proxy | 1 | 0.0 | 0.8 | 0.4682 | 1.0 | 0.8824 |
| high_cofactor_signature_proxy | 1 | 0.0 | 1.0 | 0.4682 | 1.0 | 0.8824 |
| same_family_structural_proxy | 17 | 0.2353 | 0.5 | 0.4806 | 0.5294 | 0.8235 |
| same_family_structural_proxy | 17 | 0.2353 | 0.8 | 0.62295 | 0.8235 | 0.4412 |
| same_family_structural_proxy | 17 | 0.2353 | 1.0 | 0.6621 | 1.0 | 0.2941 |
| all_expanded_calibration_oos | 75 | 0.4 | 0.5 | 0.46725 | 0.5067 | 0.8824 |
| all_expanded_calibration_oos | 75 | 0.4 | 0.8 | 0.5365 | 0.8 | 0.7353 |
| all_expanded_calibration_oos | 75 | 0.4 | 1.0 | 0.6621 | 1.0 | 0.2941 |

## Decision

- Apply or change threshold now: False
- Structural proxy 80% abstain retention ok: False
- High-cofactor proxy 80% abstain retention ok: False
- Next gate: Do not raise the fixed threshold from heldout behavior. The train/cal stress shows whether proxy abstention targets can be met while preserving calibration in-scope retention; use it to decide whether more train/cal proxy evidence is needed.

## Interpretation

- Counterfactual proxy-abstention thresholds are not adopted; they expose the train/cal retention cost of stricter confounded proxy behavior.
- If the retention cost is unacceptable, add or review more train/cal confounded proxy rows rather than changing the fixed operating point from heldout readout.
