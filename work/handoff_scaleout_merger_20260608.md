# Scale-out Merger/Repair Handoff - 20260608

- Automation ID: `ce-expansion-merger-qa`
- STARTED_AT_UTC: `2026-06-08T14:17:14Z`
- STARTED_AT_LOCAL: `2026-06-08T09:17:14-0500`
- ENDED_AT_UTC: `2026-06-08T14:52:33Z`
- ENDED_AT_LOCAL: `2026-06-08T09:52:33-0500`
- ELAPSED_MINUTES: `35.317`
- RUN_ARTIFACT: `artifacts/v3_scaleout_merged_acceptance_surface_current702_20260608.json`
- RUN_REPORT: `work/scaleout_merged_acceptance_surface_current702_20260608.md`
- REPAIR_ARTIFACT: `artifacts/v3_scaleout_locator_coordinate_repair_current702_20260608.json`
- REPAIR_REPORT: `work/scaleout_locator_coordinate_repair_current702_20260608.md`
- Lock: `/tmp/ce_scaleout_merger_repair_current702.lock`
- Source branch/head at merger assembly: `ce-expansion-merger-qa-20260608` / `a9a0c4af208151e346c0f42eb4842f681c982751`
- Origin main consumed: `5a915007d68d4df05f7d0b1f4eef6761357b7b63`
- Status: consolidated artifact/report produced and validation passed. Commit/push/sync, memory update, and lock release are final wrap steps recorded in the automation response.

## QA Rerun - 2026-06-08T15:16Z

- Automation ID: `ce-expansion-merger-qa`
- STARTED_AT_UTC: `2026-06-08T15:16:18Z`
- STARTED_AT_LOCAL: `2026-06-08T10:16:18-0500`
- ENDED_AT_UTC: `2026-06-08T15:21:12Z`
- ENDED_AT_LOCAL: `2026-06-08T10:21:12-0500`
- ELAPSED_MINUTES: `4.911`
- Source head checked: `main` / `3201971e1c1c7cc859f213bf34c8ec33f97ee95a`
- Lock: `/tmp/ce_scaleout_merger_repair_current702.lock`
- Result: existing consolidated surface and repair overlay were already present
  on `origin/main`; four shard artifacts were still available, no additional
  shard artifacts were present, and no new locator/coordinate/readiness repair
  work was found.
- QA confirmed: 2,058 shard rows, 1,116 canonical records, 516 current-registry
  overlap keys, seven repair-overlay rows consumed, and zero eligible
  import-preview candidates.
- Validation passed: JSON parse for the mandatory source/merged/repair
  artifacts, `git diff --check`, CLI validate, docs artifact-reference check
  with 0 missing references, and a custom merger partition/guardrail QA script.
- No import-preview artifact, registry edit, locator sidecar copy,
  threshold/model/split edit, or heldout training/tuning was performed.

## Mode

This run started in repair mode because fewer than three shard artifacts were
available at first. During wrap, `origin/main` advanced with four shard
artifacts, so the branch was rebased onto `origin/main` and the consolidated
merger surface was built from the current shard artifacts plus the repair
overlay.

## Durable Repair

- Audited the seven `blocked_locator` rows from the current acquisition conversion artifact.
- Confirmed all seven have local AFDB coordinate files under `artifacts/v3_external_structural_coordinates_1025_all30/` and that their hashes match the structural-screen records.
- Left six rows as locator-blocked because no approved source-free active-site locator sidecar exists; within that queue, `uniprot:P60174` now has a source-backed locator-mapping preflight candidate from two local active-site feature positions mapped to AFDB residues 96/HIS and 166/GLU, but it still needs review before any sidecar copy.
- Recommended `uniprot:Q9BXS1` as `reject/OOS_preserve_signal` for future consolidated surfaces through source-free transitive structural duplicate evidence via `uniprot:Q13907` and current-countable `m_csa:190`.
- Performed no import, registry edit, threshold/model/split edit, or heldout training/tuning.

## Consolidated Surface

- Consumed four shard artifacts:
  `artifacts/v3_scaleout_glycoside_nucleoside_shard_current702_20260608.json`,
  `artifacts/v3_scaleout_metal_hydrolase_shard_current702_20260608.json`,
  `artifacts/v3_scaleout_plp_children_shard_current702_20260608.json`, and
  `artifacts/v3_scaleout_redox_oxygen_sulfur_shard_current702_20260608.json`.
- Merged 2,058 shard source rows into 1,116 canonical candidate keys.
- Preserved source terminal counts:
  `reject/OOS_preserve_signal=784`, `review_only_evidence=808`,
  `blocked_locator=268`, `blocked_coordinate=135`,
  `blocked_family_decision=60`, and
  `countable_candidate_preflight_only=3`.
- Conservative canonical states:
  `reject/OOS_preserve_signal=583`, `review_only_evidence=284`,
  `blocked_locator=122`, `blocked_coordinate=68`,
  `blocked_family_decision=59`, and
  `countable_candidate_preflight_only=0`.
- No import-preview artifact was built because the three source
  preflight-only rows (`uniprot:P78549`, `m_csa:127`, and `m_csa:281`) all
  overlap current702 by exact/current-screen evidence and/or resolve to non-new
  canonical terminal states.
- Current-registry overlap records after separating structural neighbors from
  exact/current-screen overlap: 516.
- Deduplication records cover accession/candidate key, sequence-neighborhood,
  structure/fold cluster, ligand/cofactor/family lane, and current-registry
  overlap axes.

## Validation

- `python -m json.tool artifacts/v3_scaleout_merged_acceptance_surface_current702_20260608.json`: passed.
- `python -m json.tool artifacts/v3_scaleout_locator_coordinate_repair_current702_20260608.json`: passed.
- `git diff --check`: passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: passed with 702 curated mechanism labels.
- `PYTHONPATH=src python -m catalytic_earth.cli build-current-docs-artifact-reference-check`: missing 0.
- Custom merger guardrail assertions: passed.

## Next Action

Review `work/scaleout_merged_acceptance_surface_current702_20260608.md`,
especially `import_preview_decision`, `terminal_conflict_records`, and the
current-registry overlaps on `uniprot:P78549`, `m_csa:127`, and `m_csa:281`.
For locator repair follow-up, review `uniprot:P60174` first because its two
local active-site feature positions now map to AFDB residues 96/HIS and
166/GLU; the other remaining locator blockers need explicit source-free
active-site locator evidence, a sufficient source-backed locator decision, or
approved terminal reject/OOS evidence before promotion or import preview.
