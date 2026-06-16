automation: ce-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-16T14:03:01Z
started_local: Tue Jun 16 09:03:27 CDT 2026
closeout_at: 2026-06-16T14:50:16Z
elapsed_minutes: 47.3
remaining_minutes: 7.7
budget_minutes: 55
planned_closeout_minute: 50

state: final_validation_passed_ready_for_commit_push_release
lock: acquired by this run at 2026-06-16T14:03:01Z
branch: main
base_at_start: 0efc3a328cfb6f011c6e4bdbd628ee4f187809ae
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

source_handle_scaleout_summary:
  registry_apply_performed: false
  validator_contract_fix: provisional_external_countable_preflight_candidate accepted as source preflight input
  prior_size5_admission_validation: artifacts/v3_external_source_admission_validation_10_current702_20260616_run1403_post_pde_bulk_size5.json
  prior_size5_ready_preview: artifacts/v3_external_source_admission_ready_preview_10_current702_20260616_run1403_post_pde_bulk_size5.json
  prior_size5_validated_rows: 10
  prior_size5_pending_coordinate_materialization: 7
  prior_size5_pending_locator_materialization: 3
  retained_scaleout_scout: artifacts/v3_external_bulk_ingestion_scout_current702_20260616_run1403_size120.json
  retained_scaleout_import_preview: artifacts/v3_external_bulk_ingestion_import_preview_current702_20260616_run1403_size120.json
  retained_scaleout_candidate_rows: 833
  retained_scaleout_provisional_preview_rows: 431
  retained_scaleout_fetch_failures: 0
  retained_scaleout_duplicate_or_current_conflicts: 40
  retained_scaleout_locator_ready_candidates: 236
  retained_scaleout_coordinate_ready_pending_locator: 117
  retained_admission_validation: artifacts/v3_external_source_admission_validation_431_current702_20260616_run1403_bulk_size120.json
  retained_ready_preview: artifacts/v3_external_source_admission_ready_preview_431_current702_20260616_run1403_bulk_size120.json
  retained_admission_ready_rows: 431
  retained_pending_coordinate_materialization: 402
  retained_pending_locator_materialization: 29
  direct_external_label_candidates: 0
  production_import_authorized: false
  scoped_wave2_materialization: artifacts/v3_external_materialization_wave2_size120_current702_20260616_run1403.json
  scoped_wave2_import_ready_preview: artifacts/v3_external_materialization_wave2_size120_import_ready_preview_current702_20260616_run1403.json
  scoped_wave2_repair_queue: artifacts/v3_external_materialization_wave2_size120_repair_queue_current702_20260616_run1403.json
  scoped_wave2_locator_dir: artifacts/external_materialization_wave2_size120_source_free_locators_current702_20260616_run1403
  scoped_wave2_input_rows: 833
  scoped_wave2_locator_sidecars_materialized_new: 667
  scoped_wave2_local_coordinates_reused: 204
  scoped_wave2_import_ready_preview_count: 197
  scoped_wave2_repair_queue_count: 636
  scoped_wave2_coordinate_downloads_performed: 0
  scoped_wave2_disk_free_gib_at_end: 8.573
  import_review_preflight: artifacts/v3_external_import_review_preflight_size120_current702_20260616_run1403.json
  import_review_ready_preview: artifacts/v3_external_import_review_ready_preview_size120_current702_20260616_run1403.json
  import_review_repair_queue: artifacts/v3_external_import_review_repair_queue_size120_current702_20260616_run1403.json
  controlled_import_review_ready_rows: 197
  import_review_repair_rows: 636
  import_review_coordinate_blockers: 473
  import_review_locator_blockers: 121
  import_review_current702_duplicates: 13
  import_review_external_duplicates: 27
  import_review_hard_blockers: 2
  frozen_current702_unchanged: true

honest_counters:
  external_rows: 8026
  external_seed: 6802
  external_positive_bronze: 6772
  external_oos_bronze: 1224
  external_silver: 30
  combined_label_surface: 8728
  combined_seed_surface: 7032
  positive_bronze: 6985
  oos_bronze: 1696
  silver_confirmed: 47
  projected: 0

