# Fold-Augmented Lever 3 Operating-Point Closure Readout - current702

Run: 2026-06-05T09:16:25Z

Lever 3 deployment-valid operating-point closure readout. It composes already-selected source-free train/cal counteraxis readouts for hard retained same-family transfer residuals and checks whether the current abstain/route operating point closes unsafe mechanism transfer without changing thresholds, scoring rows, staging coordinates, or using heldout rows.

## Status

- fold_augmented_lever3_operating_point_closure_readout_closed
- Deployment-valid safe abstention route available now: True
- Zero residual retained-transfer risk available now: True
- Fixed-threshold scoring closure available now: False
- Guardrail violations: []
- Closure consistency checks pass: True

## Operating Point

- Route ID: fixed_baseline_plus_accepted_counteraxes_plus_descriptor_plus_channel_margin_fold_pressure_plus_pocket_chemistry_plus_geometry_mismatch
- Baseline threshold: 0.44155
- Threshold selection source: train_calibration_only
- Threshold/value changed now: False
- Calibration retained: 31/34 (0.911765)
- Train/cal OOS abstained or routed: 167/204 (0.818627)
- Retained residual rows after all counteraxes: 0

## Residual Route Stages

| stage | rows routed | remaining after stage | entry ids |
| --- | ---: | ---: | --- |
| accepted_cofactor_or_same_family_bandpass | 10 | 11 | m_csa:135, m_csa:223, m_csa:289, m_csa:451, m_csa:463, m_csa:464, m_csa:488, m_csa:502, m_csa:503, m_csa:646 |
| descriptor_generalization_and_pairwise | 2 | 9 | m_csa:25, m_csa:84 |
| channel_margin_fold_bandpass_and_fold_cofactor_pressure | 7 | 2 | m_csa:52, m_csa:74, m_csa:89, m_csa:190, m_csa:229, m_csa:256, m_csa:638 |
| pocket_chemistry | 1 | 1 | m_csa:468 |
| geometry_mismatch | 1 | 0 | m_csa:308 |

## Operating Traces

| stage | train/cal OOS abstained or routed |
| --- | ---: |
| accepted_counteraxes | 105 |
| descriptor_plus_accepted | 110 |
| channel_margin_fold_pressure | 165 |
| pocket_chemistry | 165 |
| geometry_mismatch | 167 |

| stage | calibration in-scope retained |
| --- | ---: |
| deployment_action | 31 |
| channel_margin | 31 |
| pocket_chemistry | 31 |
| geometry_mismatch | 31 |

## Counts

- Residual rows entering closure: 21
- Residual rows abstained/routed after all counteraxes: 21
- Residual rows without final route: 0
- P07658 fail-closed action rows: 1

## Consistency Checks

| check | passed |
| --- | ---: |
| residual_row_count_matches_deployment_artifact | True |
| accepted_counteraxis_count_matches_deployment_artifact | True |
| descriptor_stage_count_matches_pairwise_artifact | True |
| channel_stage_count_matches_channel_artifact | True |
| pocket_stage_count_matches_pocket_artifact | True |
| geometry_stage_count_matches_geometry_artifact | True |
| final_residual_count_matches_geometry_artifact | True |
| train_cal_oos_abstention_trace_monotonic | True |
| calibration_retention_trace_stable | True |
| source_artifact_statuses_ready | True |

## Source Status Checks

| check | passed |
| --- | ---: |
| deployment_action_readout_ready | True |
| pairwise_counteraxis_selected | True |
| channel_margin_counteraxis_selected | True |
| pocket_chemistry_counteraxis_selected | True |
| geometry_mismatch_counteraxis_selected | True |
| source_artifacts_all_measured_readouts | True |
| source_artifacts_no_blocker_packets | True |
| source_artifacts_no_candidate_rows_scored_now | True |
| source_artifacts_no_threshold_value_changes | True |
| source_artifacts_no_production_threshold_changes | True |
| source_artifacts_no_experimental_pdb_metadata_shortcut | True |

## Residual Row Actions

| row | accession | route stage | action | force label |
| --- | --- | --- | --- | ---: |
| m_csa:25 | P32400 | descriptor_generalization_counteraxis | abstain_or_route_novel_oos | False |
| m_csa:52 | P0AB71 | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | False |
| m_csa:74 | P13000 | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | False |
| m_csa:84 | P27213 | pairwise_descriptor_counteraxis | abstain_or_route_novel_oos | False |
| m_csa:89 | Q55012 | channel_margin_counteraxis | abstain_or_route_novel_oos | False |
| m_csa:135 | P14925 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | False |
| m_csa:190 | Q46822 | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | False |
| m_csa:223 | Q2K340 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | False |
| m_csa:229 | P9WIL5 | channel_margin_counteraxis | abstain_or_route_novel_oos | False |
| m_csa:256 | P00327 | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | False |
| m_csa:289 | P07342 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | False |
| m_csa:308 | P12070 | geometry_mismatch_counteraxis | abstain_or_route_novel_oos | False |
| m_csa:451 | P0AES2 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | False |
| m_csa:463 | Q89FH0 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | False |
| m_csa:464 | P11766 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | False |
| m_csa:468 | Q05514 | pocket_chemistry_counteraxis | abstain_or_route_novel_oos | False |
| m_csa:488 | P32170 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | False |
| m_csa:502 | Q8EMJ9 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | False |
| m_csa:503 | B9JNP7 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | False |
| m_csa:638 | P42676 | fold_cofactor_pressure_counteraxis | abstain_or_route_novel_oos | False |
| m_csa:646 | P31939 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | False |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Operator action: abstain_or_route_novel_oos_for_all_hard_retained_residuals; do_not_force_mechanism_labels; keep fixed-threshold scoring closure fail-closed
- Exact missing evidence for scoring closure: ['one credentialed provider route or local predictor that accepts the exact 715-aa P07658 FASTA', 'returned full-length coordinate file at the preferred staging path', 'filled provenance with provider/model/version/path/checksum, input sequence hash, and documented U140 handling', 'P07658 acceptance preflight with all required checks passing']
- Next gate: Use this closure readout as the current Lever 3 abstain/route operating point. Do not change threshold 0.44155 or force mechanism labels; fixed-threshold scoring closure remains blocked only on the separate exact P07658 coordinate/provenance route.

## Guardrails

- Measured readout only. Existing source-free artifacts only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 has a deployment-valid abstain/route operating point with 0 retained residual rows.
- The composed route keeps 31/34 calibration in-scope rows and abstains or routes 167/204 train/cal OOS rows, while routing all hard retained residuals instead of assigning mechanism labels.
- Harden this closure with source-hash and reproducibility checks; fixed-threshold scoring closure is a separate P07658 coordinate/provenance task.
