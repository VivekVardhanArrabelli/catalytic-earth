# Fold-Augmented Confounded Proxy Current Unavailable Coordinate Reprobe - current702

Run: 2026-06-04T06:43:22Z

Current-run live AFDB-v6 coordinate availability reprobe for the four predicted-structure-unavailable rows in the Lever 3 protein-only-extended remaining combined-score blocker set. It records availability only and does not download coordinates, score rows, tune thresholds, or alter the audit surface.

## Status

- fold_augmented_confounded_proxy_current_unavailable_coordinate_reprobe_no_rows_cleared
- Probe rows: 4
- AFDB-v6 coordinate available rows: 0
- AFDB-v6 coordinate unavailable rows: 4
- UniProt records with AlphaFoldDB xrefs: 0
- UniProt records with secondary accessions: 3
- Secondary accession AFDB-v6 probes: 0/6 available
- Rows cleared by reprobe: 0
- Blockers: ['four_current_remaining_rows_still_afdb_v6_unavailable', 'no_coordinate_reprobe_rows_cleared', 'fixed_threshold_audit_still_blocked']

## Rows

| row | accession | AFDB-v6 HTTP | secondary AFDB-v6 | blocker cleared | missing evidence | next gate |
| --- | --- | ---: | --- | --- | --- | --- |
| m_csa:416 | P07071 | 404 | P07073:404, Q38428:404, Q9T0V5:404 | False | approved deployment-valid predicted-structure coordinate source | approve an alternate predicted-structure source or keep row blocked |
| m_csa:562 | P07658 | 404 | P78137:404, Q2M6M5:404 | False | approved deployment-valid predicted-structure coordinate source | approve an alternate predicted-structure source or keep row blocked |
| m_csa:586 | P00806 | 404 | Q38567:404 | False | approved deployment-valid predicted-structure coordinate source | approve an alternate predicted-structure source or keep row blocked |
| m_csa:637 | P04531 | 404 | none | False | approved deployment-valid predicted-structure coordinate source | approve an alternate predicted-structure source or keep row blocked |

## Decision

- Coordinate import authorized now: False
- Fixed-threshold audit ready to rerun now: False
- Apply or change threshold now: False
- Smallest next gate: Use an approved alternate deployment-valid predicted-structure source for each unavailable accession, or keep these rows outside the fixed-threshold audit surface.

## Interpretation

- The four current predicted-structure-unavailable Lever 3 blocker rows remain unavailable from direct AFDB-v6 CIF URLs.
- Direct HEAD probes on 2026-06-04 returned HTTP 404 for all four AFDB-v6 CIF URLs; current UniProt records expose no AlphaFoldDB cross-references for these accessions, and all six secondary-accession AFDB-v6 probes also returned 404.
- Find approved alternate predicted-structure evidence for P07071, P07658, P00806, and P04531, or keep those rows as disclosed full-channel blockers.
