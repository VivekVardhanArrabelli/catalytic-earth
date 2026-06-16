automation: ce-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-16T16:04:36Z
started_local: Tue Jun 16 11:04:36 CDT 2026
closeout_at: 2026-06-16T16:59:00Z
elapsed_minutes: 54.4
remaining_minutes: 0.6
budget_minutes: 55
planned_closeout_minute: 50

state: source_transfer_pilot_review_queue_built_no_registry_apply
lock: acquired by this run at 2026-06-16T16:04:51Z
branch: main
base_at_start: 41a7102177fc9c4500454b8cf84e4bd41c167865
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

validation:
  registry_validate: passed
  baseline_critical_suite: 273 passed, 14 subtests
  sequence_and_structural_regressions: 3 passed
  final_focused_suite: 366 passed, 14 subtests
  full_pytest: 2366 passed, 1 warning
  current_docs_artifact_reference_check: 0 missing
  json_jsonl_parse: passed
  git_diff_check: passed
  registry_and_run1604_file_size_scan_over_45mb: none

current_counts:
  frozen_current702_rows: 702
  expansion_rows: 8026
  combined_labels: 8728
  positive_holes: 0
  floor_deficit: 0
  novelty_replay: 7565 admit / 414 throttle / 47 reject
  factory_ready_existing_lanes_ge150: 0
  top_projected_clean_admits: 77

run1604_source_transfer:
  candidate_manifest_rows: 47
  full47_blocker_matrix_rows: 47
  full47_blocker_matrix_import_ready_rows: 0
  active_site_source_gaps: 21
  heuristic_scope_mismatches: 14
  representation_backend_not_selected: 12
  exact_sequence_holdouts: 2
  representation_near_duplicate_holdouts: 1
  pilot_rows: 12
  pilot_explicit_active_site_source_present: 6
  pilot_binding_context_only: 6
  transfer_gate: 65 passed / 66 total
  transfer_gate_blocker: external_pilot_representation_sample_review_only
  terminal_decisions: 12
  terminal_rejected_active_site_evidence_missing: 6
  terminal_deferred_requires_human_expert: 6
  normalized_human_expert_queue_rows: 6
  import_ready_rows: 0
  countable_label_candidate_rows: 0

code_changes:
  - build-external-source-sequence-neighborhood-plan gained opt-in --include-manifest-rows for complete review-only manifest coverage.
  - build-external-structural-tm-holdout-path now prefers artifact-lineage slice/path metadata over stale manifest/default 1025 values.

next_action: >
  Build or provide a current learned pilot-representation backend sample for the 12 selected
  source-transfer pilot rows, rerun stability/adjudication plus the transfer gate/confidence audit,
  then complete review/factory/duplicate gates before considering any external-registry-only import.
