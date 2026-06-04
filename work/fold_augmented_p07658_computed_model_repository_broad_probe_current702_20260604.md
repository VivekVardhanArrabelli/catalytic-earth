# Fold-Augmented P07658 Computed-Model Repository Broad Probe - current702

Run: 2026-06-04T11:17:06Z

Review-only broad public computed-model repository probe for the remaining P07658 Lever 3 coordinate blocker after Q43088 locator approval. It checks whether RCSB exposes any computational polymer entity for the exact UniProt accession and records ModelArchive web-search endpoint behavior. It stages no coordinates, scores no rows, and does not change threshold 0.44155.

## Status

- fold_augmented_p07658_computed_model_repository_broad_probe_blocked_no_public_computed_model
- RCSB computed model rows: 0
- Direct computed-model coordinate hits: 0
- Direct computed-model endpoint 404 rows: 4
- RCSB experimental control rows: 5
- Deployment-valid predicted coordinate rows ready now: 0
- Blockers: ['public_computed_model_repository_no_p07658_hit', 'p07658_full_length_predicted_coordinate_missing', 'sixteen_row_high_cofactor_train_cal_probe_not_acquired', 'fixed_threshold_audit_not_ready_to_rerun']

## Repository Probes

| probe | status | result count | deployment-valid predicted rows | result |
| --- | ---: | ---: | ---: | --- |
| rcsb_search_computed_models_by_uniprot_accession | 204 | 0 | 0 | no_content_no_computed_model_hits |
| rcsb_search_experimental_control_by_uniprot_accession | 200 | 5 | 0 | experimental content type is a control only; these rows are not predicted-structure inputs |
| modelarchive_web_search_endpoint_smoke | 200 | 0 | 0 | web_app_shell_returned_no_coordinate_record_for_staging |
| rcsb_modelserver_af_underscore_id_direct_cif | 404 | 0 | 0 | direct_computed_model_coordinate_endpoint_not_found |
| rcsb_modelserver_af_hyphen_id_direct_cif | 404 | 0 | 0 | direct_computed_model_coordinate_endpoint_not_found |
| alphafold_db_v6_direct_cif | 404 | 0 | 0 | direct_computed_model_coordinate_endpoint_not_found |
| alphafold_db_v5_direct_cif | 404 | 0 | 0 | direct_computed_model_coordinate_endpoint_not_found |

## Decision

- Broad public repository probe clears P07658 now: False
- Fixed-threshold audit ready to rerun now: False
- Apply or change threshold now: False
- Smallest next experiment: Provision or run an approved full-length predictor/provider that supports the exact 715-residue P07658 sequence including selenocysteine; stage provider/model/version/path/checksum provenance after a coordinate is actually returned.

## Interpretation

- A broader public repository check still cannot clear P07658: RCSB has no computational model hit for the accession, direct RCSB ModelServer/AlphaFold-style coordinate URLs return 404, and the experimental control returns the same five non-deployment-valid PDB entities.
- The smallest concrete next experiment is no longer another public-repository search; it is a credentialed or local full-length predictor run with exact-sequence provenance.
