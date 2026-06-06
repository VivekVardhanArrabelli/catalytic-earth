# Lever 2 Source-Free Electron-Flow Current-Split Row Gate Audit - current702

Run: 2026-06-06T02:40:46Z

Lever 2 measured row-level gate audit for the direct source-free electron-flow current-split delta. It consumes the protected import sequence preflight and source delta package, emits the smoke/remaining/full row gate matrices, and verifies that each direct event flag and count is component-consistent. It does not apply imports, edit approved sidecars, change thresholds, train models, read heldout, or touch labels, registries, ontologies, or Lever 3 surfaces.

## Status

- lever2_source_free_electron_flow_current_split_row_gate_audit_readout_research_only_current_split_row_gate_audit_operating_point_signal
- Result class: research_only_current_split_row_gate_audit_operating_point_signal
- Critical row violations: 0
- Protected imports executed: 0
- Approved sidecar rows written: 0
- Row gate matrix SHA-256: 98a5eb56d8c5cf28bba414f085fa4f3723ef65ce46c73007825b29acb3a8d5b1

## Row Gate Summary

| tranche | rows complete | primary positives | retained-OOS IDs | primary retain |
| --- | ---: | ---: | --- | ---: |
| smoke | 35/35 | 0 | m_csa:104 | 1.0 |
| remaining | 39/39 | 0 | m_csa:119, m_csa:464 | n/a |
| full current split | 74/74 | 0 | m_csa:104, m_csa:119, m_csa:464 | 1.0 |

## Component Positives

- PQQ: ['m_csa:104']
- NAD-family: ['m_csa:464']
- Fe-S/iron: ['m_csa:119']
- Field consistency violation rows: 0
- Field conflict rows: 0

## Full Positive Rows

| row | components | direct count | gate action |
| --- | --- | ---: | --- |
| m_csa:104 | pqq | 1 | would_abstain_retained_oos |
| m_csa:119 | iron_sulfur_or_iron | 1 | would_abstain_retained_oos |
| m_csa:464 | nad_family | 1 | would_abstain_retained_oos |

## Decision

- Row-level audit confirms operating-point value: True
- Smoke gate preserves primary retention: True
- Full gate preserves primary retention: True
- Full gate adds value beyond geometry/fold: True
- Direct fields are component-consistent: True
- Deployable now: False
- Remaining gap: The row-level source-free electron-flow gate is measured and primary-safe on the current train/cal split; protected import authorization remains absent.

## Interpretation

- The row-level direct source-free electron-flow matrix is complete for the 35-row smoke tranche and 74-row current split, preserves all 34 current primary rows, and catches m_csa:104, m_csa:119, and m_csa:464 as retained OOS rows.
- No source-free row evidence gap remains for the current train/cal split; the next experiment is protected smoke import authorization and rerun of this audit.
