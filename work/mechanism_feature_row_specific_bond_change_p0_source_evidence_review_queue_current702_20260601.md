# Mechanism Feature Row-Specific Bond-Change P0 Source-Evidence Review Queue - current702

Run: 2026-06-02T09:19:55Z

Manual-review queue for the draft P0 source-evidence sidecar. It orders rows by review blockers and complexity, but authorizes no approval, feature-contract refresh, or model use.

## Status

- p0_source_evidence_review_queue_ready_manual_only
- Queue rows: 15
- Category counts: {'approved_m_csa_only_source_evidence': 3, 'approved_rhea_backed_source_evidence': 12}
- Blocker counts: {}
- Approved rows: 15
- Feature-contract consumable rows: 15
- Critical violations: 0

## Priority Rows

- P9 m_csa:102: approved_rhea_backed_source_evidence; events=5; blockers=
- P9 m_csa:124: approved_rhea_backed_source_evidence; events=5; blockers=
- P9 m_csa:133: approved_rhea_backed_source_evidence; events=5; blockers=
- P9 m_csa:6: approved_rhea_backed_source_evidence; events=4; blockers=
- P9 m_csa:11: approved_m_csa_only_source_evidence; events=4; blockers=
- P9 m_csa:16: approved_rhea_backed_source_evidence; events=4; blockers=
- P9 m_csa:147: approved_rhea_backed_source_evidence; events=4; blockers=
- P9 m_csa:169: approved_m_csa_only_source_evidence; events=4; blockers=
- P9 m_csa:15: approved_rhea_backed_source_evidence; events=3; blockers=
- P9 m_csa:66: approved_rhea_backed_source_evidence; events=3; blockers=
- P9 m_csa:68: approved_rhea_backed_source_evidence; events=3; blockers=
- P9 m_csa:37: approved_rhea_backed_source_evidence; events=2; blockers=
- P9 m_csa:94: approved_rhea_backed_source_evidence; events=2; blockers=
- P9 m_csa:186: approved_rhea_backed_source_evidence; events=2; blockers=
- P9 m_csa:5: approved_m_csa_only_source_evidence; events=1; blockers=

## Interpretation

- The P0 sidecar has a manual-review ordering surface; rows with reviewer-approved source evidence are separated from remaining draft review rows.
- Materialize only approved train/cal rows into the feature contract after strict split filtering; continue manual review for remaining draft rows.
