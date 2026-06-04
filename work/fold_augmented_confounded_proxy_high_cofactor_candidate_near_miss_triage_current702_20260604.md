# Fold-Augmented Confounded Proxy High-Cofactor Candidate Near-Miss Triage - current702

Run: 2026-06-04T11:42:38Z

Train/cal-only review packet for the high-cofactor 16-row acquisition blocker. It sorts the existing ready train/cal OOS candidate pool by source-free organic cofactor score and records that no row satisfies the frozen high-cofactor proxy membership. It registers no rows, scores no candidates, and does not change threshold 0.44155.

## Status

- fold_augmented_confounded_proxy_high_cofactor_candidate_near_miss_triage_blocked_zero_eligible_rows
- Ready train/cal OOS rows: 353
- Priority candidate rows available: 80
- High-cofactor-axis candidate rows: 0
- Minimum new abstained rows for 80%: 16
- Near misses reported: 16
- Blockers: ['current_train_cal_candidate_pool_has_zero_high_cofactor_axis_rows', 'candidate_rows_not_acquired_or_reviewed', 'candidate_rows_not_scored_at_fixed_threshold', 'fixed_threshold_audit_not_ready_to_rerun']

## Decision

- Current pool can supply 16 high-cofactor rows: False
- Candidate rows ready to score now: False
- Fixed-threshold audit ready to rerun now: False
- Next gate: Do not relax proxy membership or threshold 0.44155 based on near misses. Source new eligible high-cofactor rows or define and pre-register a new source-free proxy axis before scoring.

## Near Miss Rows

| rank | row | organic max | axes | reason |
| ---: | --- | --- | --- | --- |
| 1 | m_csa:288 | heme:0.407563 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |
| 2 | m_csa:89 | heme:0.398339 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |
| 3 | m_csa:214 | plp:0.353171 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |
| 4 | m_csa:75 | heme:0.34378 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |
| 5 | m_csa:60 | plp:0.337092 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |
| 6 | m_csa:583 | heme:0.296056 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |
| 7 | m_csa:64 | plp:0.246623 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |
| 8 | m_csa:607 | heme:0.236789 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |
| 9 | m_csa:610 | plp:0.222226 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |
| 10 | m_csa:618 | flavin:0.215006 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |
| 11 | m_csa:555 | flavin:0.213904 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |
| 12 | m_csa:404 | heme:0.193581 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |
| 13 | m_csa:26 | plp:0.177608 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |
| 14 | m_csa:515 | plp:0.150245 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |
| 15 | m_csa:232 | plp:0.147019 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |
| 16 | m_csa:351 | plp:0.144021 | background_train_cal_oos_structural_pool | current source-free cofactor/locus axes do not mark this row as high-cofactor candidate |

## Interpretation

- The existing ready train/cal OOS candidate pool cannot supply the required 16 high-cofactor rows: 0 rows satisfy the frozen high-cofactor axis, even though the packet lists the top source-free organic-cofactor near misses.
- Acquire genuinely new high-cofactor train/cal OOS rows or pre-register a new source-free proxy axis; do not score or tune near misses as if they closed the high-cofactor blocker.
