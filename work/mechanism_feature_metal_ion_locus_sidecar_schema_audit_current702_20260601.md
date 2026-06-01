# Mechanism-Feature Metal-Ion Locus Sidecar Schema Audit - current702

Strict review-only schema audit for the current702 `metal_ion_locus` sidecar.

Status: `metal_ion_locus_sidecar_schema_passed_current702`

## Critical Counts

- duplicate_entry_rows: 0
- missing_manifest_rows: 0
- extra_rows: 0
- required_key_violations: 0
- status_violations: 0
- split_mismatches: 0
- predictive_or_import_flag_violations: 0
- distance_range_violations: 0
- proximal_consistency_violations: 0

## Status Counts

| Status | Rows |
|---|---:|
| `no_metal_context_detected` | 422 |
| `proximal_metal_context_available` | 175 |
| `structure_wide_metal_context_only` | 85 |
| `unsupported_or_missing_geometry` | 20 |

## Interpretation

- The metal-ion locus sidecar is row-aligned with current702 and passes strict review-only schema checks.
- Repeat the schema-plus-sidecar pattern for cobalamin_locus, with explicit structure-wide-only B12 handling.

## Source Artifacts

| Artifact | SHA256 |
|---|---|
| `artifacts/v3_mechanism_feature_metal_ion_locus_sidecar_current702_20260601.json` | `341746d27757caad0ba72cf9fb683f1ee9cd91bc9c031e67fdde8c098f966672` |
| `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json` | `d924a588456d4460c44cd189db5d7ebe4cad6622f802eba163bc4c5f3947d151` |
| `artifacts/v3_mechanism_feature_inorganic_cofactor_locus_schema_current702_20260601.json` | `0ec97a47135ada1dcecbcbcaf27a24abe54a1fc91b2ae08ef638cfbc0691e974` |
