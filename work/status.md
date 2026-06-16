automation: ce-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-16T17:04:58Z
started_local: Tue Jun 16 12:04:58 CDT 2026
closeout_at: 2026-06-16T17:24:31Z
elapsed_minutes: 19.6
remaining_minutes: 35.4
budget_minutes: 55
planned_closeout_minute: 50

state: learned_source_transfer_representation_gate_cleared_no_registry_apply
lock: acquired by this run at 2026-06-16T17:04:45Z
branch: main
base_at_start: 46e8112cf5cfa43c58419318180e3dd5316b3bc2
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

validation:
  registry_validate: passed
  baseline_critical_suite: 251 passed
  focused_cli_transfer_regression: 15 passed, 110 deselected
  full_pytest: 2367 passed, 1 warning, 244 subtests
  current_docs_artifact_reference_check: 0 missing
  run1704_json_parse: 24 JSON files parsed
  progress_jsonl_parse: 649 lines parsed
  git_diff_check: passed
  registry_file_size_scan_over_45mb: none
  pre_existing_artifact_file_size_scan_over_45mb: 4 known 20260609/20260610 artifacts

current_counts:
  frozen_current702_rows: 702
  expansion_rows: 8026
  combined_labels: 8728
  positive_holes: 0
  floor_deficit: 0
  novelty_replay: 7565 admit / 414 throttle / 47 reject
  factory_ready_existing_lanes_ge150: 0
  top_projected_clean_admits: 77

run1704_source_transfer:
  selected_pilot_rows: 12
  esm2_t6_8m_sample: 10 complete / 2 near_duplicate_holdout
  esm2_t12_35m_sample: 10 complete / 2 near_duplicate_holdout
  esm2_t30_150m_sample: 7 complete / 5 near_duplicate_holdout
  selected_representation_state: esm2_t12_35m
  selected_representation_adjudication: 8 adjudicated_review_only / 2 stability_review / 2 near_duplicate_holdout
  transfer_gate: 66 passed / 66 total
  terminal_decisions: 12
  terminal_rejected_active_site_evidence_missing: 6
  terminal_rejected_duplicate_or_near_duplicate: 2
  terminal_deferred_requires_human_expert: 4
  normalized_human_expert_queue_rows: 5
  mechanism_repair_lane_rows: 5
  mechanism_repair_lane_type: manual_source_mechanism_review_required
  import_ready_rows: 0
  countable_label_candidate_rows: 0

code_changes:
  - audit-external-source-pilot-decision-confidence no longer loads stale 1025 optional structural/all-vs-all defaults when those optional paths are omitted.
  - Added parser regression coverage for omitted and explicit optional confidence-audit context paths.

early_closeout_reason: >
  No holes or floor deficits exist; no current high-yield lane projects >=150 clean admits;
  coordinate materialization remains blocked by disk below the 10 GiB download floor; the 197
  controlled-ready external import rows still require explicit batch/label-factory/registry
  authorization; and the source-transfer pilot now requires manual source/mechanism review plus
  duplicate/factory gates before any import. No other safe autonomous bronze-scaleout item could be
  advanced without violating these gates.

next_action: >
  Inspect the 5 rows in
  artifacts/v3_external_source_pilot_mechanism_repair_lanes_t12_current702_20260616_run1704.json,
  resolve source-supported mechanism context manually, then rerun duplicate/factory/review gates.
  Do not import/apply from the run1704 source-transfer artifacts.
