automation: ce-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-15T21:13:19Z
started_local: Mon Jun 15 16:13:19 CDT 2026
closeout_at: 2026-06-15T21:46:55Z
elapsed_minutes: 33.6
remaining_minutes: 21.4
budget_minutes: 55
planned_closeout_minute: 50

state: ready_to_commit_push_and_release_lock
lock: held by this run until post-push release
branch: main
base_at_start: f60617d6a1492cdf264689cdf3216bd428425250
early_closeout_reason: >
  APH closed cleanly at cap; the only remaining hole is PDE, and reviewed, alternate, tier-2,
  exact-EC, and broad-name PDE source paths are all blocked below the clean batch gate or
  boundary-heavy. The remaining high-yield work requires a new source-wall/OOS design, not a safe
  same-run registry apply.

honest_counters:
  external_rows: 7720
  external_seed: 6496
  external_positive_bronze: 6466
  external_oos_bronze: 1224
  external_silver_confirmed: 30
  combined_label_surface: 8422
  combined_seed_surface: 6726
  positive_bronze: 6679
  oos_bronze: 1696
  silver_confirmed: 47
  projected: 0

aph_tier2_apply_summary:
  current_positive_universe: label_factory_v1_44fp
  mechanism_fingerprints: 44
  ontology_families: 41
  registry_mutation: external_bronze_append_only
  preview_fetched_rows: 240
  preview_target_labels: 239
  preview_novelty_admitted: 150
  preview_novelty_throttled: 19
  preview_held_at_cap: 70
  row_guardrail_problem_rows: 0
  source_tier: source_tier_2
  required_non_ec_mechanism_axes: 3
  predictive_evidence_empty: true
  external_rows_before: 7570
  external_rows_after: 7720
  combined_label_surface_after: 8422
  frozen_sha_before: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
  frozen_sha_after: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

planning_refresh:
  coverage_combined: 8422
  coverage_fingerprint_gini: 0.1944
  coverage_holes:
    - metal_independent_phosphodiesterase
  coverage_over_cap:
    - metal_dependent_hydrolase
  novelty_replay:
    admit: 7259
    throttle: 414
    reject: 47
  ready_existing_lanes_ge_150: 0
  top_projected_clean_admits:
    family: short_chain_dehydrogenase_reductase
    count: 84

post_aph_source_strategy:
  pde_reviewed_preview_novelty_admitted: 14
  pde_alternate_reviewed_preview_novelty_admitted: 0
  pde_tier2_preview_novelty_admitted: 0
  pde_exact_ec_largest_cyclic_split_after_non_metal_filter: 18
  pde_exact_ec_broad_non_metal_count: 490
  evidence_handle_families_probed: 6
  evidence_handle_unlocked_families: 4
  evidence_handle_reachable_positive_bronze_uplift: 741

validation:
  cli_validate: passed: 12 source records, 44 fingerprints, 41 ontology families, 702 curated labels
  focused_critical_after_code_changes: 97 passed
  full_suite_after_code_changes: 2337 passed, 1 warning, 244 subtests passed in 169.68s
  compileall: passed
  progress_and_doc_reference: 5 passed
  json_parse: passed: 9394 JSON files checked
  jsonl_parse: passed: 27 JSONL files, 8206 lines checked
  diff_check: passed
  frozen_sha: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
  file_size_scan: passed: manifest 1.2K; shards 17M, 17M, 17M, 6.7M; curated 496K

artifacts:
  aph_preview: artifacts/v3_aminoglycoside_phosphotransferase_tier2_sourcing_preview_cursor_pages3_size80_current702_20260615.json
  aph_preview_report: work/aminoglycoside_phosphotransferase_tier2_sourcing_preview_cursor_pages3_size80_current702_20260615.md
  aph_row_guardrail: artifacts/v3_aminoglycoside_phosphotransferase_tier2_row_guardrail_audit_current702_20260615.json
  coverage: artifacts/v3_coverage_redundancy_audit_current702_20260615_post_aph_tier2_apply.json
  novelty: artifacts/v3_novelty_admission_gate_audit_current702_20260615_post_aph_tier2_apply.json
  factory: artifacts/v3_high_yield_family_lane_factory_current702_20260615_post_aph_tier2_apply.json
  bronze_silver: artifacts/v3_bronze_silver_promotion_preview_current702_20260615_post_aph_tier2_apply.json
  mechanism_representation: artifacts/v3_mechanism_representation_loop_current702_20260615_post_aph_tier2_apply.json
  pde_strategy: artifacts/v3_metal_independent_phosphodiesterase_post_aph_source_strategy_current702_20260615.json
  pde_exact_ec_scout: artifacts/v3_metal_independent_phosphodiesterase_exact_ec_distribution_scout_current702_20260615_post_aph_apply.json
  evidence_handle_scout: artifacts/v3_evidence_handle_expansion_current702_20260615_post_aph_apply.json

next_action: >
  Do not source more APH or retry the same PDE EC/name windows. Build a new mechanism-bearing PDE
  source wall beyond EC/name counts, or pivot to a split high-yield source-tier/family strategy
  such as SDR/AKR or serine beta-lactamase. Any mutation must go through OOS preregistration if the
  fingerprint universe changes, non-destructive preview, row audit, novelty/governor/dedup/cap
  replay, leakage/source-contract validation, and explicit apply only if the clean batch gate is
  met.
