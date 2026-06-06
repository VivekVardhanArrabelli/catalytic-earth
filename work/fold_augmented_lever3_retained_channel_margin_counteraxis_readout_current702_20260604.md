# Fold-Augmented Lever 3 Retained Channel-Margin Counteraxis Readout - current702

Run: 2026-06-05T07:47:48Z

Lever 3 measured retained channel-margin counteraxis readout. It selects a strict-positive score-margin buffer over frozen train/cal source-free channel scores and then selects a fold-nearest-atlas TM midband over the same frozen channel surface, followed by a high-fold/low-geometry-cofactor pressure rule. All stages exclude retained application rows from rule selection and apply the selected rules only after selection. It changes no thresholds, scores no new rows, stages no coordinates, and uses no heldout rows.

## Status

- fold_augmented_lever3_retained_channel_margin_counteraxis_readout_partial_application
- Channel-margin counteraxis selected now: True
- Fold-TM bandpass counteraxis selected now: True
- Fold/cofactor pressure counteraxis selected now: True
- Ready for partial application now: True
- Application rows used for rule selection: False

## Selection Policy

- Rule family: pairwise_or_of_strict_positive_channel_margin_buffer_rules followed by fold_tm_closed_interval_bandpass_rules and fold_cofactor_pressure_two_channel_rules
- Candidate features: ['primary_channel_margin', 'active_route_min_positive_margin']
- Fold-TM bandpass feature: fold_nearest_atlas_tm_score
- Fold/cofactor pressure features: ['combined_mean_geometry_cofactor_fold', 'fold_nearest_atlas_tm_score']
- Active route channels: ['cofactor_max_score', 'combined_mean_geometry_cofactor_fold', 'combined_mean_geometry_fold', 'combined_min_geometry_fold', 'fold_nearest_atlas_tm_score']
- Strict-positive lower bound open: True
- All train/cal OOS breadth cap rows: 50
- Margin selection objective: maximize design same-family OOS rows fired, then maximize component design-row support, then minimize all train/cal OOS full-channel rows fired, then deterministic rule id
- Fold-TM bandpass selection objective: within the fold-nearest-atlas TM bandpass family, maximize design same-family OOS rows fired, then maximize train/cal OOS pressure under the breadth cap, then deterministic rule id
- Fold/cofactor pressure selection objective: within the low combined geometry/cofactor plus high fold-TM pressure family at or above the selected fold-TM bandpass lower bound, maximize design same-family OOS rows fired, then maximize train/cal OOS pressure under the breadth cap, then deterministic rule id

## Operating Point

- Calibration retained before/after margin: 31/31 of 34
- Train/cal OOS abstained after accepted counteraxes / descriptors / margin: 105/110/138 of 204
- Train/cal OOS abstained after margin+fold-TM bandpass: 161 of 204
- Train/cal OOS abstained after all counteraxes: 165 of 204
- Production threshold change: False

## Counts

- Design same-family full-channel rows: 48/59
- Atom/pair rules checked: 11/66
- Candidate pair rules within breadth cap: 66
- Fold-TM bandpass rules evaluated / within breadth cap: 1176/286
- Fold/cofactor pressure rules evaluated / within breadth cap: 1296/285
- New retained rows fired after descriptor rules: 7
- Retained residual rows before/after margin/after fold-TM bandpass/after all: 9/7/3/2
- New train/cal OOS abstentions from margin: 28
- New train/cal OOS abstentions from fold-TM bandpass: 23
- New train/cal OOS abstentions from fold/cofactor pressure: 4

## Selected Margin Rule

- Rule: active_route_min_positive_margin in (0, 0.004750] OR primary_channel_margin in (0, 0.018650]
- Calibration retained in-scope fired: 0
- Design same-family rows fired: 10
- Component design support total: 11
- All train/cal OOS rows fired: 44
- Retained application rows fired after selection: ['m_csa:89', 'm_csa:229']

## Selected Fold-TM Bandpass Rule

- Rule: fold_nearest_atlas_tm_score in [0.577600, 0.685700]
- Calibration retained in-scope fired: 0
- Design same-family rows fired: 17
- All train/cal OOS rows fired: 50
- Retained application rows fired after selection: ['m_csa:52', 'm_csa:74', 'm_csa:190', 'm_csa:256']

## Selected Fold/Cofactor Pressure Rule

