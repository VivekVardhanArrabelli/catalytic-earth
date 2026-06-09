# External Materialization Admission Batch - current702

Run: 2026-06-09T01:36:27Z

Large-scale external materialization/admission batch across the validated 16-row queue and the 354-row provisional bulk queue. It preserves source provenance, checks duplicate/current702 conflicts, materializes supported AFDB/PDB coordinates into a review-only external bundle, writes review-only source-free locator sidecars, and emits only preview artifacts without touching production registries or audited locator directories.

## Terminal Counts

- Input rows: `370`
- Coordinate materialized: `337`
- Locator sidecar materialized: `333`
- Import-ready preview: `333`
- Repairable coordinate blockers: `0`
- Repairable locator blockers: `37`
- Duplicate/current-registry conflicts: `0`
- Family-decision blockers: `0`
- Reject/OOS preserve-signal: `0`
- Hard blockers: `0`

## Lane Counts

- PLP children: `{"import_ready_preview": 72, "repairable_locator_blocker": 20}`
- glycoside/nucleoside: `{"import_ready_preview": 43, "repairable_locator_blocker": 6}`
- metal hydrolase: `{"import_ready_preview": 15, "repairable_locator_blocker": 1}`
- near-orphan/no-reliable-structure: `{"import_ready_preview": 1}`
- phosphoryl transfer: `{"import_ready_preview": 88, "repairable_locator_blocker": 4}`
- radical-SAM/cobalamin: `{"import_ready_preview": 50, "repairable_locator_blocker": 5}`
- redox oxygen/sulfur: `{"import_ready_preview": 64, "repairable_locator_blocker": 1}`

## Import-Ready Preview

- Rows: `333`
- Preview artifact: `artifacts/v3_external_materialization_import_ready_preview_current702_20260608.json`

## Next Actions

- Non-ready rows keep their exact next action inline in the batch artifact.
- Import-ready preview rows remain preview-only; structural duplicate screening and explicit production authorization are still required outside this lane.
