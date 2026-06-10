# Cofactor/EC Disambiguation Of Held Redox + Radical-SAM/Cobalamin Lanes

Run: 2026-06-10T02:59:48Z

Makes a high-precision subset of the previously-HELD cofactor-confounded
redox and secondary-probe radical-SAM/cobalamin rows countable, by
corroborating the annotated cofactor against the reviewed reaction/EC
class. Only unique single-fingerprint matches are imported; multi-signal
rows stay held. EC is used for scope assignment only and is never a
predictive feature. The frozen current702 benchmark is NOT written.

## Result

- Held rows examined: 875.
- **Disambiguated bronze labels: 143** -> expansion registry 1567 -> **1710** if merged.
- Fingerprints recovered: {'cobalamin_radical_rearrangement': 7, 'flavin_dehydrogenase_reductase': 37, 'flavin_monooxygenase': 41, 'heme_peroxidase_oxidase': 49, 'radical_sam_enzyme': 9}.
- Confidence: {'medium': 143}.
- Still held: 730 ({'no_cofactor_ec_corroboration': 723, 'multi_fingerprint_signal_conflict': 7}).
- Skipped: 2.

## Per-pool decisions

| Pool | decisions |
| --- | --- |
| plp_radical_cobalamin | {'hold': 10, 'import': 15} |
| redox_cofactor_confounded | {'import': 128, 'hold': 613, 'skip_screen': 2} |
| wave2_held_redox_radical | {'hold': 107} |

## Diversity by lane (recovered fingerprint)

| Lane | recovered |
| --- | --- |
| B12/cobalamin broad enzymes | {'cobalamin_radical_rearrangement': 2} |
| Fe-S/flavin combined systems | {'flavin_dehydrogenase_reductase': 5, 'flavin_monooxygenase': 1, 'radical_sam_enzyme': 1} |
| SAM-dependent radical-like boundary | {'radical_sam_enzyme': 1} |
| cobalamin radical rearrangement | {'cobalamin_radical_rearrangement': 4} |
| coupled PLP adenosylcobalamin aminomutase | {'cobalamin_radical_rearrangement': 1} |
| flavin monooxygenase | {'flavin_monooxygenase': 28} |
| flavin redox boundary | {'flavin_dehydrogenase_reductase': 23, 'flavin_monooxygenase': 2} |
| heme peroxidase/oxidase-like | {'heme_peroxidase_oxidase': 47, 'flavin_dehydrogenase_reductase': 6} |
| radical SAM iron-sulfur | {'radical_sam_enzyme': 5} |
| radical SAM named families | {'radical_sam_enzyme': 2} |
| redox oxygen/sulfur | {'flavin_monooxygenase': 10, 'heme_peroxidase_oxidase': 2} |
| sulfur oxidoreductase | {'flavin_dehydrogenase_reductase': 3} |

## Guardrails

- Curated registry written: False.
- EC used for scope assignment only, never predictive: True.
- Multi-fingerprint-signal rows held: True.
- All new labels bronze / automation_curated; uniprot namespace; heldout benchmark unchanged.

## Next action

- On explicit authorization, append `applied_labels` to the SEPARATE expansion registry `data/registries/external_bronze_labels.json` via `apply-external-annotation-anchored-import`. Rows still held (no/ambiguous cofactor-EC corroboration) remain a review queue.
