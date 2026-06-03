# Fold-Augmented Confounded Proxy Train/Cal Background-Axis Scout - current702

Run: 2026-06-03T18:14:50Z

Train/cal-only scout over the 170 background-only Lever 3 confounded-proxy rows. It summarizes source-free feature axes that could inspire a future proxy-axis contract, but it does not register an axis, score rows, tune thresholds, read heldout rows, or count any background row as abstained evidence.

## Status

- fold_augmented_confounded_proxy_train_cal_background_axis_scout_blocked
- Background-only rows: 160
- Active-site residue-count 10+ rows: 0
- Organic score 0.30 to below high-axis rows: 0
- Unsupported geometry rows: 8
- Mechanically ready axis tests: 0/3
- Blockers: ['no_pre_registered_new_proxy_axis_contract', 'background_rows_not_countable_as_current_axis_evidence', 'unsupported_geometry_rows_require_coordinate_or_locus_repair']

## Feature Distribution

- Active-site residue-count bins: {'1_to_3': 57, '4_to_6': 72, '7_to_9': 31}
- Organic score bins: {'0_05_to_0_15': 51, '0_15_to_0_30': 9, 'lt_0_05': 100}
- Role graph statuses: {'ok': 160}

## Candidate Axis Tests

| axis | rows | ready now | blocker |
| --- | ---: | --- | --- |
| active_site_residue_count_10_plus | 0 | False | axis_has_no_pre_registered_train_cal_acceptance_criterion |
| organic_score_0_30_to_below_high_axis_threshold | 0 | False | would_create_new_proxy_axis_without_pre_registered_calibration_contract |
| unsupported_inorganic_locus_geometry | 8 | False | unsupported_or_missing_geometry_is_a_data-quality_blocker_not_abstained_evidence |

## Decision

- New proxy axis ready to score now: False
- Proxy calibration rerun ready now: False
- Next gate: Pre-register a train/cal-only acceptance contract for exactly one source-free proxy axis before scoring or rerunning the fixed-threshold audit. Otherwise continue with reviewed source decisions or Lever 2/4 gates.

## Interpretation

- 160 background-only rows expose 3 possible source-free scout axes, but 0 are mechanically ready to score.
- The remaining row features are useful for designing a future proxy-axis contract, not for counting abstained evidence under the current high-cofactor or inorganic/structural axes.
- If Lever 3 continues without reviewer decisions, define a pre-registered train/cal-only proxy-axis contract before any new scoring tranche.
