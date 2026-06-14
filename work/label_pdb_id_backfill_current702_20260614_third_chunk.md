# Label PDB-ID Backfill - UniProt xref provenance

Run: 2026-06-14T16:09:21Z

Backfills missing `evidence.structure_provenance.pdb_ids` from UniProt
`xref_pdb` cross-references. PDB IDs remain structure provenance for holo
confirmation and are never predictive features. No frozen current702 row is written.

## Result

- Expansion labels: 6862 (row count unchanged).
- Accessions queried: 1000; UniProt records returned: 1000.
- **Backfilled PDB rows this run: 332**.
- Already had PDB IDs: 1485.
- UniProt records without PDB xrefs: 668.
- Deferred over limit: 4377.
- Rows with PDB IDs after: 1817.

## Guardrails

- Frozen current702 preserved: True.
- Writes expansion registry only: True.
- Row count unchanged: True.
- PDB IDs are provenance, not predictive features; existing PDB IDs are preserved.

## Next action

- Review counts, then re-run with --apply to write only the external registry. Follow with holo structure promotion and bronze-silver promotion preview.
