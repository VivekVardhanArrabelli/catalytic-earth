# Fold-Augmented Confounded Proxy Same-Family Structural Acquisition Contract - current702

Run: 2026-06-04T07:08:27Z

Train/cal-only same-family structural acquisition contract for the large Lever 3 confounded-proxy scale blocker. It registers no rows, scores nothing, and freezes the source-free membership and pass/fail rules for a future acquisition surface.

## Status

- fold_augmented_confounded_proxy_same_family_structural_acquisition_contract_ready_for_candidate_acquisition
- Fixed threshold: 0.44155
- Current same-family structural proxy: 10/55 abstained
- Loose same-family current surface if included: 25/76 abstained
- Minimum new abstained rows for 80%: 170
- Candidate rows registered now: 0
- High-cofactor probe still separate: 16
- Blockers: ['candidate_rows_not_acquired_or_reviewed', 'candidate_rows_not_scored_at_fixed_threshold', 'scale_experiment_large_170_row_lower_bound', 'high_cofactor_probe_still_separate']

## Membership Contract

- Row must be non-heldout train/cal OOS calibration evidence.
- Row must have a deployment-valid predicted structure or explicitly approved deployment-valid predicted-structure substitute.
- Same-family structural membership must be derived from source-free fold/geometry or cofactor-locus evidence, not mechanism text, EC/Rhea IDs, labels, source IDs, or target names.
- Row must not already be part of the current strict same-family structural proxy, loose same-family current-surface diagnostics, or retained-gap evidence request set.
- Row must be scored through the predicted-structure-vs-train-atlas fold/geometry/cofactor channel before any abstention claim.
- Threshold 0.44155 must remain unchanged; this is scale evidence, not threshold tuning.

## Pass/Fail

- Pass condition: Enough newly acquired train/cal same-family structural proxy rows abstain at fixed threshold 0.44155 to raise the structural proxy from 10/55 to at least 80% abstain recall; under the current all-new-rows-abstain lower bound this requires 170 new abstained rows.
- Fail conditions: Any candidate row is heldout or lacks deployment-valid predicted structure evidence.; Any candidate uses mechanism text, EC/Rhea IDs, labels, source IDs, or target names as predictive membership evidence.; The scored surface cannot reach 80% same-family structural abstain recall while preserving the train/cal in-scope retention floor.

## Decision

- Candidate rows ready to score now: False
- Fixed-threshold audit ready to rerun now: False
- Deployable closure after contract alone: False
- Apply or change threshold now: False
- Next gate: Acquire a large new non-heldout train/cal same-family structural OOS surface with deployment-valid predicted structures and source-free membership evidence. Under the current lower bound, 170 additional rows must abstain at unchanged threshold 0.44155 to reach 80% structural-proxy abstain recall.
