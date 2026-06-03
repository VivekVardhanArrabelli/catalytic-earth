# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Event-Axis Linker Signoff Finalization - current702

Run: 2026-06-03T21:17:19Z

Review-to-gate bridge for source-free event-axis linker rows. It copies only explicitly approved, fully attested linker rows into the event_axis_linker_rows container consumed by the materialization gate; pending, rejected, incomplete, or guardrail-violating rows remain non-consumable.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_signoff_finalization_blocked_review_only
- Draft signoff rows: 53
- Rows with both roles: 14
- Priority 1 both-roles moderate evidence rows: 3
- Priority 2 both-roles weak evidence rows: 11
- Priority 3 weak missing-both-roles rewrite rows: 6
- Insufficient event-axis evidence rewrite/reject rows: 33
- Pending reviewer signoff rows: 53
- Explicit approved rows: 0
- Explicit rejected rows: 0
- Gate-consumable rows: 0
- Priority review rows: 14
- Approved invalid rows: 0
- Blockers: ['event_axis_signoff_decisions_pending', 'explicit_event_axis_linker_approvals_missing', 'source_free_event_axis_linker_rows_missing']

## Decision

- Reviewer decisions available: False
- Rows ready for materialization gate: False
- Event-axis linkers materialized: False
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: Collect explicit event-axis signoff decisions. Once one or more rows are approved with ready status, reviewer metadata, filled source-free evidence, confidence values, and clean guardrail audits, pass this artifact to the event-axis materialization gate.

## Priority Review Rows

- m_csa:418 P37821 priority_1_both_roles_moderate_evidence_review linkers=4
- m_csa:545 Q7M523 priority_1_both_roles_moderate_evidence_review linkers=3
- m_csa:750 P55792 priority_1_both_roles_moderate_evidence_review linkers=2
- m_csa:3 P15559 priority_2_both_roles_weak_evidence_review linkers=2
- m_csa:115 Q9T0N8 priority_2_both_roles_weak_evidence_review linkers=4
- m_csa:121 P07850 priority_2_both_roles_weak_evidence_review linkers=1
- m_csa:211 P38489 priority_2_both_roles_weak_evidence_review linkers=6
- m_csa:239 P00433 priority_2_both_roles_weak_evidence_review linkers=4
- m_csa:250 P04963 priority_2_both_roles_weak_evidence_review linkers=2
- m_csa:419 O52552 priority_2_both_roles_weak_evidence_review linkers=2
- m_csa:709 P00431 priority_2_both_roles_weak_evidence_review linkers=4
- m_csa:714 P0ABI8 priority_2_both_roles_weak_evidence_review linkers=1
- m_csa:854 P80147 priority_2_both_roles_weak_evidence_review linkers=2
- m_csa:990 Q8GS60 priority_2_both_roles_weak_evidence_review linkers=2

## Interpretation

- 0 gate-consumable linker rows finalized from 53 draft signoff rows; 53 rows still await reviewer signoff.
- Do not rerun the heldout threshold. First secure explicit event-axis approvals and rerun the materialization gate on this finalized rows artifact.
