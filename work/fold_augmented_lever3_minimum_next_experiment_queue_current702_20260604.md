# Fold-Augmented Lever 3 Minimum Next Experiment Queue - current702

Run: 2026-06-04T16:38:55Z

Review-only queue of the smallest remaining Lever 3 experiments needed before any fixed-threshold novelty/abstention readout can be treated as deployment-valid and confounded-safe.

## Status

- fold_augmented_lever3_minimum_next_experiment_queue_blocked
- Blocked experiment steps: 3
- P07658 failed acceptance checks: 7
- Missing high-cofactor train/cal rows: 16
- Missing same-family structural train/cal rows: 170
- Guardrail violation artifacts: 0

## Experiment Queue

| priority | experiment | gate | missing rows | blocked |
| ---: | --- | --- | ---: | --- |
| 1 | p07658_full_length_prediction_acceptance | surface_completeness_before_fixed_threshold_readout | 1 | True |
| 2 | high_cofactor_train_cal_oos_acquisition | confounded_safe_high_cofactor_calibration | 16 | True |
| 3 | same_family_structural_train_cal_oos_acquisition | confounded_safe_same_family_structural_calibration | 170 | True |

## Decision

- Current evidence can clear Lever 3 done-bar now: False
- Fixed-threshold audit ready to rerun now: False
- First experiment: p07658_full_length_prediction_acceptance
- Next gate: Run or provision an approved full-length predictor/provider on the frozen P07658 sequence, write coordinate provenance with provider/model/version/path/checksum and sequence hash, then rerun this acceptance preflight.

## Interpretation

- Lever 3 remains blocked by P07658 surface completeness, 16 missing high-cofactor train/cal OOS rows, and 170 missing same-family structural train/cal OOS rows.
- Run the priority-1 P07658 full-length prediction acceptance experiment first, then acquire source-free high-cofactor rows before the larger same-family structural acquisition.
