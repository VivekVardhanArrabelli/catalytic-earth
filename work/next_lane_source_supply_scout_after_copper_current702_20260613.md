# Next-lane source-supply scout after copper

Run: 2026-06-13T03:16:29Z

Non-destructive reviewed Swiss-Prot supply scout over remaining breadth candidates after copper_oxidoreductase became the 21st fingerprint. No registry write, no labels emitted.

- Candidates probed: 9.
- Fetch failures: 0.
- Recommended next candidate: `metal_racemase_epimerase_non_plp`.
- Wire 22fp lane now: True (mechanism-handle scout still required first).

| Candidate | reviewed supply | EC-only ceiling | capture | est. admissible | distinct full EC sample | reaction-poor | clean | cap |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: |
| metal_racemase_epimerase_non_plp | 2141 | 2319 | 0.923 | 150 | 52 | False | True | 150 |
| atp_amide_ligase | 13599 | 12835 | 1.06 | 150 | 51 | False | True | 150 |
| class_ii_metal_aldolase | 846 | 1921 | 0.44 | 150 | 37 | True | True | 150 |
| atp_phosphotransferase_kinase | 21822 | 34140 | 0.639 | 150 | 28 | True | True | 150 |
| thiamine_diphosphate_enzyme | 1262 | 7020 | 0.18 | 150 | 20 | True | True | 150 |
| zinc_lyase_hydratase | 488 | 8582 | 0.057 | 150 | 15 | True | True | 150 |
| enolase_superfamily_lyase | 915 | 8582 | 0.107 | 150 | 1 | True | True | 150 |
| manganese_iron_superoxide_dismutase | 1 | 470 | 0.002 | 0 | 1 | False | False | 250 |
| biotin_dependent_carboxylase | 88 | 4071 | 0.022 | 44 | 10 | True | False | 250 |

## Guardrails

- EC was used only for scope/supply estimation; no labels or predictive features were emitted.
- Any recommended lane still needs a mechanism-handle scout and explicit boundary guards before 22fp wiring.
