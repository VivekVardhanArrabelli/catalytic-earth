# Active Lever Priority Decision Templates - current702

Run: 2026-06-03T10:22:01Z

Review-only patch templates for the active Lever 2/3/4 decision queue. The templates preserve hashes and allowed decision values but leave every decision pending; they are not applied by automation.

## Status

- active_lever_priority_decision_templates_ready_review_only
- Template rows: 78
- P10746 policy decision templates: 1
- Family-panel import-preview candidate templates: 6
- Clean locator rewrite approval templates: 49
- Warning locator rewrite approval templates: 6
- Source locations matched by hash: 78
- Source locations unresolved: 0
- Blockers: []

## Decision

- Templates ready for review: True
- Apply templates now: False
- Decisions still required: True
- Next gate: Copy only reviewed decisions back into the source decision packets with hashes unchanged, then rerun the relevant application or materialization gate. Pending template values must not be consumed as approvals.

## Priority Rows

| group | row | source artifact | pending field | source pointer | allowed decisions |
| --- | --- | --- | --- | --- | --- |
| p10746_policy_decisions | m_csa:204 | p10746_decision_packet | decision | /decision_stubs/0 | ['explicit_accept_p10746_fold_only_deployment_caveat', 'reject_p10746_caveat_require_approved_non_residue_sidecar'] |
| family_panel_import_preview_candidates | m_csa:10 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/12 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| family_panel_import_preview_candidates | m_csa:30 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/7 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| family_panel_import_preview_candidates | m_csa:31 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/8 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| family_panel_import_preview_candidates | m_csa:191 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/21 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| family_panel_import_preview_candidates | m_csa:448 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/10 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| family_panel_import_preview_candidates | m_csa:973 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/6 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| clean_locator_rewrite_approvals | m_csa:3 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/0 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| clean_locator_rewrite_approvals | m_csa:9 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/1 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| clean_locator_rewrite_approvals | m_csa:32 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/2 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| clean_locator_rewrite_approvals | m_csa:43 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/3 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| clean_locator_rewrite_approvals | m_csa:44 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/4 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| clean_locator_rewrite_approvals | m_csa:45 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/5 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| clean_locator_rewrite_approvals | m_csa:46 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/6 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| clean_locator_rewrite_approvals | m_csa:97 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/8 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| clean_locator_rewrite_approvals | m_csa:109 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/9 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| clean_locator_rewrite_approvals | m_csa:115 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/10 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| clean_locator_rewrite_approvals | m_csa:121 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/11 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| clean_locator_rewrite_approvals | m_csa:131 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/12 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| other_family_panel_expert_decisions | m_csa:116 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/13 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| other_family_panel_expert_decisions | m_csa:131 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/3 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| other_family_panel_expert_decisions | m_csa:132 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/4 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| other_family_panel_expert_decisions | m_csa:267 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/9 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| other_family_panel_expert_decisions | m_csa:551 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/5 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| other_family_panel_expert_decisions | m_csa:750 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/0 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| other_family_panel_expert_decisions | mh_066 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/17 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| other_family_panel_expert_decisions | mh_067 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/18 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| other_family_panel_expert_decisions | mh_068 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/19 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| other_family_panel_expert_decisions | mh_073 | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/14 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| other_family_panel_expert_decisions | secondary_probe::radical_sam_enzyme | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/2 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| other_family_panel_expert_decisions | external_glycoside_panel | family_panel_expert_import_decision_packet | decision | /expert_import_decision_stubs/11 | ['explicit_accept_family_panel_import_candidate', 'reject_family_panel_import_candidate', 'keep_family_panel_review_only_require_more_evidence'] |
| warning_locator_rewrite_approvals | m_csa:56 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/7 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| warning_locator_rewrite_approvals | m_csa:199 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/18 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| warning_locator_rewrite_approvals | m_csa:356 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/29 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| warning_locator_rewrite_approvals | m_csa:480 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/37 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| warning_locator_rewrite_approvals | m_csa:541 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/41 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |
| warning_locator_rewrite_approvals | m_csa:599 | lever2_locator_rewrite_approval_packet | reviewer_decision | /locator_rewrite_decision_stubs/44 | ['explicit_approve_locator_rewrite', 'reject_locator_rewrite'] |

## Interpretation

- 78 decision templates are staged, with all decision values still pending.
- The priority review surface is now patch-ready: one P10746 policy template, six import-preview family-panel templates, and 49 clean locator-approval templates are separated from lower-priority or warning rows.
- Review and replace pending values in the source packets, not in this derived template artifact; rerun actionability after those packet edits land.
