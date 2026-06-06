# Fold-Augmented P07658 Local Predictor Runtime Scan - current702

Run: 2026-06-04T10:32:44Z

Review-only local-runtime scan for the remaining P07658 Lever 3 coordinate blocker. It checks only local command, Python-module, and shallow filesystem availability for full-length predicted-structure generators; it stages no coordinates, scores no rows, and does not change threshold 0.44155.

## Status

- fold_augmented_p07658_local_predictor_runtime_scan_blocked_no_runtime
- Path commands available: 0 of 5
- Conda envs checked: 3
- Python module hits: 0
- Coordinates staged: 0
- Remaining coordinate-source blockers: 1
- Blockers: ['local_full_length_predictor_runtime_not_installed', 'p07658_exact_sequence_requires_715_residue_and_selenocysteine_support', 'p07658_predicted_coordinate_not_staged', 'fixed_threshold_audit_not_ready_to_rerun']

## Command Probe

| command | on PATH |
| --- | --- |
| colabfold_batch | False |
| foldSequence | False |
| esm-fold | False |
| esmfold | False |
| omegafold | False |

## Env Module Probe

| env | module hits |
| --- | ---: |
| base | 0 |
| alzheimers | 0 |
| neo4j_env | 0 |

## Decision

- Local runtime clears P07658 now: False
- Fixed-threshold audit ready to rerun now: False
- Missing evidence type: approved full-length predicted-structure runtime or provider output for the exact 715-residue P07658 sequence including selenocysteine, with provider/model/version/path/checksum provenance
- Smallest next experiment: Install or provision an approved full-length predictor/runtime that supports the exact P07658 sequence, or use a credentialed provider, then stage one coordinate with provider/model/version/path/checksum provenance.

## Interpretation

- No local command, Python module, or shallow filesystem evidence exposes a usable full-length predictor/runtime for P07658. The row remains a coordinate-source blocker.
- Provision a full-length predictor or credentialed provider for P07658; do not retry partial sequence truncation or experimental-PDB shortcuts.
