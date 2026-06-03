# Fold-Augmented Family-Panel Acceptance Scenario Plan - current702

Run: 2026-06-03T13:20:58Z

Review-only Lever 4 counterfactual scenario for the pending expert import decision packet. It lists rows that would become accepted import-preview candidates if explicitly accepted with unchanged context hashes. It does not apply decisions, write import preview rows, run label-factory gates, edit labels, or make rows countable.

## Status

- family_panel_acceptance_scenario_plan_ready_review_only
- Decision stubs: 22
- Acceptance scenario rows: 6
- Non-preview rows if accepted: 16
- Panels represented: 5
- Label-factory candidates if all scenario rows accepted: 6
- Countable label candidates now: 0
- Rows by panel: {'flavin_monooxygenase_and_flavin_oxygen_transfer': 1, 'glycyl_radical_or_thiamine_radical_lyase_boundary': 2, 'lipoamide_or_sulfur_transfer_redox_boundary': 1, 'near_orphan_glycoside_or_nucleoside_hydrolase_controls': 1, 'thiol_disulfide_oxidoreductase_isomerase_boundary': 1}
- Non-preview blocker classes: {'completed_source_check_review_only_no_promotion': 11, 'source_free_locator_or_primary_channel_missing': 5}
- Blockers: ['expert_import_decisions_not_recorded', 'some_family_panel_rows_still_blocked_after_accept_decision']

## Decision

- Apply expert decisions now: False
- Write import preview now: False
- Run label-factory gate now: False
- New countable labels authorized: False
- Next gate: If reviewers explicitly accept any scenario rows with unchanged decision_context_sha256 values and reviewed_expert_import_decision status, rerun the expert decision application, then build the accepted import preview and label-factory readiness artifacts. Do not count labels until the label-factory gate passes.

## Acceptance Scenario Rows

| row | panel | required decision | decision context sha | next gate |
| --- | --- | --- | --- | --- |
| m_csa:973 | flavin_monooxygenase_and_flavin_oxygen_transfer | explicit_accept_family_panel_import_candidate | 1dabc7673a19 | accepted_import_preview_then_label_factory_gate |
| m_csa:30 | glycyl_radical_or_thiamine_radical_lyase_boundary | explicit_accept_family_panel_import_candidate | 053f26507363 | accepted_import_preview_then_label_factory_gate |
| m_csa:31 | glycyl_radical_or_thiamine_radical_lyase_boundary | explicit_accept_family_panel_import_candidate | 53c1ef64975b | accepted_import_preview_then_label_factory_gate |
| m_csa:448 | lipoamide_or_sulfur_transfer_redox_boundary | explicit_accept_family_panel_import_candidate | 5b858c3589a6 | accepted_import_preview_then_label_factory_gate |
| m_csa:10 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | explicit_accept_family_panel_import_candidate | 7ed5f5d914a8 | accepted_import_preview_then_label_factory_gate |
| m_csa:191 | thiol_disulfide_oxidoreductase_isomerase_boundary | explicit_accept_family_panel_import_candidate | ec8b364f55c8 | accepted_import_preview_then_label_factory_gate |

## Interpretation

- 6 family-panel rows could reach import preview if explicitly accepted; zero are countable now.
- The scenario isolates the near-term Lever 4 upside from rows that still need family-promotion, locator, or primary-channel work after an accept decision.
- Review the scenario rows first if the goal is to widen the countable benchmark surface fastest; keep the non-preview rows review-only until their primary blockers clear.
