# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Partial-Surface Policy Gate - current702

Run: 2026-06-04T00:14:12Z

Explicit policy gate for the post-event-axis partial source-free heldout surface. Rows with approved source-free pair features are marked score-eligible only if a later full read is authorized; rows without approved source-free locators are deterministic deployment abstentions with no residual score. This gate defines the policy but does not apply the frozen residual threshold or read heldout outcomes.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_partial_surface_policy_gate_ready_no_threshold_read
- Heldout rows: 140
- Source-free pair feature rows: 53
- Source-free event/residue-role positive rows: 14
- Missing-locator policy abstention rows: 87
- Blockers: source_free_current702_heldout_locator_coverage_incomplete, partial_surface_policy_not_accepted_for_frozen_threshold_read

## Policy

- Feature-complete row action: eligible_for_residual_score_if_full_read_authorized
- Missing-locator row action: abstain_without_residual_score
- Partial-surface metric read allowed: False

## Decision

- Heldout-safe partial-surface policy ready: True
- Partial policy accepted for frozen threshold read: False
- Ready to apply frozen residual threshold once: False
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: This partial policy is explicit and heldout-safe, but it is not an authorization to read the frozen residual threshold. Either materialize approved source-free locators for the remaining heldout rows, or write a separate operating contract that accepts deterministic missing-locator abstention as the deployable readout before any heldout read.

## Interpretation

- 53 current702 heldout rows have approved source-free pair features and 87 rows are policy abstentions because approved source-free locator sidecars are still missing. The partial policy avoids feature imputation and threshold scoring on missing rows.
- Rerun pre-threshold readiness with this policy gate present. The frozen residual threshold should remain blocked until complete locator coverage exists or a separate deterministic missing-locator abstention operating contract is explicitly accepted.
