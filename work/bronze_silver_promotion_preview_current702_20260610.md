# Bronze->Silver Promotion Preview

Run: 2026-06-10T05:37:59Z

Turns the representation loop's promotion triage into an explicit, non-destructive promotion QUEUE. It does NOT run or fake the deferred geometry confirmation (that gate abstains on predicted-apo coordinates) and flips no tier -- it stages which bronze labels are ready for that confirmation, which are blocked, and which need review first.

- Seed labels: 486.
- **Silver-ready (pending the geometry-confirmation run): 47**.

## Decision counts

| decision | count |
| --- | --- |
| blocked_apo_needs_cofactor_fusion | 50 |
| blocked_pending_structure | 295 |
| hold_low_chemistry_cohesion | 67 |
| review_chemistry_disagrees | 27 |
| silver_ready_pending_geometry_run | 47 |

## Per-fingerprint breakdown

| fingerprint | decisions |
| --- | --- |
| cobalamin_radical_rearrangement | {'blocked_pending_structure': 6, 'hold_low_chemistry_cohesion': 1} |
| flavin_dehydrogenase_reductase | {'blocked_apo_needs_cofactor_fusion': 2, 'blocked_pending_structure': 21, 'hold_low_chemistry_cohesion': 6, 'review_chemistry_disagrees': 10} |
| flavin_monooxygenase | {'blocked_pending_structure': 27, 'hold_low_chemistry_cohesion': 5, 'review_chemistry_disagrees': 9} |
| heme_peroxidase_oxidase | {'blocked_pending_structure': 30, 'hold_low_chemistry_cohesion': 19} |
| metal_dependent_hydrolase | {'blocked_apo_needs_cofactor_fusion': 48, 'blocked_pending_structure': 104, 'hold_low_chemistry_cohesion': 22, 'review_chemistry_disagrees': 8, 'silver_ready_pending_geometry_run': 43} |
| plp_dependent_enzyme | {'blocked_pending_structure': 99, 'hold_low_chemistry_cohesion': 13, 'silver_ready_pending_geometry_run': 4} |
| radical_sam_enzyme | {'blocked_pending_structure': 8, 'hold_low_chemistry_cohesion': 1} |

## Policy

- Silver-ready: chemistry independently corroborates the assigned fingerprint AND the deferred geometry confirmation is runnable (holo structure), OR ser_his with a confirmed Ser-His-Asp triad.
- Gating audit NOT run here: geometry_inverse_gate_confirmation abstains on predicted-apo coordinates; it is NOT run or faked -- silver_ready rows are staged for that confirmation as a separate authorized step.

## Guardrails

- Registry written: False.
- Tier changed: False.
- Geometry confirmation run or faked: False.
- Chemistry corroboration is leakage-safe; promotion + geometry run are separate authorized steps.
