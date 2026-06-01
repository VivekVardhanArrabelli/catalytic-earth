# Fold-Augmented Train/Cal OOS Negative Surface Blocker Resolution - current702

Run: 2026-06-01T07:12:19Z

Row-level blocker-resolution packet for calibration OOS negatives missing full fold-augmented channel scores.

## Status

- blocker_resolution_packet_ready
- Score-complete rows: 71 / 76
- Missing full-score rows: 5
- Rows with fold-only but no geometry: 4
- Blocker reason counts: {'alphafold_db_coordinate_unavailable': 1, 'experimental_geometry_not_ok:None': 1, 'experimental_geometry_not_ok:insufficient_resolved_residues': 1, 'not_m_csa_entry': 2}

## Blocker Rows

| Entry | accession | reason | fold TM available | recommended action |
| --- | --- | --- | ---: | --- |
| m_csa:78 | P23007 | alphafold_db_coordinate_unavailable | False | verify replacement accession or alternate local coordinate source; AFDB has no v1-v6 model for this accession |
| m_csa:204 | P10746 | experimental_geometry_not_ok:None | True | repair source geometry evidence or keep row excluded from geometry-calibrated OOS surface |
| m_csa:531 | P31572 | experimental_geometry_not_ok:insufficient_resolved_residues | True | repair source geometry evidence or keep row excluded from geometry-calibrated OOS surface |
| uniprot:P78549 | P78549 | not_m_csa_entry | True | provide an active-site residue sidecar for UniProt-only rows or score them in a fold-only negative surface |
| uniprot:Q3LXA3 | Q3LXA3 | not_m_csa_entry | True | provide an active-site residue sidecar for UniProt-only rows or score them in a fold-only negative surface |

## Interpretation

- The accession-compatible active-site mapping blockers are cleared; the remaining OOS calibration gap is source geometry, UniProt-only active-site sidecars, or AFDB coordinate availability.
- Resolve the remaining five blockers by sourcing/replacing the missing AFDB coordinate for `m_csa:78`, repairing source geometry for `m_csa:204` and `m_csa:531`, and adding UniProt-only active-site sidecars for `uniprot:P78549` and `uniprot:Q3LXA3`.
