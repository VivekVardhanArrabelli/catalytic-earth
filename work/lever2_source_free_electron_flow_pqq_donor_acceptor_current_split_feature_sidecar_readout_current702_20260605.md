# Lever 2 Source-Free Electron-Flow PQQ Donor/Acceptor Current-Split Feature Sidecar Readout - current702

Run: 2026-06-05T07:52:20Z

Lever 2 train/cal-disciplined source-free feature-sidecar materialization readout for the direct PQQ donor/acceptor electron-flow primitive on the current split. It consumes the measured donor/acceptor artifact, emits standalone normal-shaped row_specific_event_features for the 34 current primary rows and 40 current-retained OOS rows, then remeasures the fixed operating point from those feature rows. It does not train, tune thresholds, read heldout, edit registries, or promote imports.

## Status

- lever2_source_free_electron_flow_pqq_donor_acceptor_current_split_feature_sidecar_readout_research_only_materialized_feature_sidecar_operating_point_signal
- Result class: research_only_materialized_feature_sidecar_operating_point_signal
- Materialized feature rows complete: 74/74
- Current primary/OOS positives: 0/1
- Primary retain recall: 1.0
- Retained-OOS abstain recall: 0.025
- Incremental OOS recall vs current geometry/fold OOS: 0.013333
- Forbidden row-feature key hits: 0
- Primary-safe non-PQQ family-exclusion candidates with retained-OOS signal: 0
- Relaxed non-PQQ distance cutoff scout rows with primary-safe retained-OOS signal: 9

## Fixed Gate

| rows complete | primary positives | retained-OOS positives | primary retain | retained-OOS recall | union OOS recall |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 74/74 | 0 | 1 | 1.0 | 0.025 | 0.48 |

## Positive Feature Rows

| row | role | electron transfer count | coordinate evidence |
| --- | --- | ---: | --- |
| m_csa:104 | current_retained_oos | 1 | artifacts/v3_foldseek_coordinates_1000/pdb_1C9U.cif |

## Non-PQQ Family-Exclusion Scout

| candidate | families | primary positives | retained-OOS positives | primary retain | retained-OOS rows |
| --- | --- | ---: | ---: | ---: | --- |
| pqq_only_control | pqq | 0 | 1 | 1.0 | m_csa:104 |
| non_pqq_all_redox | flavin, heme, iron_sulfur_or_iron, nad, other | 6 | 0 | 0.823529 | none |
| non_pqq_excluding_heme_and_flavin_ligation | iron_sulfur_or_iron, nad, other | 0 | 0 | 1.0 | none |
| flavin_only | flavin | 3 | 0 | 0.911765 | none |
| heme_only | heme | 3 | 0 | 0.911765 | none |
| nad_family_only | nad | 0 | 0 | 1.0 | none |
| pqq_plus_non_pqq_excluding_heme_and_flavin_ligation | iron_sulfur_or_iron, nad, other, pqq | 0 | 1 | 1.0 | m_csa:104 |

- No predeclared non-PQQ donor/acceptor family filter adds a primary-safe current-retained OOS catch. Heme/flavin contacts are the measured primary leaks, and excluding them leaves no non-PQQ retained-OOS positives.

## Relaxed Non-PQQ Distance Scout

Scout only; the fixed donor/acceptor primitive above remains 3.2 A.

| candidate | cutoff | primary positives | retained-OOS positives | retained-OOS rows |
| --- | ---: | ---: | ---: | --- |
| non_pqq_excluding_heme_and_flavin_ligation | 8.0 | 0 | 2 | m_csa:464, m_csa:119 |
| non_pqq_excluding_heme_and_flavin_ligation | 12.0 | 0 | 2 | m_csa:464, m_csa:119 |
| non_pqq_excluding_heme_and_flavin_ligation | 25.0 | 0 | 2 | m_csa:464, m_csa:119 |
| nad_family_only | 8.0 | 0 | 1 | m_csa:464 |
| nad_family_only | 12.0 | 0 | 1 | m_csa:464 |
| nad_family_only | 25.0 | 0 | 1 | m_csa:464 |
| iron_sulfur_or_iron_only | 8.0 | 0 | 1 | m_csa:119 |
| iron_sulfur_or_iron_only | 12.0 | 0 | 1 | m_csa:119 |
| iron_sulfur_or_iron_only | 25.0 | 0 | 1 | m_csa:119 |

- Relaxed non-PQQ distance cutoffs can recover NAD/Fe-S retained-OOS rows while excluding the measured heme/flavin primary leaks, but this is scout-only distance expansion and not the fixed 3.2 A donor/acceptor contact primitive.

## Decision

- Standalone sidecar materialized: True
- Current-split sidecar complete: True
- Preserves primary retention: True
- Adds value beyond current geometry/fold: True
- PQQ projection rows have positive train/cal signal: False
- Non-PQQ family-exclusion scout adds primary-safe retained-OOS signal: False
- Relaxed non-PQQ distance scout finds primary-safe signal: True
- Deployable now: False
- Remaining gap: The current-split source-free feature sidecar rows are now materialized and primary-safe for the fixed PQQ donor/acceptor primitive, but the primitive contract remains unapproved and unimported. It also has no positive PQQ train/cal projection rows, so a model-style train/cal rerun would not reproduce the prior electron-flow projection ceiling.

## Interpretation

- The standalone current-split source-free feature sidecar is complete on 74/74 rows, preserves all current primary rows, and catches 1/40 current-retained OOS rows from normal-shaped row_specific_event_features.
- Treat the missing current-split-row blocker as closed for the narrow PQQ donor/acceptor primitive, but keep the route research-only until the primitive contract is explicitly approved or replaced by a primary-safe non-PQQ electron-flow primitive.
