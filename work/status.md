automation: ce-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-15T18:39:03Z
started_local: Mon Jun 15 13:39:03 CDT 2026
closeout_at: 2026-06-15T19:29:22Z
elapsed_minutes: 50.3
remaining_minutes: 4.7
budget_minutes: 55
planned_closeout_minute: 50

state: metal-independent phosphodiesterase 43fp infrastructure built; registry unchanged
lock: held by this run until post-push release
branch: main
base_at_start: 45be297288793783d0b8083d19d4323d628d9a71

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

pde_43fp_summary:
  current_positive_universe: label_factory_v1_43fp
  mechanism_fingerprints: 43
  ontology_families: 40
  registry_mutation: none
  reviewed_preview_fetched_rows: 265
  reviewed_preview_target_labels: 18
  reviewed_preview_novelty_admitted: 14
  alternate_reviewed_preview_fetched_rows: 130
  alternate_reviewed_preview_novelty_admitted: 0
  tier2_preview_fetched_rows: 400
  tier2_preview_target_labels: 0
  tier2_preview_novelty_admitted: 0
  tier2_trust_holds: 197
  apply_authorized: false

planning_refresh:
  coverage_combined: 8272
  coverage_fingerprint_gini: 0.1974
  coverage_holes:
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
  cli_validate: passed: 12 source records, 43 fingerprints, 40 ontology families, 702 curated labels
  focused_affected: 350 passed in 3.15s
  failed_pin_rerun_after_update: 2 passed in 0.38s
  full_suite_final: 2326 passed, 1 warning in 165.71s
  progress_and_doc_reference: 5 passed
  diff_check: passed
  json_parse: passed for progress log and 15 new/current JSON artifacts
  file_size_scan: passed: manifest 1.2K; shards 17M, 17M, 17M, 5.9M
  frozen_sha: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
  preregistration_consistency: passed: 43 live fingerprints match 43fp artifact

next_action: Design sharper PDE source splits or pivot to a higher-yield source-tier/family strategy such as SDR/AKR; do not apply the 14-row PDE preview.
