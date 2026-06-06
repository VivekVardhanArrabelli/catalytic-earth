# Fold-Augmented Lever 3 Deployment Operator Transfer-Safety Matrix Readout - current702

Run: 2026-06-05T14:11:21Z

Operator transfer-safety matrix for the current Lever 3 route-class/provenance chain. It converts route classes into allowed deployment actions and verifies that every hard confounded row remains abstain/route novel-OOS with mechanism transfer, scoring, and threshold changes disallowed.

## Status

- fold_augmented_lever3_deployment_operator_transfer_safety_matrix_readout_passed
- Transfer-safety matrix ready: True
- Mechanism transfer disallowed for all rows: True
- Fixed-threshold scoring closure available now: False
- Transfer-safety violations: []

## Counts

- Operator rows safe-to-abstain/route: 21/21
- Operator rows abstain/route novel-OOS: 21/21
- Route classes with rows: 5
- Route class counts: {'cofactor_or_same_family_confound': 11, 'fold_similarity_confound': 4, 'pocket_chemistry_confound': 1, 'pocket_geometry_confound': 3, 'protein_descriptor_counteraxis': 2}
- Route-class stage-source links lineage-covered: 7/7
- Route-class stage-source links guardrail-clean: 7/7
- Route-class stage-source links hash-current: 7/7
- Direct source hashes current: 3/3
- Calibration retention: 31/34
- Train/cal OOS abstain or route: 167/204
- Retained residual rows after all counteraxes: 0

## Transfer-Safety Matrix

| route class | rows | allowed action | transfer allowed | stage links clean | entry ids |
| --- | ---: | --- | ---: | ---: | --- |
| cofactor_or_same_family_confound | 11 | abstain_or_route_novel_oos | False | 2/2 | m_csa:135, m_csa:223, m_csa:289, m_csa:451, m_csa:463, m_csa:464, m_csa:488, m_csa:502, m_csa:503, m_csa:638, m_csa:646 |
| fold_similarity_confound | 4 | abstain_or_route_novel_oos | False | 1/1 | m_csa:52, m_csa:74, m_csa:190, m_csa:256 |
| pocket_chemistry_confound | 1 | abstain_or_route_novel_oos | False | 1/1 | m_csa:468 |
| pocket_geometry_confound | 3 | abstain_or_route_novel_oos | False | 2/2 | m_csa:89, m_csa:229, m_csa:308 |
| protein_descriptor_counteraxis | 2 | abstain_or_route_novel_oos | False | 1/1 | m_csa:25, m_csa:84 |

## Row Safety Records

| entry | route class | route stage | observed action | safe | transfer allowed | provenance clean |
| --- | --- | --- | --- | ---: | ---: | ---: |
| m_csa:25 | protein_descriptor_counteraxis | descriptor_generalization_counteraxis | abstain_or_route_novel_oos | True | False | True |
| m_csa:52 | fold_similarity_confound | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | True | False | True |
| m_csa:74 | fold_similarity_confound | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | True | False | True |
| m_csa:84 | protein_descriptor_counteraxis | pairwise_descriptor_counteraxis | abstain_or_route_novel_oos | True | False | True |
| m_csa:89 | pocket_geometry_confound | channel_margin_counteraxis | abstain_or_route_novel_oos | True | False | True |
| m_csa:135 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | True | False | True |
| m_csa:190 | fold_similarity_confound | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | True | False | True |
| m_csa:223 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | True | False | True |
| m_csa:229 | pocket_geometry_confound | channel_margin_counteraxis | abstain_or_route_novel_oos | True | False | True |
| m_csa:256 | fold_similarity_confound | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | True | False | True |
| m_csa:289 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | True | False | True |
| m_csa:308 | pocket_geometry_confound | geometry_mismatch_counteraxis | abstain_or_route_novel_oos | True | False | True |
| m_csa:451 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | True | False | True |
| m_csa:463 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | True | False | True |
| m_csa:464 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | True | False | True |
| m_csa:468 | pocket_chemistry_confound | pocket_chemistry_counteraxis | abstain_or_route_novel_oos | True | False | True |
| m_csa:488 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | True | False | True |
| m_csa:502 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | True | False | True |
| m_csa:503 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | True | False | True |
| m_csa:638 | cofactor_or_same_family_confound | fold_cofactor_pressure_counteraxis | abstain_or_route_novel_oos | True | False | True |
| m_csa:646 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | True | False | True |

## Checks

| check | passed |
| --- | ---: |
| route_class_readout_passed | True |
| route_class_provenance_readout_passed | True |
| route_class_provenance_reproducibility_audit_passed | True |
| direct_source_hashes_current | True |
| operator_row_count_matches_route_class_readout | True |
| all_operator_rows_have_transfer_safety_records | True |
| all_operator_rows_abstain_or_route_novel_oos | True |
| all_operator_rows_safe_to_abstain_or_route | True |
| no_operator_rows_allow_mechanism_transfer | True |
| no_operator_rows_allow_scoring_or_forced_labels | True |
| no_operator_rows_allow_threshold_change | True |
| no_operator_rows_used_for_rule_selection | True |
| all_operator_rows_have_clean_provenance | True |
| route_class_counts_match_readout | True |
| matrix_covers_all_route_classes | True |
| matrix_stage_source_links_match_provenance | True |
| matrix_stage_sources_lineage_covered_guardrail_clean_hash_current | True |
| operating_point_metrics_match_sources | True |
| calibration_retention_stays_high_at_operating_point | True |
| hard_confounded_rows_all_abstain_or_route | True |
| train_cal_oos_abstention_stays_current | True |
| fixed_threshold_scoring_fail_closed | True |
| predicted_source_free_evidence_sufficient_for_safe_abstention | True |
| no_forbidden_guardrail_hits_in_sources | True |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Operator action: apply_transfer_safety_matrix_to_abstain_or_route_novel_oos
- Next gate: Use the transfer-safety matrix for operator abstain/route decisions only; keep mechanism transfer and fixed-threshold scoring closure fail-closed pending exact P07658 evidence.

## Guardrails

- Measured readout only. Existing route-class, provenance, and provenance-reproducibility artifacts only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 transfer-safety matrix is ready.
- 21/21 operator rows are safe-to-abstain/route, with mechanism transfer allowed for 0 rows across 5 route classes.
- Apply only the abstain/route novel-OOS action for rows in the matrix.
