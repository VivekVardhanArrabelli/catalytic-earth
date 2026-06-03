# Fold-Augmented Post-Rerun Confounded Deployment Closure Audit - current702

Run: 2026-06-03T07:08:43Z

Post-rerun Lever 3 synthesis for the predicted-structure-vs-atlas fold channel at the expanded OOS-calibrated operating point, focused on the six cofactor-confounded heldout OOS rows and the remaining P10746 fold-only deployment caveat.

## Status

- post_rerun_confounded_fold_channel_research_ready_p10746_caveat
- Fixed threshold: combined_mean_geometry_fold >= 0.44155
- Expanded full-channel rows: 75/76
- Confounded heldout OOS abstained: 5/6
- Remaining combined-score blockers: 1

## Confounded Rows

| row | nearest atlas | atlas fingerprint | TM |
| --- | --- | --- | ---: |
| m_csa:30 | m_csa:11 | metal_dependent_hydrolase | 0.4988 |
| m_csa:31 | m_csa:900 | ser_his_acid_hydrolase | 0.3809 |
| m_csa:80 | m_csa:973 | flavin_dehydrogenase_reductase | 0.5109 |
| m_csa:191 | m_csa:631 | ser_his_acid_hydrolase | 0.3863 |
| m_csa:267 | m_csa:800 | flavin_dehydrogenase_reductase | 0.7389 |
| m_csa:448 | m_csa:528 | metal_dependent_hydrolase | 0.5106 |

## Remaining Blocker

| row | blocker | next action |
| --- | --- | --- |
| m_csa:204 | fold_only_policy_caveat_not_combined_scored | Decide whether the P10746 fold-only caveat is acceptable for deployment closure, or provide an approved non-residue sidecar. |

## Interpretation

- After the fixed-threshold combined rerun, the confounded subset target remains met: 5/6 cofactor-confounded heldout OOS rows abstain while in-scope retention is preserved.
- The only remaining deployment blocker recorded here is m_csa:204/P10746, which lacks an approved non-residue sidecar and therefore remains fold-only.
