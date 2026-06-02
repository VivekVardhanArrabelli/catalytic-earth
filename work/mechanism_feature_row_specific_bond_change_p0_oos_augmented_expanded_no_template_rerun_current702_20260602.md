# Mechanism Feature Row-Specific Bond-Change P0 No-Template Rerun - current702

Run: 2026-06-02T11:15:43Z

Train/cal-only no-template rerun over the expanded OOS-augmented row-specific feature sidecar. It fits centroids on train rows and selects thresholds on calibration rows only; heldout is unread.

## Status

- p0_row_specific_no_template_train_cal_operating_point_ready
- Feature rows: 43
- Train rows: 11
- Calibration rows: 32
- Calibration OOS rows: 28
- Feature dimensions: 560

## Centroid Variant

- Train summary: {'rows': 11, 'primary_rows': 11, 'oos_rows': 0, 'primary_nearest_label_accuracy': 1.0, 'mean_primary_similarity': 0.163489, 'mean_oos_similarity': None, 'auc_primary_vs_oos': None}
- Calibration summary: {'rows': 32, 'primary_rows': 4, 'oos_rows': 28, 'primary_nearest_label_accuracy': 0.25, 'mean_primary_similarity': 0.056466, 'mean_oos_similarity': 0.062307, 'auc_primary_vs_oos': 0.285714}
- Calibration threshold: {'retention_target': 0.9, 'threshold': 0.0492274, 'primary_retain_recall': 1.0, 'oos_abstain_recall': 0.035714, 'primary_rows': 4, 'oos_rows': 28}

## Residual Variant

- Train summary: {'rows': 11, 'primary_rows': 11, 'oos_rows': 0, 'mean_primary_residual': 10.5814, 'mean_oos_residual': None, 'auc_oos_gt_primary': None}
- Calibration summary: {'rows': 32, 'primary_rows': 4, 'oos_rows': 28, 'mean_primary_residual': 16.981108, 'mean_oos_residual': 15.213428, 'auc_oos_gt_primary': 0.285714}
- Calibration threshold: {'retention_target': 0.9, 'threshold': 19.31389136, 'primary_retain_recall': 1.0, 'oos_abstain_recall': 0.035714, 'primary_rows': 4, 'oos_rows': 28}

## Decision

- Known-vs-novel operating point evaluable: True
- Heldout read once performed: False
- Next gate: Apply the calibrated operating point to a heldout-safe surface exactly once.

## Interpretation

- The no-template centroid and residual rerun has a calibration OOS operating point.
- Compare this calibration-only operating point against the coarse OOS-augmented surface; only replace the frozen residual contract if a follow-on calibration contract artifact explicitly records the change.
