# Fold-Augmented Confounded Proxy Train/Cal Scored Extension - current702

Run: 2026-06-03T15:38:49Z

Train/cal-only scored extension for the Lever 3 confounded-proxy evidence tranche. It parses the tranche-vs-train-atlas Foldseek TSV, recomputes source-free predicted geometry for the same non-heldout OOS rows, and applies no threshold tuning.

## Status

- confounded_proxy_train_cal_scored_extension_partial
- Blockers: ['some_tranche_rows_missing_predicted_geometry', 'some_tranche_rows_missing_fold_scores', 'tranche_query_coordinate_files_missing']
- Full-channel rows: 64/66
- Query coordinate files observed: 64/66
- Foldseek nearest-train hits: 64

## Score Preview

| row | axes | geometry top1 | geometry | nearest train | TM | combined |
| --- | --- | --- | ---: | --- | ---: | ---: |
| m_csa:309 | same_family_structural_proxy | metal_dependent_hydrolase | 0.3437 | m_csa:94 | 0.4389 | 0.3913 |
| m_csa:138 | same_family_structural_proxy | metal_dependent_hydrolase | 0.5942 | m_csa:117 | 0.4758 | 0.535 |
| m_csa:380 | same_family_structural_proxy | metal_dependent_hydrolase | 0.3802 | m_csa:518 | 0.5601 | 0.47015 |
| m_csa:48 | same_family_structural_proxy | metal_dependent_hydrolase | 0.3468 | m_csa:411 | 0.5756 | 0.4612 |
| m_csa:637 | same_family_structural_proxy | metal_dependent_hydrolase | 0.075 | None | None | None |
| m_csa:223 | same_family_structural_proxy | metal_dependent_hydrolase | 0.3777 | m_csa:300 | 0.6379 | 0.5078 |
| m_csa:508 | same_family_structural_proxy | metal_dependent_hydrolase | 0.343 | m_csa:716 | 0.5153 | 0.42915 |
| m_csa:451 | same_family_structural_proxy | metal_dependent_hydrolase | 0.5419 | m_csa:376 | 0.6341 | 0.588 |
| m_csa:231 | same_family_structural_proxy | metal_dependent_hydrolase | 0.5432 | m_csa:111 | 0.3944 | 0.4688 |
| m_csa:350 | same_family_structural_proxy | metal_dependent_hydrolase | 0.365 | m_csa:546 | 0.3984 | 0.3817 |
| m_csa:280 | same_family_structural_proxy | ser_his_acid_hydrolase | 0.3711 | m_csa:94 | 0.523 | 0.44705 |
| m_csa:70 | same_family_structural_proxy | metal_dependent_hydrolase | 0.3633 | m_csa:808 | 0.5958 | 0.47955 |
| m_csa:150 | same_family_structural_proxy | ser_his_acid_hydrolase | 0.3737 | m_csa:111 | 0.5139 | 0.4438 |
| m_csa:151 | same_family_structural_proxy | metal_dependent_hydrolase | 0.4321 | m_csa:111 | 0.5655 | 0.4988 |
| m_csa:310 | same_family_structural_proxy | metal_dependent_hydrolase | 0.3656 | m_csa:518 | 0.5208 | 0.4432 |
| m_csa:359 | same_family_structural_proxy | metal_dependent_hydrolase | 0.4045 | m_csa:205 | 0.4539 | 0.4292 |
| m_csa:72 | same_family_structural_proxy | metal_dependent_hydrolase | 0.3792 | m_csa:147 | 0.4665 | 0.42285 |
| m_csa:640 | same_family_structural_proxy | metal_dependent_hydrolase | 0.5983 | m_csa:941 | 0.4364 | 0.51735 |
| m_csa:84 | same_family_structural_proxy | metal_dependent_hydrolase | 0.5971 | m_csa:917 | 0.538 | 0.56755 |
| m_csa:194 | same_family_structural_proxy | ser_his_acid_hydrolase | 0.4367 | m_csa:727 | 0.4751 | 0.4559 |
| m_csa:463 | same_family_structural_proxy | metal_dependent_hydrolase | 0.4162 | m_csa:11 | 0.6791 | 0.54765 |
| m_csa:190 | same_family_structural_proxy | metal_dependent_hydrolase | 0.5886 | m_csa:823 | 0.6844 | 0.6365 |
| m_csa:450 | same_family_structural_proxy | metal_dependent_hydrolase | 0.3721 | m_csa:446 | 0.4026 | 0.38735 |
| m_csa:224 | same_family_structural_proxy | metal_dependent_hydrolase | 0.3697 | m_csa:636 | 0.4325 | 0.4011 |
| m_csa:405 | same_family_structural_proxy | metal_dependent_hydrolase | 0.3639 | m_csa:636 | 0.6035 | 0.4837 |
| m_csa:638 | same_family_structural_proxy | metal_dependent_hydrolase | 0.3756 | m_csa:170 | 0.7968 | 0.5862 |
| m_csa:312 | same_family_structural_proxy | metal_dependent_hydrolase | 0.5977 | m_csa:522 | 0.5451 | 0.5714 |
| m_csa:256 | same_family_structural_proxy | metal_dependent_hydrolase | 0.5974 | m_csa:716 | 0.6411 | 0.61925 |
| m_csa:587 | same_family_structural_proxy | flavin_monooxygenase | 0.2413 | m_csa:167 | 0.6782 | 0.45975 |
| m_csa:74 | same_family_structural_proxy | metal_dependent_hydrolase | 0.5864 | m_csa:535 | 0.6397 | 0.61305 |

## Missing Full Scores

- m_csa:586
- m_csa:637

## Interpretation

- 64/66 tranche rows now have full geometry/fold/cofactor channel scores.
- Compose these train/cal-only scores into an extended OOS surface, then rerun the fixed-threshold confounded proxy audit without changing the threshold.
