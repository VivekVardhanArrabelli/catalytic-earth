# Mechanism-Feature Inorganic Cofactor Locus Schema - current702

Review-only schema and materialization queue for the cofactor_catalytic_locus gap left after the organic flavin/heme/PLP sidecar schema pass. No labels, imports, thresholds, splits, models, or coordinates changed.

## Counts

- current702_manifest_rows: 702
- geometry_feature_rows_in_current702: 698
- geometry_status_counts: {'insufficient_resolved_residues': 14, 'no_structure_positions': 2, 'ok': 682}
- organic_cofactor_row_class_records: 2106
- organic_cofactor_classes_schema_passed: ['flavin', 'heme', 'plp']
- active_site_role_graph_ok_rows: 656
- proximal_context_counts: {'metal_ion': 176, 'cobalamin': 4, 'sam': 8, 'fe_s_cluster': 17}
- structure_wide_context_counts: {'metal_ion': 264, 'cobalamin': 4, 'sam': 11, 'fe_s_cluster': 29}
- schema_classes: 4

## Schema Classes

| Class | Current rows with context | Required policy |
|---|---:|---|
| `metal_ion_locus` | 264 | Use geometry ligand_context first; require distance and ligand-code provenance before any train/cal feature use. |
| `cobalamin_locus` | 4 | Separate proximal B12 evidence from structure-wide B12 context; structure-wide only must not count as local catalytic evidence. |
| `radical_sam_locus` | 39 | Require SAM plus Fe-S co-context for strong radical-SAM locus; partial evidence remains a separate weak/blocked status. |
| `iron_sulfur_locus` | 29 | Keep Fe-S as a locus feature separate from radical-SAM class membership; source role must be explicit before train/cal use. |

## Materialization Queue

| Rank | Work item | Blocker | Next action |
|---:|---|---|---|
| 1 | `derive_metal_ion_locus_sidecar_from_geometry_ligand_context` | needs row-level schema implementation plus distance/provenance extraction | Create review-only sidecar records for current702 rows with metal_ion ligand_context, marking proximal versus structure-wide-only status. |
| 2 | `derive_cobalamin_locus_sidecar_with_structure_wide_only_guardrail` | needs explicit proximal-vs-structure-wide B12 evidence policy | Materialize cobalamin rows with a structure_wide_only flag before any cobalamin/radical feature pilot. |
| 3 | `derive_radical_sam_and_fe_s_locus_sidecars` | needs SAM and Fe-S co-context separation plus source-role policy | Materialize SAM and Fe-S context records separately, then add a copresence status for radical-SAM candidate rows. |

## Interpretation

- Organic flavin/heme/PLP cofactor score sidecars pass strict schema, but inorganic/cobalamin/radical loci are only available as raw geometry ligand context today.
- The mechanism-feature embedding pilot can use role graph and reaction-center templates, but cofactor_catalytic_locus should stay incomplete until these four sidecar classes are materialized or marked absent per row.
- Implement a review-only metal_ion_locus sidecar first because it has the largest current702 surface and can be validated directly from geometry_features ligand_context without new downloads.

## Source Artifacts

| Artifact | SHA256 | Role |
|---|---|---|
| `artifacts/v3_learned_mechanism_feature_embedding_plan_current702_20260601.json` | `b24c77243f2eb22d762c7f5cf80ab7923f4fce2650f0ff2c526e211c1121d7a5` | embedding scaffold gap that names metal/cobalamin/radical/Fe-S loci |
| `artifacts/v3_mechanism_feature_sidecar_schema_audit_current702_20260601.json` | `8c18e359045fd5ce84ab4415063cd10a8eed83d8e9f641d06c63b966c88e589b` | current role-graph and reaction-center schema pass |
| `artifacts/v3_selected_organic_cofactor_sidecar_schema_audit_current702_20260601.json` | `26f67fa0d9b4ace5bccfee20b66f006e57e12cbdb440e28ca3788388642beb0c` | strict schema pass for flavin/heme/PLP organic cofactor score sidecars |
| `artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json` | `840d572b92cf61c1d1038e777bb432f8efa1ce29e8c21090f84442f48701e61a` | current organic cofactor row-class records |
| `artifacts/v3_geometry_features_1025.json` | `be7af8462397425062075ff8df5959cc9b68b165d07017692099deb66db1f8f6` | local ligand/cofactor context for current702 rows |
| `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json` | `d924a588456d4460c44cd189db5d7ebe4cad6622f802eba163bc4c5f3947d151` | current702 row universe and split assignments |