planning_refresh:
  coverage_combined: 8728
  coverage_fingerprint_gini: 0.1779
  coverage_holes: []
  coverage_over_cap:
    - metal_dependent_hydrolase
  floor_deficit_total: 0
  novelty_replay:
    admit: 7565
    throttle: 414
    reject: 47
  ready_existing_lanes_ge_150: 0
  top_projected_clean_admits: 77

post_pde_source_strategy_refresh:
  breadth_feasibility_artifact: artifacts/v3_breadth_feasibility_scout_current702_20260616_run1302_post_pde_apply.json
  reviewed_swissprot_clean_families: 14
  estimated_new_clean_positive_bronze: 2641
  projected_positive_bronze_clean_only: 9673
  gap_to_10k_positive_bronze: 327
  verdict: ten_k_diverse_positive_bronze_NOT_reachable_from_reviewed_swissprot_alone
  external_bulk_ingestion_scout_attempt: size30_interrupted_no_artifact_then_size5_succeeded_provisional_no_import
  external_bulk_ingestion_scout_artifact: artifacts/v3_external_bulk_ingestion_scout_current702_20260616_run1302_post_pde_apply_size5.json
  external_bulk_ingestion_import_preview_artifact: artifacts/v3_external_bulk_ingestion_import_preview_current702_20260616_run1302_post_pde_apply_size5.json
  external_bulk_ingestion_candidate_rows: 35
  external_bulk_ingestion_provisional_import_preview_rows: 10
  external_bulk_ingestion_countable_import_authorized: false
  external_bulk_ingestion_required_lane: ce-external-admission-16-validation
  strategy_artifact: artifacts/v3_post_pde_source_tier_strategy_current702_20260616_run1302.json

validation:
  baseline_validate: passed: 12 source records, 46 fingerprints, 43 ontology families, 702 curated labels
  baseline_focused: 308 passed, 14 subtests
  source_admission_fix_focus: 232 passed, 14 subtests
  full_suite_after_wave2: passed: 2364 passed, 1 warning, 244 subtests
  final_validate: passed: 12 source records, 46 fingerprints, 43 ontology families, 702 curated labels
  final_focused: passed: 15 passed
  full_suite: passed: 2364 passed, 1 warning, 244 subtests
  json_parse: passed: 10163 JSON files
  jsonl_parse: passed: 27 JSONL files, 8247 lines
  file_size_scan: passed: data/registries plus current-run artifacts under 45 MB
  final_scope_audit: passed: no staged size10/size30/size60 intermediates; 667 locator sidecars staged
  diff_check: passed

artifacts:
  - artifacts/v3_coverage_redundancy_audit_current702_20260616_run1403_pre_lane.json
  - artifacts/v3_novelty_admission_gate_audit_current702_20260616_run1403_pre_lane.json
  - artifacts/v3_high_yield_family_lane_factory_current702_20260616_run1403_pre_lane.json
  - artifacts/v3_external_source_admission_validation_10_current702_20260616_run1403_post_pde_bulk_size5.json
  - artifacts/v3_external_source_admission_ready_preview_10_current702_20260616_run1403_post_pde_bulk_size5.json
  - artifacts/v3_external_bulk_ingestion_scout_current702_20260616_run1403_size120.json
  - artifacts/v3_external_bulk_ingestion_import_preview_current702_20260616_run1403_size120.json
  - artifacts/v3_external_source_admission_validation_431_current702_20260616_run1403_bulk_size120.json
  - artifacts/v3_external_source_admission_ready_preview_431_current702_20260616_run1403_bulk_size120.json
  - artifacts/v3_external_materialization_wave2_size120_current702_20260616_run1403.json
  - artifacts/v3_external_materialization_wave2_size120_import_ready_preview_current702_20260616_run1403.json
  - artifacts/v3_external_materialization_wave2_size120_repair_queue_current702_20260616_run1403.json
  - artifacts/v3_external_import_review_preflight_size120_current702_20260616_run1403.json
  - artifacts/v3_external_import_review_ready_preview_size120_current702_20260616_run1403.json
  - artifacts/v3_external_import_review_repair_queue_size120_current702_20260616_run1403.json

next_action: >
  Do not import directly from these artifacts. Run label-factory/novelty/governor/row-guardrail/
  leakage gates on the 197 controlled-review-ready rows and require explicit production
  authorization before any external-registry-only apply. Separately, restore disk free above 10 GiB
  and continue coordinate materialization for the 636 repair rows.
