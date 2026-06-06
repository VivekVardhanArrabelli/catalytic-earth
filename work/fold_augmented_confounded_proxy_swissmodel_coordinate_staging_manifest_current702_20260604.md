# Fold-Augmented Confounded Proxy SWISS-MODEL Coordinate Staging Manifest - current702

Run: 2026-06-04T10:12:34Z

Review-only Lever 3 staging manifest for non-AFDB predicted coordinates from the SWISS-MODEL Repository. It accepts only provider=SWISSMODEL, method=HOMOLOGY MODELLING coordinate records as predicted-structure inputs, rejects provider=PDB experimental mappings, records provider/model/version/path/checksum provenance, scores no rows, and does not change threshold 0.44155.

## Status

- fold_augmented_confounded_proxy_swissmodel_coordinate_staging_manifest_partial_3_of_4
- Staged predicted coordinate rows: 3
- PDB-provider-only rows rejected: 1
- Remaining coordinate-source blockers: 1
- Blockers: ['p07658_has_only_experimental_pdb_repository_mappings', 'q43088_locator_or_geometry_sidecar_still_missing', 'fixed_threshold_audit_not_ready_to_rerun']

## Rows

| row | accession | status | provider | template | coverage | path |
| --- | --- | --- | --- | --- | ---: | --- |
| m_csa:416 | P07071 | swissmodel_predicted_coordinate_staged_review_only | SWISSMODEL | 9d3x.1.A | 0.992 | artifacts/v3_fold_augmented_swissmodel_coordinates_current702_20260604/SWISSMODEL_P07071_9d3x_1_A_range_6_605.pdb |
| m_csa:562 | P07658 | swissmodel_repository_pdb_only_disallowed | none | none | none | none |
| m_csa:586 | P00806 | swissmodel_predicted_coordinate_staged_review_only | SWISSMODEL | 1lba.1.A | 0.96 | artifacts/v3_fold_augmented_swissmodel_coordinates_current702_20260604/SWISSMODEL_P00806_1lba_1_A_range_7_151.pdb |
| m_csa:637 | P04531 | swissmodel_predicted_coordinate_staged_review_only | SWISSMODEL | 1del.1.A | 1.0 | artifacts/v3_fold_augmented_swissmodel_coordinates_current702_20260604/SWISSMODEL_P04531_1del_1_A_range_1_241.pdb |

## Decision

- Coordinate-source surface fully clear now: False
- Partial coordinate-source clearance rows: 3
- Remaining coordinate-source blockers: 1
- Fixed-threshold audit ready to rerun now: False
- Apply or change threshold now: False
- Next gate: Keep P07071, P00806, and P04531 staged as review-only SWISS-MODEL predicted-coordinate inputs. Do not use P07658 provider=PDB repository mappings; obtain a true predicted coordinate for P07658, and clear Q43088 locator evidence before any fixed-threshold audit rerun.

## Interpretation

- The non-AFDB coordinate blocker is partially clearable with current source-free predicted-structure evidence: three rows have staged SWISS-MODEL homology models, while P07658 remains blocked because the repository exposes only experimental PDB mappings for that accession.
- Run the smallest next coordinate experiment for P07658: obtain or generate a deployment-valid predicted structure with provider/model/version/path/checksum provenance. In parallel, continue the Q43088 source-free locator review.
