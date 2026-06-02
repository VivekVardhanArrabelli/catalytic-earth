# Mechanism Feature Row-Specific Bond-Change P0 Refresh-Blocker Audit - current702

Run: 2026-06-02T09:19:56Z

Automation-only decision audit for whether the P0 row-specific bond/proton/electron draft evidence can refresh the no-template mechanism-feature contract.

## Status

- p0_no_template_feature_refresh_allowed_after_review_gate
- Automation feature-contract refresh allowed: True
- Sidecar rows: 15
- Structurally ready draft rows: 15
- Approved consumable rows: 15
- Reviewer decision required rows: 0
- Copy-ready approved decisions: 0
- Rhea unresolved rows: 0

## Source Statuses

- strict_audit: p0_source_evidence_sidecar_strict_audit_passed_reviewed_consumable
- feature_readiness: p0_feature_readiness_audit_ready_for_feature_contract_refresh
- rhea_resolution_consumption: p0_rhea_resolution_consumption_audit_passed_review_only
- unresolved_official_source: p0_rhea_unresolved_official_source_audit_ready_review_only
- reviewer_decision_matrix: p0_reviewer_decision_matrix_ready_review_only
- feature_contract_gap: row_specific_bond_change_gap_not_consumed_by_feature_contract

## Unresolved Decision Rows

| row | accession | source status | reviewer | copy ready | blockers |
| --- | --- | --- | --- | --- | --- |

## Interpretation

- The reviewed P0 evidence passes all refresh gates.
- Run only split-filtered train/cal materialization or the no-template mechanism-feature pilot; do not tune on heldout rows.
