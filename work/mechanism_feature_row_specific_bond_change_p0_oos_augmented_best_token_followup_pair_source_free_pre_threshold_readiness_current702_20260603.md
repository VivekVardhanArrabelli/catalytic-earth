# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Pre-Threshold Readiness - current702

Run: 2026-06-03T11:11:09Z

Composed pre-threshold readiness gate for applying the frozen Lever 2 row-specific residual contract to heldout exactly once. It requires a calibration-only contract, approved source-free heldout locator sidecars, materialized source-free event-axis linkers, and a complete heldout-safe pair application surface. It does not apply the threshold or read heldout outcomes.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_pre_threshold_readiness_blocked
- Pair operating-point contract ready: True
- Approved source-free locator surface ready: False
- Source-free event-axis linkers materialized: False
- Heldout-safe pair application surface ready: False
- Locator preflight rows: 55
- Locator approval records: 0
- Locator pending reviewer decisions: 55
- Locator review warning rows: 6
- Locator sidecars written: 0
- Source-free residue-count feature rows: 0
- Source-free event/residue-role feature rows: 0
- Event-axis materialized linker rows: 0
- Blockers: approved_source_free_locator_surface_missing, source_free_event_axis_linkers_missing, heldout_safe_pair_application_surface_missing, explicit_locator_rewrite_approval_decisions_missing, approved_locator_rewrite_rows_missing, approved_locator_sidecar_write_flag_not_enabled, approved_locator_sidecars_not_materialized, source_free_current702_heldout_locator_rows_missing, source_free_current702_heldout_locator_coverage_incomplete, source_free_event_residue_role_extractor_missing, source_free_proton_transfer_event_axis_missing, approved_source_free_locator_surface_still_required, source_free_event_axis_linker_rows_missing, source_free_event_axis_linkers_not_materialized

## Frozen Contract

- Preferred contract: residual_distance_threshold
- Residual distance threshold: 3.21469422
- Calibration OOS abstain recall: 0.857143

## Decision

- Ready to apply frozen residual threshold once: False
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: Supply explicit locator rewrite approvals, materialize the approved heldout locator sidecars, validate source-free event axis linker rows through the materialization gate, rerun the source-free application surface, then rerun this readiness gate before applying the frozen residual threshold exactly once.

## Interpretation

- The frozen residual contract is calibrated, but the heldout application surface is not ready because approved source-free locator sidecars and validated source-free event-axis linkers are still absent.
- Consume explicit locator approvals first; preflight rows alone must not become heldout features, and the residual threshold must remain unapplied until this readiness gate passes.
