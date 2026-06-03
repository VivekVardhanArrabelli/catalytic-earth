# Fold-Augmented Confounded Proxy Train/Cal New Proxy-Axis Contract - current702

Run: 2026-06-03T18:06:40Z

Train/cal-only pre-registration contract for one source-free replacement proxy axis after the current high-cofactor and inorganic/structural axes were exhausted. It freezes membership for a bounded future scoring tranche but does not score rows, tune thresholds, read heldout rows, or count any row as abstained evidence.

## Status

- fold_augmented_confounded_proxy_train_cal_new_proxy_axis_contract_ready
- Selected axis: organic_score_0_30_to_below_high_axis_threshold
- Membership rule: 0.30 <= selected_organic_cofactor_max_score < 0.50
- Contracted scoring rows: 4
- Heldout-like rows: 0
- Blockers: []

## Decision

- New proxy axis registered: True
- New proxy axis ready to score now: True
- Scoring tranche rows ready now: True
- Score contract tranche now: False
- Proxy calibration rerun ready now: False
- Next gate: Use this contract artifact as the scoring tranche input for the train/cal scoring-input manifest, then materialize or stage the listed coordinates and run Foldseek before parsing any scores. Do not rerun the fixed-threshold proxy audit until the contracted rows have real full-channel scores.

## Contracted Rows

| row | active-site count | split | label type | organic max |
| --- | ---: | --- | --- | --- |
| m_csa:60 | 4 | in_distribution | out_of_scope | plp:0.337092 |
| m_csa:75 | 7 | in_distribution | out_of_scope | heme:0.34378 |
| m_csa:214 | 6 | in_distribution | out_of_scope | plp:0.353171 |
| m_csa:288 | 6 | in_distribution | out_of_scope | heme:0.407563 |

## Acceptance Contract

- Use only rows emitted by the current train/cal background-axis scout.
- Require organic_subthreshold_score_bin == 0_30_to_below_high_axis and numeric selected_organic_cofactor_max_score below the high-axis threshold.
- Exclude rows already scored by any supplied scored-extension artifact.
- Keep all rows non-heldout and out-of-scope calibration rows.
- Run predicted-structure-vs-atlas scoring before any abstention claim.
- Rerun the fixed-threshold proxy audit only with threshold values unchanged.

## Interpretation

- Registered organic_score_0_30_to_below_high_axis_threshold as a train/cal-only source-free proxy-axis contract with 4 rows.
- This removes the missing-contract blocker but creates no abstained evidence until the contracted rows are scored at the unchanged fixed threshold.
- Build the scoring-input manifest from this contract and run only the contracted train/cal rows through predicted-structure-vs-atlas Foldseek scoring.
