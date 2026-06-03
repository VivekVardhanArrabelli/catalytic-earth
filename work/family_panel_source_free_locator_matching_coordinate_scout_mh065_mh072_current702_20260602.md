# Source-Free Locator Matching-Coordinate Scout: mh_065/mh_072 - current702

Run: 2026-06-02T23:10:49Z

Local-cache-only scout for the mh_065/mh_072 matching-coordinate decision class. It searches already-frozen coordinates for exact source-accession struct_ref mappings and records whether any can replace the representative-coordinate locator path.

## Status

- source_free_locator_matching_coordinate_scout_blocked_no_replacement_matches_review_only
- Local coordinate files scanned: 712
- Rows with matching replacement coordinate: 0
- Same-accession struct_ref coordinates: 2
- Rows with same-accession AFDB coordinate only: 2
- Ready for predicted-geometry scoring: 0

## Row Scouts

| row | accession | selected PDB | selected struct_ref | replacement matches | AFDB matches | decision |
| --- | --- | --- | --- | ---: | ---: | --- |
| mh_065 | uniprot:Q79MP6 | 1DDK | Q932P5 | 0 | 1 | only_requested_afdb_coordinate_present_prior_residue_mismatch |
| mh_072 | uniprot:P0A6P9 | 1E9I | P08324 | 0 | 1 | only_requested_afdb_coordinate_present_prior_residue_mismatch |

## Guardrails

- Local-cache-only scout; no coordinates or source data were fetched.
- No locator sidecars were copied, created, or marked scoring-ready.
- No labels, registries, ontologies, imports, thresholds, training data, or model weights changed.

## Interpretation

- For mh_065/mh_072, matching non-AFDB replacement coordinates are absent. Same-accession AFDB files exist but already failed the prior residue-position transfer, so do not copy the raw 1DDK/1E9I locators; provide matching frozen PDB/mmCIF coordinates or explicit remapped-locator approval.
