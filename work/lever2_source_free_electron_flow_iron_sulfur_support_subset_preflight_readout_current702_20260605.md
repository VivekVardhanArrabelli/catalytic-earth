# Lever 2 Source-Free Electron-Flow Fe-S/Iron Support-Subset Preflight Readout - current702

Run: 2026-06-05T14:53:00Z

Lever 2 train/cal-disciplined source-free Fe-S/iron support-subset preflight for the direct electron-flow route. It consumes the measured tiny-tranche approval-readiness readout, the measured current-split smoke materialization readout, and the fixed approval-qualified union readout to decide whether the remaining m_csa:119 increment is an operating-point failure or only an unapproved support-contract gap. It does not approve, import, tune, train, score heldout, edit registries, or promote any feature.

## Status

- lever2_source_free_electron_flow_iron_sulfur_support_subset_preflight_readout_research_only_fe_s_support_subset_preflight_positive_pending_predictive_import
- Result class: research_only_fe_s_support_subset_preflight_positive_pending_predictive_import
- Current split complete source-free rows: 74/74
- Tiny bundle-ready support subset rows: 2
- Expanded bundle-ready support subset rows: 8
- Supported-now retained-OOS positives: 2
- Approval-qualified retained-OOS positives: 3
- Fe-S incremental retained-OOS rows beyond PQQ+NAD: 1
- Forbidden row-feature key hits: 0

## Support Options

| option | rows | entry IDs | blocked only by gate/import | bundle blockers |
| --- | ---: | --- | --- | --- |
| selected tiny bundle-ready | 2 | m_csa:127, m_csa:281 | m_csa:127, m_csa:281 | m_csa:443 |
| expanded bundle-ready | 8 | m_csa:127, m_csa:281, m_csa:130, m_csa:398, m_csa:358, m_csa:108, m_csa:562, m_csa:276 | m_csa:127, m_csa:281, m_csa:130, m_csa:398, m_csa:358, m_csa:108, m_csa:562, m_csa:276 | m_csa:443, m_csa:208, m_csa:123, m_csa:212 |

## Fixed Operating Point

| route | primary positives | retained-OOS positives | union OOS recall |
| --- | ---: | ---: | ---: |
| supported PQQ+NAD now | 0 | 2 | 0.493333 |
| approval-qualified PQQ+NAD+Fe-S | 0 | 3 | 0.506667 |

- Incremental Fe-S rows if imported: m_csa:119
- Incremental OOS recall beyond PQQ+NAD: 0.013333

## Approved Sidecar Preflight

- Approved train/cal sidecar rows: 43
- Projection support rows present: m_csa:59, m_csa:256
- Selected Fe-S support rows present: none
- Current positive rows present: none
- Generic electron fields present: has_electron_transfer_event, electron_transfer_count
- Direct source-free component fields present: none

## Decision

- Current split operating point measured: True
- Selected support subset blocked only by predictive gate/import: True
- Approval-qualified union preserves primary retention if imported: True
- Approval-qualified union adds incremental OOS abstention if imported: True
- Base PQQ+NAD contract approved: False
- Approved sidecar missing direct source-free component fields: True
- Support-contract gap only: True
- Deployable now: False
- Remaining gap: The 74-row current-split electron-flow operating point is measured and the fixed PQQ+NAD+Fe-S/iron union would preserve primary retention while adding m_csa:119. The selected bundle-ready Fe-S/iron support rows remain unapproved: they need predictive_use_allowed=true plus approved train/cal feature-sidecar rows before the m_csa:119 increment can be counted as supported. For full deployability, the base projection-backed PQQ+NAD component contracts also remain research-only/unapproved. The approved train/cal feature sidecar contains the projection-support rows but lacks the direct source-free PQQ/NAD/Fe-S component fields and current positive rows; this preflight only isolates the Fe-S support gap for the m_csa:119 increment.
- Smallest next experiment: Approve/import the selected bundle-ready Fe-S/iron support subset (m_csa:127, m_csa:281) with predictive_use_allowed=true and explicit train/cal split assignment, then rerun the fixed PQQ+NAD+Fe-S/iron union. Do not change thresholds or use heldout rows.

## Interpretation

- The pending Fe-S/iron increment is not an operating-point failure. The selected bundle-ready source-free support subset (m_csa:127, m_csa:281) is blocked only by predictive-use approval/import, while the fixed approval-qualified union catches m_csa:119 with 0 current-primary positives. Full direct electron-flow deployability still needs approval/import of the base PQQ+NAD component contracts.
- Use this preflight as the import contract target for the bundle-ready support subset; repair the larger tiny-tranche bundle gap only if the approval contract requires all three tiny support rows.
