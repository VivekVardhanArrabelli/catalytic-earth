# Family Panel High-Value Glycyl-Radical No-Template Feature Guardrail - current702

Run: 2026-06-01T22:09:02Z

Review-only guardrail joining the high-value glycyl-radical/thiamine panel to the P0 no-template feature-readiness audit. It prevents heldout OOS panel rows from being mistaken for train/cal feature-refresh inputs.

## Status

- glycyl_radical_panel_no_template_feature_guardrail_ready_review_only
- Panel rows: 2
- Heldout final-only rows: 2
- Rows present in P0 train/cal readiness: 0
- Rows allowed for no-template feature refresh: 0

## Rows

| row | gate status | geometry top1 | fold TM | present in P0 readiness | decision |
| --- | --- | --- | ---: | --- | --- |
| m_csa:30 | abstained_at_research_threshold | metal_dependent_hydrolase:0.2616 | 0.4988 | False | hold_review_only_final_readout_control_not_train_cal_feature_input |
| m_csa:31 | abstained_at_research_threshold | metal_dependent_hydrolase:0.3466 | 0.3809 | False | hold_review_only_final_readout_control_not_train_cal_feature_input |

## Interpretation

- Both high-value panel rows are score-complete and abstained at the fixed research threshold, but they are heldout OOS controls and absent from train/cal feature-readiness inputs.
- Source-check row-specific radical/thiamine bond-change evidence for review-only interpretation; keep no-template feature-contract refresh limited to approved train/cal rows.
