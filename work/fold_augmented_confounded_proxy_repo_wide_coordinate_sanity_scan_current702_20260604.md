# Fold-Augmented Confounded Proxy Repo-Wide Coordinate Sanity Scan - current702

Run: 2026-06-04T09:45:56Z

Review-only repo-wide sanity scan for the four residual Lever 3 coordinate-source blockers. It scans local CIF accession hits under requested roots, classifies them against the deployment preflight, downloads no files, stages no coordinates, scores no rows, approves no source, and does not change threshold 0.44155.

## Status

- fold_augmented_confounded_proxy_repo_wide_coordinate_sanity_scan_no_additional_approved_predicted_coordinates
- Local CIF files scanned: 1636
- Local CIF accession hits: 3
- Unclassified local CIF hits: 0
- Rows with no local CIF hit: 1
- Rows with only disallowed experimental hits: 3
- Deployment-valid rows ready now: 0
- Blockers: ['repo_wide_scan_finds_no_additional_approved_predicted_coordinates', 'experimental_pdb_coordinate_shortcuts_remain_disallowed', 'provider_model_version_path_checksum_provenance_missing', 'fixed_threshold_audit_not_ready_to_rerun']

## Rows

| row | accession | repo-wide status | local CIF hits |
| --- | --- | --- | --- |
| m_csa:416 | P07071 | no_local_cif_accession_hit_observed | none |
| m_csa:562 | P07658 | only_disallowed_experimental_shortcut_hits_observed | artifacts/v3_foldseek_coordinates_1000/pdb_1AA6.cif (disallowed_experimental_coordinate_shortcut_recorded_in_preflight) |
| m_csa:586 | P00806 | only_disallowed_experimental_shortcut_hits_observed | artifacts/v3_foldseek_coordinates_1000/pdb_1LBA.cif (disallowed_experimental_coordinate_shortcut_recorded_in_preflight) |
| m_csa:637 | P04531 | only_disallowed_experimental_shortcut_hits_observed | artifacts/v3_foldseek_coordinates_1000/pdb_1DEK.cif (disallowed_experimental_coordinate_shortcut_recorded_in_preflight) |

## Decision

- Repo-wide scan changes deployment-input blocker: False
- Approved predicted-structure rows ready now: False
- Experimental coordinate shortcuts blocked: True
- Fixed-threshold audit ready to rerun now: False
- Apply or change threshold now: False
- Next gate: Approve and stage deployment-valid predicted coordinates for P07071, P07658, P00806, and P04531 with provider/model/version/path/checksum provenance. The repo-wide local CIF scan found no additional approved predicted-coordinate inputs.

## Interpretation

- The repo-wide CIF sanity scan agrees with the deployment-input preflight: no approved deployment-valid predicted coordinates are locally discoverable for the four coordinate-source blockers.
- Stage a provider-neutral predicted-coordinate approval manifest with checksums; do not use the local experimental PDB CIF hits as deployment shortcuts.
