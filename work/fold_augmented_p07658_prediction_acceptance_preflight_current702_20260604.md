# Fold-Augmented P07658 Prediction Acceptance Preflight - current702

Run: 2026-06-04T12:20:41Z

Fail-closed acceptance preflight for the P07658 full-length prediction request manifest. It verifies whether an exact deployment-valid predicted coordinate plus provider provenance exists, stages no coordinate, scores no row, and does not change threshold 0.44155.

## Status

- fold_augmented_p07658_prediction_acceptance_preflight_blocked
- Candidate coordinate exists: False
- Candidate provenance exists: False
- Acceptance checks passed/failed: 1/7
- Fixed-threshold audit ready to rerun now: False
- Blockers: ['p07658_candidate_coordinate_file_missing', 'p07658_candidate_prediction_provenance_missing', 'p07658_acceptance_checks_not_all_passing', 'fixed_threshold_audit_not_ready_to_rerun']

## Acceptance Checks

| check | passed | observed |
| --- | --- | --- |
| coordinate_file_exists | False | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/p07658_full_length_predictor_current702_20260604.cif |
| coordinate_sha256_recorded | False | None |
| provider_model_version_recorded | False | {'provider': None, 'model_name_or_id': None, 'model_version': None} |
| input_sequence_sha256_matches_manifest | False | None |
| sequence_length_is_715 | False | None |
| selenocysteine_handling_documented | False | {'selenocysteine_count': None, 'selenocysteine_positions': [], 'selenocysteine_handling': None} |
| experimental_pdb_metadata_not_used_as_deployment_input | False | None |
| row_not_scored_until_coordinate_staged | True | True |

## Decision

- P07658 acceptance preflight passes now: False
- Coordinate blocker cleared now: False
- Next gate: Stage P07658 only after every acceptance check passes; then score only the staged surface rows at unchanged threshold 0.44155.

## Interpretation

- P07658 cannot be staged from the current repo state because the exact full-length predicted coordinate and provenance are not both present.
- Produce one deployment-valid full-length prediction for the exact sequence, including documented selenocysteine handling, then rerun this preflight before any fixed-threshold readout.
