# Fold-Augmented Confounded Proxy High-Cofactor Acquisition Dispatch Packet - current702

Run: 2026-06-04T13:35:32Z

Dispatch-ready intake packet for the 16-row high-cofactor train/cal OOS acquisition experiment. It creates unfilled slots and acceptance criteria only; it does not source rows, register candidates, score candidates, tune thresholds, or read heldout.

## Status

- fold_augmented_confounded_proxy_high_cofactor_acquisition_dispatch_packet_ready_unfilled
- Intake slots required: 16
- Intake slots filled now: 0
- Intake slots ready to score now: 0
- Near-miss rows not countable: 16
- Blockers: ['high_cofactor_acquisition_slots_unfilled', 'candidate_rows_not_registered_or_scored', 'fixed_threshold_audit_not_ready_to_rerun']

## Acceptance Checks

- row is non-heldout train/cal OOS under the frozen split
- row is not already in the scored train/cal OOS surface
- source-free high-cofactor membership is satisfied without relaxing the axis
- deployment-valid predicted coordinate and provenance are present
- experimental PDB metadata is not used as a deployment input
- row is scored only after intake acceptance passes
- fixed threshold remains 0.44155

## Intake Slots

| slot | status | score now | count now |
| --- | --- | --- | --- |
| high_cofactor_train_cal_oos_slot_01 | unfilled | False | False |
| high_cofactor_train_cal_oos_slot_02 | unfilled | False | False |
| high_cofactor_train_cal_oos_slot_03 | unfilled | False | False |
| high_cofactor_train_cal_oos_slot_04 | unfilled | False | False |
| high_cofactor_train_cal_oos_slot_05 | unfilled | False | False |
| high_cofactor_train_cal_oos_slot_06 | unfilled | False | False |
| high_cofactor_train_cal_oos_slot_07 | unfilled | False | False |
| high_cofactor_train_cal_oos_slot_08 | unfilled | False | False |
| high_cofactor_train_cal_oos_slot_09 | unfilled | False | False |
| high_cofactor_train_cal_oos_slot_10 | unfilled | False | False |
| high_cofactor_train_cal_oos_slot_11 | unfilled | False | False |
| high_cofactor_train_cal_oos_slot_12 | unfilled | False | False |
| high_cofactor_train_cal_oos_slot_13 | unfilled | False | False |
| high_cofactor_train_cal_oos_slot_14 | unfilled | False | False |
| high_cofactor_train_cal_oos_slot_15 | unfilled | False | False |
| high_cofactor_train_cal_oos_slot_16 | unfilled | False | False |

## Decision

- Acquisition dispatch ready for row intake: True
- Candidate rows ready to score now: False
- Fixed-threshold audit ready to rerun now: False
- Next gate: Do not rerun the fixed-threshold audit until all filled slots pass intake checks and have real predicted-structure-vs-atlas scores.

## Interpretation

- The high-cofactor acquisition experiment is dispatch-ready as 16 unfilled intake slots, but no new rows are registered or scoreable now.
- Fill the intake slots with source-free high-cofactor train/cal OOS evidence; keep near misses non-countable.
