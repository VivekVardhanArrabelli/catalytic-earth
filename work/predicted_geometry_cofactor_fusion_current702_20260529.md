# Predicted Geometry Cofactor Fusion

Run: 2026-05-29T23:02:14Z

## Metrics

### raw_fused_geometry_metrics

- Naive cofactor injection recovers the named failures and cuts abstentions, but over-opens OOS/secondary rows.
- Primary: 31/45 correct, 1 abstained, 13 wrong nonabstained.
- OOS/sec FP rate: 0.567901.

| Entry | Called | Abstained | Exact | Score |
| --- | --- | --- | --- | ---: |
| m_csa:44 | metal_dependent_hydrolase | False | True | 0.5973 |
| m_csa:239 | heme_peroxidase_oxidase | False | True | 0.7209 |
| m_csa:250 | heme_peroxidase_oxidase | False | True | 0.7104 |
| m_csa:497 | flavin_dehydrogenase_reductase | False | True | 0.6729 |
| m_csa:990 | flavin_dehydrogenase_reductase | False | True | 0.7329 |

### conservative_switch_metrics

- Route-preserving switch policy avoids broad abstention release; it is the safer candidate for follow-up thresholding.
- Primary: 21/45 correct, 17 abstained, 7 wrong nonabstained.
- OOS/sec FP rate: 0.123457.

| Entry | Called | Abstained | Exact | Score |
| --- | --- | --- | --- | ---: |
| m_csa:44 | metal_dependent_hydrolase | False | True | 0.5973 |
| m_csa:239 | heme_peroxidase_oxidase | False | True | 0.7209 |
| m_csa:250 | heme_peroxidase_oxidase | False | True | 0.7104 |
| m_csa:497 | flavin_dehydrogenase_reductase | False | True | 0.6729 |
| m_csa:990 | flavin_dehydrogenase_reductase | False | True | 0.7329 |

### target_failure_diagnostic_metrics

- Diagnostic readout for the five named known failures only; not a deployable routing policy, but it verifies the missing cofactor channel can flip the exact intended calls without changing OOS route volume.
- Primary: 28/45 correct, 17 abstained, 0 wrong nonabstained.
- OOS/sec FP rate: 0.123457.

| Entry | Called | Abstained | Exact | Score |
| --- | --- | --- | --- | ---: |
| m_csa:44 | metal_dependent_hydrolase | False | True | 0.5973 |
| m_csa:239 | heme_peroxidase_oxidase | False | True | 0.7209 |
| m_csa:250 | heme_peroxidase_oxidase | False | True | 0.7104 |
| m_csa:497 | flavin_dehydrogenase_reductase | False | True | 0.6729 |
| m_csa:990 | flavin_dehydrogenase_reductase | False | True | 0.7329 |

### sequence_supported_suppression_metrics

- Diagnostic target switches plus a sequence-support suppression gate. This recovers the five named failures and reduces OOS/sec FP substantially, at the cost of more abstentions.
- Primary: 16/45 correct, 29 abstained, 0 wrong nonabstained.
- OOS/sec FP rate: 0.024691.

| Entry | Called | Abstained | Exact | Score |
| --- | --- | --- | --- | ---: |
| m_csa:44 | metal_dependent_hydrolase | False | True | 0.5973 |
| m_csa:239 | heme_peroxidase_oxidase | False | True | 0.7209 |
| m_csa:250 | heme_peroxidase_oxidase | False | True | 0.7104 |
| m_csa:497 | flavin_dehydrogenase_reductase | False | True | 0.6729 |
| m_csa:990 | flavin_dehydrogenase_reductase | False | True | 0.7329 |
