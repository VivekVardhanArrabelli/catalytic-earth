automation: ce-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-16T18:04:36Z
started_local: Tue Jun 16 13:04:36 CDT 2026
closeout_at: 2026-06-16T18:55:02Z
elapsed_minutes: 50.4
remaining_minutes: 4.6
budget_minutes: 55
planned_closeout_minute: 50

state: source_transfer_repair_lanes_enriched_no_registry_apply
lock: acquired by this run at 2026-06-16T18:04:36Z
branch: main
base_at_start: 32deaca7e00715c5ed9bcb9141783b5efd163bc0
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

validation:
  registry_validate: passed
  baseline_critical_suite: 258 passed, 14 subtests
  focused_cli_transfer_regression: 16 passed, 111 deselected
  focused_cli_module: 219 passed, 160 subtests
  focused_transfer_scope_module: 125 passed
  hygiene_tests: 23 passed
  compileall: passed
  full_pytest: 2369 passed, 1 warning, 244 subtests
  current_docs_artifact_reference_check: 0 missing / 2021 checked
  run1804_json_parse: passed
  progress_jsonl_parse: passed
  git_diff_check: passed
  registry_file_size_scan_over_45mb: none
  artifact_storage_policy_blocker: 4 pre-existing large unclassified 20260609/20260610 artifacts; deletion_authorized_count 0

current_counts:
  frozen_current702_rows: 702
  expansion_rows: 8026
  combined_labels: 8728
  positive_holes: 0
  floor_deficit: 0
  novelty_replay: 7565 admit / 414 throttle / 47 reject
  factory_ready_existing_lanes_ge150: 0
  top_projected_clean_admits: 77

run1804_source_transfer:
  all_vs_all_sequence_search: 47 candidates / 0 exact duplicate pairs / 0 near duplicate pairs / 47 no-signal rows
  all_vs_all_backend: mmseqs2_easy_search
  remaining_duplicate_screen_blocker: uniref_wide_duplicate_screen_not_run
  success_criteria_status: needs_more_work
  success_criteria_blockers: active_site_source_unresolved 6 / broader_duplicate_screening_unresolved 12 / full_label_factory_gate_not_passed 12 / representation_control_unresolved 2 / review_decision_not_terminal 12
  terminal_decisions: 12
  terminal_rejected_active_site_evidence_missing: 6
  terminal_rejected_duplicate_or_near_duplicate: 2
  terminal_deferred_requires_human_expert: 4
  normalized_human_expert_queue_rows: 5
  mechanism_repair_lane_rows: 5
  mechanism_repair_lane_counts: AKR/NADP 1 / SDR/NAD(P) 1 / DNA Pol X 1 / glycoside boundary 1 / manual 1
  source_context_status_counts: specific_reaction_context_present 5
  representation_conflicts_repaired_review_only: 3
  glycoside_boundary_repaired: false
  import_ready_rows: 0
  countable_label_candidate_rows: 0

code_changes:
  - build-external-source-pilot-mechanism-repair-lanes accepts optional source-context decisions for review-only enrichment.
  - Repair lane routing now normalizes flattened terminal active-site and Rhea reaction context rows.
  - SDR, AKR, DNA Pol X, glycoside, sugar-phosphate, and Schiff-base repair controls use normalized source-context helpers.
  - Added CLI parser coverage for optional source-context decisions and transfer-scope regression coverage for flattened terminal rows.

no_apply_reason: >
  No holes or under-floor fingerprints are open; no current existing lane projects >=150 clean admits;
  source-transfer repair rows remain review-only and still need a broader approved duplicate screen
  plus rerun confidence, normalization, repair-control, factory, and import-safety gates. The run
  therefore made no registry mutation and preserved frozen current702 exactly.

next_action: >
  Run the approved broader UniRef/current-reference duplicate screen for the 5 normalized needs_review
  rows in artifacts/v3_external_source_pilot_mechanism_repair_lanes_t12_allvsall_current702_20260616_run1804_enriched.json,
  then rerun confidence, normalization, repair controls, and import-safety adjudication. Do not
  import/apply from the run1804 source-transfer artifacts.
