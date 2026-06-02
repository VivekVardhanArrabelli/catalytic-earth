# Mechanism Feature Row-Specific Bond-Change P0 Refresh-Blocker Audit - current702

Run: 2026-06-02T02:07:14Z

Automation-only decision audit for whether the P0 row-specific bond/proton/electron draft evidence can refresh the no-template mechanism-feature contract.

## Status

- p0_no_template_feature_refresh_blocked_review_required
- Automation feature-contract refresh allowed: False
- Sidecar rows: 15
- Structurally ready draft rows: 15
- Approved consumable rows: 0
- Reviewer decision required rows: 3
- Copy-ready approved decisions: 0
- Rhea unresolved rows: 3

## Source Statuses

- strict_audit: p0_source_evidence_sidecar_strict_audit_passed_draft_not_consumable
- feature_readiness: p0_feature_readiness_audit_blocked_review_required
- rhea_resolution_consumption: p0_rhea_resolution_consumption_audit_passed_review_only
- unresolved_official_source: p0_rhea_unresolved_official_source_audit_ready_review_only
- reviewer_decision_matrix: p0_reviewer_decision_matrix_ready_review_only
- feature_contract_gap: row_specific_bond_change_gap_not_consumed_by_feature_contract

## Unresolved Decision Rows

| row | accession | source status | reviewer | copy ready | blockers |
| --- | --- | --- | --- | --- | --- |
| m_csa:5 | P08819 | official_ec_activity_present_without_rhea_cross_reference | None | False | review_status_not_approved, reviewer_id_missing, rhea_equation_missing, rhea_lookup_unresolved |
| m_csa:11 | P0A6C1 | official_ec_activity_present_without_rhea_cross_reference | None | False | low_confidence_event_review, multi_event_mechanism_review, review_status_not_approved, reviewer_id_missing, rhea_equation_missing, rhea_lookup_unresolved |
| m_csa:169 | P27487 | official_ec_activity_present_without_rhea_cross_reference | None | False | multi_event_mechanism_review, review_status_not_approved, reviewer_id_missing, rhea_equation_missing, rhea_lookup_unresolved |

## Interpretation

- The no-template mechanism-feature contract refresh remains blocked: draft P0 evidence is structurally present, but no row has reviewer provenance or feature-contract consumption approval.
- Use the reviewer decision matrix for m_csa:5, m_csa:11, and m_csa:169; after human decisions are recorded, rerun the strict sidecar, review queue, Rhea manifest, feature-readiness, consumption, and this blocker audit before refreshing any feature contract.
