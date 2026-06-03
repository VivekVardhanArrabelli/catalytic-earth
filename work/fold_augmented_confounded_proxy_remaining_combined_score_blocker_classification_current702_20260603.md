# Fold-Augmented Confounded Proxy Remaining Combined-Score Blocker Classification - current702

Run: 2026-06-03T20:16:45Z

Review-only classification of the six remaining combined-score blockers on the
current Lever 3 protein-only-extended train/cal OOS surface.

## Status

- fold_augmented_confounded_proxy_remaining_combined_score_blockers_classified_blocked
- Remaining combined-score blocker rows: 6
- Mechanically clearable now: 0
- Policy-decision rows: 1
- Predicted-structure unavailable rows: 4
- Approved geometry-feature missing rows: 1
- Fixed-threshold audit allowed now: False

## Rows

| row | accession | blocker class | next gate |
| --- | --- | --- | --- |
| m_csa:204 | P10746 | policy_decision_required | explicit P10746 accept/reject decision or approved non-residue sidecar |
| m_csa:416 | P07071 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate source |
| m_csa:562 | P07658 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate source |
| m_csa:586 | P00806 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate source |
| m_csa:604 | Q43088 | approved_geometry_feature_missing | approved source-free geometry/locator evidence |
| m_csa:637 | P04531 | predicted_structure_unavailable | approved deployment-valid predicted-structure coordinate source |

## Decision

- Do not rerun the fixed-threshold confounded proxy audit from the partial
  204/210 surface.
- Continue Lever 2 event-axis linker materialization or obtain explicit
  P10746/coordinate decisions before rescoring these rows.

## Guardrails

- No labels, registries, ontologies, imports, production thresholds, model
  weights, heldout reads, or threshold tuning were changed.
