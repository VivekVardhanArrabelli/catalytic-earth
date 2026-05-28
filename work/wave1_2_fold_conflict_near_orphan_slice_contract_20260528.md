# Wave 1.2 Fold-Conflict / Near-Orphan Slice Contract - 2026-05-28

Review-only contract compiled from existing Wave 1.1, full-TM, bronze/TM, and sequence-failure artifacts. No labels, registries, thresholds, scoring, imports, or model outputs were changed.

## Answer

Learned representations add value where Foldseek is weak only in a limited, non-decision-grade way: `limited_not_decision_grade`. Geometry remains the stronger rescue signal in both wrong-transfer and near-orphan cells.

## Row-Use Summary

- `clean_near_orphan_anchor`: 7
- `coordinate_or_tm_uncertainty_hold`: 5
- `fold_conflict_candidate_needs_review`: 2
- `fold_conflict_reference_anchor`: 3
- `mixed_high_tm_review_candidate`: 4
- `near_orphan_candidate_from_retained_hits`: 37
- `not_primary_due_same_neighbor`: 17
- `oos_fold_conflict_hard_negative_candidate`: 11
- `oos_router_control`: 9
- `quarantine_do_not_anchor_metric`: 7

Clean anchor IDs:
- near-orphan: m_csa:97, m_csa:211, m_csa:250, m_csa:517, m_csa:686, m_csa:916, m_csa:990
- fold-conflict reference: m_csa:217, m_csa:428, m_csa:477
- OOS router controls: m_csa:10, m_csa:30, m_csa:31, m_csa:116, m_csa:191, m_csa:369, m_csa:440, m_csa:634, m_csa:651
- quarantined before claims: m_csa:403, m_csa:497, m_csa:714, m_csa:723, m_csa:735, m_csa:750, m_csa:994

## Policy

This artifact can choose rows for review-only diagnostics and canaries. It cannot support a new benchmark score, label import, threshold change, or model-scaling decision by itself.

