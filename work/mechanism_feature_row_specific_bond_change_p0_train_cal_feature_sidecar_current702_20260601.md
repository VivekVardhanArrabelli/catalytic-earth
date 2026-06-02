# Mechanism Feature Row-Specific Bond-Change P0 Train/Cal Feature Sidecar - current702

Run: 2026-06-02T09:19:56Z

Partial no-fit row-specific bond/proton/electron feature sidecar for reviewer-approved P0 rows only. It joins approved source evidence to the existing train/cal split and excludes draft and heldout rows.

## Status

- p0_train_cal_row_specific_feature_sidecar_ready_partial_no_fit
- Materialized feature rows: 15
- Train rows: 11
- Calibration rows: 4
- Draft rows excluded: 0
- Heldout approved rows excluded: 0
- Event type counts: {'bond_broken': 8, 'bond_formed': 8, 'bond_order_changed': 9, 'electron_transfer': 10, 'proton_transfer': 16}
- Critical violations: 0

## Decision

- Partial train/cal feature materialization ready: True
- Full no-template rerun ready: True

## Feature Rows

| row | split | event count | bond changes | proton | electron | unique residues |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| m_csa:5 | train | 1 | 1 | 0 | 0 | 2 |
| m_csa:6 | calibration | 4 | 2 | 1 | 1 | 6 |
| m_csa:11 | train | 4 | 2 | 0 | 2 | 6 |
| m_csa:15 | train | 3 | 2 | 1 | 0 | 6 |
| m_csa:16 | train | 4 | 2 | 2 | 0 | 4 |
| m_csa:37 | train | 2 | 0 | 0 | 2 | 1 |
| m_csa:66 | train | 3 | 3 | 0 | 0 | 1 |
| m_csa:68 | train | 3 | 1 | 1 | 1 | 3 |
| m_csa:94 | train | 2 | 2 | 0 | 0 | 1 |
| m_csa:102 | train | 5 | 2 | 2 | 1 | 3 |
| m_csa:124 | train | 5 | 0 | 4 | 1 | 8 |
| m_csa:133 | calibration | 5 | 1 | 2 | 2 | 6 |
| m_csa:147 | calibration | 4 | 3 | 1 | 0 | 2 |
| m_csa:169 | train | 4 | 2 | 2 | 0 | 2 |
| m_csa:186 | calibration | 2 | 2 | 0 | 0 | 1 |

## Interpretation

- 15 approved P0 rows were materialized into label-stripped train/cal row-specific event features; no draft or heldout rows were copied.
- Continue reviewer approval for the remaining P0 rows, then rerun this sidecar before attempting the no-template centroid pilot or out-of-atlas-span residual on the richer feature surface.
