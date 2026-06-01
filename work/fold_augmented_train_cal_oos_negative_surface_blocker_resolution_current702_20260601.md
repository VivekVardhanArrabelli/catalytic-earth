# Fold-Augmented Train/Cal OOS Negative Surface Blocker Resolution - current702

Run: 2026-06-01T05:21:04Z

Row-level blocker-resolution packet for calibration OOS negatives missing full fold-augmented channel scores.

## Status

- blocker_resolution_packet_ready
- Score-complete rows: 65 / 76
- Missing full-score rows: 11
- Rows with fold-only but no geometry: 10
- Blocker reason counts: {'alphafold_db_coordinate_unavailable': 1, 'experimental_geometry_not_ok:None': 1, 'experimental_geometry_not_ok:insufficient_resolved_residues': 1, 'missing_accession_compatible_sequence_positions': 6, 'not_m_csa_entry': 2}

## Blocker Rows

| Entry | accession | reason | fold TM available | recommended action |
| --- | --- | --- | ---: | --- |
| m_csa:57 | P13448 | missing_accession_compatible_sequence_positions | True | repair_or_add accession-compatible catalytic residue sequence-position mapping before predicted-geometry scoring |
| m_csa:78 | P23007 | alphafold_db_coordinate_unavailable | False | verify replacement accession or alternate local coordinate source; AFDB has no v1-v6 model for this accession |
| m_csa:106 | P21873 | missing_accession_compatible_sequence_positions | True | repair_or_add accession-compatible catalytic residue sequence-position mapping before predicted-geometry scoring |
| m_csa:178 | P00829 | missing_accession_compatible_sequence_positions | True | repair_or_add accession-compatible catalytic residue sequence-position mapping before predicted-geometry scoring |
| m_csa:204 | P10746 | experimental_geometry_not_ok:None | True | repair source geometry evidence or keep row excluded from geometry-calibrated OOS surface |
| m_csa:284 | O66186 | missing_accession_compatible_sequence_positions | True | repair_or_add accession-compatible catalytic residue sequence-position mapping before predicted-geometry scoring |
| m_csa:314 | Q06128 | missing_accession_compatible_sequence_positions | True | repair_or_add accession-compatible catalytic residue sequence-position mapping before predicted-geometry scoring |
| m_csa:503 | B9JNP7 | missing_accession_compatible_sequence_positions | True | repair_or_add accession-compatible catalytic residue sequence-position mapping before predicted-geometry scoring |
| m_csa:531 | P31572 | experimental_geometry_not_ok:insufficient_resolved_residues | True | repair source geometry evidence or keep row excluded from geometry-calibrated OOS surface |
| uniprot:P78549 | P78549 | not_m_csa_entry | True | provide an active-site residue sidecar for UniProt-only rows or score them in a fold-only negative surface |
| uniprot:Q3LXA3 | Q3LXA3 | not_m_csa_entry | True | provide an active-site residue sidecar for UniProt-only rows or score them in a fold-only negative surface |

## Interpretation

- The remaining OOS calibration gap is mostly active-site mapping/geometry eligibility, not Foldseek runtime.
- Repair accession-compatible active-site mappings for the six m_csa rows first; then rerun the scorer and OOS-calibrated threshold contract.
