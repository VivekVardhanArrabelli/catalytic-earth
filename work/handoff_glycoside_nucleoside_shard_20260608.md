# Glycoside / Nucleoside Shard Handoff

- Automation ID: `ce-expansion-shard-glycoside-nucleoside`
- STARTED_AT_UTC: `2026-06-08T14:12:10Z`
- STARTED_AT_LOCAL: `2026-06-08T09:12:10-0500`
- CREATED_UTC: `2026-06-08T14:24:20Z`
- ELAPSED_MINUTES_AT_HANDOFF_WRITE: `13.799`
- Lock: `/tmp/ce_scaleout_glycoside_nucleoside.lock.d`
- Status: lane artifact and report generated; commit/push/sync and lock release happen after validation wrap.

## Outputs

- JSON artifact: `artifacts/v3_scaleout_glycoside_nucleoside_shard_current702_20260608.json`
- Markdown report: `work/scaleout_glycoside_nucleoside_shard_current702_20260608.md`
- Lane handoff: `work/handoff_glycoside_nucleoside_shard_20260608.md`

## Summary

- Rows: `835`
- Validation passed: `True`
- Direct glycoside/nucleoside hydrolase lane rows: `102`
- Explicit nucleoside hydrolase reference controls: `3`
- TIM-barrel fold confounder rows: `7`
- Mechanistically distinct OOS rows: `233`
- Acquisition conversion overlays: `86`
- Supplemental evidence overlays: `84`

## Guardrails

- No label registry, ontology, import, split, model-weight, or production-threshold files were edited.
- No external fetch was performed in this shard.
- Mechanism text fields are not copied into rows; source names and candidate names are retained only as provenance/rationale.
- All rows carry source hashes, row context hashes, duplicate-screen axes, terminal state, confidence tier, and machine-actionable next step.

## Wrap Status

- Commit hash: recorded by git after this handoff is committed.
- Push/sync status: pending at handoff write.
- Lock release status: pending at handoff write.
