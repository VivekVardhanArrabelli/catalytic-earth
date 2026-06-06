# Fold-Augmented P07658 Prediction Dispatch Packet - current702

Run: 2026-06-04T16:36:51Z

Dispatch-ready P07658 full-length prediction packet for the remaining Lever 3 surface-completeness blocker. It composes the frozen FASTA, provenance template, failed provider/runtime probes, and acceptance preflight; it stages no coordinates, scores no rows, and does not rerun or change threshold 0.44155.

## Status

- fold_augmented_p07658_prediction_dispatch_packet_ready_blocked_no_coordinate
- Entry: m_csa:562 / P07658
- Sequence length: 715
- Sequence SHA-256: 3090cc03d7d9a4015e6607c7008d258d99b15b4dfec5db660eadfea94b8fe9fa
- Dispatch inputs present: 4/4
- Provider routes returning coordinates now: 0/6
- Acceptance checks failed: 7
- Blockers: ['no_current_provider_or_local_runtime_returns_p07658_coordinate', 'p07658_candidate_coordinate_file_missing', 'p07658_candidate_prediction_provenance_missing', 'p07658_acceptance_checks_not_all_passing', 'fixed_threshold_audit_not_ready_to_rerun']

## Provider Routes

| route | status | coordinate now | blocker |
| --- | --- | --- | --- |
| public_esmfold_endpoint | fold_augmented_p07658_esmfold_api_preflight_blocked_sequence_too_long | False | public_esmfold_sequence_length_limit |
| local_full_length_predictor_runtime | fold_augmented_p07658_local_predictor_runtime_scan_blocked_no_runtime | False | local_full_length_predictor_runtime_not_installed |
| BioLM ESMFold | http_401 | False | provider_requires_credentials_or_access |
| OpenProtein ESMFold | http_403 | False | provider_requires_credentials_or_access |
| 3dbeacons_predicted_structure_probe | fold_augmented_p07658_3dbeacons_probe_blocked_experimental_only | False | three_d_beacons_has_no_deployment_valid_prediction |
| broad_public_computed_model_repository_probe | fold_augmented_p07658_computed_model_repository_broad_probe_blocked_no_public_computed_model | False | public_computed_model_repository_no_p07658_hit |

## Fill Targets

- FASTA: work/fold_augmented_p07658_full_length_prediction_input_current702_20260604.fasta
- Coordinate path: artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/p07658_full_length_predictor_current702_20260604.cif
- Filled provenance path: artifacts/v3_fold_augmented_p07658_prediction_provenance_filled_current702_20260604.json
- Rerun command:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-fold-augmented-p07658-prediction-acceptance-preflight --candidate-coordinate artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/p07658_full_length_predictor_current702_20260604.cif --candidate-provenance artifacts/v3_fold_augmented_p07658_prediction_provenance_filled_current702_20260604.json
```

## Decision

- Dispatch packet ready for provider run: True
- P07658 acceptance preflight passes now: False
- Fixed-threshold audit ready to rerun now: False
- Next gate: Do not score or rerun the fixed-threshold operating point until the P07658 coordinate/provenance packet passes all acceptance checks.

## Interpretation

- The P07658 provider dispatch inputs are ready, but no current credential-free provider, public repository, or local runtime has produced the required full-length coordinate.
- Use the recorded FASTA, fill targets, and rerun command for the smallest approved predictor experiment; keep P07658 blocked until the acceptance preflight passes.
