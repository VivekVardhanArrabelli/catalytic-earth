# Fold-Augmented Confounded Proxy Train/Cal Scoring Tranche Plan - current702

Run: 2026-06-03T14:31:55Z

Bounded train/cal-only scoring tranche plan for the Lever 3 confounded-proxy acquisition gap. It selects unscored candidate rows for future predicted-structure-vs-atlas scoring; it does not run scoring, read heldout rows, or change thresholds.

## Status

- fold_augmented_confounded_proxy_train_cal_scoring_tranche_plan_ready
- Tranche rows: 50
- Selected high-cofactor-axis rows: 13
- Selected structural-axis rows: 48
- High shortfall: 4
- Structural shortfall: 48
- Blockers: ['scoring_tranche_not_run']

## Decision

- Score tranche now: False
- Apply/change threshold now: False
- Proxy calibration rerun ready now: False
- Tranche ready for scoring plan: True
- Next gate: Run predicted-structure-vs-atlas scoring for exactly these tranche rows, join the resulting fixed-channel scores back to train/cal only, then rerun the proxy operating-point audit without changing threshold 0.44155.

## Scoring Tranche Rows

| row | reason | bucket | axes | organic max |
| --- | --- | ---: | --- | --- |
| m_csa:289 | high_cofactor_axis_candidate | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | flavin:0.980742 |
| m_csa:361 | high_cofactor_axis_candidate | 1 | high_cofactor_signature_proxy | heme:0.97392 |
| m_csa:604 | high_cofactor_axis_candidate | 1 | high_cofactor_signature_proxy | flavin:0.605709 |
| m_csa:298 | high_cofactor_axis_candidate | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | flavin:0.515522 |
| m_csa:268 | high_cofactor_axis_candidate | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | plp:0.267672 |
| m_csa:332 | high_cofactor_axis_candidate | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | heme:0.109821 |
| m_csa:398 | high_cofactor_axis_candidate | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | flavin:0.09856 |
| m_csa:127 | high_cofactor_axis_candidate | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | flavin:0.068596 |
| m_csa:427 | high_cofactor_axis_candidate | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | heme:0.048754 |
| m_csa:130 | high_cofactor_axis_candidate | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | flavin:0.044528 |
| m_csa:276 | high_cofactor_axis_candidate | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | heme:0.03172 |
| m_csa:562 | high_cofactor_axis_candidate | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | flavin:0.012957 |
| m_csa:23 | high_cofactor_axis_candidate | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | heme:0.001625 |
| m_csa:215 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.379526 |
| m_csa:263 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.343767 |
| m_csa:367 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.325641 |
| m_csa:21 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.302412 |
| m_csa:308 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.291653 |
| m_csa:182 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.268877 |
| m_csa:139 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.253779 |
| m_csa:221 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.246079 |
| m_csa:540 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.216 |
| m_csa:502 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.206148 |
| m_csa:468 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.181268 |
| m_csa:331 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.172985 |
| m_csa:135 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.153072 |
| m_csa:648 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.151453 |
| m_csa:134 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.151172 |
| m_csa:270 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.138432 |
| m_csa:326 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.133397 |
| m_csa:251 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.13156 |
| m_csa:601 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.120138 |
| m_csa:552 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.119035 |
| m_csa:416 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.115904 |
| m_csa:51 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.113362 |
| m_csa:365 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.109043 |
| m_csa:240 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.102791 |
| m_csa:514 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.101561 |
| m_csa:539 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.100854 |
| m_csa:99 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.09978 |
| m_csa:652 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.099308 |
| m_csa:272 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.095155 |
| m_csa:498 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.094616 |
| m_csa:287 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.092806 |
| m_csa:7 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.086786 |
| m_csa:259 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.08665 |
| m_csa:488 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | heme:0.084131 |
| m_csa:95 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.082176 |
| m_csa:179 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | flavin:0.081808 |
| m_csa:207 | structural_locus_axis_candidate | 2 | same_family_structural_proxy | plp:0.07504 |

## Interpretation

- 50 train/cal OOS rows are selected for the next fixed-threshold scoring tranche.
- The tranche covers 13 high-cofactor-axis rows for a 4-row lower bound and 48 structural-axis rows for a 48-row lower bound, by count only.
- Score the tranche; do not count any row as new abstained proxy evidence until the actual fixed-threshold scores exist.
