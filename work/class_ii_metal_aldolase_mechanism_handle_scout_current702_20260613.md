# Class-II metal aldolase mechanism-handle scout

Run: 2026-06-13T04:20:51Z

Non-destructive reviewed Swiss-Prot scout over EC 4.1.2/4.1.3 metal lyase candidates. EC is scope-only; no labels or predictive features were emitted.

- Entries examined: 80.
- Fetch failures: 0.
- Wire 24fp lane now: True.

| Handle | Count |
| --- | ---: |
| active_or_binding_or_metal_site_context | 80 |
| aldolase_or_oxoacid_text | 61 |
| c_c_bond_reaction_text | 58 |
| hydrolase_side_ec_boundary | 8 |
| likely_wireable_by_non_ec_handles | 53 |
| lyase_keyword_or_text | 80 |
| metal_context | 80 |
| non_4_1_2_or_4_1_3_side_ec_boundary | 20 |
| plp_boundary | 2 |
| rhea_cross_reference_present | 80 |
| schiff_base_class_i_boundary | 4 |
| thdp_boundary | 5 |
| transferase_side_ec_boundary | 9 |

## Guardrails

- EC 4.1.2/4.1.3 was used only for scope/supply.
- Counted corroborators for any future import should be metal cofactor/site, Lyase/aldolase/domain text, Rhea C-C/oxoacid reaction context, active-/binding-/metal-site evidence, or structure; EC alone cannot admit a row.
- Guard PLP, ThDP, class-I Schiff-base aldolases, hydrolase/transferase/oxidoreductase side rows, and multi-fingerprint signals.
