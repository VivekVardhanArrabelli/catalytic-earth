automation: ce-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-16T21:05:34Z
started_local: Tue Jun 16 16:05:34 CDT 2026
closeout_at: 2026-06-16T21:54:29Z
elapsed_minutes: 48.9
remaining_minutes: 6.1
budget_minutes: 55
planned_closeout_minute: 50

state: run2105_source_transfer_review_gap_mapped_acyl_control_adjudicated_no_apply
lock: acquired by this run at 2026-06-16T21:05:34Z after stale run2004 recovery
branch: main
origin_main_at_start: c99f07bd44a63daac5c20cc4d75349d05147cc3c
base_at_start: 2654643e9ef3024d08835a9de2994cdf4fd337a3
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

validation:
  registry_validate: passed
  baseline_critical_suite: 581 passed, 174 subtests
  focused_transfer_cli_after_gap_and_control: 355 passed, 160 subtests
  final_critical_suite_pre_acyl_adjudication: 715 passed, 174 subtests
  pre_acyl_full_pytest: 2380 passed, 1 warning, 244 subtests
  focused_acyl_adjudication_regressions: 3 passed
  final_critical_suite_post_acyl_adjudication: 717 passed, 174 subtests
  final_full_pytest: 2382 passed, 1 warning, 244 subtests
  compileall: passed
  current_docs_artifact_reference_check: 0 missing / 2080 checked / 14 ignored
  run2105_json_parse: passed
  progress_jsonl_parse: passed
  git_diff_check: passed
  frozen_registry_diff: none observed
  registry_artifact_hard_limit_scan_over_90mb: none

current_counts:
  frozen_current702_rows: 702
  expansion_rows: 8026
  combined_labels: 8728
  positive_holes: 0
  floor_deficit: 0
  novelty_replay: 7565 admit / 414 throttle / 47 reject
  factory_ready_existing_lanes_ge150: 0
  top_projected_clean_admits: 77
  evidence_handle_reachable_positive_bronze_uplift: 741
  breadth_projected_positive_bronze_clean_only: 9673
  breadth_gap_to_10k_positive_bronze: 327
  source_scale_recommendation: stop_m_csa_only_tranche_growth_and_scope_external_source_transfer

run2105_source_transfer_review_gap:
  repair_lanes: artifacts/v3_external_source_pilot_mechanism_repair_lanes_t12_allvsall_uniref_current702_20260616_run2105_enriched.json
  acyl_coa_control: artifacts/v3_external_source_pilot_acyl_coa_lyase_thioesterase_control_t12_allvsall_uniref_current702_20260616_run2105.json
  acyl_coa_import_safety_adjudication: artifacts/v3_external_source_pilot_acyl_coa_lyase_thioesterase_import_safety_adjudication_t12_allvsall_uniref_current702_20260616_run2105.json
  review_resolution_gap_audit: artifacts/v3_external_source_pilot_review_resolution_gap_audit_t12_allvsall_uniref_current702_20260616_run2105.json
  review_resolution_gap_audit_with_acyl: artifacts/v3_external_source_pilot_review_resolution_gap_audit_t12_allvsall_uniref_with_acyl_import_safety_current702_20260616_run2105.json
  review_resolution_gap_import_safety: artifacts/v3_external_source_pilot_review_resolution_gap_import_safety_current702_20260616_run2105.json
  review_resolution_gap_import_safety_with_acyl: artifacts/v3_external_source_pilot_review_resolution_gap_import_safety_with_acyl_current702_20260616_run2105.json
  candidate_rows: 5
  import_ready_rows: 0
  countable_label_candidate_rows: 0
  initial_resolution_gap_status_counts: review_decision_and_factory_gate_blocked_after_control_repair 3 / family_import_safety_adjudication_missing 1 / family_control_unresolved_after_adjudication 1
  with_acyl_resolution_gap_status_counts: review_decision_and_factory_gate_blocked_after_control_repair 4 / family_control_unresolved_after_adjudication 1
  repair_lane_counts: AKR/NADP 1 / SDR/NAD(P) 1 / DNA Pol X 1 / acyl-CoA lyase-thioesterase 1 / glycoside boundary 1
  q8n0x4_control_status: review_only_acyl_coa_lyase_thioesterase_scope_ready
  q8n0x4_import_safety_status: acyl_coa_lyase_thioesterase_scope_control_repaired
  q8n0x4_active_site_context: D320, sequence window GKGAFTFQGSMIDMPLLKQAQNTVT, Rhea context present
  import_safety: safe / 0 unsafe artifacts / 0 new countable labels

storage_and_docs:
  current_docs_artifact_reference_check: artifacts/v3_current_docs_artifact_reference_check_current702_20260616_run2105.json
  artifact_storage_inventory: artifacts/v3_artifact_storage_inventory_current702_20260616_run2105.json
  artifact_storage_policy_check: artifacts/v3_artifact_storage_policy_check_current702_20260616_run2105.json
  artifact_storage_policy_status: blocked by 43 large-unclassified artifacts; deletion_authorized_count 0; source_file_count 14932
  source_scale_limit_audit: artifacts/v3_source_scale_limit_audit_current702_20260616_run2105.json

code_changes:
  - Added build-external-source-pilot-review-resolution-gap-audit plus CLI/parser coverage.
  - Routed Q8N0X4/citramalyl-CoA lyase/thioesterase context to add_acyl_coa_lyase_thioesterase_scope_control.
  - Added build-external-source-pilot-acyl-coa-lyase-thioesterase-control to stage review-only D320/Rhea scope evidence.
  - Added build-external-source-pilot-acyl-coa-lyase-thioesterase-import-safety-adjudication and wired it into the review-resolution gap audit.
  - Preserved non-countable semantics: no predictive evidence admission, no import-ready rows, no label rows, and no registry mutation.

no_apply_reason: >
  No holes or under-floor fingerprints are open, and no existing high-yield lane projects >=150
  clean admits. The source-transfer pilot still has zero import-ready/countable rows: three rows
  require explicit review decisions plus factory gates after control repair, Q8N0X4 is now
  adjudicated as a non-authorizing acyl-CoA scope-control repair but still blocked by
  review/factory/representation/heuristic gates, and P33025 remains blocked by glycoside-boundary
  control issues.

next_action: >
  Record explicit review decisions for the four control-repaired rows and rerun duplicate/factory
  gates only after those decisions exist; separately repair or replace the P33025 glycoside-boundary
  control. Do not import/apply from run2105 artifacts unless review decision, duplicate,
  label-factory, novelty, governor, and row-guardrail gates pass explicitly.
