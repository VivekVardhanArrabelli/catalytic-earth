# Lever 2 Source-Free Electron-Flow Approval Import Candidate Sidecar Readout - current702

Run: 2026-06-05T20:48:18Z

Lever 2 measured readout for the collision-safe namespaced electron-flow candidate sidecar route. It materializes the 35-row smoke tranche and then the remaining current-split rows inside this research artifact only, reruns fixed written-sidecar-only gates, and leaves the canonical approved train/cal sidecar and all imports unchanged.

## Status

- lever2_source_free_electron_flow_approval_import_candidate_sidecar_readout_research_only_candidate_sidecar_smoke_written_gate_positive_full_expansion_positive
- Result class: research_only_candidate_sidecar_smoke_written_gate_positive_full_expansion_positive
- Candidate sidecar rows after smoke: 77
- Candidate sidecar rows after full current-split expansion: 116
- Smoke add/update rows: 34/1
- Remaining expansion rows after smoke: 39
- Critical violations: 0

## Candidate Smoke Gate

| rows complete | primary positives | retained-OOS positives | retained-OOS IDs | union OOS recall | matches prior |
| ---: | ---: | ---: | --- | ---: | --- |
| 35/35 | 0 | 1 | m_csa:104 | 0.48 | True |

## Candidate Full Gate

| rows complete | primary positives | retained-OOS positives | retained-OOS IDs | union OOS recall | matches prior |
| ---: | ---: | ---: | --- | ---: | --- |
| 74/74 | 0 | 3 | m_csa:104, m_csa:119, m_csa:464 | 0.506667 | True |

## Candidate Component Ablation

| ablation | components | retained-OOS IDs | primary positives | incremental OOS recall |
| --- | --- | --- | ---: | ---: |
| pqq_only | pqq | m_csa:104 | 0 | 0.013333 |
| nad_family_only | nad_family | m_csa:464 | 0 | 0.013333 |
| iron_sulfur_only | iron_sulfur | m_csa:119 | 0 | 0.013333 |
| pqq_plus_nad_family | nad_family, pqq | m_csa:104, m_csa:464 | 0 | 0.026667 |
| pqq_plus_nad_family_plus_iron_sulfur | iron_sulfur, nad_family, pqq | m_csa:104, m_csa:119, m_csa:464 | 0 | 0.04 |

## Decision

- Candidate smoke sidecar materialized inside artifact: True
- Smoke preserves primary retention: True
- Smoke catches m_csa:104: True
- Full gate preserves primary retention: True
- Full gate catches retained OOS: True
- Direct electron-flow adds operating-point value after candidate sidecar import: True
- Component ablation confirms PQQ/NAD/Fe-S direct signal: True
- Fe-S adds an incremental row beyond PQQ+NAD: True
- Canonical approved sidecar modified: False
- Protected surfaces modified: False
- Deployable now: False
- Remaining gap: The source-free namespaced electron-flow fields now have a written-sidecar-shaped train/cal readout in a candidate artifact. Canonical approved-sidecar import/promotion remains unexecuted because this run does not edit imports or protected surfaces.
- Smallest next experiment: If import edits are explicitly allowed in a future Lever 2 run, apply exactly this candidate smoke sidecar delta to the protected approved sidecar, rerun the written-sidecar-only smoke gate, then apply the remaining 39 current-split rows.

## Interpretation

- The candidate written-sidecar smoke gate preserves all current primary rows and abstains m_csa:104; the expanded candidate current-split gate preserves primary retention and abstains m_csa:104, m_csa:119, and m_csa:464 beyond the current geometry/fold surface.
- No blocker packet is needed: the remaining issue is policy, not missing source-free evidence. The exact candidate deltas are included for a future protected import-authorized run.
