# Fold-Augmented Confounded Proxy Evidence Extension Plan - current702

Run: 2026-06-03T15:39:12Z

Train/cal-only Lever 3 plan for extending confounded proxy evidence after the fixed predicted-structure-vs-atlas operating point failed to meet proxy calibration targets. It estimates how much additional proxy evidence would be needed at the unchanged threshold and maps retained proxy gaps to source-free evidence axes.

## Status

- fold_augmented_confounded_proxy_evidence_extension_plan_ready
- Blockers: ['high_cofactor_proxy_needs_16_more_abstained_train_cal_rows_at_fixed_threshold', 'same_family_structural_proxy_needs_170_more_abstained_train_cal_rows_at_fixed_threshold', 'threshold_stress::structural_proxy_80pct_abstain_breaks_85pct_in_scope_retention', 'threshold_stress::high_cofactor_proxy_80pct_abstain_breaks_90pct_in_scope_retention', 'current_train_cal_surface_lacks_high_cofactor_proxy_scale', 'current_train_cal_surface_cannot_reach_structural_proxy_80pct_by_loosened_membership']
- Fixed channel: combined_mean_geometry_fold
- Fixed threshold: 0.44155
- Retained proxy gaps: 48
- High-cofactor minimum new abstained rows for 80%: 16
- Same-family structural minimum new abstained rows for 80%: 170
- Current-surface unused high-cofactor rows: 0
- Current-surface additional same-family rows if loosened: 21
- Current-surface unscored candidate rows: 6

## Extension Requirements

| proxy | rows | fixed abstained | current recall | min new abstained @50% | min new abstained @80% |
| --- | ---: | ---: | ---: | ---: | ---: |
| high_cofactor_signature_proxy | 4 | 0 | 0.0 | 4 | 16 |
| same_family_structural_proxy | 55 | 10 | 0.1818 | 35 | 170 |

## Current Surface Pool

| pool | rows | abstained | recall/capacity |
| --- | ---: | ---: | ---: |
| high-cofactor rows | 4 | 0 | False |
| same-family loose rows | 76 | 25 | 0.3289 |
| strict same-family structural rows | 55 | 10 | 21 |

### Current Surface High-Cofactor Rows

| entry | score | margin | abstains | nearest fingerprint | top1 fingerprint |
| --- | ---: | ---: | --- | --- | --- |
| m_csa:289 | 0.6398 | 0.19825 | False | flavin_dehydrogenase_reductase | flavin_dehydrogenase_reductase |
| m_csa:298 | 0.5344 | 0.09285 | False | flavin_dehydrogenase_reductase | flavin_monooxygenase |
| m_csa:361 | 0.45695 | 0.0154 | False | flavin_dehydrogenase_reductase | metal_dependent_hydrolase |
| m_csa:368 | 0.4537 | 0.01215 | False | flavin_dehydrogenase_reductase | heme_peroxidase_oxidase |

### Current Surface Same-Family Extras If Loosened

| entry | score | margin | abstains | fold | geometry | fingerprint |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| m_csa:4 | 0.3729 | -0.06865 | True | 0.3812 | 0.3646 | metal_dependent_hydrolase |
| m_csa:525 | 0.37455 | -0.067 | True | 0.375 | 0.3741 | metal_dependent_hydrolase |
| m_csa:539 | 0.37695 | -0.0646 | True | 0.4091 | 0.3448 | metal_dependent_hydrolase |
| m_csa:350 | 0.3817 | -0.05985 | True | 0.3984 | 0.365 | metal_dependent_hydrolase |
| m_csa:282 | 0.38295 | -0.0586 | True | 0.41 | 0.3559 | metal_dependent_hydrolase |
| m_csa:450 | 0.38735 | -0.0542 | True | 0.4026 | 0.3721 | metal_dependent_hydrolase |
| m_csa:439 | 0.3933 | -0.04825 | True | 0.4242 | 0.3624 | metal_dependent_hydrolase |
| m_csa:648 | 0.3987 | -0.04285 | True | 0.4684 | 0.329 | metal_dependent_hydrolase |
| m_csa:177 | 0.3993 | -0.04225 | True | 0.4176 | 0.381 | metal_dependent_hydrolase |
| m_csa:145 | 0.40385 | -0.0377 | True | 0.3769 | 0.4308 | metal_dependent_hydrolase |
| m_csa:540 | 0.40915 | -0.0324 | True | 0.4002 | 0.4181 | metal_dependent_hydrolase |
| m_csa:134 | 0.40925 | -0.0323 | True | 0.391 | 0.4275 | metal_dependent_hydrolase |
| m_csa:130 | 0.41015 | -0.0314 | True | 0.4061 | 0.4142 | metal_dependent_hydrolase |
| m_csa:88 | 0.41345 | -0.0281 | True | 0.4188 | 0.4081 | metal_dependent_hydrolase |
| m_csa:209 | 0.4348 | -0.00675 | True | 0.5398 | 0.3298 | metal_dependent_hydrolase |
| m_csa:126 | 0.5127 | 0.07115 | False | 0.421 | 0.6044 | metal_dependent_hydrolase |
| m_csa:390 | 0.48795 | 0.0464 | False | 0.4323 | 0.5436 | metal_dependent_hydrolase |
| m_csa:325 | 0.4878 | 0.04625 | False | 0.4216 | 0.554 | metal_dependent_hydrolase |
| m_csa:537 | 0.4835 | 0.04195 | False | 0.3857 | 0.5813 | metal_dependent_hydrolase |
| m_csa:547 | 0.46725 | 0.0257 | False | 0.3899 | 0.5446 | metal_dependent_hydrolase |
| m_csa:284 | 0.45095 | 0.0094 | False | 0.4067 | 0.4952 | metal_dependent_hydrolase |

