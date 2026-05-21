# ePK false-positive hunter handoff

- Last updated: 2026-05-21T21:33:47Z
- Started: 2026-05-21T20:30:56Z
- Ended: 2026-05-21T21:33:47Z
- Measured minutes: 62.85
- Primary outcome: regression_rows_emitted
- Pushed evidence commit: `f8ad879d0cd9b4a57bab20a5d4d669fc0a2b97f9` via alternate-index commit/push.
- Local checked-out HEAD remains behind origin because linked-worktree metadata writes are blocked.
- Rule under attack: metric-seeded biological-assembly/deposited-coordinate split sufficiency for review-only ePK materialization, plus the lane regression gate for ATPase/transporter/ORC-MCM/motor/same-chain/internal-fragment/ligand-materialization controls.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Ran three bounded metric-seeded ligand continuation shards. CIFs were fetched in memory only and reduced to compact evidence; no raw coordinate dumps were written.

- Priority continuation artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_continuation3_20260521_203056Z.json`
- Older ACP/DTP artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_acp_dtp_older_20260521_204225Z.json`
- Second older ACP/DTP artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_acp_dtp_older2_20260521_210051Z.json`
- Refreshed regression gate: `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_213316Z.json`

Reviewed surface this run:

- Continuation3: 90 IDs, 90 entry rows, 193 coordinate contexts, 0 fetch errors, 9 deposited-v4 entries, 2 metric non-ORC prefilter entries, 8 split contexts.
- Older ACP/DTP shard 1: 180 IDs, 180 entry rows, 374 coordinate contexts, 0 fetch errors, 5 deposited-v4 entries, 3 metric non-ORC prefilter entries, 0 split contexts.
- Older ACP/DTP shard 2: 120 IDs, 119 entry rows, 252 coordinate contexts, 1 fetch error (`6FII`), 4 deposited-v4 entries, 3 metric non-ORC prefilter entries, 0 split contexts.

## Result

No new unsafe expected-policy ePK non-abstention was found.

- `9Y4F` and `9E5C` were recovered in continuation3; neither remained a fetch error.
- Continuation3 reached `DTP_recent_60` and found split contexts only for `6TXC` and `6TXE` assemblies 1-4.
- All eight `6TXC`/`6TXE` split contexts materializer-abstained as `no_substrate_mode_materializer_hit_review_only`.
- None of the new contexts were metric-seeded non-ORC deposited-v4/assembly-below-floor heteromeric candidates.
- The refreshed regression gate emits 353 rows from 23 source artifacts.
- `unsafe_nonabstention_after_expected_policy_count` remains 0.
- `5UJ7:biological_assembly_1` remains the pinned context-v4-only biological-assembly split failure.

## Tooling Changes

- `tools/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_stress.py` now supports repeatable `--extra-ligand-query name:ligand:start:rows` for explicit older ligand-component pages.

## Evidence For / Against

Evidence against this bounded split-trap surface:

- 390 unique-ID slots across the three shards yielded 389 reviewed entry rows and 819 coordinate contexts.
- Eight split contexts were reviewed through the materializer and all abstained.
- Eight deposited-v4 metric non-ORC prefilter entries across the shards produced zero metric-seeded non-ORC split contexts.
- The 353-row regression gate kept expected-policy unsafe non-abstention at zero.

Evidence for continued search:

- `6FII` remains a bounded fetch retry from older shard 2.
- Older shard 2 did not reach `DTP_recent_180`, `DTP_recent_240`, or `DTP_recent_300` before the 120-ID cap.
- `5UJ7:biological_assembly_1` still falsifies context-v4-only sufficiency and must stay pinned.
- `9FXK`, `6TXC`, and `6TXE` are useful assembly-below-floor abstention controls.

## Verification

- `python -m py_compile` for the changed metric helper.
- `python -m json.tool` for the new metric artifacts and regression gate.
- JSONL parse validation for `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`.
- `git diff --check` over lane files changed this run.

## Blockers

- `git fetch origin` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git pull --ff-only origin research/epk-false-positive-hunter` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git fetch --no-write-fetch-head origin` succeeded.
- Normal worktree status remains noisy with linked-worktree metadata/index drift.
- `6FII` remains a bounded older2 fetch error.
- `ps`/`pkill` process-list operations were denied while monitoring the slow older2 shard.

## Next Query

Retry `6FII` from `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_acp_dtp_older2_20260521_210051Z.json`, then continue explicit DTP older pages starting at `DTP:180:60`, `DTP:240:60`, and `DTP:300:60` with prior metric artifacts excluded. Add ACP 360+ only after DTP is exhausted. Keep `5UJ7` pinned, preserve `9FXK`/`6TXC`/`6TXE` as abstention controls, and avoid production claims.

Production claims, label changes, threshold calibration, registry/fingerprint edits, artifact migrations, and production scoring remain forbidden.

## Files Changed

- `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_continuation3_20260521_203056Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_acp_dtp_older_20260521_204225Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_acp_dtp_older2_20260521_210051Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_213316Z.json`
- `tools/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_stress.py`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`
