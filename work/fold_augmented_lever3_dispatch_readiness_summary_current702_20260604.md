# Fold-Augmented Lever 3 Dispatch Readiness Summary - current702

Run: 2026-06-04T13:40:31Z

Combined Lever 3 dispatch readiness summary for the remaining deployment-valid/confounded-safe novelty blockers. It composes the P07658 provider dispatch and the high-cofactor/same-family train-cal intake packets; it does not source rows, stage coordinates, score rows, tune thresholds, or read heldout.

## Status

- fold_augmented_lever3_dispatch_readiness_summary_blocked
- Dispatch packets ready for external action: 3/3
- P07658 coordinate routes now: 0
- P07658 acceptance failures: 7
- Train/cal intake slots required: 186
- Train/cal intake slots ready to score now: 0
- Guardrail violations: 0
- Blockers: ['p07658_prediction_dispatch_blocked_no_coordinate', 'high_cofactor_acquisition_dispatch_slots_unfilled', 'same_family_structural_acquisition_dispatch_slots_unfilled', 'fixed_threshold_audit_not_ready_to_rerun']

## Dispatch Rows

| experiment | status | ready | blocker |
| --- | --- | --- | --- |
| p07658_full_length_prediction_acceptance | fold_augmented_p07658_prediction_dispatch_packet_ready_blocked_no_coordinate | True | no provider/local runtime returned a coordinate and the acceptance preflight still fails |
| high_cofactor_train_cal_oos_acquisition | fold_augmented_confounded_proxy_high_cofactor_acquisition_dispatch_packet_ready_unfilled | True | 16 intake slots are unfilled |
| same_family_structural_train_cal_oos_acquisition | fold_augmented_confounded_proxy_same_family_structural_acquisition_dispatch_packet_ready_unfilled | True | 170 intake slots are unfilled |

## Decision

- All dispatch packets ready for external action: True
- Current evidence can clear Lever 3 done-bar now: False
- Fixed-threshold audit ready to rerun now: False
- Next gate: First run/fill the P07658 coordinate/provenance dispatch; then fill the 16 high-cofactor slots; then fill the 170 same-family structural slots. Do not rerun the operating point until accepted dispatch evidence has real scores.

## Interpretation

- Lever 3 is dispatch-ready but still blocked: P07658 has no coordinate, 16 high-cofactor slots are unfilled, and 170 same-family structural slots are unfilled.
- Treat this as the current single Lever 3 handoff: fill the dispatch evidence, then score only accepted train/cal rows at the unchanged fixed threshold.
