# Fold-Augmented Confounded Proxy Extended Train/Cal OOS Surface - current702

Run: 2026-06-03T19:43:41Z

Extended train/cal OOS-negative surface for the Lever 3 confounded-proxy operating-point audit. It appends scored non-heldout tranche rows to the existing expanded surface and does not select, tune, or change thresholds.

## Status

- confounded_proxy_extended_train_cal_oos_surface_partial
- Blockers: ['remaining_fold_only_policy_caveat_not_combined_scored', 'scored_extension_has_blockers', 'some_extended_train_cal_oos_rows_missing_full_channel_scores']
- Full-channel rows: 204/210
- Appended rows: 8
- Appended full-channel rows: 8
- Remaining combined-score blockers: 6

## Appended Rows

| row | combined | abstains if fixed threshold applied |
| --- | ---: | --- |
| m_csa:610 | 0.43915 | see operating-point audit |
| m_csa:137 | 0.2836 | see operating-point audit |
| m_csa:318 | 0.34875 | see operating-point audit |
| m_csa:360 | 0.5407 | see operating-point audit |
| m_csa:105 | 0.40305 | see operating-point audit |
| m_csa:327 | 0.36295 | see operating-point audit |
| m_csa:649 | 0.37305 | see operating-point audit |
| m_csa:618 | 0.43035 | see operating-point audit |

## Remaining Blockers

- m_csa:204
- m_csa:416
- m_csa:562
- m_csa:586
- m_csa:604
- m_csa:637

## Interpretation

- The extended train/cal OOS surface now has 204/210 full-channel rows, including 8 newly appended scored tranche rows.
- Do not rerun the fixed-threshold confounded proxy operating-point audit on this partial surface yet; clear the remaining full-channel score blockers first.
