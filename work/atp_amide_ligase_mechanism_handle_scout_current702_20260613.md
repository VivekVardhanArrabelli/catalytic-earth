# ATP amide ligase mechanism-handle scout

Run: 2026-06-13T04:01:39Z

Non-destructive reviewed Swiss-Prot scout over EC 6.3 + Ligase candidates. EC is scope-only; no labels or predictive features were emitted.

- Entries examined: 80.
- Fetch failures: 0.
- Wire 23fp lane now: False.

| Handle | Count |
| --- | ---: |
| active_or_binding_site_context | 73 |
| amide_or_c_n_ligation_text | 62 |
| atp_grasp_text | 1 |
| biotin_or_carboxylase_boundary | 30 |
| hydrolase_side_ec_boundary | 7 |
| ligase_text_or_keyword | 80 |
| likely_wireable_by_non_ec_handles | 42 |
| mg_context | 54 |
| non_6_3_side_ec_boundary | 16 |
| rhea_adp_or_phosphate | 78 |
| rhea_cross_reference_present | 78 |
| rhea_or_feature_atp | 75 |
| transferase_side_ec_boundary | 9 |

## Guardrails

- EC 6.3 was used only for scope/supply.
- Counted corroborators for any future import must be ATP/Mg or ATP/ADP/phosphate Rhea participants, Ligase/ATP-grasp/domain text, active-/binding-site evidence, or structure/deferred promotion handles; EC alone cannot admit a row.
- Guard kinase/phosphotransferase, biotin carboxylase, generic ATP-transferase, hydrolase side rows, and multi-fingerprint signals.

## Narrowed Non-Biotin Follow-Up

Run: 2026-06-13T04:03:30Z

- Entries examined: 80.
- Fetch failures: 0.
- Wire 23fp lane now: True.

| Handle | Count |
| --- | ---: |
| active_or_binding_site_context | 69 |
| amide_or_c_n_ligation_text | 63 |
| atp_grasp_text | 1 |
| hydrolase_side_ec_boundary | 2 |
| ligase_text_or_keyword | 80 |
| likely_wireable_by_non_ec_handles | 68 |
| mg_context | 53 |
| non_6_3_side_ec_boundary | 10 |
| rhea_adp_or_phosphate | 78 |
| rhea_cross_reference_present | 78 |
| rhea_or_feature_atp | 78 |
| transferase_side_ec_boundary | 5 |
