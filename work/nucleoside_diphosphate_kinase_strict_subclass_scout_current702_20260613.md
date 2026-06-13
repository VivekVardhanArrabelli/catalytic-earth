# Strict Nucleoside Diphosphate Kinase Subclass Scout

Run: 2026-06-13T07:48:29Z

Non-destructive reviewed UniProt scout for a strict EC 2.7.4.6 NDK subclass. EC/Rhea/name text is scope/admission context only; no labels or predictive features were emitted.

- Reviewed supply count: 714.
- Entries examined: 80.
- Fetch failures: 0.
- Wire 28fp lane next: True.

| Handle | Count |
| --- | ---: |
| active_or_binding_site_context | 80 |
| ec_2_7_4_6_scope | 80 |
| likely_wireable_by_non_ec_handles | 80 |
| mg_or_metal_context | 79 |
| ndk_family_text | 80 |
| ntp_ndp_reaction_text | 80 |
| phosphohistidine_or_active_his_context | 80 |
| phosphoryl_transfer_text | 80 |
| rhea_cross_reference_present | 80 |

## Recommendation

- Next action: `wire_guarded_nucleoside_diphosphate_kinase_28fp_lane`.
- Reason: Strict NDK supply remains floor-reachable after excluding side ECs; sampled entries have EC 2.7.4.6, NDK family text, Rhea-backed NTP/NDP phosphoryl-transfer text, active/binding-site context, and no sampled side-EC boundaries.
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
| Q9WV85 | 2.7.4.6 | Nucleoside diphosphate kinase C (NDPK-C) (EC 2.7.4.6) (DR-nm23) (Nucleoside diph | True | - |
| P87355 | 2.7.4.6 | Nucleoside diphosphate kinase D, mitochondrial (NDPK-D) (EC 2.7.4.6) (Nucleoside | True | - |
| P39207 | 2.7.4.6 | Nucleoside diphosphate kinase 1 (EC 2.7.4.6) (Nucleoside diphosphate kinase I) ( | True | - |
| P36010 | 2.7.4.6 | Nucleoside diphosphate kinase (NDK) (NDP kinase) (EC 2.7.4.6) | True | - |
| P22887 | 2.7.4.6 | Nucleoside diphosphate kinase, cytosolic (NDK) (NDP kinase) (EC 2.7.4.6) | True | - |
| P34093 | 2.7.4.6 | Nucleoside diphosphate kinase, mitochondrial (NDK) (NDP kinase) (EC 2.7.4.6) | True | - |
