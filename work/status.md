automation: ce-autonomous-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-16T22:05:40Z
started_local: Tue Jun 16 17:05:40 CDT 2026
closeout_at: 2026-06-16T22:52:19Z
elapsed_minutes: 46.7
remaining_minutes: 8.3
budget_minutes: 55
planned_closeout_minute: 50

state: run2205_q6nsj0_replacement_packet_review_only_pre_push
lock: acquired by this run at 2026-06-16T22:05:40Z
branch: main
origin_main_at_start: e399887446677b2c47c0b72564d634842d357b4d
base_at_start: e399887446677b2c47c0b72564d634842d357b4d
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

validation:
  registry_validate: passed
  baseline_critical_suite: passed
  focused_critical_suite: 608 passed, 174 subtests
  full_pytest: 2390 passed, 1 warning, 244 subtests
  compileall: passed
  git_diff_check: passed
  docs_reference_check: 0 missing / 2094 checked / 14 ignored
  hard_limit_scan_over_90mb: none
  artifact_storage_policy: blocked by 43 large-unclassified artifacts; 0 deletion-authorized; 0 migration-ready
  github_fetch_push: fetch_ok_push_pending

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
  - selected Q6NSJ0 as the review-only glycoside replacement for failed P33025 boundary control
  - added pinned source-transfer pilot priority support and downstream selected-row handling
  - generated Q6NSJ0 review export, evidence packet, evidence dossier, active-site decisions, representation plan/sample/stability/adjudication, success criteria, terminal decisions, confidence normalization, UniRef/current-reference screen, and review-resolution gap audit
  - fixed terminal/queue duplicate-screen propagation so UniRef-cleared rows do not retain stale broader-duplicate blockers
  - fixed human-review wording for heuristic fingerprint context changes in representation evidence

key_artifacts:
  replacement_scout: artifacts/v3_external_source_pilot_glycoside_hydrolase_replacement_scout_current702_20260616_run2205.json
  pinned_priority: artifacts/v3_external_source_pilot_candidate_priority_q6nsj0_replacement_current702_20260616_run2205.json
  active_site_decisions: artifacts/v3_external_source_pilot_active_site_evidence_decisions_q6nsj0_replacement_current702_20260616_run2205.json
  representation_adjudication: artifacts/v3_external_source_pilot_representation_adjudication_q6nsj0_replacement_current702_20260616_run2205.json
  uniref_screen: artifacts/v3_external_source_pilot_uniref_current_reference_screen_q6nsj0_replacement_current702_20260616_run2205.json
  terminal_decisions: artifacts/v3_external_source_pilot_terminal_decisions_q6nsj0_replacement_current702_20260616_run2205.json
  expert_queue: artifacts/v3_external_source_pilot_human_expert_review_queue_q6nsj0_replacement_current702_20260616_run2205.json
  gap_audit: artifacts/v3_external_source_pilot_review_resolution_gap_audit_q6nsj0_replacement_current702_20260616_run2205.json
  closure_note: work/external_source_transfer_q6nsj0_replacement_closure_current702_20260616_run2205.md

current_gate_state:
  selected_pilot_rows: 13
  q6nsj0_evidence: active-site positions 463 and 520; Rhea RHEA:21112; UniRef/current-reference no-overlap
  terminal_status_counts: 7 deferred_requires_human_expert; 6 rejected_active_site_evidence_missing
  expert_queue_rows: 7
  expert_queue_non_human_blocker: full_label_factory_gate_not_run
  gap_audit_status: 7 family_import_safety_adjudication_missing
  import_ready_rows: 0
  countable_label_candidate_rows: 0

next_action: >
  Build a current-slice needs_review_resolution and repair-lane mapping for Q6NSJ0,
  then run build-external-source-pilot-glycoside-hydrolase-import-safety-adjudication
  against the Q6NSJ0 replacement packet. Only after that, rerun success criteria,
  terminal/confidence normalization, label-factory, novelty, governor, and row-guardrail
  gates before any import.
