# Automation Status

- automation_id: ce-nad-glyco-floor-expansion
- started_at_utc: 2026-06-14T14:56:15Z
- started_local: Sun Jun 14 09:56:15 CDT 2026
- budget_minutes: 55
- planned_closeout_minute: 50
- state: closeout_validation_green
- updated_at_utc: 2026-06-14T15:38:48Z
- lock: acquired
- current_action: docs/commit/push/lock release
- result: registry sharded, full suite green, bounded PDB-ID backfill applied
- elapsed_minutes: 44.1
- remaining_minutes: 10.9
- external_bronze: 6862
- combined_label_surface: 7564
- combined_seed_surface: 5868
- remaining_gap_to_10k_seed_surface: 4132
- honest_counters: positive_bronze_count=5638, oos_bronze_count=1224, silver_ready_count=260_pending_geometry_run, silver_confirmed_count=17, projected_provisional_count=0
- registry_file_size_safety: external registry manifest 1203 bytes; four shard files <= 17996716 bytes; no changed/new file over 45MB
- validation: focused changed-state tests 39 passed; full suite 2238 passed, 1 warning, 244 subtests; cli validate ok; git diff --check ok

## Automation run start
- automation_id: ce-nad-glyco-floor-expansion
- started_at: 2026-06-14T15:56:31Z
- started_local: Sun Jun 14 10:56:31 CDT 2026
- budget_minutes: 55
- planned_closeout_minute: 50

## Automation run closeout
- automation_id: ce-nad-glyco-floor-expansion
- updated_at_utc: 2026-06-14T16:27:11Z
- lock: acquired
- current_action: docs/commit/push/lock release
- result: silver geometry blocker audited; PDB-ID pool scaled; planning artifacts refreshed
- elapsed_minutes: 30.7
- remaining_minutes: 24.3
- early_closeout_reason: remaining lanes require SIFTS/PDB residue-mapping materialization, RCSB network recovery, no-xref policy changes, or new HAD fingerprint/runner implementation
- external_bronze: 6862
- combined_label_surface: 7564
- combined_seed_surface: 5868
- remaining_gap_to_10k_seed_surface: 4132
- honest_counters: positive_bronze_count=5638, oos_bronze_count=1224, silver_ready_count=260_pending_geometry_run, silver_confirmed_count=17, projected_provisional_count=0
- pdb_id_pool: rows_with_pdb_ids=2020, delta_this_run=722
- silver_geometry_audit: runnable=0, blocked=260, silver_flips=0, blockers=missing_explicit_pdb_residue_mapping:260;missing_local_holo_coordinate_file:259;insufficient_exact_active_site_residues:20
- registry_file_size_safety: external registry manifest ~1.2KB; four shard files all under 18MB; no changed/new file over 45MB
- validation: focused critical tests 233 passed + 14 subtests; full suite 2241 passed, 1 warning, 244 subtests; cli validate ok; json parse ok; git diff --check ok
