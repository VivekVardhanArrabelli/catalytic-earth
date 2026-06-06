# Lever 2 Source-Free Electron-Flow PQQ Donor/Acceptor Contact Readout - current702

Run: 2026-06-05T07:18:39Z

Lever 2 train/cal-disciplined operating-point readout for a research-only direct source-free PQQ donor/acceptor-capable atom contact field. It starts from the PQQ primitive-axis audit and requires a fixed PQQ O4/O5 atom to contact a fixed active-site N/O/S heavy atom within 3.2 A. It does not train, tune thresholds, read heldout, or promote a registry/import contract.

## Status

- lever2_source_free_electron_flow_pqq_donor_acceptor_contact_readout_research_only_pqq_donor_acceptor_contact_operating_point_signal
- Result class: research_only_pqq_donor_acceptor_contact_operating_point_signal
- Projection electron-flow OOS recall delta: 0.142857
- Full current-split donor/acceptor rows complete: 74/74
- Full current-split positives primary/OOS: 0/1
- Primary retain recall: 1.0
- Retained-OOS abstain recall: 0.025
- Incremental OOS recall vs current geometry/fold OOS: 0.013333
- Donor/acceptor positives beyond PQQ redox-center contact: 0
- PQQ redox-center positives not donor/acceptor: 0

## Fixed Gate Readouts

| tranche | rows complete | primary positives | retained-OOS positives | primary retain | retained-OOS recall |
| --- | ---: | ---: | ---: | ---: | ---: |
| smoke | 35/35 | 0 | 1 | 1.0 | 1.0 |
| full current split | 74/74 | 0 | 1 | 1.0 | 0.025 |

## Positive Donor/Acceptor Rows

| row | role | contact count | atom contact | coordinate path |
| --- | --- | ---: | --- | --- |
| m_csa:104 | current_retained_oos | 1 | O5 to ARG 228 NH1 at 2.768 A | artifacts/v3_foldseek_coordinates_1000/pdb_1C9U.cif |

## Comparison To PQQ Redox-Center Contact

- PQQ redox-center positives: ['m_csa:104']
- PQQ donor/acceptor positives: ['m_csa:104']
- Same positive IDs as PQQ redox-center contact: True

## Decision

- Current-split donor/acceptor sidecar complete: True
- Preserves primary retention: True
- Adds retained-OOS abstention: True
- Adds value beyond current geometry/fold: True
- Adds rows beyond PQQ redox-center contact: False
- Deployable now: False
- Remaining gap: The fixed PQQ donor/acceptor-capable contact field is measured and source-free on the current split, but it remains an unapproved narrow primitive and does not add rows beyond the existing PQQ redox-center contact candidate.

## Interpretation

- The fixed PQQ donor/acceptor-capable contact field is complete on 74/74 current-split rows, preserves all current primary rows, and catches 1/40 current-retained OOS rows.
- Decide whether the fixed PQQ O4/O5 to active-site N/O/S contact contract is acceptable as a primitive; if not, test the same donor/acceptor atom-contact rule on a minimal non-PQQ redox cofactor atomset.
