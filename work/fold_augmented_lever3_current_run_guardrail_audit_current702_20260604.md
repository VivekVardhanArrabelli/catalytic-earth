# Fold-Augmented Lever 3 Current Run Guardrail Audit - current702

Run: 2026-06-04T11:40:45Z

Review-only guardrail audit over the new Lever 3 artifacts from the current run. It verifies that the packets preserve threshold 0.44155, do not score rows, do not stage P07658 coordinates, do not use heldout rows for tuning, and do not change labels/registries/ontologies/imports.

## Status

- fold_augmented_lever3_current_run_guardrail_audit_passed
- Artifacts checked: 7
- Guardrail violation artifacts: 0
- Threshold-change artifacts: 0
- Scoring artifacts: 0
- Coordinate-stage artifacts: 0

## Artifact Rows

| artifact | status | blockers |
| --- | --- | --- |
| v3_fold_augmented_q43088_locator_approval_packet_current702_20260604 | fold_augmented_q43088_locator_approval_packet_cleared_review_only | 4 |
| v3_fold_augmented_q43088_source_free_locator_sidecar_current702_20260604 | q43088_source_free_locator_sidecar_ready_review_only | 0 |
| v3_fold_augmented_confounded_proxy_current_evidence_after_q43088_locator_approval_current702_20260604 | fold_augmented_confounded_proxy_current_evidence_after_q43088_locator_approval_blocked_p07658 | 4 |
| v3_fold_augmented_p07658_computed_model_repository_broad_probe_current702_20260604 | fold_augmented_p07658_computed_model_repository_broad_probe_blocked_no_public_computed_model | 4 |
| v3_fold_augmented_confounded_proxy_surface_and_calibration_state_after_q43088_p07658_current702_20260604 | fold_augmented_confounded_proxy_surface_and_calibration_state_blocked_p07658_and_train_cal_acquisition | 5 |
| v3_fold_augmented_confounded_proxy_high_cofactor_candidate_near_miss_triage_current702_20260604 | fold_augmented_confounded_proxy_high_cofactor_candidate_near_miss_triage_blocked_zero_eligible_rows | 4 |
| v3_fold_augmented_p07658_full_length_prediction_request_manifest_current702_20260604 | fold_augmented_p07658_full_length_prediction_request_manifest_ready_blocker_not_cleared | 3 |

## Decision

- Keep Q43088 staged review-only, clear P07658 with an approved full-length predicted coordinate, and acquire eligible high-cofactor train/cal OOS rows before any fixed-threshold operating-point rerun.

## Interpretation

- The current run artifacts remain deployment-valid review artifacts: Q43088 is staged, P07658 is still blocked, and high-cofactor acquisition has zero eligible rows in the current pool.
- Run/provision the P07658 full-length predictor request manifest, then score only after coordinate provenance passes acceptance checks; separately acquire source-free high-cofactor train/cal OOS rows.
