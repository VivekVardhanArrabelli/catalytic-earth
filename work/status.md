automation: ce-autonomous-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-16T23:06:35Z
started_local: Tue Jun 16 18:06:35 CDT 2026
closeout_at: 2026-06-16T23:54:45Z
elapsed_minutes: 48.2
remaining_minutes: 6.8
budget_minutes: 55
planned_closeout_minute: 50

state: run2306_q6nsj0_p55263_source_transfer_replay_held_no_apply
lock: acquired by this run at 2026-06-16T23:06:35Z
branch: main
origin_main_at_start: 490eb6856a77478b730a7642589f867c18b6ff84
origin_main_before_push: 490eb6856a77478b730a7642589f867c18b6ff84
base_at_start: 490eb6856a77478b730a7642589f867c18b6ff84
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

validation:
  registry_validate: passed
  baseline_critical_suite: 494 passed, 160 subtests
  focused_transfer_cli_suite: 367 passed, 160 subtests
  full_pytest: 2392 passed, 1 warning, 244 subtests
  compileall: passed
  git_diff_check: passed
  docs_reference_check: 0 missing / 2118 checked / 14 ignored
  json_jsonl_parse: passed
  hard_limit_scan_over_90mb: none
  artifact_storage_policy: blocked: 44 large-unclassified artifacts, 0 deletions authorized
  artifact_migration_dry_run: passed: 116 rows, removal_allowed=0
  github_fetch_push: fetch passed; push pending at status write

coverage_state:
  combined_labels: 8728
  frozen_rows: 702
  expansion_rows: 8026
  positive_holes: 0
  floor_deficit: 0
  novelty_replay: 7565 admit / 414 throttle / 47 reject
  over_cap: metal_dependent_hydrolase
  ready_existing_lanes_ge150: 0
  top_projected_clean_admits: 77

work_completed:
  - completed current-slice Q6NSJ0 needs_review, review-resolved, and repair-lane routing
  - adjudicated Q6NSJ0 glycoside boundary control; held it as incomplete / not repaired
  - merged Q6NSJ0 with historical P33025 glycoside adjudication; both remain not repaired
  - fixed glycoside import-safety duplicate-state precedence so later UniRef/current-reference no-overlap clears stale broader-duplicate blockers
  - added non-authorizing manual source-mechanism review packet CLI with optional matched representation-stability evidence
  - routed P55263 through the stability-enriched manual packet; matched stability row is present but nearest reference is unstable
  - reran no-fetch and live glycoside replacement scouts after Q6NSJ0 failure; no replacement selected from six remaining glycan rows
  - refreshed storage inventory, policy, producer/consumer manifest, readiness plan, and no-op migration execution dry run

key_artifacts:
  q6nsj0_needs_review: artifacts/v3_external_source_pilot_needs_review_resolution_q6nsj0_replacement_current702_20260616_run2306.json
  q6nsj0_glycoside_boundary: artifacts/v3_external_source_pilot_glycoside_hydrolase_boundary_control_q6nsj0_replacement_current702_20260616_run2306.json
  merged_glycoside_adjudication: artifacts/v3_external_source_pilot_glycoside_hydrolase_import_safety_adjudication_merged_q6nsj0_p33025_current702_20260616_run2306.json
  p55263_stability: artifacts/v3_external_source_pilot_representation_backend_stability_p55263_matched_current702_20260616_run2306.json
  p55263_manual_packet: artifacts/v3_external_source_pilot_manual_source_mechanism_review_packet_p55263_with_stability_current702_20260616_run2306.json
  final_gap_audit: artifacts/v3_external_source_pilot_review_resolution_gap_audit_q6nsj0_p55263_with_merged_glyco_import_safety_current702_20260616_run2306.json
  final_import_safety: artifacts/v3_external_source_pilot_review_resolution_gap_import_safety_q6nsj0_p55263_with_stability_packet_current702_20260616_run2306.json
  post_q6nsj0_live_scout: artifacts/v3_external_source_pilot_glycoside_hydrolase_replacement_scout_after_q6nsj0_live_current702_20260616_run2306.json
  storage_policy: artifacts/v3_artifact_storage_policy_check_current702_20260616_run2306.json
  migration_execution_manifest: artifacts/v3_artifact_migration_execution_manifest_current702_20260616_run2306.json

current_gate_state:
  final_gap_rows: 7
  review_decision_and_factory_gate_blocked_after_control_repair: 4
  family_control_unresolved_after_adjudication: 2
  manual_source_mechanism_review_required: 1
  import_ready_rows: 0
  countable_label_candidate_rows: 0
  review_only_import_safety: safe; 0 unsafe artifacts; 0 new countable labels
  q6nsj0_status: glycoside boundary incomplete; representation conflict not repaired
  p33025_status: glycoside boundary not repaired
  p55263_status: manual source-mechanism review; representation instability Q9TVW2 -> P03958
  post_q6nsj0_glycan_replacement_scout: no selected replacement; 6 scope-mismatch-or-low-priority rows

next_action: >
  Repair or replace the glycoside boundary control with source-free representation/heuristic
  evidence for Q6NSJ0/P33025, or manually resolve P55263's mechanism-control family. Do not
  apply/import until explicit review decisions, duplicate checks, family controls, full
  label-factory gates, novelty, governor, and row guardrails all pass.
