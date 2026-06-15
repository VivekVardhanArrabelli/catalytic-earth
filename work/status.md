automation: ce-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-15T19:40:17Z
started_local: Mon Jun 15 14:40:17 CDT 2026
closeout_at: 2026-06-15T20:55:19Z
elapsed_minutes: 75.0
remaining_minutes: -20.0
budget_minutes: 55
planned_closeout_minute: 50

state: ready to commit, push, and release lock
lock: held by this run until post-push release
branch: main
base_at_start: eccb5125746353377b5d4d00a2a4aca38d7c6f08

honest_counters:
  external_rows: 7570
  external_seed: 6346
  external_positive_bronze: 6316
  external_oos_bronze: 1224
  external_silver_confirmed: 30
  combined_label_surface: 8272
  combined_seed_surface: 6576
  positive_bronze: 6529
  oos_bronze: 1696
  silver_confirmed: 47
  projected: 0

aph_44fp_summary:
  current_positive_universe: label_factory_v1_44fp
  mechanism_fingerprints: 44
  ontology_families: 41
  registry_mutation: none
  exact_ec_scope_corrected:
    removed_false_scopes:
      - 2.7.1.130
      - 2.7.1.192
    retained_aph_scopes:
      - 2.7.1.95
      - 2.7.1.72
      - 2.7.1.87
      - 2.7.1.119
      - 2.7.1.163
  corrected_preview_fetched_rows: 18
  corrected_preview_target_labels: 17
  corrected_preview_novelty_admitted: 17
  corrected_preview_off_target_held: 0
  apply_authorized: false
  no_apply_reason: below_150_clean_admit_batch_gate

planning_refresh:
  coverage_combined: 8272
  coverage_fingerprint_gini: 0.2156
  coverage_holes:
    - aminoglycoside_phosphotransferase
    - metal_independent_phosphodiesterase
  coverage_over_cap:
    - metal_dependent_hydrolase
  novelty_replay:
    admit: 7109
    throttle: 414
    reject: 47
  ready_existing_lanes_ge_150: 0
  top_projected_clean_admits:
    family: short_chain_dehydrogenase_reductase
    count: 84

validation:
  cli_validate: passed: 12 source records, 44 fingerprints, 41 ontology families, 702 curated labels
  focused_critical_final: 433 passed, 14 subtests passed in 2.94s
  aph_factory_leakage_focus_after_ec_correction: 302 passed, 14 subtests passed
  file_size_scan: passed: manifest 4K; shards 17M, 17M, 17M, 5.9M; curated 500K
  registry_mutation: none

artifacts:
  preregistration_44fp: artifacts/v3_external_hard_negative_next_tranche_preregistration_44fp_1025.json
  aph_preview: artifacts/v3_aminoglycoside_phosphotransferase_sourcing_preview_corrected_active_binding_bounded50_current702_20260615.json
  aph_preview_report: work/aminoglycoside_phosphotransferase_sourcing_corrected_active_binding_bounded50_current702_20260615.md
  factory: artifacts/v3_high_yield_family_lane_factory_current702_20260615_post_aph_44fp_infra.json
  coverage: artifacts/v3_coverage_redundancy_audit_current702_20260615_post_aph_44fp_infra.json
  novelty: artifacts/v3_novelty_admission_gate_audit_current702_20260615_post_aph_44fp_infra.json

next_action: Do not apply the 17-row APH preview. Pivot to a higher-yield mechanism-first source strategy such as SDR/AKR or another source tier/family that can plausibly clear >=150 clean admits.
