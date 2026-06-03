# Fold-Augmented Confounded Proxy Extended Train/Cal OOS Surface - current702

Run: 2026-06-03T15:38:59Z

Extended train/cal OOS-negative surface for the Lever 3 confounded-proxy operating-point audit. It appends scored non-heldout tranche rows to the existing expanded surface and does not select, tune, or change thresholds.

## Status

- confounded_proxy_extended_train_cal_oos_surface_partial
- Blockers: ['remaining_fold_only_policy_caveat_not_combined_scored', 'scored_extension_has_blockers', 'some_extended_train_cal_oos_rows_missing_full_channel_scores']
- Full-channel rows: 186/192
- Appended rows: 66
- Appended full-channel rows: 64
- Remaining combined-score blockers: 6

## Appended Rows

| row | combined | abstains if fixed threshold applied |
| --- | ---: | --- |
| m_csa:309 | 0.3913 | see operating-point audit |
| m_csa:138 | 0.535 | see operating-point audit |
| m_csa:380 | 0.47015 | see operating-point audit |
| m_csa:48 | 0.4612 | see operating-point audit |
| m_csa:637 | None | unscored |
| m_csa:223 | 0.5078 | see operating-point audit |
| m_csa:508 | 0.42915 | see operating-point audit |
| m_csa:451 | 0.588 | see operating-point audit |
| m_csa:231 | 0.4688 | see operating-point audit |
| m_csa:350 | 0.3817 | see operating-point audit |
| m_csa:280 | 0.44705 | see operating-point audit |
| m_csa:70 | 0.47955 | see operating-point audit |
| m_csa:150 | 0.4438 | see operating-point audit |
| m_csa:151 | 0.4988 | see operating-point audit |
| m_csa:310 | 0.4432 | see operating-point audit |
| m_csa:359 | 0.4292 | see operating-point audit |
| m_csa:72 | 0.42285 | see operating-point audit |
| m_csa:640 | 0.51735 | see operating-point audit |
| m_csa:84 | 0.56755 | see operating-point audit |
| m_csa:194 | 0.4559 | see operating-point audit |
| m_csa:463 | 0.54765 | see operating-point audit |
| m_csa:190 | 0.6365 | see operating-point audit |
| m_csa:450 | 0.38735 | see operating-point audit |
| m_csa:224 | 0.4011 | see operating-point audit |
| m_csa:405 | 0.4837 | see operating-point audit |
| m_csa:638 | 0.5862 | see operating-point audit |
| m_csa:312 | 0.5714 | see operating-point audit |
| m_csa:256 | 0.61925 | see operating-point audit |
| m_csa:587 | 0.45975 | see operating-point audit |
| m_csa:74 | 0.61305 | see operating-point audit |
| m_csa:237 | 0.4887 | see operating-point audit |
| m_csa:282 | 0.38295 | see operating-point audit |
| m_csa:146 | 0.43465 | see operating-point audit |
| m_csa:585 | 0.4867 | see operating-point audit |
| m_csa:229 | 0.5438 | see operating-point audit |
| m_csa:236 | 0.56265 | see operating-point audit |
| m_csa:24 | 0.43875 | see operating-point audit |
| m_csa:265 | 0.3886 | see operating-point audit |
| m_csa:364 | 0.51145 | see operating-point audit |
| m_csa:505 | 0.4158 | see operating-point audit |
| m_csa:586 | None | unscored |
| m_csa:603 | 0.4415 | see operating-point audit |
| m_csa:107 | 0.5142 | see operating-point audit |
| m_csa:645 | 0.50615 | see operating-point audit |
| m_csa:234 | 0.45495 | see operating-point audit |
| m_csa:441 | 0.41695 | see operating-point audit |
| m_csa:621 | 0.4602 | see operating-point audit |
| m_csa:460 | 0.5277 | see operating-point audit |
| m_csa:500 | 0.61935 | see operating-point audit |
| m_csa:533 | 0.5423 | see operating-point audit |
| m_csa:209 | 0.4348 | see operating-point audit |
| m_csa:273 | 0.4133 | see operating-point audit |
| m_csa:293 | 0.4763 | see operating-point audit |
| m_csa:322 | 0.53375 | see operating-point audit |
| m_csa:391 | 0.4853 | see operating-point audit |
| m_csa:421 | 0.61545 | see operating-point audit |
| m_csa:371 | 0.5353 | see operating-point audit |
| m_csa:8 | 0.52555 | see operating-point audit |
| m_csa:206 | 0.63845 | see operating-point audit |
| m_csa:91 | 0.45895 | see operating-point audit |
| m_csa:200 | 0.4614 | see operating-point audit |
| m_csa:187 | 0.65175 | see operating-point audit |
| m_csa:88 | 0.41345 | see operating-point audit |
| m_csa:59 | 0.60775 | see operating-point audit |
| m_csa:269 | 0.65065 | see operating-point audit |
| m_csa:348 | 0.649 | see operating-point audit |

## Remaining Blockers

- m_csa:204
- m_csa:416
- m_csa:562
- m_csa:586
- m_csa:604
- m_csa:637

## Interpretation

- The extended train/cal OOS surface now has 186/192 full-channel rows, including 64 newly appended scored tranche rows.
- Rerun the fixed-threshold confounded proxy operating-point audit against this extended surface; keep the threshold unchanged and heldout final-only.
