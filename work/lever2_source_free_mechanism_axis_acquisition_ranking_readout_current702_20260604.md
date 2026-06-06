# Lever 2 Source-Free Mechanism Axis Acquisition-Ranking Readout - current702

Run: 2026-06-05T01:52:59Z

Lever 2 measured train/cal ranking of missing source-free mechanism axes by operating-point value and evidence burden. It consumes the source-free projection readout plus candidate-surface field coverage, does not materialize mechanism rows, and does not read heldout, tune thresholds, or promote deployment state.

## Status

- lever2_source_free_mechanism_axis_acquisition_ranking_readout_research_only_axis_ranked_evidence_gap
- Result class: research_only_axis_ranked_evidence_gap
- Best genuine mechanism axis: electron_flow
- Best genuine-axis train/cal OOS recall delta: 0.142857
- Source-free ready genuine axes now: 0/3
- Current candidate overlap with primary rows: 0/34
- Current candidate overlap with calibration OOS rows: 0/75

## Axis Ranking

| axis | genuine mechanism | delta | AUC | added fields | value/field | ready now |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| electron_flow | True | 0.142857 | 0.870536 | 2 | 0.071429 | False |
| bond_change | True | 0.107143 | 0.790179 | 5 | 0.021429 | False |
| event_topology | True | 0.071429 | 0.803571 | 2 | 0.035715 | False |
| confidence_metadata | False | 0.142857 | 0.8125 | 4 | 0.035714 | False |
| active_site_locator_count | False | 0.035714 | 0.830357 | 2 | 0.017857 | False |

## Best Genuine Axis Evidence Burden

- Axis: electron_flow
- Added fields: electron_transfer_count, has_electron_transfer_event
- Candidate-surface missing field counts: {'electron_transfer_count': 53, 'has_electron_transfer_event': 53}

## Decision

- Best genuine axis has train/cal value: True
- Best genuine axis source-free ready now: False
- Current-split axis readout measurable now: False
- Adds operating-point value beyond current surface: False
- Deployable now: False
- Research-only: True
- Next gate: Prioritize the best genuine mechanism axis, electron_flow, only after direct source-free fields and current-split primary plus OOS rows are materialized; then rerun train/cal projection and fixed-threshold incremental readouts.

## Interpretation

- Research-only axis ranking: electron-flow is the best measured genuine missing mechanism axis by train/cal OOS-recall gain, with delta 0.142857, but no genuine mechanism axis is source-free ready on the current split.
- Materialize direct source-free electron-flow fields first; do not spend promotion effort on confidence metadata, and do not evaluate heldout until the current train/cal split is measurable.
