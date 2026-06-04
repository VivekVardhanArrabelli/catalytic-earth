# Fold-Augmented Confounded Proxy High-Cofactor Probe Contract - current702

Run: 2026-06-04T07:08:27Z

Train/cal-only high-cofactor mini-probe contract for the smallest Lever 3 new-evidence experiment identified by the deployment-validity blocker packet. It registers no rows and performs no scoring; it freezes the source-free membership and pass/fail rules for a future 16-row acquisition.

## Status

- fold_augmented_confounded_proxy_high_cofactor_probe_contract_ready_for_candidate_acquisition
- Fixed threshold: 0.44155
- Probe target new rows: 16
- Current high-cofactor proxy: 0/4 abstained
- Minimum new abstained rows for 80%: 16
- Candidate rows registered now: 0
- Structural proxy shortfall still separate: 170
- Blockers: ['candidate_rows_not_acquired_or_reviewed', 'candidate_rows_not_scored_at_fixed_threshold', 'structural_proxy_shortfall_remains_after_this_probe']

## Membership Contract

- Row must be non-heldout train/cal OOS calibration evidence, not heldout final-eval or family-panel breadth evidence.
- Row must have a deployment-valid predicted structure or an explicitly approved deployment-valid predicted-structure substitute.
- High-cofactor membership must be derived from source-free cofactor/locus evidence, not mechanism text, EC/Rhea IDs, labels, source IDs, or target names.
- Row must not already be part of the current high-cofactor retained-gap set or current scored train/cal OOS surface.
- Row must be scored through the predicted-structure-vs-train-atlas fold/geometry/cofactor channel before any abstention claim.
- Threshold 0.44155 must remain unchanged; this probe is pass/fail evidence, not threshold tuning.

## Excluded Rows

| class | rows |
| --- | --- |
| current high-cofactor retained gaps | m_csa:289, m_csa:298, m_csa:361, m_csa:368 |
| heldout/not-train-cal rows not allowed | m_csa:30, m_csa:31, m_csa:191, m_csa:448, m_csa:973 |

## Pass/Fail

- Pass condition: All 16 newly acquired train/cal high-cofactor proxy rows abstain at fixed threshold 0.44155, raising the high-cofactor proxy lower-bound readout from 0/4 to 16/20.
- Fail conditions: Any candidate row is heldout or lacks a deployment-valid predicted structure.; Any candidate uses mechanism text, EC/Rhea IDs, labels, source IDs, or target names as predictive membership evidence.; Fewer than 16 of 16 new rows abstain at fixed threshold 0.44155.

## Decision

- Candidate rows ready to score now: False
- Fixed-threshold audit ready to rerun now: False
- Deployable closure after probe alone: False
- Apply or change threshold now: False
- Next gate: Acquire exactly 16 new non-heldout train/cal OOS rows with source-free high-cofactor signatures and deployment-valid predicted structures, then score them at unchanged threshold 0.44155. All 16 must abstain to close only the high-cofactor 80% lower-bound target.
