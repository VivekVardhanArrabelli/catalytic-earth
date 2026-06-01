# Mechanism-Feature Inorganic Cofactor Locus Completion Audit - current702

Run: 2026-06-01T11:13:09Z

Review-only completion audit for the metal, cobalamin, radical-SAM, and Fe-S cofactor_catalytic_locus sidecars named by the current702 inorganic locus schema.

## Status

- inorganic_cofactor_locus_completion_audit_passed_review_only
- Schema classes: 4
- Materialized sidecar classes: 4
- Schema-audit passed classes: 4
- Critical violations: 0
- Predictive-use rows: 0
- Import-ready rows: 0

## Classes

| class | sidecar status | audit status | rows | proximal | structure-wide only | critical violations |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| metal_ion_locus | metal_ion_locus_sidecar_ready_review_only | metal_ion_locus_sidecar_schema_passed_current702 | 702 | 175 | 85 | 0 |
| cobalamin_locus | cobalamin_locus_sidecar_ready_review_only | cobalamin_locus_sidecar_schema_passed_current702 | 702 | 4 | 0 | 0 |
| radical_sam_locus | radical_sam_locus_sidecar_ready_review_only | radical_sam_locus_sidecar_schema_passed_current702 | 702 | 8 | 2 | 0 |
| iron_sulfur_locus | iron_sulfur_locus_sidecar_ready_review_only | iron_sulfur_locus_sidecar_schema_passed_current702 | 702 | 17 | 11 | 0 |

## Interpretation

- All four schema-named inorganic/cobalamin/radical/Fe-S locus sidecar classes are materialized for 702 current rows and pass their schema audits with zero critical violations.
- cofactor_catalytic_locus is no longer blocked on row-level sidecar materialization, but remains review-only until a train/cal-only feature pilot is explicitly staged.
- Stage a train/cal-only mechanism-feature embedding pilot that consumes these sidecars without label/import changes or heldout leakage.
