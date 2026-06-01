# Predicted-Atlas Geometry Novelty Variants - current702

Run: 2026-06-01T02:44:25Z

Bounded predicted-geometry atlas novelty rerun using the newly available in-distribution predicted atlas rows. All atlas statistics are computed from in-distribution rows only; heldout rows are final evaluation diagnostics.

## Counts

- Atlas rows: 168
- Heldout rows: 126
- In-scope: 47
- OOS: 79
- Cofactor-confounded OOS: 6

## Best Signal

- negative_nearest_class_centroid_robust_distance: AUC all OOS 0.776461; confounded AUC 0.847518
- Best >=90% retention diagnostic: {'threshold': -2.079745, 'inscope_retain_recall': 0.9149, 'oos_abstain_recall': 0.2278, 'confounded_abstain_recall': 0.3333}
- Best >=85% retention diagnostic: {'threshold': -1.473053, 'inscope_retain_recall': 0.8723, 'oos_abstain_recall': 0.5949, 'confounded_abstain_recall': 0.6667}

## Signals

| Signal | all OOS AUC | confounded AUC | agnostic AUC |
| --- | ---: | ---: | ---: |
| top1_score_raw | 0.756935 | 0.840426 | 0.750073 |
| top1_score_atlas_percentile | 0.756396 | 0.842199 | 0.749344 |
| role_match_fraction_raw | 0.654861 | 0.687943 | 0.652142 |
| role_match_fraction_atlas_percentile | 0.654861 | 0.687943 | 0.652142 |
| top1_score_x_role_raw | 0.744816 | 0.744681 | 0.744827 |
| top1_score_x_role_atlas_percentile | 0.748047 | 0.748227 | 0.748033 |
| cofactor_context_score_raw | 0.687988 | 0.737589 | 0.683911 |
| cofactor_context_score_atlas_percentile | 0.687988 | 0.737589 | 0.683911 |
| negative_robust_distance_to_atlas_median | 0.614328 | 0.663121 | 0.610318 |
| negative_nearest_class_centroid_robust_distance | 0.776461 | 0.847518 | 0.770621 |

## Interpretation

- Best predicted-atlas geometry variant is negative_nearest_class_centroid_robust_distance with AUC 0.776461.
- Post-hoc retention rows are diagnostics only; no deployment threshold is selected or written to production.
