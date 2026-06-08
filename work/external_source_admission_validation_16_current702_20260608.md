# External Source Admission Validation - 16 current702 candidates

Read-only admission validation for the first 16 reviewed UniProt external import-preview rows. No labels, registries, imports, ontologies, models, thresholds, splits, coordinates, or locator sidecars were edited.

## Summary

- Created UTC: `2026-06-08T23:47:35Z`
- Validated rows: `16`
- Admission-ready rows: `16`
- Direct external label candidates: `0`
- Pending coordinate materialization: `10`
- Pending locator materialization: `6`
- Validation passed: `True`

## Terminal State Counts

| Terminal state | Count |
| --- | ---: |
| `admission_ready_pending_coordinate_materialization` | 10 |
| `admission_ready_pending_locator_materialization` | 6 |

## Family/Lane Counts

| Family/lane | admission_ready_pending_coordinate_materialization | admission_ready_pending_locator_materialization |
| --- | ---: | ---: |
| PLP children | 0 | 3 |
| glycoside/nucleoside | 1 | 1 |
| phosphoryl transfer | 2 | 2 |
| radical-SAM/cobalamin | 3 | 0 |
| redox oxygen/sulfur | 4 | 0 |

## Admission Matrix

| Candidate | Lane | Terminal state | Exact locators | Coordinate | Local coordinate | Source-free locator | Next action |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| `uniprot:P09601` | redox oxygen/sulfur | `admission_ready_pending_coordinate_materialization` | 6 | 1N3U | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:P30519` | redox oxygen/sulfur | `admission_ready_pending_coordinate_materialization` | 9 | 2Q32 | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:P29082` | redox oxygen/sulfur | `admission_ready_pending_coordinate_materialization` | 4 | 2CB2 | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:Q9UGB7` | redox oxygen/sulfur | `admission_ready_pending_coordinate_materialization` | 9 | 2IBN | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:Q9Y617` | PLP children | `admission_ready_pending_locator_materialization` | 23 | 3E77 | local_coordinate_materialized | pending_source_free_locator_materialization | materialize an approved source-free locator sidecar from exact reviewed residue locators against the local coordinate, then rerun |
| `uniprot:P04181` | PLP children | `admission_ready_pending_locator_materialization` | 13 | 1GBN | local_coordinate_materialized | pending_source_free_locator_materialization | materialize an approved source-free locator sidecar from exact reviewed residue locators against the local coordinate, then rerun |
| `uniprot:Q96255` | PLP children | `admission_ready_pending_locator_materialization` | 7 | 6CZX | local_coordinate_materialized | pending_source_free_locator_materialization | materialize an approved source-free locator sidecar from exact reviewed residue locators against the local coordinate, then rerun |
| `uniprot:O60502` | glycoside/nucleoside | `admission_ready_pending_coordinate_materialization` | 9 | 2YDQ | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:P04062` | glycoside/nucleoside | `admission_ready_pending_locator_materialization` | 2 | 1OGS | local_coordinate_materialized | pending_source_free_locator_materialization | materialize an approved source-free locator sidecar from exact reviewed residue locators against the local coordinate, then rerun |
| `uniprot:Q3T906` | phosphoryl transfer | `admission_ready_pending_coordinate_materialization` | 10 | 2N6D | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:Q969G6` | phosphoryl transfer | `admission_ready_pending_locator_materialization` | 13 | 1NB0 | local_coordinate_materialized | pending_source_free_locator_materialization | materialize an approved source-free locator sidecar from exact reviewed residue locators against the local coordinate, then rerun |
| `uniprot:P32189` | phosphoryl transfer | `admission_ready_pending_locator_materialization` | 23 | AF-P32189-F1 | local_coordinate_materialized | pending_source_free_locator_materialization | materialize an approved source-free locator sidecar from exact reviewed residue locators against the local coordinate, then rerun |
| `uniprot:Q9Y6K0` | phosphoryl transfer | `admission_ready_pending_coordinate_materialization` | 9 | 8GYW | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:Q99707` | radical-SAM/cobalamin | `admission_ready_pending_coordinate_materialization` | 17 | 2O2K | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:A6H5Y3` | radical-SAM/cobalamin | `admission_ready_pending_coordinate_materialization` | 17 | AF-A6H5Y3-F1 | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:Q9Z2Q4` | radical-SAM/cobalamin | `admission_ready_pending_coordinate_materialization` | 17 | AF-Q9Z2Q4-F1 | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |

## Mechanical Findings

- All 16 preview rows reconcile exactly to pilot rows in `external_countable_preflight_candidate` state.
- All 16 rows have reviewed Swiss-Prot status, source hashes/provenance, exact residue locators, PDB/AFDB handles, Rhea/specific EC provenance, and no recomputed exact current702 accession or sequence conflict.
- 6 rows have a matching local coordinate file in existing artifacts and remain pending source-free locator materialization.
- 10 rows have coordinate provenance but no matching local CIF in the current artifact cache, so they are pending coordinate materialization before locator sidecar materialization.
- No direct production/import-ready label candidate is emitted; the ready preview is an admission/materialization queue only.

## Validation

- `passed`: `True`
- `violation_count`: `0`
- `json_inputs_parsed`: `True`
- `preview_candidate_count_matches_expected`: `True`
- `preview_row_count_matches_expected`: `True`
- `preview_rows_reconciled_to_pilot`: `True`
- `preview_rows_match_pilot_preflight_state`: `True`
- `all_terminal_states_known`: `True`
- `all_rows_have_required_fields`: `True`
- `all_rows_have_source_hashes_and_provenance`: `True`
- `all_rows_have_duplicate_status`: `True`
- `all_duplicate_statuses_recomputed_match_artifact`: `True`
- `pilot_file_sha256`: `d224e15dca0c0f56237510ae1be70b07ab28170dbb088422c2868cb3799e269d`
- `import_preview_file_sha256`: `237759dda87fe16872d5db974911180796ef8d1cea085a9bd0ad888322b9bb87`
- `preview_declared_pilot_file_sha256_matches`: `True`
- `pilot_artifact_id`: `v3_external_source_ingestion_pilot_current702_20260608`
- `import_preview_artifact_id`: `v3_external_source_ingestion_import_preview_current702_20260608`
