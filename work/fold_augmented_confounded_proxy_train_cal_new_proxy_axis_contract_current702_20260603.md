# Fold-Augmented Confounded Proxy Train/Cal New Proxy-Axis Contract - current702

Run: 2026-06-03T17:10:27Z

Train/cal-only pre-registration contract for one source-free replacement proxy axis after the current high-cofactor and inorganic/structural axes were exhausted. It freezes membership for a bounded future scoring tranche but does not score rows, tune thresholds, read heldout rows, or count any row as abstained evidence.

## Status

- fold_augmented_confounded_proxy_train_cal_new_proxy_axis_contract_ready
- Selected axis: active_site_residue_count_10_plus
- Membership rule: active_site_residue_count >= 10
- Contracted scoring rows: 6
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
| m_csa:89 | 13 | in_distribution | out_of_scope | heme:0.398339 |
| m_csa:90 | 14 | in_distribution | out_of_scope | plp:0.014237 |
| m_csa:143 | 16 | in_distribution | out_of_scope | heme:0.05565 |
| m_csa:253 | 10 | in_distribution | out_of_scope | heme:0.024512 |
| m_csa:466 | 12 | in_distribution | out_of_scope | heme:0.00075 |
| m_csa:501 | 10 | in_distribution | out_of_scope | plp:0.015665 |

## Acceptance Contract

- Use only rows emitted by the current train/cal background-axis scout.
- Require active_site_residue_count_bin == 10_plus and numeric active_site_residue_count >= 10.
- Keep all rows non-heldout and out-of-scope calibration rows.
- Run predicted-structure-vs-atlas scoring before any abstention claim.
- Rerun the fixed-threshold proxy audit only with threshold values unchanged.

## Interpretation

- Registered active_site_residue_count_10_plus as a train/cal-only source-free proxy-axis contract with 6 rows.
- This removes the missing-contract blocker but creates no abstained evidence until the contracted rows are scored at the unchanged fixed threshold.
- Build the scoring-input manifest from this contract and run only the contracted train/cal rows through predicted-structure-vs-atlas Foldseek scoring.
