# Lever 2 Source-Free Electron-Flow Smoke-Tranche Evidence Scan - current702

Run: 2026-06-05T02:46:15Z

Lever 2 measured evidence scan for the smallest source-free electron-flow smoke tranche. It verifies whether the direct source-free electron-flow fields required by the acquisition ceiling already exist in current candidate artifacts. It does not materialize features, infer labels, tune thresholds, score heldout, or promote deployment state.

## Status

- lever2_source_free_electron_flow_smoke_tranche_evidence_scan_research_only_smoke_tranche_evidence_gap
- Result class: research_only_smoke_tranche_evidence_gap
- Train/cal electron-flow OOS recall delta: 0.142857
- Smoke-tranche source-free rows complete now: 0/35
- Candidate projection rows in smoke tranche: 0/35
- Partial-surface rows still missing in smoke tranche: 35/35
- Rows with any source-free acquisition scaffold: 1/35

## Smoke Tranche

- Tranche: top_1_retained_oos_plus_all_primary
- Retained-OOS rows: 1
- Primary retention-gate rows: 34
- Required direct electron-flow fields: has_electron_transfer_event, electron_transfer_count

| row | role | candidate row | locator candidate | materialized locator | event-axis linker | complete electron-flow fields | missing fields |
| --- | --- | --- | --- | --- | --- | --- | --- |
| m_csa:104 | current_retained_oos | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:973 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:165 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:399 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:233 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:216 | current_primary_retention_gate | False | True | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:837 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:338 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:754 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:38 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:320 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:41 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:160 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:410 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:800 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:277 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:865 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:933 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:879 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:988 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:319 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:482 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:102 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:630 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:305 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:694 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:87 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:27 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:912 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:473 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:556 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:387 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:900 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:922 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |
| m_csa:173 | current_primary_retention_gate | False | False | False | False | False | has_electron_transfer_event, electron_transfer_count |

## Missing Evidence

| gap | required | valid now | missing now | why it matters |
| --- | ---: | ---: | ---: | --- |
| source_free_electron_flow_smoke_tranche_direct_fields | 35 | 0 | 35 | The smoke tranche is the smallest train/cal-disciplined experiment that can test whether electron-flow evidence adds current-split operating-point value. |
| source_free_electron_flow_smoke_tranche_primary_gate | 34 | 0 | 34 | Primary retention cost must be measurable before a mechanism-axis promotion or heldout read. |
| source_free_electron_flow_smoke_tranche_retained_oos | 1 | 0 | 1 | At least one current-retained OOS row is required to measure incremental abstention beyond geometry/fold. |

## Decision

- Smoke tranche measurable now: False
- Direct source-free electron-flow fields complete now: False
- Adds operating-point value beyond current surface: False
- Deployable now: False
- Research-only: True
- Smallest next experiment: Materialize direct source-free electron-flow fields has_electron_transfer_event and electron_transfer_count for 35 smoke-tranche rows, then rerun the train/cal projection and incremental readouts.
- Promotion gate: Require complete direct source-free electron-flow fields for the smoke tranche first; only expand to the full retained-OOS current split if the smoke readout preserves primary retention and adds incremental OOS abstention.

## Interpretation

- Research-only evidence gap: the smoke tranche retains the measured train/cal electron-flow delta 0.142857, but 0/35 rows currently have complete direct source-free electron-flow fields.
- Fill the two direct electron-flow fields on exactly the smoke-tranche rows before rerunning train/cal readouts; do not use partial locator/proton support as an electron-flow substitute.
