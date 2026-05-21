# ePK false-positive hunter handoff

- Last updated: 2026-05-21T20:27:02Z
- Started: 2026-05-21T19:28:57Z
- Ended: 2026-05-21T20:27:02Z
- Measured minutes: 58.08
- Primary outcome: regression_rows_emitted
- Pushed evidence commit: `c863816594c1a0007a7da932d69c56f3feb5e5ad` via alternate-index commit/push
- Local checked-out HEAD remains behind origin because linked-worktree metadata writes are blocked.
- Rule under attack: metric-seeded biological-assembly/deposited-coordinate split sufficiency for review-only ePK materialization, plus the lane regression gate for ATPase/transporter/ORC-MCM/motor/same-chain/internal-fragment/ligand-materialization controls.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Ran a priority retry of the prior metric fetch-error queue, then two bounded metric-seeded ligand continuation shards. CIFs were fetched in memory only and reduced to compact evidence; no raw coordinate dumps were written.

- Priority fetch-error retry artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_fetch_error_retry_20260521_192857Z.json`
- Main continuation artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_retry3_20260521_192857Z.json`
- Second continuation artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_continuation2_20260521_201017Z.json`
- Refreshed regression gate: `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_202430Z.json`

Reviewed surface this run:

- Fetch-error retry: 67 IDs, 67 entry rows, 136 coordinate contexts, 0 fetch errors, 38 deposited-v4 entries, zero split contexts. `9K5E` was skipped by the atom-site cap.
- Continuation retry3: 240 IDs, 239 entry rows, 512 coordinate contexts, 1 fetch error (`9E5C`), 45 deposited-v4 entries, 34 non-ORC metric prefilter entries, two split contexts.
- Continuation2: 80 IDs, 79 entry rows, 164 coordinate contexts, 1 fetch error (`9Y4F`), 4 deposited-v4 entries, 2 non-ORC metric prefilter entries, zero split contexts.

## Result

No new unsafe expected-policy ePK non-abstention was found.

- The explicit 67-ID fetch-error retry recovered the previous queue with zero remaining fetch errors.
- The only new split contexts were `9FXK:biological_assembly_1` and `9FXK:biological_assembly_2`; both materializer checks abstained as `no_substrate_mode_materializer_hit_review_only`.
- No metric-seeded non-ORC deposited-v4 / assembly-below-floor split context with pre-materializer heteromeric geometry was found.
- The refreshed regression gate emits 345 rows from 20 source artifacts.
- `unsafe_nonabstention_after_expected_policy_count` remains 0.
- `5UJ7:biological_assembly_1` remains the pinned context-v4-only biological-assembly split failure.

## Tooling Changes

- `tools/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_stress.py` now supports `--priority-fetch-error-artifact` and lets explicit retry IDs override reviewed-ID exclusions.
- `tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py` now sorts latest-only globs by artifact metadata timestamps and includes all metric-split artifacts so zero-row later shards do not hide earlier metric regression rows.

## Evidence For / Against

Evidence against this bounded split-trap surface:

- 67 prior fetch-error IDs, 240 continuation IDs, and 80 second-continuation IDs produced zero unsafe materializer non-abstentions.
- 34 retry3 and 2 continuation2 non-ORC deposited-v4 prefilter entries produced zero metric-seeded non-ORC assembly split contexts.
- The two new `9FXK` assembly split contexts abstained in the materializer.

Evidence for continued search:

- `9Y4F` remains a bounded transient fetch error.
- `DTP_recent_60` was not reached by continuation2.
- `5UJ7:biological_assembly_1` still falsifies context-v4-only sufficiency and must stay pinned.

## Verification

- `python -m py_compile` for the two changed lane helpers.
- `python -m json.tool` for the new metric artifacts and regression gate.
- JSONL parse validation for `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`.
- `git diff --check` over lane files changed this run.

## Blockers

- `git fetch origin` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git pull --ff-only origin research/epk-false-positive-hunter` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git fetch --no-write-fetch-head origin` succeeded.
- Normal worktree status remains noisy with linked-worktree metadata/index drift.
- `9Y4F` remains a bounded continuation2 fetch error.

## Next Query

Retry `9Y4F` from `v4_metric_seeded_ligand_assembly_split_continuation2_20260521_201017Z.json`, then continue `DTP_recent_60` and remaining ACP/DTP ligand-component shards while excluding the fetch-error retry, retry3, and continuation2 artifacts. Separately audit `9FXK:biological_assembly_1` and `9FXK:biological_assembly_2` as assembly-below-floor abstention controls; keep `5UJ7` pinned and avoid production claims.

Production claims, label changes, threshold calibration, registry/fingerprint edits, artifact migrations, and production scoring remain forbidden.

## Files Changed

- `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_fetch_error_retry_20260521_192857Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_retry3_20260521_192857Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_continuation2_20260521_201017Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_202430Z.json`
- `tools/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_stress.py`
- `tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`
