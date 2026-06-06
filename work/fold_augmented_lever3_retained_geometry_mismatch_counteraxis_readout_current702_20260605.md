# Fold-Augmented Lever 3 Retained Geometry-Mismatch Counteraxis Readout - current702

Run: 2026-06-05T08:44:06Z

Lever 3 measured retained channel-geometry mismatch counteraxis readout. It selects a two-threshold source-free channel rule over frozen train/cal predicted-geometry scores: low top-1 active-site geometry score with high combined minimum geometry/fold score. Selection uses train/cal same-family OOS design rows only under zero retained-calibration fires and bounded train/cal OOS support, then applies the selected rule to retained application rows only after selection. It changes no thresholds, scores no rows, stages no coordinates, and uses no heldout rows.

## Status

- fold_augmented_lever3_retained_geometry_mismatch_counteraxis_readout_closed
- Geometry-mismatch counteraxis selected now: True
- Ready for application now: True
- Application rows used for rule selection: False

## Selection Policy

- Rule family: geometry_top1_score_less_equal_and_combined_min_geometry_fold_greater_equal
- Low channel: geometry_top1_score
- High channel: combined_min_geometry_fold
- Minimum design same-family rows fired: 2
- Train/cal OOS support floor/cap: 5/8
- Selection objective: maximize high-channel lower threshold, then minimize low-channel upper threshold, then maximize design support, then minimize train/cal OOS breadth

## Operating Point

- Calibration retained before/after geometry mismatch: 31/31 of 34
- Train/cal OOS abstained before/after geometry mismatch: 165/167 of 204
- New train/cal OOS abstentions from geometry mismatch: 2
- Production threshold change: False

## Counts

- Design same-family full-channel rows: 48/59
- Application rows with full channels: 11/11
- Rules evaluated / candidates within support bounds: 2025/45
- New retained rows fired after pocket chemistry: 1
- Retained residual rows after geometry mismatch: 0

## Selected Rule

- Rule: geometry_top1_score <= 0.582200 AND combined_min_geometry_fold >= 0.578200
- Calibration retained in-scope fired: 0
- Design same-family rows fired: 2
- All train/cal OOS rows fired: 5
- Retained application rows fired after selection: ['m_csa:308']

## Application Rows

| row | retained after pocket | mismatch fires | new mismatch | geometry top1 | combined min geometry/fold | action delta |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| m_csa:25 | False | False | False | 0.3778 | 0.3778 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:52 | False | False | False | 0.5977 | 0.5977 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:74 | False | False | False | 0.5864 | 0.5864 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:84 | False | False | False | 0.5971 | 0.538 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:89 | False | False | False | 0.409 | 0.409 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:190 | False | False | False | 0.5886 | 0.5886 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:229 | False | False | False | 0.5829 | 0.5047 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:256 | False | False | False | 0.5974 | 0.5974 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:308 | True | True | True | 0.5788 | 0.5788 | abstain_or_route_novel_oos_by_channel_geometry_mismatch |
| m_csa:468 | False | False | False | 0.591 | 0.591 | already_abstain_or_route_novel_oos_by_prior_counteraxis |
| m_csa:638 | False | False | False | 0.3756 | 0.3756 | already_abstain_or_route_novel_oos_by_prior_counteraxis |

## Top Candidate Rules

| rule | design fired | all OOS fired | application fired |
| --- | ---: | ---: | ---: |
| geometry_top1_score <= 0.582200 AND combined_min_geometry_fold >= 0.578200 | 2 | 5 | 1 |
| geometry_top1_score <= 0.585100 AND combined_min_geometry_fold >= 0.578200 | 3 | 6 | 1 |
| geometry_top1_score <= 0.582200 AND combined_min_geometry_fold >= 0.577500 | 3 | 6 | 1 |
| geometry_top1_score <= 0.585100 AND combined_min_geometry_fold >= 0.577500 | 4 | 7 | 1 |
| geometry_top1_score <= 0.578200 AND combined_min_geometry_fold >= 0.565800 | 3 | 5 | 0 |
| geometry_top1_score <= 0.577500 AND combined_min_geometry_fold >= 0.565100 | 3 | 5 | 0 |
| geometry_top1_score <= 0.578200 AND combined_min_geometry_fold >= 0.565100 | 4 | 6 | 0 |
| geometry_top1_score <= 0.577500 AND combined_min_geometry_fold >= 0.563800 | 4 | 6 | 0 |
| geometry_top1_score <= 0.578200 AND combined_min_geometry_fold >= 0.563800 | 5 | 7 | 0 |
| geometry_top1_score <= 0.577500 AND combined_min_geometry_fold >= 0.550300 | 5 | 7 | 0 |

## Decision

- Zero residual retained-transfer risk available now: True
- Fixed-threshold scoring closure available now: False
- Unsafe forced mechanism transfer allowed: False
- Apply/change threshold now: False
- Newly abstained retained rows: ['m_csa:308']
- Remaining retained rows after geometry mismatch: []
- Next gate: Treat the selected geometry-mismatch rule as fail-closed evidence for newly fired retained rows. Do not change threshold 0.44155 or force a mechanism label; fixed-threshold scoring closure still requires the separate exact P07658 coordinate/provenance route.

## Guardrails

- Measured readout only. Existing source-free artifacts only; no coordinates, row scores, labels, registries, ontologies, imports, thresholds, heldout tuning, provider calls, or secret values changed.

## Interpretation

- The channel-geometry mismatch counteraxis adds 1 retained-row abstention after pocket chemistry.
- The selected rule is geometry_top1_score <= 0.582200 AND combined_min_geometry_fold >= 0.578200; retained residual rows after this stage are [].
- Use this readout as the current Lever 3 zero-residual retained-transfer operating point, while keeping scoring closure fail-closed until exact P07658 coordinate provenance exists.
