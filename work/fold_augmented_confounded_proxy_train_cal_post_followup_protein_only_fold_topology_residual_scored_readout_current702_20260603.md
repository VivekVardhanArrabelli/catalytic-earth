# Fold-Augmented Confounded Proxy Train/Cal Scored Extension - current702

Run: 2026-06-03T19:36:25Z

Train/cal-only scored extension for the Lever 3 confounded-proxy evidence tranche. It parses the tranche-vs-train-atlas Foldseek TSV, recomputes source-free predicted geometry for the same non-heldout OOS rows, and applies no threshold tuning.

## Status

- confounded_proxy_train_cal_scored_extension_complete
- Blockers: ['some_tranche_rows_missing_predicted_geometry']
- Full-channel rows: 8/8
- Query coordinate files observed: 8/8
- Foldseek nearest-train hits: 8

## Score Preview

| row | axes | geometry top1 | geometry | nearest train | TM | combined |
| --- | --- | --- | ---: | --- | ---: | ---: |
| m_csa:610 |  | metal_dependent_hydrolase | 0.3063 | m_csa:205 | 0.572 | 0.43915 |
| m_csa:137 |  | flavin_dehydrogenase_reductase | 0.185 | m_csa:856 | 0.3822 | 0.2836 |
| m_csa:318 |  | flavin_monooxygenase | 0.2122 | m_csa:862 | 0.4853 | 0.34875 |
| m_csa:360 |  | metal_dependent_hydrolase | 0.3062 | m_csa:740 | 0.7752 | 0.5407 |
| m_csa:105 |  | metal_dependent_hydrolase | 0.3478 | m_csa:42 | 0.4583 | 0.40305 |
| m_csa:327 |  | metal_dependent_hydrolase | 0.3544 | m_csa:706 | 0.3715 | 0.36295 |
| m_csa:649 |  | metal_dependent_hydrolase | 0.3041 | m_csa:166 | 0.442 | 0.37305 |
| m_csa:618 |  | metal_dependent_hydrolase | 0.3001 | m_csa:94 | 0.5606 | 0.43035 |

## Missing Full Scores

- None

## Interpretation

- 8/8 tranche rows now have full geometry/fold/cofactor channel scores.
- Compose these train/cal-only scores into an extended OOS surface, then rerun the fixed-threshold confounded proxy audit without changing the threshold.
