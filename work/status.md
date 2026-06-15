automation: ce-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-15T23:14:13Z
started_local: Mon Jun 15 18:14:13 CDT 2026
closeout_at: 2026-06-15T23:37:38Z
elapsed_minutes: 23.4
remaining_minutes: 31.6
budget_minutes: 55
planned_closeout_minute: 50

state: ready_to_commit_push_and_release_lock
lock: held by this run until post-push release
branch: main
base_at_start: a4c86f131f0bbbfae38b3c7e309942009aa49311
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_no_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
early_closeout_reason: >
  Safe mutation paths were concretely blocked: PDE PLD produced only 7 novelty-safe rows,
  terpene cap-close window170 produced 0 novelty-safe rows, current balanced/capped families
  must not be padded, and serine beta-lactamase requires new fingerprint/OOS/source-runner
  work before any preview/apply authority.

honest_counters:
  external_rows: 7820
  external_seed: 6596
  external_positive_bronze: 6566
  external_oos_bronze: 1224
  external_silver_confirmed: 30
  combined_label_surface: 8522
  combined_seed_surface: 6826
  positive_bronze: 6779
  oos_bronze: 1696
  silver_confirmed: 47
  projected: 0

run2314_summary:
  pde_pld_fetched_rows: 22
  pde_pld_target_labels: 7
  pde_pld_novelty_admitted: 7
  pde_pld_row_guardrail_problem_rows: 0
  terpene_window_fetched_rows: 138
  terpene_window_target_labels: 7
  terpene_window_novelty_admitted: 0
  serine_beta_lactamase_reviewed_exact_name_rows: 147
  serine_beta_lactamase_reviewed_active_site_rows: 132
  serine_beta_lactamase_tier2_active_site_reaction_rows: 1854

validation:
  cli_validate: passed: 12 source records, 45 fingerprints, 42 ontology families, 702 curated labels
  baseline_focused: 128 passed in 1.78s
  pde_terpene_factory_import_focus: 136 passed in 1.93s
  full_suite: 2348 passed, 1 warning, 244 subtests passed in 175.77s
  compileall_json_jsonl: passed
  doc_progress_reference: 5 passed
  diff_check: passed
  file_size_scan: passed: no data/registries file over 45 MB
  frozen_sha: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

artifacts:
  - artifacts/v3_coverage_redundancy_audit_current702_20260615_run2314_pre_lane.json
  - artifacts/v3_novelty_admission_gate_audit_current702_20260615_run2314_pre_lane.json
  - artifacts/v3_high_yield_family_lane_factory_current702_20260615_run2314_pre_lane.json
  - artifacts/v3_metal_independent_phosphodiesterase_phospholipase_d_preview_current702_20260615_run2314.json
  - artifacts/v3_metal_independent_phosphodiesterase_phospholipase_d_row_guardrail_audit_current702_20260615_run2314.json
  - artifacts/v3_metal_independent_phosphodiesterase_source_strategy_current702_20260615_run2314.json
  - artifacts/v3_terpene_cyclase_synthase_capclose_window170_preview_current702_20260615_run2314.json
  - artifacts/v3_evidence_handle_expansion_current702_20260615_run2314.json
  - artifacts/v3_serine_beta_lactamase_source_tier_scout_current702_20260615_run2314.json
  - artifacts/v3_serine_beta_lactamase_build_plan_current702_20260615_run2314.json

reports:
  - work/coverage_redundancy_audit_current702_20260615_run2314_pre_lane.md
  - work/novelty_admission_gate_audit_current702_20260615_run2314_pre_lane.md
  - work/high_yield_family_lane_factory_current702_20260615_run2314_pre_lane.md
  - work/metal_independent_phosphodiesterase_phospholipase_d_preview_current702_20260615_run2314.md
  - work/metal_independent_phosphodiesterase_phospholipase_d_row_guardrail_audit_current702_20260615_run2314.md
  - work/metal_independent_phosphodiesterase_source_strategy_current702_20260615_run2314.md
  - work/terpene_cyclase_synthase_capclose_window170_preview_current702_20260615_run2314.md
  - work/evidence_handle_expansion_current702_20260615_run2314.md
  - work/serine_beta_lactamase_source_tier_scout_current702_20260615_run2314.md
  - work/serine_beta_lactamase_build_plan_current702_20260615_run2314.md

next_action: >
  Do not apply the 7-row PLD preview, do not retry terpene window170, and do not reuse broad
  PDE EC/name handles. Next safe scaling is a sharper mechanism-bearing PDE split capable of
  closing the 100 floor, or the guarded serine_beta_lactamase lane from the build plan if PDE
  remains blocked: add fingerprint/ontology/OOS/source runner, preview, row-audit, replay gates,
  and validate before any apply.
