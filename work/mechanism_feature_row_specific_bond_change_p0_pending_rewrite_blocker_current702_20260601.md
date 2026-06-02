# Mechanism Feature Row-Specific Bond-Change P0 Pending Rewrite Blocker - current702

Run: 2026-06-02T09:19:57Z

Manual rewrite blocker packet for P0 row-specific bond/proton/electron rows that were reviewed but kept out of feature consumption because current events are low-confidence, unmapped, or too complex.

## Status

- p0_pending_rewrite_blocker_cleared_ready_for_no_template_rerun
- Pending rewrite rows: 0
- Blocked event rows: 0
- Approved materialized rows: 15
- Approved train/cal split: 11 train, 4 calibration
- Blocked event types: {}
- Critical violations: 0

## Rows

| row | split | blocked events | blockers | decision |
| --- | --- | ---: | --- | --- |

## Interpretation

- All reviewed P0 rewrite blockers are cleared and the full train/cal row-specific feature surface is materialized.
- Attempt no-template centroid/residual reruns only from the label-stripped train/cal feature sidecar, then keep heldout as a read-once final evaluation surface.
