automation: ce-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-16T19:04:40Z
started_local: Tue Jun 16 14:04:40 CDT 2026
closeout_at: 2026-06-16T19:54:16Z
elapsed_minutes: 49.6
remaining_minutes: 5.4
budget_minutes: 55
planned_closeout_minute: 50

state: source_transfer_uniref_duplicate_screen_no_registry_apply
lock: acquired by this run at 2026-06-16T19:04:53Z
branch: main
base_at_start: dcebefa0a15a1e589834a391b1279c3b0b741340
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

validation:
  registry_validate: passed
  baseline_critical_suite: 587 passed, 174 subtests
  focused_uniref_regression: 6 passed, 126 deselected
  cli_transfer_scope_modules: 349 passed, 160 subtests
  final_critical_suite: 592 passed, 174 subtests
  final_full_pytest: 2374 passed, 1 warning, 244 subtests
  source_scout_focused_tests: 14 passed
  final_pinpoint_transfer_scope: 1 passed, 129 deselected
  final_pinpoint_cli_parser: 1 passed
  compileall: passed
  current_docs_artifact_reference_check: 0 missing / 2036 checked
  run1904_json_parse: passed
  progress_jsonl_parse: passed
  git_diff_check: passed
  staged_git_diff_check: passed
  frozen_registry_diff: none
  registry_artifact_hard_limit_scan_over_90mb: none
  run1904_artifact_footprint: 9.7M

current_counts:
  frozen_current702_rows: 702
  expansion_rows: 8026
  combined_labels: 8728
  positive_holes: 0
  floor_deficit: 0
  novelty_replay: 7565 admit / 414 throttle / 47 reject
  factory_ready_existing_lanes_ge150: 0
  top_projected_clean_admits: 77
  source_scale_recommendation: stop_m_csa_only_tranche_growth_and_scope_external_source_transfer

run1904_source_transfer:
  uniref_current_reference_screen: 5 candidates / 13 UniRef clusters fetched / 5 no-overlap rows / 0 fetch failures / 0 overlap holdouts
  success_criteria_status: needs_more_work
  broader_duplicate_screening_status_counts: current_reference_external_all_vs_all_uniref_no_signal 5 / broader_duplicate_screening_required 7
  success_criteria_blockers: active_site_source_unresolved 6 / broader_duplicate_screening_unresolved 7 / full_label_factory_gate_not_passed 12 / representation_control_unresolved 2 / review_decision_not_terminal 12
  terminal_decisions: 12
  terminal_rejected_active_site_evidence_missing: 6
  terminal_rejected_duplicate_or_near_duplicate: 2
  terminal_deferred_requires_human_expert: 4
  normalized_human_expert_queue_rows: 5
  queued_needs_review_accessions: C9JRZ8 / O14756 / P06746 / Q8N0X4 / P33025
  mechanism_repair_lane_rows: 5
  mechanism_repair_lane_counts: AKR/NADP 1 / SDR/NAD(P) 1 / DNA Pol X 1 / glycoside boundary 1 / manual 1
  representation_conflicts_repaired_review_only: 3
  glycoside_boundary_repaired: false
  import_ready_rows: 0
  countable_label_candidate_rows: 0
  lower_priority_duplicate_residue: 7 rows still require broader duplicate screening, but 6 also lack explicit active-site source and 1 is a representation near-duplicate holdout

source_scouts:
  evidence_handle_expansion: 6 families probed / 4 unlocked by better handles / source-supply uplift 63967 / reachable positive-bronze uplift 741
  breadth_feasibility: 18 families probed / 14 clean / estimated new clean bronze 2641 / projected positive bronze 9673 / gap to 10k positive bronze 327
  breadth_verdict: ten_k_diverse_positive_bronze_NOT_reachable_from_reviewed_swissprot_alone

storage_and_docs:
  current_docs_artifact_reference_check: artifacts/v3_current_docs_artifact_reference_check_current702_20260616_run1904.json
  artifact_storage_policy_status: blocked by 40 large-unclassified policy blockers; deletion_authorized_count 0; migration_ready_now_count 0
  source_scale_limit_audit: artifacts/v3_source_scale_limit_audit_current702_20260616_run1904.json

code_changes:
  - Added build-external-source-pilot-uniref-current-reference-screen for review-only source-transfer pilot duplicate screening against current countable UniRef90/50 references.
  - Wired optional external_uniref_current_reference_screen context into source-transfer confidence and success-criteria replay.
  - Preserved non-countable semantics: no predictive evidence, no import-ready rows, no label rows, and no registry mutation.
  - Added CLI/parser and transfer-scope regression coverage for clear and overlap-hold UniRef/current-reference behavior.

no_apply_reason: >
  No holes or under-floor fingerprints are open; no current existing lane projects >=150 clean admits.
  The source-transfer pilot cleared the broader duplicate-screen process blocker for 5 queued review
  rows, but every row remains review-only and blocked by terminal review, label-factory, active-site,
  representation, or lower-priority duplicate-screen process gates. No registry mutation was made.

next_action: >
  Run the external source pilot review/factory path for the 5 queued needs_review rows in
  artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_t12_allvsall_uniref_current702_20260616_run1904.json,
  using work/external_source_transfer_pilot_uniref_review_queue_current702_20260616_run1904.md
  as the routing note. Then rerun repair controls, import-safety adjudication, success criteria,
  label-factory/novelty/governor/row-guardrail gates, and keep all run1904 rows out of import
  unless those gates pass explicitly.
