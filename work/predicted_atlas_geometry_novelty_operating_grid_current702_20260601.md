# Predicted-Atlas Geometry Novelty Operating Grid - current702

Run: 2026-06-01T12:49:30Z

Review-only operating-grid readout over the existing predicted-atlas geometry novelty variants. It computes post-hoc diagnostic retention/OOS-abstention points for each frozen geometry signal and does not select or write a deployment threshold.

## Counts

- Row scores: 126
- In-scope: 47
- OOS: 79
- Cofactor-confounded OOS: 6
- Signals: 10
- Grid rows: 40

## Best Signal From Variant Artifact

- Signal: negative_nearest_class_centroid_robust_distance
- >=90% retention diagnostic: {'threshold': -2.079745, 'inscope_retain_recall': 0.9149, 'oos_abstain_recall': 0.2278, 'confounded_abstain_recall': 0.3333}
- >=85% retention diagnostic: {'threshold': -1.473053, 'inscope_retain_recall': 0.8723, 'oos_abstain_recall': 0.5949, 'confounded_abstain_recall': 0.6667}

## Best By Retention Target

| target | signal | in-scope retain | OOS abstain | confounded abstain | threshold |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0.80 | `negative_nearest_class_centroid_robust_distance` | 0.8085 | 0.6203 | 0.6667 | -1.434876 |
| 0.85 | `negative_nearest_class_centroid_robust_distance` | 0.8723 | 0.5949 | 0.6667 | -1.473053 |
| 0.90 | `negative_nearest_class_centroid_robust_distance` | 0.9149 | 0.2278 | 0.3333 | -2.079745 |
| 0.95 | `negative_nearest_class_centroid_robust_distance` | 0.9574 | 0.1519 | 0.1667 | -2.517866 |

## Confounded Rows

| row | score | abstained at 90% | abstained at 85% |
| --- | ---: | --- | --- |
| m_csa:30 | -2.309839 | True | True |
| m_csa:31 | -1.399238 | False | False |
| m_csa:80 | -4.05767 | True | True |
| m_csa:191 | -1.800092 | False | True |
| m_csa:267 | -1.475892 | False | True |
| m_csa:448 | -1.350762 | False | False |

## Interpretation

- The best predicted-atlas geometry signal remains useful as a rank diagnostic, but its 90% retention operating point is still too weak for a standalone deployment gate.
- Treat this as input evidence for fold-augmented or mechanism-feature signals; do not promote a geometry-only novelty threshold.
