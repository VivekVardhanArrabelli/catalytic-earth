# Lever 2 Source-Free Electron-Flow Acquisition-Ceiling Readout - current702

Run: 2026-06-05T01:47:33Z

Lever 2 measured acquisition-ceiling readout for source-free electron-flow evidence. It consumes the prior train/cal electron-flow split-alignment artifact, measures the smallest source-free row tranches needed to make the current split operating-point readout measurable, and does not materialize features, train models, tune thresholds, score heldout, or promote deployment state.

## Status

- lever2_source_free_electron_flow_acquisition_ceiling_readout_research_only_acquisition_ceiling
- Result class: research_only_acquisition_ceiling
- Train/cal electron-flow OOS recall delta: 0.142857
- Current candidate coverage for retained OOS rows: 0/40
- Current candidate coverage for primary rows: 0/34
- Smallest smoke tranche rows required: 35
- Full retained-OOS current-split rows required: 74

## Measured Signal Context

| surface | OOS abstain recall | AUC OOS > primary | primary retain |
| --- | ---: | ---: | ---: |
| current projected subset | 0.642857 | 0.794643 | 1.0 |
| current + electron flow | 0.785714 | 0.870536 | 1.0 |

## Current-Split Measurability

- Raw current-split overlap available: True
- Valid current-primary feature overlap rows: 0
- Current OOS feature overlap rows: 8
- Electron-positive current-retained OOS overlap rows: 1/5
- Best-axis current-retained OOS catches in extended surface: 2
- Best-axis catches already in acquisition queue: 0

## Acquisition Tranches

| tranche | retained OOS | primary | rows required | candidate rows now | max retained-OOS catches measurable |
| --- | ---: | ---: | ---: | ---: | ---: |
| top_1_retained_oos_plus_all_primary | 1 | 34 | 35 | 0 | 1 |
| top_2_retained_oos_plus_all_primary | 2 | 34 | 36 | 0 | 2 |
| top_5_retained_oos_plus_all_primary | 5 | 34 | 39 | 0 | 5 |
| top_10_retained_oos_plus_all_primary | 10 | 34 | 44 | 0 | 10 |
| top_20_retained_oos_plus_all_primary | 20 | 34 | 54 | 0 | 20 |
| top_40_retained_oos_plus_all_primary | 40 | 34 | 74 | 0 | 40 |

## Smallest Next Experiment

- Smoke tranche: top_1_retained_oos_plus_all_primary with 35 rows.
- Full retained-OOS tranche: top_40_retained_oos_plus_all_primary with 74 rows.
- Smoke tranche retained-OOS rows: m_csa:104
- Smoke tranche primary row count: 34

## Decision

- Measured train/cal signal available: True
- Smallest smoke tranche measurable now: False
- Full retained current split measurable now: False
- Adds operating-point value beyond current surface: False
- Deployable now: False
- Research-only: True
- Smallest next experiment: Acquire source-free electron-flow fields for the top 1 current-retained OOS row(s) and all 34 current primary rows, then rerun the train/cal projection and incremental readouts.
- Promotion gate: Require actual source-free electron-flow rows for all 40 retained-OOS priority rows and all 34 primary rows, followed by a fixed train/cal operating-point readout, before any heldout or deployment claim.

## Interpretation

- Research-only acquisition ceiling: electron-flow has measured train/cal OOS recall delta 0.142857, but the current source-free candidate surface covers 0/40 retained OOS rows and 0/34 primary rows, so no split-aligned operating-point value can be claimed yet.
- Run the 35-row source-free electron-flow smoke tranche first; only expand to the 74-row retained-OOS current-split tranche if the smoke tranche preserves primary retention and adds incremental OOS abstention.
