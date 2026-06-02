# Mechanism Feature Row-Specific Bond-Change P0 Train/Cal Coverage Gap - current702

Run: 2026-06-02T09:19:56Z

Review-priority audit for the partial P0 row-specific train/cal feature sidecar. It identifies draft rows that would add missing calibration coverage or new event-type coverage before any no-template rerun.

## Status

- p0_train_cal_feature_coverage_gap_ready_review_queue
- Materialized train rows: 11
- Materialized calibration rows: 4
- Draft train rows: 0
- Draft calibration rows: 0
- Priority classes: {}
- Missing event types: {}

## Decision

- Full no-template rerun ready: True
- Rerun blocked by calibration coverage: False
- Next review gate rows: (none)

## Review Priorities

| row | split | priority | category | event types | blockers |
| --- | --- | --- | --- | --- | --- |

## Interpretation

- The approved P0 train/cal feature surface is materialized but train-only; calibration-assigned draft rows are the next review gate before rerunning no-template novelty methods.
- Review the listed P0.1 calibration rows, record decisions in the source-evidence sidecar, rerun strict/readiness audits, then rerun the train/cal materialization sidecar.
