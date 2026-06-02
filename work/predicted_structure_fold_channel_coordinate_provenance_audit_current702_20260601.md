# Predicted-Structure Fold Channel Coordinate Provenance Audit - current702

Run: 2026-06-02T16:13:09Z

Coordinate-provenance audit for the already scored AlphaFoldDB-predicted Foldseek/TM channel. This validates the remaining persistent CIF bundle blocker without rerunning Foldseek/TM or changing downstream scores.

## Status

- coordinate_provenance_complete
- Unique coordinate files expected: 299
- Unique coordinate files observed: 299
- Unique coordinate files missing: 0
- Deduplicated AFDB accessions expected: 293
- Deduplicated AFDB accessions with no local file: 0
- Foldseek result files missing: 0
- Result files parseable: True

## Coordinate Groups

- all_heldout_queries_when_cheap: requests=126, observed=126, missing=0, unique_paths=126
- atlas_in_distribution: requests=167, observed=167, missing=0, unique_paths=167
- priority_cofactor_confounded_oos_queries: requests=6, observed=6, missing=0, unique_paths=6

## Foldseek Results

- all_heldout_vs_atlas: exists=True, parsed=parsed, lines=11297, hits=126
- priority_cofactor_confounded_oos_vs_atlas: exists=True, parsed=parsed, lines=402, hits=6

## Contract Audit

- Status: fold_channel_contract_passed_current702
- Critical violations: 0

## Materialization Plan

- Persist the AFDB-v6 CIF coordinate bundle if byte-level Foldseek reproduction is required; the scored TSVs already support downstream diagnostics.
- Missing coordinate paths: 0
- Deduplicated missing AFDB accessions: 0

## Interpretation

- The fold-channel coordinate bundle and Foldseek/TM result files are locally present.
- Keep the coordinate bundle with the scored TSVs and rerun this audit after any fold-channel score refresh.
