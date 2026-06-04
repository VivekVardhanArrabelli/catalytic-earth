# Fold-Augmented Confounded Proxy Residual Queue After P10746/Q43088 - current702

Run: 2026-06-04T08:26:58Z

Consolidated Lever 3 residual blocker queue after accepting the P10746 fold-only caveat and isolating Q43088 to an approved locator-sidecar gap. It does not approve sources, download coordinates, rescore rows, rerun thresholds, or use heldout rows for calibration.

## Status

- fold_augmented_confounded_proxy_residual_queue_blocked_after_p10746_q43088
- P10746 policy blockers resolved: 1
- Residual full-channel rows: 5
- Coordinate-source rows: 4
- Locator/geometry sidecar rows: 1
- Q43088 additional locator positions needed: 2
- High-cofactor new abstained rows needed: 16
- Same-family structural new abstained rows needed: 170
- Blockers: ['four_rows_need_approved_alternate_predicted_structure_source', 'q43088_needs_two_additional_approved_locator_positions_or_geometry_sidecar', 'sixteen_row_high_cofactor_train_cal_probe_not_acquired', 'one_hundred_seventy_row_same_family_structural_acquisition_not_acquired', 'fixed_threshold_audit_not_ready_to_rerun']

## Residual Full-Channel Rows

| row | accession | blocker | next gate detail |
| --- | --- | --- | --- |
| m_csa:416 | P07071 | predicted_structure_unavailable | approve alternate deployment-valid predicted-structure source; AFDB-v6 direct and secondary probes remain unavailable |
| m_csa:562 | P07658 | predicted_structure_unavailable | approve alternate deployment-valid predicted-structure source; AFDB-v6 direct and secondary probes remain unavailable |
| m_csa:586 | P00806 | predicted_structure_unavailable | approve alternate deployment-valid predicted-structure source; AFDB-v6 direct and secondary probes remain unavailable |
| m_csa:604 | Q43088 | approved_geometry_feature_missing | approve/source two additional source-free locator positions or an approved geometry sidecar for Q43088 |
| m_csa:637 | P04531 | predicted_structure_unavailable | approve alternate deployment-valid predicted-structure source; AFDB-v6 direct and secondary probes remain unavailable |

## Decision

- Fixed-threshold audit ready to rerun now: False
- Surface completeness action: For surface completeness, either approve alternate deployment-valid predicted structures for P07071/P07658/P00806/P04531 or source them from an approved non-AFDB predicted-structure provider; in parallel, source/approve two Q43088 locator positions.
- Calibration closure action: For confounded-safe calibration closure, start the frozen 16-row non-heldout train/cal high-cofactor acquisition contract; structural closure still needs the 170-row acquisition surface.

## Interpretation

- After today's reconciliation, Lever 3 no longer has a fresh P10746 policy-decision blocker. The remaining local full-channel blockers are four approved predicted-structure-source gaps plus Q43088's approved locator/geometry sidecar gap; the confounded-safe calibration shortfalls remain 16 high-cofactor rows and 170 same-family structural rows.
- Do not rerun or retune threshold 0.44155. The smallest calibration experiment remains the frozen 16-row high-cofactor train/cal OOS acquisition; the smallest surface-completeness experiment is Q43088 locator approval plus one approved alternate predicted structure for any of the four AFDB-unavailable rows.
