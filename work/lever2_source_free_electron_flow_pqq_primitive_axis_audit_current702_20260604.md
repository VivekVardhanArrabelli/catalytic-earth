# Lever 2 Source-Free Electron-Flow PQQ Primitive Axis Audit - current702

Run: 2026-06-05T04:48:58Z

Lever 2 train/cal-disciplined measured audit of a candidate source-free PQQ/quinone redox-center electron-flow field. The field uses only local coordinate ligand chemistry, fixed PQQ redox-center atom names, active-site atom contacts, and committed CIF sidecars; it does not use mechanism text, labels, EC/Rhea IDs, accessions, source IDs, target names, heldout rows, or threshold tuning.

## Status

- lever2_source_free_electron_flow_pqq_primitive_axis_audit_research_only_pqq_redox_center_candidate_axis_signal
- Result class: research_only_pqq_redox_center_candidate_axis_signal
- Train/cal electron-flow OOS recall delta: 0.142857
- Smoke PQQ redox-center rows complete: 35/35
- Smoke PQQ redox-center positives primary/OOS: 0/1
- Full current-split PQQ redox-center rows complete: 74/74
- Full current-split PQQ redox-center positives primary/OOS: 0/1
- Full current-split union control positives primary/OOS: 0/3

## Variant Readouts

| tranche | primary positives | retained-OOS positives | primary retain | OOS recall | complete rows |
| --- | ---: | ---: | ---: | ---: | ---: |
| smoke | 0 | 1 | 1.0 | 1.0 | 35/35 |
| full | 0 | 1 | 1.0 | 0.025 | 74/74 |

## Positive Atom-Level Evidence

| row | role | coordinate path | min PQQ-center distance | contact count |
| --- | --- | --- | ---: | ---: |
| m_csa:104 | current_retained_oos | artifacts/v3_foldseek_coordinates_1000/pdb_1C9U.cif | 2.768 | 1 |

## Research-Only Union Control

This control unions the atom-level PQQ candidate with the prior primary-safe generic coordinate redox-contact count threshold. It is not an approved primitive axis.

| threshold | primary positives | retained-OOS positives | retained-OOS rows |
| ---: | ---: | ---: | --- |
| 12 | 0 | 3 | m_csa:104, m_csa:368, m_csa:464 |

## Field Status Counts

| tranche | status | rows |
| --- | --- | ---: |
| smoke | complete_negative_no_proximal_pqq_coordinate_evidence | 34 |
| smoke | ok | 1 |
| full | complete_negative_from_gap_cif_inventory | 2 |
| full | complete_negative_no_proximal_pqq_coordinate_evidence | 71 |
| full | ok | 1 |

## Decision

- Full current-split fields complete: True
- Preserves primary retention: True
- Adds full current-split OOS abstention: True
- Deployable now: False
- Promotion gate: The atom-level PQQ redox-center contact field is a measured candidate source-free electron-flow subaxis. It should remain research-only until this narrow PQQ/quinone chemistry contract is explicitly approved as a primitive axis and imported through the normal source-free feature materialization path.

## Interpretation

- A fixed atom-level PQQ redox-center contact field is complete for the smoke tranche and the 74-row retained-OOS current split. It preserves all primary rows and catches the smoke retained-OOS row, yielding a sparse 1/40 retained-OOS full-split increment beyond the current geometry/fold surface. A research-only union with the prior primary-safe generic redox-contact count control would catch 3/40 retained-OOS rows at primary retain 1.0, but that control is not an approved primitive axis.
- Approve or reject the PQQ/quinone redox-center contact contract as a primitive source-free electron-flow subaxis; approval would make the next measurable step a fixed train/cal sidecar rerun, while rejection points to a donor/acceptor contact primitive.
