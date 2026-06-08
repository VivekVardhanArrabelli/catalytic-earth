# Metal Hydrolase Shard Handoff

- Automation ID: `ce-expansion-shard-metal-hydrolase`
- STARTED_AT_UTC: `2026-06-08T14:13:00Z`
- STARTED_AT_LOCAL: `2026-06-08T09:13:00-0500`
- ENDED_AT_UTC: `2026-06-08T14:27:04Z`
- ELAPSED_MINUTES: `14.067`
- Lock: `/tmp/ce_scaleout_metal_hydrolase_shard.lock`
- Status: durable lane artifact/report generated; candidate/evidence lane only.

## Outputs

- JSON: `artifacts/v3_scaleout_metal_hydrolase_shard_current702_20260608.json`
- Report: `work/scaleout_metal_hydrolase_shard_current702_20260608.md`
- Handoff: `work/handoff_metal_hydrolase_shard_20260608.md`

## Counts

- Candidate rows: `411`
- `blocked_coordinate`: 10
- `blocked_family_decision`: 2
- `blocked_locator`: 34
- `reject/OOS_preserve_signal`: 117
- `review_only_evidence`: 248

## Next Action

Main merger lane should review the metal hydrolase shard by subfamily and terminal state, then choose which source-free preflight, locator, coordinate, or family-decision queues to advance. Do not import from this shard directly.
