# Label PDB-ID Backfill - UniProt xref provenance

Run: 2026-06-14T23:45:23Z

Backfills missing `evidence.structure_provenance.pdb_ids` from UniProt
`xref_pdb` cross-references. PDB IDs remain structure provenance for holo
confirmation and are never predictive features. No frozen current702 row is written.

## Result

- Expansion labels: 7420 (row count unchanged).
- Accessions queried: 150; UniProt records returned: 150.
- **Backfilled PDB rows this run: 0**.
- Already had PDB IDs: 2100.
- UniProt records without PDB xrefs: 150.
- Deferred over limit: 5170.
- Rows with PDB IDs after: 2100.

## Guardrails

- Frozen current702 preserved: True.
- Writes expansion registry only: True.
- Row count unchanged: True.
- PDB IDs are provenance, not predictive features; existing PDB IDs are preserved.

## Next action

- Review counts, then re-run with --apply to write only the external registry. Follow with holo structure promotion and bronze-silver promotion preview.
