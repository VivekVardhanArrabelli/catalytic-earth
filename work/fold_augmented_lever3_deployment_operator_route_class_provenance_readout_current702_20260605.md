# Fold-Augmented Lever 3 Deployment Operator Route-Class Provenance Readout - current702

Run: 2026-06-05T13:20:48Z

Class-level provenance readout for the current Lever 3 operator route-class table. It verifies that every route-class/stage-source link is present in clean stage provenance, lineage-covered, source-hash current, guardrail-clean, and still fail-closed for fixed-threshold scoring.

## Status

- fold_augmented_lever3_deployment_operator_route_class_provenance_readout_passed
- Route-class provenance ready: True
- Fixed-threshold scoring closure available now: False
- Provenance violations: []

## Counts

- Route-class stage-source links present: 7/7
- Route-class stage-source links lineage-covered: 7/7
- Route-class stage-source links guardrail-clean: 7/7
- Route-class stage-source links hash-current: 7/7
- Route-class stage-source counts: {'cofactor_or_same_family_confound': 2, 'fold_similarity_confound': 1, 'pocket_chemistry_confound': 1, 'pocket_geometry_confound': 2, 'protein_descriptor_counteraxis': 1}
- Operator rows abstain/route: 21/21
- Calibration retained: 31/34
- Train/cal OOS abstained or routed: 167/204

## Route-Class Stage Sources

| route class | source artifact | rows | lineage | clean | hashes | entry ids |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| cofactor_or_same_family_confound | v3_fold_augmented_lever3_deployment_action_readout_current702_20260604 | 10 | True | True | True | m_csa:135, m_csa:223, m_csa:289, m_csa:451, m_csa:463, m_csa:464, m_csa:488, m_csa:502, m_csa:503, m_csa:646 |
| cofactor_or_same_family_confound | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 | 1 | True | True | True | m_csa:638 |
| fold_similarity_confound | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 | 4 | True | True | True | m_csa:52, m_csa:74, m_csa:190, m_csa:256 |
| pocket_chemistry_confound | v3_fold_augmented_lever3_retained_pocket_chemistry_counteraxis_readout_current702_20260605 | 1 | True | True | True | m_csa:468 |
| pocket_geometry_confound | v3_fold_augmented_lever3_retained_channel_margin_counteraxis_readout_current702_20260604 | 2 | True | True | True | m_csa:89, m_csa:229 |
| pocket_geometry_confound | v3_fold_augmented_lever3_retained_geometry_mismatch_counteraxis_readout_current702_20260605 | 1 | True | True | True | m_csa:308 |
| protein_descriptor_counteraxis | v3_fold_augmented_lever3_retained_pairwise_descriptor_counteraxis_readout_current702_20260604 | 2 | True | True | True | m_csa:25, m_csa:84 |

## Checks

| check | passed |
| --- | ---: |
| route_class_readout_passed | True |
| stage_provenance_audit_passed | True |
| direct_source_hashes_current | True |
| all_route_class_stage_sources_present | True |
| all_route_class_stage_sources_lineage_covered | True |
| all_route_class_stage_sources_guardrail_clean | True |
| all_route_class_stage_source_hashes_current | True |
| route_class_counts_match_readout | True |
| stage_source_counts_match_stage_provenance | True |
| safe_operator_actions_remain_current | True |
| fixed_threshold_scoring_fail_closed | True |

## Decision

- Predicted/source-free evidence enough for safe abstention: True
- Predicted/source-free evidence enough for fixed-threshold scoring closure: False
- Unsafe forced mechanism transfer allowed: False
- Next gate: Use route-class provenance as the class-level audit trail for abstain/route explanations only; keep fixed-threshold scoring closure fail-closed pending exact P07658 evidence.

## Guardrails

- Measured readout only. Existing route-class and stage-provenance artifacts only; no new rule selection, row scoring, coordinates, labels, registries, ontologies, imports, production threshold changes, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 route-class provenance is clean.
- 7/7 route-class stage-source links are lineage-covered and 7/7 are guardrail-clean.
- Use the class-level provenance readout for abstain/route explanations only; do not score or force mechanism labels.
