# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Train/Cal Projection Readout - current702

Run: 2026-06-04T14:57:25Z

Lever 2 measured train/cal readout for the currently source-free projectable subset of the row-specific bond-change/event-pair feature surface. It fits only train rows, selects only on calibration rows, compares against the full row-specific train/cal contract plus current fold/geometry context, and does not read or rescore heldout.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_train_cal_projection_readout_measured_research_only
- Result classification: research_only_signal_current_projection_incomplete
- Feature rows: 43
- Train rows: 11
- Calibration rows: 32
- Source-free projected fields: 4/19
- Missing frozen fields: 15
- Source-free candidate overlap with current calibration primary rows: 0/34
- Source-free candidate overlap with current calibration OOS rows: 0/75
- Blockers: none

## Measured Projection

- Projected residual calibration summary: {'rows': 32, 'primary_rows': 4, 'oos_rows': 28, 'mean_primary_residual': 0.30246, 'mean_oos_residual': 1.841015, 'auc_oos_gt_primary': 0.794643}
- Projected residual threshold: {'retention_target': 0.9, 'threshold': 0.40327957, 'primary_retain_recall': 1.0, 'oos_abstain_recall': 0.642857, 'primary_rows': 4, 'oos_rows': 28}
- Full row-specific residual calibration summary: {'auc_oos_gt_primary': 0.875, 'mean_oos_residual': 3.952038, 'mean_primary_residual': 2.75291, 'oos_rows': 28, 'primary_rows': 4, 'rows': 32}
- Full row-specific residual threshold: {'oos_abstain_recall': 0.857143, 'oos_rows': 28, 'primary_retain_recall': 1.0, 'primary_rows': 4, 'retention_target': 0.9, 'threshold': 3.21469422}
- Fold/geometry calibration context: {'calibration_in_scope_retain_recall': 0.9118, 'calibration_in_scope_retained': 31, 'calibration_in_scope_total': 34, 'calibration_oos_abstain_recall': 0.4, 'calibration_oos_abstained': 30, 'calibration_oos_total': 75, 'min_retain_target': 0.9, 'objective': 'maximize_calibration_oos_abstain_recall_subject_to_in_scope_retention', 'threshold': 0.44155}
- Split-aligned current-surface overlap: {'available': True, 'current_geometry_fold_calibration_primary_rows': 34, 'current_geometry_fold_calibration_oos_rows': 75, 'full_row_specific_feature_overlap_primary_rows': 1, 'full_row_specific_feature_overlap_oos_rows': 8, 'source_free_candidate_projection_overlap_primary_rows': 0, 'source_free_candidate_projection_overlap_oos_rows': 0, 'full_row_specific_feature_overlap_primary_entry_ids': ['m_csa:102'], 'full_row_specific_feature_overlap_oos_entry_ids': ['m_csa:17', 'm_csa:25', 'm_csa:40', 'm_csa:78', 'm_csa:85', 'm_csa:149', 'm_csa:222', 'm_csa:246'], 'source_free_candidate_projection_overlap_primary_entry_ids': [], 'source_free_candidate_projection_overlap_oos_entry_ids': [], 'measurability_note': 'The current source-free candidate projection cannot support a split-aligned incremental operating-point readout until it covers the current geometry/fold calibration-primary and train/cal OOS rows.'}
- Deltas: {'residual_oos_abstain_recall_delta_vs_full_row_specific': -0.214286, 'residual_auc_delta_vs_full_row_specific': -0.080357, 'residual_oos_abstain_recall_delta_vs_fold_geometry_context': 0.242857}

## Axis Repair Ceiling

| variant | fields | primary retain | OOS abstain | AUC | delta vs current | gap to full |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| current_source_free_projected_subset | 4 | 1.0 | 0.642857 | 0.794643 | 0.0 | 0.214286 |
| current_plus_missing_active_site_locator_count | 6 | 1.0 | 0.678571 | 0.830357 | 0.035714 | 0.178572 |
| current_plus_missing_bond_change | 9 | 1.0 | 0.75 | 0.790179 | 0.107143 | 0.107143 |
| current_plus_missing_confidence_metadata | 8 | 1.0 | 0.785714 | 0.8125 | 0.142857 | 0.071429 |
| current_plus_missing_electron_flow | 6 | 1.0 | 0.785714 | 0.870536 | 0.142857 | 0.071429 |
| current_plus_missing_event_topology | 6 | 1.0 | 0.714286 | 0.803571 | 0.071429 | 0.142857 |
| full_frozen_row_specific_surface | 19 | 1.0 | 0.857143 | 0.875 | 0.214286 | 0.0 |

## Best Axis Newly Caught OOS Rows

| row | current residual | current threshold | best-axis residual | best-axis threshold | current geometry/fold OOS |
| --- | ---: | ---: | ---: | ---: | --- |
| m_csa:154 | 0.40327957 | 0.40327957 | 1.90740451 | 1.72848324 | False |
| m_csa:221 | 0.40327957 | 0.40327957 | 1.90740451 | 1.72848324 | False |
| m_csa:224 | 0.40327957 | 0.40327957 | 1.90740451 | 1.72848324 | False |
| m_csa:256 | 0.0 | 0.40327957 | 2.71877433 | 1.72848324 | False |

## Projected Fields

- expanded_event_residue_role__event_residue_role_proton_transfer_electrostatic_stabiliser
- expanded_residue_code_count__residue_code_count_his_3
- has_proton_transfer_event
- proton_transfer_count

## Missing Frozen Fields

- bond_broken_count
- bond_change_event_count
- bond_formed_count
- bond_order_changed_count
- electron_transfer_count
- event_count
- has_bond_change_event
- has_electron_transfer_event
- high_confidence_event_count
- low_confidence_event_count
- mapped_active_site_residue_count
- medium_confidence_event_count
- multi_event_mechanism_flag
- unique_mapped_active_site_residue_count
- unknown_confidence_event_count

## Decision

- Deployable now: False
- Research-only: True
- Negative: False
- Complete for frozen contract: False
- Split-aligned current-surface incremental readout measurable: False
- Value beyond fold/geometry context: True
- Value beyond full row-specific surface: False
- Best-axis new OOS rows overlap current geometry/fold OOS: False
- Best next source-free axis by ceiling: electron_flow
- Heldout read once performed: False
- Next gate: Prioritize source-free electron-flow projection first by the train/cal ceiling, then materialize the remaining bond-change and event-topology axes; rerun this projection readout before any heldout or deployment claim.

## Interpretation

- The current source-free projection is measured on train/cal using 4/19 frozen feature fields. Residual OOS abstain recall is 0.642857 at primary retain recall 1.0; full row-specific context is 0.857143.
- Prioritize source-free electron-flow projection first by the train/cal ceiling, then materialize the remaining bond-change and event-topology axes; rerun this projection readout before any heldout or deployment claim.
