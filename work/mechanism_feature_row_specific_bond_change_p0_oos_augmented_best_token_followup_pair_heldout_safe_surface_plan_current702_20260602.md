# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Heldout-Safe Surface Plan - current702

Run: 2026-06-02T14:18:10Z

Review-only materialization plan for a heldout-safe application surface for the best-token follow-up pair. It records the source-free extractors needed before applying the frozen residual threshold to heldout exactly once.

## Status

- p0_oos_augmented_best_token_followup_pair_heldout_safe_surface_plan_ready_surface_blocked
- Heldout rows: 140
- Source-free predicted geometry ready rows: 3
- Source-free application residue-count rows: 0
- Source-free locator priority-1 candidates: 126
- Source-free locator priority-1 rows without anchor: 24
- Source-free locator priority-1 rows with coordinate-anchor candidate: 102
- Source-free locator auto-create allowed rows: 0
- Required residue locators per approved sidecar: 2
- Pair calibration OOS abstain recall: 0.857143
- Pair retained OOS rows: 4
- Blockers: source_free_current702_heldout_locator_surface_missing, source_free_event_residue_role_extractor_missing, m_csa_curated_heldout_active_site_roles_not_deployment_input, source_free_predicted_geometry_heldout_coverage_incomplete

## Required Extractors

| token | extractor | status |
| --- | --- | --- |
| event_residue_role:proton_transfer|electrostatic_stabiliser | source_free_event_residue_role_linker | missing_source_free_event_axis |
| residue_code_count:his=3 | source_free_active_site_residue_identity_counter | blocked_source_free_coordinate_anchor_review_pending |

## Decision

- Heldout-safe pair application surface ready: False
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: Build a source-free current702 heldout active-site locator and event/residue-role extraction sidecar for the selected pair; rerun this plan and the preflight, then apply the frozen residual threshold exactly once without retuning.

## Interpretation

- The calibrated pair surface is ready on train/cal, but heldout application remains blocked until the selected pair can be computed from source-free active-site/event evidence.
- Use the source-free locator action queue and input audit to materialize approved current702 heldout locator sidecars only after source-free anchor evidence is present; then add a source-free event/residue-role linker before any heldout threshold application.
