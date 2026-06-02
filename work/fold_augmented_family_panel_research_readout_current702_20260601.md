# Fold-Augmented Family-Panel Research Readout - current702

Run: 2026-06-02T19:15:47Z

Downstream fold-augmented research readout over review-only family-expansion packets. It applies the already selected combined_mean_geometry_fold threshold from the OOS-calibrated research contract to packet rows with both predicted geometry and predicted-structure Foldseek/TM evidence.

## Status

- family_panel_research_readout_ready_review_only
- Blockers: []
- Primary threshold: combined_mean_geometry_fold >= 0.44155
- Train/cal OOS sufficiency: research_contract_sufficient_with_blocker_disclosure

## Counts

- Panel packets: 7
- Candidate rows: 22
- Primary score-complete rows: 17
- Non-abstained review rows: 11
- Abstained review rows: 6
- Missing primary-channel scores: 5

## Panel Readout

| Panel | status | rows | complete | non-abstained | abstained | missing |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| glycyl_radical_or_thiamine_radical_lyase_boundary | score_complete_rows_all_abstained | 2 | 2 | 0 | 2 | 0 |
| thiol_disulfide_oxidoreductase_isomerase_boundary | score_complete_rows_all_abstained | 1 | 1 | 0 | 1 | 0 |
| lipoamide_or_sulfur_transfer_redox_boundary | has_non_abstained_review_rows | 2 | 2 | 1 | 1 | 0 |
| flavin_monooxygenase_and_flavin_oxygen_transfer | has_non_abstained_review_rows | 4 | 4 | 3 | 1 | 0 |
| cobalamin_and_radical_rearrangement_panel | has_non_abstained_review_rows | 3 | 2 | 2 | 0 | 1 |
| no_reliable_structure_metal_hydrolase_controls | has_non_abstained_review_rows | 6 | 3 | 3 | 0 | 3 |
| near_orphan_glycoside_or_nucleoside_hydrolase_controls | has_non_abstained_review_rows | 4 | 3 | 2 | 1 | 1 |

## Review-Priority Rows

| Row | panel | combined mean geometry+fold | margin | geometry top1 | nearest fold fingerprint | cofactor max |
| --- | --- | ---: | ---: | --- | --- | ---: |
| mh_068 | no_reliable_structure_metal_hydrolase_controls | 0.6903 | 0.24875 | metal_dependent_hydrolase | metal_dependent_hydrolase | None |
| mh_067 | no_reliable_structure_metal_hydrolase_controls | 0.68975 | 0.2482 | metal_dependent_hydrolase | metal_dependent_hydrolase | None |
| mh_066 | no_reliable_structure_metal_hydrolase_controls | 0.66335 | 0.2218 | metal_dependent_hydrolase | metal_dependent_hydrolase | None |
| m_csa:267 | lipoamide_or_sulfur_transfer_redox_boundary | 0.5679 | 0.12635 | heme_peroxidase_oxidase | flavin_dehydrogenase_reductase | 0.834847 |
| m_csa:131 | flavin_monooxygenase_and_flavin_oxygen_transfer | 0.5516 | 0.11005 | metal_dependent_hydrolase | flavin_dehydrogenase_reductase | 0.980908 |
| m_csa:750 | cobalamin_and_radical_rearrangement_panel | 0.55105 | 0.1095 | metal_dependent_hydrolase | flavin_dehydrogenase_reductase | 0.703989 |
| m_csa:551 | flavin_monooxygenase_and_flavin_oxygen_transfer | 0.5446 | 0.10305 | metal_dependent_hydrolase | flavin_dehydrogenase_reductase | 0.922628 |
| m_csa:132 | flavin_monooxygenase_and_flavin_oxygen_transfer | 0.53865 | 0.0971 | ser_his_acid_hydrolase | flavin_dehydrogenase_reductase | 0.010805 |
| mh_073 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | 0.48775 | 0.0462 | ser_his_acid_hydrolase | metal_dependent_hydrolase | None |
| secondary_probe::radical_sam_enzyme | cobalamin_and_radical_rearrangement_panel | 0.48335 | 0.0418 | metal_dependent_hydrolase | plp_dependent_enzyme | None |
| m_csa:116 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | 0.45755 | 0.016 | metal_dependent_hydrolase | metal_dependent_hydrolase | 0.050535 |

## Interpretation

- 11/17 score-complete review rows remain non-abstained at the bounded fold-augmented research threshold.
- This is a downstream review readout only. It does not promote family rows, retune thresholds, train on heldout rows, or change production scoring.
- Source-check the non-abstained review-priority rows and keep geometry/fold-missing packet rows in the coordinate or sidecar materialization queue before any family-expansion decision.
