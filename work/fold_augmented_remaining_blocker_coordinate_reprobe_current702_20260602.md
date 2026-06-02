# Fold-Augmented Remaining Blocker Coordinate Reprobe - current702

Run: 2026-06-02T08:39:22Z

Live coordinate-availability reprobe for the five remaining Lever 3 deployment blockers after the fold-only deployment contract no-go. This artifact records availability only; it imports no coordinates and changes no threshold or training surface.

## Status

- fold_augmented_remaining_blocker_coordinate_reprobe_no_rows_cleared
- Remaining blocker rows: 5
- Coordinate unavailable rows: 1
- Coordinate available but source-geometry blocked rows: 4
- Rows cleared by reprobe: 0
- P23007 UniProt AlphaFoldDB xrefs: none

## Rows

| row | accession | coordinate | blocker cleared | remaining blocker | next action |
| --- | --- | --- | --- | --- | --- |
| m_csa:78 | P23007 | False | False | alphafold_db_coordinate_unavailable | Find a source-backed alternate accession outside the current UniProt P23007 record, or keep this row outside the deployment-valid predicted fold channel. |
| m_csa:204 | P10746 | True | False | source active-site geometry evidence missing | Create a source-backed row-specific active-site residue or interaction sidecar before using the coordinate in the combined channel. |
| m_csa:531 | P31572 | True | False | source active-site geometry evidence insufficient | Source additional active-site residue or interaction evidence before using the coordinate in the combined channel. |
| uniprot:P78549 | P78549 | True | False | UniProt-only active-site sidecar missing | Create a source-backed UniProt-only active-site sidecar before using the coordinate in the combined channel. |
| uniprot:Q3LXA3 | Q3LXA3 | True | False | UniProt-only active-site sidecar missing | Create a source-backed UniProt-only active-site sidecar before using the coordinate in the combined channel. |

## Interpretation

- The live coordinate reprobe clears zero deployment blockers: P23007 still has no AFDB model through v7 and its current UniProt record has no AlphaFoldDB cross-reference; the other four rows remain blocked by source active-site geometry sidecars rather than coordinate availability.
- Continue Lever 3 by clearing source-backed active-site sidecars for P10746, P31572, P78549, and Q3LXA3, and by finding an alternate predicted coordinate policy or accession for P23007.
