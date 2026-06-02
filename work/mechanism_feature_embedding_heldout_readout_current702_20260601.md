# Mechanism-Feature Embedding Heldout Readout - current702

Run: 2026-06-01T21:19:00Z

Once-only heldout readout for the train/cal-fitted mechanism-feature embedding pilot. It materializes the same allowed feature fields for heldout rows from existing sidecars and applies train-fit, calibration-thresholded pilot variants without refit.

## Status

- mechanism_feature_embedding_heldout_readout_applied_once
- Heldout rows total: 140
- Heldout feature rows: 132
- Missing feature rows: 8
- Blocker counts: {'role_graph:missing_accession_compatible_sequence_positions': 8}

## Variant Readouts

| variant | rows | primary rows | OOS rows | AUC | threshold | primary retain | OOS abstain |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| full_contract_with_reaction_template | 132 | 48 | 84 | 0.8812 | 0.20976681 | 0.75 | 1.0 |
| no_reaction_template_ablation | 132 | 48 | 84 | 0.488591 | 0.20976681 | 0.854167 | 0.095238 |

## Interpretation

- The train/cal-fitted mechanism-feature pilot has now been applied to the heldout feature surface once.
- Use the no-template heldout readout as the honest mechanism signal floor, and continue row-specific bond-change/proton/electron-flow materialization before any production claim.
