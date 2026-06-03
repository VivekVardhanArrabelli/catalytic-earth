# Fold-Augmented Confounded Proxy Operating-Point Audit - current702

Run: 2026-06-03T12:14:37Z

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
| all calibration OOS | 75 | 30 | 0.4 |
| high-cofactor calibration OOS | 1 | 0 | 0.0 |
| low-cofactor calibration OOS | 74 | 30 | 0.4054 |
| same-family structural proxy OOS | 17 | 4 | 0.2353 |

## Heldout Carry-Through

- Confounded OOS abstained: 5/6
- In-scope retained: 45/47

## High-Cofactor Train/Cal Rows

| entry | cofactor | score | margin | abstains | nearest atlas fingerprint | top1 geometry fingerprint |
| --- | ---: | ---: | ---: | --- | --- | --- |
| m_csa:368 | 0.990498 | 0.4537 | 0.01215 | False | flavin_dehydrogenase_reductase | heme_peroxidase_oxidase |

## Same-Family Structural Train/Cal Rows

| entry | cofactor | score | margin | abstains | nearest atlas fingerprint | top1 geometry fingerprint |
| --- | ---: | ---: | ---: | --- | --- | --- |
| m_csa:119 | 0.118424 | 0.4463 | 0.00475 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:565 | 0.00687 | 0.46835 | 0.0268 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:299 | 0.081064 | 0.4712 | 0.02965 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:244 | 0.037277 | 0.4724 | 0.03085 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:422 | 0.058882 | 0.47265 | 0.0311 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:36 | 0.016795 | 0.51785 | 0.0763 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:646 | 0.174004 | 0.54185 | 0.1003 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:503 | 0.043551 | 0.55265 | 0.1111 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:464 | 0.028904 | 0.60295 | 0.1614 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:52 | 0.084691 | 0.6154 | 0.17385 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:25 | 0.161876 | 0.6241 | 0.18255 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:483 | 0.020918 | 0.6341 | 0.19255 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:104 | 0.009963 | 0.6498 | 0.20825 | False | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:78 | 0.15676 | 0.4054 | -0.03615 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:189 | 0.047288 | 0.4103 | -0.03125 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:22 | 0.057451 | 0.42405 | -0.0175 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |
| m_csa:342 | 0.045025 | 0.43935 | -0.0022 | True | metal_dependent_hydrolase | metal_dependent_hydrolase |

## Decision

- Fixed threshold preserved: True
- Apply or change threshold now: False
- Deployment closed now: False
- Next gate: Keep the fixed 0.44155 combined_mean_geometry_fold threshold unchanged. The heldout confounded operating point remains research-ready under predicted-only inputs, but the train/cal cofactor and same-family structural proxies do not by themselves meet a confounded-safe calibration target; deployment closure still needs the explicit P10746 caveat decision or an approved non-residue sidecar.

## Interpretation

- The fixed fold operating point remains predicted-input-valid, but train/cal confounded-proxy abstention is weaker than the heldout confounded readout.
- Do not tune on the six heldout confounded rows. Resolve the source-decision blocker for P10746, and if stronger deployable confounded calibration is required, add more reviewed train/cal confounded proxy rows rather than changing the threshold from heldout.
