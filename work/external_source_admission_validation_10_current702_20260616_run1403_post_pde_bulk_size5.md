# External Source Admission Validation - 10 current702 candidates

Read-only admission validation for 10 reviewed UniProt external import-preview rows. No labels, registries, imports, ontologies, models, thresholds, splits, coordinates, or locator sidecars were edited.

## Summary

- Created UTC: `2026-06-16T14:08:51Z`
- Validated rows: `10`
- Admission-ready rows: `10`
- Direct external label candidates: `0`
- Pending coordinate materialization: `7`
- Pending locator materialization: `3`
- Validation passed: `True`

## Terminal State Counts

| Terminal state | Count |
| --- | ---: |
| `admission_ready_pending_coordinate_materialization` | 7 |
| `admission_ready_pending_locator_materialization` | 3 |

## Family/Lane Counts

| Family/lane | admission_ready_pending_coordinate_materialization | admission_ready_pending_locator_materialization |
| --- | ---: | ---: |
| PLP children | 1 | 0 |
| glycoside/nucleoside | 3 | 0 |
| phosphoryl transfer | 0 | 3 |
| redox oxygen/sulfur | 3 | 0 |

## Admission Matrix

| Candidate | Lane | Terminal state | Exact locators | Coordinate | Local coordinate | Source-free locator | Next action |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| `uniprot:P21912` | redox oxygen/sulfur | `admission_ready_pending_coordinate_materialization` | 14 | 7KCL | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:Q8S7E1` | redox oxygen/sulfur | `admission_ready_pending_coordinate_materialization` | 8 | AF-Q8S7E1-F1 | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:Q9MBA1` | redox oxygen/sulfur | `admission_ready_pending_coordinate_materialization` | 8 | AF-Q9MBA1-F1 | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:Q9Y600` | PLP children | `admission_ready_pending_coordinate_materialization` | 1 | 2JIS | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:P0AF12` | glycoside/nucleoside | `admission_ready_pending_coordinate_materialization` | 4 | 1JYS | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:Q7XA67` | glycoside/nucleoside | `admission_ready_pending_coordinate_materialization` | 6 | 3BSF | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:Q9T0I8` | glycoside/nucleoside | `admission_ready_pending_coordinate_materialization` | 6 | 2H8G | coordinate_provenance_available_local_file_missing | pending_source_free_locator_materialization | materialize or hash-match local PDB/AFDB coordinates, then materialize source-free locator sidecar and rerun admission validation |
| `uniprot:P55263` | phosphoryl transfer | `admission_ready_pending_locator_materialization` | 11 | 1BX4 | local_coordinate_materialized | pending_source_free_locator_materialization | materialize an approved source-free locator sidecar from exact reviewed residue locators against the local coordinate, then rerun |
| `uniprot:P27144` | phosphoryl transfer | `admission_ready_pending_locator_materialization` | 12 | 2AR7 | local_coordinate_materialized | pending_source_free_locator_materialization | materialize an approved source-free locator sidecar from exact reviewed residue locators against the local coordinate, then rerun |
| `uniprot:A2RU49` | phosphoryl transfer | `admission_ready_pending_locator_materialization` | 1 | AF-A2RU49-F1 | local_coordinate_materialized | pending_source_free_locator_materialization | materialize an approved source-free locator sidecar from exact reviewed residue locators against the local coordinate, then rerun |

## Mechanical Findings

- 10 preview rows were reconciled to pilot rows; accepted source preflight states are `external_countable_preflight_candidate`, `provisional_external_countable_preflight_candidate`.
- 10 rows were checked for reviewed Swiss-Prot status, source hashes/provenance, exact residue locators, PDB/AFDB handles, Rhea/specific EC provenance, and recomputed exact current702 accession or sequence conflicts.
- 3 rows have a matching local coordinate file in existing artifacts and remain pending source-free locator materialization.
- 7 rows have coordinate provenance but no matching local CIF in the current artifact cache, so they are pending coordinate materialization before locator sidecar materialization.
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
- `pilot_file_sha256`: `616b4f12292975422f48e75f136777a0a5e1757ecbe32def3a4d5c20fdbcf5e3`
- `import_preview_file_sha256`: `ff590ec343ebb1a4af5c99337dab77b1ad9e2a04cf9a83e93399520fde7d2cec`
- `preview_declared_pilot_file_sha256_matches`: `True`
- `pilot_artifact_id`: `v3_external_bulk_ingestion_scout_current702_20260608`
- `import_preview_artifact_id`: `v3_external_bulk_ingestion_provisional_import_preview_current702_20260608`
