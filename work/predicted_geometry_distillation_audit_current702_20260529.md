# Predicted Geometry Distillation Audit

Run: 2026-05-29T19:23:38Z

This trains/calibrates geometry heads on AlphaFoldDB-predicted in-distribution geometry and evaluates AlphaFoldDB-predicted heldout geometry once. Current M-CSA/current702 labels are the teacher labels. No labels, registries, ontologies, production scoring, imports, or global thresholds were edited.

## Cheap Error-Mode Fork

- Wrong non-abstained hand-router primary rows: 5.
- True-channel counts: {'cofactor_defined': 5}.
- Called-channel counts: {'cofactor_defined': 4, 'cofactor_independent': 1}.

| Entry | True fingerprint | True channel | Called fingerprint | Score |
| --- | --- | --- | --- | ---: |
| m_csa:44 | metal_dependent_hydrolase | cofactor_defined | ser_his_acid_hydrolase | 0.4316 |
| m_csa:239 | heme_peroxidase_oxidase | cofactor_defined | metal_dependent_hydrolase | 0.5423 |
| m_csa:250 | heme_peroxidase_oxidase | cofactor_defined | metal_dependent_hydrolase | 0.5425 |
| m_csa:497 | flavin_dehydrogenase_reductase | cofactor_defined | metal_dependent_hydrolase | 0.5899 |
| m_csa:990 | flavin_dehydrogenase_reductase | cofactor_defined | metal_dependent_hydrolase | 0.5209 |

## Distillation Result

- Target rows: 641/702 current702 rows; split counts {'heldout': 128, 'in_distribution': 513}.
- AlphaFoldDB geometry availability: 624/641 ok; 16 fetch failures; 0 rows with proximal ligands.
- Hand router on predicted heldout geometry: 23/45 primary correct, 17 abstained, 5 wrong nonabstained; OOS/sec FP rate 0.123457.
- Logistic: 2/45 primary correct, 43 abstained, 0 wrong nonabstained; OOS/sec FP rate 0.012346.
- MLP-32: 2/45 primary correct, 43 abstained, 0 wrong nonabstained; OOS/sec FP rate 0.0.
- OOS-aware MLP-32: 11/45 primary correct, 33 abstained, 1 wrong nonabstained; OOS/sec FP rate 0.012346.
- Interpretation: predicted_geometry_distillation_does_not_recover_clean_geometry.

## Caveat

This is still an active-site-position-known experiment: M-CSA catalytic residue identities, roles, and sequence positions are used to extract predicted geometry. It tests degraded-coordinate robustness, not active-site localization from raw sequence.
