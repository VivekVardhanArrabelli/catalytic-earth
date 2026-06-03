# Fold-Augmented Expanded Train/Cal OOS Negative Surface Scores - current702

Run: 2026-06-03T01:09:52Z

Expanded train/cal OOS-negative calibration surface after the Lever 3 fixed-threshold combined rerun. It composes the approved rerun readout rows into the prior train/cal OOS surface, keeps P10746 as the single fold-only policy caveat, and does not read heldout rows or select thresholds.

## Status

- computed_partial_expanded_train_cal_oos_negative_surface_scores
- Blockers: ['remaining_fold_only_policy_caveat_not_combined_scored']
- Expanded full-channel rows: 75/76
- New combined readout rows: 4
- Replaced candidate rows: 4
- Remaining combined-score blocker rows: 1

## Replaced Rows

| row | combined | source | abstains at fixed threshold |
| --- | ---: | --- | --- |
| m_csa:78 | 0.4054 | fixed_threshold_combined_rerun_readout | True |
| m_csa:531 | 0.4756 | fixed_threshold_combined_rerun_readout | False |
| uniprot:P78549 | 0.42485 | fixed_threshold_combined_rerun_readout | True |
| uniprot:Q3LXA3 | 0.4483 | fixed_threshold_combined_rerun_readout | False |

## Remaining Blockers

- m_csa:204

## Guardrails

- No threshold was selected or changed by this surface composer.
- No heldout rows were read.
- No label, registry, ontology, import, model-weight, or production scorer changed.

## Next Gate

- Regenerate the OOS-calibrated threshold contract from this expanded train/cal surface, then carry the P10746 caveat into the deployment-closure decision.
