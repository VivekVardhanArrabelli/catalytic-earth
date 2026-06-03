# Active Lever Decision Application Contract Audit - current702

Run: 2026-06-03T11:20:34Z

Read-only contract audit across the active Lever 2/3/4 source-decision intake preflight and the three downstream decision application gates. It checks that reviewed status, approval booleans, and application readiness stay fail-closed before any follow-on gate is run.

## Status

- active_lever_decision_application_contract_audit_passed_pending_source_decisions
- Contract violations: 0
- Source-intake pending rows: 78
- Source-intake follow-on ready rows: 0
- Mechanical gates ready now: 0

## Gate Checks

| gate | status | reviewed/approved | pending | invalid | intake ready |
| --- | --- | ---: | ---: | ---: | ---: |
| p10746_deployment_caveat_decision_application | p10746_deployment_caveat_decision_application_blocked_pending_explicit_decision | 0 | 1 | 0 | 0 |
| family_panel_expert_import_decision_application | family_panel_expert_import_decision_application_blocked | 0 | 22 | 0 | 0 |
| locator_rewrite_materialization_gate | p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_materialization_gate_ready_blocked | 0 | None | 0 | 0 |

## Decision

- Application contracts aligned: True
- Run any matching gate now: False
- Next gate: If source intake is ready and this contract audit has zero violations, rerun only the matching application/materialization gate. Otherwise edit source decision packets, not derived application artifacts.

## Interpretation

- 0 active decision application contract violations found.
- The active decision applications and source intake remain fail-closed while source decisions are pending.
- Record reviewed source decisions with required review statuses and approval booleans, rerun intake, then rerun this contract audit.
