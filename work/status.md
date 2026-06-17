automation: ce-autonomous-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-17T01:07:32Z
started_local: Tue Jun 16 20:07:32 CDT 2026
closeout_at: 2026-06-17T01:55:08Z
elapsed_minutes: 47.6
remaining_minutes: 7.4
budget_minutes: 55
planned_closeout_minute: 50

state: run0009_p55263_pfkb_keepheld_terminal_queue_tier2_source_strategy_no_apply
lock: acquired by this run at 2026-06-17T01:07:32Z
branch: main
origin_main_at_start: e9e80382644583cfb885806af4e0479509cd8955
origin_main_before_push: e9e80382644583cfb885806af4e0479509cd8955
base_at_start: e9e80382644583cfb885806af4e0479509cd8955
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

validation:
  registry_validate: passed
  baseline_critical_suite: 728 passed, 174 subtests
  focused_transfer_cli_review_only_suite: 380 passed, 160 subtests
  focused_broad_suite: 616 passed, 174 subtests
  touched_tier2_guardrail_suite: 21 passed
  full_pytest: 2402 passed, 1 warning, 244 subtests
  compileall: passed
  git_diff_check: passed
  docs_reference_check: missing 0
  json_jsonl_parse: parsed 27 run0009 JSON artifacts and 689 progress JSONL records before final append
  hard_limit_scan_over_90mb: none
  github_fetch_push: origin/main unchanged before commit

coverage_state:
  combined_labels: 8728
  frozen_rows: 702
  expansion_rows: 8026
  positive_holes: 0
  floor_deficit: 0
  novelty_replay:
    admit: 7565
    throttle: 414
    reject: 47
  ready_existing_lanes_ge150: 0
  top_projected_clean_admits: 77
  reviewed_swiss_prot_clean_projection: 9673
  gap_to_10k_reviewed_only: 327

work_completed:
  - acquired automation lock and fast-forward checked origin/main
  - recorded frozen current702 SHA before and after no-apply work
  - ran baseline validation and critical tests
  - refreshed coverage, novelty, high-yield factory, evidence-handle, breadth, and source-scale state
  - added review-only P55263 PfkB source-free keep-held decision and import-safety adjudication
  - replayed review-resolution gap with P55263 keep-held and removed only stale missing-adjudication blocker
  - added terminal-review/factory replay queue for five control-repaired source-transfer rows
  - validated PfkB keep-held and terminal queue zero-import artifacts
  - ran bounded tier-2 source-handle scouts for PfkB, biotin carboxylase, and metal-independent PDE
  - ran row guardrail audits for all tier-2 source-handle scout previews
  - refreshed artifact storage inventory, storage policy, producer-consumer manifest, readiness plan, execution manifest, and admission guard
  - validated artifact migration dry-run with zero removal authorization
  - updated durable docs and handoff

key_artifacts:
  - artifacts/v3_external_source_pilot_p55263_pfkb_source_free_control_decision_current702_20260616_run0009.json
  - artifacts/v3_external_source_pilot_p55263_pfkb_import_safety_adjudication_current702_20260616_run0009.json
  - artifacts/v3_external_source_pilot_review_resolution_gap_audit_p55263_pfkb_keepheld_replay_current702_20260616_run0009.json
  - artifacts/v3_external_source_pilot_terminal_review_factory_replay_queue_current702_20260616_run0009.json
  - artifacts/v3_pfkb_ribokinase_family_tier2_source_handle_scout_current702_20260616_run0009.json
  - artifacts/v3_biotin_dependent_carboxylase_tier2_source_handle_scout_current702_20260616_run0009.json
  - artifacts/v3_metal_independent_phosphodiesterase_tier2_source_handle_scout_current702_20260616_run0009.json
  - artifacts/v3_artifact_storage_policy_check_current702_20260616_run0009.json
  - artifacts/v3_artifact_migration_execution_current702_20260616_run0009.json
  - artifacts/v3_artifact_admission_guard_current702_20260616_run0009.json

current_gate_state:
  registry_apply: not attempted
  import_ready_rows: 0
  countable_label_candidate_rows: 0
  p55263_status: manual_source_mechanism_keep_held_after_import_safety
  terminal_review_factory_queue_rows: 5
  pfkb_tier2_scout: 2 novelty-admitted, not authorized for apply
  biotin_tier2_scout: 9 novelty-admitted, not authorized for apply because floor already reached
  pde_tier2_scout: 0 novelty-admitted, 66 off-target held
  storage_policy: blocked by 46 large-unclassified/admission blockers; zero deletion authorized
  artifact_migration: dry-run passed, 116 rows, removal_allowed=0

next_action: >
  Do not import P55263 or tier-2 scout rows. Consume the five-row terminal-review/factory
  replay queue with explicit review decisions and full factory/novelty/governor/row-guardrail
  gates, implement a tested source-free PfkB/ribokinase control, or open a higher-yield
  source-transfer/source-handle lane that passes duplicate, active-site, factory, novelty,
  governor, row-guardrail, and lane-authorization gates.
