# Active-Site Cache 41 Unsupervised Router Stress - 2026-05-28
Review-only diagnostic. Distances used only `predictive_features`; labels/fingerprints/source groups were metadata-only after scoring.

## Summary
- `row_count`: 41
- `input_cache_counts`: {'artifacts/v3_active_site_encoder_cache_wave1_2_31_20260528.jsonl': 31, 'artifacts/v3_active_site_encoder_cache_local_tail_extension_10_20260528.jsonl': 10}
- `source_group_counts`: {'clean_near_orphan_anchor': 7, 'fold_conflict_reference_anchor': 3, 'oos_router_control': 9, 'external_router_priority': 12, 'current702_local_tail_extension': 10}
- `nearest_neighbor_cross_source_group_count`: 31
- `nearest_neighbor_cross_source_group_rate`: 0.7561
- `mean_nearest_distance_by_source_group`: {'clean_near_orphan_anchor': 20.2209, 'fold_conflict_reference_anchor': 25.8785, 'oos_router_control': 24.8089, 'external_router_priority': 29.4933, 'current702_local_tail_extension': 28.7425}
- `local_tail_row_count`: 10
- `local_tail_nearest_neighbor_source_group_counts`: {'current702_local_tail_extension': 5, 'external_router_priority': 3, 'clean_near_orphan_anchor': 2}
- `local_tail_nearest_neighbor_fingerprint_metadata_counts`: {'metal_dependent_hydrolase': 3, 'None': 6, 'flavin_dehydrogenase_reductase': 1}
- `local_tail_expected_pattern_pass_count`: 10
- `local_tail_expected_pattern_failure_count`: 0
- `interpretation`: This is a label-blind unsupervised stress diagnostic, not performance evidence. The 41-row cache is ready for review-only router diagnostics; supervised claims still require a separate leakage-safe gate.

## Local-tail expected-pattern checks
- `m_csa:15`: PASS | positive_tail_has_metal_hydrolase_neighbor_in_top5 | top5 fp metadata ['metal_dependent_hydrolase', 'metal_dependent_hydrolase', 'None', 'None', 'metal_dependent_hydrolase']
- `m_csa:258`: PASS | positive_tail_has_metal_hydrolase_neighbor_in_top5 | top5 fp metadata ['None', 'metal_dependent_hydrolase', 'None', 'metal_dependent_hydrolase', 'None']
- `m_csa:158`: PASS | positive_tail_has_metal_hydrolase_neighbor_in_top5 | top5 fp metadata ['metal_dependent_hydrolase', 'None', 'None', 'None', 'None']
- `m_csa:178`: PASS | oos_tail_not_exclusively_primary_metal_in_top5 | top5 fp metadata ['None', 'metal_dependent_hydrolase', 'None', 'None', 'flavin_dehydrogenase_reductase']
- `m_csa:179`: PASS | oos_tail_not_exclusively_primary_metal_in_top5 | top5 fp metadata ['None', 'None', 'None', 'None', 'metal_dependent_hydrolase']
- `m_csa:533`: PASS | oos_tail_not_exclusively_primary_metal_in_top5 | top5 fp metadata ['None', 'None', 'None', 'flavin_dehydrogenase_reductase', 'None']
- `m_csa:534`: PASS | oos_tail_not_exclusively_primary_metal_in_top5 | top5 fp metadata ['None', 'None', 'metal_dependent_hydrolase', 'None', 'None']
- `m_csa:216`: PASS | positive_tail_has_metal_hydrolase_neighbor_in_top5 | top5 fp metadata ['None', 'None', 'None', 'metal_dependent_hydrolase', 'None']
- `m_csa:516`: PASS | positive_tail_has_metal_hydrolase_neighbor_in_top5 | top5 fp metadata ['metal_dependent_hydrolase', 'None', 'None', 'metal_dependent_hydrolase', 'None']
- `m_csa:54`: PASS | oos_tail_not_exclusively_primary_metal_in_top5 | top5 fp metadata ['flavin_dehydrogenase_reductase', 'None', 'metal_dependent_hydrolase', 'None', 'None']

## Guardrails
- `coordinate_fetches_performed`: False
- `labels_changed`: False
- `registries_changed`: False
- `ontologies_changed`: False
- `production_scoring_changed`: False
- `thresholds_changed`: False
- `training_executed`: False
- `metadata_used_as_predictive_input`: False
