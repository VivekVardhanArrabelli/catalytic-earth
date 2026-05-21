# ePK false-positive hunter handoff

- Last updated: 2026-05-21T18:56:50Z
- Started: 2026-05-21T17:26:28Z
- Ended: 2026-05-21T18:56:50Z
- Measured minutes: 90.37
- Primary outcome: evidence_against
- Pushed evidence commit: `acde35fa81c1951079297c06deabf64859dc463d` via alternate-index commit/push
- Local checked-out HEAD remains `c444f088082208ec9de2aba575cfb1f9ddf03d15` because linked-worktree metadata writes are blocked.
- Rule under attack: metric-seeded biological-assembly/deposited-coordinate split sufficiency for review-only ePK materialization, plus the lane regression gate for ATPase/transporter/ORC-MCM/motor/same-chain/internal-fragment/ligand-materialization controls.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Preserved and extended the metric-seeded ligand-only split stress after the previous handoff reported a live-lock. The earlier non-TTY helper later completed and wrote a compact artifact; this run also completed an independent 320-ID metric pass and refreshed the regression gate. CIFs were fetched in memory and reduced to compact evidence only; no raw coordinate dumps were written.

- Post-wrap completed metric artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_20260521_164900Z.json`
- Capped metric follow-up artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_retry_20260521_182728Z.json`
- Current metric stress artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_stress_20260521_172628Z.json`
- Refreshed regression gate: `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_185303Z.json`
- Audited prior retry artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_remaining_fetch_error_retry_20260521_162454Z.json`

Metric-seeded reviewed surfaces now preserved:

- `164900Z`: 320 unique IDs, 285 entry rows, 590 coordinate contexts, 35 fetch errors, 133 deposited-v4 entries, 131 non-ORC deposited-v4 prefilter entries, zero split contexts.
- `182728Z`: 100 unique IDs, 100 entry rows, 175 coordinate contexts, zero fetch errors, 13 deposited-v4 entries, 12 non-ORC deposited-v4 prefilter entries, zero split contexts.
- `172628Z`: 320 unique IDs, 254 entry rows, 528 coordinate contexts, 66 fetch errors, 107 deposited-v4 entries, 105 non-ORC deposited-v4 prefilter entries, zero split contexts.

## Result

No new unsafe expected-policy ePK non-abstention was found.

- Zero metric-seeded deposited-v4 / biological-assembly-below-floor split contexts were found across the preserved metric artifacts.
- Zero metric-seeded materializer contexts were selected because split contexts were zero.
- The 207-ID remaining fetch-error retry remains exhausted as a reviewed surface with zero split contexts.
- The refreshed gate emitted 343 `epk_candidate_evidence_v1` rows from 14 source slots.
- `unsafe_nonabstention_after_expected_policy_count` stayed 0.
- `5UJ7:biological_assembly_1` remains the pinned context-v4-only biological-assembly split failure.

## Evidence For / Against

Evidence against metric-seeded ATP recent split traps on the reviewed surface:

- 131, 12, and 105 non-ORC deposited-v4 prefilter entries in the three metric artifacts produced zero assembly-below-floor split contexts.
- The capped 100-ID follow-up had zero fetch errors, so the cap path is usable for the next retry/sharding pass.
- The regression gate stayed green under expected policy while preserving the known context-v4-only failure.

Evidence for continued search:

- The current 320-ID stress still has 66 fetch-error IDs to retry.
- Later ATP pages and ANP/ACP/DTP ligand-component pages were not exhausted in this run.
- The metric source slot emits zero rows when no materializer contexts exist, so absence of rows is evidence about the split filter, not a production sufficiency claim.

## Verification

- `python -m json.tool` for the new metric artifacts and regression gates.
- JSONL parse validation for `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`.
- `git diff --check` over lane files changed this run.

## Blockers

- `git fetch origin` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git pull --ff-only origin research/epk-false-positive-hunter` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git fetch --no-write-fetch-head origin` succeeded.
- Local checked-out HEAD remains behind origin because linked-worktree metadata writes are denied.
- Normal worktree status remains noisy with staged deletions plus untracked replacements from linked-worktree index metadata drift.
- The current metric pass has 66 fetch errors and does not exhaust later ATP/ANP/ACP/DTP ligand-component pages.

## Next Query

Retry the 66 fetch-error IDs from `v4_metric_seeded_ligand_assembly_split_stress_20260521_172628Z.json` with the atom-site cap enabled, then shard ATP `start=640` and ANP/ACP/DTP ligand-component pages while excluding the `164900Z`, `182728Z`, and `172628Z` metric artifacts. Continue only metric-seeded deposited-v4 / assembly-below-floor traps with no ORC/MCM role tokens, `polymer_entity_count > 1`, and pre-materializer heteromeric local geometry. Keep `5UJ7` pinned and avoid production claims.

Production claims, label changes, threshold calibration, registry/fingerprint edits, artifact migrations, and production scoring remain forbidden.

## Files Changed

- `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_20260521_164900Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_retry_20260521_182728Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_stress_20260521_172628Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_184508Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_185303Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`
