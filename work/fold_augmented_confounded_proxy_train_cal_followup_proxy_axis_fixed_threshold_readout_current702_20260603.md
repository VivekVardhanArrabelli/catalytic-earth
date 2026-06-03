# Fold-Augmented Confounded Proxy Train/Cal New Proxy-Axis Fixed-Threshold Readout - current702

Run: 2026-06-03T18:10:11Z

Train/cal-only fixed-threshold readout for the newly contracted source-free proxy-axis tranche. It reports the six scored rows at the already selected combined geometry/fold threshold and does not rerun the global operating-point audit, tune thresholds, read heldout rows, edit labels, or count new benchmark labels.

## Status

- fold_augmented_confounded_proxy_train_cal_new_proxy_axis_fixed_threshold_readout_ready
- Fixed threshold: 0.44155
- Full-channel rows: 4
- Abstained/retained at fixed threshold: 1/3
- Blockers: []

## Decision

- Global operating-point audit ready now: False
- New proxy axis closes structural shortfall now: False
- Next gate: Do not rerun the global fixed-threshold audit from this readout alone. The new axis contributes 1 abstained rows at the fixed threshold; clear prior/base surface blockers or add additional train/cal proxy evidence before any operating-point claim.

## Row Readout

| row | combined | margin | abstains | nearest train | top1 |
| --- | ---: | ---: | --- | --- | --- |
| m_csa:214 | 0.4598 | 0.01825 | False | m_csa:111 | heme_peroxidase_oxidase |
| m_csa:60 | 0.4709 | 0.02935 | False | m_csa:430 | metal_dependent_hydrolase |
| m_csa:75 | 0.4884 | 0.04685 | False | m_csa:94 | metal_dependent_hydrolase |
| m_csa:288 | 0.41995 | -0.0216 | True | m_csa:83 | ser_his_acid_hydrolase |

## Interpretation

- 1/4 new proxy-axis rows abstain at the unchanged fixed threshold.
- The active-site-count proxy axis is now deployably scored, but its fixed-threshold contribution is too small to close the Lever 3 structural proxy shortfall by itself.
- Keep this as a tranche readout; do not promote it to an operating-point claim until the broader extended surface is complete or another pre-registered train/cal proxy axis is scored.
