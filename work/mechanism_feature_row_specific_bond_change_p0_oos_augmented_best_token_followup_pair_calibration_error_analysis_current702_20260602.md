# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Calibration Error Analysis - current702

Run: 2026-06-02T12:28:24Z

Read-only calibration error analysis for the best-token follow-up pair row-specific operating point. It names retained and abstained calibration OOS rows under the pair residual contract without changing thresholds or reading heldout.

## Status

- p0_oos_augmented_best_token_followup_pair_calibration_error_analysis_ready
- Calibration rows: 32
- Calibration OOS rows: 28
- Outcome counts: {'oos_abstained': 24, 'oos_non_abstained': 4, 'primary_retained': 4}
- Residual threshold: 3.21469422
- Retained OOS nearest-primary counts: {'flavin_dehydrogenase_reductase': 1, 'heme_peroxidase_oxidase': 2, 'metal_dependent_hydrolase': 1}
- Retained OOS priority counts: {'near_contract_miss': 1, 'strong_primary_alias': 3}

## Retained OOS Rows

| row | residual | nearest primary | events | bond | proton | electron |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| m_csa:246 | 1.71494092 | flavin_dehydrogenase_reductase | 4 | 1 | 2 | 1 |
| m_csa:49 | 1.93341908 | heme_peroxidase_oxidase | 3 | 0 | 1 | 2 |
| m_csa:78 | 2.33596541 | metal_dependent_hydrolase | 3 | 2 | 1 | 0 |
| m_csa:256 | 2.79157886 | heme_peroxidase_oxidase | 3 | 0 | 0 | 3 |

## Retained OOS Failure Set

| row | priority | residual margin | nearest primary | event profile |
| --- | --- | ---: | --- | --- |
| m_csa:256 | near_contract_miss | 0.42311536 | heme_peroxidase_oxidase | events=3;bond=0;proton=0;electron=3 |
| m_csa:78 | strong_primary_alias | 0.87872881 | metal_dependent_hydrolase | events=3;bond=2;proton=1;electron=0 |
| m_csa:49 | strong_primary_alias | 1.28127514 | heme_peroxidase_oxidase | events=3;bond=0;proton=1;electron=2 |
| m_csa:246 | strong_primary_alias | 1.4997533 | flavin_dehydrogenase_reductase | events=4;bond=1;proton=2;electron=1 |

## Abstained OOS Rows

| row | residual | nearest primary | events | bond | proton | electron |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| m_csa:17 | 6.02277599 | metal_dependent_hydrolase | 5 | 4 | 1 | 0 |
| m_csa:292 | 5.99472729 | metal_dependent_hydrolase | 5 | 3 | 1 | 1 |
| m_csa:222 | 5.21496062 | ser_his_acid_hydrolase | 5 | 2 | 3 | 0 |
| m_csa:194 | 5.12488835 | metal_dependent_hydrolase | 5 | 2 | 2 | 1 |
| m_csa:85 | 4.96150995 | ser_his_acid_hydrolase | 2 | 0 | 2 | 0 |
| m_csa:287 | 4.61602905 | metal_dependent_hydrolase | 3 | 3 | 0 | 0 |
| m_csa:253 | 4.44010536 | ser_his_acid_hydrolase | 2 | 1 | 1 | 0 |
| m_csa:263 | 4.28326141 | flavin_dehydrogenase_reductase | 4 | 2 | 1 | 1 |
| m_csa:312 | 4.23552349 | heme_peroxidase_oxidase | 2 | 0 | 1 | 1 |
| m_csa:59 | 4.23431067 | heme_peroxidase_oxidase | 5 | 0 | 3 | 2 |
| m_csa:154 | 4.17866247 | metal_dependent_hydrolase | 4 | 2 | 2 | 0 |
| m_csa:224 | 4.13211893 | heme_peroxidase_oxidase | 2 | 0 | 2 | 0 |
| m_csa:101 | 4.03641685 | ser_his_acid_hydrolase | 2 | 2 | 0 | 0 |
| m_csa:241 | 4.02683164 | flavin_dehydrogenase_reductase | 5 | 1 | 4 | 0 |
| m_csa:273 | 3.92572474 | metal_dependent_hydrolase | 4 | 1 | 3 | 0 |
| m_csa:221 | 3.84686852 | metal_dependent_hydrolase | 4 | 2 | 2 | 0 |
| m_csa:2 | 3.82174651 | ser_his_acid_hydrolase | 3 | 2 | 1 | 0 |
| m_csa:23 | 3.74834254 | ser_his_acid_hydrolase | 2 | 1 | 1 | 0 |
| m_csa:25 | 3.67227966 | ser_his_acid_hydrolase | 3 | 3 | 0 | 0 |
| m_csa:40 | 3.63849194 | ser_his_acid_hydrolase | 1 | 1 | 0 | 0 |
| m_csa:149 | 3.55609944 | ser_his_acid_hydrolase | 3 | 1 | 2 | 0 |
| m_csa:317 | 3.55034026 | metal_dependent_hydrolase | 5 | 2 | 3 | 0 |
| m_csa:318 | 3.3510611 | ser_his_acid_hydrolase | 2 | 1 | 1 | 0 |
| m_csa:70 | 3.26807732 | ser_his_acid_hydrolase | 3 | 2 | 1 | 0 |

## Interpretation

- The follow-up pair residual threshold abstains on 24/28 calibration OOS rows while retaining all calibration primaries.
- Build a source-free heldout application surface for the deployed feature pair before any heldout read.
