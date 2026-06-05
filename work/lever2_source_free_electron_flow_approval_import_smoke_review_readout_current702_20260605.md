# Lever 2 Source-Free Electron-Flow Approval Import Smoke Review Readout - current702

Run: 2026-06-05T18:44:05Z

Lever 2 measured smoke-review readout for the direct source-free electron-flow approval/import route. It consumes the committed approval/import dry-run artifact, isolates the smallest smoke tranche requested by the research loop (m_csa:104 plus the 34 current primary retention-gate rows), then measures the full 74-row current-split expansion in memory. It does not edit labels, registries, ontologies, imports, approved sidecars, predictive-use flags, production thresholds, model weights, or heldout splits.

## Status

- lever2_source_free_electron_flow_approval_import_smoke_review_readout_research_only_smoke_review_positive_full_expansion_positive_pending_protected_import
- Result class: research_only_smoke_review_positive_full_expansion_positive_pending_protected_import
- Smoke rows complete: 35/35
- Smoke primary/OOS positives: 0/1
- Smoke primary retain recall: 1.0
- Smoke incremental OOS recall vs current geometry/fold: 0.013333
- Full current-split rows complete: 74/74
- Full primary/OOS positives: 0/3
- Full incremental OOS recall vs current geometry/fold: 0.04
- Forbidden row-feature key hits: 0

## Smoke Gate

| rows complete | primary positives | retained-OOS positives | retained-OOS IDs | union OOS recall |
| ---: | ---: | ---: | --- | ---: |
| 35/35 | 0 | 1 | m_csa:104 | 0.48 |

## Full Expansion Gate

| rows complete | primary positives | retained-OOS positives | retained-OOS IDs | union OOS recall |
| ---: | ---: | ---: | --- | ---: |
| 74/74 | 0 | 3 | m_csa:104, m_csa:119, m_csa:464 | 0.506667 |

## Import Deltas

- Smoke rows new to approved sidecar: 34
- Smoke rows updating existing approved sidecar rows: 1
- Full rows new to approved sidecar: 73
- Full rows updating existing approved sidecar rows: 1

## Protected Steps

- approve the direct source-free PQQ/NAD/Fe-S component-field contract for train/cal use
- materialize the 35-row smoke tranche first: m_csa:104 plus the 34 current primary retention-gate rows
- rerun the approved-sidecar-only smoke gate and require primary retain recall 1.0 with m_csa:104 abstained
- if smoke passes, expand the same component fields to the remaining 39 current-split rows and the four support rows from the 78-row dry-run import set

## Decision

- Smoke tranche measured: True
- Smoke preserves primary retention: True
- Smoke catches m_csa:104: True
- Full expansion preserves primary retention: True
- Direct electron-flow adds value beyond current geometry/fold: True
- Protected surfaces modified: False
- Deployable now: False
- Remaining gap: approve the direct source-free PQQ/NAD/Fe-S component-field contract for train/cal use; materialize the 35-row smoke tranche first: m_csa:104 plus the 34 current primary retention-gate rows; rerun the approved-sidecar-only smoke gate and require primary retain recall 1.0 with m_csa:104 abstained; if smoke passes, expand the same component fields to the remaining 39 current-split rows and the four support rows from the 78-row dry-run import set
- Smallest next experiment: Materialize only the 35-row smoke tranche into the protected approved train/cal feature sidecar, rerun the approved-sidecar-only smoke gate unchanged, and expand to the remaining current-split rows only if primary retention remains 1.0.

## Interpretation

- The 35-row smoke tranche is source-free complete, preserves all current primary retention-gate rows, and abstains m_csa:104 from direct PQQ electron-flow features. The same fixed component surface also remains positive on the full 74-row current split.
- Use the smoke tranche as the smallest protected materialization target; the exact protected-row deltas are included here and no protected surface was modified.
