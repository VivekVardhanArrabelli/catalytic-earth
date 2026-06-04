# Fold-Augmented Lever 3 Cofactor-Context Counteraxis Readout - current702

Run: 2026-06-04T20:45:44Z

Lever 3 measured cofactor-context counteraxis readout. It adds a bounded, source-free supplemental veto over train/cal-selected operating points: high cofactor score, zero predicted cofactor-context support, high fold similarity, and geometry above the train/cal geometry floor. It does not use heldout rows, labels, source IDs, target names, mechanism text, EC/Rhea IDs, or experimental-PDB metadata as predictive features.

## Status

- fold_augmented_lever3_cofactor_context_counteraxis_readout_ready_same_family_bandpass_scout_closure
- Baseline threshold: 0.44155
- Geometry floor: 0.338
- Selected cofactor threshold: 0.95
- Selected fold threshold: 0.85
- Calibration retained with counteraxis: 31/34
- Residual high-cofactor fired/remaining: 1/0
- Residual same-family fired/remaining: 1/20
- Same-family residual pocket descriptor coverage: 5/21
- Same-family bandpass scout fired/shortfall: 9/0

## Selected Counteraxis Rows

| subset | counteraxis rows |
| --- | --- |
| all_train_cal_oos | m_csa:289 |
| strict_high_cofactor_proxy | m_csa:289 |
| strict_same_family_structural_proxy | m_csa:289 |
| residual_all | m_csa:289 |

## Route Readouts

| route | subset | rows | baseline abstained | counteraxis fired | augmented abstained | retained |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| fixed_baseline_plus_counteraxis | all_train_cal_oos | 204 | 72 | 1 | 73 | 131 |
| fixed_baseline_plus_counteraxis | strict_high_cofactor_proxy | 4 | 0 | 1 | 1 | 3 |
| fixed_baseline_plus_counteraxis | strict_same_family_structural_proxy | 59 | 11 | 1 | 12 | 47 |
| fixed_baseline_plus_counteraxis | residual_all | 21 | 0 | 1 | 1 | 20 |
| fixed_baseline_plus_counteraxis | residual_high_cofactor | 1 | 0 | 1 | 1 | 0 |
| fixed_baseline_plus_counteraxis | residual_same_family | 21 | 0 | 1 | 1 | 20 |
| best_retention_preserving_union_plus_counteraxis | all_train_cal_oos | 204 | 26 | 1 | 27 | 177 |
| best_retention_preserving_union_plus_counteraxis | strict_high_cofactor_proxy | 4 | 2 | 1 | 3 | 1 |
| best_retention_preserving_union_plus_counteraxis | strict_same_family_structural_proxy | 59 | 0 | 1 | 1 | 58 |
| best_retention_preserving_union_plus_counteraxis | residual_all | 21 | 0 | 1 | 1 | 20 |
| best_retention_preserving_union_plus_counteraxis | residual_high_cofactor | 1 | 0 | 1 | 1 | 0 |
| best_retention_preserving_union_plus_counteraxis | residual_same_family | 21 | 0 | 1 | 1 | 20 |

## Same-Family Numeric Bandpass Scout

- Status: same_family_numeric_bandpass_scout_closes_required_shortfall
- Eligible/closing rules: 570/20
- Selected fold band: 0.6257 to 0.7357
- Selected geometry max: 0.5757
- Selected calibration fired: 0
- Selected all train/cal OOS fired: 32
- Remaining same-family residual rows fired: 9
- Same-family shortfall after scout: 0
- Combined operating-point calibration retained: 31/34
- Combined operating-point all train/cal OOS abstained: 105/204
- Combined operating-point strict proxies abstained: high=1, same-family=26

| fired same-family residual rows |
| --- |
| m_csa:135, m_csa:223, m_csa:451, m_csa:463, m_csa:464, m_csa:488, m_csa:502, m_csa:503, m_csa:646 |

## Decision

- Cofactor-context counteraxis preserves in-scope floor: True
- Resolves high-cofactor residual: True
- Resolves same-family residual: False
- Same-family numeric bandpass scout closes required shortfall: True
- Source-free numeric scout supports operating-point closure: True
- Current evidence sufficient for deployment closure: False
- Exact missing evidence: ['accepted deployment counteraxis contract for the measured same-family numeric bandpass scout before production use', 'accepted full-length P07658 predicted coordinate provenance before fixed-threshold surface rerun']
- Next gate: Keep threshold 0.44155 unchanged. The new source-free numeric cofactor-context counteraxis safely abstains the high-cofactor residual row while preserving 31/34 train/cal in-scope retention; the same-family numeric bandpass scout is now the next contract hardening target, alongside P07658 predicted-coordinate acceptance before deployment closure.

## Interpretation

- A source-free cofactor-context counteraxis can safely catch the high-cofactor residual row without losing additional in-scope calibration rows.
- The selected counteraxis fires on 1/1 high-cofactor residual rows and 1/21 same-family residual rows while retaining 31/34 calibration in-scope rows.
- The high-cofactor residual shortfall is cleared for this measured route. The same-family numeric bandpass scout closes the remaining shortfall to 0 on train/cal while preserving the in-scope floor; current candidate pocket descriptors still cover only 5/21 same-family residual rows.
