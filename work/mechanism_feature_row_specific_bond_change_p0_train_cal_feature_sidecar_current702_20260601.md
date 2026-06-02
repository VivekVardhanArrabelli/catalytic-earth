# Mechanism Feature Row-Specific Bond-Change P0 Train/Cal Feature Sidecar - current702

Run: 2026-06-02T06:38:47Z

Partial no-fit row-specific bond/proton/electron feature sidecar for reviewer-approved P0 rows only. It joins approved source evidence to the existing train/cal split and excludes draft and heldout rows.

## Status

- p0_train_cal_row_specific_feature_sidecar_ready_partial_no_fit
- Materialized feature rows: 3
- Train rows: 3
- Calibration rows: 0
- Draft rows excluded: 12
- Heldout approved rows excluded: 0
- Event type counts: {'bond_broken': 3, 'bond_formed': 2, 'electron_transfer': 2, 'proton_transfer': 2}
- Critical violations: 0

## Decision

- Partial train/cal feature materialization ready: True
- Full no-template rerun ready: False
- Reason: Only a partial approved P0 surface is materialized; continue review until train and calibration rows cover the intended no-template feature pilot.

## Feature Rows

| row | split | event count | bond changes | proton | electron | unique residues |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| m_csa:5 | train | 1 | 1 | 0 | 0 | 2 |
| m_csa:11 | train | 4 | 2 | 0 | 2 | 6 |
| m_csa:169 | train | 4 | 2 | 2 | 0 | 2 |

## Interpretation

- 3 approved P0 rows were materialized into label-stripped train/cal row-specific event features; no draft or heldout rows were copied.
- Continue reviewer approval for the remaining P0 rows, then rerun this sidecar before attempting the no-template centroid pilot or out-of-atlas-span residual on the richer feature surface.
