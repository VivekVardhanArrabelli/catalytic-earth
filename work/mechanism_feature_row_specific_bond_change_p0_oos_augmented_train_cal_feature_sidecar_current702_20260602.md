# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Train/Cal Feature Sidecar - current702

Run: 2026-06-02T10:28:18Z

No-fit OOS-augmented row-specific bond/proton/electron feature sidecar for approved P0 rows plus approved OOS calibration rows. Only label-stripped scalar event summaries are materialized.

## Status

- p0_oos_augmented_train_cal_row_specific_feature_sidecar_ready_no_fit
- Feature rows: 43
- Train rows: 11
- Calibration rows: 32
- Label type counts: {'out_of_scope': 28, 'seed_fingerprint': 15}
- Event type counts: {'bond_broken': 24, 'bond_formed': 32, 'bond_order_changed': 10, 'electron_transfer': 22, 'proton_transfer': 57}
- Critical violations: 0

## Decision

- Full no-template rerun ready: True

## Feature Rows

| row | split | events | bond changes | proton | electron | residues |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| m_csa:2 | calibration | 3 | 2 | 1 | 0 | 4 |
| m_csa:5 | train | 1 | 1 | 0 | 0 | 2 |
| m_csa:6 | calibration | 4 | 2 | 1 | 1 | 6 |
| m_csa:11 | train | 4 | 2 | 0 | 2 | 6 |
| m_csa:15 | train | 3 | 2 | 1 | 0 | 6 |
| m_csa:16 | train | 4 | 2 | 2 | 0 | 4 |
| m_csa:17 | calibration | 5 | 4 | 1 | 0 | 7 |
| m_csa:23 | calibration | 2 | 1 | 1 | 0 | 5 |
| m_csa:25 | calibration | 3 | 3 | 0 | 0 | 2 |
| m_csa:37 | train | 2 | 0 | 0 | 2 | 1 |
| m_csa:40 | calibration | 1 | 1 | 0 | 0 | 4 |
| m_csa:49 | calibration | 3 | 0 | 1 | 2 | 4 |
| m_csa:59 | calibration | 5 | 0 | 3 | 2 | 6 |
| m_csa:66 | train | 3 | 3 | 0 | 0 | 1 |
| m_csa:68 | train | 3 | 1 | 1 | 1 | 3 |
| m_csa:70 | calibration | 3 | 2 | 1 | 0 | 3 |
| m_csa:78 | calibration | 3 | 2 | 1 | 0 | 5 |
| m_csa:85 | calibration | 2 | 0 | 2 | 0 | 3 |
| m_csa:94 | train | 2 | 2 | 0 | 0 | 1 |
| m_csa:101 | calibration | 2 | 2 | 0 | 0 | 2 |
| m_csa:102 | train | 5 | 2 | 2 | 1 | 3 |
| m_csa:124 | train | 5 | 0 | 4 | 1 | 8 |
| m_csa:133 | calibration | 5 | 1 | 2 | 2 | 6 |
| m_csa:147 | calibration | 4 | 3 | 1 | 0 | 2 |
| m_csa:149 | calibration | 3 | 1 | 2 | 0 | 2 |
| m_csa:154 | calibration | 4 | 2 | 2 | 0 | 1 |
| m_csa:169 | train | 4 | 2 | 2 | 0 | 2 |
| m_csa:186 | calibration | 2 | 2 | 0 | 0 | 1 |
| m_csa:194 | calibration | 5 | 2 | 2 | 1 | 8 |
| m_csa:221 | calibration | 4 | 2 | 2 | 0 | 2 |
| m_csa:222 | calibration | 5 | 2 | 3 | 0 | 3 |
| m_csa:224 | calibration | 2 | 0 | 2 | 0 | 1 |
| m_csa:241 | calibration | 5 | 1 | 4 | 0 | 2 |
| m_csa:246 | calibration | 4 | 1 | 2 | 1 | 4 |
| m_csa:253 | calibration | 2 | 1 | 1 | 0 | 6 |
| m_csa:256 | calibration | 3 | 0 | 0 | 3 | 5 |
| m_csa:263 | calibration | 4 | 2 | 1 | 1 | 4 |
| m_csa:273 | calibration | 4 | 1 | 3 | 0 | 5 |
| m_csa:287 | calibration | 3 | 3 | 0 | 0 | 5 |
| m_csa:292 | calibration | 5 | 3 | 1 | 1 | 6 |
| m_csa:312 | calibration | 2 | 0 | 1 | 1 | 4 |
| m_csa:317 | calibration | 5 | 2 | 3 | 0 | 3 |
| m_csa:318 | calibration | 2 | 1 | 1 | 0 | 1 |

## Interpretation

- 43 approved train/cal rows were materialized; 28 are OOS calibration rows.
- Run the leakage guardrail and no-template centroid/residual rerun on this train/cal-only surface.
