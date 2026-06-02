# Mechanism Feature Row-Specific Bond-Change P0 Rhea Resolution Consumption Audit - current702

Run: 2026-06-02T05:15:15Z

Strict review-only audit that the bounded P0 Rhea lookup resolution was consumed only as draft sidecar evidence: resolved rows must carry their Rhea equation, unresolved rows must remain in the lookup/readiness blockers, and no row may become consumable.

## Status

- p0_rhea_resolution_consumption_audit_passed_review_only
- Resolution rows: 4
- Resolved rows: 1
- Unresolved rows: 0
- Remaining lookup manifest rows: 0
- Critical violations: 0

## Row Audits

| row | resolved | Rhea | in remaining manifest | review category | status |
| --- | --- | --- | --- | --- | --- |
| m_csa:5 | False | None | False | approved_m_csa_only_source_evidence | passed |
| m_csa:11 | False | None | False | approved_m_csa_only_source_evidence | passed |
| m_csa:124 | True | RHEA:11436 | False | high_complexity_multi_event_review | passed |
| m_csa:169 | False | None | False | approved_m_csa_only_source_evidence | passed |

## Interpretation

- The Rhea lookup resolution and reviewer decisions are consumed as review evidence; unresolved rows without reviewer approval stay blocked, while approved M-CSA-only rows may be used only by split-filtered feature materialization.
- Continue with feature-readiness and refresh-blocker audits; do not train on heldout rows or use unapproved draft rows.
