# Family Panel Source-Free Predicted-Geometry Retrieval - current702

Run: 2026-06-02T19:15:47Z

Review-only predicted active-site geometry retrieval for family-panel rows with approved source-free locator sidecars. The scorer uses only residue sequence positions/codes, generic source-free locator role hints, local AlphaFoldDB coordinates, and geometry-derived pocket/ligand context.

## Status

- source_free_predicted_geometry_retrieval_scored_review_only
- Manifest target rows: 10
- Ready-to-score rows: 5
- Retrieval rows emitted: 5
- Predicted-geometry ok rows: 5
- Fixed-threshold retained/abstained: 5 / 0

## Row Scores

| rank | row | top1 fingerprint | geometry score | fold TM | combined mean | fixed-threshold status |
| ---: | --- | --- | ---: | ---: | ---: | --- |
| 2 | secondary_probe::radical_sam_enzyme | metal_dependent_hydrolase | 0.2628 | 0.7039 | 0.4833 | retained |
| 4 | mh_073 | ser_his_acid_hydrolase | 0.1733 | 0.8022 | 0.4878 | retained |
| 7 | mh_066 | metal_dependent_hydrolase | 0.3822 | 0.9445 | 0.6633 | retained |
| 8 | mh_067 | metal_dependent_hydrolase | 0.3755 | 1.004 | 0.6897 | retained |
| 9 | mh_068 | metal_dependent_hydrolase | 0.3786 | 1.002 | 0.6903 | retained |

## Blocked Rows Carried

- secondary_probe::cobalamin_radical_rearrangement: approved_source_free_active_site_locator_missing, source_backed_sidecar_lacks_residue_locator
- external_glycoside_panel: approved_source_free_active_site_locator_missing, source_backed_sidecar_lacks_residue_locator
- mh_064: approved_source_free_active_site_locator_missing, source_backed_sidecar_lacks_residue_locator
- mh_065: approved_source_free_active_site_locator_missing, source_backed_sidecar_lacks_residue_locator
- mh_072: approved_source_free_active_site_locator_missing, source_backed_sidecar_lacks_residue_locator

## Interpretation

- 5/5 ready rows now have source-free predicted-geometry retrieval scores.
- 5/5 scored rows are retained by the existing combined_mean_geometry_fold research threshold.
- Refresh the review-only family-panel readout to consume these source-free predicted-geometry scores, while keeping all rows non-importable and outside threshold selection.

## Guardrails

- Review-only. No labels, registries, ontologies, imports, thresholds, training data, production scoring, source fetching, or coordinate downloads changed.
