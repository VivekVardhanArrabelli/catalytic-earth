# Radical SAM Cobalamin Shard Handoff

- Automation ID: `ce-expansion-shard-radical-sam-cobalamin`
- STARTED_AT_UTC: `2026-06-08T15:13:13Z`
- STARTED_AT_LOCAL: `2026-06-08T10:13:13-0500`
- ENDED_AT_UTC: `2026-06-08T15:28:57Z`
- ELAPSED_MINUTES: `15.733`
- Lock: `/tmp/ce_scaleout_radical_sam_cobalamin_current702.lock`
- Status: durable lane artifact/report generated; candidate/evidence lane only.

## Outputs

- JSON: `artifacts/v3_scaleout_radical_sam_cobalamin_shard_current702_20260608.json`
- Report: `work/scaleout_radical_sam_cobalamin_shard_current702_20260608.md`
- Handoff: `work/handoff_radical_sam_cobalamin_shard_20260608.md`

## Counts

- Candidate rows: `735`
- `blocked_coordinate`: 23
- `blocked_family_decision`: 21
- `reject/OOS_preserve_signal`: 681
- `review_only_evidence`: 10

## Next Action

Merger lane should review the radical/SAM/cobalamin shard by subfamily and terminal state, with special attention to CX3CX2C+SF4 external radical-SAM rows, cobalamin/AdoCbl locus rows, m_csa:737 coupled PLP-AdoCbl schema blocking, and near-OOD Fe-S controls. Do not import from this shard directly.
