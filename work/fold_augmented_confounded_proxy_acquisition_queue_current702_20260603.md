# Fold-Augmented Confounded Proxy Acquisition Queue - current702

Run: 2026-06-03T15:39:12Z

Lever 3 acquisition queue for closing the train/cal confounded-proxy calibration gap at the fixed operating point. It consumes the evidence-extension plan and family-panel acceptance scenario to distinguish calibration-eligible train/cal OOS rows from review-only breadth rows.

## Status

- fold_augmented_confounded_proxy_acquisition_queue_blocked
- Fixed threshold: 0.44155 (combined_mean_geometry_fold)
- Evidence request rows: 48
- Existing retained-gap queue rows: 48
- Loose same-family current-surface rows: 21
- Family-panel scenario rows: 6
- Scenario train/cal OOS eligible now: 0
- Scenario heldout confounded rows: 4
- High-cofactor shortfall after scenario: 16
- Structural shortfall after scenario: 170
- Blockers: ['high_cofactor_proxy_acquisition_shortfall_16', 'same_family_structural_proxy_acquisition_shortfall_170', 'family_panel_acceptance_scenario_rows_do_not_close_train_cal_proxy_calibration', 'heldout_confounded_scenario_rows_guardrailed', 'current_surface_unscored_candidate_not_scale_evidence', 'loosened_current_surface_still_below_structural_80pct']

## Decision

- Apply/change threshold now: False
- Proxy calibration rerun ready now: False
- Family-panel acceptance closes proxy calibration now: False
- Heldout rows available for train/tune: False
- Next gate: Acquire or review new non-heldout train/cal OOS proxy rows on the high-cofactor and same-family structural axes, then rerun the fixed-threshold proxy operating-point audit and threshold stress. Keep family-panel accept decisions on the separate Lever 4 import-preview/label-factory path.

## Acquisition Tracks

| track | axis | eligible now | shortfall | status |
| --- | --- | ---: | ---: | --- |
| high_cofactor_train_cal_oos_extension | high_cofactor_signature_proxy | 0 | 16 | blocked_need_new_train_cal_oos_proxy_rows |
| same_family_structural_train_cal_oos_extension | same_family_structural_proxy | 0 | 170 | blocked_need_new_train_cal_oos_structural_proxy_rows |
| lever4_family_panel_breadth | benchmark_breadth_not_calibration | 0 |  | review_only_breadth_path_not_lever3_calibration_closure |
| p10746_unscored_current_surface_candidate | deployment_caveat_or_non_residue_sidecar | 0 |  | blocked_missing_predicted_geometry_not_scale_evidence |

## Family-Panel Calibration Screen

| row | panel | axes | eligible now | reasons |
| --- | --- | --- | ---: | --- |
| m_csa:973 | flavin_monooxygenase_and_flavin_oxygen_transfer | high_cofactor_signature_proxy | 0 | not_train_cal_oos_calibration_row_label_type |
| m_csa:30 | glycyl_radical_or_thiamine_radical_lyase_boundary | high_cofactor_signature_proxy | 0 | current_heldout_confounded_oos_row_not_allowed_for_train_cal_calibration, not_on_train_cal_feature_manifest |
| m_csa:31 | glycyl_radical_or_thiamine_radical_lyase_boundary | high_cofactor_signature_proxy | 0 | current_heldout_confounded_oos_row_not_allowed_for_train_cal_calibration, not_on_train_cal_feature_manifest |
| m_csa:448 | lipoamide_or_sulfur_transfer_redox_boundary | high_cofactor_signature_proxy | 0 | current_heldout_confounded_oos_row_not_allowed_for_train_cal_calibration, not_on_train_cal_feature_manifest |
| m_csa:10 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | same_family_structural_proxy | 0 | not_on_train_cal_feature_manifest |
| m_csa:191 | thiol_disulfide_oxidoreductase_isomerase_boundary | high_cofactor_signature_proxy | 0 | current_heldout_confounded_oos_row_not_allowed_for_train_cal_calibration, not_on_train_cal_feature_manifest |

