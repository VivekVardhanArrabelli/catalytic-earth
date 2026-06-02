# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Residue-Count Fallback Contract - current702

Run: 2026-06-02T20:15:42Z

Calibration-only fallback contract for the source-free-compatible residue-count token in the row-specific feature surface. It formalizes the lower-recall His-count-only option without requiring the event/residue-role linker and without applying the heldout threshold.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_residue_count_fallback_contract_ready_calibration_only_surface_blocked
- Heldout rows: 140
- Current702 heldout source-free locator sidecars: 0
- Source-free residue-count feature rows: 0
- Locator preflight-passed pending explicit approval: 55
- Locator preflight rows with warnings: 6
- Fallback token scored: 1
- Blockers: source_free_current702_heldout_locator_surface_missing, source_free_residue_count_surface_missing, source_free_locator_rewrite_explicit_approval_pending, source_free_residue_count_fallback_lower_recall_requires_explicit_acceptance

## Calibration Contract

- Feature token: residue_code_count:his=3
- Residual distance threshold: 3.21469422
- Calibration OOS abstain recall: 0.642857
- Calibration AUC: 0.758929
- Pair calibration OOS abstain recall: 0.857143
- Recall delta vs pair: 0.214286

## Decision

- Fallback calibrated train/cal only: True
- Fallback avoids event axis: True
- Fallback accepted as deployable replacement: False
- Explicit acceptance required before heldout read: True
- Heldout-safe fallback application surface ready: False
- Apply frozen fallback threshold now: False
- Heldout read once performed: False
- Next gate: Use this fallback only if the lower calibration OOS abstention is explicitly accepted. Otherwise build the source-free event linker for the stronger pair. In either case, materialize approved current702 heldout locator sidecars before any heldout threshold application.

## Interpretation

- The His-count-only fallback is calibration-scored and avoids the missing event axis, but it is a lower-recall alternative to the calibrated pair and still needs approved current702 heldout locators before a heldout-safe application surface exists.
- Either explicitly accept this lower-recall fallback contract or continue building the source-free event linker for the stronger pair; do not read heldout until the selected surface is source-free and complete.
