# ATP phosphotransferase kinase mechanism-handle scout

Run: 2026-06-13T04:34:17Z

Non-destructive reviewed Swiss-Prot scout over EC 2.7 kinase/phosphotransferase candidates. EC is scope-only; no labels or predictive features were emitted.

- Entries examined: 80.
- Fetch failures: 0.
- Wire 25fp lane now: False; split/guard subclasses first.

| Handle | Count |
| --- | ---: |
| active_or_binding_site_context | 79 |
| adp_or_phosphate_context | 80 |
| atp_context | 80 |
| kinase_text | 80 |
| likely_wireable_by_non_ec_handles | 4 |
| mg_context | 36 |
| multi_subclass_boundary | 75 |
| non_2_7_side_ec_boundary | 1 |
| nucleotide_transferase_boundary | 2 |
| phosphoryl_transfer_text | 12 |
| protein_kinase_boundary | 75 |
| rhea_cross_reference_present | 80 |
| sugar_kinase_boundary | 80 |
| transferase_keyword | 80 |

## Guardrails

- EC 2.7 was used only for scope/supply.
- Strong ATP/Mg/phosphoryl handles exist, but the lane is broad; split ePK/ASKHA/Pfk/GHMP/NDK/DNK/GHKL or define a narrow family before any 25fp wiring.
- Guard ATP ligases, glycosyltransferases, hydrolase side rows, nucleotide transferases, and multi-subclass signals.
