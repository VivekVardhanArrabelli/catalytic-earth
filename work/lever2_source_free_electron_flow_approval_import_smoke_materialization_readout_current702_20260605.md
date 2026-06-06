# Lever 2 Source-Free Electron-Flow Approval Import Smoke Materialization Readout - current702

Run: 2026-06-05T19:50:35Z

Lever 2 measured readout for the approved-sidecar-shaped smoke materialization route. It consumes the prior smoke-review readout plus the current approved train/cal feature sidecar, simulates the 35-row protected smoke import in memory, and reruns the fixed approved-sidecar-only gate using only direct source-free electron-flow fields. It does not write approved sidecars, imports, labels, registries, ontologies, production thresholds, model weights, or heldout splits.

## Status

- lever2_source_free_electron_flow_approval_import_smoke_materialization_readout_research_only_collision_safe_namespaced_smoke_materialization_gate_positive_pending_protected_import
- Result class: research_only_collision_safe_namespaced_smoke_materialization_gate_positive_pending_protected_import
- Existing approved sidecar rows before smoke: 43
- Simulated approved sidecar rows after smoke: 77
- Smoke add/update rows: 34/1
- Approved-sidecar-only smoke complete rows: 35/35
- Approved-sidecar-only smoke primary/OOS positives: 0/1
- Approved-sidecar-only smoke primary retain recall: 1.0
- Approved-sidecar-only smoke incremental OOS recall vs current geometry/fold: 0.013333
- Remaining expansion rows after smoke: 39/39
- Forbidden/conflict hits: 0
- Generic direct-field conflicts avoided by namespaced route: 2

## Approved-Sidecar-Only Smoke Gate

| rows complete | primary positives | retained-OOS positives | retained-OOS IDs | union OOS recall | matches prior smoke |
| ---: | ---: | ---: | --- | ---: | --- |
| 35/35 | 0 | 1 | m_csa:104 | 0.48 | True |

## Collision-Safe Namespaced Smoke Gate

| rows complete | primary positives | retained-OOS positives | retained-OOS IDs | union OOS recall | matches prior smoke |
| ---: | ---: | ---: | --- | ---: | --- |
| 35/35 | 0 | 1 | m_csa:104 | 0.48 | True |

## Collision-Safe Full 74-Row Gate

| rows complete | primary positives | retained-OOS positives | retained-OOS IDs | union OOS recall |
| ---: | ---: | ---: | --- | ---: |
| 74/74 | 0 | 3 | m_csa:104, m_csa:119, m_csa:464 | 0.506667 |

## Remaining Expansion

- Remaining rows new to approved sidecar after smoke: 39
- Remaining rows updating existing approved sidecar after smoke: 0
- Remaining retained-OOS positives after smoke: m_csa:119, m_csa:464
- Full 74-row incremental OOS recall vs current geometry/fold: 0.04

| remaining row | role | components | electron-transfer count |
| --- | --- | --- | ---: |
| m_csa:119 | current_retained_oos | iron_sulfur | 1 |
| m_csa:464 | current_retained_oos | nad_family | 1 |

## Decision

- Approved-sidecar-shaped smoke materialization measured: True
- Approved-sidecar-only smoke gate matches prior smoke review: True
- Approved-sidecar-only smoke preserves primary retention: True
- Approved-sidecar-only smoke catches m_csa:104: True
- Smoke materialization has no direct feature conflicts: False
- Generic direct-field import has existing sidecar collisions: True
- Collision-safe namespaced smoke gate preserves primary retention: True
- Collision-safe namespaced smoke catches m_csa:104: True
- Collision-safe namespaced route ready for protected import: True
- Full 74-row expansion ready after smoke passes: True
- Collision-safe full 74-row gate preserves primary retention: True
- Collision-safe full 74-row gate catches retained OOS: True
- Collision-safe full 74-row gate has no direct feature conflicts: True
- Direct electron-flow adds value after smoke materialization: True
- Protected surfaces modified: False
- Deployable now: False
- Remaining gap: Execute the protected approval/import write for only the 35-row smoke tranche using collision-safe namespaced direct electron-transfer event fields, or explicitly approve overwriting the existing generic electron-transfer fields on m_csa:102; then rerun this same approved-sidecar-only gate against the written sidecar before expanding the remaining 39 current-split rows.
- Smallest next experiment: Protected-write only the 35-row smoke tranche into the approved train/cal feature sidecar with has_source_free_direct_electron_transfer_event and source_free_direct_electron_transfer_count as the collision-safe direct event fields, verify primary retain recall 1.0 and m_csa:104 abstention, then materialize the remaining 39 current-split rows.

## Interpretation

- The collision-safe namespaced approved-sidecar-shaped 35-row smoke materialization exactly reproduces the prior smoke gate from direct source-free electron-flow fields without overwriting existing generic electron-transfer fields, preserves all current primary rows, and abstains m_csa:104.
- The remaining step is protected approval/import execution for the 35-row smoke tranche with the collision-safe namespaced direct event fields; after that written-sidecar gate passes, the remaining 39 current-split rows carry complete direct fields for the 74-row expansion.
