# Wave 1.2 Decoder/Join Confound Audit

Run: 2026-05-29T04:02:14Z
Automation: `catalytic-earth-work-loop`
Scope: current702 heldout rows from `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`. No labels, registries, ontologies, imports, production scoring, or global thresholds were edited. No heldout threshold tuning or large downloads were performed.

## Answer

Geometry join policy was a real confound in the prior model-by-cell report: the preview geometry eval joined 135/140 heldout rows and missed `m_csa:577, m_csa:599, m_csa:710, m_csa:892, m_csa:897`. Re-exporting from the full geometry retrieval artifact joins 140/140 rows.

Decoder choice is also a real learned-representation confound. The same ESM-C representation is 37.8% primary accuracy with the logistic head versus 8.9% with cosine NN, and its OOS/secondary false-positive rate changes from 16.8% to 34.7%. ProtT5 and SaProt cannot receive the matched logistic-head treatment locally because raw sidecars/weights are absent; their existing exports are NN/cosine readouts only.

## Geometry Re-export

- Join key: `entry_id`, left-joined from the standardized 140 heldout rows.
- Missing/non-joined rows in the re-export: none.
- Prior preview missing rows now recovered: `m_csa:577, m_csa:599, m_csa:710, m_csa:892, m_csa:897`.
- Canonical primary: 45/45 correct with 0 abstentions.
- Pure OOS: 0/92 false positives.
- OOS plus secondary probes: 2/95 nonabstained; both are true secondary fingerprints, not pure OOS rows.

## Decoder Comparison

| Track | Decoder | Joined | Primary support | Primary abstain | Primary acc | OOS/sec support | OOS/sec abstain | OOS/sec FP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Active-site geometry baseline re-export | hand_scored_geometry_retrieval | 140/140 | 45 | 0 | 100.0% | 95 | 93 | 2.1% |
| Geometry-feature logistic head | logistic_head | 140/140 | 45 | 15 | 66.7% | 95 | 91 | 4.2% |
| ESM-2 150M logistic | logistic_head | 140/140 | 45 | 19 | 57.8% | 95 | 79 | 16.8% |
| ESM-C 300M corrected logistic | logistic_head | 140/140 | 45 | 24 | 37.8% | 95 | 79 | 16.8% |
| ESM-C 300M cosine NN | cosine_nearest_neighbor | 140/140 | 45 | 30 | 8.9% | 95 | 62 | 34.7% |
| ProtT5 Swiss-Prot H5 cosine NN | cosine_nearest_neighbor | 132/140 | 45 | 19 | 39.5% | 95 | 67 | 24.7% |
| SaProt 35M structure-token NN | nearest_neighbor | 140/140 | 45 | 23 | 33.3% | 95 | 76 | 20.0% |
| Foldseek full-structure NN | nearest_neighbor | 140/140 | 45 | 12 | 62.2% | 95 | 86 | 9.5% |
| Sequence-NN 3-mer Jaccard | nearest_neighbor_jaccard | 140/140 | 45 | 33 | 15.6% | 95 | 68 | 28.4% |

## Per-bin Results

Support and abstention counts are shown before accuracy.

