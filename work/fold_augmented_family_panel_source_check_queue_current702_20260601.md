# Fold-Augmented Family-Panel Source-Check Queue - current702

Run: 2026-06-02T19:15:47Z

Review-only source-check queue for family-panel rows that remain non-abstained under the fixed fold-augmented research threshold.

## Status

- source_check_queue_ready_review_only
- Source-check rows: 11
- Panels represented: 5

## Queue

| rank | row | panel | combined mean geometry+fold | margin | geometry top1 | nearest fold fingerprint | focus |
| ---: | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | mh_068 | no_reliable_structure_metal_hydrolase_controls | 0.6903 | 0.24875 | metal_dependent_hydrolase | metal_dependent_hydrolase | row_specific_bond_change_and_mechanism_locus, cofactor_locus_and_redox_partner_identity, occupied_primary_fold_false_confidence_review |
| 2 | mh_067 | no_reliable_structure_metal_hydrolase_controls | 0.68975 | 0.2482 | metal_dependent_hydrolase | metal_dependent_hydrolase | row_specific_bond_change_and_mechanism_locus, cofactor_locus_and_redox_partner_identity, occupied_primary_fold_false_confidence_review |
| 3 | mh_066 | no_reliable_structure_metal_hydrolase_controls | 0.66335 | 0.2218 | metal_dependent_hydrolase | metal_dependent_hydrolase | row_specific_bond_change_and_mechanism_locus, cofactor_locus_and_redox_partner_identity, occupied_primary_fold_false_confidence_review |
| 4 | m_csa:267 | lipoamide_or_sulfur_transfer_redox_boundary | 0.5679 | 0.12635 | heme_peroxidase_oxidase | flavin_dehydrogenase_reductase | row_specific_bond_change_and_mechanism_locus, cofactor_locus_and_redox_partner_identity, occupied_primary_fold_false_confidence_review, geometry_fold_fingerprint_disagreement, selected_organic_cofactor_confounding |
| 5 | m_csa:131 | flavin_monooxygenase_and_flavin_oxygen_transfer | 0.5516 | 0.11005 | metal_dependent_hydrolase | flavin_dehydrogenase_reductase | row_specific_bond_change_and_mechanism_locus, cofactor_locus_and_redox_partner_identity, occupied_primary_fold_false_confidence_review, geometry_fold_fingerprint_disagreement, selected_organic_cofactor_confounding |
| 6 | m_csa:750 | cobalamin_and_radical_rearrangement_panel | 0.55105 | 0.1095 | metal_dependent_hydrolase | flavin_dehydrogenase_reductase | row_specific_bond_change_and_mechanism_locus, cofactor_locus_and_redox_partner_identity, occupied_primary_fold_false_confidence_review, geometry_fold_fingerprint_disagreement, selected_organic_cofactor_confounding |
| 7 | m_csa:551 | flavin_monooxygenase_and_flavin_oxygen_transfer | 0.5446 | 0.10305 | metal_dependent_hydrolase | flavin_dehydrogenase_reductase | row_specific_bond_change_and_mechanism_locus, cofactor_locus_and_redox_partner_identity, occupied_primary_fold_false_confidence_review, geometry_fold_fingerprint_disagreement, selected_organic_cofactor_confounding |
| 8 | m_csa:132 | flavin_monooxygenase_and_flavin_oxygen_transfer | 0.53865 | 0.0971 | ser_his_acid_hydrolase | flavin_dehydrogenase_reductase | row_specific_bond_change_and_mechanism_locus, cofactor_locus_and_redox_partner_identity, occupied_primary_fold_false_confidence_review, geometry_fold_fingerprint_disagreement, selected_organic_cofactor_confounding |
| 9 | mh_073 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | 0.48775 | 0.0462 | ser_his_acid_hydrolase | metal_dependent_hydrolase | row_specific_bond_change_and_mechanism_locus, cofactor_locus_and_redox_partner_identity, occupied_primary_fold_false_confidence_review, geometry_fold_fingerprint_disagreement |
| 10 | secondary_probe::radical_sam_enzyme | cobalamin_and_radical_rearrangement_panel | 0.48335 | 0.0418 | metal_dependent_hydrolase | plp_dependent_enzyme | row_specific_bond_change_and_mechanism_locus, cofactor_locus_and_redox_partner_identity, occupied_primary_fold_false_confidence_review, geometry_fold_fingerprint_disagreement |
| 11 | m_csa:116 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | 0.45755 | 0.016 | metal_dependent_hydrolase | metal_dependent_hydrolase | row_specific_bond_change_and_mechanism_locus, cofactor_locus_and_redox_partner_identity, occupied_primary_fold_false_confidence_review, selected_organic_cofactor_confounding |

## Guardrails

- Review-only source checking only. No labels, registries, ontologies, imports, thresholds, training data, or production scoring changed.

## Interpretation

- 11 non-abstained family-panel rows need review-only source checking before any family-expansion decision.
- Work the queue in rank order, starting with the largest positive threshold margin, and record source-backed accept/reject/hold evidence without changing labels.
