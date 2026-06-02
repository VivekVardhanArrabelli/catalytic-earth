# Predicted-Structure Fold Channel Reproduction Manifest - current702

Run: 2026-06-02T16:13:09Z

Validation-only reproduction manifest for the already scored AlphaFoldDB-predicted Foldseek/TM channel. It records exact coordinate inputs, scored TSV hashes, rerun commands, and the remaining byte-level reproduction blockers without downloading coordinates or rerunning Foldseek/TM.

## Status

- fold_channel_byte_reproduction_ready
- Heldout ok rows: 126
- Priority cofactor-confounded rows: 6
- Result TSVs parseable: True
- Foldseek runtime available: True
- Unique coordinate files expected: 299
- Unique coordinate files missing: 0
- Deduplicated missing AFDB accessions: 0
- Byte-level reproduction ready: True

## Coordinate Groups

- all_heldout_queries_when_cheap: requests=126, observed=126, missing=0, unique_paths=126
- atlas_in_distribution: requests=167, observed=167, missing=0, unique_paths=167
- priority_cofactor_confounded_oos_queries: requests=6, observed=6, missing=0, unique_paths=6

## Foldseek Result Files

- all_heldout_vs_atlas: exists=True, parsed=parsed, lines=11297, hits=126, sha256=b9dfa47f421c981dfde2f9b8050bba4c5e48c9d0be79c34c4cb6c7c1155f5871
- priority_cofactor_confounded_oos_vs_atlas: exists=True, parsed=parsed, lines=402, hits=6, sha256=b35dc803a7dcbfaae069214a4556abeb723c704cf9775b0bc3c1cd7f5fa8b31f

## Contract Audit

- Status: fold_channel_contract_passed_current702
- Critical violations: 0

## Blockers

- none

## Commands

- Materialize coordinates: `reproduction_commands.materialize_all_missing_afdb_v6_coordinates`
- Rerun priority Foldseek/TM: `reproduction_commands.run_priority_cofactor_confounded_oos_vs_atlas`
- Rerun all-heldout Foldseek/TM: `reproduction_commands.run_all_heldout_vs_atlas_when_cheap`
- Rerun audits: `reproduction_commands.rerun_contract_audit`, `reproduction_commands.rerun_coordinate_provenance_audit`, then `reproduction_commands.rerun_reproduction_manifest`

## Interpretation

- The coordinate bundle, Foldseek runtime, result TSVs, and contract audit are all present for byte-level reproduction.
- Rerun the reproduction manifest after any Foldseek/TM score refresh.
