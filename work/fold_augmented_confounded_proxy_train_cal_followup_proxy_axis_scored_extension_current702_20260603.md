# Fold-Augmented Confounded Proxy Train/Cal Scored Extension - current702

Run: 2026-06-03T18:09:36Z

Train/cal-only scored extension for the Lever 3 confounded-proxy evidence tranche. It parses the tranche-vs-train-atlas Foldseek TSV, recomputes source-free predicted geometry for the same non-heldout OOS rows, and applies no threshold tuning.

## Status

- confounded_proxy_train_cal_scored_extension_complete
- Blockers: []
- Full-channel rows: 4/4
- Query coordinate files observed: 4/4
- Foldseek nearest-train hits: 4

## Score Preview

| row | axes | geometry top1 | geometry | nearest train | TM | combined |
| --- | --- | --- | ---: | --- | ---: | ---: |
| m_csa:60 | organic_score_0_30_to_below_high_axis_proxy, background_train_cal_oos_cofactor_pool | metal_dependent_hydrolase | 0.3704 | m_csa:430 | 0.5714 | 0.4709 |
| m_csa:75 | organic_score_0_30_to_below_high_axis_proxy, background_train_cal_oos_cofactor_pool | metal_dependent_hydrolase | 0.5757 | m_csa:94 | 0.4011 | 0.4884 |
| m_csa:214 | organic_score_0_30_to_below_high_axis_proxy, background_train_cal_oos_cofactor_pool | heme_peroxidase_oxidase | 0.3559 | m_csa:111 | 0.5637 | 0.4598 |
| m_csa:288 | organic_score_0_30_to_below_high_axis_proxy, background_train_cal_oos_cofactor_pool | ser_his_acid_hydrolase | 0.4272 | m_csa:83 | 0.4127 | 0.41995 |

## Missing Full Scores

- None

## Interpretation

- 4/4 tranche rows now have full geometry/fold/cofactor channel scores.
- Compose these train/cal-only scores into an extended OOS surface, then rerun the fixed-threshold confounded proxy audit without changing the threshold.
