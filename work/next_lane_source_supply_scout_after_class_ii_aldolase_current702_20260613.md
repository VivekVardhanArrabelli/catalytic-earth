# Next-lane source-supply scout after class-II metal aldolase

Run: 2026-06-13T04:33:19Z

Non-destructive reviewed Swiss-Prot supply scout over remaining breadth candidates after class_ii_metal_aldolase became the 24th fingerprint. No registry write, no labels emitted.

- Candidates probed: 6.
- Fetch failures: 0.
- Recommended next candidate: `atp_phosphotransferase_kinase`.
- Wire next lane now: True (mechanism-handle scout still required first).

| Candidate | reviewed supply | EC-only ceiling | capture | est. admissible | distinct full EC sample | reaction-poor | clean | cap |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: |
| atp_phosphotransferase_kinase | 21822 | 34140 | 0.639 | 150 | 30 | True | True | 150 |
| thiamine_diphosphate_enzyme | 1262 | 7020 | 0.18 | 150 | 22 | True | True | 150 |
| zinc_lyase_hydratase | 488 | 8582 | 0.057 | 150 | 21 | True | True | 150 |
| enolase_superfamily_lyase | 915 | 8582 | 0.107 | 150 | 1 | True | True | 150 |
| biotin_dependent_carboxylase | 88 | 4071 | 0.022 | 44 | 10 | True | False | 250 |
| manganese_iron_superoxide_dismutase | 1 | 470 | 0.002 | 0 | 1 | False | False | 250 |

## Guardrails

- EC/cofactor handles were used only for source-supply and scope estimation.
- The recommended lane still needs a mechanism-handle scout and explicit boundary guards before 25fp wiring.
