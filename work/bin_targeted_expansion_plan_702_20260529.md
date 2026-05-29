# Bin-targeted Expansion Plan

Run: 2026-05-29T13:09:52Z

Review-only plan. No labels, registries, imports, production scoring, or thresholds were changed.

## Current Gaps

| Bin | Primary | Primary gap | OOS/sec | OOS/sec gap | Priority |
| --- | ---: | ---: | ---: | ---: | --- |
| no_reliable_structure | 5 | 25 | 1 | 9 | high_primary_and_oos_gap |
| low_structure_neighborhood_near_orphan | 30 | 0 | 0 | 10 | high_oos_control_gap |

## Recommendation

First batch: `near_orphan_oos_control_materialization`.
near_orphan already has primary support at the target but lacks OOS/secondary controls; no_reliable_structure remains underpowered on both primary and OOS support.

Required before metric use: review-only materialization/scoring, expert decision artifact, label-factory gates, batch acceptance, new frozen split or pre-registered eval slice.
