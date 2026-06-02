# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Event-Linker Blocker Audit - current702

Run: 2026-06-02T20:09:34Z

Leakage-safe blocker audit for the source-free event/residue-role linker needed by the calibrated row-specific feature pair. It compares the frozen pair contract with the source-free-computable residue-code fallback, rejects curated heldout role graphs as deployment inputs, and does not apply the heldout threshold.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_event_linker_blocker_audit_ready_blocked
- Heldout rows: 140
- Current702 heldout source-free locator sidecars: 0
- Source-free event/residue-role feature rows: 0
- M-CSA curated heldout role-graph ok rows: 132
- Blockers: source_free_current702_heldout_locator_surface_missing, source_free_proton_transfer_event_axis_missing, source_free_event_residue_role_linker_missing, m_csa_curated_active_site_role_graph_forbidden_as_deployment_input, source_free_residue_code_only_fallback_underperforms_pair_contract

## Contract Comparison

- Pair residual OOS abstain recall: 0.857143
- Residue-code-only OOS abstain recall: 0.642857
- Residue-code-only recall delta vs pair: 0.214286
- Pair residual AUC: 0.875
- Residue-code-only AUC: 0.758929

## Decision

- Source-free event linker ready: False
- Source-free residue-code-only fallback sufficient: False
- Curated active-site role graph allowed for deployment: False
- Heldout-safe pair application surface ready: False
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: Do not substitute the M-CSA active-site role graph for heldout deployment. Either build an approved source-free proton-transfer event-axis linker for the pair token, or explicitly choose the lower-recall residue-code-only fallback as a separate calibration contract before any heldout read.

## Interpretation

- The calibrated pair remains deployment-blocked because the event/residue-role token requires a source-free proton-transfer event axis. The source-free His-count fallback is measurable on train/cal but loses calibration OOS abstention relative to the pair, and the curated heldout active-site role graph is an explicitly forbidden deployment shortcut.
- Build the source-free event-axis linker contract for proton_transfer to electrostatic_stabiliser, then rerun the source-free application surface and heldout-safe surface plan.
