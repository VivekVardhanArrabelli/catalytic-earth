# Automation status

- automation_id: ce-nad-glyco-floor-expansion
- started_at_utc: 2026-06-14T20:02:35Z
- started_local: Sun Jun 14 15:02:35 CDT 2026
- budget_minutes: 55
- planned_closeout_minute: 50
- closeout_snapshot_utc: 2026-06-14T20:52:47Z
- elapsed_minutes: 50.2
- remaining_minutes: 4.8
- current_task: closeout after ALDH bronze apply, 39fp OOS preregistration refresh, ALDH PDB preview, and alpha/beta hydrolase preregistration
- registry_safety: green; external registry remains sharded, registry max shard ~18 MB, no
  `data/registries/` file above 45 MB
- frozen_current702_sha256: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
- honest_counters:
  - external_rows: 7158
  - external_positive_bronze: 5904
  - external_oos_bronze: 1224
  - external_silver_confirmed: 30
  - combined_label_surface: 7860
  - combined_seed_surface: 6164
  - positive_bronze: 6117
  - oos_bronze: 1696
  - silver_confirmed: 47
  - projected: 0
- validation:
  - cli_validate: passed; 12 source records, 39 fingerprints, 36 ontology families, 702 curated labels
  - focused_source_wall: 303 passed, 14 subtests passed
  - focused_count_sensitive: 66 passed
  - full_suite_final: 2272 passed, 1 warning, 244 subtests passed
  - progress_jsonl: parsed and tests/test_progress.py 3 passed
  - json_parse: passed for new/updated JSON artifacts
  - diff_check: passed
  - file_size_scan: passed; no `data/registries/` file over 45 MB
- artifacts:
  - `artifacts/v3_aldehyde_dehydrogenase_sourcing_preview_current702_20260614.json`
  - `artifacts/v3_aldehyde_dehydrogenase_row_guardrail_audit_current702_20260614.json`
  - `artifacts/v3_coverage_redundancy_audit_current702_20260614_post_aldehyde_dehydrogenase_apply.json`
  - `artifacts/v3_novelty_admission_gate_audit_current702_20260614_post_aldehyde_dehydrogenase_apply.json`
  - `artifacts/v3_high_yield_family_lane_factory_current702_20260614_post_aldehyde_dehydrogenase_apply.json`
  - `artifacts/v3_external_hard_negative_next_tranche_preregistration_39fp_1025.json`
  - `artifacts/v3_label_pdb_id_backfill_preview_aldehyde_dehydrogenase_current702_20260614.json`
  - `artifacts/v3_alpha_beta_hydrolase_esterase_lipase_lane_preregistration_current702_20260614_post_aldehyde_dehydrogenase_apply.json`
- next_action: build the `alpha_beta_hydrolase_esterase_lipase` fingerprint/ontology/source runner
  from its design-only preregistration; preview and row-audit before any apply; continue silver
  residue mapping and treat the ALDH/NAD(P) representation collision as a future leakage-safe
  feature/geometry design gap
