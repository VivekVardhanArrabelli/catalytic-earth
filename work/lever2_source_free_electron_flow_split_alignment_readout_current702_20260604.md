# Lever 2 Source-Free Electron-Flow Split-Alignment Readout - current702

Run: 2026-06-04T15:47:44Z

Lever 2 measured train/cal readout for the source-free electron-flow repair axis, tied to the current geometry/fold calibration split. It consumes existing train/cal projection metrics and current-surface missing-row evidence, does not materialize features, and does not read or tune heldout.

## Status

- lever2_source_free_electron_flow_split_alignment_readout_research_only
- Result class: research_only
- Electron-flow train/cal OOS recall delta: 0.142857
- Best-axis new OOS catches on current geometry/fold OOS rows: 0/4
- Source-free candidate overlap with current calibration primary rows: 0/34
- Source-free candidate overlap with current calibration OOS rows: 0/75

## Measured Train/Cal Axis Readout

| variant | fields | primary retain | OOS abstain | AUC | threshold |
| --- | ---: | ---: | ---: | ---: | ---: |
| current projected subset | 4 | 1.0 | 0.642857 | 0.794643 | 0.40327957 |
| current + electron flow | 6 | 1.0 | 0.785714 | 0.870536 | 1.72848324 |
| full row-specific surface | 19 | 1.0 | 0.857143 | 0.875 | 3.21469422 |

## Raw Full-Sidecar Current-Surface Overlap

- Available: True
- Valid current-primary calibration-feature overlap rows: 0
- Current-primary rows excluded as mechanism train targets: 1
- Current-OOS calibration-feature overlap rows: 8
- Current-retained OOS overlap rows with electron transfer: 1/5

## Missing Split-Aligned Evidence

- Current-retained OOS rows missing electron-flow evidence: 40
- Current primary retention-gate rows missing electron-flow evidence: 34
- Already-abstained OOS rows missing electron-flow evidence: 27
- Candidate-surface overlap with retained OOS priority rows: 0

## Acquisition Priority Rows

