# Fold-Augmented Confounded Proxy Train/Cal Background-Axis Blocker - current702

Run: 2026-06-03T18:14:50Z

Train/cal-only blocker artifact for the exhausted Lever 3 confounded-proxy acquisition axes. It classifies the unscored ready OOS rows against the current high-cofactor and inorganic/structural proxy axes, records why the scoring tranche is empty, and does not score rows, tune thresholds, read heldout rows, or change labels.

## Status

- fold_augmented_confounded_proxy_train_cal_background_axis_blocker_complete
- Remaining unscored ready train/cal OOS rows: 160
- Background-only rows: 160
- High-cofactor-axis rows: 0
- Structural-axis rows: 0
- Scoring tranche rows: 0
- High/structural shortfalls: 16/170
- Blockers: ['remaining_train_cal_oos_rows_background_only_current_axes', 'no_high_cofactor_axis_candidates_available', 'no_structural_locus_axis_candidates_available', 'scoring_tranche_plan_empty_for_current_proxy_axes']

## Decision

- All remaining rows background-only under current axes: True
- Score background-only rows now: False
- Score tranche now: False
- Proxy calibration rerun ready now: False
- Next gate: Do not run an empty Foldseek/scoring tranche. Apply hash-valid reviewed source decisions if they arrive; otherwise open a new source-free proxy axis or pivot within Levers 2/4, because the current 170-row train/cal remainder is background-only under the high-cofactor and inorganic/structural proxy axes.

## Classification Counts

- Priority buckets: {'3': 160}
- Organic cofactor max classes: {'flavin': 43, 'heme': 50, 'plp': 67}
- Metal-ion locus statuses: {'no_metal_context_detected': 152, 'unsupported_or_missing_geometry': 8}

## Background-Only Rows

| row | bucket | organic max | exclusion reasons |
| --- | ---: | --- | --- |
| m_csa:1 | 3 | flavin:0.024314 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:2 | 3 | heme:0.029778 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:18 | 3 | plp:0.055247 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:26 | 3 | plp:0.177608 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:29 | 3 | heme:0.018463 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:33 | 3 | flavin:0.025633 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:47 | 3 | heme:0.013946 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:49 | 3 | flavin:0.098011 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:50 | 3 | plp:0.052999 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:55 | 3 | plp:0.031299 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:64 | 3 | plp:0.246623 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:69 | 3 | plp:0.015265 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:76 | 3 | flavin:0.035629 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:77 | 3 | plp:0.031529 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:81 | 3 | plp:0.141 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:92 | 3 | plp:0.106514 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:96 | 3 | plp:0.037385 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:100 | 3 | flavin:0.047641 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:101 | 3 | plp:0.032566 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:105 | 3 | flavin:0.024633 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus, some_inorganic_locus_geometry_unsupported_or_missing |
| m_csa:112 | 3 | heme:0.037765 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:122 | 3 | flavin:0.037925 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:128 | 3 | plp:0.11803 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:137 | 3 | flavin:0.003489 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus, some_inorganic_locus_geometry_unsupported_or_missing |
| m_csa:148 | 3 | plp:0.10865 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:153 | 3 | flavin:0.063819 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:154 | 3 | heme:0.023478 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:162 | 3 | plp:0.131705 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:164 | 3 | plp:0.051493 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:174 | 3 | plp:0.070105 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:175 | 3 | heme:0.12583 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:196 | 3 | heme:0.020949 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:202 | 3 | plp:0.074818 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:203 | 3 | plp:0.004498 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:210 | 3 | heme:0.060519 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:226 | 3 | flavin:0.051011 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:227 | 3 | plp:0.012418 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:228 | 3 | plp:0.032141 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:232 | 3 | plp:0.147019 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:235 | 3 | plp:0.126653 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:241 | 3 | plp:0.037606 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:245 | 3 | flavin:0.112395 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:247 | 3 | plp:0.011039 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:252 | 3 | flavin:0.069699 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:257 | 3 | flavin:0.095406 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:260 | 3 | heme:0.011704 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:261 | 3 | heme:0.012463 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:266 | 3 | heme:0.011219 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:278 | 3 | heme:0.017115 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:279 | 3 | heme:0.109212 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:291 | 3 | flavin:0.000546 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:292 | 3 | flavin:0.017833 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:296 | 3 | plp:0.118926 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:302 | 3 | heme:0.020396 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:306 | 3 | heme:0.119577 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:315 | 3 | flavin:0.017559 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:316 | 3 | plp:0.104929 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:317 | 3 | heme:0.018605 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:318 | 3 | heme:0.034086 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus, some_inorganic_locus_geometry_unsupported_or_missing |
| m_csa:324 | 3 | plp:0.041833 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:327 | 3 | heme:0.005613 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus, some_inorganic_locus_geometry_unsupported_or_missing |
| m_csa:328 | 3 | plp:0.048545 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:329 | 3 | plp:0.001807 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:335 | 3 | plp:0.042031 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:336 | 3 | flavin:0.054143 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:339 | 3 | flavin:0.05048 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:340 | 3 | plp:0.067825 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:341 | 3 | plp:0.022702 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:343 | 3 | flavin:0.060874 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:344 | 3 | plp:0.016782 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:349 | 3 | plp:0.019585 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:351 | 3 | plp:0.144021 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:357 | 3 | heme:0.063288 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:360 | 3 | heme:0.035844 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus, some_inorganic_locus_geometry_unsupported_or_missing |
| m_csa:362 | 3 | flavin:0.034413 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:366 | 3 | plp:0.035329 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:373 | 3 | heme:0.088163 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:374 | 3 | heme:0.088163 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:377 | 3 | heme:0.009383 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |
| m_csa:382 | 3 | plp:0.049148 | organic_cofactor_below_high_axis_threshold, no_high_inorganic_cofactor_locus, no_source_free_inorganic_structural_locus |

## Interpretation

- 160/160 remaining unscored ready train/cal OOS rows are background-only under the current confounded-proxy axes.
- 0 high-cofactor-axis rows and 0 inorganic/structural-axis rows remain for shortfalls of 16 and 170.
- Treat the current Lever 3 automatic scoring path as exhausted until reviewed decisions or a new source-free proxy axis create non-background train/cal evidence.
