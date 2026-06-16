automation: ce-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-16T00:13:51Z
started_local: Mon Jun 15 19:13:51 CDT 2026
closeout_at: 2026-06-16T00:53:00Z
elapsed_minutes: 39.2
remaining_minutes: 15.8
budget_minutes: 55
planned_closeout_minute: 50

state: ready_to_commit_push_and_release_lock
lock: held by this run until post-push release
branch: main
base_at_start: a4c86f131f0bbbfae38b3c7e309942009aa49311
registry_mutation: external_bronze_append_only
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
early_closeout_reason: >
  SBL reached the 100 floor and is reaction-saturated; the only remaining true hole is
  metal_independent_phosphodiesterase, but existing PDE reviewed/PLD/tier-2 handles are documented
  below gate or boundary-heavy. The post-SBL high-yield factory reports 0 ready existing lanes
  >=150, and evidence-handle/breadth scouts are strategy inputs rather than apply authority.

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

sbl_run0014_summary:
  fingerprint_universe: label_factory_v1_46fp
  mechanism_fingerprints: 46
  ontology_families: 43
  source_tier: source_tier_2
  fetched_candidate_rows: 240
  target_mechanism_corroborated: 115
  novelty_admitted: 106
  off_target_held: 0
  row_guardrail_problem_rows: 0
  external_rows_before: 7820
  external_rows_after: 7926
  combined_labels_before: 8522
  combined_labels_after: 8628

post_apply_planning:
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
  evidence_handle_reachable_positive_bronze_uplift: 741
  reviewed_swissprot_clean_only_positive_projection: 9573
  reviewed_swissprot_positive_gap_to_10k: 427
  representation_loop:
    seed_labels: 6702
    leave_one_out_self_consistency: 0.7635
    serine_beta_lactamase_self_consistency: 1.0

validation:
  baseline_validate: passed: 12 source records, 45 fingerprints, 42 ontology families, 702 curated labels
  baseline_focused: 363 passed
  post_apply_validate: passed: 12 source records, 46 fingerprints, 43 ontology families, 702 curated labels
  focused_sbl_leakage_import: 156 passed
  stale_invariant_rerun: 5 passed
  full_suite: 2357 passed, 1 warning, 244 subtests passed in 169.66s
  doc_progress_reference: 5 passed
  compileall: passed
  json_jsonl_parse: passed
  file_size_scan: passed: no data/registries file over 45 MB
  diff_check: passed
  frozen_sha: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

artifacts:
  - artifacts/v3_external_hard_negative_next_tranche_preregistration_46fp_1025.json
  - artifacts/v3_serine_beta_lactamase_tier2_sourcing_preview_cursor_pages3_size80_current702_20260616_run0014.json
  - artifacts/v3_serine_beta_lactamase_tier2_row_guardrail_audit_current702_20260616_run0014.json
  - artifacts/v3_coverage_redundancy_audit_current702_20260616_run0014_pre_lane.json
  - artifacts/v3_novelty_admission_gate_audit_current702_20260616_run0014_pre_lane.json
  - artifacts/v3_high_yield_family_lane_factory_current702_20260616_run0014_pre_lane.json
  - artifacts/v3_coverage_redundancy_audit_current702_20260616_run0014_post_sbl_apply.json
  - artifacts/v3_novelty_admission_gate_audit_current702_20260616_run0014_post_sbl_apply.json
  - artifacts/v3_high_yield_family_lane_factory_current702_20260616_run0014_post_sbl_apply.json
  - artifacts/v3_mechanism_representation_loop_current702_20260616_run0014_post_sbl_apply.json
  - artifacts/v3_evidence_handle_expansion_current702_20260616_run0014_post_sbl_apply.json
  - artifacts/v3_breadth_feasibility_scout_current702_20260616_run0014_post_sbl_apply.json
  - artifacts/v3_post_sbl_source_strategy_current702_20260616_run0014.json

reports:
  - work/serine_beta_lactamase_tier2_sourcing_preview_cursor_pages3_size80_current702_20260616_run0014.md
  - work/serine_beta_lactamase_tier2_row_guardrail_audit_current702_20260616_run0014.md
  - work/coverage_redundancy_audit_current702_20260616_run0014_post_sbl_apply.md
  - work/novelty_admission_gate_audit_current702_20260616_run0014_post_sbl_apply.md
  - work/high_yield_family_lane_factory_current702_20260616_run0014_post_sbl_apply.md
  - work/mechanism_representation_loop_current702_20260616_run0014_post_sbl_apply.md
  - work/evidence_handle_expansion_current702_20260616_run0014_post_sbl_apply.md
  - work/breadth_feasibility_scout_current702_20260616_run0014_post_sbl_apply.md
  - work/post_sbl_source_strategy_current702_20260616_run0014.md

next_action: >
  Do not source more SBL without a new reaction-diversity split. Do not retry broad PDE EC/name
  handles, the 7-row PLD preview, or terpene window170. Next safe scaling is a sharper
  metal_independent_phosphodiesterase source wall capable of closing the 100 floor, or a
  source-tier expansion beyond reviewed Swiss-Prot through count scout, preregistration if needed,
  non-destructive preview, row audit, novelty/governor/dedup/cap replay, and tests before apply.
