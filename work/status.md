automation: ce-autonomous-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-17T03:09:49Z
started_local: Tue Jun 16 22:09:49 CDT 2026
closeout_at: 2026-06-17T03:58:51Z
elapsed_minutes: 49.0
remaining_minutes: 6.0
budget_minutes: 55
planned_closeout_minute: 50

state: run0310_source_transfer_all_vs_all_no_registry_apply
lock: acquired by this run at 2026-06-17T03:08:31Z
branch: main
origin_main_at_start: 8359eb6e5ef26a454494e6edb12195084b22ef56
base_at_start: 8359eb6e5ef26a454494e6edb12195084b22ef56
origin_main_pre_push_fetch: 8359eb6e5ef26a454494e6edb12195084b22ef56
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

validation:
  registry_validate: passed
  baseline_critical_suite: 525 passed, 14 subtests
  final_affected_suite: 536 passed, 14 subtests
  focused_all_vs_all_transfer_cli: 39 passed, 340 deselected
  final_full_pytest: 2404 passed, 1 warning, 244 subtests
  compileall: passed
  current_docs_reference_check: missing 0 / checked 2206 / ignored 14
  json_jsonl_parse: parsed 94 run0310 JSON artifacts and 693 progress JSONL records before final append
  git_diff_check: passed
  hard_limit_scan_over_90mb: none
  frozen_current702_sha_check: passed

coverage_state:
  combined_labels: 8728
  frozen_rows: 702
  expansion_rows: 8026
  positive_holes: 0
  floor_deficit: 0
  novelty_replay: admit 7565 / throttle 414 / reject 47
  ready_existing_lanes_ge150: 0
  top_projected_clean_admits: 77
  reviewed_swissprot_clean_projection: 9673
  gap_to_10k_positive_bronze: 327

work_completed:
  - acquired automation lock and fast-forward checked origin/main
  - recorded frozen current702 SHA before any apply
  - refreshed coverage, novelty, high-yield factory, evidence-handle, breadth, and source-scale state
  - generated reviewed biotin-dependent carboxylase broad-handle preview with 41 clean novelty-admitted rows, not applied
  - confirmed reviewed biotin offset-250 window fetched 0 rows
  - rebuilt current external source-transfer chain through import readiness, blocker matrix, pilot decisions, and normalized expert queue
  - added run0310 external all-vs-all sequence duplicate screen with real mmseqs2 backend and clean audit
  - refreshed artifact storage inventory, storage policy, migration dry-run, and admission guard
  - attempted bounded NAD/glycosyltransferase live scout; interrupted before preview due slow UniProt entry fetch latency

current_gate_state:
  registry_apply: not attempted
  import_ready_rows: 0
  countable_label_candidate_rows: 0
  transfer_candidate_rows: 47
  transfer_import_readiness_status: 21 active-site sourcing / 14 heuristic control / 9 representation control / 2 sequence holdout / 1 review-factory
  pilot_terminal_decisions: 6 deferred_requires_human_expert / 6 rejected_active_site_evidence_missing
  all_vs_all_duplicate_screen: 47 no-signal rows / 0 exact duplicate / 0 near duplicate / max identity 0.874
  sequence_reference_screen: fail-closed, 30 current-reference top-hit alignments incomplete
  storage_policy: blocked on 4 large unclassified artifacts at 50 MB policy threshold; no files over 90 MB
  registry_apply_blocker: no import-ready rows; active-site, representation, UniRef-wide duplicate, terminal review, factory, novelty, governor, and row-guardrail gates remain required

next_action: >
  Do not import the biotin preview or run0310 source-transfer review-only rows. Add or expose a
  current needs_review_resolution producer so run0310 mechanism-repair lanes and review-resolution
  gap replay can run, or directly resolve the remaining active-site sourcing, real representation
  backend/control, UniRef-wide duplicate, terminal review, full label-factory, novelty, governor,
  and row-guardrail gates before any import/apply.

## Automation run ce-nad-glyco-floor-expansion start
- started_at_utc: 2026-06-28T01:30:17Z
- started_local: Sat Jun 27 20:30:17 CDT 2026
- budget_minutes: 55
- planned_closeout_minute: 50
- frozen_current702_sha_before: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

