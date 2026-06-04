# Fold-Augmented Lever 3 Residual Safety Readout - current702

Run: 2026-06-04T19:44:53Z

Lever 3 measured residual-safety readout for the hard-confounded train/cal OOS rows left retained by the best current source-free route. It uses only prior train/cal-selected channel diagnostics; it reads no heldout rows, scores no new rows, stages no coordinates, and does not select or change thresholds.

## Status

- fold_augmented_lever3_residual_safety_readout_ready_residual_unsafe_transfer
- Best current route: channel_union::cofactor_max_score+combined_mean_geometry_cofactor_fold+combined_mean_geometry_fold+combined_min_geometry_fold+fold_nearest_atlas_tm_score
- Best route in-scope retained/lost: 20/14
- Residual high-cofactor/same-family rows: 1/21
- Unique residual rows: 21
- Retained by all current channels: 21
- Near/wide selected-threshold margins: 16/5
- Closest-channel shifts preserving in-scope floor: 0/21
- Any-channel shifts preserving in-scope floor: 0/21

## Residual Rows

| row | axes | closest channel | margin | retained by all channels | evidence need |
| --- | --- | --- | ---: | --- | --- |
| m_csa:25 | same_family | combined_min_geometry_fold | 0.0398 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:52 | same_family | cofactor_max_score | 0.062269 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:74 | same_family | cofactor_max_score | 0.011125 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:84 | same_family | cofactor_max_score | 0.026454 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:89 | same_family | combined_mean_geometry_fold | 0.00845 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:135 | same_family | combined_mean_geometry_cofactor_fold | 0.048023 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:190 | same_family | cofactor_max_score | 0.025247 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:223 | same_family | combined_mean_geometry_cofactor_fold | 0.003929 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:229 | same_family | cofactor_max_score | 0.004742 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:256 | same_family | cofactor_max_score | 0.015781 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:289 | high_cofactor, same_family | combined_min_geometry_fold | 0.0287 | True | new_source_free_cofactor_role_and_same_family_counteraxis_required |
| m_csa:308 | same_family | combined_mean_geometry_cofactor_fold | 0.19385 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:451 | same_family | cofactor_max_score | 0.042344 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:463 | same_family | combined_mean_geometry_cofactor_fold | 0.023826 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:464 | same_family | cofactor_max_score | 0.006482 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:468 | same_family | combined_mean_geometry_cofactor_fold | 0.131121 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:488 | same_family | cofactor_max_score | 0.061709 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:502 | same_family | combined_mean_geometry_cofactor_fold | 0.108381 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:503 | same_family | cofactor_max_score | 0.021129 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:638 | same_family | cofactor_max_score | 0.019535 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:646 | same_family | combined_min_geometry_fold | 0.0287 | True | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |

## Any-Channel Shift Diagnostics

| row | best current channel by in-scope preservation | in-scope retained if shifted | in-scope loss | floor met |
| --- | --- | ---: | ---: | --- |
| m_csa:25 | geometry_top1_score | 24 | 10 | False |
| m_csa:52 | combined_mean_geometry_cofactor_fold | 24 | 10 | False |
| m_csa:74 | cofactor_max_score | 27 | 7 | False |
| m_csa:84 | combined_mean_geometry_cofactor_fold | 26 | 8 | False |
| m_csa:89 | combined_mean_geometry_fold | 30 | 4 | False |
| m_csa:135 | combined_mean_geometry_cofactor_fold | 25 | 9 | False |
| m_csa:190 | cofactor_max_score | 24 | 10 | False |
| m_csa:223 | combined_mean_geometry_cofactor_fold | 30 | 4 | False |
| m_csa:229 | cofactor_max_score | 28 | 6 | False |
| m_csa:256 | cofactor_max_score | 25 | 9 | False |
| m_csa:289 | combined_min_geometry_fold | 25 | 9 | False |
| m_csa:308 | combined_mean_geometry_cofactor_fold | 19 | 15 | False |
| m_csa:451 | combined_mean_geometry_cofactor_fold | 25 | 9 | False |
| m_csa:463 | combined_mean_geometry_cofactor_fold | 27 | 7 | False |
| m_csa:464 | cofactor_max_score | 28 | 6 | False |
| m_csa:468 | combined_mean_geometry_cofactor_fold | 22 | 12 | False |
| m_csa:488 | combined_mean_geometry_cofactor_fold | 22 | 12 | False |
| m_csa:502 | combined_mean_geometry_cofactor_fold | 22 | 12 | False |
| m_csa:503 | combined_mean_geometry_cofactor_fold | 27 | 7 | False |
| m_csa:638 | combined_mean_geometry_cofactor_fold | 25 | 9 | False |
| m_csa:646 | combined_mean_geometry_fold | 25 | 9 | False |

## Decision

- Current source-free channels can resolve residual rows: False
- Current evidence sufficient for deployment closure: False
- Exact missing evidence: ['one source-free high-cofactor/cofactor-role counteraxis that abstains m_csa:289 while preserving the train/cal in-scope retention floor; all current source-free channels retain this row', 'a source-free same-family chemistry or pocket-architecture counteraxis that abstains at least 10 of 21 retained same-family residual rows; all current source-free channels retain the residual set', 'accepted full-length P07658 predicted coordinate provenance before fixed-threshold surface rerun']
- Next gate: Do not change threshold 0.44155. The remaining hard-confounded residual rows are retained by every current source-free channel, so continue with new deployment-valid evidence: accepted P07658 prediction provenance, then a strict high-cofactor/cofactor-role counteraxis measured on train/cal rows.

## Interpretation

- The residual unsafe-transfer set is not catchable by another union of current source-free channel thresholds.
- 21 unique hard-confounded residual rows remain under the best current route; 21 are retained by every current channel. The high-cofactor shortfall is 1 row and the same-family shortfall is 10 rows.
- Treat near-threshold residuals as diagnostics only, not tuning permission: any-channel threshold shifts would preserve the in-scope floor for 0/21 residual rows. Add a new source-free chemistry/cofactor-role counteraxis or acquire accepted strict high-cofactor train/cal OOS rows before any fixed-threshold rerun.