- Rule: combined_mean_geometry_cofactor_fold <= 0.413589 AND fold_nearest_atlas_tm_score >= 0.577600
- Calibration retained in-scope fired: 0
- Design same-family rows fired: 16
- All train/cal OOS rows fired: 47
- Retained application rows fired after selection: ['m_csa:638']

## Application Rows

| row | descriptor routed | margin fires | fold bandpass fires | pressure fires | new margin | new fold bandpass | new pressure | primary margin | active-route margin | fold TM | action delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| m_csa:25 | True | False | False | False | False | False | False | 0.18255 | 0.0398 | 0.8704 | already_abstain_or_route_novel_oos_by_descriptor_rule |
| m_csa:52 | False | False | True | False | False | True | False | 0.17385 | 0.062269 | 0.6331 | abstain_or_route_novel_oos_by_fold_tm_bandpass |
| m_csa:74 | False | False | True | False | False | True | False | 0.1715 | 0.011125 | 0.6397 | abstain_or_route_novel_oos_by_fold_tm_bandpass |
| m_csa:84 | True | False | False | False | False | False | False | 0.126 | 0.026454 | 0.538 | already_abstain_or_route_novel_oos_by_descriptor_rule |
| m_csa:89 | False | True | False | False | True | False | False | 0.00845 | 0.00845 | 0.491 | abstain_or_route_novel_oos_by_channel_margin |
| m_csa:190 | False | False | True | False | False | True | False | 0.19495 | 0.025247 | 0.6844 | abstain_or_route_novel_oos_by_fold_tm_bandpass |
| m_csa:229 | False | True | False | False | True | False | False | 0.10225 | 0.004742 | 0.5047 | abstain_or_route_novel_oos_by_channel_margin |
| m_csa:256 | False | False | True | False | False | True | False | 0.1777 | 0.015781 | 0.6411 | abstain_or_route_novel_oos_by_fold_tm_bandpass |
| m_csa:308 | False | False | False | False | False | False | False | 0.2396 | 0.19385 | 0.7835 | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:468 | False | False | False | False | False | False | False | 0.2007 | 0.131121 | 0.6935 | retain_at_fixed_operating_point_not_scoring_closure |
| m_csa:638 | False | False | False | True | False | False | True | 0.14465 | 0.019535 | 0.7968 | abstain_or_route_novel_oos_by_fold_cofactor_pressure |

## Top Candidate Margin Pair Rules

| rule | design fired | component support | all OOS fired | application fired |
| --- | ---: | ---: | ---: | ---: |
| active_route_min_positive_margin in (0, 0.004750] OR primary_channel_margin in (0, 0.018650] | 10 | 11 | 44 | 2 |
| active_route_min_positive_margin in (0, 0.003929] OR primary_channel_margin in (0, 0.018650] | 10 | 10 | 40 | 1 |
| active_route_min_positive_margin in (0, 0.004750] OR primary_channel_margin in (0, 0.017400] | 9 | 10 | 41 | 2 |
| active_route_min_positive_margin in (0, 0.002211] OR primary_channel_margin in (0, 0.018650] | 9 | 9 | 33 | 1 |
| active_route_min_positive_margin in (0, 0.003929] OR primary_channel_margin in (0, 0.017400] | 9 | 9 | 37 | 1 |
| active_route_min_positive_margin in (0, 0.004750] OR primary_channel_margin in (0, 0.013400] | 8 | 9 | 37 | 2 |
| active_route_min_positive_margin in (0, 0.002211] OR primary_channel_margin in (0, 0.017400] | 8 | 8 | 30 | 1 |
| active_route_min_positive_margin in (0, 0.002127] OR primary_channel_margin in (0, 0.018650] | 8 | 8 | 31 | 1 |
| active_route_min_positive_margin in (0, 0.003929] OR primary_channel_margin in (0, 0.013400] | 8 | 8 | 33 | 1 |
| active_route_min_positive_margin in (0, 0.004750] OR primary_channel_margin in (0, 0.005500] | 7 | 8 | 31 | 1 |

## Top Candidate Fold-TM Bandpass Rules