## Automation run ce-nad-glyco-floor-expansion closeout
- closeout_at_utc: 2026-06-28T01:49:00Z
- elapsed_minutes: 18.7
- remaining_minutes: 36.3
- state: predicted_geometry_atlas_prereg_blocked_current57_router_drift
- branch: main
- origin_main_at_start: ae6b313fed4d0c2f7e8952520c5251676a626b21
- registry_mutation: none
- frozen_current702_sha_after: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
- work_completed:
  - added and ran predicted-geometry atlas-engine full-env/preregistration artifact
  - added row-level train/cal diagnostics to cofactor-fusion operating-point builder
  - preserved current-57 cofactor precision rerun as a diagnostic artifact, not a replacement contract
  - updated project state, decision log, handoff, and docs artifact-reference check
- current_gate_state:
  - existing scored fold/TM surfaces reusable: true
  - new Foldseek/TM scoring runnable: false (foldseek missing)
  - current-router cofactor precision drift detected: true
  - cached atlas-engine readout allowed now: false
- validation:
  - registry_validate: passed
  - focused_recovery_precision_tests: 86 passed, 2 subtests
  - full_pytest: 2524 passed, 1 warning, 244 subtests
  - compileall: passed
  - current_docs_reference_check: missing 0
  - json_jsonl_parse: 4581 JSON files and 715 progress JSONL records parsed
  - git_diff_check: passed
- next_action: >
  Resolve the current-router/fingerprint-surface drift before atlas-engine fusion: either freeze/replay
  the intended June 9 cofactor precision router surface, or preregister a new current-57 train/cal
  precision rule. Install/expose foldseek before new Foldseek/TM scoring.

## Automation run 2026-06-28T02:31:07Z
- started_at_utc: 2026-06-28T02:31:07Z
- started_local: Sat Jun 27 21:31:07 CDT 2026
- budget_minutes: 55
- planned_closeout_minute: 50
- frozen_current702_sha_before: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
- status: in_progress

## Automation run ce-nad-glyco-floor-expansion closeout
- closeout_at_utc: 2026-06-28T02:51:33Z
- elapsed_minutes: 20.4
- remaining_minutes: 34.6
- state: current57_cofactor_precision_contract_fail_closed_atlas_prereg_updated
- branch: main
- origin_main_at_start: 60b17cdf2635843f3fc62beb71ad5e7ed26915e9
- registry_mutation: none
- frozen_current702_sha_after: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
- work_completed:
  - added current-57 cofactor precision contract builder and CLI
  - generated fail-closed current-57 precision contract artifact/report
  - integrated contract blocker into predicted-geometry atlas-engine preregistration
  - regenerated docs artifact-reference check and updated project state/decision log/handoff
- current_gate_state:
  - current57_precision_contract_status: blocked_current57_cofactor_precision_contract_not_deployable
  - current57_exact_fused_calibration: 13/35 recovery, 26/26 OOS FP
  - current57_v1_metal_compatible_calibration: 26/35 recovery, 26/26 OOS FP
  - best_under_trusted_oos_fp_ceiling: threshold 0.733, 20/35 recovery, 8/26 OOS FP
  - atlas_prereg_status: preregistered_cached_surface_blocked_current57_precision_contract_new_foldseek_backend_blocked
- validation:
  - focused_contract_prereg_tests: 8 passed, 242 deselected
  - focused_recovery_precision_suite: 89 passed, 2 subtests
  - registry_validate: passed
  - full_pytest_final: 2528 passed, 1 warning, 244 subtests
  - compileall: passed
  - current_docs_reference_check: missing 0
  - json_jsonl_parse: 10723 JSON files and 8336 JSONL records across 27 JSONL files
  - git_diff_check: passed
- next_action: >
  Do not run atlas-engine fusion or heldout on the current-57 cofactor surface. Pin/replay
  the intended June 9 router/fingerprint surface, or build a new preregistered current-57
  precision channel/fusion rule that clears a train/cal recovery/OOS done bar. Install/expose
  foldseek before any new Foldseek/TM scoring.
