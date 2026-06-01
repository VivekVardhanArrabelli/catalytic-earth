# Predicted-Structure Fold Channel Reproduction Manifest - current702

Run: 2026-06-01T17:52:25Z

Validation-only reproduction manifest for the already scored AlphaFoldDB-predicted Foldseek/TM channel. It records exact coordinate inputs, scored TSV hashes, rerun commands, and the remaining byte-level reproduction blockers without downloading coordinates or rerunning Foldseek/TM.

## Status

- fold_channel_reproduction_manifest_ready_missing_coordinates
- Heldout ok rows: 126
- Priority cofactor-confounded rows: 6
- Result TSVs parseable: True
- Foldseek runtime available: True
- Unique coordinate files expected: 299
- Unique coordinate files missing: 299
- Deduplicated missing AFDB accessions: 293
- Byte-level reproduction ready: False

## Coordinate Groups

- all_heldout_queries_when_cheap: requests=126, observed=0, missing=126, unique_paths=126
- atlas_in_distribution: requests=167, observed=0, missing=167, unique_paths=167
- priority_cofactor_confounded_oos_queries: requests=6, observed=0, missing=6, unique_paths=6

## Foldseek Result Files

- all_heldout_vs_atlas: exists=True, parsed=parsed, lines=11297, hits=126, sha256=b9dfa47f421c981dfde2f9b8050bba4c5e48c9d0be79c34c4cb6c7c1155f5871
- priority_cofactor_confounded_oos_vs_atlas: exists=True, parsed=parsed, lines=402, hits=6, sha256=b35dc803a7dcbfaae069214a4556abeb723c704cf9775b0bc3c1cd7f5fa8b31f

## Contract Audit

- Status: fold_channel_contract_passed_current702
- Critical violations: 0

## Blockers

- persistent_afdb_v6_coordinate_bundle_missing

## Commands

- Materialize coordinates: `reproduction_commands.materialize_all_missing_afdb_v6_coordinates`
- Rerun priority Foldseek/TM: `reproduction_commands.run_priority_cofactor_confounded_oos_vs_atlas`
- Rerun all-heldout Foldseek/TM: `reproduction_commands.run_all_heldout_vs_atlas_when_cheap`
- Rerun audits: `reproduction_commands.rerun_contract_audit`, `reproduction_commands.rerun_coordinate_provenance_audit`, then `reproduction_commands.rerun_reproduction_manifest`

## Interpretation

- The scored Foldseek/TM channel remains usable for downstream diagnostics because the TSVs parse and the scoring contract passes; byte-level reproduction is blocked only by the missing persistent AFDB-v6 coordinate bundle.
- Materialize the missing AFDB-v6 CIF paths with the recorded download command only if byte-level Foldseek reproduction is needed; otherwise continue downstream diagnostics from the existing scored TSVs and contract audit.
