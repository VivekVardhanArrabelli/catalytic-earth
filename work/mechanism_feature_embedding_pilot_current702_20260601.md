# Mechanism-Feature Embedding Pilot - current702

Run: 2026-06-01T21:13:28Z

Train/cal-only mechanism-feature embedding pilot over the audited current702 feature contract. It fits standardized nearest-primary centroids on assigned train rows and selects a review threshold on assigned calibration rows only.

## Status

- mechanism_feature_embedding_pilot_fit_train_cal_ready
- Feature rows: 524
- Train rows: 418
- Calibration rows: 106
- Heldout excluded rows: 140
- Variants: 2
- Best calibration variant: full_contract_with_reaction_template

## Variant Results

| variant | dim | cal primary acc | cal AUC primary>OOS | cal threshold | cal primary retain | cal OOS abstain |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| full_contract_with_reaction_template | 27 | 1.0 | 0.948491 | 0.20976681 | 0.914286 | 1.0 |
| no_reaction_template_ablation | 19 | 0.971429 | 0.549698 | 0.20976681 | 0.914286 | 0.140845 |

## Heldout Follow-Up

- heldout_not_evaluated_no_feature_surface
- materialize the same allowed feature fields for heldout rows, then apply the train-fit/cal-selected model exactly once

## Interpretation

- A real train/cal mechanism-feature centroid pilot is fit and calibrated without heldout use.
- Extend the audited feature materializer to heldout rows and run a once-only heldout readout; prioritize the no-template ablation if the full variant wins only by reaction-template leakage.