| priority | row | class | accession | current score | candidate row exists |
| ---: | --- | --- | --- | ---: | --- |
| 1 | m_csa:104 | current_retained_oos_missing_electron_flow_axis | P13650 | 0.6498 | False |
| 1 | m_csa:483 | current_retained_oos_missing_electron_flow_axis | A9CEQ8 | 0.6341 | False |
| 1 | m_csa:52 | current_retained_oos_missing_electron_flow_axis | P0AB71 | 0.6154 | False |
| 1 | m_csa:464 | current_retained_oos_missing_electron_flow_axis | P11766 | 0.60295 | False |
| 1 | m_csa:415 | current_retained_oos_missing_electron_flow_axis | P22643 | 0.58595 | False |
| 1 | m_csa:471 | current_retained_oos_missing_electron_flow_axis | Q9GPQ4 | 0.5853 | False |
| 1 | m_csa:39 | current_retained_oos_missing_electron_flow_axis | Q27546 | 0.58215 | False |
| 1 | m_csa:271 | current_retained_oos_missing_electron_flow_axis | P56839 | 0.5757 | False |
| 1 | m_csa:622 | current_retained_oos_missing_electron_flow_axis | P31677 | 0.5615 | False |
| 1 | m_csa:54 | current_retained_oos_missing_electron_flow_axis | P24670 | 0.55665 | False |
| 1 | m_csa:503 | current_retained_oos_missing_electron_flow_axis | B9JNP7 | 0.55265 | False |
| 1 | m_csa:65 | current_retained_oos_missing_electron_flow_axis | P0A7D4 | 0.5474 | False |
| 1 | m_csa:646 | current_retained_oos_missing_electron_flow_axis | P31939 | 0.54185 | False |
| 1 | m_csa:542 | current_retained_oos_missing_electron_flow_axis | P38677 | 0.5365 | False |
| 1 | m_csa:243 | current_retained_oos_missing_electron_flow_axis | P0A794 | 0.53445 | False |
| 1 | m_csa:36 | current_retained_oos_missing_electron_flow_axis | Q60099 | 0.51785 | False |
| 1 | m_csa:136 | current_retained_oos_missing_electron_flow_axis | P22337 | 0.51505 | False |
| 1 | m_csa:126 | current_retained_oos_missing_electron_flow_axis | P12944 | 0.5127 | False |
| 1 | m_csa:285 | current_retained_oos_missing_electron_flow_axis | P21332 | 0.50825 | False |
| 1 | m_csa:106 | current_retained_oos_missing_electron_flow_axis | P21873 | 0.50535 | False |
| 1 | m_csa:35 | current_retained_oos_missing_electron_flow_axis | P00518 | 0.4967 | False |
| 1 | m_csa:390 | current_retained_oos_missing_electron_flow_axis | Q5EBY5 | 0.48795 | False |
| 1 | m_csa:325 | current_retained_oos_missing_electron_flow_axis | P38051 | 0.4878 | False |
| 1 | m_csa:537 | current_retained_oos_missing_electron_flow_axis | P9WN39 | 0.4835 | False |
| 1 | m_csa:61 | current_retained_oos_missing_electron_flow_axis | Q01468 | 0.4799 | False |
| 1 | m_csa:462 | current_retained_oos_missing_electron_flow_axis | P11064 | 0.4766 | False |
| 1 | m_csa:531 | current_retained_oos_missing_electron_flow_axis | P31572 | 0.4756 | False |
| 1 | m_csa:82 | current_retained_oos_missing_electron_flow_axis | P17169 | 0.47405 | False |
| 1 | m_csa:422 | current_retained_oos_missing_electron_flow_axis | P00722 | 0.47265 | False |
| 1 | m_csa:244 | current_retained_oos_missing_electron_flow_axis | Q13126 | 0.4724 | False |
| 1 | m_csa:299 | current_retained_oos_missing_electron_flow_axis | P0A6I6 | 0.4712 | False |
| 1 | m_csa:565 | current_retained_oos_missing_electron_flow_axis | Q58819 | 0.46835 | False |
| 1 | m_csa:547 | current_retained_oos_missing_electron_flow_axis | Q93099 | 0.46725 | False |
| 1 | m_csa:490 | current_retained_oos_missing_electron_flow_axis | P00374 | 0.4638 | False |
| 1 | m_csa:368 | current_retained_oos_missing_electron_flow_axis | P37747 | 0.4537 | False |
| 1 | m_csa:284 | current_retained_oos_missing_electron_flow_axis | O66186 | 0.45095 | False |
| 1 | m_csa:499 | current_retained_oos_missing_electron_flow_axis | Q05871 | 0.44955 | False |
| 1 | uniprot:Q3LXA3 | current_retained_oos_missing_electron_flow_axis | Q3LXA3 | 0.4483 | False |
| 1 | m_csa:119 | current_retained_oos_missing_electron_flow_axis | P94692 | 0.4463 | False |
| 1 | m_csa:295 | current_retained_oos_missing_electron_flow_axis | P06134 | 0.44365 | False |
| 2 | m_csa:973 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.41 | False |
| 2 | m_csa:165 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.42755 | False |
| 2 | m_csa:399 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.4405 | False |
| 2 | m_csa:233 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.44155 | False |
| 2 | m_csa:216 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.4682 | False |
| 2 | m_csa:837 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.46975 | False |
| 2 | m_csa:338 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.4806 | False |
| 2 | m_csa:754 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.51735 | False |
| 2 | m_csa:38 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.5219 | False |
| 2 | m_csa:320 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.54915 | False |
| 2 | m_csa:41 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.5508 | False |
| 2 | m_csa:160 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.5702 | False |
| 2 | m_csa:410 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.5715 | False |
| 2 | m_csa:800 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.57285 | False |
| 2 | m_csa:277 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.57485 | False |
| 2 | m_csa:865 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.57705 | False |
| 2 | m_csa:933 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.5803 | False |
| 2 | m_csa:879 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.5846 | False |
| 2 | m_csa:988 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.6095 | False |
| 2 | m_csa:319 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.62295 | False |
| 2 | m_csa:482 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.624 | False |
| 2 | m_csa:102 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.63105 | False |
| 2 | m_csa:630 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.6399 | False |
| 2 | m_csa:305 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.64755 | False |
| 2 | m_csa:694 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.6621 | False |
| 2 | m_csa:87 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.66345 | False |
| 2 | m_csa:27 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.6649 | False |
| 2 | m_csa:912 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.69605 | False |
| 2 | m_csa:473 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.7287 | False |
| 2 | m_csa:556 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.7384 | False |
| 2 | m_csa:387 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.86325 | False |
| 2 | m_csa:900 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.8844 | False |
| 2 | m_csa:922 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.89215 | False |
| 2 | m_csa:173 | current_primary_retention_gate_missing_electron_flow_axis | None | 0.8963 | False |
| 3 | m_csa:342 | already_abstained_oos_missing_electron_flow_axis | Q62651 | 0.43935 | False |
| 3 | m_csa:345 | already_abstained_oos_missing_electron_flow_axis | Q6NVY1 | 0.4383 | False |
| 3 | m_csa:347 | already_abstained_oos_missing_electron_flow_axis | O69762 | 0.4354 | False |
| 3 | m_csa:140 | already_abstained_oos_missing_electron_flow_axis | Q59490 | 0.4294 | False |
| 3 | m_csa:303 | already_abstained_oos_missing_electron_flow_axis | P0DJQ7 | 0.4257 | False |
| 3 | uniprot:P78549 | already_abstained_oos_missing_electron_flow_axis | P78549 | 0.42485 | False |
| ... | 21 additional rows |  |  |  |  |

## Raw Overlap OOS Rows

| row | current score | current abstains | has electron transfer | electron count |
| --- | ---: | --- | --- | ---: |
| m_csa:17 | 0.45885 | False | False | 0 |
| m_csa:25 | 0.6241 | False | False | 0 |
| m_csa:40 | 0.41725 | True | False | 0 |
| m_csa:78 | 0.4054 | True | False | 0 |
| m_csa:85 | 0.49955 | False | False | 0 |
| m_csa:149 | 0.37655 | True | False | 0 |
| m_csa:222 | 0.52675 | False | False | 0 |
| m_csa:246 | 0.5171 | False | True | 1 |

## Decision

- Electron-flow train/cal signal measured: True
- Split-aligned current-surface incremental readout measurable: False
- Adds operating-point value beyond current surface: False
- Deployable now: False
- Research-only: True
- Next gate: Materialize source-free electron-flow fields for the 40 current-retained OOS rows and 34 current calibration-primary rows first, then rerun the train/cal projection and fixed-threshold incremental readouts before any heldout or deployment claim.

## Interpretation

- Research-only: electron-flow is the best single missing source-free axis on the existing train/cal mechanism sidecar, adding 0.142857 OOS abstain recall versus the current projected subset, but its newly caught OOS rows overlap 0 current geometry/fold calibration-OOS rows.
- Acquire split-aligned source-free electron-flow evidence for the priority rows in this artifact; start with current-retained OOS rows, then primary retention-gate rows.
