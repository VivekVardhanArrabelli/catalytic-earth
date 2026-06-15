automation: ce-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-15T22:13:48Z
started_local: Mon Jun 15 17:13:49 CDT 2026
closeout_at: 2026-06-15T22:58:46Z
elapsed_minutes: 45.0
remaining_minutes: 10.0
budget_minutes: 55
planned_closeout_minute: 50

state: ready_to_commit_push_and_release_lock
lock: held by this run until post-push release
branch: main
base_at_start: 5e7c1006e7f4a0438bc3bc4943eedd78acded89f
current_run_focus: >
  Closed the high-yield SDR source-handle lane through the mechanism-first gated path after
  documented PDE source walls remained subscale. No frozen current702 rows were written.

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

sdr_45fp_apply_summary:
  current_positive_universe: label_factory_v1_45fp
  mechanism_fingerprints: 45
  ontology_families: 42
  registry_mutation: external_bronze_append_only
  source_family: short_chain_dehydrogenase_reductase
  preview_fetched_rows: 220
  preview_target_labels: 103
  preview_novelty_admitted: 100
  preview_off_target_held: 0
  preview_held_at_cap: 0
  row_guardrail_problem_rows: 0
  source_tier: source_tier_0
  required_non_ec_mechanism_axes: 3
  predictive_evidence_empty: true
  external_rows_before: 7720
  external_rows_after: 7820
  combined_label_surface_after: 8522
  frozen_sha_before: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
  frozen_sha_after: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

planning_refresh:
  coverage_combined: 8522
  coverage_fingerprint_gini: 0.1944
  coverage_holes:
    - metal_independent_phosphodiesterase
  coverage_over_cap:
    - metal_dependent_hydrolase
  novelty_replay:
    admit: 7359
    throttle: 414
    reject: 47
  ready_existing_lanes_ge_150: 0
  top_projected_clean_admits: 77
  mechanism_representation_loop:
    leave_one_out_self_consistency: 0.7576
    sdr_self_consistency: 0.95
    note: generic_nad_p_dehydrogenase_sdr_reaction_chemistry_ceiling_documented

validation:
  cli_validate: passed: 12 source records, 45 fingerprints, 42 ontology families, 702 curated labels
  focused_sdr_leakage_import_suite: 106 passed in 0.18s
  targeted_stale_invariant_rerun: 6 passed in 23.44s
  full_suite_final: 2346 passed, 1 warning, 244 subtests passed in 166.99s
  compileall: passed
  json_parse: passed
  jsonl_parse: passed
  progress_and_doc_reference: 5 passed
  diff_check: passed after doc closeout
  frozen_sha: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
  file_size_scan: passed: manifest 4K; shards 17M, 17M, 17M, 7.4M; curated 500K

artifacts:
  sdr_preview: artifacts/v3_short_chain_dehydrogenase_reductase_sourcing_preview_named220_current702_20260615_run2213.json
  sdr_preview_report: work/short_chain_dehydrogenase_reductase_sourcing_preview_named220_current702_20260615_run2213.md
  sdr_row_guardrail: artifacts/v3_short_chain_dehydrogenase_reductase_row_guardrail_audit_current702_20260615_run2213.json
  oos_preregistration_45fp: artifacts/v3_external_hard_negative_next_tranche_preregistration_45fp_1025.json
  coverage: artifacts/v3_coverage_redundancy_audit_current702_20260615_run2213_post_sdr_apply.json
  novelty: artifacts/v3_novelty_admission_gate_audit_current702_20260615_run2213_post_sdr_apply.json
  factory: artifacts/v3_high_yield_family_lane_factory_current702_20260615_run2213_post_sdr_apply.json
  mechanism_representation: artifacts/v3_mechanism_representation_loop_current702_20260615_run2213_post_sdr_apply.json
  bronze_silver: artifacts/v3_bronze_silver_promotion_preview_current702_20260615_run2213_post_sdr_apply.json
  family_set_targets: artifacts/v3_family_set_expansion_targets_current702_20260615_run2213_post_sdr_apply.json

next_action: >
  Do not source more SDR, APH, or retry the same PDE EC/name windows. The only current hole is
  metal_independent_phosphodiesterase; build a materially sharper mechanism-bearing PDE source wall
  beyond EC/name counts, or pivot to a new high-yield family/source-tier strategy. Any mutation
  must go through OOS preregistration if the fingerprint universe changes, non-destructive preview,
  row audit, novelty/governor/dedup/cap replay, leakage/source-contract validation, and explicit
  apply only if the clean batch gate is met.
