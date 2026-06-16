automation: ce-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-16T12:07:30Z
started_local: Tue Jun 16 07:07:30 CDT 2026
closeout_at: 2026-06-16T12:56:08Z
elapsed_minutes: 48.6
remaining_minutes: 6.4
budget_minutes: 55
planned_closeout_minute: 50

state: final_validation_passed_ready_to_commit_push_release
lock: held by this run until post-push release
branch: main
base_at_start: cd04a5fcaac9c97aa3050736878f78128e172bf5
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

safety_recovery:
  dead_lock_started_at: 2026-06-16T05:32:47Z
  stale_pde_workers_terminated: true
  incomplete_size120_tier2_fetch_terminated: true
  incomplete_size120_artifact_written: false
  unauthorized_external_append_detected: 17 metal_independent_phosphodiesterase rows
  unauthorized_external_append_reverted: true
  external_rows_after_revert: 7926
  frozen_current702_unchanged: true

honest_counters:
  external_rows: 7926
  external_seed: 6702
  external_positive_bronze: 6672
  external_oos_bronze: 1224
  external_silver: 30
  combined_label_surface: 8628
  combined_seed_surface: 6932
  positive_bronze: 6885
  oos_bronze: 1696
  silver_confirmed: 47
  projected: 0

pde_run1207_summary:
  hydrolase_reviewed_preview:
    fetched_candidate_rows: 120
    target_mechanism_corroborated: 17
    novelty_admitted: 17
    off_target_held: 22
    disambiguation_holds: 69
    row_guardrail_problem_rows: 0
    apply_authorized: false
    no_apply_reason: 17 rows would leave PDE at 17/100; tiny topup is not floor-closing
  strict_tier2_sample:
    fetched_candidate_rows: 40
    target_mechanism_corroborated: 0
    novelty_admitted: 0
    off_target_held: 6
    mechanism_or_trust_holds: 34
    apply_authorized: false
  actsite_catalytic_preview:
    fetched_candidate_rows: 40
    target_mechanism_corroborated: 2
    novelty_admitted: 2
    off_target_held: 4
    disambiguation_holds: 23
    row_guardrail_problem_rows: 0
    apply_authorized: false
  tier2_gdpd_cyclic_preview:
    fetched_candidate_rows: 60
    target_mechanism_corroborated: 28
    novelty_admitted: 28
    off_target_held: 0
    disambiguation_holds: 32
    row_guardrail_problem_rows: 0
    apply_authorized: false
  sharp_handle_count_scout:
    best_baseline_handle: broad_ec314_hydrolase_non_metal
    baseline_reviewed_rows: 490
    best_sharp_nonbaseline_handle: actsite_catalytic_non_metal
    best_sharp_reviewed_rows: 119
    handles_with_count_ge_150: 1
    apply_authorized: false
  strict_tier2_gdpd_cyclic_preview:
    fetched_candidate_rows: 60
    target_mechanism_corroborated: 28
    novelty_admitted: 28
    off_target_held: 0
    mechanism_or_trust_holds: 32
    row_guardrail_problem_rows: 0
    projected_pde_after: 28
    deficit_to_floor_after: 72
    apply_authorized: false
    no_apply_reason: 28 rows would leave PDE at 28/100; tiny topup is not floor-closing

planning_refresh:
  coverage_combined: 8628
  coverage_fingerprint_gini: 0.1948
  coverage_holes:
    - metal_independent_phosphodiesterase
  coverage_over_cap:
    - metal_dependent_hydrolase
  floor_deficit_total: 100
  novelty_replay:
    admit: 7465
    throttle: 414
    reject: 47
  ready_existing_lanes_ge_150: 0
  top_projected_clean_admits: 77
  reviewed_swissprot_clean_only_positive_projection: 9573
  reviewed_swissprot_positive_gap_to_10k: 427

