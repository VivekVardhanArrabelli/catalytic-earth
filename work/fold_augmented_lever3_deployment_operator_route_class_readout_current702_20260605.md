# Fold-Augmented Lever 3 Deployment Operator Route-Class Readout - current702

Run: 2026-06-05T13:12:36Z

Operator-facing route-class readout for the current Lever 3 abstain/route manifest. It classifies already-approved hard confounded OOS operator actions by confounder class and verifies that the action surface remains source-current, guardrail-clean, threshold-unchanged, and fail-closed for fixed-threshold scoring.

## Status

- fold_augmented_lever3_deployment_operator_route_class_readout_passed
- Route-class readout ready: True
- Fixed-threshold scoring closure available now: False
- Route-class violations: []

## Counts

- Operator rows abstain/route: 21/21
- Route classes with rows: 5
- Route class counts: {'cofactor_or_same_family_confound': 11, 'fold_similarity_confound': 4, 'pocket_chemistry_confound': 1, 'pocket_geometry_confound': 3, 'protein_descriptor_counteraxis': 2}
- Route stage counts: {'accepted_cofactor_or_same_family_bandpass': 10, 'channel_margin_counteraxis': 2, 'descriptor_generalization_counteraxis': 1, 'fold_cofactor_pressure_counteraxis': 1, 'fold_tm_bandpass_counteraxis': 4, 'geometry_mismatch_counteraxis': 1, 'pairwise_descriptor_counteraxis': 1, 'pocket_chemistry_counteraxis': 1}
- Source hashes current: 2/2
- Calibration retained: 31/34
- Train/cal OOS abstained or routed: 167/204
- Retained residual rows after all counteraxes: 0

## Route Classes

| route class | rows | route stages | entry ids |
| --- | ---: | --- | --- |
| cofactor_or_same_family_confound | 11 | accepted_cofactor_or_same_family_bandpass, fold_cofactor_pressure_counteraxis | m_csa:135, m_csa:223, m_csa:289, m_csa:451, m_csa:463, m_csa:464, m_csa:488, m_csa:502, m_csa:503, m_csa:638, m_csa:646 |
| fold_similarity_confound | 4 | fold_tm_bandpass_counteraxis | m_csa:52, m_csa:74, m_csa:190, m_csa:256 |
| pocket_chemistry_confound | 1 | pocket_chemistry_counteraxis | m_csa:468 |
| pocket_geometry_confound | 3 | channel_margin_counteraxis, geometry_mismatch_counteraxis | m_csa:89, m_csa:229, m_csa:308 |
| protein_descriptor_counteraxis | 2 | descriptor_generalization_counteraxis, pairwise_descriptor_counteraxis | m_csa:25, m_csa:84 |

## Operator Rows

| row | route class | route stage | action | source artifact |
| --- | --- | --- | --- | --- |
| m_csa:25 | protein_descriptor_counteraxis | descriptor_generalization_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_pairwise_descriptor_counteraxis_readout_current702_20260604 |
| m_csa:52 | fold_similarity_confound | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 |
| m_csa:74 | fold_similarity_confound | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 |
| m_csa:84 | protein_descriptor_counteraxis | pairwise_descriptor_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_pairwise_descriptor_counteraxis_readout_current702_20260604 |
| m_csa:89 | pocket_geometry_confound | channel_margin_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 |
| m_csa:135 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 |
| m_csa:190 | fold_similarity_confound | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 |
| m_csa:223 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 |
| m_csa:229 | pocket_geometry_confound | channel_margin_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 |
| m_csa:256 | fold_similarity_confound | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 |
| m_csa:289 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 |
| m_csa:308 | pocket_geometry_confound | geometry_mismatch_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_geometry_mismatch_counteraxis_readout_current702_20260605 |
| m_csa:451 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 |
| m_csa:463 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 |
| m_csa:464 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 |
| m_csa:468 | pocket_chemistry_confound | pocket_chemistry_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_pocket_chemistry_counteraxis_readout_current702_20260605 |
| m_csa:488 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 |
| m_csa:502 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 |
| m_csa:503 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 |
| m_csa:638 | cofactor_or_same_family_confound | fold_cofactor_pressure_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 |
| m_csa:646 | cofactor_or_same_family_confound | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 |

## Checks

| check | passed |
| --- | ---: |
| stage_provenance_reproducibility_audit_passed | True |
| deployment_operator_manifest_audit_passed | True |
| direct_source_hashes_current | True |
| manifest_row_count_matches_stage_provenance | True |
| all_manifest_rows_classified | True |
| all_manifest_rows_abstain_or_route_novel_oos | True |
| no_forced_mechanism_labels | True |
| no_rule_selection_rows | True |
| all_rows_have_entry_id | True |
| all_rows_have_stage_source | True |
| operator_manifest_has_no_forbidden_fields | True |
| operating_point_metrics_available | True |
| zero_retained_residual_rows_after_all_counteraxes | True |
| fixed_threshold_scoring_fail_closed | True |
| safe_abstention_evidence_sufficient | True |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Next gate: Use this route-class readout as the operator-facing explanation layer for abstain/route actions only; keep fixed-threshold scoring closure fail-closed pending exact P07658 coordinate/provenance evidence.

## Guardrails

- Measured readout only. Existing stage-provenance and operator-manifest artifacts only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 operator route classes are ready.
- 21/21 operator rows abstain or route novel/OOS across 5 confounder classes, with 31/34 calibration in-scope rows retained and 167/204 train/cal OOS rows abstained or routed.
- Use the route-classified manifest for abstain/route explanations only; do not score or force mechanism labels.
