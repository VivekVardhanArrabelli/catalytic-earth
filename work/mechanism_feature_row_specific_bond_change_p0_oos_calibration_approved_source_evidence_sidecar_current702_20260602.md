# Mechanism Feature Row-Specific Bond-Change P0 OOS Calibration Approved Source-Evidence Sidecar - current702

Run: 2026-06-02T10:28:17Z

Approved source-evidence sidecar for the first staged P0 OOS calibration rows. It materializes row-specific source evidence only for split-safe train/cal OOS rows and keeps them out of model training.

## Status

- p0_oos_calibration_approved_source_evidence_sidecar_ready
- Selected OOS rows: 28
- Approved rows: 28
- Calibration rows: 28
- Rows with Rhea equations: 28
- Event type counts: {'bond_broken': 16, 'bond_formed': 24, 'bond_order_changed': 1, 'electron_transfer': 12, 'proton_transfer': 41}
- Blocker counts: {'rhea_equation_missing': 2}

## Approved Rows

| row | split | events | consumable |
| --- | --- | ---: | --- |
| m_csa:2 | calibration | 3 | True |
| m_csa:17 | calibration | 5 | True |
| m_csa:23 | calibration | 2 | True |
| m_csa:25 | calibration | 3 | True |
| m_csa:40 | calibration | 1 | True |
| m_csa:49 | calibration | 3 | True |
| m_csa:59 | calibration | 5 | True |
| m_csa:70 | calibration | 3 | True |
| m_csa:78 | calibration | 3 | True |
| m_csa:85 | calibration | 2 | True |
| m_csa:101 | calibration | 2 | True |
| m_csa:149 | calibration | 3 | True |
| m_csa:154 | calibration | 4 | True |
| m_csa:194 | calibration | 5 | True |
| m_csa:221 | calibration | 4 | True |
| m_csa:222 | calibration | 5 | True |
| m_csa:224 | calibration | 2 | True |
| m_csa:241 | calibration | 5 | True |
| m_csa:246 | calibration | 4 | True |
| m_csa:253 | calibration | 2 | True |
| m_csa:256 | calibration | 3 | True |
| m_csa:263 | calibration | 4 | True |
| m_csa:273 | calibration | 4 | True |
| m_csa:287 | calibration | 3 | True |
| m_csa:292 | calibration | 5 | True |
| m_csa:312 | calibration | 2 | True |
| m_csa:317 | calibration | 5 | True |
| m_csa:318 | calibration | 2 | True |

## Skipped Candidate Rows

| row | split | blockers |
| --- | --- | --- |
| m_csa:76 | calibration | rhea_equation_missing |
| m_csa:202 | calibration | rhea_equation_missing |

## Interpretation

- 28 OOS calibration rows were approved with source-spanned M-CSA/Rhea row-specific events.
- Run the strict OOS sidecar audit, then merge approved rows with the approved P0 source sidecar for train/cal-only feature materialization.
