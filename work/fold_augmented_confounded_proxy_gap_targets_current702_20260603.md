# Fold-Augmented Confounded Proxy Gap Targets - current702

Run: 2026-06-03T12:17:17Z

Review-only Lever 3 packet of train/cal confounded-proxy rows that are retained by the fixed predicted-structure-vs-atlas fold operating point. It is derived from the proxy audit and does not read heldout rows or select a threshold.

## Status

- fold_augmented_confounded_proxy_gap_targets_ready
- Fixed channel: combined_mean_geometry_fold
- Fixed threshold: 0.44155
- Retained proxy gap rows: 14
- High-cofactor retained proxy gaps: 1
- Same-family structural retained proxy gaps: 13

## Priority Counts

- priority_1_high_cofactor_retained_proxy_gap: 1
- priority_2_hard_retained_structural_proxy_gap: 8
- priority_3_near_threshold_retained_structural_proxy_gap: 5

## Retained Gap Rows

| priority | entry | margin | score | proxies | nearest fingerprint | top1 fingerprint |
| --- | --- | ---: | ---: | --- | --- | --- |
| priority_1_high_cofactor_retained_proxy_gap | m_csa:368 | 0.01215 | 0.4537 | high_cofactor_signature_proxy | flavin_dehydrogenase_reductase | heme_peroxidase_oxidase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:104 | 0.20825 | 0.6498 | same_family_structural_proxy | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:483 | 0.19255 | 0.6341 | same_family_structural_proxy | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:25 | 0.18255 | 0.6241 | same_family_structural_proxy | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:52 | 0.17385 | 0.6154 | same_family_structural_proxy | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:464 | 0.1614 | 0.60295 | same_family_structural_proxy | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:503 | 0.1111 | 0.55265 | same_family_structural_proxy | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:646 | 0.1003 | 0.54185 | same_family_structural_proxy | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_2_hard_retained_structural_proxy_gap | m_csa:36 | 0.0763 | 0.51785 | same_family_structural_proxy | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:422 | 0.0311 | 0.47265 | same_family_structural_proxy | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:244 | 0.03085 | 0.4724 | same_family_structural_proxy | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:299 | 0.02965 | 0.4712 | same_family_structural_proxy | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:565 | 0.0268 | 0.46835 | same_family_structural_proxy | metal_dependent_hydrolase | metal_dependent_hydrolase |
| priority_3_near_threshold_retained_structural_proxy_gap | m_csa:119 | 0.00475 | 0.4463 | same_family_structural_proxy | metal_dependent_hydrolase | metal_dependent_hydrolase |

## Decision

- Apply or change threshold now: False
- Deployment closed now: False
- Next gate: Use these retained train/cal proxy rows to design or review additional calibration-confounded proxy evidence. Do not adjust the fixed operating threshold from these rows without rerunning the full train/cal contract, and do not tune on heldout.

## Interpretation

- 14 train/cal confounded-proxy rows are retained at the fixed fold operating point and define the next calibration gap surface.
- Prioritize high-cofactor retained gaps first, then hard retained same-family structural gaps with the largest positive margins.
