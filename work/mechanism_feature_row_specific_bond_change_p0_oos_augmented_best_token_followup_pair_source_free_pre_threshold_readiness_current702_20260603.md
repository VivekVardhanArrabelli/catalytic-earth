# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Pre-Threshold Readiness - current702

Run: 2026-06-04T00:14:13Z

Composed pre-threshold readiness gate for applying the frozen Lever 2 row-specific residual contract to heldout exactly once. It requires a calibration-only contract, approved source-free heldout locator sidecars, materialized source-free event-axis linkers, and a complete heldout-safe pair application surface. It does not apply the threshold or read heldout outcomes.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_pre_threshold_readiness_blocked
- Pair operating-point contract ready: True
- Approved source-free locator surface ready: True
- Source-free event-axis linkers materialized: True
- Source-free event-axis signoff finalization ready: True
- Heldout-safe pair application surface ready: False
- Heldout-safe partial-surface policy ready: True
- Partial-surface policy accepted for frozen threshold read: False
- Locator preflight rows: 55
- Locator approval records: 55
- Locator pending reviewer decisions: 0
- Locator review warning rows: 6
- Locator sidecars written: 53
- Source-free residue-count feature rows: 53
- Source-free event/residue-role feature rows: 14
- Partial policy pair feature rows: 53
- Partial policy missing-locator abstain rows: 87
- Event-axis materialized linker rows: 14
- Event-axis signoff draft rows: 53
- Event-axis signoff rows with both roles: 14
- Event-axis pending reviewer signoff rows: 0
- Event-axis explicit approved rows: 14
- Event-axis gate-consumable signoff rows: 14
- Event-axis priority 1 signoff rows: 3
- Event-axis priority 2 signoff rows: 11
- Event-axis priority 3 signoff rows: 6
- Event-axis insufficient signoff rows: 33
- Blockers: heldout_safe_pair_application_surface_partial_policy_no_threshold_read, source_free_current702_heldout_locator_coverage_incomplete, partial_surface_policy_not_accepted_for_frozen_threshold_read

## Frozen Contract

- Preferred contract: residual_distance_threshold
- Residual distance threshold: 3.21469422
- Calibration OOS abstain recall: 0.857143

## Decision

- Ready to apply frozen residual threshold once: False
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: Do not read the frozen residual threshold on the partial surface. Either materialize approved source-free locators for the remaining heldout rows, or write a separate operating contract accepting deterministic missing-locator abstention as the deployable readout; then rerun this readiness gate.

## Interpretation

- The frozen residual contract is calibrated and source-free event-axis linkers are materialized. A partial-surface policy is present, but the frozen heldout read remains blocked because locator coverage is incomplete and the partial policy is not accepted as a threshold-read operating contract.
- Materialize the remaining approved source-free locator sidecars or explicitly accept deterministic missing-locator abstention in a separate operating contract; keep the frozen residual threshold unapplied until this readiness gate passes.
