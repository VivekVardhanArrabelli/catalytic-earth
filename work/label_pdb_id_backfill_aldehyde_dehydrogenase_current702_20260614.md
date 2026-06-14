# ALDH PDB-ID Backfill Preview - UniProt xref provenance

Run: 2026-06-14T20:34:24Z

Scope: the 150 `aldehyde_dehydrogenase` rows added in the 2026-06-14 post-HAD lane.

No registry was written. PDB IDs remain structure provenance for holo confirmation and are never predictive features.

## Result

- ALDH rows examined: 150.
- Accessions queried: 123; UniProt records returned: 123.
- Backfilled PDB rows in preview: 0.
- Already had PDB IDs: 27.
- UniProt records without PDB xrefs: 123.
- Rows with PDB IDs after preview: 27.

## Next action

- If this preview reports backfills, adapt the full backfill tool to support a fingerprint filter or rerun the full writer when UniProt latency is stable, then apply only to the external registry with frozen current702 SHA verification.
