# Fold-Augmented Confounded Proxy Train/Cal Candidate Pool - current702

Run: 2026-06-03T14:28:05Z

Train/cal-only source-free candidate pool for the Lever 3 confounded-proxy evidence acquisition gap. It filters out rows already in the current scored OOS surface and ranks the remaining train/cal OOS rows for future predicted-structure-vs-atlas scoring.

## Status

- fold_augmented_confounded_proxy_train_cal_candidate_pool_ready_for_scoring_plan
- Ready train/cal OOS rows: 353
- Current scored train/cal OOS rows: 76
- Unscored ready train/cal OOS candidate rows: 286
- High-cofactor-axis candidate rows: 13
- Structural-locus candidate rows: 114
- Priority rows emitted: 80
- Priority bucket counts: {'1': 13, '2': 103, '3': 170}
- Blockers: ['candidate_pool_not_scored_at_fixed_threshold']

## Decision

- Score candidate pool now: False
- Apply/change threshold now: False
- Proxy calibration rerun ready now: False
- Candidate pool meets high shortfall by count: True
- Candidate pool meets structural shortfall by count: True
- Next gate: Score a bounded tranche from priority_candidate_rows with the predicted-structure-vs-atlas channel, then rerun the fixed-threshold proxy operating-point audit only after new train/cal OOS rows have actual channel scores.

## Priority Candidate Rows

