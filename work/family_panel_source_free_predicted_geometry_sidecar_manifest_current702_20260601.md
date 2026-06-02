# Family Panel Source-Free Predicted-Geometry Sidecar Manifest - current702

Run: 2026-06-02T19:15:46Z

Review-only readiness manifest for materializing source-free predicted active-site geometry sidecars for the 10 family-panel rows that already have source-backed AFDB-vs-predicted-atlas Foldseek/TM scores.

## Status

- source_free_predicted_geometry_manifest_partially_ready_to_score_review_only
- Targeted rows: 10
- Rows with AFDB predicted CIFs: 10
- Rows with source-backed fold scores: 10
- Rows with approved source-free active-site locator: 5
- Source-free geometry ready rows: 5
- Source-free geometry blocked rows: 5
- Blocker counts: {'approved_source_free_active_site_locator_missing': 5, 'source_backed_sidecar_lacks_residue_locator': 5}

## Rows

| rank | row | accession | AFDB CIF | fold TM | source-free geometry status | blockers |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | secondary_probe::cobalamin_radical_rearrangement | uniprot:Q59490 | True | 0.4655 | blocked_source_free_geometry_preconditions | approved_source_free_active_site_locator_missing, source_backed_sidecar_lacks_residue_locator |
| 2 | secondary_probe::radical_sam_enzyme | uniprot:A0A1M6T2I7 | True | 0.7039 | ready_to_score_source_free_predicted_geometry |  |
| 3 | external_glycoside_panel | uniprot:Q6NSJ0 | True | 0.6259 | blocked_source_free_geometry_preconditions | approved_source_free_active_site_locator_missing, source_backed_sidecar_lacks_residue_locator |
| 4 | mh_073 | uniprot:P01112 | True | 0.8022 | ready_to_score_source_free_predicted_geometry |  |
| 5 | mh_064 | uniprot:C7C422 | True | 0.9222 | blocked_source_free_geometry_preconditions | approved_source_free_active_site_locator_missing, source_backed_sidecar_lacks_residue_locator |
| 6 | mh_065 | uniprot:Q79MP6 | True | 0.9411 | blocked_source_free_geometry_preconditions | approved_source_free_active_site_locator_missing, source_backed_sidecar_lacks_residue_locator |
| 7 | mh_066 | uniprot:P52699 | True | 0.9445 | ready_to_score_source_free_predicted_geometry |  |
| 8 | mh_067 | uniprot:P00918 | True | 1.004 | ready_to_score_source_free_predicted_geometry |  |
| 9 | mh_068 | uniprot:P15289 | True | 1.002 | ready_to_score_source_free_predicted_geometry |  |
| 10 | mh_072 | uniprot:P0A6P9 | True | 0.5936 | blocked_source_free_geometry_preconditions | approved_source_free_active_site_locator_missing, source_backed_sidecar_lacks_residue_locator |

## Blocker-Clearing Attempts

- looked_up_existing_predicted_geometry_by_review_entry_id: 0 targeted review-only rows are present as source-free predicted-geometry rows in the current combined atlas/heldout retrieval artifact.
- checked_current702_label_manifest_membership: Targeted rows may be secondary/external family-panel rows; this is recorded for provenance but is no longer a blocker once an approved source-free active-site locator is present.
- checked_source_backed_sidecars_and_approved_locator_audit: Source-backed sidecars remain review-context only; approved source-free locator sidecars from the schema audit are the only mechanism allowed to clear active-site localization.
- checked_coordinate_and_fold_runtime_state: AFDB v6 CIFs and source-backed Foldseek/TM scores are already present for all 10 rows, so the blocker is data semantics for active-site localization rather than runtime or coordinate availability.

## Commands

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-family-panel-source-free-predicted-geometry-sidecar-manifest
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-predicted-structure-fold-channel-contract
```

## Interpretation

- 10/10 rows have source-backed fold scores and AFDB coordinate hashes; 5 now have approved source-free active-site locators and 5 remain blocked before predicted-geometry scoring.
- Run predicted-geometry retrieval only for ready rows using the approved locator sidecars; do not promote rows or use source-backed review prose as scoring input.
