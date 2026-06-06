# Fold-Augmented Confounded Proxy Deployment-Validity Blocker Packet - current702

Run: 2026-06-04T07:08:19Z

Lever 3 blocker packet for the predicted-structure-vs-atlas novelty/abstention channel after the current train/cal proxy axes and protein-only fold-topology tranche failed to close the confounded-safe calibration gap.

## Status

- fold_augmented_confounded_proxy_deployment_validity_blocker_packet_blocked
- Fixed threshold: 0.44155
- Retained proxy-gap rows: 48
- Protein-only tranche abstained/retained at fixed threshold: 7/1
- Protein-only extended full-channel rows: 204/210
- Remaining combined-score blockers: 6
- Blockers: ['current_train_cal_proxy_surface_cannot_close_confounded_safe_calibration', 'high_cofactor_proxy_needs_new_abstained_train_cal_rows', 'same_family_structural_proxy_needs_new_abstained_train_cal_rows', 'threshold_stress_retention_cost_blocks_threshold_raise', 'protein_only_extended_surface_still_partial', 'remaining_combined_score_blockers_not_mechanically_clearable_now']

## Train/Cal Proxy Behavior

| proxy | rows | abstained | recall | min new abstained for 80% |
| --- | ---: | ---: | ---: | ---: |
| high_cofactor_signature_proxy | 4 | 0 | 0.0 | 16 |
| same_family_structural_proxy | 55 | 10 | 0.1818 | 170 |

## Remaining Full-Channel Blockers

| row | accession | blocker class | missing evidence | smallest row experiment |
| --- | --- | --- | --- | --- |
| m_csa:204 | P10746 | policy_decision_required | explicit deployment caveat decision or approved non-residue sidecar | record an explicit P10746 accept/reject decision with hash-valid review |
| m_csa:416 | P07071 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate source | fetch or approve one source-free predicted coordinate for this accession, then score only that row |
| m_csa:562 | P07658 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate source | fetch or approve one source-free predicted coordinate for this accession, then score only that row |
| m_csa:586 | P00806 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate source | fetch or approve one source-free predicted coordinate for this accession, then score only that row |
| m_csa:604 | Q43088 | approved_geometry_feature_missing | approved source-free geometry/locator evidence | materialize the approved source-free geometry feature or locator sidecar, then rescore only that row |
| m_csa:637 | P04531 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate source | fetch or approve one source-free predicted coordinate for this accession, then score only that row |

## Smallest Next Experiments

| experiment | sufficient for closure | success criterion |
| --- | --- | --- |
| complete_six_partial_surface_blockers_no_threshold_rerun | False | All six rows receive deployment-valid full-channel scores; fixed-threshold proxy audit rerun remains separate and threshold 0.44155 stays unchanged. |
| sixteen_row_high_cofactor_train_cal_oos_probe | False | Score 16 new train/cal high-cofactor proxy rows at unchanged threshold 0.44155; all 16 must abstain to close only the high-cofactor 80% lower-bound target. |
| one_hundred_seventy_row_same_family_structural_acquisition | False | Score enough new train/cal same-family structural proxy rows at fixed threshold 0.44155 to reach 80% abstain recall while preserving the train/cal in-scope retention floor. |

## Decision

- Deployment closure valid now: False
- Fixed-threshold audit ready to rerun now: False
- Apply or change threshold now: False
- Current evidence can solve confounded-safe calibration: False
- Next gate: Do not rerun the fixed-threshold audit or change threshold 0.44155. First clear the six full-channel blockers if the goal is surface completeness; the smallest new-evidence experiment is a 16-row train/cal high-cofactor OOS probe, while true structural-proxy closure requires a much larger train/cal same-family structural acquisition.

## Interpretation

- Current Lever 3 evidence is deployment-valid but not confounded-safe enough for closure.
- The channel retains the frozen heldout carry-through, but train/cal high-cofactor and same-family structural proxies remain far below the 80% abstention target and threshold stress shows a retention cost for forcing the target by threshold alone.
- Treat the six-row full-channel repair as an audit-unblocker, not calibration closure; then acquire new non-heldout train/cal proxy evidence, starting with the 16-row high-cofactor probe.
