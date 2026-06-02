# Mechanism Feature Row-Specific Bond-Change P0 Pending Rewrite Blocker - current702

Run: 2026-06-02T08:23:35Z

Manual rewrite blocker packet for P0 row-specific bond/proton/electron rows that were reviewed but kept out of feature consumption because current events are low-confidence, unmapped, or too complex.

## Status

- p0_pending_rewrite_blocker_ready_manual_only
- Pending rewrite rows: 6
- Blocked event rows: 16
- Approved materialized rows: 9
- Approved train/cal split: 7 train, 2 calibration
- Blocked event types: {'electron_transfer': 16}
- Critical violations: 0

## Rows

| row | split | blocked events | blockers | decision |
| --- | --- | ---: | --- | --- |
| m_csa:6 | calibration | 4 | low_confidence_event_review, unmapped_event_review, multi_event_rewrite | rewrite_events_and_keep_review_pending |
| m_csa:15 | train | 1 | low_confidence_event_review, unmapped_event_review | rewrite_events_and_keep_review_pending |
| m_csa:16 | train | 1 | low_confidence_event_review, unmapped_event_review | rewrite_events_and_keep_review_pending |
| m_csa:68 | train | 3 | low_confidence_event_review, unmapped_event_review | rewrite_events_and_keep_review_pending |
| m_csa:102 | train | 4 | low_confidence_event_review, unmapped_event_review, multi_event_rewrite | rewrite_events_and_keep_review_pending |
| m_csa:133 | calibration | 3 | low_confidence_event_review, unmapped_event_review, multi_event_rewrite | rewrite_events_and_keep_review_pending |

## Interpretation

- The calibration coverage blocker is cleared and the current approved P0 rows are materialized, but reviewed pending rows remain blocked by low-confidence or unmapped event surfaces.
- Rewrite or reject the listed blocked events, rerun strict/readiness/materialization artifacts, and only then attempt no-template centroid/residual reruns.
