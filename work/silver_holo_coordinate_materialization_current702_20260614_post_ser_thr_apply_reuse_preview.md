# Silver Holo Coordinate Materialization

Run: 2026-06-14T23:44:53Z

Materializes verified local experimental-PDB coordinates for the silver-ready
queue. This is a provenance-only step: no geometry scoring is run and no tier is
changed.

## Result

- Silver-ready input rows: 202.
- Already verified local coordinates: 202.
- Reused existing artifact coordinates: 0.
- Fetched and materialized coordinates: 0.
- Registry coordinate updates staged: 0.
- Verified local coordinates after: 202.
- Deferred over fetch limit: 0.
- Existing local sha mismatches: 0.
- Fetched sha mismatches: 0.

## Guardrails

- Row count unchanged: True.
- Tier changed: False.
- Geometry confirmation run or faked: False.
- Coordinates are review-only provenance and are not predictive features.

## Next Action

- Apply the verified coordinate-path updates, rerun the silver geometry audit, then build explicit PDB chain/residue mappings before any geometry-confirmation or silver tier apply.
