# Lever 2 Source-Free Electron-Flow Donor/Acceptor Contact Readout - current702

Run: 2026-06-05T07:18:50Z

Lever 2 train/cal-disciplined measured readout for a direct source-free electron-flow donor/acceptor contact primitive. The candidate field uses fixed PQQ O4/O5 ligand atoms, fixed active-site N/O/S donor-acceptor atoms, committed local CIF atom sites, and a fixed 3.2 A atom-contact cutoff on the 34 current primary rows and 40 current-retained OOS rows. It does not train, tune thresholds, read heldout, or promote a registry/import contract.

## Status

- lever2_source_free_electron_flow_donor_acceptor_contact_readout_research_only_direct_pqq_donor_acceptor_operating_point_signal
- Result class: research_only_direct_pqq_donor_acceptor_operating_point_signal
- PQQ donor/acceptor direct rows complete: 74/74
- PQQ donor/acceptor positives primary/OOS: 0/1
- Primary retain recall: 1.0
- Retained-OOS abstain recall: 0.025
- Incremental OOS recall vs current geometry/fold OOS: 0.013333
- Broad control positives primary/OOS: 6/1
- Projection-row scout PQQ/broad positives: 0/6
- PQQ cutoff scout finite rows/primary-safe expansion: 1/False

## Fixed Gate Readouts

| tranche | rows complete | primary positives | retained-OOS positives | primary retain | retained-OOS recall |
| --- | ---: | ---: | ---: | ---: | ---: |
| smoke PQQ donor/acceptor | 35/35 | 0 | 1 | 1.0 | 1.0 |
| full PQQ donor/acceptor | 74/74 | 0 | 1 | 1.0 | 0.025 |
| full broad control | 74/74 | 6 | 1 | 0.823529 | 0.025 |

## Organic Redox Family Controls

| control | primary positives | retained-OOS positives | primary retain | retained-OOS rows |
| --- | ---: | ---: | ---: | --- |
| nad_family_center_only | 0 | 0 | 1.0 | none |
| pqq_or_nad_family_center | 0 | 1 | 1.0 | m_csa:104 |
| pqq_or_organic_nonheme_center | 3 | 1 | 0.911765 | m_csa:104 |

## Broad Positive Family Audit

- Current-split broad positive families: {'flavin': 3, 'heme': 3, 'pqq': 1}
- Current-split broad positive split/role families: {'current_primary_retention_gate': {'flavin': 3, 'heme': 3}, 'current_retained_oos': {'pqq': 1}}
- Projection-row broad positive families: {'flavin': 2, 'heme': 3, 'nad': 1}
- Projection-row broad positive split families: {'calibration': {'flavin': 1, 'heme': 1, 'nad': 1}, 'train': {'flavin': 1, 'heme': 2}}

## Positive PQQ Donor/Acceptor Rows

| row | role | contact count | minimum distance | coordinate path |
| --- | --- | ---: | ---: | --- |
| m_csa:104 | current_retained_oos | 1 | 2.768 | artifacts/v3_foldseek_coordinates_1000/pdb_1C9U.cif |

## PQQ Cutoff Sensitivity Scout

- Scout only, not threshold selection: True
- Finite current-split PQQ donor/acceptor distance rows: 1
- Closest primary/OOS distance: None/2.768
- Primary-safe cutoffs adding rows beyond fixed 3.2 A: []
- No cutoff in the audited PQQ distance scout adds a current-split row beyond the fixed 3.2 A positive row while preserving primary retention.

## Decision

- Current-split PQQ donor/acceptor fields complete: True
- Preserves primary retention: True
- Adds retained-OOS abstention: True
- Adds value beyond current geometry/fold: True
- Broad control preserves primary retention: False
- Deployable now: False
- Remaining gap: The PQQ donor/acceptor contact primitive is measured and source-free on the current split, but it remains unapproved as a primitive electron-flow axis and has not been imported through the normal source-free feature materialization path.

## Interpretation

- The fixed PQQ O4/O5-to-active-site N/O/S donor/acceptor primitive is complete on 74/74 current-split rows, preserves all current primary rows, and catches 1/40 current-retained OOS rows. The broad redox-center donor/acceptor control is complete but hits 6 primary rows. PQQ+NAD-family center contacts add no retained-OOS rows beyond PQQ, NAD-family center contacts alone catch none, and organic non-heme center contacts leak into primary rows. Projection-row scout shows PQQ donor/acceptor has no positive train/cal rows, while broad redox donor/acceptor has train/cal positives but is not current-split primary-safe.
- Resolve whether the PQQ donor/acceptor contact contract is an approved source-free electron-flow primitive or remains a narrow research-only quinone subaxis; do not promote the broad control because it fails primary retention.
