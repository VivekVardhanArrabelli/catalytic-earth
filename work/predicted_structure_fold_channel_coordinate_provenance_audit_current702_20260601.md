# Predicted-Structure Fold Channel Coordinate Provenance Audit - current702

Run: 2026-06-01T16:51:29Z

Coordinate-provenance audit for the already scored AlphaFoldDB-predicted Foldseek/TM channel. This validates the remaining persistent CIF bundle blocker without rerunning Foldseek/TM or changing downstream scores.

## Status

- coordinate_bundle_not_persisted_results_parseable
- Unique coordinate files expected: 299
- Unique coordinate files observed: 0
- Unique coordinate files missing: 299
- Deduplicated AFDB accessions expected: 293
- Deduplicated AFDB accessions with no local file: 293
- Foldseek result files missing: 0
- Result files parseable: True

## Coordinate Groups

- all_heldout_queries_when_cheap: requests=126, observed=0, missing=126, unique_paths=126
- atlas_in_distribution: requests=167, observed=0, missing=167, unique_paths=167
- priority_cofactor_confounded_oos_queries: requests=6, observed=0, missing=6, unique_paths=6

## Foldseek Results

- all_heldout_vs_atlas: exists=True, parsed=parsed, lines=11297, hits=126
- priority_cofactor_confounded_oos_vs_atlas: exists=True, parsed=parsed, lines=402, hits=6

## Contract Audit

- Status: fold_channel_contract_passed_current702
- Critical violations: 0

## Materialization Plan

- Persist the AFDB-v6 CIF coordinate bundle if byte-level Foldseek reproduction is required; the scored TSVs already support downstream diagnostics.
- Missing coordinate paths: 299
- Deduplicated missing AFDB accessions: 293

## Interpretation

- The Foldseek/TM result TSVs are present and parsed, but the persistent AFDB-v6 coordinate bundle is not committed locally.
- If byte-level score reproduction is needed, materialize the 299 missing coordinate paths (293 deduplicated AFDB-v6 accessions) using the recorded download script, rerun the contract audit, and then rerun this provenance audit.
