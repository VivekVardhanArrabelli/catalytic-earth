# Lever 2 Source-Free Electron-Flow Relaxed Non-PQQ Donor/Acceptor Feature Sidecar Readout - current702

Run: 2026-06-05T09:32:13Z

Lever 2 train/cal-disciplined source-free feature-sidecar readout for a fixed relaxed non-PQQ donor/acceptor electron-flow distance primitive on the current split. It consumes the measured broad redox-center donor/acceptor rows, emits standalone normal-shaped row_specific_event_features for the 34 current primary rows and 40 current-retained OOS rows, and measures a fixed 8 A gate. It does not train, tune thresholds, read heldout, edit registries, or promote imports.

## Status

- lever2_source_free_electron_flow_relaxed_non_pqq_donor_acceptor_feature_sidecar_readout_research_only_fixed_relaxed_non_pqq_distance_operating_point_signal
- Result class: research_only_fixed_relaxed_non_pqq_distance_operating_point_signal
- Materialized feature rows complete: 74/74
- Current primary/OOS positives: 0/2
- Primary retain recall: 1.0
- Retained-OOS abstain recall: 0.05
- Incremental OOS recall vs current geometry/fold OOS: 0.026667
- Union OOS recall: 0.493333
- Projection-row positives: 2
- Forbidden row-feature key hits: 0

## Fixed Gate

| rows complete | primary positives | retained-OOS positives | primary retain | retained-OOS recall | union OOS recall |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 74/74 | 0 | 2 | 1.0 | 0.05 | 0.493333 |

## Positive Feature Rows

| row | role | count | min distance | families | coordinate evidence |
| --- | --- | ---: | ---: | --- | --- |
| m_csa:119 | current_retained_oos | 1 | 5.054 | iron_sulfur_or_iron | artifacts/v3_foldseek_coordinates_1000/pdb_2C3M.cif |
| m_csa:464 | current_retained_oos | 1 | 5.527 | nad | artifacts/v3_foldseek_coordinates_1000/pdb_1TEH.cif |

## Projection Scout

- Available: True
- Complete rows: 43/43
- Positive train/cal rows: 0/2
- Positive row IDs: m_csa:59, m_csa:256
- The fixed relaxed non-PQQ distance contract has source-free train/cal projection positives.

## Family Split

| candidate | primary positives | retained-OOS positives | projection positives | projection support | closest projection negative | retained-OOS rows |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| nad_family_only | 0 | 1 | 2 | True | none | m_csa:464 |
| iron_sulfur_or_iron_only | 0 | 1 | 0 | False | none | m_csa:119 |
| other_non_pqq_only | 0 | 0 | 0 | False | none | none |

- Current-split signal without projection support: [{'candidate_id': 'iron_sulfur_or_iron_only', 'retained_oos_positive_entry_ids': ['m_csa:119'], 'missing_source_free_evidence': 'positive train/cal projection rows for the same fixed family-specific 8 A source-free distance contract'}]

## Decision

- Standalone sidecar materialized: True
- Current-split sidecar complete: True
- Preserves primary retention: True
- Adds value beyond current geometry/fold: True
- Projection rows support fixed contract: True
- Deployable now: False
- Remaining gap: The fixed 8 A relaxed non-PQQ donor/acceptor distance contract is measured and primary-safe on the current split, but remains an unapproved research primitive and is not imported into the normal source-free train/cal feature sidecar.

## Interpretation

- The fixed 8 A relaxed non-PQQ donor/acceptor distance feature sidecar is complete on 74/74 current-split rows, preserves all current primary rows, and catches 2/40 current-retained OOS rows from normal-shaped row_specific_event_features.
- Keep this primitive research-only until explicitly approved, then test a union with the narrow PQQ donor/acceptor feature to measure the combined direct electron-flow operating point.
