# PLP Children Shard Handoff 20260608

- Automation ID: `ce-expansion-shard-plp-children`
- STARTED_AT_UTC: `2026-06-08T14:11:58Z`
- STARTED_AT_LOCAL: `Mon Jun  8 09:11:58 CDT 2026`
- ENDED_AT_UTC: `2026-06-08T14:24:20Z`
- ENDED_AT_LOCAL: `Mon Jun  8 09:24:20 CDT 2026`
- ELAPSED_MINUTES: `12.367`
- WRAP_DISK_FREE_GIB: `10.51`
- Lane lock: `/Users/vivekvardhanarrabelli/Documents/Codex/2026-05-08/check-out-careflly-u-can-use-2/catalytic-earth/.git/worktrees/catalytic-earth/ce-expansion-shard-plp-children.lock`
- Status: durable lane artifact/report generated and validated; commit/push/sync/release follow this handoff update.

## Outputs

- JSON artifact: `artifacts/v3_scaleout_plp_children_shard_current702_20260608.json`
- Markdown report: `work/scaleout_plp_children_shard_current702_20260608.md`
- Lane handoff: `work/handoff_plp_children_shard_20260608.md`

## Result

- Candidate rows: `442`
- `blocked_coordinate`: `2`
- `blocked_family_decision`: `2`
- `blocked_locator`: `90`
- `reject/OOS_preserve_signal`: `314`
- `review_only_evidence`: `34`

## Subfamily Coverage

- `aminotransferase`: `11`
- `beta_gamma_replacement`: `5`
- `cobalamin_boundary_oos_control`: `2`
- `cobalamin_only_boundary`: `2`
- `coupled_plp_adenosylcobalamin_aminomutase`: `1`
- `decarboxylase`: `3`
- `external_plp_aminotransferase_review`: `14`
- `geometry_retrieval_low_rank_oos_control`: `337`
- `geometry_retrieval_plp_boundary_oos_control`: `28`
- `geometry_retrieval_unassigned_plp_parent`: `11`
- `lyase_eliminase`: `9`
- `non_plp_aminomutase_boundary`: `1`
- `non_plp_racemase_oos_control`: `1`
- `non_plp_schiff_base_hard_negative`: `8`
- `plp_adjacent_boundary`: `7`
- `racemase_epimerase`: `2`

## Validation

- `python -m json.tool artifacts/v3_scaleout_plp_children_shard_current702_20260608.json`
- `custom row-contract validation: required row fields, allowed terminal states, no mechanism snippets/Rhea IDs, guardrails false for imports/registry edits`
- `git diff --check`
- `PYTHONPATH=src python -m catalytic_earth.cli validate`
- `git status path-scope guard: only lane-specific files changed`

## Guardrails

- No curated label registry edits, ontology edits, imports, train/test split changes, production threshold/model-weight changes, or heldout training/tuning.
- No mechanism snippets or Rhea IDs are emitted in candidate rows; display names are provenance-only fields.
- OOS/reject signal is preserved rather than promoted.

## Next Action

Merger lane should review blocked-family-decision rows first, then blocked-locator rows with local PLP/LLP or coupled cobalamin context. No direct registry import is authorized from this shard.
