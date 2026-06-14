# Automation status

- automation_id: ce-nad-glyco-floor-expansion
- started_at_utc: 2026-06-14T19:02:07Z
- started_local: Sun Jun 14 14:02:07 CDT 2026
- budget_minutes: 55
- planned_closeout_minute: 50
- closeout_snapshot_utc: 2026-06-14T19:48:24Z
- elapsed_minutes: 46.3
- remaining_minutes: 8.7
- current_task: HAD-like phosphatase high-yield bronze lane implemented and applied
- registry_safety: green; external registry remains sharded, registry max shard ~18 MB, no
  `data/registries/` file above 45 MB
- frozen_current702_sha256: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
- honest_counters:
  - external_rows: 7008
  - external_positive_bronze: 5754
  - external_oos_bronze: 1224
  - external_silver_confirmed: 30
  - combined_label_surface: 7710
  - combined_seed_surface: 6014
  - positive_bronze: 5967
  - oos_bronze: 1696
  - silver_confirmed: 47
  - projected: 0
- validation:
  - focused_had_registry_suite: 326 passed
  - targeted_stale_pin_suite: 26 passed
  - full_suite: 2262 passed, 1 warning in 162.56s
  - cli_validate: passed; 12 source records, 38 fingerprints, 35 ontology families, 702 curated labels
  - json_parse: passed for new artifacts
  - git_diff_check: passed
  - file_size_scan: passed for data registries
- next_action: build the aldehyde_dehydrogenase fingerprint/ontology/source runner from
  `artifacts/v3_aldehyde_dehydrogenase_lane_preregistration_current702_20260614_post_had_apply.json`,
  then preview and row-audit before any apply; continue silver residue mapping for the 106 blocked
  silver-ready rows in parallel
