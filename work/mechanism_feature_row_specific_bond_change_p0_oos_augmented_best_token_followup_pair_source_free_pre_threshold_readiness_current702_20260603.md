# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Pre-Threshold Readiness - current702

Run: 2026-06-03T21:39:26Z

Composed pre-threshold readiness gate for applying the frozen Lever 2 row-specific residual contract to heldout exactly once. It requires a calibration-only contract, approved source-free heldout locator sidecars, materialized source-free event-axis linkers, and a complete heldout-safe pair application surface. It does not apply the threshold or read heldout outcomes.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_pre_threshold_readiness_blocked
- Pair operating-point contract ready: True
- Approved source-free locator surface ready: True
- Source-free event-axis linkers materialized: False
- Source-free event-axis signoff finalization ready: False
- Heldout-safe pair application surface ready: False
- Locator preflight rows: 55
- Locator approval records: 55
- Locator pending reviewer decisions: 0
- Locator review warning rows: 6
- Locator sidecars written: 53
- Source-free residue-count feature rows: 53
- Source-free event/residue-role feature rows: 0
- Event-axis materialized linker rows: 0
- Event-axis signoff draft rows: 53
- Event-axis signoff rows with both roles: 14
- Event-axis pending reviewer signoff rows: 53
- Event-axis explicit approved rows: 0
- Event-axis gate-consumable signoff rows: 0
- Event-axis priority 1 signoff rows: 3
- Event-axis priority 2 signoff rows: 11
- Event-axis priority 3 signoff rows: 6
- Event-axis insufficient signoff rows: 33
- Blockers: source_free_event_axis_linkers_missing, heldout_safe_pair_application_surface_missing, source_free_current702_heldout_locator_coverage_incomplete, source_free_event_residue_role_extractor_missing, source_free_proton_transfer_event_axis_missing, source_free_event_axis_linker_rows_missing, source_free_event_axis_linkers_not_materialized, event_axis_signoff_decisions_pending, explicit_event_axis_linker_approvals_missing

## Frozen Contract

- Preferred contract: residual_distance_threshold
- Residual distance threshold: 3.21469422
- Calibration OOS abstain recall: 0.857143

## Decision

- Ready to apply frozen residual threshold once: False
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: Keep the approved locator surface fixed, validate source-free event-axis linker rows or an accepted fallback, rerun the source-free application surface, then rerun this readiness gate before applying the frozen residual threshold exactly once.

## Interpretation

- The frozen residual contract is calibrated, but the heldout application surface is not ready because source-free event-axis linkers and complete heldout-safe feature coverage are still absent.
- Keep the materialized approved locators, supply source-free event-axis linker rows or an accepted fallback, and leave the residual threshold unapplied until this readiness gate passes.
