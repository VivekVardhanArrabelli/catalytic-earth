# Silver Holo Coordinate Materialization

Run: 2026-06-14T17:22:23Z

Materializes verified local experimental-PDB coordinates for the silver-ready
queue. This is a provenance-only step: no geometry scoring is run and no tier is
changed.

## Result

- Silver-ready input rows: 260.
- Already verified local coordinates: 15.
- Reused existing artifact coordinates: 0.
- Fetched and materialized coordinates: 12.
- Registry coordinate updates staged: 12.
- Verified local coordinates after: 27.
- Deferred over fetch limit: 233.
- Existing local sha mismatches: 0.
- Fetched sha mismatches: 0.

## Guardrails

- Row count unchanged: True.
- Tier changed: False.
- Geometry confirmation run or faked: False.
- Coordinates are review-only provenance and are not predictive features.

## Next Action

- Apply the verified coordinate-path updates, rerun the silver geometry audit, then build explicit PDB chain/residue mappings before any geometry-confirmation or silver tier apply.
