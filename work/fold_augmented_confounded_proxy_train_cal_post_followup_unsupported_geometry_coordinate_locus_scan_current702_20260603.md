# Fold-Augmented Confounded Proxy Train/Cal Unsupported-Geometry Coordinate Locus Scan - current702

Run: 2026-06-03T19:14:43Z

Train/cal-only source-free scan of the repaired AFDB-v6 CIF files for inorganic/cofactor locus evidence. It checks only local coordinate atom-site records and ligand/metal component IDs; it does not score rows, register a proxy axis, tune thresholds, read heldout rows, or count unsupported geometry as abstention evidence.

## Status

- fold_augmented_confounded_proxy_train_cal_unsupported_geometry_coordinate_locus_scan_protein_only_no_locus_evidence
- Coordinate files scanned: 8/8
- Protein-only AFDB files: 8
- Files with source-free locus evidence: 0
- Ready to score now: 0
- Blockers: ['afdb_predicted_coordinates_do_not_carry_ligands_or_metals', 'inorganic_locus_statuses_still_unsupported']

## Decision

- Background scout can create structural axis now: False
- Score repair rows now: False
- New proxy axis ready now: False
- Next gate: The repaired AFDB-v6 files are protein-only and do not repair the inorganic/cofactor locus feature. Do not register an unsupported-geometry proxy axis from these rows; next progress requires a different source-free structural proxy or reviewed P10746/Lever 4 decisions.

## Scan Rows

| accession | rows | atoms | HETATM | status | locus codes |
| --- | --- | ---: | ---: | --- | --- |
| P15807 | m_csa:610 | 2245 | 0 | protein_only_afdb_no_locus_evidence | none |
| P18548 | m_csa:137 | 2432 | 0 | protein_only_afdb_no_locus_evidence | none |
| P27000 | m_csa:318 | 3814 | 0 | protein_only_afdb_no_locus_evidence | none |
| P68175 | m_csa:360 | 2699 | 0 | protein_only_afdb_no_locus_evidence | none |
| Q46509 | m_csa:105 | 6814 | 0 | protein_only_afdb_no_locus_evidence | none |
| Q56310 | m_csa:327 | 5301 | 0 | protein_only_afdb_no_locus_evidence | none |
| Q7SIE1 | m_csa:649 | 6060 | 0 | protein_only_afdb_no_locus_evidence | none |
| Q9P4R4 | m_csa:618 | 3450 | 0 | protein_only_afdb_no_locus_evidence | none |

## Interpretation

- 8/8 AFDB-v6 repair CIFs were scanned for source-free inorganic/cofactor locus evidence.
- 8 files are protein-only and 0 files expose source-free inorganic/cofactor locus evidence.
- Treat the coordinate-missing blocker as cleared but the inorganic-locus evidence blocker as still open.
