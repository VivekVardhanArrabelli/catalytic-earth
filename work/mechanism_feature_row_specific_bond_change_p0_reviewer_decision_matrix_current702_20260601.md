# Mechanism Feature Row-Specific Bond-Change P0 Reviewer Decision Matrix - current702

Run: 2026-06-02T00:26:02Z

Review-only decision matrix for P0 source-evidence rows where official Rhea/UniProt checks did not provide a Rhea cross-reference. It defines the reviewer provenance gate without approving rows or changing feature contracts.

## Status

- p0_reviewer_decision_matrix_ready_review_only
- Decision rows: 3
- Rows with UniProt matching EC activity: 3
- Rows with existing reviewer ID: 0
- Copy-ready approved decisions: 0
- Feature-contract consumable rows: 0

## Decision Rows

| row | accession | events | readiness blockers | available decisions |
| --- | --- | ---: | --- | ---: |
| m_csa:5 | P08819 | 1 | review_status_not_approved, reviewer_id_missing, rhea_equation_missing, rhea_lookup_unresolved | 3 |
| m_csa:11 | P0A6C1 | 4 | low_confidence_event_review, multi_event_mechanism_review, review_status_not_approved, reviewer_id_missing, rhea_equation_missing, rhea_lookup_unresolved | 3 |
| m_csa:169 | P27487 | 4 | multi_event_mechanism_review, review_status_not_approved, reviewer_id_missing, rhea_equation_missing, rhea_lookup_unresolved | 3 |

## Interpretation

- 3 unresolved P0 Rhea rows now have an explicit reviewer decision matrix; zero decisions are recorded by this artifact.
- Human review must choose approve/reject/hold for each row with reviewer provenance before any no-template feature-contract refresh.
