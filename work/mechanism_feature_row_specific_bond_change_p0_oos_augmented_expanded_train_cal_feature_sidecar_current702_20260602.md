# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Expanded Train/Cal Feature Sidecar - current702

Run: 2026-06-02T11:15:34Z

No-fit expanded train/cal row-specific feature sidecar for the approved OOS-augmented surface. It preserves the original coarse event-count features and adds sanitized boolean tokens only from the retained-OOS target's ready feature families.

## Status

- p0_oos_augmented_expanded_train_cal_row_specific_feature_sidecar_ready_no_fit
- Feature rows: 43
- Train rows: 11
- Calibration rows: 32
- Base feature dimensions: 17
- Expanded feature dimensions: 543
- Total feature dimensions: 560
- Selected feature families: ['event_residue_code', 'event_residue_code_count', 'event_residue_role_count', 'residue_role_count', 'event_mapped_residue_count', 'event_participant_arity', 'event_type_sequence', 'event_mapped_residue_bucket']
- Critical violations: 0

## Decision

- Full no-template rerun ready: True
- Next gate: Run the leakage guardrail and no-template centroid/residual rerun on this expanded train/cal-only surface.

## Feature Rows

| row | split | feature dimensions | expanded true features |
| --- | --- | ---: | ---: |
| m_csa:2 | calibration | 58 | 41 |
| m_csa:5 | train | 43 | 26 |
| m_csa:6 | calibration | 84 | 67 |
| m_csa:11 | train | 43 | 26 |
| m_csa:15 | train | 48 | 31 |
| m_csa:16 | train | 62 | 45 |
| m_csa:17 | calibration | 63 | 46 |
| m_csa:23 | calibration | 52 | 35 |
| m_csa:25 | calibration | 53 | 36 |
| m_csa:37 | train | 38 | 21 |
| m_csa:40 | calibration | 31 | 14 |
| m_csa:49 | calibration | 65 | 48 |
| m_csa:59 | calibration | 54 | 37 |
| m_csa:66 | train | 45 | 28 |
| m_csa:68 | train | 64 | 47 |
| m_csa:70 | calibration | 57 | 40 |
| m_csa:78 | calibration | 57 | 40 |
| m_csa:85 | calibration | 38 | 21 |
| m_csa:94 | train | 39 | 22 |
| m_csa:101 | calibration | 47 | 30 |
| m_csa:102 | train | 74 | 57 |
| m_csa:124 | train | 61 | 44 |
| m_csa:133 | calibration | 72 | 55 |
| m_csa:147 | calibration | 58 | 41 |
| m_csa:149 | calibration | 47 | 30 |
| m_csa:154 | calibration | 43 | 26 |
| m_csa:169 | train | 69 | 52 |
| m_csa:186 | calibration | 56 | 39 |
| m_csa:194 | calibration | 82 | 65 |
| m_csa:221 | calibration | 45 | 28 |
| m_csa:222 | calibration | 68 | 51 |
| m_csa:224 | calibration | 32 | 15 |
| m_csa:241 | calibration | 52 | 35 |
| m_csa:246 | calibration | 64 | 47 |
| m_csa:253 | calibration | 48 | 31 |
| m_csa:256 | calibration | 39 | 22 |
| m_csa:263 | calibration | 71 | 54 |
| m_csa:273 | calibration | 48 | 31 |
| m_csa:287 | calibration | 39 | 22 |
| m_csa:292 | calibration | 70 | 53 |
| m_csa:312 | calibration | 41 | 24 |
| m_csa:317 | calibration | 65 | 48 |
| m_csa:318 | calibration | 40 | 23 |

## Interpretation

- 43 approved train/cal rows were materialized with 543 expanded boolean feature dimensions from retained-OOS target families.
- Run the strict leakage guardrail and no-template rerun; compare the calibration operating point against the coarse surface without reading heldout.
