# Fold-Augmented Confounded Proxy Train/Cal Scoring Tranche Plan - current702

Run: 2026-06-03T15:39:12Z

Bounded train/cal-only scoring tranche plan for the Lever 3 confounded-proxy acquisition gap. It selects unscored candidate rows for future predicted-structure-vs-atlas scoring; it does not run scoring, read heldout rows, or change thresholds.

## Status

- fold_augmented_confounded_proxy_train_cal_scoring_tranche_plan_blocked
- Tranche rows: 0
- Selected high-cofactor-axis rows: 0
- Selected structural-axis rows: 0
- High shortfall: 16
- Structural shortfall: 170
- Blockers: ['scoring_tranche_not_run', 'selected_high_cofactor_rows_below_shortfall', 'selected_structural_rows_below_shortfall']

## Decision

- Score tranche now: False
- Apply/change threshold now: False
- Proxy calibration rerun ready now: False
- Tranche ready for scoring plan: False
- Next gate: Run predicted-structure-vs-atlas scoring for exactly these tranche rows, join the resulting fixed-channel scores back to train/cal only, then rerun the proxy operating-point audit without changing threshold 0.44155.

## Scoring Tranche Rows

| row | reason | bucket | axes | organic max |
| --- | --- | ---: | --- | --- |

## Interpretation

- 0 train/cal OOS rows are selected for the next fixed-threshold scoring tranche.
- The tranche covers 0 high-cofactor-axis rows for a 16-row lower bound and 0 structural-axis rows for a 170-row lower bound, by count only.
- Score the tranche; do not count any row as new abstained proxy evidence until the actual fixed-threshold scores exist.
