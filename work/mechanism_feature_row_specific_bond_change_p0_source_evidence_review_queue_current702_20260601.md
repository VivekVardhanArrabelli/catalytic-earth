# Mechanism Feature Row-Specific Bond-Change P0 Source-Evidence Review Queue - current702

Run: 2026-06-01T20:06:02Z

Manual-review queue for the draft P0 source-evidence sidecar. It orders rows by review blockers and complexity, but authorizes no approval, feature-contract refresh, or model use.

## Status

- p0_source_evidence_review_queue_ready_manual_only
- Queue rows: 15
- Category counts: {'high_complexity_multi_event_review': 4, 'rhea_lookup_required_before_approval': 4, 'standard_draft_event_review': 7}
- Blocker counts: {'low_confidence_event_review': 7, 'multi_event_mechanism_review': 7, 'review_status_not_approved': 15, 'rhea_equation_missing': 4}
- Approved rows: 0
- Feature-contract consumable rows: 0
- Critical violations: 0

## Priority Rows

- P1 m_csa:124: rhea_lookup_required_before_approval; events=5; blockers=review_status_not_approved, rhea_equation_missing, multi_event_mechanism_review
- P1 m_csa:11: rhea_lookup_required_before_approval; events=4; blockers=review_status_not_approved, rhea_equation_missing, multi_event_mechanism_review, low_confidence_event_review
- P1 m_csa:169: rhea_lookup_required_before_approval; events=4; blockers=review_status_not_approved, rhea_equation_missing, multi_event_mechanism_review
- P1 m_csa:5: rhea_lookup_required_before_approval; events=1; blockers=review_status_not_approved, rhea_equation_missing
- P2 m_csa:6: high_complexity_multi_event_review; events=5; blockers=review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review
- P2 m_csa:102: high_complexity_multi_event_review; events=5; blockers=review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review
- P2 m_csa:133: high_complexity_multi_event_review; events=5; blockers=review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review
- P2 m_csa:147: high_complexity_multi_event_review; events=4; blockers=review_status_not_approved, multi_event_mechanism_review
- P3 m_csa:66: standard_draft_event_review; events=3; blockers=review_status_not_approved
- P3 m_csa:68: standard_draft_event_review; events=3; blockers=review_status_not_approved, low_confidence_event_review
- P3 m_csa:15: standard_draft_event_review; events=2; blockers=review_status_not_approved, low_confidence_event_review
- P3 m_csa:16: standard_draft_event_review; events=2; blockers=review_status_not_approved, low_confidence_event_review
- P3 m_csa:37: standard_draft_event_review; events=2; blockers=review_status_not_approved
- P3 m_csa:94: standard_draft_event_review; events=2; blockers=review_status_not_approved
- P3 m_csa:186: standard_draft_event_review; events=2; blockers=review_status_not_approved

## Interpretation

- The draft P0 sidecar is ready for manual review ordering, not for feature consumption. Rows with missing Rhea equations come first, followed by multi-event mechanism reviews.
- Start with the Rhea-missing rows in priority order; update row review_status only after source-backed manual review and rerun the strict sidecar audit.