| Bin | Track | Rows | Primary support | Primary abstain | Primary acc | OOS/sec support | OOS/sec abstain | OOS/sec FP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| low_structure_neighborhood_near_orphan | Active-site geometry baseline re-export | 30 | 30 | 0 | 100.0% | 0 | 0 | n/a |
| low_structure_neighborhood_near_orphan | Geometry-feature logistic head | 30 | 30 | 10 | 66.7% | 0 | 0 | n/a |
| low_structure_neighborhood_near_orphan | ESM-2 150M logistic | 30 | 30 | 14 | 53.3% | 0 | 0 | n/a |
| low_structure_neighborhood_near_orphan | ESM-C 300M corrected logistic | 30 | 30 | 16 | 33.3% | 0 | 0 | n/a |
| low_structure_neighborhood_near_orphan | ESM-C 300M cosine NN | 30 | 30 | 20 | 10.0% | 0 | 0 | n/a |
| low_structure_neighborhood_near_orphan | ProtT5 Swiss-Prot H5 cosine NN | 30 | 30 | 15 | 27.6% | 0 | 0 | n/a |
| low_structure_neighborhood_near_orphan | SaProt 35M structure-token NN | 30 | 30 | 12 | 36.7% | 0 | 0 | n/a |
| low_structure_neighborhood_near_orphan | Foldseek full-structure NN | 30 | 30 | 7 | 60.0% | 0 | 0 | n/a |
| no_reliable_structure | Active-site geometry baseline re-export | 6 | 5 | 0 | 100.0% | 1 | 1 | 0.0% |
| no_reliable_structure | Geometry-feature logistic head | 6 | 5 | 2 | 60.0% | 1 | 0 | 100.0% |
| no_reliable_structure | ESM-2 150M logistic | 6 | 5 | 2 | 60.0% | 1 | 1 | 0.0% |
| no_reliable_structure | ESM-C 300M corrected logistic | 6 | 5 | 2 | 60.0% | 1 | 1 | 0.0% |
| no_reliable_structure | ESM-C 300M cosine NN | 6 | 5 | 3 | 0.0% | 1 | 1 | 0.0% |
| no_reliable_structure | ProtT5 Swiss-Prot H5 cosine NN | 6 | 5 | 2 | 40.0% | 1 | 0 | n/a |
| no_reliable_structure | SaProt 35M structure-token NN | 6 | 5 | 5 | 0.0% | 1 | 1 | 0.0% |
| no_reliable_structure | Foldseek full-structure NN | 6 | 5 | 5 | 0.0% | 1 | 1 | 0.0% |
| dense_same_mechanism_structural_neighborhood | Active-site geometry baseline re-export | 10 | 10 | 0 | 100.0% | 0 | 0 | n/a |
| dense_same_mechanism_structural_neighborhood | Geometry-feature logistic head | 10 | 10 | 3 | 70.0% | 0 | 0 | n/a |
| dense_same_mechanism_structural_neighborhood | ESM-2 150M logistic | 10 | 10 | 3 | 70.0% | 0 | 0 | n/a |
| dense_same_mechanism_structural_neighborhood | ESM-C 300M corrected logistic | 10 | 10 | 6 | 40.0% | 0 | 0 | n/a |
| dense_same_mechanism_structural_neighborhood | ESM-C 300M cosine NN | 10 | 10 | 7 | 10.0% | 0 | 0 | n/a |
| dense_same_mechanism_structural_neighborhood | ProtT5 Swiss-Prot H5 cosine NN | 10 | 10 | 2 | 77.8% | 0 | 0 | n/a |
| dense_same_mechanism_structural_neighborhood | SaProt 35M structure-token NN | 10 | 10 | 6 | 40.0% | 0 | 0 | n/a |
| dense_same_mechanism_structural_neighborhood | Foldseek full-structure NN | 10 | 10 | 0 | 100.0% | 0 | 0 | n/a |
| fold_conflict_oos_hard_negative | Active-site geometry baseline re-export | 11 | 0 | 0 | n/a | 11 | 11 | 0.0% |
| fold_conflict_oos_hard_negative | Geometry-feature logistic head | 11 | 0 | 0 | n/a | 11 | 10 | 9.1% |
| fold_conflict_oos_hard_negative | ESM-2 150M logistic | 11 | 0 | 0 | n/a | 11 | 9 | 18.2% |
| fold_conflict_oos_hard_negative | ESM-C 300M corrected logistic | 11 | 0 | 0 | n/a | 11 | 9 | 18.2% |
| fold_conflict_oos_hard_negative | ESM-C 300M cosine NN | 11 | 0 | 0 | n/a | 11 | 5 | 54.5% |
| fold_conflict_oos_hard_negative | ProtT5 Swiss-Prot H5 cosine NN | 11 | 0 | 0 | n/a | 11 | 9 | 18.2% |
| fold_conflict_oos_hard_negative | SaProt 35M structure-token NN | 11 | 0 | 0 | n/a | 11 | 10 | 9.1% |
| fold_conflict_oos_hard_negative | Foldseek full-structure NN | 11 | 0 | 0 | n/a | 11 | 11 | 0.0% |

## Logistic-head Feasibility

ProtT5: blocked. Existing heldout NN export is missing 8 rows: `m_csa:67, m_csa:201, m_csa:372, m_csa:428, m_csa:453, m_csa:509, m_csa:634, m_csa:688`. No raw ProtT5 H5/sidecar or local weights were found.

SaProt: blocked. Existing heldout NN export joins all rows, but no raw SaProt embedding/structure-token sidecar or local weights were found, so a matched logistic head would require sidecar implementation or downloads outside this audit.

Geometry-feature logistic head: evaluated_train_cal_only_threshold. It used train/cal rows only, selected its abstention threshold on calibration rows only, and reached 66.7% primary accuracy with 4.2% OOS/secondary false-positive rate. The hand-scored geometry router remains stronger on this audit.

## Gate

Decision: `geometry_first_router`.

Rationale: The geometry baseline re-export joins all 140 standardized heldout rows and removes the prior 5-row preview join gap. With the existing calibrated geometry abstention threshold, hand-scored geometry is 45/45 on canonical primary rows and 0/92 false positives on pure out-of-scope rows; only secondary OOD probes are nonabstained because they are real registry fingerprints. ESM-C logistic versus ESM-C cosine demonstrates decoder confounding, and ProtT5/SaProt matched logistic reruns are blocked by missing raw sidecars rather than by a model result.

## Verification

- JSON parse: passed with `jq`.
- CLI validate: passed with `PYTHONPATH=src python -m catalytic_earth.cli validate`.
- Diff whitespace: passed with `git diff --check`.
- Disk headroom after run: 26.06 GiB free.
