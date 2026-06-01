# Mechanism-Feature Embedding Train/Cal Split Manifest - current702

Run: 2026-06-01T12:07:43Z

Deterministic train/cal split manifest for the no-fit mechanism-feature embedding pilot. It partitions only in_distribution rows with the minimal feature bundle ready and carries heldout rows only as an excluded count.

## Status

- mechanism_feature_embedding_train_cal_split_ready_no_model_fit
- Train rows: 418
- Calibration rows: 106
- Heldout excluded rows: 140
- Not-ready rows: 38
- Strata: 6
- Not-ready reasons: {'role_graph:missing_accession_compatible_sequence_positions': 34, 'role_graph:missing_catalytic_residue_nodes': 1, 'role_graph:not_m_csa_no_curated_active_site_roles': 3}

## Strata

| stratum | total | train | calibration |
| --- | ---: | ---: | ---: |
| `fingerprint:flavin_dehydrogenase_reductase` | 38 | 30 | 8 |
| `fingerprint:heme_peroxidase_oxidase` | 14 | 11 | 3 |
| `fingerprint:metal_dependent_hydrolase` | 64 | 51 | 13 |
| `fingerprint:plp_dependent_enzyme` | 24 | 19 | 5 |
| `fingerprint:ser_his_acid_hydrolase` | 31 | 25 | 6 |
| `label_type:out_of_scope` | 353 | 282 | 71 |

## Interpretation

- 418 train and 106 calibration rows are ready for an explicitly authorized no-fit embedding pilot.
- If model fitting is authorized later, fit only on assigned train rows, select any operating threshold only on calibration rows, and evaluate heldout once.
