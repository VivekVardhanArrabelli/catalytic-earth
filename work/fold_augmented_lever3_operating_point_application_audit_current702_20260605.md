# Fold-Augmented Lever 3 Operating-Point Application Audit - current702

Run: 2026-06-05T10:22:46Z

Row-level application audit for the current Lever 3 abstain/route operating point. It consumes the closure readout and the closure reproducibility audit, then verifies that each hard confounded residual row has an evidence-backed abstain/route action and no forced mechanism label.

## Status

- fold_augmented_lever3_operating_point_application_audit_passed
- Operating-point application contract ready: True
- Safe abstention route remains current: True
- Fixed-threshold scoring closure available now: False
- Application violations: []

## Operating Point

- Route ID: fixed_baseline_plus_accepted_counteraxes_plus_descriptor_plus_channel_margin_fold_pressure_plus_pocket_chemistry_plus_geometry_mismatch
- Baseline threshold: 0.44155
- Threshold selection source: train_calibration_only
- Calibration retained: 31/34 (0.911765)
- Train/cal OOS abstained or routed: 167/204 (0.818627)
- Retained residual rows after all counteraxes: 0

## Counts

- Application rows abstain/route: 21/21
- Application rows with stage source: 21/21
- Stage count mismatches: 0
- Forced mechanism-label rows: 0
- Unsafe non-abstain residual action rows: 0

## Application Checks

| check | passed |
| --- | ---: |
| closure_reproducibility_audit_passed | True |
| closure_rebuild_hash_matches_stored | True |
| closure_source_hashes_current | True |
| closure_readout_closed | True |
| deployment_valid_safe_route_available | True |
| application_row_count_matches_closure | True |
| all_application_rows_have_stage_source | True |
| stage_counts_match_closure | True |
| all_application_rows_abstain_or_route_novel_oos | True |
| no_forced_mechanism_labels | True |
| application_rows_not_used_for_rule_selection | True |
| zero_retained_residual_rows | True |
| zero_residual_rows_without_final_route | True |
| true_in_scope_retention_above_90_percent | True |
| train_cal_oos_operating_point_present | True |
| fixed_threshold_scoring_fail_closed | True |
| threshold_not_changed | True |
| no_row_scoring_provider_or_coordinate_changes | True |
| no_heldout_metadata_label_or_import_shortcuts | True |

## Stage Counts

| route stage | expected | observed | matches |
| --- | ---: | ---: | ---: |
| accepted_cofactor_or_same_family_bandpass | 10 | 10 | True |
| descriptor_generalization_counteraxis | 1 | 1 | True |
| pairwise_descriptor_counteraxis | 1 | 1 | True |
| channel_margin_counteraxis | 2 | 2 | True |
| fold_tm_bandpass_counteraxis | 4 | 4 | True |
| fold_cofactor_pressure_counteraxis | 1 | 1 | True |
| pocket_chemistry_counteraxis | 1 | 1 | True |
| geometry_mismatch_counteraxis | 1 | 1 | True |

## Application Rows

| row | accession | route stage | action | source artifact | force label |
| --- | --- | --- | --- | --- | ---: |
| m_csa:25 | P32400 | descriptor_generalization_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_pairwise_descriptor_counteraxis_readout_current702_20260604 | False |
| m_csa:52 | P0AB71 | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 | False |
| m_csa:74 | P13000 | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 | False |
| m_csa:84 | P27213 | pairwise_descriptor_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_pairwise_descriptor_counteraxis_readout_current702_20260604 | False |
| m_csa:89 | Q55012 | channel_margin_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 | False |
| m_csa:135 | P14925 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 | False |
| m_csa:190 | Q46822 | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 | False |
| m_csa:223 | Q2K340 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 | False |
| m_csa:229 | P9WIL5 | channel_margin_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 | False |
| m_csa:256 | P00327 | fold_tm_bandpass_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 | False |
| m_csa:289 | P07342 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 | False |
| m_csa:308 | P12070 | geometry_mismatch_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_geometry_mismatch_counteraxis_readout_current702_20260605 | False |
| m_csa:451 | P0AES2 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 | False |
| m_csa:463 | Q89FH0 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 | False |
| m_csa:464 | P11766 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 | False |
| m_csa:468 | Q05514 | pocket_chemistry_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_pocket_chemistry_counteraxis_readout_current702_20260605 | False |
| m_csa:488 | P32170 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 | False |
| m_csa:502 | Q8EMJ9 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 | False |
| m_csa:503 | B9JNP7 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 | False |
| m_csa:638 | P42676 | fold_cofactor_pressure_counteraxis | abstain_or_route_novel_oos | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 | False |
| m_csa:646 | P31939 | accepted_cofactor_or_same_family_bandpass | abstain_or_route_novel_oos | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 | False |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Operator action: apply row-level abstain_or_route_novel_oos actions for hard confounded residual rows; do not force mechanism labels
- Exact missing evidence for scoring closure: ['one credentialed provider route or local predictor that accepts the exact 715-aa P07658 FASTA', 'returned full-length coordinate file at the preferred staging path', 'filled provenance with provider/model/version/path/checksum, input sequence hash, and documented U140 handling', 'P07658 acceptance preflight with all required checks passing']
- Next gate: Use this application audit as the row-level contract for the current Lever 3 abstain/route operating point; keep threshold 0.44155 unchanged and fixed-threshold scoring fail-closed pending the separate exact P07658 coordinate/provenance route.

## Guardrails

- Measured readout only. Existing closure and reproducibility artifacts only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 operating-point application contract is ready.
- 21 hard residual rows have row-level abstain/route actions, 0 forced mechanism labels, 0 missing stage sources, and 0 retained hard residual rows after all counteraxes.
- Apply the current closure as an abstain/route gate only; keep fixed-threshold scoring closure fail-closed.
