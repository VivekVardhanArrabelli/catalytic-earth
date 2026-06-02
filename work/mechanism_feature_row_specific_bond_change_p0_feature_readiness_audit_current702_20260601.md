# Mechanism Feature Row-Specific Bond-Change P0 Feature-Readiness Audit - current702

Run: 2026-06-02T05:15:15Z

Review-only readiness audit for converting the P0 row-specific bond-change source-evidence sidecar into future mechanism-feature contract fields. It inventories proton-transfer, electron-transfer, and bond-change draft coverage while keeping every draft row out of training and threshold selection.

## Status

- p0_feature_readiness_audit_blocked_review_required
- Sidecar rows: 15
- Structurally ready draft rows: 15
- Approved consumable rows: 3
- Rows with bond-change events: 10
- Rows with proton-transfer events: 6
- Rows with electron-transfer events: 9
- Draft event type counts: {'bond_broken': 5, 'bond_formed': 6, 'bond_order_changed': 7, 'electron_transfer': 21, 'proton_transfer': 10}
- Blocker counts: {'low_confidence_event_review': 6, 'multi_event_mechanism_review': 5, 'review_status_not_approved': 12, 'reviewer_id_missing': 12}
- Feature-contract refresh allowed: False

## Row Readiness

| row | events | event types | structurally ready | approved consumable | blockers |
| --- | ---: | --- | --- | --- | --- |
| m_csa:5 | 1 | bond_broken | True | True |  |
| m_csa:6 | 5 | electron_transfer, proton_transfer | True | False | low_confidence_event_review, multi_event_mechanism_review, review_status_not_approved, reviewer_id_missing |
| m_csa:11 | 4 | bond_broken, bond_formed, electron_transfer | True | True |  |
| m_csa:15 | 2 | bond_formed, electron_transfer | True | False | low_confidence_event_review, review_status_not_approved, reviewer_id_missing |
| m_csa:16 | 2 | electron_transfer, proton_transfer | True | False | low_confidence_event_review, review_status_not_approved, reviewer_id_missing |
| m_csa:37 | 2 | electron_transfer | True | False | review_status_not_approved, reviewer_id_missing |
| m_csa:66 | 3 | bond_order_changed | True | False | review_status_not_approved, reviewer_id_missing |
| m_csa:68 | 3 | electron_transfer | True | False | low_confidence_event_review, review_status_not_approved, reviewer_id_missing |
| m_csa:94 | 2 | bond_formed | True | False | review_status_not_approved, reviewer_id_missing |
| m_csa:102 | 5 | bond_broken, electron_transfer | True | False | low_confidence_event_review, multi_event_mechanism_review, review_status_not_approved, reviewer_id_missing |
| m_csa:124 | 5 | electron_transfer, proton_transfer | True | False | multi_event_mechanism_review, review_status_not_approved, reviewer_id_missing |
| m_csa:133 | 5 | bond_formed, electron_transfer, proton_transfer | True | False | low_confidence_event_review, multi_event_mechanism_review, review_status_not_approved, reviewer_id_missing |
| m_csa:147 | 4 | bond_order_changed, proton_transfer | True | False | multi_event_mechanism_review, review_status_not_approved, reviewer_id_missing |
| m_csa:169 | 4 | bond_broken, bond_formed, proton_transfer | True | True |  |
| m_csa:186 | 2 | bond_broken, bond_order_changed | True | False | review_status_not_approved, reviewer_id_missing |

## Interpretation

- The P0 sidecar has approved consumable rows for bounded split-filtered materialization, but the full 15-row refresh remains blocked until all draft rows are reviewed.
- Resolve the Rhea-missing rows, manually approve or reject each draft event with reviewer provenance, rerun the strict audit and this readiness audit, then refresh only train/cal feature contracts if the refresh gate passes.
