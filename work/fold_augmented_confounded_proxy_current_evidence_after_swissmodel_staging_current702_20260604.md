# Fold-Augmented Confounded Proxy Current Evidence After SWISS-MODEL Staging - current702

Run: 2026-06-04T10:43:09Z

Updated Lever 3 current-evidence blocker after SWISS-MODEL coordinate staging, P07658 rescue probes, local predictor-runtime scan, and 3D-Beacons predicted-structure probe. It records staged deployment-valid predicted-coordinate inputs, remaining surface blockers, unchanged train/cal calibration shortfalls, and does not rescore rows or change threshold 0.44155.

## Status

- fold_augmented_confounded_proxy_current_evidence_after_swissmodel_staging_blocked_partial_surface
- Staged predicted coordinate rows: 3
- Surface-completeness blockers: 2
- Coordinate-source blockers: 1
- Q43088 locator/geometry blockers: 1
- High-cofactor shortfall: 16
- Same-family structural shortfall: 170
- Blockers: ['p07658_full_length_predicted_coordinate_missing', 'q43088_two_source_free_locator_positions_missing', 'sixteen_row_high_cofactor_train_cal_probe_not_acquired', 'one_hundred_seventy_row_same_family_structural_acquisition_not_acquired', 'fixed_threshold_audit_not_ready_to_rerun']

## Staged Coordinate Rows

| row | accession | provider | template | path |
| --- | --- | --- | --- | --- |
| m_csa:416 | P07071 | SWISSMODEL | 9d3x.1.A | artifacts/v3_fold_augmented_swissmodel_coordinates_current702_20260604/SWISSMODEL_P07071_9d3x_1_A_range_6_605.pdb |
| m_csa:586 | P00806 | SWISSMODEL | 1lba.1.A | artifacts/v3_fold_augmented_swissmodel_coordinates_current702_20260604/SWISSMODEL_P00806_1lba_1_A_range_7_151.pdb |
| m_csa:637 | P04531 | SWISSMODEL | 1del.1.A | artifacts/v3_fold_augmented_swissmodel_coordinates_current702_20260604/SWISSMODEL_P04531_1del_1_A_range_1_241.pdb |

## Remaining Surface Blockers

| row | accession | blocker | missing evidence | smallest next experiment | failed rescue paths |
| --- | --- | --- | --- | --- | --- |
| m_csa:562 | P07658 | predicted_structure_unavailable | full-length deployment-valid predicted structure for exact 715-residue sequence including selenocysteine | Install or provision an approved full-length predictor/runtime that supports the exact 715-residue P07658 sequence including selenocysteine, or use a credentialed provider; then stage provider/model/version/path/checksum provenance. | SWISS-MODEL primary accession has only provider=PDB rows; SWISS-MODEL secondary accessions P78137/Q2M6M5 resolve to same PDB-only surface; AlphaFoldDB v6 direct and secondary accessions are 404; public ESMFold API rejects sequence length >400; credential-free BioLM/OpenProtein provider probes require credentials/access; local PATH, conda env, and shallow filesystem runtime scan found no full-length predictor; 3D-Beacons summary returns only experimentally determined PDBe rows |
| m_csa:604 | Q43088 | approved_geometry_feature_missing | two additional approved source-free locator positions or approved source-free geometry sidecar | approve two additional Q43088 locator positions from source-free evidence, or approve an equivalent geometry sidecar | n/a |

## Decision

- Fixed-threshold audit ready now: False
- Smallest surface-completeness experiment: Clear P07658 with an exact full-length predicted coordinate from an approved runtime/provider and approve two Q43088 source-free locator positions or an equivalent geometry sidecar.
- Smallest calibration experiment: Run the frozen 16-row high-cofactor train/cal OOS acquisition first; the 170-row same-family structural acquisition remains after it.

## Interpretation

- Surface completeness is partially advanced: P07071, P00806, and P04531 now have staged SWISS-MODEL homology-model coordinates; P07658 and Q43088 remain blocked, and calibration shortfalls are unchanged.
- Provision or run a full-length P07658 predictor/provider and complete Q43088 locator review before any fixed-threshold rerun; do not use experimental PDBe/3D-Beacons rows as deployment shortcuts.
