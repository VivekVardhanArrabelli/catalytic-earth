# Scale-out Merger/Repair Handoff - 20260608

- Automation ID: `ce-expansion-merger-qa`
- STARTED_AT_UTC: `2026-06-08T14:17:14Z`
- STARTED_AT_LOCAL: `2026-06-08T09:17:14-0500`
- RUN_ARTIFACT: `artifacts/v3_scaleout_locator_coordinate_repair_current702_20260608.json`
- RUN_REPORT: `work/scaleout_locator_coordinate_repair_current702_20260608.md`
- Lock: `/tmp/ce_scaleout_merger_repair_current702.lock`
- Source branch/head: `ce-expansion-merger-qa-20260608` / `fcee1b768934da05f9fc24ac8cc303fe8897b21a`
- Origin main at fetch: `ad12659099f3be62586378e60a3ca83e8889164b`
- Status: repair artifact/report produced; commit/push/sync and lock release are wrap steps.

## Mode

Fewer than three shard artifacts were available on `origin/main` or fetched origin branches, so no consolidated merger acceptance surface or import preview was built. This run stayed in the repair lane.

## Durable Repair

- Audited the seven `blocked_locator` rows from the current acquisition conversion artifact.
- Confirmed all seven have local AFDB coordinate files under `artifacts/v3_external_structural_coordinates_1025_all30/` and that their hashes match the structural-screen records.
- Left six rows as locator-blocked because no approved source-free active-site locator sidecar exists; within that queue, `uniprot:P60174` now has a source-backed locator-mapping preflight candidate from two local active-site feature positions mapped to AFDB residues 96/HIS and 166/GLU, but it still needs review before any sidecar copy.
- Recommended `uniprot:Q9BXS1` as `reject/OOS_preserve_signal` for future consolidated surfaces through source-free transitive structural duplicate evidence via `uniprot:Q13907` and current-countable `m_csa:190`.
- Performed no import, registry edit, threshold/model/split edit, or heldout training/tuning.

## Next Action

Future shard/merger runs should consume the repair artifact before building the consolidated acceptance surface. The remaining locator queue is `uniprot:O60568`, `uniprot:P29372`, `uniprot:P60174`, `uniprot:Q96I15`, `uniprot:A2RUC4`, and `uniprot:A5PLL7`; `uniprot:P60174` should be reviewed first because its two local active-site feature positions now map to AFDB residues 96/HIS and 166/GLU, while the others need explicit source-free active-site locator evidence, a sufficient source-backed locator decision, or approved terminal reject/OOS evidence before promotion or import preview.
