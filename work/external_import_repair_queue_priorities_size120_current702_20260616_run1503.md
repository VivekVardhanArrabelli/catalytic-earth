# External Import Repair Queue Priorities - current702 run1503

Created UTC: `2026-06-16T15:03:49Z`

This is a non-import planning note derived from
`artifacts/v3_external_import_review_repair_queue_size120_current702_20260616_run1503.json`.
It performs no registry edit, label import, coordinate download, model change, threshold change,
ontology edit, or split edit.

## Current Blocker State

- Repair queue rows: **636**
- Coordinate blockers: **473**
- Locator blockers: **121**
- Current702 duplicate conflicts: **13**
- External duplicate conflicts: **27**
- Hard blockers: **2**
- Disk free at this run: about **8 GiB**, below the **10 GiB** coordinate-download floor.

## Highest-Yield Repair Windows

| lane | blocker | rows | next action |
| --- | --- | ---: | --- |
| PLP children | `repairable_coordinate_blocker` | 106 | Restore disk above 10 GiB, then rerun coordinate materialization for this lane first. |
| phosphoryl transfer | `repairable_coordinate_blocker` | 105 | Restore disk above 10 GiB, then rerun coordinate materialization. |
| redox oxygen/sulfur | `repairable_coordinate_blocker` | 76 | Restore disk above 10 GiB, then rerun coordinate materialization. |
| radical-SAM/cobalamin | `repairable_coordinate_blocker` | 73 | Restore disk above 10 GiB, then rerun coordinate materialization. |
| near-orphan/no-reliable-structure | `repairable_locator_blocker` | 70 | Repair/rematerialize source-free locator sidecars before coordinate work. |
| glycoside/nucleoside | `repairable_coordinate_blocker` | 60 | Restore disk above 10 GiB, then rerun coordinate materialization. |
| glycoside/nucleoside | `repairable_locator_blocker` | 32 | Repair/rematerialize source-free locator sidecars. |
| metal hydrolase | `repairable_coordinate_blocker` | 31 | Lower priority because `metal_dependent_hydrolase` is already over cap. |

## Do Not Do

- Do not import the **197** controlled-review-ready rows without explicit controlled batch approval,
  label-factory decision, and production registry-change authorization.
- Do not start coordinate downloads while disk free is below **10 GiB**.
- Do not delete or move pre-existing large artifacts; the run1503 migration readiness plan
  authorizes **0** migrations/deletions.
