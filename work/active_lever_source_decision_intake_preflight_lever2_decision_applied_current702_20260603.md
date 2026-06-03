# Active Lever Source Decision Intake Preflight - current702

Run: 2026-06-03T16:37:37Z

Fail-closed preflight for reviewed source decision packets across active Levers 2/3/4. It compares the source packet rows to the hash-preserving priority templates and reports which downstream application/materialization gates are worth rerunning. It does not apply decisions, copy locator sidecars, write import previews, run label-factory gates, edit labels or registries, train models, or read heldout rows.

## Status

- active_lever_source_decision_intake_preflight_ready
- Template rows: 78
- Explicit decision rows: 55
- Pending decision rows: 23
- Invalid decision rows: 0
- Source edit-contract violation rows: 0
- Follow-on gate-ready rows: 53
- Family-panel accepted candidate rows: 0
- Locator materialization-ready approvals: 53
- Blockers: ['explicit_source_decisions_missing']

## Decision

- P10746 application gate ready: False
- Family-panel application gate ready: False
- Locator materialization gate ready: True
- Run any matching gate now: True
- Next gate: Run only the matching application/materialization gate for hash-valid reviewed rows. If this preflight remains blocked, edit the source decision packets, not the derived template artifact.

## Intake Rows

| priority | lever | row | source pointer | decision field | decision | review status | approved | status | follow-on ready | blockers |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- |
| 1 | Lever 3 | m_csa:204 | /decision_stubs/0 | decision | None | pending_explicit_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 2 | Lever 4 | m_csa:10 | /expert_import_decision_stubs/12 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 2 | Lever 4 | m_csa:30 | /expert_import_decision_stubs/7 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 2 | Lever 4 | m_csa:31 | /expert_import_decision_stubs/8 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 2 | Lever 4 | m_csa:191 | /expert_import_decision_stubs/21 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 2 | Lever 4 | m_csa:448 | /expert_import_decision_stubs/10 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 2 | Lever 4 | m_csa:973 | /expert_import_decision_stubs/6 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 3 | Lever 2 | m_csa:3 | /locator_rewrite_decision_stubs/0 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:9 | /locator_rewrite_decision_stubs/1 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:32 | /locator_rewrite_decision_stubs/2 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:43 | /locator_rewrite_decision_stubs/3 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:44 | /locator_rewrite_decision_stubs/4 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:45 | /locator_rewrite_decision_stubs/5 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:46 | /locator_rewrite_decision_stubs/6 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:97 | /locator_rewrite_decision_stubs/8 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:109 | /locator_rewrite_decision_stubs/9 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:115 | /locator_rewrite_decision_stubs/10 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:121 | /locator_rewrite_decision_stubs/11 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:131 | /locator_rewrite_decision_stubs/12 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:159 | /locator_rewrite_decision_stubs/13 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:163 | /locator_rewrite_decision_stubs/14 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:171 | /locator_rewrite_decision_stubs/15 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:180 | /locator_rewrite_decision_stubs/16 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:188 | /locator_rewrite_decision_stubs/17 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:211 | /locator_rewrite_decision_stubs/19 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:220 | /locator_rewrite_decision_stubs/20 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:239 | /locator_rewrite_decision_stubs/21 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:242 | /locator_rewrite_decision_stubs/22 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:250 | /locator_rewrite_decision_stubs/23 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:311 | /locator_rewrite_decision_stubs/24 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:321 | /locator_rewrite_decision_stubs/25 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:323 | /locator_rewrite_decision_stubs/26 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:333 | /locator_rewrite_decision_stubs/27 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:352 | /locator_rewrite_decision_stubs/28 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:370 | /locator_rewrite_decision_stubs/30 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:384 | /locator_rewrite_decision_stubs/31 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:392 | /locator_rewrite_decision_stubs/32 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:397 | /locator_rewrite_decision_stubs/33 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:403 | /locator_rewrite_decision_stubs/34 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:418 | /locator_rewrite_decision_stubs/35 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:419 | /locator_rewrite_decision_stubs/36 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:497 | /locator_rewrite_decision_stubs/38 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:517 | /locator_rewrite_decision_stubs/39 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:526 | /locator_rewrite_decision_stubs/40 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:545 | /locator_rewrite_decision_stubs/42 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:551 | /locator_rewrite_decision_stubs/43 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:709 | /locator_rewrite_decision_stubs/45 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:710 | /locator_rewrite_decision_stubs/46 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:714 | /locator_rewrite_decision_stubs/47 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:723 | /locator_rewrite_decision_stubs/48 | reviewer_decision | reject_locator_rewrite | None | False | reviewed_locator_rejection_no_materialization | 0 | none |
| 3 | Lever 2 | m_csa:750 | /locator_rewrite_decision_stubs/49 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:853 | /locator_rewrite_decision_stubs/50 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:854 | /locator_rewrite_decision_stubs/51 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:916 | /locator_rewrite_decision_stubs/52 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:990 | /locator_rewrite_decision_stubs/53 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 3 | Lever 2 | m_csa:994 | /locator_rewrite_decision_stubs/54 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 4 | Lever 4 | external_glycoside_panel | /expert_import_decision_stubs/11 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 4 | Lever 4 | m_csa:116 | /expert_import_decision_stubs/13 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 4 | Lever 4 | m_csa:131 | /expert_import_decision_stubs/3 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 4 | Lever 4 | m_csa:132 | /expert_import_decision_stubs/4 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 4 | Lever 4 | m_csa:267 | /expert_import_decision_stubs/9 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 4 | Lever 4 | m_csa:551 | /expert_import_decision_stubs/5 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 4 | Lever 4 | m_csa:750 | /expert_import_decision_stubs/0 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 4 | Lever 4 | mh_064 | /expert_import_decision_stubs/15 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 4 | Lever 4 | mh_065 | /expert_import_decision_stubs/16 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 4 | Lever 4 | mh_066 | /expert_import_decision_stubs/17 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 4 | Lever 4 | mh_067 | /expert_import_decision_stubs/18 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 4 | Lever 4 | mh_068 | /expert_import_decision_stubs/19 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 4 | Lever 4 | mh_072 | /expert_import_decision_stubs/20 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 4 | Lever 4 | mh_073 | /expert_import_decision_stubs/14 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 4 | Lever 4 | secondary_probe::cobalamin_radical_rearrangement | /expert_import_decision_stubs/1 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 4 | Lever 4 | secondary_probe::radical_sam_enzyme | /expert_import_decision_stubs/2 | decision | pending_review | pending_expert_import_decision | None | pending_external_decision | 0 | explicit_decision_missing |
| 5 | Lever 2 | m_csa:56 | /locator_rewrite_decision_stubs/7 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 5 | Lever 2 | m_csa:199 | /locator_rewrite_decision_stubs/18 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 5 | Lever 2 | m_csa:356 | /locator_rewrite_decision_stubs/29 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 5 | Lever 2 | m_csa:480 | /locator_rewrite_decision_stubs/37 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 5 | Lever 2 | m_csa:541 | /locator_rewrite_decision_stubs/41 | reviewer_decision | explicit_approve_locator_rewrite | None | True | ready_for_locator_materialization_gate | 1 | none |
| 5 | Lever 2 | m_csa:599 | /locator_rewrite_decision_stubs/44 | reviewer_decision | reject_locator_rewrite | None | False | reviewed_locator_rejection_no_materialization | 0 | none |

## Interpretation

- 53 hash-valid reviewed source decisions are ready for matching follow-on gates.
- The active lever source packets remain fail-closed unless reviewed decisions use allowed values and preserve every decision-context, candidate, and planned-payload hash.
- Record source packet decisions for the P10746 policy caveat, priority family-panel import rows, or locator rewrite approvals, then rerun this preflight before application gates.