validation:
  baseline_validate: passed: 12 source records, 46 fingerprints, 43 ontology families, 702 curated labels
  baseline_focused: 128 passed
  compileall_after_source_fix: passed
  focused_after_source_fix: 128 passed
  final_validate: passed: 12 source records, 46 fingerprints, 43 ontology families, 702 curated labels
  final_focused: 267 passed, 14 subtests passed in 2.10s
  json_parse: passed: 9455 JSON files
  jsonl_parse: passed: 27 JSONL files, 8217 lines
  file_size_scan: passed: no data/registries file over 45 MB
  diff_check: passed
  full_suite: 2363 passed, 1 warning, 244 subtests passed in 180.85s
  frozen_sha: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

artifacts:
  - artifacts/v3_coverage_redundancy_audit_current702_20260616_run0114_pre_lane.json
  - artifacts/v3_novelty_admission_gate_audit_current702_20260616_run0114_pre_lane.json
  - artifacts/v3_high_yield_family_lane_factory_current702_20260616_run0114_pre_lane.json
  - artifacts/v3_metal_independent_phosphodiesterase_ec314_hydrolase_preview_window0_120_current702_20260616_run0114.json
  - artifacts/v3_metal_independent_phosphodiesterase_ec314_hydrolase_preview_window120_120_current702_20260616_run0114.json
  - artifacts/v3_metal_independent_phosphodiesterase_ec314_hydrolase_row_guardrail_audit_current702_20260616_run0114.json
  - artifacts/v3_metal_independent_phosphodiesterase_ec314_hydrolase_source_strategy_current702_20260616_run0114.json
  - artifacts/v3_metal_independent_phosphodiesterase_tier2_preview_size20_current702_20260616_run1209.json
  - artifacts/v3_metal_independent_phosphodiesterase_actsite_catalytic_preview_size40_current702_20260616_run1218.json
  - artifacts/v3_metal_independent_phosphodiesterase_actsite_catalytic_row_guardrail_audit_current702_20260616_run1218.json
  - artifacts/v3_metal_independent_phosphodiesterase_actsite_catalytic_source_strategy_current702_20260616_run1218.json
  - artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_preview_size30_current702_20260616_run1235.json
  - artifacts/v3_metal_independent_phosphodiesterase_tier2_gdpd_cyclic_row_guardrail_audit_current702_20260616_run1235.json
  - artifacts/v3_coverage_redundancy_audit_current702_20260616_run1209_post_tier2_scout.json
  - artifacts/v3_novelty_admission_gate_audit_current702_20260616_run1209_post_tier2_scout.json
  - artifacts/v3_high_yield_family_lane_factory_current702_20260616_run1209_post_tier2_scout.json
  - artifacts/v3_breadth_feasibility_scout_current702_20260616_run1209_post_tier2_scout.json
  - artifacts/v3_metal_independent_phosphodiesterase_sharp_handle_count_scout_current702_20260616_run1207.json

next_action: >
  Do not apply the 17-row PDE hydrolase preview, the 2-row active-site catalytic preview, the
  28-row GDPD/cyclic tier-2 preview, or retry the same broad reviewed EC/name/PLD/hydrolase/ACT_SITE
  windows. The next safe scaleout step is a stable, paginated GDPD/cyclic tier-2 source window or
  a genuinely sharper metal_independent_phosphodiesterase source wall that can close the 100 floor,
  with row audit, novelty/governor/dedup/cap replay, leakage/source-contract tests, and explicit
  apply only if the batch gate passes.

no_apply_reason: >
  The clean previews remained subfloor: Hydrolase 17, ACT_SITE 2, strict tier-2 0, and GDPD/cyclic
  28. A larger GDPD/cyclic size-120 preview was attempted after the 28-row scout but terminated by
  SIGTERM before writing an artifact, so it is not evidence and was not applied. External registry
  append attempts from stale workers were reverted to the SBL baseline; frozen current702 stayed
  unchanged.

early_closeout_reason: >
  Safe mutation paths were concretely blocked before minute 50: every completed PDE preview stayed
  below the 100-row floor, the only plausible larger GDPD/cyclic tier-2 fetch did not produce an
  artifact safely in this run, existing reviewed PDE windows are exhausted or boundary-heavy, and
  the current factory/governor state has 0 ready existing lanes >=150.
