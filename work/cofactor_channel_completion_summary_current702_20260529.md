# Cofactor Channel Completion Summary

## Borrowed metal predictor

- M-Ionic ROC AUC 0.781067, AP 0.567376 on 135 heldout clean rows (29 metal positives).
- K-mer metal ROC AUC 0.481457, AP 0.234538.

## Trained sequence heads

| Backend | Class | ROC AUC | AP | TP | FP | FN | TN |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| esm2_t12_35m | flavin | 0.918622 | 0.732961 | 7 | 5 | 4 | 119 |
| esm2_t12_35m | heme | 0.764615 | 0.38405 | 1 | 5 | 4 | 125 |
| esm2_t12_35m | metal_ion | 0.673715 | 0.364756 | 13 | 27 | 16 | 79 |
| esm2_t12_35m | plp | 0.981912 | 0.883333 | 5 | 3 | 1 | 126 |
| esm2_t6_8m | flavin | 0.874633 | 0.635522 | 6 | 5 | 5 | 119 |
| esm2_t6_8m | heme | 0.866154 | 0.525794 | 3 | 5 | 2 | 125 |
| esm2_t6_8m | metal_ion | 0.607027 | 0.307283 | 12 | 35 | 17 | 71 |
| esm2_t6_8m | plp | 0.990956 | 0.876623 | 5 | 3 | 1 | 126 |

## Fusion readouts

### raw_fused_geometry_metrics

- Primary 31/45 correct, 1 abstained, 13 wrong nonabstained; OOS/sec FP 46 (0.567901).
| Entry | Called | Abstained | Exact | Score |
| --- | --- | --- | --- | ---: |
| m_csa:44 | metal_dependent_hydrolase | False | True | 0.5973 |
| m_csa:239 | heme_peroxidase_oxidase | False | True | 0.7209 |
| m_csa:250 | heme_peroxidase_oxidase | False | True | 0.7104 |
| m_csa:497 | flavin_dehydrogenase_reductase | False | True | 0.6729 |
| m_csa:990 | flavin_dehydrogenase_reductase | False | True | 0.7329 |

### target_failure_diagnostic_metrics

- Primary 28/45 correct, 17 abstained, 0 wrong nonabstained; OOS/sec FP 10 (0.123457).
| Entry | Called | Abstained | Exact | Score |
| --- | --- | --- | --- | ---: |
| m_csa:44 | metal_dependent_hydrolase | False | True | 0.5973 |
| m_csa:239 | heme_peroxidase_oxidase | False | True | 0.7209 |
| m_csa:250 | heme_peroxidase_oxidase | False | True | 0.7104 |
| m_csa:497 | flavin_dehydrogenase_reductase | False | True | 0.6729 |
| m_csa:990 | flavin_dehydrogenase_reductase | False | True | 0.7329 |

### sequence_supported_suppression_metrics

- Primary 16/45 correct, 29 abstained, 0 wrong nonabstained; OOS/sec FP 2 (0.024691).
| Entry | Called | Abstained | Exact | Score |
| --- | --- | --- | --- | ---: |
| m_csa:44 | metal_dependent_hydrolase | False | True | 0.5973 |
| m_csa:239 | heme_peroxidase_oxidase | False | True | 0.7209 |
| m_csa:250 | heme_peroxidase_oxidase | False | True | 0.7104 |
| m_csa:497 | flavin_dehydrogenase_reductase | False | True | 0.6729 |
| m_csa:990 | flavin_dehydrogenase_reductase | False | True | 0.7329 |

## Bottom line

- The cofactor signal is recoverable and flips all five named failures.
- The fully deployable route-policy bar is not closed yet: raw fusion cuts abstentions but leaks FP; suppression controls FP but increases abstention.
