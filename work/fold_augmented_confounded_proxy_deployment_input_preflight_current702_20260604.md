# Fold-Augmented Confounded Proxy Deployment Input Preflight - current702

Run: 2026-06-04T09:13:34Z

Deployment-input preflight for the four residual Lever 3 AFDB-unavailable coordinate-source blockers. It checks whether repo-local CIFs can satisfy the alternate predicted-structure source contract, explicitly rejects experimental-coordinate shortcuts, downloads no files, stages no coordinates, scores no rows, and does not change threshold 0.44155.

## Status

- fold_augmented_confounded_proxy_deployment_input_preflight_blocked_no_approved_predicted_coordinates
- Affected rows: 4
- Approved predicted coordinate hits: 0
- Disallowed experimental coordinate hits: 3
- Rows with no local coordinate hit: 1
- Deployment-valid rows ready now: 0
- Blockers: ['no_approved_predicted_coordinate_hits_for_residual_rows', 'experimental_pdb_coordinate_shortcuts_disallowed_for_deployment', 'provider_model_version_path_checksum_provenance_missing', 'fixed_threshold_audit_not_ready_to_rerun']

## Rows

| row | accession | local status | predicted hits | disallowed hits |
| --- | --- | --- | --- | --- |
| m_csa:416 | P07071 | no_local_coordinate_hit_observed | none | none |
| m_csa:562 | P07658 | experimental_only_disallowed_for_deployment | none | artifacts/v3_foldseek_coordinates_1000/pdb_1AA6.cif |
| m_csa:586 | P00806 | experimental_only_disallowed_for_deployment | none | artifacts/v3_foldseek_coordinates_1000/pdb_1LBA.cif |
| m_csa:637 | P04531 | experimental_only_disallowed_for_deployment | none | artifacts/v3_foldseek_coordinates_1000/pdb_1DEK.cif |

## Source Requirements

- provider
- model_name_or_id
- model_version
- coordinate_path
- checksum_sha256
- accession_or_isoform_mapping_review
- source_free_evidence_contract

## Decision

- Local repo can clear coordinate-source blockers now: False
- Experimental coordinate shortcuts blocked: True
- Approved predicted-structure rows ready now: False
- Fixed-threshold audit ready to rerun now: False
- Apply or change threshold now: False
- Next gate: Approve and stage deployment-valid predicted coordinates with provider/model/version/path/checksum provenance for P07071, P07658, P00806, and P04531. Do not use the local experimental PDB CIFs as deployment shortcuts, and do not retune threshold 0.44155.

## Interpretation

- No approved predicted coordinates are locally staged for the four residual coordinate-source blockers. Three accessions have local experimental CIF shortcuts, but those shortcuts are deployment-invalid for Lever 3.
- Create a provider-neutral predicted-coordinate approval and staging manifest with checksums; P07071 is the smallest first row because it has no local CIF hit at all.
