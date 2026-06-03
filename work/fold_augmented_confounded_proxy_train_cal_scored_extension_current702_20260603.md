# Fold-Augmented Confounded Proxy Train/Cal Scored Extension - current702

Run: 2026-06-03T15:15:39Z

Train/cal-only scored extension for the Lever 3 confounded-proxy evidence tranche. It parses the tranche-vs-train-atlas Foldseek TSV, recomputes source-free predicted geometry for the same non-heldout OOS rows, and applies no threshold tuning.

## Status

- confounded_proxy_train_cal_scored_extension_partial
- Blockers: ['some_tranche_rows_missing_predicted_geometry', 'some_tranche_rows_missing_fold_scores', 'tranche_query_coordinate_files_missing']
- Full-channel rows: 47/50
- Query coordinate files observed: 48/50
- Foldseek nearest-train hits: 48

## Score Preview

| row | axes | geometry top1 | geometry | nearest train | TM | combined |
| --- | --- | --- | ---: | --- | ---: | ---: |
| m_csa:289 | high_cofactor_signature_proxy, same_family_structural_proxy | flavin_dehydrogenase_reductase | 0.3667 | m_csa:275 | 0.9129 | 0.6398 |
| m_csa:361 | high_cofactor_signature_proxy | metal_dependent_hydrolase | 0.5274 | m_csa:822 | 0.3865 | 0.45695 |
| m_csa:604 | high_cofactor_signature_proxy | None | None | m_csa:528 | 0.4713 | None |
| m_csa:298 | high_cofactor_signature_proxy, same_family_structural_proxy | flavin_monooxygenase | 0.1856 | m_csa:275 | 0.8832 | 0.5344 |
| m_csa:268 | high_cofactor_signature_proxy, same_family_structural_proxy | metal_dependent_hydrolase | 0.6016 | m_csa:120 | 0.6715 | 0.63655 |
| m_csa:332 | high_cofactor_signature_proxy, same_family_structural_proxy | metal_dependent_hydrolase | 0.2908 | m_csa:120 | 0.4936 | 0.3922 |
| m_csa:398 | high_cofactor_signature_proxy, same_family_structural_proxy | metal_dependent_hydrolase | 0.4583 | m_csa:518 | 0.4343 | 0.4463 |
| m_csa:127 | high_cofactor_signature_proxy, same_family_structural_proxy | metal_dependent_hydrolase | 0.5689 | m_csa:518 | 0.4621 | 0.5155 |
| m_csa:427 | high_cofactor_signature_proxy, same_family_structural_proxy | metal_dependent_hydrolase | 0.3655 | m_csa:337 | 0.5265 | 0.446 |
| m_csa:130 | high_cofactor_signature_proxy, same_family_structural_proxy | metal_dependent_hydrolase | 0.4142 | m_csa:98 | 0.4061 | 0.41015 |
| m_csa:276 | high_cofactor_signature_proxy, same_family_structural_proxy | flavin_dehydrogenase_reductase | 0.3984 | m_csa:771 | 0.4798 | 0.4391 |
| m_csa:562 | high_cofactor_signature_proxy, same_family_structural_proxy | metal_dependent_hydrolase | 0.075 | None | None | None |
| m_csa:23 | high_cofactor_signature_proxy, same_family_structural_proxy | metal_dependent_hydrolase | 0.3552 | m_csa:862 | 0.6022 | 0.4787 |
| m_csa:215 | same_family_structural_proxy | metal_dependent_hydrolase | 0.3775 | m_csa:275 | 0.8444 | 0.61095 |
| m_csa:263 | same_family_structural_proxy | flavin_dehydrogenase_reductase | 0.2958 | m_csa:528 | 0.5635 | 0.42965 |
| m_csa:367 | same_family_structural_proxy | metal_dependent_hydrolase | 0.5719 | m_csa:275 | 0.876 | 0.72395 |
| m_csa:21 | same_family_structural_proxy | metal_dependent_hydrolase | 0.58 | m_csa:631 | 0.5915 | 0.58575 |
| m_csa:308 | same_family_structural_proxy | metal_dependent_hydrolase | 0.5788 | m_csa:11 | 0.7835 | 0.68115 |
| m_csa:182 | same_family_structural_proxy | metal_dependent_hydrolase | 0.4113 | m_csa:120 | 0.7119 | 0.5616 |
| m_csa:139 | same_family_structural_proxy | metal_dependent_hydrolase | 0.3454 | m_csa:353 | 0.5273 | 0.43635 |
| m_csa:221 | same_family_structural_proxy | metal_dependent_hydrolase | 0.3336 | m_csa:275 | 0.8748 | 0.6042 |
| m_csa:540 | same_family_structural_proxy | metal_dependent_hydrolase | 0.4181 | m_csa:716 | 0.4002 | 0.40915 |
| m_csa:502 | same_family_structural_proxy | metal_dependent_hydrolase | 0.5262 | m_csa:168 | 0.6652 | 0.5957 |
| m_csa:468 | same_family_structural_proxy | metal_dependent_hydrolase | 0.591 | m_csa:11 | 0.6935 | 0.64225 |
| m_csa:331 | same_family_structural_proxy | metal_dependent_hydrolase | 0.3639 | m_csa:862 | 0.5687 | 0.4663 |
| m_csa:135 | same_family_structural_proxy | metal_dependent_hydrolase | 0.404 | m_csa:740 | 0.6594 | 0.5317 |
| m_csa:648 | same_family_structural_proxy | metal_dependent_hydrolase | 0.329 | m_csa:528 | 0.4684 | 0.3987 |
| m_csa:134 | same_family_structural_proxy | metal_dependent_hydrolase | 0.4275 | m_csa:83 | 0.391 | 0.40925 |
| m_csa:270 | same_family_structural_proxy | metal_dependent_hydrolase | 0.4214 | m_csa:108 | 0.7311 | 0.57625 |
| m_csa:326 | same_family_structural_proxy | flavin_monooxygenase | 0.2517 | m_csa:937 | 0.624 | 0.43785 |

## Missing Full Scores

- m_csa:416
- m_csa:562
- m_csa:604

## Interpretation

- 47/50 tranche rows now have full geometry/fold/cofactor channel scores.
- Compose these train/cal-only scores into an extended OOS surface, then rerun the fixed-threshold confounded proxy audit without changing the threshold.
