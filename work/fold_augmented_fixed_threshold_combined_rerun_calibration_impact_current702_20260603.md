# Fold-Augmented Fixed-Threshold Combined Rerun Calibration Impact - current702

Run: 2026-06-03T00:57:46Z

Fixed-threshold calibration-impact audit after the Lever 3 combined rerun readout. It adds the four newly combined-score rows to the prior train/cal OOS negative surface at the frozen 0.44155 threshold, keeps P10746 as a fold-only caveat, and does not select a new threshold or inspect heldout rows.

## Status

- fold_augmented_fixed_threshold_combined_rerun_calibration_impact_ready
- Fixed threshold: 0.44155
- Prior full-channel rows: 71
- Expanded full-channel rows: 75/76
- Expanded abstained at fixed threshold: 30
- Expanded retained at fixed threshold: 45
- Remaining combined-score blockers: 1

## New Rows

| row | combined | abstains |
| --- | ---: | --- |
| m_csa:78 | 0.4054 | True |
| m_csa:531 | 0.4756 | False |
| uniprot:P78549 | 0.42485 | True |
| uniprot:Q3LXA3 | 0.4483 | False |

## Remaining Blockers

- m_csa:204

## Guardrails

- No threshold was selected or changed.
- No heldout rows were read for this calibration-impact audit.

## Next Gate

- Regenerate the OOS-calibrated threshold contract from the expanded train/cal surface only if a threshold-selection run is explicitly wanted; otherwise carry this fixed-threshold impact and the P10746 fold-only caveat into the deployment-closure audit.
