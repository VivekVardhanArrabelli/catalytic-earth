# Fold-Augmented Confounded Proxy AFDB Version Sweep - current702

Run: 2026-06-04T08:31:25Z

Live AlphaFoldDB v1-v6 HEAD availability sweep for the four remaining Lever 3 predicted-structure-unavailable rows. It performs no downloads, imports, scoring, threshold changes, or heldout calibration use.

## Status

- fold_augmented_confounded_proxy_afdb_version_sweep_no_models_available
- Probe rows: 4
- AFDB HTTP 200 rows: 0
- AFDB all-version 404 rows: 4
- Blockers: ['four_remaining_rows_unavailable_from_afdb_v1_through_v6', 'approved_non_afdb_predicted_structure_source_missing']

## Rows

| row | accession | v6 | v5 | v4 | v3 | v2 | v1 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| m_csa:416 | P07071 | 404 | 404 | 404 | 404 | 404 | 404 |
| m_csa:562 | P07658 | 404 | 404 | 404 | 404 | 404 | 404 |
| m_csa:586 | P00806 | 404 | 404 | 404 | 404 | 404 | 404 |
| m_csa:637 | P04531 | 404 | 404 | 404 | 404 | 404 | 404 |

## Interpretation

- The repo-supported AlphaFoldDB auto-version fallback is exhausted for all four remaining coordinate-missing rows; every checked v1-v6 CIF URL returned 404.
- Do not rerun Foldseek or thresholds. Choose/approve a non-AFDB predicted-structure source, or keep these rows as disclosed deployment-validity blockers.
