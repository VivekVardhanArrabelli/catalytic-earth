# Lever 2 Source-Free Electron-Flow Combined Direct Feature Sidecar Readout - current702

Run: 2026-06-05T09:32:03Z

Lever 2 train/cal-disciplined source-free feature-sidecar readout for the union of two measured direct electron-flow features on the current split: fixed PQQ donor/acceptor contact and fixed 8 A relaxed non-PQQ donor/acceptor distance. It consumes only measured sidecar artifacts, emits normal-shaped row_specific_event_features, and does not train, tune thresholds, read heldout, edit registries, or promote imports.

## Status

- lever2_source_free_electron_flow_combined_direct_feature_sidecar_readout_research_only_combined_direct_electron_flow_operating_point_signal
- Result class: research_only_combined_direct_electron_flow_operating_point_signal
- Materialized feature rows complete: 74/74
- Current primary/OOS positives: 0/3
- Primary retain recall: 1.0
- Retained-OOS abstain recall: 0.075
- Incremental OOS recall vs current geometry/fold OOS: 0.04
- Union OOS recall: 0.506667
- Combined projection positive rows: 2

## Fixed Gate

| variant | rows complete | primary positives | retained-OOS positives | primary retain | retained-OOS recall | union OOS recall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| smoke m_csa:104+primary | 35/35 | 0 | 1 | 1.0 | 1.0 | None |
| combined direct union | 74/74 | 0 | 3 | 1.0 | 0.075 | 0.506667 |
| projection-backed PQQ+NAD | 74/74 | 0 | 2 | 1.0 | 0.05 | 0.493333 |

## Positive Feature Rows

| row | role | count | PQQ | relaxed non-PQQ |
| --- | --- | ---: | --- | --- |
| m_csa:104 | current_retained_oos | 1 | True | False |
| m_csa:119 | current_retained_oos | 1 | False | True |
| m_csa:464 | current_retained_oos | 1 | False | True |

## Projection Support

- PQQ projection positives: 0
- Relaxed non-PQQ projection positives: 2
- Combined projection positive row IDs: m_csa:59, m_csa:256
- Train/cal supports combined contract: True
- Projection-backed PQQ+NAD retained-OOS rows: m_csa:104, m_csa:464
- Unsupported relaxed non-PQQ positives: [{'entry_id': 'm_csa:119', 'current_split_role': 'current_retained_oos', 'unsupported_families': ['iron_sulfur_or_iron']}]

## Decision

- Standalone sidecar materialized: True
- Current-split sidecar complete: True
- Smoke tranche preserves primary retention: True
- Smoke tranche adds retained-OOS abstention: True
- Preserves primary retention: True
- Adds value beyond current geometry/fold: True
- Projection rows support combined contract: True
- Projection-backed PQQ+NAD adds value: True
- Deployable now: False
- Remaining gap: The combined direct electron-flow sidecar is measured and primary-safe on the current split, but both component contracts remain research-only and unimported.

## Interpretation

- The combined direct source-free electron-flow feature sidecar is complete on 74/74 current-split rows, preserves all current primary rows, and catches 3/40 current-retained OOS rows.
- Keep the union research-only; use the component rows to decide whether to approve the fixed non-PQQ distance contract as-is or split it into smaller NAD and Fe-S/iron source-free primitives.
