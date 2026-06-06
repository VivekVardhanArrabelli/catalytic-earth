# Fold-Augmented Confounded Proxy Surface And Calibration State After Q43088/P07658 - current702

Run: 2026-06-04T11:15:48Z

Consolidated Lever 3 state after Q43088 locator approval and the broad P07658 public computed-model repository probe. It records the exact remaining surface blocker, unchanged train/cal calibration blockers, and the smallest next experiments. It does not score rows, rerun or retune threshold 0.44155, edit labels, or use heldout rows for calibration.

## Status

- fold_augmented_confounded_proxy_surface_and_calibration_state_blocked_p07658_and_train_cal_acquisition
- Surface blockers: 1
- Partial rescore-input ready rows: 4
- P07658 public computed model rows: 0
- High-cofactor candidate pool rows available now: 0
- High-cofactor new abstained rows needed: 16
- Same-family structural new abstained rows needed: 170
- Blockers: ['p07658_full_length_predicted_coordinate_missing', 'public_computed_model_repository_no_p07658_hit', 'sixteen_row_high_cofactor_train_cal_probe_not_acquired', 'one_hundred_seventy_row_same_family_structural_acquisition_not_acquired', 'fixed_threshold_audit_not_ready_to_rerun']

## Remaining Surface Blocker

| row | accession | missing evidence | smallest next experiment |
| --- | --- | --- | --- |
| m_csa:562 | P07658 | full-length deployment-valid predicted structure for exact 715-residue sequence including selenocysteine | Install or provision an approved full-length predictor/runtime that supports the exact 715-residue P07658 sequence including selenocysteine, or use a credentialed provider; then stage provider/model/version/path/checksum provenance. |

## Decisions

- Q43088 requires more locator work now: False
- P07658 requires credentialed/local predictor now: True
- High-cofactor current candidate pool can close shortfall: False
- Fixed-threshold audit ready to rerun now: False
- Next gate: Do not rerun or retune threshold 0.44155. The next mechanical surface action is P07658 full-length prediction; the next calibration action is new train/cal acquisition because the current candidate pool has zero high-cofactor-axis rows.

## Interpretation

- Q43088 is no longer a surface-completeness blocker, but P07658 and train/cal calibration still block Lever 3 deployment validity. The current ready train/cal pool has zero high-cofactor-axis candidates, so current evidence cannot close the 16-row calibration shortfall.
- Run the P07658 full-length predictor/provider experiment first for surface completeness, and separately acquire the frozen 16-row high-cofactor train/cal OOS probe for calibration behavior.
