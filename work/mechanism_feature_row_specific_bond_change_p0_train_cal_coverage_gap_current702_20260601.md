# Mechanism Feature Row-Specific Bond-Change P0 Train/Cal Coverage Gap - current702

Run: 2026-06-02T08:29:58Z

Review-priority audit for the partial P0 row-specific train/cal feature sidecar. It identifies draft rows that would add missing calibration coverage or new event-type coverage before any no-template rerun.

## Status

- p0_train_cal_feature_coverage_gap_ready_review_queue
- Materialized train rows: 7
- Materialized calibration rows: 2
- Draft train rows: 4
- Draft calibration rows: 2
- Priority classes: {'P0.3_train_cal_depth': 6}
- Missing event types: {}

## Decision

- Full no-template rerun ready: False
- Rerun blocked by calibration coverage: False
- Next review gate rows: (none)

## Review Priorities

| row | split | priority | category | event types | blockers |
| --- | --- | --- | --- | --- | --- |
| m_csa:15 | train | P0.3_train_cal_depth | standard_draft_event_review | bond_formed, electron_transfer | review_status_not_approved, low_confidence_event_review |
| m_csa:16 | train | P0.3_train_cal_depth | standard_draft_event_review | electron_transfer, proton_transfer | review_status_not_approved, low_confidence_event_review |
| m_csa:68 | train | P0.3_train_cal_depth | standard_draft_event_review | electron_transfer | review_status_not_approved, low_confidence_event_review |
| m_csa:6 | calibration | P0.3_train_cal_depth | high_complexity_multi_event_review | electron_transfer, proton_transfer | review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review |
| m_csa:102 | train | P0.3_train_cal_depth | high_complexity_multi_event_review | bond_broken, electron_transfer | review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review |
| m_csa:133 | calibration | P0.3_train_cal_depth | high_complexity_multi_event_review | bond_formed, electron_transfer, proton_transfer | review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review |

## Interpretation

- The approved P0 train/cal feature surface is materialized but train-only; calibration-assigned draft rows are the next review gate before rerunning no-template novelty methods.
- Review the listed P0.1 calibration rows, record decisions in the source-evidence sidecar, rerun strict/readiness audits, then rerun the train/cal materialization sidecar.
