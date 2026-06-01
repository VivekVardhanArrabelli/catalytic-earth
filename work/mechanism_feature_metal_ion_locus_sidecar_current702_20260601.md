# Mechanism-Feature Metal-Ion Locus Sidecar - current702

Review-only current702 row sidecar for the metal-ion cofactor locus, derived only from existing `geometry_features` ligand context. No labels, imports, thresholds, splits, models, coordinates, or production scorers changed.

## Counts

- rows: 702
- status_counts: {'no_metal_context_detected': 422, 'proximal_metal_context_available': 175, 'structure_wide_metal_context_only': 85, 'unsupported_or_missing_geometry': 20}
- proximal_context_rows: 175
- structure_wide_only_rows: 85
- unsupported_or_missing_geometry_rows: 20
- top_proximal_metal_codes: {'MG': 65, 'ZN': 61, 'MN': 20, 'CA': 18, 'CU': 7, 'FE': 7, 'FE2': 6, 'K': 5, 'VO4': 5, 'NA': 5, 'NI': 5, 'FES': 3}
- ready_for_label_import_rows: 0
- predictive_use_allowed_rows: 0

## Status Counts

| Status | Rows |
|---|---:|
| `no_metal_context_detected` | 422 |
| `proximal_metal_context_available` | 175 |
| `structure_wide_metal_context_only` | 85 |
| `unsupported_or_missing_geometry` | 20 |

## Top Proximal Metal Codes

| Code | Rows |
|---|---:|
| `MG` | 65 |
| `ZN` | 61 |
| `MN` | 20 |
| `CA` | 18 |
| `CU` | 7 |
| `FE` | 7 |
| `FE2` | 6 |
| `K` | 5 |
| `VO4` | 5 |
| `NA` | 5 |
| `NI` | 5 |
| `FES` | 3 |

## Interpretation

- The metal-ion locus is now materialized as a review-only current702 row sidecar from existing geometry ligand context.
- A future train/cal-only embedding pilot may consume this sidecar after split filtering; heldout rows remain final evaluation only.
- Add a strict schema audit for this sidecar, then repeat the same pattern for cobalamin_locus with explicit structure-wide-only B12 handling.

## Source Artifacts

| Artifact | SHA256 | Role |
|---|---|---|
| `artifacts/v3_mechanism_feature_inorganic_cofactor_locus_schema_current702_20260601.json` | `0ec97a47135ada1dcecbcbcaf27a24abe54a1fc91b2ae08ef638cfbc0691e974` | schema/materialization queue authorizing review-only metal locus sidecar shape |
| `artifacts/v3_geometry_features_1025.json` | `be7af8462397425062075ff8df5959cc9b68b165d07017692099deb66db1f8f6` | source ligand_context and active-site geometry rows |
| `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json` | `d924a588456d4460c44cd189db5d7ebe4cad6622f802eba163bc4c5f3947d151` | current702 row universe and split assignments |
