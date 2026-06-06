# Lever 2 Source-Free Electron-Flow Current-Split Field-Sensitivity Readout - current702

Run: 2026-06-06T04:45:06Z

Lever 2 measured field-level sensitivity readout for the direct source-free electron-flow row-gate matrix. It tests the generic direct event flag/count fields and the component-specific flag/count fields on the current train/cal split without applying protected imports, editing approved sidecars, changing thresholds, training models, scoring heldout, or touching labels, registries, ontologies, or Lever 3 surfaces.

## Status

- lever2_source_free_electron_flow_current_split_field_sensitivity_readout_research_only_direct_source_free_electron_flow_field_sensitivity_signal
- Result class: research_only_direct_source_free_electron_flow_field_sensitivity_signal
- Critical violations: 0
- Protected imports executed: 0
- Approved sidecar rows written: 0

## Field Summary

- Field variants: 8
- Primary-safe field variants: True
- Field variants with full operating-point value: 8
- Direct generic fields recover full OR gate: True
- Component field union matches full positives: True
- Flag/count pairs consistent: True

## Field Variants

| field variant | field | group | full positives | full delta | smoke positives | smoke delta | primary positives |
| --- | --- | --- | --- | ---: | --- | ---: | ---: |
| direct_event_flag | has_source_free_direct_electron_transfer_event | direct_generic | m_csa:104, m_csa:119, m_csa:464 | 0.04 | m_csa:104 | 0.013333 | 0 |
| direct_event_count_ge_1 | source_free_direct_electron_transfer_count | direct_generic | m_csa:104, m_csa:119, m_csa:464 | 0.04 | m_csa:104 | 0.013333 | 0 |
| pqq_flag | has_source_free_pqq_donor_acceptor_contact | pqq | m_csa:104 | 0.013333 | m_csa:104 | 0.013333 | 0 |
| pqq_count_ge_1 | source_free_pqq_donor_acceptor_contact_count | pqq | m_csa:104 | 0.013333 | m_csa:104 | 0.013333 | 0 |
| nad_family_flag | has_source_free_nad_family_donor_acceptor_distance | nad_family | m_csa:464 | 0.013333 | none | 0.0 | 0 |
| nad_family_count_ge_1 | source_free_nad_family_donor_acceptor_distance_count | nad_family | m_csa:464 | 0.013333 | none | 0.0 | 0 |
| iron_sulfur_or_iron_flag | has_source_free_iron_sulfur_or_iron_donor_acceptor_distance | iron_sulfur_or_iron | m_csa:119 | 0.013333 | none | 0.0 | 0 |
| iron_sulfur_or_iron_count_ge_1 | source_free_iron_sulfur_or_iron_donor_acceptor_distance_count | iron_sulfur_or_iron | m_csa:119 | 0.013333 | none | 0.0 | 0 |

## Decision

- Field sensitivity measured: True
- Generic direct fields recover full signal: True
- Generic direct fields recover smoke signal: True
- Component fields recover all full positives: True
- Primary retention preserved for all fields: True
- Deployable now: False
- Remaining gap: No source-free electron-flow field evidence gap remains for the current train/cal split; the remaining gap is explicit protected import authorization and approved-sidecar rerun.

## Interpretation

- The generic direct source-free electron-transfer flag and count each recover the full 3-row operating-point signal; component fields are primary-safe and jointly recover the same retained-OOS positives.
- Treat the remaining gap as protected import authorization, not missing source-free electron-flow field evidence.
