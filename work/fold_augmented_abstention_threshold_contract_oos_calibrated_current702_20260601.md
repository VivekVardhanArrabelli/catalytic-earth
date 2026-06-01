# Fold-Augmented OOS-Calibrated Threshold Contract - current702

Run: 2026-06-01T07:11:13Z

Leakage-safe OOS-calibrated fold-augmented threshold contract. Thresholds are selected using deterministic in-distribution calibration in-scope rows plus hash-selected in-distribution OOS calibration negatives; heldout rows remain final evaluation only.

## Status

- computed_oos_calibrated_threshold_contract
- Blockers: ['train_cal_oos_negative_surface_is_partial']
- Calibration in-scope rows: 34
- Calibration OOS negative rows: 71
- Heldout final-eval rows: 126

## Primary Channel

- Channel: combined_mean_geometry_fold
- OOS-calibrated 90% threshold: {'threshold': 0.44155, 'min_retain_target': 0.9, 'calibration_in_scope_retain_recall': 0.9118, 'calibration_in_scope_retained': 31, 'calibration_in_scope_total': 34, 'calibration_oos_abstain_recall': 0.3944, 'calibration_oos_abstained': 28, 'calibration_oos_total': 71, 'objective': 'maximize_calibration_oos_abstain_recall_subject_to_in_scope_retention'}
- Prior in-scope-only 90% threshold: {'calibration_in_scope_retain_recall': 0.9118, 'calibration_in_scope_retained': 31, 'calibration_in_scope_total': 34, 'min_retain_target': 0.9, 'threshold': 0.44155}
- Heldout final eval at OOS-calibrated threshold: {'threshold': 0.44155, 'heldout_in_scope_retained': 45, 'heldout_in_scope_total': 47, 'heldout_in_scope_retain_recall': 0.9574, 'heldout_oos_abstained': 44, 'heldout_oos_total': 79, 'heldout_oos_abstain_recall': 0.557, 'heldout_confounded_oos_abstained': 5, 'heldout_confounded_oos_total': 6, 'heldout_confounded_oos_abstain_recall': 0.8333}

## Thresholds

| Channel | OOS-cal >=90 threshold | cal OOS abstain | heldout in-scope retain | heldout OOS abstain | heldout confounded abstain |
| --- | ---: | ---: | ---: | ---: | ---: |
| cofactor_max_score | 0.022422 | 0.2535 | 0.8723 | 0.2532 | 0.0 |
| combined_mean_geometry_cofactor_fold | 0.357468 | 0.6901 | 0.9574 | 0.6329 | 0.0 |
| combined_mean_geometry_fold | 0.44155 | 0.3944 | 0.9574 | 0.557 | 0.8333 |
| combined_min_geometry_fold | 0.338 | 0.1127 | 0.9362 | 0.1266 | 0.1667 |
| fold_nearest_atlas_tm_score | 0.4325 | 0.3239 | 0.9574 | 0.2785 | 0.3333 |
| geometry_top1_score | 0.338 | 0.1127 | 0.9362 | 0.1266 | 0.1667 |

## Contract

- maximize_calibration_oos_abstain_recall_subject_to_in_scope_retention
- heldout rows are evaluated after threshold selection and do not affect thresholds
- research_contract_not_production_threshold; no production scorer or global threshold was changed

## Interpretation

- The fold-augmented threshold contract now has an OOS-negative calibration surface.
- Review the primary channel's calibration-OOS and heldout final readout, then decide whether the partial 65-row OOS calibration surface is enough or whether to clear the remaining candidate geometry blockers first.
