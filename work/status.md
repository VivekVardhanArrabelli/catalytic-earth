automation: ce-autonomous-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-17T00:08:09Z
started_local: Tue Jun 16 19:08:09 CDT 2026
closeout_at: 2026-06-17T00:58:06Z
elapsed_minutes: 50.0
remaining_minutes: 5.0
budget_minutes: 55
planned_closeout_minute: 50

state: run0008_q6nsj0_boundary_repaired_p55263_design_packeted_no_apply
lock: acquired by this run at 2026-06-17T00:08:20Z
branch: main
origin_main_at_start: 69f1785647469dd6eac671bbb72aef2b0a3dd59d
origin_main_before_push: 69f1785647469dd6eac671bbb72aef2b0a3dd59d
base_at_start: 69f1785647469dd6eac671bbb72aef2b0a3dd59d
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

validation:
  registry_validate: passed
  baseline_critical_suite: 786 passed, 174 subtests
  final_critical_suite: 788 passed, 174 subtests
  focused_transfer_cli_suite: 371 passed, 160 subtests
  full_pytest: 2396 passed, 1 warning, 244 subtests
  compileall: passed
  git_diff_check: passed
  docs_reference_check: 0 missing / 2147 checked / 14 ignored
  json_jsonl_parse: parsed 22 run0008 json artifacts and 688 progress JSONL records
  hard_limit_scan_over_90mb: none
  artifact_storage_policy: blocked; 45 large-unclassified artifacts, 0 deletions authorized
  artifact_migration_dry_run: passed; 116 rows, removal_allowed=0
  github_fetch_push: pending

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
  reviewed_swissprot_projection: 9673
  gap_to_10k_reviewed_swissprot_only: 327

work_completed:
  - refreshed coverage, novelty, high-yield factory, evidence-handle, breadth, and source-scale audits for run0008
  - repaired Q6NSJ0 glycoside boundary-control interpretation by separating raw role hints from evidence-bearing metal role support
  - regenerated Q6NSJ0 glycoside boundary control; Q6NSJ0 is now review-only boundary-ready with raw role-hint count 1 and evidence-bearing metal role-hint count 0
  - regenerated Q6NSJ0 glycoside import-safety; Q6NSJ0 representation conflict is repaired but still not import-ready
  - merged Q6NSJ0 with historical P33025 glycoside adjudication; merged replay has one repaired and one unrepaired glycoside row
  - replayed source-transfer review-resolution gap; seven rows remain held, zero import-ready, zero countable
  - added non-authorizing P55263 manual source-mechanism control-design builder and CLI
  - integrated optional manual source-mechanism control-design context into review-resolution gap audits without relaxing import gates
  - built P55263 control-design packet mapping adenosine kinase / RHEA:20824 context to candidate pfkb_ribokinase_family while keeping predictive_evidence empty
  - recorded P55263 PfkB source-free control feasibility audit; current status remains source-free control not implemented
  - refreshed storage inventory, policy, producer/consumer manifest, readiness plan, and no-op migration execution dry run

key_artifacts:
  coverage_pre: artifacts/v3_coverage_redundancy_audit_current702_20260616_run0008_pre_lane.json
  coverage_post_noapply: artifacts/v3_coverage_redundancy_audit_current702_20260616_run0008_post_noapply.json
  novelty_pre: artifacts/v3_novelty_admission_gate_audit_current702_20260616_run0008_pre_lane.json
  novelty_post_noapply: artifacts/v3_novelty_admission_gate_audit_current702_20260616_run0008_post_noapply.json
  high_yield_factory: artifacts/v3_high_yield_family_lane_factory_current702_20260616_run0008_pre_lane.json
  evidence_handle_expansion: artifacts/v3_evidence_handle_expansion_current702_20260616_run0008_pre_lane.json
  breadth_scout: artifacts/v3_breadth_feasibility_scout_current702_20260616_run0008_pre_lane.json
  source_scale_audit: artifacts/v3_source_scale_limit_audit_current702_20260616_run0008.json
  q6nsj0_glycoside_boundary: artifacts/v3_external_source_pilot_glycoside_hydrolase_boundary_control_q6nsj0_replacement_current702_20260616_run0008.json
  q6nsj0_glycoside_import_safety: artifacts/v3_external_source_pilot_glycoside_hydrolase_import_safety_adjudication_q6nsj0_replacement_current702_20260616_run0008.json
  merged_glycoside_adjudication: artifacts/v3_external_source_pilot_glycoside_hydrolase_import_safety_adjudication_merged_q6nsj0_p33025_current702_20260616_run0008.json
  final_gap_audit: artifacts/v3_external_source_pilot_review_resolution_gap_audit_q6nsj0_p55263_with_glyco_repair_replay_current702_20260616_run0008.json
  final_import_safety: artifacts/v3_external_source_pilot_review_resolution_gap_import_safety_q6nsj0_p55263_with_glyco_repair_replay_current702_20260616_run0008.json
  p55263_control_design: artifacts/v3_external_source_pilot_p55263_mechanism_control_design_current702_20260616_run0008.json
  p55263_control_design_safety: artifacts/v3_external_source_pilot_p55263_mechanism_control_design_import_safety_current702_20260616_run0008.json
  p55263_pfkb_feasibility_audit: artifacts/v3_external_source_pilot_p55263_pfkb_control_feasibility_audit_current702_20260616_run0008.json
  storage_policy: artifacts/v3_artifact_storage_policy_check_current702_20260616_run0008.json
  migration_execution_manifest: artifacts/v3_artifact_migration_execution_manifest_current702_20260616_run0008.json

current_gate_state:
  q6nsj0_status: glycoside boundary control repaired; review-only; still needs terminal review and full factory/inverse gates
  p33025_status: glycoside boundary representation conflict not repaired
  p55263_status: non-authorizing pfkb_ribokinase_family control design only; manual-review-only
  final_gap_rows: 7
  review_decision_and_factory_gate_blocked_after_control_repair: 5
  family_control_unresolved_after_adjudication: 1
  manual_source_mechanism_control_design_review_only: 1
  import_ready_rows: 0
  countable_label_candidate_rows: 0
  review_only_import_safety: safe; 0 unsafe artifacts; 0 new countable labels

next_action: >
  Use Q6NSJ0's repaired boundary and P55263's design packet only as review planning evidence.
  Do not apply/import from run0008 artifacts. The next scaling unlock is explicit terminal
  review/factory replay for the five control-repaired rows, an implemented source-free
  PfkB/ribokinase-family control plus P55263 import-safety adjudication, or a new
  source-handle/source-transfer lane that passes duplicate, active-site, factory, novelty,
  governor, and row-guardrail gates.
