# Fold-Augmented Confounded Proxy Operating-Point Audit - current702

Run: 2026-06-03T15:39:11Z

Leakage-safe Lever 3 audit for the fixed predicted-structure-vs-atlas fold operating point. It preserves the existing train/cal-selected combined_mean_geometry_fold threshold, stratifies only train/cal OOS negatives by the existing cofactor-signature proxy, and carries the already-frozen heldout confounded readout without selecting thresholds on heldout rows.

## Status

- fold_augmented_confounded_proxy_operating_point_ready_with_proxy_caveat
- Blockers: ['calibration_high_cofactor_proxy_target_not_met', 'calibration_same_family_structural_proxy_target_not_met']
- Fixed channel: combined_mean_geometry_fold
- Fixed threshold: 0.44155
- Deployment input contract passed: True
- Heldout confounded operating point met: True
- Calibration high-cofactor proxy target met: False
- Calibration same-family structural proxy target met: False

## Readout

| subset | rows | abstained | abstain recall |
| --- | ---: | ---: | ---: |
| all calibration OOS | 186 | 63 | 0.3387 |
| high-cofactor calibration OOS | 4 | 0 | 0.0 |
| low-cofactor calibration OOS | 182 | 63 | 0.3462 |
| same-family structural proxy OOS | 55 | 10 | 0.1818 |

## Heldout Carry-Through

- Confounded OOS abstained: 5/6
- In-scope retained: 45/47

## High-Cofactor Train/Cal Rows

| entry | cofactor | score | margin | abstains | nearest atlas fingerprint | top1 geometry fingerprint |
| --- | ---: | ---: | ---: | --- | --- | --- |
| m_csa:368 | 0.990498 | 0.4537 | 0.01215 | False | flavin_dehydrogenase_reductase | heme_peroxidase_oxidase |
| m_csa:361 | 0.97392 | 0.45695 | 0.0154 | False | flavin_dehydrogenase_reductase | metal_dependent_hydrolase |
| m_csa:298 | 0.515522 | 0.5344 | 0.09285 | False | flavin_dehydrogenase_reductase | flavin_monooxygenase |
| m_csa:289 | 0.980742 | 0.6398 | 0.19825 | False | flavin_dehydrogenase_reductase | flavin_dehydrogenase_reductase |

## Same-Family Structural Train/Cal Rows

| entry | cofactor | score | margin | abstains | nearest atlas fingerprint | top1 geometry fingerprint |
| --- | ---: | ---: | ---: | --- | --- | --- |
| m_csa:119 | 0.118424 | 0.4463 | 0.00475 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:498 | 0.094616 | 0.4466 | 0.00505 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:280 | 0.059279 | 0.44705 | 0.0055 | False | ser_his_acid_hydrolase | ser_his_acid_hydrolase |
| m_csa:234 | 0.017819 | 0.45495 | 0.0134 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:91 | 0.006689 | 0.45895 | 0.0174 | False | ser_his_acid_hydrolase | ser_his_acid_hydrolase |
| m_csa:621 | 0.016341 | 0.4602 | 0.01865 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:565 | 0.00687 | 0.46835 | 0.0268 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:299 | 0.081064 | 0.4712 | 0.02965 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:240 | 0.102791 | 0.4716 | 0.03005 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:244 | 0.037277 | 0.4724 | 0.03085 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:422 | 0.058882 | 0.47265 | 0.0311 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:405 | 0.042608 | 0.4837 | 0.04215 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:585 | 0.027437 | 0.4867 | 0.04515 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:645 | 0.018774 | 0.50615 | 0.0646 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:223 | 0.068591 | 0.5078 | 0.06625 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:36 | 0.016795 | 0.51785 | 0.0763 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:135 | 0.153072 | 0.5317 | 0.09015 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:322 | 0.011284 | 0.53375 | 0.0922 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:646 | 0.174004 | 0.54185 | 0.1003 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:533 | 0.015353 | 0.5423 | 0.10075 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:229 | 0.027164 | 0.5438 | 0.10225 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:463 | 0.048582 | 0.54765 | 0.1061 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:503 | 0.043551 | 0.55265 | 0.1111 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:84 | 0.048876 | 0.56755 | 0.126 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:638 | 0.041957 | 0.5862 | 0.14465 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:451 | 0.064766 | 0.588 | 0.14645 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:502 | 0.206148 | 0.5957 | 0.15415 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:464 | 0.028904 | 0.60295 | 0.1614 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:59 | 0.003362 | 0.60775 | 0.1662 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:74 | 0.033547 | 0.61305 | 0.1715 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:52 | 0.084691 | 0.6154 | 0.17385 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:256 | 0.038203 | 0.61925 | 0.1777 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:500 | 0.016116 | 0.61935 | 0.1778 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:25 | 0.161876 | 0.6241 | 0.18255 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:483 | 0.020918 | 0.6341 | 0.19255 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:190 | 0.047669 | 0.6365 | 0.19495 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:206 | 0.007512 | 0.63845 | 0.1969 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:289 | 0.980742 | 0.6398 | 0.19825 | False | flavin_dehydrogenase_reductase | flavin_dehydrogenase_reductase |
| m_csa:488 | 0.084131 | 0.64045 | 0.1989 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:468 | 0.181268 | 0.64225 | 0.2007 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:348 | 0.002478 | 0.649 | 0.20745 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:104 | 0.009963 | 0.6498 | 0.20825 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:269 | 0.003333 | 0.65065 | 0.2091 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:187 | 0.005281 | 0.65175 | 0.2102 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:308 | 0.291653 | 0.68115 | 0.2396 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:224 | 0.045267 | 0.4011 | -0.04045 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:78 | 0.15676 | 0.4054 | -0.03615 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:189 | 0.047288 | 0.4103 | -0.03125 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:441 | 0.016924 | 0.41695 | -0.0246 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:179 | 0.081808 | 0.42145 | -0.0201 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:22 | 0.057451 | 0.42405 | -0.0175 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:508 | 0.067949 | 0.42915 | -0.0124 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:51 | 0.113362 | 0.4314 | -0.01015 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:146 | 0.027848 | 0.43465 | -0.0069 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:342 | 0.045025 | 0.43935 | -0.0022 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |

## Decision

- Fixed threshold preserved: True
- Apply or change threshold now: False
- Deployment closed now: False
- Next gate: Keep the fixed 0.44155 combined_mean_geometry_fold threshold unchanged. The heldout confounded operating point remains research-ready under predicted-only inputs, but the train/cal cofactor and same-family structural proxies do not by themselves meet a confounded-safe calibration target; deployment closure still needs the explicit P10746 caveat decision or an approved non-residue sidecar.

## Interpretation

- The fixed fold operating point remains predicted-input-valid, but train/cal confounded-proxy abstention is weaker than the heldout confounded readout.
- Do not tune on the six heldout confounded rows. Resolve the source-decision blocker for P10746, and if stronger deployable confounded calibration is required, add more reviewed train/cal confounded proxy rows rather than changing the threshold from heldout.
