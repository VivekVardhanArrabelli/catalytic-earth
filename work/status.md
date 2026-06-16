automation: ce-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-16T13:02:12Z
started_local: Tue Jun 16 08:02:12 CDT 2026
closeout_at: 2026-06-16T13:41:26Z
elapsed_minutes: 39.2
remaining_minutes: 15.8
budget_minutes: 55
planned_closeout_minute: 50

state: final_validation_passed_ready_to_commit_push_release
lock: reacquired by this run at 2026-06-16T13:24:06Z after unexpected unlock
branch: main
base_at_start: ebc1aad2972e94398f7345ccde8b0c0c0e15cd2e
registry_mutation: external_bronze_append_only_then_reaction_cap_surplus_correction
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

pde_apply_summary:
  source_lane: strict GDPD/cyclic source-tier-2 local slices
  component_fetched_candidate_rows: 240
  component_target_mechanism_corroborated: 118
  combined_unique_candidate_labels: 118
  combined_novelty_admitted_before_reaction_cap: 116
  novelty_throttled_or_rejected: 2
  reaction_aware_cap_trimmed: 16
  applied_labels_after_trim: 100
  row_guardrail_problem_rows: 0
  external_rows_before_apply: 7926
  transient_external_rows_before_surplus_correction: 8042
  surplus_rows_removed: 16
  external_rows_after_correction: 8026
  pde_rows_after_correction: 100
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
  baseline_focused: 351 passed, 14 subtests
  post_apply_validate: passed: 12 source records, 46 fingerprints, 43 ontology families, 702 curated labels
  post_apply_focused: 383 passed, 14 subtests
  full_suite: 2363 passed, 1 warning, 244 subtests passed in 171.07s
  json_parse: passed: 9481 JSON files
  jsonl_parse: passed: 27 JSONL files, 8240 lines
  file_size_scan: passed: no data/registries file over 45 MB
  diff_check: passed

artifacts:
  - artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_local_slice_offset30_size30_current702_20260616_run1302.json
  - artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_local_slice_offset60_size30_current702_20260616_run1302.json
  - artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_local_slice_offset90_size30_current702_20260616_run1302.json
  - artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_combined_local_slice_preview_current702_20260616_run1302.json
  - artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_combined_local_slice_preview_governor_current702_20260616_run1302.json
  - artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_reaction_cap_trimmed_preview_current702_20260616_run1302.json
  - artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_reaction_cap_trimmed_row_guardrail_audit_current702_20260616_run1302.json
  - artifacts/v3_metal_independent_phosphodiesterase_reaction_cap_surplus_registry_correction_current702_20260616_run1302.json
  - artifacts/v3_coverage_redundancy_audit_current702_20260616_run1302_post_pde_apply.json
  - artifacts/v3_novelty_admission_gate_audit_current702_20260616_run1302_post_pde_apply.json
  - artifacts/v3_high_yield_family_lane_factory_current702_20260616_run1302_post_pde_apply.json
  - artifacts/v3_breadth_feasibility_scout_current702_20260616_run1302_post_pde_apply.json
  - artifacts/v3_post_pde_source_tier_strategy_current702_20260616_run1302.json
  - artifacts/v3_external_bulk_ingestion_scout_current702_20260616_run1302_post_pde_apply_size5.json
  - artifacts/v3_external_bulk_ingestion_import_preview_current702_20260616_run1302_post_pde_apply_size5.json

next_action: >
  Do not pad PDE or any balanced/reaction-saturated lane. All positive fingerprint holes are now
  closed. Use the post-PDE coverage/governor/factory state to design the next high-yield source-tier
  or source-handle expansion. A size-5 external bulk scout found 10 provisional import-preview rows;
  validate those through the admission gate before any countable import. Then run non-destructive
  preview, row guardrail audit, novelty/governor/dedup/cap replay, leakage/source-contract tests,
  and explicit apply only if a meaningful clean batch passes.
