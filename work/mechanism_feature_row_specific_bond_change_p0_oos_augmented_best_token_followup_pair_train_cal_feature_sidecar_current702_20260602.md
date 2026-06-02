# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Expanded Train/Cal Feature Sidecar - current702

Run: 2026-06-02T12:28:23Z

No-fit train/cal row-specific feature sidecar for the best-token plus best follow-up-token pair. It preserves the previous best-token surface and adds exactly one additional sanitized boolean token selected by the follow-up ablation artifact.

## Status

- p0_oos_augmented_best_token_followup_pair_train_cal_feature_sidecar_ready_no_fit
- Feature rows: 43
- Train rows: 11
- Calibration rows: 32
- Base feature dimensions: 18
- Expanded feature dimensions: 1
- Total feature dimensions: 19
- Selected feature families: ['event_residue_role', 'residue_code_count']
- Critical violations: 0

## Decision

- Full no-template rerun ready: True
- Next gate: Run the strict leakage guardrail and no-template rerun, then write an explicit calibration-only operating-point contract before any heldout read.

## Feature Rows

| row | split | feature dimensions | expanded true features |
| --- | --- | ---: | ---: |
| m_csa:2 | calibration | 18 | 1 |
| m_csa:5 | train | 17 | 0 |
| m_csa:6 | calibration | 17 | 0 |
| m_csa:11 | train | 17 | 0 |
| m_csa:15 | train | 17 | 0 |
| m_csa:16 | train | 18 | 1 |
| m_csa:17 | calibration | 19 | 2 |
| m_csa:23 | calibration | 18 | 1 |
| m_csa:25 | calibration | 17 | 0 |
| m_csa:37 | train | 17 | 0 |
| m_csa:40 | calibration | 17 | 0 |
| m_csa:49 | calibration | 17 | 0 |
| m_csa:59 | calibration | 18 | 1 |
| m_csa:66 | train | 17 | 0 |
| m_csa:68 | train | 17 | 0 |
| m_csa:70 | calibration | 18 | 1 |
| m_csa:78 | calibration | 17 | 0 |
| m_csa:85 | calibration | 18 | 1 |
| m_csa:94 | train | 17 | 0 |
| m_csa:101 | calibration | 18 | 1 |
| m_csa:102 | train | 17 | 0 |
| m_csa:124 | train | 17 | 0 |
| m_csa:133 | calibration | 17 | 0 |
| m_csa:147 | calibration | 17 | 0 |
| m_csa:149 | calibration | 18 | 1 |
| m_csa:154 | calibration | 17 | 0 |
| m_csa:169 | train | 18 | 1 |
| m_csa:186 | calibration | 17 | 0 |
| m_csa:194 | calibration | 18 | 1 |
| m_csa:221 | calibration | 17 | 0 |
| m_csa:222 | calibration | 18 | 1 |
| m_csa:224 | calibration | 17 | 0 |
| m_csa:241 | calibration | 17 | 0 |
| m_csa:246 | calibration | 17 | 0 |
| m_csa:253 | calibration | 18 | 1 |
| m_csa:256 | calibration | 17 | 0 |
| m_csa:263 | calibration | 18 | 1 |
| m_csa:273 | calibration | 18 | 1 |
| m_csa:287 | calibration | 17 | 0 |
| m_csa:292 | calibration | 18 | 1 |
| m_csa:312 | calibration | 18 | 1 |
| m_csa:317 | calibration | 17 | 0 |
| m_csa:318 | calibration | 18 | 1 |

## Interpretation

- Follow-up token residue_code_count:his=3 was materialized on top of best token event_residue_role:proton_transfer|electrostatic_stabiliser as a two-token train/cal surface.
- Run guardrail, no-template rerun, and calibration contract without reading heldout.
