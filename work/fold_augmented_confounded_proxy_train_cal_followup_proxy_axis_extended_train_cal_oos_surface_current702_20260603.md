# Fold-Augmented Confounded Proxy Extended Train/Cal OOS Surface - current702

Run: 2026-06-03T18:10:20Z

Extended train/cal OOS-negative surface for the Lever 3 confounded-proxy operating-point audit. It appends scored non-heldout tranche rows to the existing expanded surface and does not select, tune, or change thresholds.

## Status

- confounded_proxy_extended_train_cal_oos_surface_partial
- Blockers: ['remaining_fold_only_policy_caveat_not_combined_scored', 'scored_extension_has_blockers', 'some_extended_train_cal_oos_rows_missing_full_channel_scores']
- Full-channel rows: 196/202
- Appended rows: 4
- Appended full-channel rows: 4
- Remaining combined-score blockers: 6

## Appended Rows

| row | combined | abstains if fixed threshold applied |
| --- | ---: | --- |
| m_csa:60 | 0.4709 | see operating-point audit |
| m_csa:75 | 0.4884 | see operating-point audit |
| m_csa:214 | 0.4598 | see operating-point audit |
| m_csa:288 | 0.41995 | see operating-point audit |

## Remaining Blockers

- m_csa:204
- m_csa:416
- m_csa:562
- m_csa:586
- m_csa:604
- m_csa:637

## Interpretation

- The extended train/cal OOS surface now has 196/202 full-channel rows, including 4 newly appended scored tranche rows.
- Do not rerun the fixed-threshold confounded proxy operating-point audit on this partial surface yet; clear the remaining full-channel score blockers first.
