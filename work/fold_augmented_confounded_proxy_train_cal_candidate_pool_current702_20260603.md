# Fold-Augmented Confounded Proxy Train/Cal Candidate Pool - current702

Run: 2026-06-03T16:13:13Z

Train/cal-only source-free candidate pool for the Lever 3 confounded-proxy evidence acquisition gap. It filters out rows already in the current scored OOS surface and ranks the remaining train/cal OOS rows for future predicted-structure-vs-atlas scoring.

## Status

- fold_augmented_confounded_proxy_train_cal_candidate_pool_ready_for_scoring_plan
- Ready train/cal OOS rows: 353
- Current scored train/cal OOS rows: 192
- Unscored ready train/cal OOS candidate rows: 170
- High-cofactor-axis candidate rows: 0
- Structural-locus candidate rows: 0
- Priority rows emitted: 80
- Priority bucket counts: {'3': 170}
- Blockers: ['high_cofactor_candidate_pool_below_shortfall', 'structural_candidate_pool_below_shortfall', 'candidate_pool_not_scored_at_fixed_threshold']

## Decision

- Score candidate pool now: False
- Apply/change threshold now: False
- Proxy calibration rerun ready now: False
- Candidate pool meets high shortfall by count: False
- Candidate pool meets structural shortfall by count: False
- Current proxy axes exhausted: True
- Next gate: Do not score background-only rows under the current proxy axes. Build the background-axis blocker, then wait for reviewed source decisions or define a new source-free proxy axis before any fixed-threshold proxy audit rerun.

## Priority Candidate Rows

