# Silver PDB Residue Mapping

Run: 2026-06-14T17:14:27Z

Maps exact UniProt active-site residues to explicit PDB chain/residue positions
through mmCIF alignment tables. This does not run geometry scoring or change
tiers.

## Result

- Silver-ready input rows: 260.
- Rows attempted with local coordinates: 2.
- Rows mapped: 1.
- Exact residues mapped: 2.
- Missing local coordinate: 256.
- Coordinate sha mismatch: 1.
- Missing mmCIF alignment tables: 1.
- No residue positions mapped: 0.

## Guardrails

- Row count unchanged: True.
- Tier changed: False.
- Geometry confirmation run or faked: False.
- Mappings are review-only provenance and are not predictive features.

## Next Action

- Apply verified mapping updates, rerun the silver geometry audit, then run the separate geometry confirmation gate only for rows that become runnable.