### Current Surface Unscored Candidates

| entry | accession | geometry status | nearest atlas | nearest fingerprint | tm |
| --- | --- | --- | --- | --- | ---: |
| m_csa:204 | P10746 | missing | m_csa:337 | ser_his_acid_hydrolase | 0.5651 |
| m_csa:604 | Q43088 | missing | m_csa:528 | metal_dependent_hydrolase | 0.4713 |
| m_csa:562 | P07658 | predicted_structure_fetch_failed | None | None | None |
| m_csa:416 | P07071 | predicted_structure_fetch_failed | None | None | None |
| m_csa:637 | P04531 | predicted_structure_fetch_failed | None | None | None |
| m_csa:586 | P00806 | predicted_structure_fetch_failed | None | None | None |

## Evidence Requests

| priority | entry | margin | axis | nearest fingerprint | top1 fingerprint |
| --- | --- | ---: | --- | --- | --- |
| priority_1_high_cofactor_retained_proxy_gap | m_csa:289 | 0.19825 | high_cofactor_confounded_proxy_extension | flavin_dehydrogenase_reductase | flavin_dehydrogenase_reductase |
| priority_1_high_cofactor_retained_proxy_gap | m_csa:298 | 0.09285 | high_cofactor_confounded_proxy_extension | flavin_dehydrogenase_reductase | flavin_monooxygenase |
| priority_1_high_cofactor_retained_proxy_gap | m_csa:361 | 0.0154 | high_cofactor_confounded_proxy_extension | flavin_dehydrogenase_reductase | metal_dependent_hydrolase |
| priority_1_high_cofactor_retained_proxy_gap | m_csa:368 | 0.01215 | high_cofactor_confounded_proxy_extension | flavin_dehydrogenase_reductase | heme_peroxidase_oxidase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:308 | 0.2396 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:187 | 0.2102 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:269 | 0.2091 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:104 | 0.20825 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:348 | 0.20745 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:468 | 0.2007 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:488 | 0.1989 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:206 | 0.1969 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:190 | 0.19495 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:483 | 0.19255 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:25 | 0.18255 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:500 | 0.1778 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:256 | 0.1777 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:52 | 0.17385 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:74 | 0.1715 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:59 | 0.1662 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:464 | 0.1614 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:502 | 0.15415 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:451 | 0.14645 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:638 | 0.14465 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:84 | 0.126 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:503 | 0.1111 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:463 | 0.1061 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:229 | 0.10225 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:533 | 0.10075 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:646 | 0.1003 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:322 | 0.0922 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:135 | 0.09015 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:36 | 0.0763 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:223 | 0.06625 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:645 | 0.0646 | hard_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:585 | 0.04515 | near_threshold_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:405 | 0.04215 | near_threshold_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:422 | 0.0311 | near_threshold_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:244 | 0.03085 | near_threshold_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:240 | 0.03005 | near_threshold_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:299 | 0.02965 | near_threshold_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:565 | 0.0268 | near_threshold_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:621 | 0.01865 | near_threshold_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:91 | 0.0174 | near_threshold_same_family_structural_counteraxis | ser_his_acid_hydrolase | ser_his_acid_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:234 | 0.0134 | near_threshold_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:280 | 0.0055 | near_threshold_same_family_structural_counteraxis | ser_his_acid_hydrolase | ser_his_acid_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:498 | 0.00505 | near_threshold_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:119 | 0.00475 | near_threshold_same_family_structural_counteraxis | metal_dependent_hydrolase | metal_dependent_hydrolase |

## Decision

- Apply or change threshold now: False
- Deployment closed now: False
- Evidence extension ready for threshold rerun: False
- Next gate: Do not raise the fixed threshold. Add or review train/cal confounded proxy rows beyond the currently scored surface on the evidence axes listed here, then rerun the proxy operating-point audit and threshold stress. Independently resolve the P10746 caveat or approved non-residue sidecar before claiming deployment closure.

## Interpretation

- At the unchanged fixed threshold, proxy calibration needs more train/cal evidence rather than a higher deployment threshold.
- Start with the one high-cofactor retained gap, then the hard same-family structural retained gaps; the current train/cal surface has no unused high-cofactor pool and loose same-family membership still misses the 80% target, so new proxy evidence is required before a rerun can close the calibration claim.
