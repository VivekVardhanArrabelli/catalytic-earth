# Fold-Augmented Lever 3 Same-Family Bandpass Counteraxis Contract - current702

Run: 2026-06-04T21:10:57Z

Deployment-valid Lever 3 same-family numeric bandpass counteraxis contract. It accepts the train/cal-selected scout rule from the cofactor-context readout only when the fixed 0.44155 baseline is unchanged, the 31/34 calibration in-scope floor is preserved, zero calibration in-scope rows newly fire, and the retained same-family residual shortfall is closed without heldout tuning.

## Status

- fold_augmented_lever3_same_family_bandpass_counteraxis_contract_accepted
- Accepted: True
- Baseline threshold: 0.44155
- Combined route: fixed_baseline_plus_cofactor_context_counteraxis_plus_same_family_numeric_bandpass_scout
- Fold band: 0.6257 to 0.7357
- Geometry max: 0.5757
- Calibration retained: 31/34
- Same-family shortfall before/after: 9/0
- Combined train/cal OOS abstained: 105/204
- Combined strict proxy abstained: high=1, same-family=26

## Validation Checks

| check | pass |
| --- | --- |
| baseline_threshold_fixed_044155 | True |
| high_cofactor_residual_already_closed | True |
| no_forbidden_predictive_features | True |
| production_threshold_unchanged | True |
| retention_floor_preserved | True |
| same_family_shortfall_closed | True |
| selected_on_train_cal_only | True |
| selection_rule_present | True |
| source_free_numeric_features_only | True |
| source_guardrails_clean | True |
| source_readout_is_measured | True |
| zero_additional_calibration_in_scope_fires | True |

## Selected Same-Family Residual Rows

| entry | fold tm | geometry | fired |
| --- | ---: | ---: | --- |
| m_csa:135 | 0.6594 | 0.404 | True |
| m_csa:223 | 0.6379 | 0.3777 | True |
| m_csa:451 | 0.6341 | 0.5419 | True |
| m_csa:463 | 0.6791 | 0.4162 | True |
| m_csa:464 | 0.6421 | 0.5638 | True |
| m_csa:488 | 0.7306 | 0.5503 | True |
| m_csa:502 | 0.6652 | 0.5262 | True |
| m_csa:503 | 0.6857 | 0.4196 | True |
| m_csa:646 | 0.717 | 0.3667 | True |

## Decision

- Deployment-valid same-family counteraxis ready: True
- Current evidence sufficient for deployment closure: False
- Fixed-threshold audit ready to rerun now: False
- Remaining missing evidence: ['accepted full-length P07658 predicted coordinate provenance before fixed-threshold surface rerun']
- Next gate: Accepted same-family bandpass counteraxis contract; continue the P07658 full-length predicted-coordinate provenance path before any fixed-threshold surface rerun.

## Interpretation

- The same-family numeric bandpass is accepted as a deployment counteraxis contract for train/cal operation.
- The contract retains 31/34 calibration in-scope rows, fires on 9/9 required retained same-family residual rows, and yields 105/204 train/cal OOS abstentions in the combined route.
- Use this as the accepted same-family counteraxis contract; the remaining deployment closure dependency is the P07658 full-length predicted-coordinate provenance gate.
