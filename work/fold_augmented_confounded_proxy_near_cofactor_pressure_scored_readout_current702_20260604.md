# Fold-Augmented Confounded Proxy Near-Cofactor Pressure Readout - current702

Run: 2026-06-04T15:17:43Z

Deployment-valid train/cal-only pressure readout over the 16 strict high-cofactor near-miss rows. It uses predicted AFDB/AFDB-Viro3D coordinates, source-free predicted geometry, existing source-free cofactor scores, and Foldseek/TM nearest-train-atlas scores at the unchanged 0.44155 operating point. It does not relax or satisfy the high-cofactor acquisition contract.

## Status

- fold_augmented_confounded_proxy_near_cofactor_pressure_readout_ready_complete_diagnostic_not_contract
- Fixed threshold: combined_mean_geometry_fold >= 0.44155
- Rows with full scores: 16/16
- Abstained at fixed threshold: 8/16
- Retained at fixed threshold: 8/16
- Coordinates staged this run: 9
- Strict high-cofactor contract rows added: 0

## Row Readout

| rank | row | accession | cofactor | score | combined | margin | abstains | nearest fingerprint | top1 fingerprint | blocker |
| ---: | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| 1 | m_csa:288 | P07662 | heme:0.407563 | 0.4272 | 0.41995 | -0.0216 | True | metal_dependent_hydrolase | ser_his_acid_hydrolase | not high-cofactor contract member |
| 2 | m_csa:89 | Q55012 | heme:0.398339 | 0.409 | 0.45 | 0.00845 | False | metal_dependent_hydrolase | metal_dependent_hydrolase | not high-cofactor contract member |
| 3 | m_csa:214 | P0AG16 | plp:0.353171 | 0.3559 | 0.4598 | 0.01825 | False | flavin_dehydrogenase_reductase | heme_peroxidase_oxidase | not high-cofactor contract member |
| 4 | m_csa:75 | P00963 | heme:0.34378 | 0.5757 | 0.4884 | 0.04685 | False | ser_his_acid_hydrolase | metal_dependent_hydrolase | not high-cofactor contract member |
| 5 | m_csa:60 | P0A759 | plp:0.337092 | 0.3704 | 0.4709 | 0.02935 | False | plp_dependent_enzyme | metal_dependent_hydrolase | not high-cofactor contract member |
| 6 | m_csa:583 | P09186 | heme:0.296056 | 0.3806 | 0.63125 | 0.1897 | False | heme_peroxidase_oxidase | metal_dependent_hydrolase | not high-cofactor contract member |
| 7 | m_csa:64 | P14294 | plp:0.246623 | 0.4014 | 0.4492 | 0.00765 | False | ser_his_acid_hydrolase | metal_dependent_hydrolase | not high-cofactor contract member |
| 8 | m_csa:607 | P29241 | heme:0.236789 | 0.3463 | 0.4249 | -0.01665 | True | ser_his_acid_hydrolase | metal_dependent_hydrolase | not high-cofactor contract member |
| 9 | m_csa:610 | P15807 | plp:0.222226 | 0.3063 | 0.43915 | -0.0024 | True | plp_dependent_enzyme | metal_dependent_hydrolase | not high-cofactor contract member |
| 10 | m_csa:618 | Q9P4R4 | flavin:0.215006 | 0.3001 | 0.43035 | -0.0112 | True | ser_his_acid_hydrolase | metal_dependent_hydrolase | not high-cofactor contract member |
| 11 | m_csa:555 | P81382 | flavin:0.213904 | 0.3228 | 0.51255 | 0.071 | False | flavin_dehydrogenase_reductase | heme_peroxidase_oxidase | not high-cofactor contract member |
| 12 | m_csa:404 | P04802 | heme:0.193581 | 0.418 | 0.42235 | -0.0192 | True | plp_dependent_enzyme | metal_dependent_hydrolase | not high-cofactor contract member |
| 13 | m_csa:26 | P14262 | plp:0.177608 | 0.3759 | 0.5146 | 0.07305 | False | metal_dependent_hydrolase | metal_dependent_hydrolase | not high-cofactor contract member |
| 14 | m_csa:515 | Q00267 | plp:0.150245 | 0.3471 | 0.39885 | -0.0427 | True | metal_dependent_hydrolase | metal_dependent_hydrolase | not high-cofactor contract member |
| 15 | m_csa:232 | P68698 | plp:0.147019 | 0.3534 | 0.3886 | -0.05295 | True | heme_peroxidase_oxidase | metal_dependent_hydrolase | not high-cofactor contract member |
| 16 | m_csa:351 | Q96C23 | plp:0.144021 | 0.3694 | 0.39725 | -0.0443 | True | metal_dependent_hydrolase | metal_dependent_hydrolase | not high-cofactor contract member |

## Decision

- Measured readout available: True
- Current near-cofactor evidence sufficient for high-cofactor contract: False
- Deployable closure after this readout: False
- Apply or change threshold now: False
- Next gate: Do not count this as high-cofactor contract closure. The complete near-cofactor pressure readout shows weak source-free cofactor scores alone are insufficient: fill 16 true high-cofactor source-free/locus rows, keep P07658 coordinate/provenance as the single surface-completeness blocker, and keep the 170-row same-family structural acquisition separate.

## Interpretation

- Near-cofactor pressure rows scored at the unchanged threshold abstain 8/16 with 0 rows missing full scores; this is a complete diagnostic readout but does not clear the strict high-cofactor axis.
- All 16 rows were selected as near misses below the frozen source-free high-cofactor/locus membership axis; counting them would relax the contract after seeing the gap.
- Acquire 16 non-heldout train/cal OOS rows with true source-free high organic-cofactor or inorganic-locus signatures and deployment-valid predicted structures, then score them at threshold 0.44155.
