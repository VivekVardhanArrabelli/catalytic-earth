# Mechanism Feature Row-Specific Bond-Change P0 Source-Evidence Review Queue - current702

Run: 2026-06-02T05:15:15Z

Manual-review queue for the draft P0 source-evidence sidecar. It orders rows by review blockers and complexity, but authorizes no approval, feature-contract refresh, or model use.

## Status

- p0_source_evidence_review_queue_ready_manual_only
- Queue rows: 15
- Category counts: {'approved_m_csa_only_source_evidence': 3, 'high_complexity_multi_event_review': 5, 'standard_draft_event_review': 7}
- Blocker counts: {'low_confidence_event_review': 6, 'multi_event_mechanism_review': 5, 'review_status_not_approved': 12}
- Approved rows: 3
- Feature-contract consumable rows: 3
- Critical violations: 0

## Priority Rows

- P2 m_csa:6: high_complexity_multi_event_review; events=5; blockers=review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review
- P2 m_csa:102: high_complexity_multi_event_review; events=5; blockers=review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review
- P2 m_csa:124: high_complexity_multi_event_review; events=5; blockers=review_status_not_approved, multi_event_mechanism_review
- P2 m_csa:133: high_complexity_multi_event_review; events=5; blockers=review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review
- P2 m_csa:147: high_complexity_multi_event_review; events=4; blockers=review_status_not_approved, multi_event_mechanism_review
- P3 m_csa:66: standard_draft_event_review; events=3; blockers=review_status_not_approved
- P3 m_csa:68: standard_draft_event_review; events=3; blockers=review_status_not_approved, low_confidence_event_review
- P3 m_csa:15: standard_draft_event_review; events=2; blockers=review_status_not_approved, low_confidence_event_review
- P3 m_csa:16: standard_draft_event_review; events=2; blockers=review_status_not_approved, low_confidence_event_review
- P3 m_csa:37: standard_draft_event_review; events=2; blockers=review_status_not_approved
- P3 m_csa:94: standard_draft_event_review; events=2; blockers=review_status_not_approved
- P3 m_csa:186: standard_draft_event_review; events=2; blockers=review_status_not_approved
- P9 m_csa:11: approved_m_csa_only_source_evidence; events=4; blockers=
- P9 m_csa:169: approved_m_csa_only_source_evidence; events=4; blockers=
- P9 m_csa:5: approved_m_csa_only_source_evidence; events=1; blockers=

## Interpretation

- The P0 sidecar has a manual-review ordering surface; rows with reviewer-approved M-CSA-only provenance are separated from remaining draft review rows.
- Materialize only approved train/cal rows into the feature contract after strict split filtering; continue manual review for remaining draft rows.
