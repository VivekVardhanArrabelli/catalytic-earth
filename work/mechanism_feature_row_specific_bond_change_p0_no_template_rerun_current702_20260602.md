# Mechanism Feature Row-Specific Bond-Change P0 No-Template Rerun - current702

Run: 2026-06-02T09:49:45Z

Train/cal-only no-template rerun over the approved P0 row-specific bond/proton/electron feature sidecar. It fits nearest-primary centroids on train rows and selects thresholds on calibration rows only; heldout rows are not materialized from M-CSA row-specific source evidence.

## Status

- p0_row_specific_no_template_train_cal_scored_oos_blocked
- Feature rows: 15
- Train rows: 11
- Calibration rows: 4
- Calibration OOS rows: 0
- Feature dimensions: 17

## Centroid Variant

- Train summary: {'rows': 11, 'primary_rows': 11, 'oos_rows': 0, 'primary_nearest_label_accuracy': 0.909091, 'mean_primary_similarity': 0.348648, 'mean_oos_similarity': None, 'auc_primary_vs_oos': None}
- Calibration summary: {'rows': 4, 'primary_rows': 4, 'oos_rows': 0, 'primary_nearest_label_accuracy': 0.25, 'mean_primary_similarity': 0.279151, 'mean_oos_similarity': None, 'auc_primary_vs_oos': None}
- Calibration threshold: {'retention_target': 0.9, 'threshold': 0.23726514, 'primary_retain_recall': 1.0, 'oos_abstain_recall': 0.0, 'primary_rows': 4, 'oos_rows': 0}

## Residual Variant

- Train summary: {'rows': 11, 'primary_rows': 11, 'oos_rows': 0, 'mean_primary_residual': 2.442243, 'mean_oos_residual': None, 'auc_oos_gt_primary': None}
- Calibration summary: {'rows': 4, 'primary_rows': 4, 'oos_rows': 0, 'mean_primary_residual': 2.618359, 'mean_oos_residual': None, 'auc_oos_gt_primary': None}
- Calibration threshold: {'retention_target': 0.9, 'threshold': 3.21469422, 'primary_retain_recall': 1.0, 'oos_abstain_recall': None, 'primary_rows': 4, 'oos_rows': 0}

## Decision

- Known-vs-novel operating point evaluable: False
- Heldout read once performed: False
- Reason: The approved P0 row-specific train/cal surface has no calibration OOS/novel rows, so known-vs-novel abstention cannot be measured at an operating point yet.
- Next gate: Add approved train/cal OOS/novel row-specific evidence rows or a non-M-CSA row-specific heldout-safe surface before claiming novelty separation.

## Interpretation

- The no-template centroid and residual rerun is scored on train/cal rows, but the P0 surface is all in-scope primary labels, so it cannot yet answer known-vs-novel separation.
- Broaden the approved row-specific surface with split-safe OOS/novel calibration evidence, then rerun this artifact and only read heldout once on a heldout-safe feature surface.
