# Family Panel Source-Free Predicted-Geometry Sidecar Manifest - current702

Run: 2026-06-01T12:48:47Z

Review-only readiness manifest for materializing source-free predicted active-site geometry sidecars for the 10 family-panel rows that already have source-backed AFDB-vs-predicted-atlas Foldseek/TM scores.

## Status

- source_free_predicted_geometry_manifest_blocked_locator_missing_review_only
- Targeted rows: 10
- Rows with AFDB predicted CIFs: 10
- Rows with source-backed fold scores: 10
- Source-free geometry ready rows: 0
- Source-free geometry blocked rows: 10
- Blocker counts: {'approved_source_free_active_site_locator_missing': 10, 'not_current702_label_manifest_row': 10, 'source_backed_sidecar_lacks_residue_locator': 10, 'source_free_predicted_geometry_retrieval_missing': 10}

## Rows

| rank | row | accession | AFDB CIF | fold TM | source-free geometry status | blockers |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | secondary_probe::cobalamin_radical_rearrangement | uniprot:Q59490 | True | 0.4655 | blocked_source_free_active_site_locator_missing | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| 2 | secondary_probe::radical_sam_enzyme | uniprot:A0A1M6T2I7 | True | 0.7039 | blocked_source_free_active_site_locator_missing | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| 3 | external_glycoside_panel | uniprot:Q6NSJ0 | True | 0.6259 | blocked_source_free_active_site_locator_missing | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| 4 | mh_073 | uniprot:P01112 | True | 0.8022 | blocked_source_free_active_site_locator_missing | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| 5 | mh_064 | uniprot:C7C422 | True | 0.9222 | blocked_source_free_active_site_locator_missing | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| 6 | mh_065 | uniprot:Q79MP6 | True | 0.9411 | blocked_source_free_active_site_locator_missing | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| 7 | mh_066 | uniprot:P52699 | True | 0.9445 | blocked_source_free_active_site_locator_missing | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| 8 | mh_067 | uniprot:P00918 | True | 1.004 | blocked_source_free_active_site_locator_missing | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| 9 | mh_068 | uniprot:P15289 | True | 1.002 | blocked_source_free_active_site_locator_missing | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| 10 | mh_072 | uniprot:P0A6P9 | True | 0.5936 | blocked_source_free_active_site_locator_missing | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |

## Blocker-Clearing Attempts

- looked_up_existing_predicted_geometry_by_review_entry_id: 0 targeted review-only rows are present as source-free predicted-geometry rows in the current combined atlas/heldout retrieval artifact.
- checked_current702_label_manifest_membership: All targeted rows are secondary/external family-panel rows, not current702 label-manifest rows with graph-backed residue locators.
- checked_source_backed_sidecars_for_residue_locators: The sidecars are present and fold-scored, but their catalytic or binding site evidence status remains `source_backed_row_context_staged_local_site_not_extracted`.
- checked_coordinate_and_fold_runtime_state: AFDB v6 CIFs and source-backed Foldseek/TM scores are already present for all 10 rows, so the blocker is data semantics for active-site localization rather than runtime or coordinate availability.

## Commands

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-family-panel-source-free-predicted-geometry-sidecar-manifest
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-predicted-structure-fold-channel-contract
```

## Interpretation

- 10/10 rows have source-backed fold scores and AFDB coordinate hashes, but 10 remain blocked for source-free predicted geometry because no approved active-site locator sidecar exists.
- Define and materialize the source-free active-site locator sidecar before refreshing family-panel packets/readout; do not promote rows or use source-backed review prose as scoring input.
