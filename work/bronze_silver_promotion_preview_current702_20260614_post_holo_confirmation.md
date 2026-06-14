# Bronze->Silver Promotion Preview

Run: 2026-06-14T12:24:54Z

Turns the representation loop's promotion triage into an explicit, non-destructive promotion QUEUE. It does NOT run or fake the deferred geometry confirmation (that gate abstains on predicted-apo coordinates) and flips no tier -- it stages which bronze labels are ready for that confirmation, which are blocked, and which need review first.

- Seed labels: 5638.
- **Silver-ready (pending the geometry-confirmation run): 109**.

## Decision counts

| decision | count |
| --- | --- |
| blocked_pending_structure | 2426 |
| hold_low_chemistry_cohesion | 1759 |
| review_chemistry_disagrees | 1344 |
| silver_ready_pending_geometry_run | 109 |

## Per-fingerprint breakdown

| fingerprint | decisions |
| --- | --- |
| askha_sugar_acetate_kinase | {'blocked_pending_structure': 96, 'review_chemistry_disagrees': 3, 'silver_ready_pending_geometry_run': 1} |
| atp_amide_ligase | {'blocked_pending_structure': 68, 'hold_low_chemistry_cohesion': 56, 'review_chemistry_disagrees': 20, 'silver_ready_pending_geometry_run': 6} |
| biotin_dependent_carboxylase | {'blocked_pending_structure': 74, 'hold_low_chemistry_cohesion': 23, 'silver_ready_pending_geometry_run': 3} |
| class_ii_metal_aldolase | {'hold_low_chemistry_cohesion': 120, 'review_chemistry_disagrees': 28, 'silver_ready_pending_geometry_run': 2} |
| coa_acyltransferase | {'blocked_pending_structure': 173, 'hold_low_chemistry_cohesion': 73, 'review_chemistry_disagrees': 4} |
| cobalamin_radical_rearrangement | {'blocked_pending_structure': 4, 'hold_low_chemistry_cohesion': 96, 'review_chemistry_disagrees': 20} |
| cofactor_independent_isomerase | {'blocked_pending_structure': 66, 'hold_low_chemistry_cohesion': 61, 'review_chemistry_disagrees': 23} |
| copper_oxidoreductase | {'hold_low_chemistry_cohesion': 125, 'review_chemistry_disagrees': 15} |
| cytochrome_p450_monooxygenase | {'blocked_pending_structure': 170, 'hold_low_chemistry_cohesion': 61, 'review_chemistry_disagrees': 12, 'silver_ready_pending_geometry_run': 7} |
| deoxynucleoside_kinase | {'blocked_pending_structure': 83, 'hold_low_chemistry_cohesion': 16, 'silver_ready_pending_geometry_run': 1} |
| flavin_dehydrogenase_reductase | {'blocked_pending_structure': 96, 'hold_low_chemistry_cohesion': 91, 'review_chemistry_disagrees': 9, 'silver_ready_pending_geometry_run': 6} |
| flavin_monooxygenase | {'blocked_pending_structure': 57, 'hold_low_chemistry_cohesion': 45, 'review_chemistry_disagrees': 6, 'silver_ready_pending_geometry_run': 6} |
| ghmp_small_molecule_kinase | {'review_chemistry_disagrees': 100} |
| glycoside_hydrolase | {'blocked_pending_structure': 61, 'hold_low_chemistry_cohesion': 14, 'review_chemistry_disagrees': 72, 'silver_ready_pending_geometry_run': 3} |
| glycosyltransferase | {'blocked_pending_structure': 126, 'hold_low_chemistry_cohesion': 33, 'review_chemistry_disagrees': 84, 'silver_ready_pending_geometry_run': 7} |
| heme_peroxidase_oxidase | {'blocked_pending_structure': 35, 'hold_low_chemistry_cohesion': 51, 'review_chemistry_disagrees': 11, 'silver_ready_pending_geometry_run': 2} |
| manganese_iron_superoxide_dismutase | {'blocked_pending_structure': 92, 'silver_ready_pending_geometry_run': 8} |
| metal_dependent_hydrolase | {'review_chemistry_disagrees': 225} |
| metal_racemase_epimerase_non_plp | {'hold_low_chemistry_cohesion': 49, 'review_chemistry_disagrees': 101} |
| metallo_amidohydrolase_deaminase | {'blocked_pending_structure': 77, 'hold_low_chemistry_cohesion': 25, 'review_chemistry_disagrees': 40, 'silver_ready_pending_geometry_run': 8} |
| metallopeptidase | {'hold_low_chemistry_cohesion': 33, 'review_chemistry_disagrees': 117} |
| metallophosphoesterase_nuclease | {'hold_low_chemistry_cohesion': 57, 'review_chemistry_disagrees': 93} |
| metallophosphomonoesterase | {'blocked_pending_structure': 108, 'hold_low_chemistry_cohesion': 16, 'review_chemistry_disagrees': 19, 'silver_ready_pending_geometry_run': 7} |
| molybdopterin_oxidoreductase | {'hold_low_chemistry_cohesion': 127, 'review_chemistry_disagrees': 123} |
| nad_p_dehydrogenase | {'blocked_pending_structure': 96, 'hold_low_chemistry_cohesion': 46, 'silver_ready_pending_geometry_run': 8} |
| non_heme_iron_2og_dioxygenase | {'blocked_pending_structure': 106, 'hold_low_chemistry_cohesion': 134, 'review_chemistry_disagrees': 7, 'silver_ready_pending_geometry_run': 3} |
| nucleoside_diphosphate_kinase | {'blocked_pending_structure': 98, 'hold_low_chemistry_cohesion': 1, 'silver_ready_pending_geometry_run': 1} |
| pfka_phosphofructokinase | {'blocked_pending_structure': 96, 'silver_ready_pending_geometry_run': 4} |
| pfkb_ribokinase_family | {'review_chemistry_disagrees': 128} |
| plp_dependent_enzyme | {'blocked_pending_structure': 19, 'hold_low_chemistry_cohesion': 88, 'review_chemistry_disagrees': 8, 'silver_ready_pending_geometry_run': 1} |
| protein_kinase_ser_thr_tyr | {'blocked_pending_structure': 91, 'hold_low_chemistry_cohesion': 4, 'review_chemistry_disagrees': 2, 'silver_ready_pending_geometry_run': 3} |
| radical_sam_enzyme | {'blocked_pending_structure': 135, 'hold_low_chemistry_cohesion': 46, 'silver_ready_pending_geometry_run': 3} |
| sam_methyltransferase | {'blocked_pending_structure': 120, 'hold_low_chemistry_cohesion': 121, 'review_chemistry_disagrees': 9} |
| ser_his_acid_hydrolase | {'hold_low_chemistry_cohesion': 79, 'review_chemistry_disagrees': 8} |
| terpene_cyclase_synthase | {'blocked_pending_structure': 141, 'hold_low_chemistry_cohesion': 12, 'review_chemistry_disagrees': 13, 'silver_ready_pending_geometry_run': 7} |
| thiamine_diphosphate_enzyme | {'blocked_pending_structure': 56, 'hold_low_chemistry_cohesion': 56, 'review_chemistry_disagrees': 32, 'silver_ready_pending_geometry_run': 6} |
| zinc_lyase_hydratase | {'blocked_pending_structure': 82, 'review_chemistry_disagrees': 12, 'silver_ready_pending_geometry_run': 6} |

## Policy

- Silver-ready: chemistry independently corroborates the assigned fingerprint AND the annotated cofactor is actually PRESENT in the coordinates (true holo, where the geometry gate is meetable), OR ser_his with a confirmed Ser-His-Asp triad.
- Gating audit NOT run here: geometry_inverse_gate_confirmation abstains on apo coordinates; it is NOT run or faked -- silver_ready rows are staged for that confirmation as a separate authorized step.

## Guardrails

- Registry written: False.
- Tier changed: False.
- Geometry confirmation run or faked: False.
- Chemistry corroboration is leakage-safe; promotion + geometry run are separate authorized steps.
