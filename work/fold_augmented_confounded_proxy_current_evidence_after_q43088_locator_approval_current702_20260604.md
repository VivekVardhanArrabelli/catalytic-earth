# Fold-Augmented Confounded Proxy Current Evidence After Q43088 Locator Approval - current702

Run: 2026-06-04T11:42:32Z

Updated Lever 3 current-evidence packet after Q43088 source-free locator approval. It composes the prior SWISS-MODEL staging state with the Q43088 locator sidecar, keeps P07658 as the only surface completeness blocker, and does not score rows or change threshold 0.44155.

## Status

- fold_augmented_confounded_proxy_current_evidence_after_q43088_locator_approval_blocked_p07658
- Q43088 approved locator positions: 2
- Surface completeness blockers: 1
- Coordinate-source blocker rows: 1
- Locator/geometry sidecar blocker rows: 0
- Partial surface rescore-input ready rows: 4
- Fixed-threshold audit ready to rerun now: False
- Blockers: ['p07658_full_length_predicted_coordinate_missing', 'sixteen_row_high_cofactor_train_cal_probe_not_acquired', 'one_hundred_seventy_row_same_family_structural_acquisition_not_acquired', 'fixed_threshold_audit_not_ready_to_rerun']

## Surface Rows

| row | accession | blocker | missing evidence | smallest next experiment |
| --- | --- | --- | --- | --- |
| m_csa:562 | P07658 | predicted_structure_unavailable | full-length deployment-valid predicted structure for exact 715-residue sequence including selenocysteine | Install or provision an approved full-length predictor/runtime that supports the exact 715-residue P07658 sequence including selenocysteine, or use a credentialed provider; then stage provider/model/version/path/checksum provenance. |
| m_csa:604 | Q43088 | cleared | source-free locator sidecar staged | no row score yet |

## Decision

- Q43088 locator gate cleared now: True
- Current evidence can solve surface completeness: False
- Current evidence can solve confounded-safe calibration: False
- Apply or change threshold now: False
- Next gate: Do not rerun or retune threshold 0.44155. Q43088 is staged; P07658 remains the only surface-completeness blocker before fixed-threshold scoring can be rerun.

## Interpretation

- Q43088's source-free locator blocker is cleared and staged review-only. Surface completeness is now blocked only by P07658's exact full-length predicted coordinate; calibration shortfalls remain unchanged.
- Provision or run a full-length P07658 predictor/provider. Do not use experimental PDBe/PDB/3D-Beacons rows as deployment shortcuts, and do not tune the fixed threshold.
