# Lever 2 Source-Free Electron-Flow Projection-Backed PQQ+NAD Feature Sidecar Readout - current702

Run: 2026-06-05T10:48:30Z

Lever 2 train/cal-disciplined source-free feature-sidecar readout for the projection-backed direct electron-flow route: fixed PQQ donor/acceptor contact plus fixed 8 A NAD-family donor/acceptor distance. It consumes the measured combined direct readout, emits normal-shaped row_specific_event_features, excludes the unsupported Fe-S/iron current-split positive, and does not train, tune thresholds, read heldout, import features, or promote a primitive.

## Status

- lever2_source_free_electron_flow_projection_backed_pqq_nad_feature_sidecar_readout_research_only_projection_backed_pqq_nad_operating_point_signal
- Result class: research_only_projection_backed_pqq_nad_operating_point_signal
- Materialized feature rows complete: 74/74
- Current primary/OOS positives: 0/2
- Primary retain recall: 1.0
- Retained-OOS abstain recall: 0.05
- Incremental OOS recall vs current geometry/fold OOS: 0.026667
- Union OOS recall: 0.493333
- Combined projection positive rows: 2
- Unsupported Fe-S/iron positives excluded: 1

## Fixed Gate

| rows complete | primary positives | retained-OOS positives | primary retain | retained-OOS recall | union OOS recall |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 74/74 | 0 | 2 | 1.0 | 0.05 | 0.493333 |

## Positive Feature Rows

| row | role | count | PQQ | NAD-family |
| --- | --- | ---: | --- | --- |
| m_csa:104 | current_retained_oos | 1 | True | False |
| m_csa:464 | current_retained_oos | 1 | False | True |

## Projection Support

- PQQ projection positives: 0
- Relaxed non-PQQ projection positives: 2
- Combined projection positive row IDs: m_csa:59, m_csa:256
- Train/cal supports PQQ+NAD contract: True

## Decision

- Standalone sidecar materialized: True
- Current-split sidecar complete: True
- Preserves primary retention: True
- Adds value beyond current geometry/fold: True
- Projection rows support PQQ+NAD contract: True
- Unsupported Fe-S/iron positive excluded: True
- Deployable now: False
- Remaining gap: The projection-backed PQQ+NAD direct electron-flow sidecar is measured, source-free, and train/cal-supported by existing projection positives, but its component contracts remain research-only and unimported.

## Interpretation

- The projection-backed PQQ+NAD direct electron-flow feature sidecar is complete on 74/74 current-split rows, preserves all current primary rows, and catches 2/40 current-retained OOS rows.
- Keep this route research-only and use it as the supported comparison point while the Fe-S/iron projection-support gap is tested.
