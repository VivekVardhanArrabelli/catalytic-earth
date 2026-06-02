# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Heldout-Safe Application Preflight - current702

Run: 2026-06-02T12:11:29Z

Preflight for applying the frozen best-token residual threshold to a heldout-safe application surface. It checks whether the single event-residue-role token can be computed without M-CSA heldout row-specific mechanism text; it does not score heldout.

## Status

- p0_oos_augmented_best_token_heldout_safe_application_preflight_blocked
- Selected token: event_residue_role:proton_transfer|electrostatic_stabiliser
- Frozen residual threshold: 3.21469422
- Heldout rows in manifest: 140
- Heldout rows in best-token sidecar: 0
- Source-free predicted geometry ready rows: 3
- Blockers: heldout_application_rows_not_materialized, source_free_event_residue_role_surface_missing, active_site_role_graph_lacks_event_type_dimension, source_free_predicted_geometry_coverage_insufficient, reaction_center_template_is_template_dependent_ceiling_only

## Decision

- Heldout-safe application surface available: False
- Frozen residual threshold applied once: False
- Heldout read once performed: False
- Next gate: Do not read heldout. Use the remaining retained calibration OOS rows from the best-token error analysis for a follow-up token ablation.

## Interpretation

- A heldout-safe application surface for the selected event-residue-role token is not mechanically available yet.
- Build a source-free event/residue-role application surface before any heldout application, or continue calibration-only feature ablation on the retained OOS misses.
