# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Pre-Threshold Readiness - current702

Run: 2026-06-04T01:10:57Z

Composed pre-threshold readiness gate for applying the frozen Lever 2 row-specific residual contract to heldout exactly once. It requires a calibration-only contract, approved source-free heldout locator sidecars, materialized source-free event-axis linkers, and a complete heldout-safe pair application surface. It does not apply the threshold or read heldout outcomes.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_pre_threshold_readiness_ready
- Pair operating-point contract ready: True
- Approved source-free locator surface ready: True
- Source-free event-axis linkers materialized: True
- Source-free event-axis signoff finalization ready: True
- Heldout-safe pair application surface ready: False
- Heldout-safe partial-surface policy ready: True
- Partial-surface policy accepted for frozen threshold read: True
- Partial-surface policy effective application surface ready: True
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
- Blockers: none

## Frozen Contract

- Preferred contract: residual_distance_threshold
- Residual distance threshold: 3.21469422
- Calibration OOS abstain recall: 0.857143

## Decision

- Ready to apply frozen residual threshold once: True
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: Apply the frozen residual threshold exactly once to the 53 feature-complete heldout rows and carry the 87 accepted missing-locator rows as deterministic abstentions.

## Interpretation

- The frozen residual contract is calibrated, source-free event-axis linkers are materialized, and the accepted partial operating contract covers missing locators as deterministic abstentions without residual scores. The one-time frozen heldout read is now mechanically ready.
- Apply the frozen residual threshold exactly once on the feature-complete rows and carry accepted missing-locator rows as deterministic abstentions; do not refit, tune, or score missing rows.
