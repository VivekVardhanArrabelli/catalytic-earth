# Predicted-Structure Fold Confounded Operating-Point Readiness - current702

Run: 2026-06-02T17:10:46Z

Read-only readiness audit for the Lever 3 predicted-structure-vs-atlas fold channel at the existing operating point. It composes the contract audit, confounded closure, fold-only no-go decision, OOS-calibrated threshold contract, deployment-input contract, and coordinate provenance audit without selecting thresholds or rerunning Foldseek/TM.

## Status

- predicted_structure_fold_confounded_operating_point_research_ready_deployment_blocked
- Research confounded operating point ready: True
- Deployment closed: False
- Deployment input contract passed: True
- Deployment input critical violations: 0
- Confounded OOS abstained: 5/6
- Remaining production blocker rows: 5
- Fold-only rows abstained at 90% threshold: 0/4
- Unique coordinate files missing: 0
- Remaining-blocker coordinate reprobe rows cleared: 0
- Source-sidecar preflight candidates: 3
- Critical violations: 6

## Deployment Closure Gate

| gate | status | key value |
| --- | --- | --- |
| predicted_structure_vs_atlas_input_contract | passed | 0 |
| fixed_oos_calibrated_operating_threshold | fixed_no_change | 0.44155 |
| confounded_oos_operating_point | passed | None |
| in_scope_retention_at_operating_point | passed | None |
| production_blocker_rows | blocked | 5 |
| persistent_afdb_coordinate_bundle | passed | 0 |
| fold_only_escape_hatch | rejected | None |

## Remaining Blocker Rows

| row | blocker | coordinate available | source-sidecar preflight | source features | fold-only evidence |
| --- | --- | --- | --- | ---: | --- |
| m_csa:78 | alphafold_db_coordinate_unavailable | False | blocked_predicted_coordinate_policy_required | 6 | False |
| m_csa:204 | experimental_geometry_not_ok:None | True | blocked_non_residue_interaction_policy_required | 0 | True |
| m_csa:531 | experimental_geometry_not_ok:insufficient_resolved_residues | True | source_feature_sidecar_candidate_ready_for_manual_review | 3 | True |
| uniprot:P78549 | not_m_csa_entry | True | source_feature_sidecar_candidate_ready_for_manual_review | 6 | True |
| uniprot:Q3LXA3 | not_m_csa_entry | True | source_feature_sidecar_candidate_ready_for_manual_review | 9 | True |

## Decision

- Keep the fixed operating point unchanged. Clear the remaining production blocker rows before claiming deployment closure; do not use the fold-only escape hatch. The persistent AFDB coordinate bundle is now complete.

## Interpretation

- The predicted-structure-vs-atlas fold channel is research-ready for the confounded subset at the existing operating point with a predicted-only deployment input contract; deployment closure remains blocked by production blocker rows and a rejected fold-only escape hatch, while the persistent AFDB coordinate bundle is complete.
- Use this audit as the Lever 3 gate: clear source-backed active-site sidecars for coordinate-available blocker rows and resolve or exclude the coordinate-unavailable P23007 row by policy before any deployment-valid claim.
