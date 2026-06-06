# Fold-Augmented Confounded Proxy Train/Cal Unsupported-Geometry Coordinate Acquisition Manifest - current702

Run: 2026-06-03T19:08:59Z

Train/cal-only coordinate-acquisition manifest for the Lever 3 unsupported-geometry repair queue. It maps each repair row to an expected AFDB-v6 CIF request and exact local path, but it does not download coordinates, score rows, register a proxy axis, tune thresholds, read heldout rows, or count unsupported geometry as abstention evidence.

## Status

- fold_augmented_confounded_proxy_train_cal_unsupported_geometry_coordinate_acquisition_manifest_ready_for_locus_repair_audit
- Repair rows: 8
- Unique query accessions: 8
- Query coordinates observed: 8/8
- Ready to score now: 0
- Blockers: ['locus_repair_audit_not_rerun_after_coordinate_materialization']

## Decision

- Coordinate manifest ready for fetch: False
- Coordinate fetch still required: False
- Ready for locus-repair audit: True
- Score repair rows now: False
- New proxy axis ready now: False
- Next gate: Rerun the background-axis scout with the repaired local coordinates before registering any new proxy-axis contract.

## Missing Query Coordinates

| accession | rows | local path | URL |
| --- | --- | --- | --- |

## Interpretation

- 8 unsupported-geometry repair rows map to 8 unique AFDB-v6 query accessions.
- 0 query coordinate files are missing locally; no scoring or threshold read was performed.
- Rerun the repair/background scout gates against the now-local AFDB-v6 CIFs before any new proxy axis is registered.
