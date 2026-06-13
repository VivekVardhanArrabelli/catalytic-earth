# Nucleoside Diphosphate Kinase Subclass Scout

Run: 2026-06-13T07:46:17Z

Non-destructive reviewed UniProt scout for a narrow EC 2.7 kinase subclass. EC/Rhea/name text is scope/admission context only; no labels or predictive features were emitted.

- Reviewed supply count: 751.
- Entries examined: 80.
- Fetch failures: 0.
- Wire 28fp lane next: False.

| Handle | Count |
| --- | ---: |
| active_or_binding_site_context | 80 |
| ec_2_7_4_6_scope | 80 |
| hydrolase_or_nuclease_side_ec_boundary | 4 |
| likely_wireable_by_non_ec_handles | 46 |
| mg_or_metal_context | 78 |
| ndk_family_text | 80 |
| non_2_7_side_ec_boundary | 4 |
| ntp_ndp_reaction_text | 80 |
| other_nmp_kinase_side_ec_boundary | 14 |
| phosphohistidine_or_active_his_context | 70 |
| phosphoryl_transfer_text | 80 |
| protein_kinase_boundary | 24 |
| rhea_cross_reference_present | 80 |
| two_component_histidine_kinase_boundary | 24 |

## Recommendation

- Next action: `do_not_wire_until_boundary_split_is_cleaner`.
- Reason: Boundary rates or mechanism handles are not clean enough for a new fingerprint.
- Required guards: hold protein kinase EC 2.7.11 side rows; hold two-component histidine kinase EC 2.7.13 side rows; hold hydrolase/nuclease EC 3.* side rows; hold adenylate/guanylate/nucleoside-monophosphate kinase side EC rows; hold multi-fingerprint signals rather than forcing subclass assignment.

## Sample

| Accession | EC | Protein | Likely | Boundary flags |
| --- | --- | --- | --- | --- |
| O00746 | 2.7.4.6 | Nucleoside diphosphate kinase D, mitochondrial (NDPK-D) (EC 2.7.4.6) (Nucleoside | True | - |
| Q9PTF3 | 2.7.4.6 | Nucleoside diphosphate kinase C (NDPK-C) (EC 2.7.4.6) (NM23 nucleoside diphospha | True | - |
| Q13232 | 2.7.4.6 | Nucleoside diphosphate kinase C (NDPK-C) (EC 2.7.4.6) (DR-nm23) (Nucleoside diph | True | - |
| Q66KP0 | 2.7.4.6 | Nucleoside diphosphate kinase C-B (EC 2.7.4.6) (Nucleoside diphosphate kinase 3- | True | - |
| A2VD68 | 2.7.4.6 | Nucleoside diphosphate kinase C-A (EC 2.7.4.6) (Nucleoside diphosphate kinase 3- | True | - |
| Q9WV84 | 2.7.4.6 | Nucleoside diphosphate kinase D, mitochondrial (NDPK-D) (EC 2.7.4.6) (Nucleoside | True | - |
| Q5EBM0 | 2.7.4.14, 2.7.4.6 | UMP-CMP kinase 2, mitochondrial (EC 2.7.4.14) (Nucleoside-diphosphate kinase) (E | False | other_nmp_kinase_side_ec_boundary |
| Q9WV85 | 2.7.4.6 | Nucleoside diphosphate kinase C (NDPK-C) (EC 2.7.4.6) (DR-nm23) (Nucleoside diph | True | - |
| P87355 | 2.7.4.6 | Nucleoside diphosphate kinase D, mitochondrial (NDPK-D) (EC 2.7.4.6) (Nucleoside | True | - |
| P39207 | 2.7.4.6 | Nucleoside diphosphate kinase 1 (EC 2.7.4.6) (Nucleoside diphosphate kinase I) ( | True | - |
| P36010 | 2.7.4.6 | Nucleoside diphosphate kinase (NDK) (NDP kinase) (EC 2.7.4.6) | True | - |
| P22887 | 2.7.4.6 | Nucleoside diphosphate kinase, cytosolic (NDK) (NDP kinase) (EC 2.7.4.6) | True | - |