## Retained Gap Queue

| row | axis | priority | margin | role |
| --- | --- | --- | ---: | --- |
| m_csa:289 | high_cofactor_confounded_proxy_extension | priority_1_high_cofactor_retained_proxy_gap | 0.19825 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:298 | high_cofactor_confounded_proxy_extension | priority_1_high_cofactor_retained_proxy_gap | 0.09285 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:361 | high_cofactor_confounded_proxy_extension | priority_1_high_cofactor_retained_proxy_gap | 0.0154 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:368 | high_cofactor_confounded_proxy_extension | priority_1_high_cofactor_retained_proxy_gap | 0.01215 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:308 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.2396 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:187 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.2102 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:269 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.2091 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:104 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.20825 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:348 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.20745 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:468 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.2007 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:488 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.1989 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:206 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.1969 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:190 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.19495 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:483 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.19255 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:25 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.18255 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:500 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.1778 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:256 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.1777 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:52 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.17385 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:74 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.1715 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:59 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.1662 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:464 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.1614 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:502 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.15415 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:451 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.14645 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:638 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.14465 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:84 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.126 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:503 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.1111 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:463 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.1061 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:229 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.10225 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:533 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.10075 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:646 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.1003 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:322 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.0922 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:135 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.09015 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:36 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.0763 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:223 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.06625 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:645 | hard_same_family_structural_counteraxis | priority_2_hard_retained_structural_proxy_gap | 0.0646 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:585 | near_threshold_same_family_structural_counteraxis | priority_3_near_threshold_retained_structural_proxy_gap | 0.04515 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:405 | near_threshold_same_family_structural_counteraxis | priority_3_near_threshold_retained_structural_proxy_gap | 0.04215 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:422 | near_threshold_same_family_structural_counteraxis | priority_3_near_threshold_retained_structural_proxy_gap | 0.0311 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:244 | near_threshold_same_family_structural_counteraxis | priority_3_near_threshold_retained_structural_proxy_gap | 0.03085 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:240 | near_threshold_same_family_structural_counteraxis | priority_3_near_threshold_retained_structural_proxy_gap | 0.03005 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:299 | near_threshold_same_family_structural_counteraxis | priority_3_near_threshold_retained_structural_proxy_gap | 0.02965 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:565 | near_threshold_same_family_structural_counteraxis | priority_3_near_threshold_retained_structural_proxy_gap | 0.0268 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:621 | near_threshold_same_family_structural_counteraxis | priority_3_near_threshold_retained_structural_proxy_gap | 0.01865 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:91 | near_threshold_same_family_structural_counteraxis | priority_3_near_threshold_retained_structural_proxy_gap | 0.0174 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:234 | near_threshold_same_family_structural_counteraxis | priority_3_near_threshold_retained_structural_proxy_gap | 0.0134 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:280 | near_threshold_same_family_structural_counteraxis | priority_3_near_threshold_retained_structural_proxy_gap | 0.0055 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:498 | near_threshold_same_family_structural_counteraxis | priority_3_near_threshold_retained_structural_proxy_gap | 0.00505 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |
| m_csa:119 | near_threshold_same_family_structural_counteraxis | priority_3_near_threshold_retained_structural_proxy_gap | 0.00475 | diagnose retained train/cal proxy gaps; does not add new abstained proxy evidence by itself |

## Interpretation

- The current family-panel acceptance scenario supplies 0 train/cal OOS rows for the Lever 3 proxy-calibration rerun.
- The fixed-threshold Lever 3 gap remains a new-evidence problem: 16 high-cofactor and 170 structural abstained train/cal proxy rows are still needed under the all-new-rows-abstain lower bound.
- Do not raise the threshold or reuse heldout canaries. Source new train/cal proxy rows outside the current scored surface, score them at the unchanged threshold, and rerun the proxy operating-point/stress artifacts.
