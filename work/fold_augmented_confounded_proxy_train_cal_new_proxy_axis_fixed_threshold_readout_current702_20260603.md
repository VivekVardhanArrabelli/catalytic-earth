# Fold-Augmented Confounded Proxy Train/Cal New Proxy-Axis Fixed-Threshold Readout - current702

Run: 2026-06-03T17:25:38Z

Train/cal-only fixed-threshold readout for the newly contracted source-free proxy-axis tranche. It reports the six scored rows at the already selected combined geometry/fold threshold and does not rerun the global operating-point audit, tune thresholds, read heldout rows, edit labels, or count new benchmark labels.

## Status

- fold_augmented_confounded_proxy_train_cal_new_proxy_axis_fixed_threshold_readout_ready
- Fixed threshold: 0.44155
- Full-channel rows: 6
- Abstained/retained at fixed threshold: 1/5
- Blockers: []

## Decision

- Global operating-point audit ready now: False
- New proxy axis closes structural shortfall now: False
- Next gate: Do not rerun the global fixed-threshold audit from this readout alone. The new axis contributes 1 abstained rows at the fixed threshold; clear prior/base surface blockers or add additional train/cal proxy evidence before any operating-point claim.

## Row Readout

| row | combined | margin | abstains | nearest train | top1 |
| --- | ---: | ---: | --- | --- | --- |
| m_csa:89 | 0.45 | 0.00845 | False | m_csa:83 | metal_dependent_hydrolase |
| m_csa:143 | 0.49495 | 0.0534 | False | m_csa:142 | metal_dependent_hydrolase |
| m_csa:90 | 0.49735 | 0.0558 | False | m_csa:445 | ser_his_acid_hydrolase |
| m_csa:253 | 0.5158 | 0.07425 | False | m_csa:528 | metal_dependent_hydrolase |
| m_csa:501 | 0.601 | 0.15945 | False | m_csa:716 | metal_dependent_hydrolase |
| m_csa:466 | 0.38555 | -0.056 | True | m_csa:412 | ser_his_acid_hydrolase |

## Interpretation

- 1/6 new proxy-axis rows abstain at the unchanged fixed threshold.
- The active-site-count proxy axis is now deployably scored, but its fixed-threshold contribution is too small to close the Lever 3 structural proxy shortfall by itself.
- Keep this as a tranche readout; do not promote it to an operating-point claim until the broader extended surface is complete or another pre-registered train/cal proxy axis is scored.