| rule | design fired | all OOS fired | application fired |
| --- | ---: | ---: | ---: |
| fold_nearest_atlas_tm_score in [0.577600, 0.685700] | 17 | 50 | 4 |
| fold_nearest_atlas_tm_score in [0.577600, 0.679100] | 16 | 47 | 3 |
| fold_nearest_atlas_tm_score in [0.585600, 0.685700] | 16 | 45 | 4 |
| fold_nearest_atlas_tm_score in [0.571700, 0.665200] | 15 | 48 | 3 |
| fold_nearest_atlas_tm_score in [0.577600, 0.675300] | 15 | 45 | 3 |
| fold_nearest_atlas_tm_score in [0.589600, 0.685700] | 15 | 44 | 4 |
| fold_nearest_atlas_tm_score in [0.585600, 0.679100] | 15 | 42 | 3 |
| fold_nearest_atlas_tm_score in [0.571700, 0.659400] | 14 | 46 | 3 |
| fold_nearest_atlas_tm_score in [0.577600, 0.665200] | 14 | 42 | 3 |
| fold_nearest_atlas_tm_score in [0.589600, 0.679100] | 14 | 41 | 3 |

## Top Candidate Fold/Cofactor Pressure Rules

| rule | design fired | all OOS fired | application fired |
| --- | ---: | ---: | ---: |
| combined_mean_geometry_cofactor_fold <= 0.413589 AND fold_nearest_atlas_tm_score >= 0.577600 | 16 | 47 | 1 |
| combined_mean_geometry_cofactor_fold <= 0.411601 AND fold_nearest_atlas_tm_score >= 0.577600 | 15 | 46 | 1 |
| combined_mean_geometry_cofactor_fold <= 0.413589 AND fold_nearest_atlas_tm_score >= 0.585600 | 15 | 44 | 1 |
| combined_mean_geometry_cofactor_fold <= 0.411601 AND fold_nearest_atlas_tm_score >= 0.585600 | 14 | 43 | 1 |
| combined_mean_geometry_cofactor_fold <= 0.413589 AND fold_nearest_atlas_tm_score >= 0.589600 | 14 | 43 | 1 |
| combined_mean_geometry_cofactor_fold <= 0.406287 AND fold_nearest_atlas_tm_score >= 0.577600 | 14 | 42 | 1 |
| combined_mean_geometry_cofactor_fold <= 0.411601 AND fold_nearest_atlas_tm_score >= 0.589600 | 13 | 42 | 1 |
| combined_mean_geometry_cofactor_fold <= 0.405888 AND fold_nearest_atlas_tm_score >= 0.577600 | 13 | 41 | 1 |
| combined_mean_geometry_cofactor_fold <= 0.406287 AND fold_nearest_atlas_tm_score >= 0.585600 | 13 | 39 | 1 |
| combined_mean_geometry_cofactor_fold <= 0.413589 AND fold_nearest_atlas_tm_score >= 0.602300 | 13 | 39 | 1 |

## Decision

- Zero residual retained-transfer risk available now: False
- Fixed-threshold scoring closure available now: False
- Unsafe forced mechanism transfer allowed: False
- Apply/change threshold now: False
- Newly abstained retained rows: ['m_csa:52', 'm_csa:74', 'm_csa:89', 'm_csa:190', 'm_csa:229', 'm_csa:256', 'm_csa:638']
- Remaining retained rows after all counteraxes: ['m_csa:308', 'm_csa:468']
- Next gate: Treat the selected strict-positive channel-margin and fold-TM midband/fold-cofactor pressure rules as partial fail-closed evidence for newly fired retained rows only. Continue designing source-free chemistry/evidence axes for the remaining retained rows; do not change threshold 0.44155 or force a mechanism label.

## Guardrails

- Measured readout only. Existing artifacts only; no coordinates, row scores, labels, registries, ontologies, imports, thresholds, heldout tuning, provider calls, or secret values changed.

## Interpretation

- The channel-margin, fold-TM bandpass, and fold/cofactor pressure counteraxes add 7 retained-row abstentions after descriptor counteraxes.
- The selected margin rule is active_route_min_positive_margin in (0, 0.004750] OR primary_channel_margin in (0, 0.018650]; the selected fold-TM bandpass is fold_nearest_atlas_tm_score in [0.577600, 0.685700]; the selected fold/cofactor pressure rule is combined_mean_geometry_cofactor_fold <= 0.413589 AND fold_nearest_atlas_tm_score >= 0.577600; retained residual rows fall from 9 to 2, while calibration retention stays 31/34.
- Keep the remaining retained rows in the evidence queue and search for another source-free chemistry/evidence axis selected only on train/cal rows.
