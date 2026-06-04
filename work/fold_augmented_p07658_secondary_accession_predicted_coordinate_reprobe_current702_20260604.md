# Fold-Augmented P07658 Secondary-Accession Predicted Coordinate Reprobe - current702

Run: 2026-06-04T10:15:20Z

Smallest follow-up probe for the remaining Lever 3 coordinate-source blocker after SWISS-MODEL staging. It checks whether P07658 secondary UniProt accessions expose deployment-valid predicted structures. It stages no coordinates, scores no rows, and does not change threshold 0.44155.

## Status

- fold_augmented_p07658_secondary_accession_reprobe_blocked_no_predicted_model
- Secondary accessions checked: 2
- SWISS-MODEL predicted model rows: 0
- SWISS-MODEL PDB-provider rows: 10
- AFDB-v6 404 rows: 2
- Remaining coordinate-source blockers: 1
- Blockers: ['p07658_secondary_accessions_no_swissmodel_predicted_model', 'p07658_secondary_accessions_afdb_v6_404', 'p07658_only_experimental_pdb_repository_mappings_observed', 'fixed_threshold_audit_not_ready_to_rerun']

## Rows

| query accession | resolved primary | SWISS-MODEL predicted rows | PDB-provider rows | AFDB v6 | decision |
| --- | --- | ---: | ---: | ---: | --- |
| P78137 | P07658 | 0 | 5 | 404 | blocked |
| Q2M6M5 | P07658 | 0 | 5 | 404 | blocked |

## Decision

- Clears P07658 now: False
- Fixed-threshold audit ready now: False
- Smallest next experiment: Generate or obtain a fresh deployment-valid predicted structure for P07658 itself, with provider/model/version/path/checksum provenance; repository secondary-accession lookup cannot clear this row.

## Interpretation

- Secondary-accession lookup does not clear the remaining P07658 coordinate blocker; both secondary accessions resolve back to the same PDB-provider-only SWISS-MODEL repository surface and AFDB-v6 is unavailable.
- The smallest remaining coordinate experiment is a fresh predicted-structure generation/acquisition for P07658, not another accession alias lookup.
