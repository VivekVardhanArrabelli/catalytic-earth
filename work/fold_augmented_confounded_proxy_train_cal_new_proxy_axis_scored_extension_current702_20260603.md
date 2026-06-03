# Fold-Augmented Confounded Proxy Train/Cal Scored Extension - current702

Run: 2026-06-03T17:21:54Z

Train/cal-only scored extension for the Lever 3 confounded-proxy evidence tranche. It parses the tranche-vs-train-atlas Foldseek TSV, recomputes source-free predicted geometry for the same non-heldout OOS rows, and applies no threshold tuning.

## Status

- confounded_proxy_train_cal_scored_extension_complete
- Blockers: []
- Full-channel rows: 6/6
- Query coordinate files observed: 6/6
- Foldseek nearest-train hits: 6

## Score Preview

| row | axes | geometry top1 | geometry | nearest train | TM | combined |
| --- | --- | --- | ---: | --- | ---: | ---: |
| m_csa:89 | active_site_residue_count_10_plus_proxy, background_train_cal_oos_structural_pool | metal_dependent_hydrolase | 0.409 | m_csa:83 | 0.491 | 0.45 |
| m_csa:90 | active_site_residue_count_10_plus_proxy, background_train_cal_oos_structural_pool | ser_his_acid_hydrolase | 0.383 | m_csa:445 | 0.6117 | 0.49735 |
| m_csa:143 | active_site_residue_count_10_plus_proxy, background_train_cal_oos_structural_pool | metal_dependent_hydrolase | 0.3767 | m_csa:142 | 0.6132 | 0.49495 |
| m_csa:253 | active_site_residue_count_10_plus_proxy, background_train_cal_oos_structural_pool | metal_dependent_hydrolase | 0.5662 | m_csa:528 | 0.4654 | 0.5158 |
| m_csa:466 | active_site_residue_count_10_plus_proxy, background_train_cal_oos_structural_pool | ser_his_acid_hydrolase | 0.4004 | m_csa:412 | 0.3707 | 0.38555 |
| m_csa:501 | active_site_residue_count_10_plus_proxy, background_train_cal_oos_structural_pool | metal_dependent_hydrolase | 0.5651 | m_csa:716 | 0.6369 | 0.601 |

## Missing Full Scores

- None

## Interpretation

- 6/6 tranche rows now have full geometry/fold/cofactor channel scores.
- Compose these train/cal-only scores into an extended OOS surface, then rerun the fixed-threshold confounded proxy audit without changing the threshold.
