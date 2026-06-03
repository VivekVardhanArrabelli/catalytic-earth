# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Event-Axis Linker Signoff Finalization - current702

Run: 2026-06-03T23:13:43Z

Review-to-gate bridge for source-free event-axis linker rows. It copies only explicitly approved, fully attested linker rows into the event_axis_linker_rows container consumed by the materialization gate; pending, rejected, incomplete, or guardrail-violating rows remain non-consumable.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_signoff_finalization_ready
- Draft signoff rows: 53
- Rows with both roles: 14
- Priority 1 both-roles moderate evidence rows: 3
- Priority 2 both-roles weak evidence rows: 11
- Priority 3 weak missing-both-roles rewrite rows: 6
- Insufficient event-axis evidence rewrite/reject rows: 33
- Pending reviewer signoff rows: 0
- Explicit approved rows: 14
- Explicit rejected rows: 39
- Gate-consumable rows: 14
- Priority review rows: 14
- Approved invalid rows: 0
- Blockers: []

## Decision

- Reviewer decisions available: True
- Rows ready for materialization gate: True
- Event-axis linkers materialized: False
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: Pass the finalized approved rows to the event-axis materialization gate, keeping rejected rows out of the gate input until rewritten.

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

- 14 gate-consumable linker rows finalized from 53 draft signoff rows; 0 rows still await reviewer signoff.
- Rerun the event-axis materialization gate on this finalized rows artifact; do not rerun the heldout threshold until pre-threshold readiness passes.
