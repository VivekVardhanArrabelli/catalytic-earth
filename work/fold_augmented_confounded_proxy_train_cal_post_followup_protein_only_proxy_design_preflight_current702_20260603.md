# Fold-Augmented Confounded Proxy Train/Cal Protein-Only Proxy Design Preflight

Run: 2026-06-03T19:28:08Z

Fail-closed design preflight for the protein-only path after the unsupported inorganic-locus AFDB coordinate repair attempt. It does not score rows, register a new proxy axis, tune thresholds, or read heldout.

## Status

- fold_augmented_confounded_proxy_train_cal_protein_only_proxy_design_preflight_ready_contract_selection
- Unsupported-geometry repair rows: 8
- Coordinate files scanned: 8
- Protein-only AFDB files: 8
- Source-free inorganic/cofactor locus-evidence files: 0
- Existing scored new-proxy-axis rows: 6
- Design contract candidate options: 2
- Ready-to-score-now rows: 0
- Blockers: ['unsupported_geometry_afdb_coordinates_protein_only_no_locus_evidence', 'protein_only_proxy_contract_not_selected']

## Decision

- Design preflight ready for contract selection: True
- Preferred next axis: protein_only_fold_topology_residual
- Score any rows now: False
- Register new proxy axis now: False
- Run fixed-threshold audit now: False
- Next gate: Choose exactly one source-free protein-only proxy axis, preferably the fold-topology residual, and write a train/cal-only pre-registration contract before any scoring. Do not score or register the unsupported inorganic-locus axis from the protein-only AFDB files.

## Design Options

| axis | status | rows/files | score now | register now |
| --- | --- | ---: | --- | --- |
| unsupported_inorganic_locus_from_afdb_components | rejected_by_coordinate_locus_scan | 8 | False | False |
| protein_only_fold_topology_residual | design_contract_candidate | 8 | False | False |
| protein_only_global_shape_confidence_residual | design_contract_candidate | 8 | False | False |
| mcsa_row_specific_active_site_or_source_locator_residual | not_deployment_closed_for_new_axis | 8 | False | False |

## Interpretation

- The unsupported inorganic-locus coordinate path is exhausted, but a protein-only proxy-axis design gate is available.
- 8 AFDB-v6 coordinate files were protein-only with 0 source-free inorganic/cofactor locus-evidence files; do not convert that locus axis into a scoreable proxy.
- Pre-register one train/cal-only protein-only proxy contract before scoring; fold-topology residual is the preferred first contract because it matches the deployment-valid predicted-structure-vs-atlas channel.
