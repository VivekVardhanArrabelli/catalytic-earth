# Mechanism Feature Row-Specific Bond-Change P0 Source-Evidence Review Queue - current702

Run: 2026-06-02T08:08:29Z

Manual-review queue for the draft P0 source-evidence sidecar. It orders rows by review blockers and complexity, but authorizes no approval, feature-contract refresh, or model use.

## Status

- p0_source_evidence_review_queue_ready_manual_only
- Queue rows: 15
- Category counts: {'approved_m_csa_only_source_evidence': 3, 'approved_rhea_backed_source_evidence': 6, 'high_complexity_multi_event_review': 3, 'standard_draft_event_review': 3}
- Blocker counts: {'low_confidence_event_review': 6, 'multi_event_mechanism_review': 3, 'review_status_not_approved': 6}
- Approved rows: 9
- Feature-contract consumable rows: 9
- Critical violations: 0

## Priority Rows

- P2 m_csa:6: high_complexity_multi_event_review; events=5; blockers=review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review
- P2 m_csa:102: high_complexity_multi_event_review; events=5; blockers=review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review
- P2 m_csa:133: high_complexity_multi_event_review; events=5; blockers=review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review
- P3 m_csa:68: standard_draft_event_review; events=3; blockers=review_status_not_approved, low_confidence_event_review
- P3 m_csa:15: standard_draft_event_review; events=2; blockers=review_status_not_approved, low_confidence_event_review
- P3 m_csa:16: standard_draft_event_review; events=2; blockers=review_status_not_approved, low_confidence_event_review
- P9 m_csa:124: approved_rhea_backed_source_evidence; events=5; blockers=
- P9 m_csa:11: approved_m_csa_only_source_evidence; events=4; blockers=
- P9 m_csa:147: approved_rhea_backed_source_evidence; events=4; blockers=
- P9 m_csa:169: approved_m_csa_only_source_evidence; events=4; blockers=
- P9 m_csa:66: approved_rhea_backed_source_evidence; events=3; blockers=
- P9 m_csa:37: approved_rhea_backed_source_evidence; events=2; blockers=
- P9 m_csa:94: approved_rhea_backed_source_evidence; events=2; blockers=
- P9 m_csa:186: approved_rhea_backed_source_evidence; events=2; blockers=
- P9 m_csa:5: approved_m_csa_only_source_evidence; events=1; blockers=

## Interpretation

- The P0 sidecar has a manual-review ordering surface; rows with reviewer-approved source evidence are separated from remaining draft review rows.
- Materialize only approved train/cal rows into the feature contract after strict split filtering; continue manual review for remaining draft rows.
