# Lever 2 Source-Free Electron-Flow Fe-S/Iron Approval-Qualified Union Readout - current702

Run: 2026-06-05T11:44:02Z

Lever 2 train/cal-disciplined source-free direct electron-flow readout that measures the supported-now PQQ+NAD route against an approval-qualified PQQ+NAD+Fe-S/iron union on the same 74-row current split. It consumes only prior source-free feature sidecars and the Fe-S/iron projection-support artifact; it does not approve, import, tune, train, score heldout, or promote any feature.

## Status

- lever2_source_free_electron_flow_iron_sulfur_approval_qualified_union_readout_research_only_approval_qualified_iron_sulfur_adds_incremental_signal_pending_feature_sidecar_approval
- Result class: research_only_approval_qualified_iron_sulfur_adds_incremental_signal_pending_feature_sidecar_approval
- Supported-now PQQ+NAD primary/OOS positives: 0/2
- Approval-qualified PQQ+NAD+Fe-S primary/OOS positives: 0/3
- Approval-qualified primary retain recall: 1.0
- Approval-qualified retained-OOS abstain recall: 0.075
- Incremental OOS recall vs current geometry/fold: 0.04
- Fe-S incremental retained-OOS rows beyond PQQ+NAD: 1
- Tiny projection tranche positives: 3/3

## Fixed Gates

| gate | complete | primary positives | retained-OOS positives | retained-OOS recall | union OOS recall |
| --- | ---: | ---: | ---: | ---: | ---: |
| supported PQQ+NAD | 74/74 | 0 | 2 | 0.05 | 0.493333 |
| approval-qualified PQQ+NAD+Fe-S | 74/74 | 0 | 3 | 0.075 | 0.506667 |

## Family Ablation

| component | primary positives | retained-OOS positives | positive rows |
| --- | ---: | ---: | --- |
| iron_sulfur_or_iron_distance_only | 0 | 1 | m_csa:119 |
| nad_family_distance_only | 0 | 1 | m_csa:464 |
| pqq_donor_acceptor_only | 0 | 1 | m_csa:104 |

## Fe-S Current Positives

| row | role | Fe-S count |
| --- | --- | ---: |
| m_csa:119 | current_retained_oos | 1 |

## Decision

- Supported PQQ+NAD adds value now: True
- Approval-qualified union adds value: True
- Fe-S adds OOS abstention beyond PQQ+NAD: True
- Tiny Fe-S projection tranche source-free positive: True
- Tiny Fe-S projection tranche consumable now: False
- m_csa:119 can join after tiny tranche approval: True
- Train/cal supported now: False
- Deployable now: False
- Remaining gap: The approval-qualified PQQ+NAD+Fe-S/iron union is measured, source-free, primary-safe, and incrementally catches m_csa:119 beyond the supported PQQ+NAD route, but the Fe-S/iron projection support rows are still not approved/imported and predictive_use_allowed remains false.
- Smallest next experiment: Approve/import the tiny Fe-S/iron projection tranche (m_csa:127, m_csa:281, m_csa:443) into the train/cal source-free feature sidecar with predictive_use_allowed true, then rerun this fixed union readout without threshold changes or heldout use.

## Interpretation

- The approval-qualified PQQ+NAD+Fe-S/iron union preserves the 34 current primary retention-gate rows, catches 3/40 current-retained OOS rows, and adds one Fe-S/iron OOS catch beyond the supported PQQ+NAD route.
- Keep PQQ+NAD as the supported measured route until the tiny Fe-S/iron projection tranche is approved/imported; after that, rerun this fixed union to decide promotion without changing thresholds.
