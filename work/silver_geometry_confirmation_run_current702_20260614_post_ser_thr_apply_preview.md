# Silver Geometry Confirmation Run

Run: 2026-06-14T23:28:27Z

Runs the separate geometry-confirmation gate for silver-ready rows that
already have sha-matched holo coordinates and explicit PDB residue mappings.

## Result

- Silver-ready input rows: 202.
- Ready/runnable rows scored: 108.
- Geometry rows OK: 106.
- Passed geometry confirmation: 0.
- Held by geometry confirmation: 108.
- Silver flips applied: 0.

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- Source annotation roles used for score: False.
- Text/name/label fields used for score: False.

## Decisions By Fingerprint

| fingerprint | pass | hold |
| --- | ---: | ---: |
| askha_sugar_acetate_kinase | 0 | 1 |
| atp_amide_ligase | 0 | 6 |
| biotin_dependent_carboxylase | 0 | 2 |
| class_ii_metal_aldolase | 0 | 1 |
| cytochrome_p450_monooxygenase | 0 | 7 |
| deoxynucleoside_kinase | 0 | 1 |
| flavin_dehydrogenase_reductase | 0 | 2 |
| flavin_monooxygenase | 0 | 7 |
| glycoside_hydrolase | 0 | 2 |
| glycosyltransferase | 0 | 6 |
| heme_peroxidase_oxidase | 0 | 1 |
| manganese_iron_superoxide_dismutase | 0 | 11 |
| metallo_amidohydrolase_deaminase | 0 | 6 |
| metallophosphomonoesterase | 0 | 5 |
| nad_p_dehydrogenase | 0 | 11 |
| non_heme_iron_2og_dioxygenase | 0 | 3 |
| nucleoside_diphosphate_kinase | 0 | 1 |
| pfka_phosphofructokinase | 0 | 2 |
| protein_kinase_ser_thr_tyr | 0 | 10 |
| radical_sam_enzyme | 0 | 1 |
| terpene_cyclase_synthase | 0 | 8 |
| thiamine_diphosphate_enzyme | 0 | 4 |
| zinc_lyase_hydratase | 0 | 10 |

## Next Action

- Continue explicit residue mapping for blocked silver-ready rows and treat
  held geometry rows as calibration/representation gaps unless new local
  structure evidence changes the gate result.
