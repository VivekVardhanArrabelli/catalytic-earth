automation: ce-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-16T15:03:49Z
started_local: Tue Jun 16 10:03:52 CDT 2026
closeout_at: 2026-06-16T15:27:05Z
elapsed_minutes: 23.3
remaining_minutes: 31.7
budget_minutes: 55
planned_closeout_minute: 50

state: blocked_closeout_after_verified_non_destructive_closure
lock: acquired by this run at 2026-06-16T15:03:49Z
branch: main
base_at_start: a611246f724128feee11857b62058a6bb64a9e5e
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

validation:
  registry_validate: passed
  baseline_focused_suite: 293 passed, 14 subtests
  closure_regression_suite: 4 passed
  full_pytest: 2364 passed, 1 warning, 244 subtests
  json_jsonl_parse: passed
  git_diff_check: passed
  registry_file_size_scan_over_45mb: none
  run1503_artifact_file_size_scan_over_45mb: none

current_counts:
  frozen_current702_rows: 702
  expansion_rows: 8026
  combined_labels: 8728
  positive_holes: 0
  floor_deficit: 0
  novelty_replay: 7565 admit / 414 throttle / 47 reject
  factory_ready_existing_lanes_ge150: 0
  top_projected_clean_admits: 77

closure_packet:
  review_surface_rows: 833
  controlled_import_review_ready_rows: 197
  blocked_rows: 636
  coordinate_blockers: 473
  locator_blockers: 121
  current702_duplicate_rows: 13
  external_duplicate_rows: 27
  hard_blockers: 2
  production_import_authorized: false
  ready_for_production_label_import: false

early_closeout_reason: >
  No safe scaling item remains actionable in this run: the 197 ready rows require explicit
  controlled batch approval plus label-factory and registry-change authorization before any apply;
  the 636-row repair queue is dominated by coordinate materialization, but local disk free space
  is below the 10 GiB coordinate-download floor; and artifact storage policy is blocked by four
  pre-existing large unclassified artifacts while the migration readiness plan authorizes zero
  migrations or deletions. Continuing without those prerequisites would either mutate registry
  state without authorization, start coordinate download work below the documented safety floor,
  or perform ad hoc artifact cleanup outside the committed manifest.

next_action: >
  Obtain explicit controlled batch approval plus label-factory/registry-change authorization for
  the 197 machine-clean rows, or restore disk free space above 10 GiB and rerun scoped
  materialization/repair for the 636 blocked rows.
