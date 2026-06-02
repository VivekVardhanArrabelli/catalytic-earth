# Mechanism Feature Row-Specific Bond-Change P0 Train/Cal Coverage Gap - current702

Run: 2026-06-02T06:41:54Z

Review-priority audit for the partial P0 row-specific train/cal feature sidecar. It identifies draft rows that would add missing calibration coverage or new event-type coverage before any no-template rerun.

## Status

- p0_train_cal_feature_coverage_gap_ready_review_queue
- Materialized train rows: 3
- Materialized calibration rows: 0
- Draft train rows: 8
- Draft calibration rows: 4
- Priority classes: {'P0.1_calibration_coverage_unblocker': 4, 'P0.2_new_event_type_coverage': 1, 'P0.3_train_cal_depth': 7}
- Missing event types: {'bond_order_changed': 3}

## Decision

- Full no-template rerun ready: False
- Rerun blocked by calibration coverage: True
- Next review gate rows: m_csa:186, m_csa:147, m_csa:6, m_csa:133

## Review Priorities

| row | split | priority | category | event types | blockers |
| --- | --- | --- | --- | --- | --- |
| m_csa:186 | calibration | P0.1_calibration_coverage_unblocker | standard_draft_event_review | bond_broken, bond_order_changed | review_status_not_approved |
| m_csa:147 | calibration | P0.1_calibration_coverage_unblocker | high_complexity_multi_event_review | bond_order_changed, proton_transfer | review_status_not_approved, multi_event_mechanism_review |
| m_csa:6 | calibration | P0.1_calibration_coverage_unblocker | high_complexity_multi_event_review | electron_transfer, proton_transfer | review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review |
| m_csa:133 | calibration | P0.1_calibration_coverage_unblocker | high_complexity_multi_event_review | bond_formed, electron_transfer, proton_transfer | review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review |
| m_csa:66 | train | P0.2_new_event_type_coverage | standard_draft_event_review | bond_order_changed | review_status_not_approved |
| m_csa:37 | train | P0.3_train_cal_depth | standard_draft_event_review | electron_transfer | review_status_not_approved |
| m_csa:94 | train | P0.3_train_cal_depth | standard_draft_event_review | bond_formed | review_status_not_approved |
| m_csa:15 | train | P0.3_train_cal_depth | standard_draft_event_review | bond_formed, electron_transfer | review_status_not_approved, low_confidence_event_review |
| m_csa:16 | train | P0.3_train_cal_depth | standard_draft_event_review | electron_transfer, proton_transfer | review_status_not_approved, low_confidence_event_review |
| m_csa:68 | train | P0.3_train_cal_depth | standard_draft_event_review | electron_transfer | review_status_not_approved, low_confidence_event_review |
| m_csa:124 | train | P0.3_train_cal_depth | high_complexity_multi_event_review | electron_transfer, proton_transfer | review_status_not_approved, multi_event_mechanism_review |
| m_csa:102 | train | P0.3_train_cal_depth | high_complexity_multi_event_review | bond_broken, electron_transfer | review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review |

## Interpretation

- The approved P0 train/cal feature surface is materialized but train-only; calibration-assigned draft rows are the next review gate before rerunning no-template novelty methods.
- Review the listed P0.1 calibration rows, record decisions in the source-evidence sidecar, rerun strict/readiness audits, then rerun the train/cal materialization sidecar.
