# Fold-Augmented Lever 3 Deployment Action Readout - current702

Run: 2026-06-05T03:25:13Z

Lever 3 measured deployment-action readout. It composes the residual-safety rows, accepted cofactor-context counteraxis, accepted same-family numeric bandpass contract, and fail-closed P07658 abstention policy into row-level deployment actions. It scores no rows, stages no coordinates, changes no thresholds, and uses no heldout rows for threshold selection.

## Status

- fold_augmented_lever3_deployment_action_readout_ready_fail_closed_p07658
- Safe abstention routing available: True
- Fixed-threshold scoring closure available: False
- Full residual row abstention coverage: False

## Operating Point

- Route: fixed_baseline_plus_cofactor_context_counteraxis_plus_same_family_numeric_bandpass_counteraxis_contract
- Baseline threshold: 0.44155
- Calibration retained: 31/34
- Train/cal OOS abstained: 105/204
- Hard-confounded residual target covered: True

## Residual Actions

- Residual rows abstained by accepted counteraxes: 10/21
- Residual rows retained after accepted counteraxes: 11
- Retained residual rows with/missing pocket descriptors: 2/9
- Best retention-preserving top bandpass rule residual rows fired: 9
- Stronger retention-preserving top bandpass rule found: False

| row | axes | action | sources | retained evidence need |
| --- | --- | --- | --- | --- |
| m_csa:25 | same_family | retain_at_fixed_operating_point_not_scoring_closure | none | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:52 | same_family | retain_at_fixed_operating_point_not_scoring_closure | none | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:74 | same_family | retain_at_fixed_operating_point_not_scoring_closure | none | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:84 | same_family | retain_at_fixed_operating_point_not_scoring_closure | none | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:89 | same_family | retain_at_fixed_operating_point_not_scoring_closure | none | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:135 | same_family | abstain_or_route_novel_oos | same_family_numeric_bandpass_counteraxis |  |
| m_csa:190 | same_family | retain_at_fixed_operating_point_not_scoring_closure | none | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:223 | same_family | abstain_or_route_novel_oos | same_family_numeric_bandpass_counteraxis |  |
| m_csa:229 | same_family | retain_at_fixed_operating_point_not_scoring_closure | none | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:256 | same_family | retain_at_fixed_operating_point_not_scoring_closure | none | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:289 | high_cofactor,same_family | abstain_or_route_novel_oos | cofactor_context_counteraxis |  |
| m_csa:308 | same_family | retain_at_fixed_operating_point_not_scoring_closure | none | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:451 | same_family | abstain_or_route_novel_oos | same_family_numeric_bandpass_counteraxis |  |
| m_csa:463 | same_family | abstain_or_route_novel_oos | same_family_numeric_bandpass_counteraxis |  |
| m_csa:464 | same_family | abstain_or_route_novel_oos | same_family_numeric_bandpass_counteraxis |  |
| m_csa:468 | same_family | retain_at_fixed_operating_point_not_scoring_closure | none | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:488 | same_family | abstain_or_route_novel_oos | same_family_numeric_bandpass_counteraxis |  |
| m_csa:502 | same_family | abstain_or_route_novel_oos | same_family_numeric_bandpass_counteraxis |  |
| m_csa:503 | same_family | abstain_or_route_novel_oos | same_family_numeric_bandpass_counteraxis |  |
| m_csa:638 | same_family | retain_at_fixed_operating_point_not_scoring_closure | none | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| m_csa:646 | same_family | abstain_or_route_novel_oos | same_family_numeric_bandpass_counteraxis |  |

## Retained Residual Evidence Queue

| rank | row | axes | closest channel | margin | pocket descriptor | evidence need |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | m_csa:229 | same_family | cofactor_max_score | 0.004742 | pocket_descriptor_missing | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| 2 | m_csa:89 | same_family | combined_mean_geometry_fold | 0.00845 | pocket_descriptor_missing | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| 3 | m_csa:74 | same_family | cofactor_max_score | 0.011125 | pocket_descriptor_missing | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| 4 | m_csa:256 | same_family | cofactor_max_score | 0.015781 | pocket_descriptor_missing | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| 5 | m_csa:638 | same_family | cofactor_max_score | 0.019535 | pocket_descriptor_missing | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| 6 | m_csa:190 | same_family | cofactor_max_score | 0.025247 | pocket_descriptor_missing | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| 7 | m_csa:84 | same_family | cofactor_max_score | 0.026454 | pocket_descriptor_missing | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| 8 | m_csa:25 | same_family | combined_min_geometry_fold | 0.0398 | pocket_descriptor_present | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| 9 | m_csa:52 | same_family | cofactor_max_score | 0.062269 | pocket_descriptor_present | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| 10 | m_csa:468 | same_family | combined_mean_geometry_cofactor_fold | 0.131121 | pocket_descriptor_missing | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |
| 11 | m_csa:308 | same_family | combined_mean_geometry_cofactor_fold | 0.19385 | pocket_descriptor_missing | new_source_free_same_family_chemistry_or_pocket_counteraxis_required |

## Incomplete Inputs

- P07658 forced abstention rows: 1

## Decision

- Unsafe forced mechanism transfer allowed: False
- Score rows with missing coordinate/provenance now: False
- Missing evidence for scoring closure or zero residual risk: ['one credentialed provider route or local predictor that accepts the exact 715-aa P07658 FASTA', 'returned full-length coordinate file at the preferred staging path', 'filled provenance with provider/model/version/path/checksum, input sequence hash, and documented U140 handling', 'P07658 acceptance preflight with all required checks passing', 'source-free chemistry or pocket counteraxis evidence for the 11 retained residual same-family rows if zero residual retained-transfer risk is required; 9 still lack same-family pocket descriptors and 2 have descriptors but no accepted counteraxis']
- Next gate: Use the fail-closed P07658 action now; for scoring closure, provision one exact full-length P07658 predictor route with coordinate/provenance and rerun acceptance preflight.

## Guardrails

- Measured readout only. No coordinates, row scores, labels, registries, ontologies, imports, thresholds, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Lever 3 has a row-level fail-closed action surface, but fixed-threshold scoring closure still waits on P07658.
- Accepted counteraxes abstain 10/21 residual hard-confounded rows, retain 31/34 calibration in-scope rows, abstain 105/204 train/cal OOS rows, and force P07658 to abstain while coordinate/provenance is missing.
- Provision one exact full-length P07658 predictor route with provenance before any fixed-threshold scoring rerun.