| row | bucket | axes | organic max | inorganic context |
| --- | ---: | --- | --- | --- |
| m_csa:289 | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | flavin:0.980742 | 1 |
| m_csa:361 | 1 | high_cofactor_signature_proxy | heme:0.97392 | 0 |
| m_csa:604 | 1 | high_cofactor_signature_proxy | flavin:0.605709 | 0 |
| m_csa:298 | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | flavin:0.515522 | 1 |
| m_csa:268 | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | plp:0.267672 | 1 |
| m_csa:332 | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | heme:0.109821 | 1 |
| m_csa:398 | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | flavin:0.09856 | 1 |
| m_csa:127 | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | flavin:0.068596 | 1 |
| m_csa:427 | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | heme:0.048754 | 1 |
| m_csa:130 | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | flavin:0.044528 | 1 |
| m_csa:276 | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | heme:0.03172 | 1 |
| m_csa:562 | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | flavin:0.012957 | 1 |
| m_csa:23 | 1 | high_cofactor_signature_proxy, same_family_structural_proxy | heme:0.001625 | 1 |
| m_csa:215 | 2 | same_family_structural_proxy | flavin:0.379526 | 1 |
| m_csa:263 | 2 | same_family_structural_proxy | heme:0.343767 | 1 |
| m_csa:367 | 2 | same_family_structural_proxy | flavin:0.325641 | 1 |
| m_csa:21 | 2 | same_family_structural_proxy | plp:0.302412 | 1 |
| m_csa:308 | 2 | same_family_structural_proxy | heme:0.291653 | 1 |
| m_csa:182 | 2 | same_family_structural_proxy | plp:0.268877 | 1 |
| m_csa:139 | 2 | same_family_structural_proxy | plp:0.253779 | 1 |
| m_csa:221 | 2 | same_family_structural_proxy | flavin:0.246079 | 1 |
| m_csa:540 | 2 | same_family_structural_proxy | plp:0.216 | 1 |
| m_csa:502 | 2 | same_family_structural_proxy | plp:0.206148 | 1 |
| m_csa:468 | 2 | same_family_structural_proxy | plp:0.181268 | 1 |
| m_csa:331 | 2 | same_family_structural_proxy | plp:0.172985 | 1 |
| m_csa:135 | 2 | same_family_structural_proxy | heme:0.153072 | 1 |
| m_csa:648 | 2 | same_family_structural_proxy | plp:0.151453 | 1 |
| m_csa:134 | 2 | same_family_structural_proxy | heme:0.151172 | 1 |
| m_csa:270 | 2 | same_family_structural_proxy | plp:0.138432 | 1 |
| m_csa:326 | 2 | same_family_structural_proxy | plp:0.133397 | 1 |
| m_csa:251 | 2 | same_family_structural_proxy | heme:0.13156 | 1 |
| m_csa:601 | 2 | same_family_structural_proxy | heme:0.120138 | 1 |
| m_csa:552 | 2 | same_family_structural_proxy | heme:0.119035 | 1 |
| m_csa:416 | 2 | same_family_structural_proxy | plp:0.115904 | 1 |
| m_csa:51 | 2 | same_family_structural_proxy | plp:0.113362 | 1 |
| m_csa:365 | 2 | same_family_structural_proxy | plp:0.109043 | 1 |
| m_csa:240 | 2 | same_family_structural_proxy | heme:0.102791 | 1 |
| m_csa:514 | 2 | same_family_structural_proxy | heme:0.101561 | 1 |
| m_csa:539 | 2 | same_family_structural_proxy | plp:0.100854 | 1 |
| m_csa:99 | 2 | same_family_structural_proxy | heme:0.09978 | 1 |
| m_csa:652 | 2 | same_family_structural_proxy | flavin:0.099308 | 1 |
| m_csa:272 | 2 | same_family_structural_proxy | flavin:0.095155 | 1 |
| m_csa:498 | 2 | same_family_structural_proxy | plp:0.094616 | 1 |
| m_csa:287 | 2 | same_family_structural_proxy | heme:0.092806 | 1 |
| m_csa:7 | 2 | same_family_structural_proxy | plp:0.086786 | 1 |
| m_csa:259 | 2 | same_family_structural_proxy | heme:0.08665 | 1 |
| m_csa:488 | 2 | same_family_structural_proxy | heme:0.084131 | 1 |
| m_csa:95 | 2 | same_family_structural_proxy | flavin:0.082176 | 1 |
| m_csa:179 | 2 | same_family_structural_proxy | flavin:0.081808 | 1 |
| m_csa:207 | 2 | same_family_structural_proxy | plp:0.07504 | 1 |
| m_csa:309 | 2 | same_family_structural_proxy | plp:0.073222 | 1 |
| m_csa:138 | 2 | same_family_structural_proxy | heme:0.070443 | 1 |
| m_csa:380 | 2 | same_family_structural_proxy | flavin:0.070437 | 1 |
| m_csa:48 | 2 | same_family_structural_proxy | flavin:0.069563 | 1 |
| m_csa:637 | 2 | same_family_structural_proxy | plp:0.069548 | 1 |
| m_csa:223 | 2 | same_family_structural_proxy | flavin:0.068591 | 1 |
| m_csa:508 | 2 | same_family_structural_proxy | plp:0.067949 | 1 |
| m_csa:451 | 2 | same_family_structural_proxy | flavin:0.064766 | 1 |
| m_csa:231 | 2 | same_family_structural_proxy | flavin:0.064335 | 1 |
| m_csa:350 | 2 | same_family_structural_proxy | plp:0.062013 | 1 |
| m_csa:280 | 2 | same_family_structural_proxy | flavin:0.059279 | 1 |
| m_csa:70 | 2 | same_family_structural_proxy | plp:0.058751 | 1 |
| m_csa:150 | 2 | same_family_structural_proxy | heme:0.058092 | 1 |
| m_csa:151 | 2 | same_family_structural_proxy | flavin:0.05522 | 1 |
| m_csa:310 | 2 | same_family_structural_proxy | plp:0.053663 | 1 |
| m_csa:359 | 2 | same_family_structural_proxy | heme:0.05146 | 1 |
| m_csa:72 | 2 | same_family_structural_proxy | plp:0.050862 | 1 |
| m_csa:640 | 2 | same_family_structural_proxy | heme:0.048929 | 1 |
| m_csa:84 | 2 | same_family_structural_proxy | plp:0.048876 | 1 |
| m_csa:194 | 2 | same_family_structural_proxy | flavin:0.048628 | 1 |
| m_csa:463 | 2 | same_family_structural_proxy | flavin:0.048582 | 1 |
| m_csa:190 | 2 | same_family_structural_proxy | plp:0.047669 | 1 |
| m_csa:450 | 2 | same_family_structural_proxy | flavin:0.0458 | 1 |
| m_csa:224 | 2 | same_family_structural_proxy | heme:0.045267 | 1 |
| m_csa:405 | 2 | same_family_structural_proxy | flavin:0.042608 | 1 |
| m_csa:638 | 2 | same_family_structural_proxy | flavin:0.041957 | 1 |
| m_csa:312 | 2 | same_family_structural_proxy | heme:0.041514 | 1 |
| m_csa:256 | 2 | same_family_structural_proxy | flavin:0.038203 | 1 |
| m_csa:587 | 2 | same_family_structural_proxy | flavin:0.036184 | 1 |
| m_csa:74 | 2 | same_family_structural_proxy | flavin:0.033547 | 1 |

## Interpretation

- 286 ready train/cal OOS rows are outside the current scored surface.
- 13 rows are plausible high-cofactor-axis candidates and 114 rows have source-free inorganic/structural locus context, but none has been scored or counted as new abstained evidence yet.
- Run a bounded predicted-structure-vs-atlas scoring tranche from the priority candidate rows; keep the fixed threshold and do not read heldout rows for calibration.
