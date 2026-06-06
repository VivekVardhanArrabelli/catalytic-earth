# Lever 2 Source-Free Electron-Flow Current-Split Smoke Materialization Readout - current702

Run: 2026-06-05T13:47:14Z

Lever 2 train/cal-disciplined direct source-free electron-flow materialization readout for the smallest current-split smoke tranche. It measures m_csa:104 plus the 34 current primary retention-gate rows first, then reports the same fixed PQQ+NAD source-free feature fields on the 74-row retained current split. It consumes existing measured feature-sidecar readouts only and does not approve, import, tune, train, score heldout, or promote any feature.

## Status

- lever2_source_free_electron_flow_current_split_smoke_materialization_readout_research_only_source_free_smoke_tranche_measured_expands_to_74row_current_split_pending_contract_approval
- Result class: research_only_source_free_smoke_tranche_measured_expands_to_74row_current_split_pending_contract_approval
- Smoke rows complete: 35/35
- Smoke primary/OOS positives: 0/1
- Smoke primary retain recall: 1.0
- Smoke retained-OOS recall: 1.0
- Full current split rows complete: 74/74
- Full retained-OOS rows complete: 40/40
- Full current split primary/OOS positives: 0/2
- Full current split incremental OOS recall vs current geometry/fold: 0.026667
- Fe-S/iron incremental rows pending support: 1

## Fixed Gates

| tranche | rows complete | primary positives | retained-OOS positives | primary retain | retained-OOS recall | union OOS recall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| m_csa:104 + primary smoke | 35/35 | 0 | 1 | 1.0 | 1.0 | 0.48 |
| 74-row PQQ+NAD expansion | 74/74 | 0 | 2 | 1.0 | 0.05 | 0.493333 |

## Positive Rows

- Smoke retained-OOS positives: m_csa:104
- Full current-split retained-OOS positives: m_csa:104, m_csa:464
- Approval-qualified retained-OOS positives: m_csa:104, m_csa:119, m_csa:464

## Fe-S Expansion Context

- Approval-qualified union status: lever2_source_free_electron_flow_iron_sulfur_approval_qualified_union_readout_research_only_approval_qualified_iron_sulfur_adds_incremental_signal_pending_feature_sidecar_approval
- Fe-S incremental retained-OOS rows beyond PQQ+NAD: 1
- Train/cal supported now: False

## Decision

- Smoke materialized: True
- Smoke preserves primary retention: True
- Smoke catches m_csa:104: True
- Full 74-row expansion materialized: True
- Full expansion adds value beyond geometry/fold: True
- Retained-OOS expansion row matrix emitted: True
- Fe-S expansion pending support: True
- Deployable now: False
- Remaining gap: The source-free smoke tranche and PQQ+NAD 74-row expansion are measured and primary-safe, but the direct electron-flow contracts remain research-only and unimported. The Fe-S/iron incremental row remains blocked by support-row approval/import before it can join the supported route.
- Smallest next experiment: Treat the m_csa:104 plus 34-primary smoke tranche as materialized; rerun the 74-row current-split PQQ+NAD route as the measured expansion baseline, then approve/import the bundle-ready Fe-S/iron support subset before adding m_csa:119 to the supported direct electron-flow route.

## Interpretation

- The direct source-free electron-flow smoke tranche is complete on 35/35 rows, preserves all current primary rows, and catches m_csa:104. The same PQQ+NAD feature fields expand to 74/74 current-split rows and catch 2/40 retained OOS rows.
- Use this smoke readout as the measured source-free baseline; continue only with approval/import evidence for the direct electron-flow contracts, especially the bundle-ready Fe-S/iron support subset.
