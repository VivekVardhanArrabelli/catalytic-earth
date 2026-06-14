# Bronze->Silver Promotion Preview

Run: 2026-06-14T11:00:13Z

Turns the representation loop's promotion triage into an explicit, non-destructive promotion QUEUE. It does NOT run or fake the deferred geometry confirmation (that gate abstains on predicted-apo coordinates) and flips no tier -- it stages which bronze labels are ready for that confirmation, which are blocked, and which need review first.

- Seed labels: 5638.
- **Silver-ready (pending the geometry-confirmation run): 0**.

## Decision counts

| decision | count |
| --- | --- |
| blocked_apo_needs_cofactor_fusion | 3 |
| blocked_pending_structure | 2612 |
| hold_low_chemistry_cohesion | 1451 |
| review_chemistry_disagrees | 1572 |

## Per-fingerprint breakdown

| fingerprint | decisions |
| --- | --- |
| askha_sugar_acetate_kinase | {'blocked_pending_structure': 97, 'review_chemistry_disagrees': 3} |
| atp_amide_ligase | {'blocked_pending_structure': 76, 'hold_low_chemistry_cohesion': 54, 'review_chemistry_disagrees': 20} |
| biotin_dependent_carboxylase | {'blocked_pending_structure': 77, 'hold_low_chemistry_cohesion': 23} |
| class_ii_metal_aldolase | {'blocked_pending_structure': 2, 'review_chemistry_disagrees': 148} |
| coa_acyltransferase | {'blocked_pending_structure': 187, 'hold_low_chemistry_cohesion': 50, 'review_chemistry_disagrees': 13} |
| cobalamin_radical_rearrangement | {'blocked_pending_structure': 4, 'hold_low_chemistry_cohesion': 96, 'review_chemistry_disagrees': 20} |
| cofactor_independent_isomerase | {'blocked_pending_structure': 67, 'hold_low_chemistry_cohesion': 59, 'review_chemistry_disagrees': 24} |
| copper_oxidoreductase | {'hold_low_chemistry_cohesion': 115, 'review_chemistry_disagrees': 25} |
| cytochrome_p450_monooxygenase | {'blocked_pending_structure': 177, 'hold_low_chemistry_cohesion': 61, 'review_chemistry_disagrees': 12} |
| deoxynucleoside_kinase | {'blocked_pending_structure': 84, 'hold_low_chemistry_cohesion': 16} |
| flavin_dehydrogenase_reductase | {'blocked_pending_structure': 115, 'hold_low_chemistry_cohesion': 67, 'review_chemistry_disagrees': 20} |
| flavin_monooxygenase | {'blocked_pending_structure': 63, 'hold_low_chemistry_cohesion': 45, 'review_chemistry_disagrees': 6} |
| ghmp_small_molecule_kinase | {'review_chemistry_disagrees': 100} |
| glycoside_hydrolase | {'blocked_pending_structure': 67, 'hold_low_chemistry_cohesion': 11, 'review_chemistry_disagrees': 72} |
| glycosyltransferase | {'blocked_pending_structure': 133, 'hold_low_chemistry_cohesion': 26, 'review_chemistry_disagrees': 91} |
| heme_peroxidase_oxidase | {'blocked_pending_structure': 50, 'hold_low_chemistry_cohesion': 38, 'review_chemistry_disagrees': 11} |
| manganese_iron_superoxide_dismutase | {'blocked_pending_structure': 100} |
| metal_dependent_hydrolase | {'review_chemistry_disagrees': 225} |
| metal_racemase_epimerase_non_plp | {'hold_low_chemistry_cohesion': 49, 'review_chemistry_disagrees': 101} |
| metallo_amidohydrolase_deaminase | {'blocked_pending_structure': 85, 'hold_low_chemistry_cohesion': 20, 'review_chemistry_disagrees': 45} |
| metallopeptidase | {'hold_low_chemistry_cohesion': 33, 'review_chemistry_disagrees': 117} |
| metallophosphoesterase_nuclease | {'hold_low_chemistry_cohesion': 18, 'review_chemistry_disagrees': 132} |
| metallophosphomonoesterase | {'blocked_pending_structure': 118, 'hold_low_chemistry_cohesion': 15, 'review_chemistry_disagrees': 17} |
| molybdopterin_oxidoreductase | {'hold_low_chemistry_cohesion': 132, 'review_chemistry_disagrees': 118} |
| nad_p_dehydrogenase | {'blocked_pending_structure': 104, 'hold_low_chemistry_cohesion': 46} |
| non_heme_iron_2og_dioxygenase | {'blocked_pending_structure': 111, 'hold_low_chemistry_cohesion': 107, 'review_chemistry_disagrees': 32} |
| nucleoside_diphosphate_kinase | {'blocked_pending_structure': 99, 'hold_low_chemistry_cohesion': 1} |
| pfka_phosphofructokinase | {'blocked_pending_structure': 100} |
| pfkb_ribokinase_family | {'review_chemistry_disagrees': 128} |
| plp_dependent_enzyme | {'blocked_apo_needs_cofactor_fusion': 3, 'blocked_pending_structure': 33, 'hold_low_chemistry_cohesion': 72, 'review_chemistry_disagrees': 8} |
| protein_kinase_ser_thr_tyr | {'blocked_pending_structure': 94, 'hold_low_chemistry_cohesion': 4, 'review_chemistry_disagrees': 2} |
| radical_sam_enzyme | {'blocked_pending_structure': 138, 'hold_low_chemistry_cohesion': 46} |
| sam_methyltransferase | {'blocked_pending_structure': 120, 'hold_low_chemistry_cohesion': 121, 'review_chemistry_disagrees': 9} |
| ser_his_acid_hydrolase | {'hold_low_chemistry_cohesion': 79, 'review_chemistry_disagrees': 8} |
| terpene_cyclase_synthase | {'blocked_pending_structure': 148, 'hold_low_chemistry_cohesion': 12, 'review_chemistry_disagrees': 13} |
| thiamine_diphosphate_enzyme | {'blocked_pending_structure': 75, 'hold_low_chemistry_cohesion': 35, 'review_chemistry_disagrees': 40} |
| zinc_lyase_hydratase | {'blocked_pending_structure': 88, 'review_chemistry_disagrees': 12} |

## Policy

- Silver-ready: chemistry independently corroborates the assigned fingerprint AND the annotated cofactor is actually PRESENT in the coordinates (true holo, where the geometry gate is meetable), OR ser_his with a confirmed Ser-His-Asp triad.
- Gating audit NOT run here: geometry_inverse_gate_confirmation abstains on apo coordinates; it is NOT run or faked -- silver_ready rows are staged for that confirmation as a separate authorized step.

## Guardrails

- Registry written: False.
- Tier changed: False.
- Geometry confirmation run or faked: False.
- Chemistry corroboration is leakage-safe; promotion + geometry run are separate authorized steps.
