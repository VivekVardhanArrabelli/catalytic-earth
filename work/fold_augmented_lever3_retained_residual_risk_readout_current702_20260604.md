# Fold-Augmented Lever 3 Retained Residual Risk Readout - current702

Run: 2026-06-05T04:08:34Z

Lever 3 measured retained-residual risk readout downstream of the deployment-action surface. It quantifies retained same-family residual rows, pocket-descriptor coverage, and the smallest source-free evidence gates needed before any zero-residual-risk claim. It scores no rows, stages no coordinates, changes no thresholds, and uses no heldout rows for training or threshold selection.

## Status

- fold_augmented_lever3_retained_residual_risk_readout_descriptor_present_actionable
- Safe abstention routing available now: True
- Fixed-threshold scoring closure available now: False
- Zero residual retained-transfer risk available now: False

## Operating Point

- Route: fixed_baseline_plus_cofactor_context_counteraxis_plus_same_family_numeric_bandpass_counteraxis_contract
- Baseline threshold: 0.44155
- Calibration retained: 31/34
- Train/cal OOS abstained: 105/204

## Retained Residual Queue

- Retained residual rows: 11
- With/missing/unknown pocket descriptors: 2/9/0
- Deployment-action residual abstentions: 10/21

| rank | row | closest channel | margin | descriptor | next evidence gate |
| ---: | --- | --- | ---: | --- | --- |
| 1 | m_csa:229 | cofactor_max_score | 0.004742 | pocket_descriptor_missing | source_free_pocket_descriptor_acquisition_required |
| 2 | m_csa:89 | combined_mean_geometry_fold | 0.00845 | pocket_descriptor_missing | source_free_pocket_descriptor_acquisition_required |
| 3 | m_csa:74 | cofactor_max_score | 0.011125 | pocket_descriptor_missing | source_free_pocket_descriptor_acquisition_required |
| 4 | m_csa:256 | cofactor_max_score | 0.015781 | pocket_descriptor_missing | source_free_pocket_descriptor_acquisition_required |
| 5 | m_csa:638 | cofactor_max_score | 0.019535 | pocket_descriptor_missing | source_free_pocket_descriptor_acquisition_required |
| 6 | m_csa:190 | cofactor_max_score | 0.025247 | pocket_descriptor_missing | source_free_pocket_descriptor_acquisition_required |
| 7 | m_csa:84 | cofactor_max_score | 0.026454 | pocket_descriptor_missing | source_free_pocket_descriptor_acquisition_required |
| 8 | m_csa:25 | combined_min_geometry_fold | 0.0398 | pocket_descriptor_present | train_cal_only_same_family_pocket_counteraxis_design_required |
| 9 | m_csa:52 | cofactor_max_score | 0.062269 | pocket_descriptor_present | train_cal_only_same_family_pocket_counteraxis_design_required |
| 10 | m_csa:468 | combined_mean_geometry_cofactor_fold | 0.131121 | pocket_descriptor_missing | source_free_pocket_descriptor_acquisition_required |
| 11 | m_csa:308 | combined_mean_geometry_cofactor_fold | 0.19385 | pocket_descriptor_missing | source_free_pocket_descriptor_acquisition_required |

## Smallest Next Experiments

| experiment | rows | countable now | action |
| --- | ---: | --- | --- |
| retained_descriptor_present_counteraxis_design | 2 | False | calibrate_or_validate a source-free pocket/chemistry counteraxis on train/cal evidence only before applying it to these retained rows |
| retained_descriptor_missing_acquisition | 9 | False | acquire source-free pocket descriptors without experimental-PDB deployment shortcuts or heldout tuning |

## Decision

- Unsafe forced mechanism transfer allowed: False
- Score or force mechanism label for retained rows now: False
- Apply/change threshold now: False
- Missing evidence for zero residual risk: ['train/cal-only source-free pocket or chemistry counteraxis for 2 descriptor-present retained residual rows', 'source-free pocket descriptor acquisition for 9 descriptor-missing retained residual rows']
- Next gate: First run a train/cal-only source-free pocket/chemistry counteraxis design for the descriptor-present retained rows; then acquire source-free pocket descriptors for the remaining descriptor-missing retained rows. Keep threshold 0.44155 unchanged and keep retained rows non-closure evidence until a counteraxis is accepted.

## Guardrails

- Measured readout only. No coordinates, row scores, labels, registries, ontologies, imports, thresholds, heldout tuning, provider calls, or secret values changed.

## Interpretation

- Safe fail-closed routing is available, but zero residual same-family transfer risk is not yet evidence-complete.
- 11 retained residual rows remain after accepted counteraxes; 2 have pocket descriptors and 9 still need descriptor acquisition.
- Use the deployment-action readout for routing now; do not treat retained residual rows as scoring closure until a train/cal-selected source-free counteraxis exists.
