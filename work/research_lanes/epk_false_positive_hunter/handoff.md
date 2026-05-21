# ePK false-positive hunter handoff

- Last updated: 2026-05-21T22:20:48Z
- Started: 2026-05-21T21:32:24Z
- Ended: 2026-05-21T22:20:48Z
- Measured minutes: 48.40
- Primary outcome: regression_rows_emitted
- Pushed evidence commit: `41ef8a0b910eb9ab2bdb24fbb7674d82321df945` via alternate-index commit/push.
- Local checked-out HEAD remains behind origin because linked-worktree metadata writes are blocked.
- Rule under attack: metric-seeded biological-assembly/deposited-coordinate split sufficiency for review-only ePK materialization, plus the lane regression gate for ATPase/transporter/ORC-MCM/motor/same-chain/internal-fragment/ligand-materialization controls.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Continued the metric-seeded ligand-component split search after the previous run's ACP/DTP handoff. CIFs were fetched in memory only and reduced to compact evidence; no raw coordinate dumps were written.

- Older ACP/DTP retry/continuation artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_acp_dtp_older2_20260521_213224Z.json`
- Older DTP/ACP continuation artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_acp_dtp_older3_20260521_215200Z.json`
- ACP exhaustion artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_acp_older4_20260521_220000Z.json`
- Refreshed regression gate: `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_220200Z.json`

Reviewed surface this run:

- Older2: 220 IDs, 220 entry rows, 475 coordinate contexts, 0 fetch errors, 9 deposited-v4 entries, 5 metric non-ORC prefilter entries, 2 split contexts.
- Older3: 134 IDs, 134 entry rows, 316 coordinate contexts, 0 fetch errors, 5 deposited-v4 entries, 2 metric non-ORC prefilter entries, 0 split contexts.
- ACP older4: 37 IDs, 37 entry rows, 73 coordinate contexts, 0 fetch errors, 0 deposited-v4 entries, 0 metric non-ORC prefilter entries, 0 split contexts.

## Result

No new unsafe expected-policy ePK non-abstention was found.

- The prior `6FII` fetch error was recovered in the older2 shard; it was not a deposited-v4 split trap.
- The only new split contexts were `3PKP:biological_assembly_1` and `3PKP:biological_assembly_2`; both materializer checks abstained as `no_substrate_mode_materializer_hit_review_only`.
- Older3 exhausted DTP at the requested older offsets: `DTP:300:60` returned 10 IDs, while `DTP:360:60` and `DTP:420:60` returned 0.
- ACP older4 exhausted the visible older ACP tail: `ACP:480:60` returned 33 IDs, while `ACP:540:60` and `ACP:600:60` returned 0.
- Across this run's three shards, 7 deposited-v4 metric prefilter entries produced zero metric-seeded non-ORC split contexts and zero heteromeric split candidates.
- The refreshed regression gate emits 355 rows from 26 source artifacts.
- `unsafe_nonabstention_after_expected_policy_count` remains 0.
- `5UJ7:biological_assembly_1` remains the pinned context-v4-only biological-assembly split failure.
- `9FXK`, `6TXC`, `6TXE`, and `3PKP` now stand as metric-seeded assembly-below-floor abstention controls in the gate.

## Tooling Changes

- None in this run.

## Evidence For / Against

Evidence against this bounded ACP/DTP split-trap surface:

- 391 entry rows and 864 coordinate contexts across the three new shards produced zero unsafe materializer non-abstentions.
- The two `3PKP` split contexts abstained in the materializer.
- DTP was exhausted through the requested older continuation offsets, and ACP was exhausted through `ACP:600:60`.
- The 355-row regression gate kept expected-policy unsafe non-abstention at zero.

Evidence for continued search:

- `5UJ7:biological_assembly_1` still falsifies context-v4-only sufficiency and must stay pinned.
- Metric-seeded split abstention controls now include `9FXK`, `6TXC`, `6TXE`, and `3PKP`.
- Older ATP/ANP pages beyond current coverage remain open and should be the next bounded metric surface.

## Verification

- `python -m json.tool` for the three new metric artifacts and refreshed regression gate.
- JSONL parse validation for `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`.
- `git diff --check` over lane files changed this run.

## Blockers

- `git fetch origin` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git pull --ff-only origin research/epk-false-positive-hunter` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git fetch --no-write-fetch-head origin` succeeded.
- Normal `git add --dry-run` failed creating linked-worktree `index.lock`: Operation not permitted.
- Local checked-out HEAD remains behind origin because linked-worktree metadata writes are denied; commits were pushed with an alternate index.

## Next Query

Move from exhausted ACP/DTP pages to older ATP/ANP metric-seeded pages beyond the current coverage, for example `ATP:720:80`, `ATP:800:80`, `ATP:960:80`, `ANP:240:80`, `ANP:320:80`, and `ANP:400:80`, with all prior metric artifacts excluded. Continue only non-ORC deposited-v4 / biological-assembly-below-floor traps with `polymer_entity_count > 1` and local heteromeric geometry. Keep `5UJ7` pinned, preserve `9FXK`, `6TXC`/`6TXE`, and `3PKP` as abstention controls, and avoid production claims.

Production claims, label changes, threshold calibration, registry/fingerprint edits, artifact migrations, and production scoring remain forbidden.

## Files Changed

- `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_acp_dtp_older2_20260521_213224Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_acp_dtp_older3_20260521_215200Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_acp_older4_20260521_220000Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_220200Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`
