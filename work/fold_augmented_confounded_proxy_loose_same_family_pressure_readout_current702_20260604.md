# Fold-Augmented Confounded Proxy Loose Same-Family Pressure Readout - current702

Run: 2026-06-04T16:40:20Z

Train/cal-only diagnostic fixed-threshold readout for the loose same-family current-surface rows named by the acquisition queue. It de-duplicates against the refreshed strict same-family rows and does not relax membership, close the contract, tune thresholds, read heldout rows, or change labels.

## Status

- fold_augmented_confounded_proxy_loose_same_family_pressure_readout_ready_diagnostic_not_contract
- Fixed threshold: 0.44155
- Strict current same-family: 11/59 abstained
- Loose diagnostic same-family: 15/21 abstained
- Strict plus loose diagnostic: 26/80 abstained
- Frozen dispatch same-family slots required: 170

## Decision

- Loose same-family evidence sufficient for contract closure: False
- Fixed-threshold audit ready to rerun now: False
- Next gate: Do not relax same-family structural membership from this diagnostic. Even strict plus loose current-surface rows abstain only 26/80 at fixed threshold 0.44155, so the same-family structural axis still needs new non-heldout train/cal OOS acquisition evidence.

## Row Readout

| row | membership | combined | margin | abstains | nearest train family | top1 family |
| --- | --- | ---: | ---: | --- | --- | --- |
| m_csa:4 | loose_same_family_current_surface_diagnostic_not_contract | 0.3729 | -0.06865 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:22 | strict_same_family_structural_proxy_current_readout | 0.42405 | -0.0175 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:25 | strict_same_family_structural_proxy_current_readout | 0.6241 | 0.18255 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:36 | strict_same_family_structural_proxy_current_readout | 0.51785 | 0.0763 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:51 | strict_same_family_structural_proxy_current_readout | 0.4314 | -0.01015 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:52 | strict_same_family_structural_proxy_current_readout | 0.6154 | 0.17385 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:59 | strict_same_family_structural_proxy_current_readout | 0.60775 | 0.1662 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:74 | strict_same_family_structural_proxy_current_readout | 0.61305 | 0.1715 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:78 | strict_same_family_structural_proxy_current_readout | 0.4054 | -0.03615 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:84 | strict_same_family_structural_proxy_current_readout | 0.56755 | 0.126 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:88 | loose_same_family_current_surface_diagnostic_not_contract | 0.41345 | -0.0281 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:89 | strict_same_family_structural_proxy_current_readout | 0.45 | 0.00845 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:91 | strict_same_family_structural_proxy_current_readout | 0.45895 | 0.0174 | False | ser_his_acid_hydrolase | ser_his_acid_hydrolase |
| m_csa:104 | strict_same_family_structural_proxy_current_readout | 0.6498 | 0.20825 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:105 | strict_same_family_structural_proxy_current_readout | 0.40305 | -0.0385 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:119 | strict_same_family_structural_proxy_current_readout | 0.4463 | 0.00475 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:126 | loose_same_family_current_surface_diagnostic_not_contract | 0.5127 | 0.07115 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:130 | loose_same_family_current_surface_diagnostic_not_contract | 0.41015 | -0.0314 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:134 | loose_same_family_current_surface_diagnostic_not_contract | 0.40925 | -0.0323 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:135 | strict_same_family_structural_proxy_current_readout | 0.5317 | 0.09015 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:145 | loose_same_family_current_surface_diagnostic_not_contract | 0.40385 | -0.0377 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:146 | strict_same_family_structural_proxy_current_readout | 0.43465 | -0.0069 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:177 | loose_same_family_current_surface_diagnostic_not_contract | 0.3993 | -0.04225 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:179 | strict_same_family_structural_proxy_current_readout | 0.42145 | -0.0201 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:187 | strict_same_family_structural_proxy_current_readout | 0.65175 | 0.2102 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:189 | strict_same_family_structural_proxy_current_readout | 0.4103 | -0.03125 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:190 | strict_same_family_structural_proxy_current_readout | 0.6365 | 0.19495 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:206 | strict_same_family_structural_proxy_current_readout | 0.63845 | 0.1969 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:209 | loose_same_family_current_surface_diagnostic_not_contract | 0.4348 | -0.00675 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:223 | strict_same_family_structural_proxy_current_readout | 0.5078 | 0.06625 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:224 | strict_same_family_structural_proxy_current_readout | 0.4011 | -0.04045 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:229 | strict_same_family_structural_proxy_current_readout | 0.5438 | 0.10225 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:234 | strict_same_family_structural_proxy_current_readout | 0.45495 | 0.0134 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:240 | strict_same_family_structural_proxy_current_readout | 0.4716 | 0.03005 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:244 | strict_same_family_structural_proxy_current_readout | 0.4724 | 0.03085 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:253 | strict_same_family_structural_proxy_current_readout | 0.5158 | 0.07425 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:256 | strict_same_family_structural_proxy_current_readout | 0.61925 | 0.1777 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:269 | strict_same_family_structural_proxy_current_readout | 0.65065 | 0.2091 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:280 | strict_same_family_structural_proxy_current_readout | 0.44705 | 0.0055 | False | ser_his_acid_hydrolase | ser_his_acid_hydrolase |
| m_csa:282 | loose_same_family_current_surface_diagnostic_not_contract | 0.38295 | -0.0586 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:284 | loose_same_family_current_surface_diagnostic_not_contract | 0.45095 | 0.0094 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:289 | strict_same_family_structural_proxy_current_readout | 0.6398 | 0.19825 | False | flavin_dehydrogenase_reductase | flavin_dehydrogenase_reductase |
| m_csa:299 | strict_same_family_structural_proxy_current_readout | 0.4712 | 0.02965 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:308 | strict_same_family_structural_proxy_current_readout | 0.68115 | 0.2396 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:322 | strict_same_family_structural_proxy_current_readout | 0.53375 | 0.0922 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:325 | loose_same_family_current_surface_diagnostic_not_contract | 0.4878 | 0.04625 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:342 | strict_same_family_structural_proxy_current_readout | 0.43935 | -0.0022 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:348 | strict_same_family_structural_proxy_current_readout | 0.649 | 0.20745 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:350 | loose_same_family_current_surface_diagnostic_not_contract | 0.3817 | -0.05985 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:390 | loose_same_family_current_surface_diagnostic_not_contract | 0.48795 | 0.0464 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:405 | strict_same_family_structural_proxy_current_readout | 0.4837 | 0.04215 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:422 | strict_same_family_structural_proxy_current_readout | 0.47265 | 0.0311 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:439 | loose_same_family_current_surface_diagnostic_not_contract | 0.3933 | -0.04825 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:441 | strict_same_family_structural_proxy_current_readout | 0.41695 | -0.0246 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:450 | loose_same_family_current_surface_diagnostic_not_contract | 0.38735 | -0.0542 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:451 | strict_same_family_structural_proxy_current_readout | 0.588 | 0.14645 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:463 | strict_same_family_structural_proxy_current_readout | 0.54765 | 0.1061 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:464 | strict_same_family_structural_proxy_current_readout | 0.60295 | 0.1614 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:468 | strict_same_family_structural_proxy_current_readout | 0.64225 | 0.2007 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:483 | strict_same_family_structural_proxy_current_readout | 0.6341 | 0.19255 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:488 | strict_same_family_structural_proxy_current_readout | 0.64045 | 0.1989 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:498 | strict_same_family_structural_proxy_current_readout | 0.4466 | 0.00505 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:500 | strict_same_family_structural_proxy_current_readout | 0.61935 | 0.1778 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:501 | strict_same_family_structural_proxy_current_readout | 0.601 | 0.15945 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:502 | strict_same_family_structural_proxy_current_readout | 0.5957 | 0.15415 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:503 | strict_same_family_structural_proxy_current_readout | 0.55265 | 0.1111 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:508 | strict_same_family_structural_proxy_current_readout | 0.42915 | -0.0124 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:525 | loose_same_family_current_surface_diagnostic_not_contract | 0.37455 | -0.067 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:533 | strict_same_family_structural_proxy_current_readout | 0.5423 | 0.10075 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:537 | loose_same_family_current_surface_diagnostic_not_contract | 0.4835 | 0.04195 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:539 | loose_same_family_current_surface_diagnostic_not_contract | 0.37695 | -0.0646 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:540 | loose_same_family_current_surface_diagnostic_not_contract | 0.40915 | -0.0324 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:547 | loose_same_family_current_surface_diagnostic_not_contract | 0.46725 | 0.0257 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:565 | strict_same_family_structural_proxy_current_readout | 0.46835 | 0.0268 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:585 | strict_same_family_structural_proxy_current_readout | 0.4867 | 0.04515 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:621 | strict_same_family_structural_proxy_current_readout | 0.4602 | 0.01865 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:638 | strict_same_family_structural_proxy_current_readout | 0.5862 | 0.14465 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:645 | strict_same_family_structural_proxy_current_readout | 0.50615 | 0.0646 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:646 | strict_same_family_structural_proxy_current_readout | 0.54185 | 0.1003 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:648 | loose_same_family_current_surface_diagnostic_not_contract | 0.3987 | -0.04285 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |

## Interpretation

- The relaxed diagnostic pressure set abstains 26/80 at the unchanged fixed threshold, far below the 80% target.
- The loose rows were already marked diagnostic-only because their membership relaxes the strict fold plus geometry component gate; counting them would change the proxy definition after seeing the gap.
- Acquire new non-heldout train/cal same-family structural OOS rows with deployment-valid predicted structures and source-free membership evidence, then score them at threshold 0.44155 under the frozen contract.
