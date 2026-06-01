# Predicted-Structure Fold-Augmented Novelty Operating Grid - current702

Run: 2026-06-01T15:13:41Z

Review-only operating-grid readout over the frozen geometry-plus-predicted-fold novelty variants. It recomputes post-hoc diagnostic retention/OOS-abstention points from existing row scores only and does not select or write a deployment threshold.

## Counts

- Row scores: 126
- In-scope: 47
- OOS: 79
- Cofactor-confounded OOS: 6
- Signals: 11
- Grid rows: 44

## Best Signal From Variant Artifact

- Signal: mean_top1_raw_and_tm
- >=90% retention diagnostic: {'threshold': 0.48945, 'inscope_retain_recall': 0.9149, 'oos_abstain_recall': 0.7215, 'confounded_abstain_recall': 0.8333}
- >=85% retention diagnostic: {'threshold': 0.503, 'inscope_retain_recall': 0.8511, 'oos_abstain_recall': 0.7722, 'confounded_abstain_recall': 0.8333}

## Best By Retention Target

| target | signal | in-scope retain | OOS abstain | confounded abstain | threshold |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0.80 | `mean_top1_raw_and_tm` | 0.8085 | 0.8608 | 0.8333 | 0.5213 |
| 0.85 | `harmonic_top1_raw_and_tm` | 0.8511 | 0.8354 | 0.8333 | 0.475146 |
| 0.90 | `mean_top1_atlas_percentile_and_tm` | 0.9149 | 0.7722 | 0.8333 | 0.416045 |
| 0.95 | `mean_top1_raw_and_tm` | 0.9574 | 0.6456 | 0.8333 | 0.45985 |

## Confounded Rows

| row | best-signal score | nearest-atlas TM | abstained at 90% | abstained at 85% |
| --- | ---: | ---: | --- | --- |
| m_csa:30 | 0.3802 | 0.4988 | True | True |
| m_csa:31 | 0.36375 | 0.3809 | True | True |
| m_csa:80 | 0.4299 | 0.5109 | True | True |
| m_csa:191 | 0.37905 | 0.3863 | True | True |
| m_csa:267 | 0.5679 | 0.7389 | False | False |
| m_csa:448 | 0.4341 | 0.5106 | True | True |

## Interpretation

- The geometry-plus-predicted-fold signal materially improves the high-retention OOS-abstention diagnostic over geometry-only predicted-atlas variants, but remains review-only.
- Use this as bounded evidence for train/cal OOS-surface and source-check prioritization; do not promote a deployment threshold from this heldout readout.
