# Label PDB-ID Backfill - UniProt xref provenance

Run: 2026-06-14T16:03:33Z

Backfills missing `evidence.structure_provenance.pdb_ids` from UniProt
`xref_pdb` cross-references. PDB IDs remain structure provenance for holo
confirmation and are never predictive features. No frozen current702 row is written.

## Result

- Expansion labels: 6862 (row count unchanged).
- Accessions queried: 500; UniProt records returned: 500.
- **Backfilled PDB rows this run: 187**.
- Already had PDB IDs: 1298.
- UniProt records without PDB xrefs: 313.
- Deferred over limit: 5064.
- Rows with PDB IDs after: 1485.

## Guardrails

- Frozen current702 preserved: True.
- Writes expansion registry only: True.
- Row count unchanged: True.
- PDB IDs are provenance, not predictive features; existing PDB IDs are preserved.

## Next action

- Review counts, then re-run with --apply to write only the external registry. Follow with holo structure promotion and bronze-silver promotion preview.
