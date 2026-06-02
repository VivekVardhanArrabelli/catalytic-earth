# Fold-Augmented Remaining Blocker Decision Matrix - current702

Run: 2026-06-02T17:22:23Z

Review-only decision matrix for the five remaining Lever 3 deployment blockers after source-sidecar preflight, draft sidecar strict audit, and P23007 alternate-accession scouting.

## Status

- fold_augmented_remaining_blocker_decision_matrix_ready_review_only
- Decision rows: 5
- Source-feature sidecar review rows: 3
- Alternate-accession policy rows: 1
- Non-residue interaction policy rows: 1
- Authorized now: 0
- Ready for scoring now: 0
- Deployment blockers cleared now: 0

## Decision Rows

| priority | row | accession | decision class | evidence status | authorized |
| ---: | --- | --- | --- | --- | ---: |
| 1 | m_csa:531 | P31572 | manual_source_feature_sidecar_review | draft_sidecar_candidate_strict_audit_passed | False |
| 1 | uniprot:P78549 | P78549 | manual_source_feature_sidecar_review | draft_sidecar_candidate_strict_audit_passed | False |
| 1 | uniprot:Q3LXA3 | Q3LXA3 | manual_source_feature_sidecar_review | draft_sidecar_candidate_strict_audit_passed | False |
| 2 | m_csa:78 | P23007 | alternate_accession_coordinate_policy_review | alternate_accession_scout_ready_policy_review_only | False |
| 3 | m_csa:204 | P10746 | non_residue_interaction_sidecar_policy_design | coordinate_available_but_no_primary_residue_features | False |

## Interpretation

- The five remaining Lever 3 production blockers are now reduced to three draft sidecar reviews, one alternate-accession policy decision, and one non-residue interaction policy decision.
- Review the three draft sidecars first; then decide whether to authorize a P23007 alternate accession; leave P10746 fold-only unless a non-residue interaction policy is explicitly defined.
