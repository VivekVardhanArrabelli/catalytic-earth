# Lever 2 Source-Free Electron-Flow PQQ Current-Split Sidecar Readout - current702

Run: 2026-06-05T06:02:57Z

Lever 2 train/cal-disciplined operating-point readout for a research-only source-free PQQ/quinone redox-center current-split sidecar. It maps the prior atom-level PQQ redox-center contact audit into direct electron-flow fields for the 34 current primary rows and 40 current-retained OOS rows, then evaluates a fixed binary OR gate beyond the current geometry/fold surface. It does not train, tune thresholds, read heldout, or promote a registry/import contract.

## Status

- lever2_source_free_electron_flow_pqq_current_split_sidecar_readout_research_only_direct_pqq_sidecar_operating_point_signal
- Result class: research_only_direct_pqq_sidecar_operating_point_signal
- Projection electron-flow OOS recall delta: 0.142857
- Full current-split direct rows complete: 74/74
- Full current-split positives primary/OOS: 0/1
- Primary retain recall: 1.0
- Retained-OOS abstain recall: 0.025
- Incremental OOS recall vs current geometry/fold OOS: 0.013333
- Current-split sidecar overlap missing train/calibration rows: 10/32
- Projection-row PQQ scout complete/positive rows: 43/0

## Fixed Gate Readouts

| tranche | rows complete | primary positives | retained-OOS positives | primary retain | retained-OOS recall |
| --- | ---: | ---: | ---: | ---: | ---: |
| smoke | 35/35 | 0 | 1 | 1.0 | 1.0 |
| full current split | 74/74 | 0 | 1 | 1.0 | 0.025 |

## Positive Direct Sidecar Rows

| row | role | contact count | coordinate path |
| --- | --- | ---: | --- |
| m_csa:104 | current_retained_oos | 1 | artifacts/v3_foldseek_coordinates_1000/pdb_1C9U.cif |

## Decision

- Current-split sidecar complete: True
- Preserves primary retention: True
- Adds retained-OOS abstention: True
- Adds value beyond current geometry/fold: True
- Deployable now: False
- Model-style projection rerun ready now: True
- Projection rows have positive PQQ train/cal signal: False
- Remaining gap: The PQQ/quinone redox-center contact contract is measured and source-free on the current split, but it remains unapproved as a primitive electron-flow axis and has not been imported through the normal source-free feature materialization path.

## Interpretation

- Direct source-free PQQ redox-center fields are complete on 74/74 current-split rows, preserve all current primary rows, and catch 1/40 current-retained OOS rows.
- Resolve the primitive-axis contract: approve the PQQ/quinone redox-center field for normal source-free materialization, or test the smallest donor/acceptor contact primitive next.
