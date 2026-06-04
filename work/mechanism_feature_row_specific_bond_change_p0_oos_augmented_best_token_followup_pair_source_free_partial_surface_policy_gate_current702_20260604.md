# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Partial-Surface Policy Gate - current702

Run: 2026-06-04T01:10:05Z

Explicit policy gate for the post-event-axis partial source-free heldout surface. Rows with approved source-free pair features are marked score-eligible only if a later full read is authorized; rows without approved source-free locators are deterministic deployment abstentions with no residual score. This gate defines the policy but does not apply the frozen residual threshold or read heldout outcomes.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_partial_surface_policy_gate_ready_no_threshold_read
- Heldout rows: 140
- Source-free pair feature rows: 53
- Source-free event/residue-role positive rows: 14
- Missing-locator policy abstention rows: 87
- Blockers: none

## Policy

- Feature-complete row action: eligible_for_residual_score_if_full_read_authorized
- Missing-locator row action: abstain_without_residual_score
- Partial-surface metric read allowed: True

## Decision

- Heldout-safe partial-surface policy ready: True
- Partial policy accepted for frozen threshold read: True
- Ready to apply frozen residual threshold once: False
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: Rerun pre-threshold readiness with this accepted deterministic missing-locator abstention operating contract; do not read heldout outcomes until that readiness gate passes.

## Interpretation

- 53 current702 heldout rows have approved source-free pair features and 87 rows are policy abstentions because approved source-free locator sidecars are still missing. The partial policy avoids feature imputation and threshold scoring on missing rows. The deterministic missing-locator abstention operating contract is explicitly accepted for the deployable readout.
- Rerun pre-threshold readiness with the accepted partial operating contract; keep the frozen residual threshold unapplied until readiness passes.
