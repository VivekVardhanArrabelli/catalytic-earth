# Fold-Augmented Confounded Proxy Same-Family Structural Acquisition Dispatch Packet - current702

Run: 2026-06-04T16:40:04Z

Dispatch-ready intake packet for the 170-row same-family structural train/cal OOS acquisition experiment. It creates unfilled slots and acceptance criteria only; it does not source rows, register candidates, score candidates, tune thresholds, or read heldout.

## Status

- fold_augmented_confounded_proxy_same_family_structural_acquisition_dispatch_packet_ready_unfilled
- Intake slots required: 170
- Intake slots filled now: 0
- Intake slots ready to score now: 0
- Background rows not countable: 80
- Blockers: ['same_family_structural_acquisition_slots_unfilled', 'candidate_rows_not_registered_or_scored', 'fixed_threshold_audit_not_ready_to_rerun']

## Acceptance Checks

- row is non-heldout train/cal OOS under the frozen split
- row is not already in the scored train/cal OOS surface
- source-free same-family structural membership is satisfied without relaxing the axis
- deployment-valid predicted coordinate and provenance are present
- experimental PDB metadata is not used as a deployment input
- row is scored only after intake acceptance passes
- fixed threshold remains 0.44155

## Intake Slot Summary

| first slot | last slot | total | filled now | ready to score now |
| --- | --- | ---: | ---: | ---: |
| same_family_structural_train_cal_oos_slot_001 | same_family_structural_train_cal_oos_slot_170 | 170 | 0 | 0 |

## Decision

- Acquisition dispatch ready for row intake: True
- Candidate rows ready to score now: False
- Fixed-threshold audit ready to rerun now: False
- Next gate: Do not rerun the fixed-threshold audit until filled slots pass intake checks and have real predicted-structure-vs-atlas scores.

## Interpretation

- The same-family structural acquisition experiment is dispatch-ready as 170 unfilled intake slots, but no new rows are registered or scoreable now.
- Fill the intake slots with source-free same-family structural train/cal OOS evidence; keep background rows non-countable.
