# Fold-Augmented Confounded Proxy P10746 Decision Impact - current702

Run: 2026-06-04T08:10:50Z

Review-only Lever 3 impact packet after applying the P10746 fold-only caveat decision. It removes only the explicit P10746 policy blocker from the current deployment-validity blocker list when accepted; it does not rerun the fixed-threshold audit, change threshold 0.44155, score rows, close deployment, or use heldout rows for calibration.

## Status

- fold_augmented_confounded_proxy_p10746_decision_impact_blocked_remaining_evidence
- P10746 policy blockers resolved: 1/1
- Remaining full-channel blockers after P10746: 5
- Remaining predicted-structure-unavailable rows: 4
- Remaining approved-geometry-feature-missing rows: 1
- High-cofactor new abstained rows needed: 16
- Same-family structural new abstained rows needed: 170
- Blockers: ['current_train_cal_proxy_surface_cannot_close_confounded_safe_calibration', 'high_cofactor_proxy_needs_new_abstained_train_cal_rows', 'same_family_structural_proxy_needs_new_abstained_train_cal_rows', 'protein_only_extended_surface_still_partial', 'remaining_non_p10746_full_channel_blockers']

## Decision

- P10746 fold-only caveat accepted: True
- Fixed-threshold audit ready to rerun now: False
- Deployment closure valid now: False
- Next gate: P10746 no longer needs a fresh policy decision, but the current Lever 3 deployment-validity gate remains blocked by five non-P10746 full-channel rows plus the 16-row high-cofactor and 170-row same-family structural train/cal proxy acquisition shortfalls.

## Remaining Full-Channel Blockers

| row | accession | blocker class | missing evidence | smallest next experiment |
| --- | --- | --- | --- | --- |
| m_csa:416 | P07071 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate source | fetch or approve one source-free predicted coordinate for this accession, then score only that row |
| m_csa:562 | P07658 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate source | fetch or approve one source-free predicted coordinate for this accession, then score only that row |
| m_csa:586 | P00806 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate source | fetch or approve one source-free predicted coordinate for this accession, then score only that row |
| m_csa:604 | Q43088 | approved_geometry_feature_missing | approved source-free geometry/locator evidence | materialize the approved source-free geometry feature or locator sidecar, then rescore only that row |
| m_csa:637 | P04531 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate source | fetch or approve one source-free predicted coordinate for this accession, then score only that row |

## Interpretation

- The existing reviewed P10746 fold-only decision can clear the policy-decision blocker, but it does not create a combined channel score and does not improve confounded-proxy abstain recall.
- Focus next on the five remaining full-channel blocker rows or the frozen 16-row high-cofactor train/cal acquisition contract; do not rerun thresholds from this P10746 impact alone.
