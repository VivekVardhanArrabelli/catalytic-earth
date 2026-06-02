# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Calibration Error Analysis - current702

Run: 2026-06-02T11:38:39Z

Read-only calibration error analysis for the best-token OOS-augmented row-specific operating point. It names retained and abstained calibration OOS rows under the best-token residual contract without changing thresholds or reading heldout.

## Status

- p0_oos_augmented_best_token_calibration_error_analysis_ready
- Calibration rows: 32
- Calibration OOS rows: 28
- Outcome counts: {'oos_abstained': 20, 'oos_non_abstained': 8, 'primary_retained': 4}
- Residual threshold: 3.21469422
- Retained OOS nearest-primary counts: {'flavin_dehydrogenase_reductase': 1, 'heme_peroxidase_oxidase': 4, 'metal_dependent_hydrolase': 2, 'ser_his_acid_hydrolase': 1}
- Retained OOS priority counts: {'borderline_contract_miss': 1, 'near_contract_miss': 1, 'strong_primary_alias': 6}

## Retained OOS Rows

| row | residual | nearest primary | events | bond | proton | electron |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| m_csa:246 | 1.71494092 | flavin_dehydrogenase_reductase | 4 | 1 | 2 | 1 |
| m_csa:49 | 1.93341908 | heme_peroxidase_oxidase | 3 | 0 | 1 | 2 |
| m_csa:78 | 2.02787819 | metal_dependent_hydrolase | 3 | 2 | 1 | 0 |
| m_csa:101 | 2.04759883 | ser_his_acid_hydrolase | 2 | 2 | 0 | 0 |
| m_csa:59 | 2.41441231 | heme_peroxidase_oxidase | 5 | 0 | 3 | 2 |
| m_csa:312 | 2.41653869 | heme_peroxidase_oxidase | 2 | 0 | 1 | 1 |
| m_csa:256 | 2.79157886 | heme_peroxidase_oxidase | 3 | 0 | 0 | 3 |
| m_csa:273 | 3.16757587 | metal_dependent_hydrolase | 4 | 1 | 3 | 0 |

## Retained OOS Failure Set

| row | priority | residual margin | nearest primary | event profile |
| --- | --- | ---: | --- | --- |
| m_csa:273 | borderline_contract_miss | 0.04711835 | metal_dependent_hydrolase | events=4;bond=1;proton=3;electron=0 |
| m_csa:256 | near_contract_miss | 0.42311536 | heme_peroxidase_oxidase | events=3;bond=0;proton=0;electron=3 |
| m_csa:312 | strong_primary_alias | 0.79815553 | heme_peroxidase_oxidase | events=2;bond=0;proton=1;electron=1 |
| m_csa:59 | strong_primary_alias | 0.80028191 | heme_peroxidase_oxidase | events=5;bond=0;proton=3;electron=2 |
| m_csa:101 | strong_primary_alias | 1.16709539 | ser_his_acid_hydrolase | events=2;bond=2;proton=0;electron=0 |
| m_csa:78 | strong_primary_alias | 1.18681603 | metal_dependent_hydrolase | events=3;bond=2;proton=1;electron=0 |
| m_csa:49 | strong_primary_alias | 1.28127514 | heme_peroxidase_oxidase | events=3;bond=0;proton=1;electron=2 |
| m_csa:246 | strong_primary_alias | 1.4997533 | flavin_dehydrogenase_reductase | events=4;bond=1;proton=2;electron=1 |

## Abstained OOS Rows

| row | residual | nearest primary | events | bond | proton | electron |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| m_csa:292 | 5.88152283 | metal_dependent_hydrolase | 5 | 3 | 1 | 1 |
| m_csa:17 | 5.55842179 | metal_dependent_hydrolase | 5 | 4 | 1 | 0 |
| m_csa:222 | 5.21496062 | ser_his_acid_hydrolase | 5 | 2 | 3 | 0 |
| m_csa:194 | 4.99199721 | metal_dependent_hydrolase | 5 | 2 | 2 | 1 |
| m_csa:85 | 4.96150995 | ser_his_acid_hydrolase | 2 | 0 | 2 | 0 |
| m_csa:287 | 4.46802862 | metal_dependent_hydrolase | 3 | 3 | 0 | 0 |
| m_csa:253 | 4.44010536 | ser_his_acid_hydrolase | 2 | 1 | 1 | 0 |
| m_csa:263 | 4.13349818 | metal_dependent_hydrolase | 4 | 2 | 1 | 1 |
| m_csa:224 | 4.13211893 | heme_peroxidase_oxidase | 2 | 0 | 2 | 0 |
| m_csa:241 | 4.02683164 | flavin_dehydrogenase_reductase | 5 | 1 | 4 | 0 |
| m_csa:154 | 4.01457041 | metal_dependent_hydrolase | 4 | 2 | 2 | 0 |
| m_csa:2 | 3.82174651 | ser_his_acid_hydrolase | 3 | 2 | 1 | 0 |
| m_csa:23 | 3.74834254 | ser_his_acid_hydrolase | 2 | 1 | 1 | 0 |
| m_csa:25 | 3.67227966 | ser_his_acid_hydrolase | 3 | 3 | 0 | 0 |
| m_csa:221 | 3.66796305 | metal_dependent_hydrolase | 4 | 2 | 2 | 0 |
| m_csa:40 | 3.63849194 | ser_his_acid_hydrolase | 1 | 1 | 0 | 0 |
| m_csa:149 | 3.55609944 | ser_his_acid_hydrolase | 3 | 1 | 2 | 0 |
| m_csa:317 | 3.3556626 | metal_dependent_hydrolase | 5 | 2 | 3 | 0 |
| m_csa:318 | 3.3510611 | ser_his_acid_hydrolase | 2 | 1 | 1 | 0 |
| m_csa:70 | 3.26807732 | ser_his_acid_hydrolase | 3 | 2 | 1 | 0 |

## Interpretation

- The best-token residual threshold abstains on 20/28 calibration OOS rows while retaining all calibration primaries.
- Use the remaining retained OOS rows as the next token-level or heldout-safe feature target; do not tune on heldout.