| row | bucket | axes | organic max | inorganic context |
| --- | ---: | --- | --- | --- |
| m_csa:288 | 3 | background_train_cal_oos_structural_pool | heme:0.407563 | 0 |
| m_csa:89 | 3 | background_train_cal_oos_structural_pool | heme:0.398339 | 0 |
| m_csa:214 | 3 | background_train_cal_oos_structural_pool | plp:0.353171 | 0 |
| m_csa:75 | 3 | background_train_cal_oos_structural_pool | heme:0.34378 | 0 |
| m_csa:60 | 3 | background_train_cal_oos_structural_pool | plp:0.337092 | 0 |
| m_csa:583 | 3 | background_train_cal_oos_structural_pool | heme:0.296056 | 0 |
| m_csa:64 | 3 | background_train_cal_oos_structural_pool | plp:0.246623 | 0 |
| m_csa:607 | 3 | background_train_cal_oos_structural_pool | heme:0.236789 | 0 |
| m_csa:610 | 3 | background_train_cal_oos_structural_pool | plp:0.222226 | 0 |
| m_csa:618 | 3 | background_train_cal_oos_structural_pool | flavin:0.215006 | 0 |
| m_csa:555 | 3 | background_train_cal_oos_structural_pool | flavin:0.213904 | 0 |
| m_csa:404 | 3 | background_train_cal_oos_structural_pool | heme:0.193581 | 0 |
| m_csa:26 | 3 | background_train_cal_oos_structural_pool | plp:0.177608 | 0 |
| m_csa:515 | 3 | background_train_cal_oos_structural_pool | plp:0.150245 | 0 |
| m_csa:232 | 3 | background_train_cal_oos_structural_pool | plp:0.147019 | 0 |
| m_csa:351 | 3 | background_train_cal_oos_structural_pool | plp:0.144021 | 0 |
| m_csa:81 | 3 | background_train_cal_oos_structural_pool | plp:0.141 | 0 |
| m_csa:394 | 3 | background_train_cal_oos_structural_pool | plp:0.132044 | 0 |
| m_csa:162 | 3 | background_train_cal_oos_structural_pool | plp:0.131705 | 0 |
| m_csa:235 | 3 | background_train_cal_oos_structural_pool | plp:0.126653 | 0 |
| m_csa:175 | 3 | background_train_cal_oos_structural_pool | heme:0.12583 | 0 |
| m_csa:306 | 3 | background_train_cal_oos_structural_pool | heme:0.119577 | 0 |
| m_csa:296 | 3 | background_train_cal_oos_structural_pool | plp:0.118926 | 0 |
| m_csa:128 | 3 | background_train_cal_oos_structural_pool | plp:0.11803 | 0 |
| m_csa:616 | 3 | background_train_cal_oos_structural_pool | plp:0.117715 | 0 |
| m_csa:245 | 3 | background_train_cal_oos_structural_pool | flavin:0.112395 | 0 |
| m_csa:417 | 3 | background_train_cal_oos_structural_pool | flavin:0.110319 | 0 |
| m_csa:279 | 3 | background_train_cal_oos_structural_pool | heme:0.109212 | 0 |
| m_csa:148 | 3 | background_train_cal_oos_structural_pool | plp:0.10865 | 0 |
| m_csa:633 | 3 | background_train_cal_oos_structural_pool | plp:0.106909 | 0 |
| m_csa:92 | 3 | background_train_cal_oos_structural_pool | plp:0.106514 | 0 |
| m_csa:316 | 3 | background_train_cal_oos_structural_pool | plp:0.104929 | 0 |
| m_csa:49 | 3 | background_train_cal_oos_structural_pool | flavin:0.098011 | 0 |
| m_csa:257 | 3 | background_train_cal_oos_structural_pool | flavin:0.095406 | 0 |
| m_csa:455 | 3 | background_train_cal_oos_structural_pool | plp:0.088367 | 0 |
| m_csa:373 | 3 | background_train_cal_oos_structural_pool | heme:0.088163 | 0 |
| m_csa:374 | 3 | background_train_cal_oos_structural_pool | heme:0.088163 | 0 |
| m_csa:386 | 3 | background_train_cal_oos_structural_pool | heme:0.088163 | 0 |
| m_csa:570 | 3 | background_train_cal_oos_structural_pool | heme:0.079017 | 0 |
| m_csa:459 | 3 | background_train_cal_oos_structural_pool | heme:0.078375 | 0 |
| m_csa:202 | 3 | background_train_cal_oos_structural_pool | plp:0.074818 | 0 |
| m_csa:174 | 3 | background_train_cal_oos_structural_pool | plp:0.070105 | 0 |
| m_csa:252 | 3 | background_train_cal_oos_structural_pool | flavin:0.069699 | 0 |
| m_csa:389 | 3 | background_train_cal_oos_structural_pool | flavin:0.069644 | 0 |
| m_csa:458 | 3 | background_train_cal_oos_structural_pool | flavin:0.069644 | 0 |
| m_csa:635 | 3 | background_train_cal_oos_structural_pool | heme:0.068761 | 0 |
| m_csa:340 | 3 | background_train_cal_oos_structural_pool | plp:0.067825 | 0 |
| m_csa:574 | 3 | background_train_cal_oos_structural_pool | flavin:0.066149 | 0 |
| m_csa:153 | 3 | background_train_cal_oos_structural_pool | flavin:0.063819 | 0 |
| m_csa:357 | 3 | background_train_cal_oos_structural_pool | heme:0.063288 | 0 |
| m_csa:436 | 3 | background_train_cal_oos_structural_pool | heme:0.061443 | 0 |
| m_csa:343 | 3 | background_train_cal_oos_structural_pool | flavin:0.060874 | 0 |
| m_csa:210 | 3 | background_train_cal_oos_structural_pool | heme:0.060519 | 0 |
| m_csa:582 | 3 | background_train_cal_oos_structural_pool | heme:0.060256 | 0 |
| m_csa:461 | 3 | background_train_cal_oos_structural_pool | flavin:0.059011 | 0 |
| m_csa:524 | 3 | background_train_cal_oos_structural_pool | plp:0.05567 | 0 |
| m_csa:143 | 3 | background_train_cal_oos_structural_pool | heme:0.05565 | 0 |
| m_csa:18 | 3 | background_train_cal_oos_structural_pool | plp:0.055247 | 0 |
| m_csa:336 | 3 | background_train_cal_oos_structural_pool | flavin:0.054143 | 0 |
| m_csa:629 | 3 | background_train_cal_oos_structural_pool | flavin:0.053871 | 0 |
| m_csa:50 | 3 | background_train_cal_oos_structural_pool | plp:0.052999 | 0 |
| m_csa:576 | 3 | background_train_cal_oos_structural_pool | heme:0.052322 | 0 |
| m_csa:164 | 3 | background_train_cal_oos_structural_pool | plp:0.051493 | 0 |
| m_csa:479 | 3 | background_train_cal_oos_structural_pool | heme:0.051428 | 0 |
| m_csa:226 | 3 | background_train_cal_oos_structural_pool | flavin:0.051011 | 0 |
| m_csa:339 | 3 | background_train_cal_oos_structural_pool | flavin:0.05048 | 0 |
| m_csa:382 | 3 | background_train_cal_oos_structural_pool | plp:0.049148 | 0 |
| m_csa:457 | 3 | background_train_cal_oos_structural_pool | plp:0.048767 | 0 |
| m_csa:328 | 3 | background_train_cal_oos_structural_pool | plp:0.048545 | 0 |
| m_csa:434 | 3 | background_train_cal_oos_structural_pool | plp:0.047994 | 0 |
| m_csa:100 | 3 | background_train_cal_oos_structural_pool | flavin:0.047641 | 0 |
| m_csa:492 | 3 | background_train_cal_oos_structural_pool | plp:0.045923 | 0 |
| m_csa:478 | 3 | background_train_cal_oos_structural_pool | flavin:0.04383 | 0 |
| m_csa:481 | 3 | background_train_cal_oos_structural_pool | heme:0.04365 | 0 |
| m_csa:532 | 3 | background_train_cal_oos_structural_pool | heme:0.043106 | 0 |
| m_csa:569 | 3 | background_train_cal_oos_structural_pool | flavin:0.042567 | 0 |
| m_csa:335 | 3 | background_train_cal_oos_structural_pool | plp:0.042031 | 0 |
| m_csa:324 | 3 | background_train_cal_oos_structural_pool | plp:0.041833 | 0 |
| m_csa:571 | 3 | background_train_cal_oos_structural_pool | heme:0.03997 | 0 |
| m_csa:550 | 3 | background_train_cal_oos_structural_pool | plp:0.037938 | 0 |

## Interpretation

- 170 ready train/cal OOS rows are outside the current scored surface.
- 0 rows are plausible high-cofactor-axis candidates and 0 rows have source-free inorganic/structural locus context, but none has been scored or counted as new abstained evidence yet.
- Build the background-axis blocker and pivot to reviewed decisions or a new source-free proxy axis; keep the fixed threshold and do not read heldout rows for calibration.
