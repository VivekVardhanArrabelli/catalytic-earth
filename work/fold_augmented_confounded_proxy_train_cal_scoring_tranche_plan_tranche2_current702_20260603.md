# Fold-Augmented Confounded Proxy Train/Cal Scoring Tranche Plan - current702

Run: 2026-06-03T15:18:11Z

Bounded train/cal-only scoring tranche plan for the Lever 3 confounded-proxy acquisition gap. It selects unscored candidate rows for future predicted-structure-vs-atlas scoring; it does not run scoring, read heldout rows, or change thresholds.

## Status

- fold_augmented_confounded_proxy_train_cal_scoring_tranche_plan_blocked
- Tranche rows: 66
- Selected high-cofactor-axis rows: 0
- Selected structural-axis rows: 66
- High shortfall: 16
- Structural shortfall: 78
- Blockers: ['scoring_tranche_not_run', 'selected_high_cofactor_rows_below_shortfall', 'selected_structural_rows_below_shortfall']

## Decision

- Score tranche now: False
- Apply/change threshold now: False
- Proxy calibration rerun ready now: False
- Tranche ready for scoring plan: False
- Next gate: Run predicted-structure-vs-atlas scoring for exactly these tranche rows, join the resulting fixed-channel scores back to train/cal only, then rerun the proxy operating-point audit without changing threshold 0.44155.

## Scoring Tranche Rows

| row | reason | bucket | axes | organic max |
| --- | --- | ---: | --- | --- |
| m_csa:309 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.073222 |
| m_csa:138 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.070443 |
| m_csa:380 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.070437 |
| m_csa:48 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.069563 |
| m_csa:637 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.069548 |
| m_csa:223 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.068591 |
| m_csa:508 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.067949 |
| m_csa:451 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.064766 |
| m_csa:231 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.064335 |
| m_csa:350 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.062013 |
| m_csa:280 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.059279 |
| m_csa:70 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.058751 |
| m_csa:150 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.058092 |
| m_csa:151 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.05522 |
| m_csa:310 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.053663 |
| m_csa:359 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.05146 |
| m_csa:72 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.050862 |
| m_csa:640 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.048929 |
| m_csa:84 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.048876 |
| m_csa:194 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.048628 |
| m_csa:463 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.048582 |
| m_csa:190 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.047669 |
| m_csa:450 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.0458 |
| m_csa:224 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.045267 |
| m_csa:405 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.042608 |
| m_csa:638 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.041957 |
| m_csa:312 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.041514 |
| m_csa:256 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.038203 |
| m_csa:587 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.036184 |
| m_csa:74 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.033547 |
| m_csa:237 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.032857 |
| m_csa:282 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.031086 |
| m_csa:146 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.027848 |
| m_csa:585 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.027437 |
| m_csa:229 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.027164 |
| m_csa:236 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.025253 |
| m_csa:24 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.023841 |
| m_csa:265 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.023065 |
| m_csa:364 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.021952 |
| m_csa:505 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.021679 |
| m_csa:586 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.020063 |
| m_csa:603 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.019783 |
| m_csa:107 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.019374 |
| m_csa:645 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.018774 |
| m_csa:234 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.017819 |
| m_csa:441 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.016924 |
| m_csa:621 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.016341 |
| m_csa:460 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.016266 |
| m_csa:500 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.016116 |
| m_csa:533 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.015353 |
| m_csa:209 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.015282 |
| m_csa:273 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.014139 |
| m_csa:293 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.011621 |
| m_csa:322 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.011284 |
| m_csa:391 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.011212 |
| m_csa:421 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.010693 |
| m_csa:371 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.010287 |
| m_csa:8 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.009425 |
| m_csa:206 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.007512 |
| m_csa:91 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.006689 |
| m_csa:200 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.005725 |
| m_csa:187 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.005281 |
| m_csa:88 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.004591 |
| m_csa:59 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.003362 |
| m_csa:269 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.003333 |
| m_csa:348 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.002478 |

## Interpretation

- 66 train/cal OOS rows are selected for the next fixed-threshold scoring tranche.
- The tranche covers 0 high-cofactor-axis rows for a 16-row lower bound and 66 structural-axis rows for a 78-row lower bound, by count only.
- Score the tranche; do not count any row as new abstained proxy evidence until the actual fixed-threshold scores exist.
