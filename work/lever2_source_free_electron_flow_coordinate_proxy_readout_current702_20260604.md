# Lever 2 Source-Free Electron-Flow Coordinate Proxy Readout - current702

Run: 2026-06-05T03:59:01Z

Lever 2 train/cal-disciplined measured readout for coordinate-only electron-flow proxy fields on the 35-row smoke tranche and the 74-row retained-OOS current-split tranche. It uses local geometry ligand codes and active-site/pocket residue contacts only; it does not use mechanism text, labels, EC/Rhea IDs, accessions, source IDs, target names, heldout rows, or threshold tuning.

## Status

- lever2_source_free_electron_flow_coordinate_proxy_readout_research_only_coordinate_proxy_smoke_signal
- Result class: research_only_coordinate_proxy_smoke_signal
- Train/cal electron-flow OOS recall delta: 0.142857
- Smoke coordinate rows ready: 35/35
- Smoke generic redox positives primary/OOS: 10/1
- Smoke PQQ positives primary/OOS: 0/1
- Full coordinate rows ready: 72/74
- Full PQQ inventory rows covered after CIF gap probe: 74/74
- Full-tranche PQQ positives primary/OOS: 0/1
- Full gap CIF probe PQQ positives: 0

## Variant Readouts

| tranche | variant | primary positives | retained-OOS positives | primary retain | OOS recall |
| --- | --- | ---: | ---: | ---: | ---: |
| smoke | coordinate_redox_contact_binary | 10 | 1 | 0.705882 | 1.0 |
| smoke | coordinate_quinone_pqq_redox_binary | 0 | 1 | 1.0 | 1.0 |
| smoke | coordinate_redox_contact_primary_safe_count_threshold | 0 | 0 | 1.0 | 0.0 |
| full_retained_current_split | coordinate_redox_contact_binary | 10 | 4 | 0.705882 | 0.1 |
| full_retained_current_split | coordinate_quinone_pqq_redox_binary | 0 | 1 | 1.0 | 0.025 |
| full_retained_current_split | coordinate_redox_contact_primary_safe_count_threshold | 0 | 2 | 1.0 | 0.05 |

## Smoke Rows

| row | role | redox ligands | PQQ | generic count |
| --- | --- | --- | ---: | ---: |
| m_csa:104 | current_retained_oos | PQQ | True | 8 |
| m_csa:973 | current_primary_retention_gate | FMN | False | 11 |
| m_csa:165 | current_primary_retention_gate | none | False | 0 |
| m_csa:399 | current_primary_retention_gate | HEM | False | 5 |
| m_csa:233 | current_primary_retention_gate | none | False | 0 |
| m_csa:216 | current_primary_retention_gate | none | False | 0 |
| m_csa:837 | current_primary_retention_gate | none | False | 0 |
| m_csa:338 | current_primary_retention_gate | none | False | 0 |
| m_csa:754 | current_primary_retention_gate | none | False | 0 |
| m_csa:38 | current_primary_retention_gate | none | False | 0 |
| m_csa:320 | current_primary_retention_gate | FAD | False | 5 |
| m_csa:41 | current_primary_retention_gate | none | False | 0 |
| m_csa:160 | current_primary_retention_gate | none | False | 0 |
| m_csa:410 | current_primary_retention_gate | none | False | 0 |
| m_csa:800 | current_primary_retention_gate | FMN | False | 5 |
| m_csa:277 | current_primary_retention_gate | FAD | False | 5 |
| m_csa:865 | current_primary_retention_gate | none | False | 0 |
| m_csa:933 | current_primary_retention_gate | none | False | 0 |
| m_csa:879 | current_primary_retention_gate | FAD | False | 8 |
| m_csa:988 | current_primary_retention_gate | none | False | 0 |
| m_csa:319 | current_primary_retention_gate | FMN | False | 6 |
| m_csa:482 | current_primary_retention_gate | none | False | 0 |
| m_csa:102 | current_primary_retention_gate | FMN | False | 4 |
| m_csa:630 | current_primary_retention_gate | none | False | 0 |
| m_csa:305 | current_primary_retention_gate | none | False | 0 |
| m_csa:694 | current_primary_retention_gate | HEM | False | 4 |
| m_csa:87 | current_primary_retention_gate | none | False | 0 |
| m_csa:27 | current_primary_retention_gate | none | False | 0 |
| m_csa:912 | current_primary_retention_gate | none | False | 0 |
| m_csa:473 | current_primary_retention_gate | HEM | False | 4 |
| m_csa:556 | current_primary_retention_gate | none | False | 0 |
| m_csa:387 | current_primary_retention_gate | none | False | 0 |
| m_csa:900 | current_primary_retention_gate | none | False | 0 |
| m_csa:922 | current_primary_retention_gate | none | False | 0 |
| m_csa:173 | current_primary_retention_gate | none | False | 0 |

## Full-Tranche Coordinate Gaps

| row | role | geometry status | diagnostic PDB |
| --- | --- | --- | --- |
| m_csa:531 | current_retained_oos | insufficient_resolved_residues | 1XVT |
| uniprot:Q3LXA3 | current_retained_oos | missing_geometry_row | none |

## Full-Tranche Gap CIF Probe

Supplemental source-free ligand-inventory scan of committed local CIF sidecars for full-tranche rows whose geometry readout was not ok. It can close absent-PQQ inventory as negative evidence, but it does not infer active-site proximity or promote a primitive electron-flow axis.

| row | sidecar status | structure ligands | redox ligands | PQQ |
| --- | --- | --- | --- | ---: |
| m_csa:531 | ok | COA, MSE | none | False |
| uniprot:Q3LXA3 | ok | none | none | False |

## Decision

- Coordinate proxy smoke measurable now: True
- PQQ coordinate subfield adds smoke OOS abstention at primary retain 1.0: True
- Deployable now: False
- Promotion gate: Treat the PQQ smoke signal as a coordinate-only electron-flow proxy until the source-free electron-flow primitive axis is explicitly reviewed and materialized for the full retained-OOS current split.

## Interpretation

- Coordinate-only PQQ redox evidence catches the smoke retained OOS row while preserving all primary rows, but the generic redox-contact proxy does not preserve primary retention at a binary operating point. The signal is research-only until the primitive source-free electron-flow axis is explicitly materialized and reviewed.
- Expand this coordinate-electron-flow materialization toward the full 74-row retained-OOS current split and resolve whether PQQ/quinone redox evidence is an approved primitive electron-flow subaxis or only a narrow ligand proxy.
