# ePK false-positive hunter handoff

- Last updated: 2026-05-21T17:44:05Z
- Started: 2026-05-21T16:24:54Z
- Ended: 2026-05-21T17:44:05Z
- Measured minutes: 79.18
- Primary outcome: evidence_against
- Pushed evidence commit: `211000f1c61e4d119ccaccb0fab64dfa0c522739` via alternate-index commit/push.
- Remote branch verified at: `211000f1c61e4d119ccaccb0fab64dfa0c522739`.
- Local checked-out HEAD remains `c444f088082208ec9de2aba575cfb1f9ddf03d15` because linked-worktree metadata writes are blocked.
- Rule under attack: biological-assembly/deposited-coordinate split sufficiency for review-only ePK materialization, plus the lane regression gate for ATPase/transporter/ORC-MCM/motor/same-chain/internal-fragment/ligand-materialization controls.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Completed the requested retry of the remaining 207 main-pass fetch-error IDs from `v4_entry_level_assembly_guard_stress_non_orc_split_retry_20260521_152251Z.json` after subtracting the 20-ID recovery artifact.

- Retry artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_remaining_fetch_error_retry_20260521_162454Z.json`
- Refreshed regression gate: `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_172900Z.json`
- New metric-seeded helper: `tools/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_stress.py`
- Updated gate converter: `tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- Retry reviewed 207 entries and 436 deposited/assembly coordinate contexts.
- Retry fetch errors: 0.
- Retry deposited-v4 entries: 51.
- Retry entry-level any-context-v4 guard hits: 54.
- Retry split contexts: 0.
- Retry selected materializer contexts: 0.
- Raw coordinate files written: false.

## Result

No new unsafe expected-policy ePK non-abstention was found.

- The remaining 207-ID retry queue is exhausted as a reviewed surface.
- Zero deposited-v4 / biological-assembly-below-floor split contexts were found in the 207-ID retry.
- Zero non-ORC split contexts and zero pre-materializer heteromeric split contexts were found in the 207-ID retry.
- The refreshed gate emitted 343 `epk_candidate_evidence_v1` rows from 14 source slots.
- `unsafe_nonabstention_after_expected_policy_count` stayed 0.
- `5UJ7:biological_assembly_1` remains the pinned context-v4-only biological-assembly split failure.

## Metric-Seeded Attempt

Started a ligand-component-only metric-seeded helper to avoid broad full-text buckets. It reached checkpoint `last_index=180`, `progress_entries_reviewed=145`, `progress_fetch_errors=35`, then live-locked before writing `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_20260521_164900Z.json`.

Process-control blocker details:

- The helper was launched without a TTY and stdin was closed, so Ctrl-C could not be sent through the session.
- `ps`, `pgrep`, `pkill`, and `killall` process inspection/termination were denied by sandbox permissions.
- No completed metric artifact existed at wrap time.
- The helper has now been patched with `--max-local-geometry-atom-site-rows` defaulting to `120000` to avoid future local-geometry scans over very large atom-site contexts.

## Evidence For / Against

Evidence against the retry-queue split hypothesis:

- All 207 formerly failed IDs recovered cleanly.
- 436 coordinate contexts contained 51 deposited-v4 entries but zero split contexts.
- No materializer contexts were selected because there were no split contexts.
- The expected-policy regression gate stayed green with zero unsafe non-abstentions.

Evidence for continued fixture coverage:

- The regression gate still includes `5UJ7:biological_assembly_1` as the pinned context-v4-only failure.
- The converter now has a separate metric-seeded source slot, so future metric artifacts will not displace the latest non-ORC split artifact in the gate.

## Verification

- `python -m py_compile tools/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_stress.py tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- `python -m json.tool artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_remaining_fetch_error_retry_20260521_162454Z.json >/dev/null`
- `python -m json.tool artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_172900Z.json >/dev/null`
- `git diff --check -- tools/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_stress.py tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_remaining_fetch_error_retry_20260521_162454Z.json artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_172900Z.json`

## Blockers

- `git fetch origin` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git pull --ff-only origin research/epk-false-positive-hunter` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git fetch --no-write-fetch-head origin` succeeded.
- Normal linked-worktree index operations remain unreliable because linked-worktree metadata writes are denied.
- Metric-seeded helper live-locked before writing a completed artifact, and process termination was denied by sandbox process-list restrictions.

## Next Query

Rerun the metric-seeded ligand-only assembly split helper with the new atom-site local-geometry cap and a smaller bounded surface, then retry or shard the failed/slow ligand-only page. Preserve the 207-ID retry as exhausted evidence; keep `5UJ7` pinned; avoid broad full-text buckets unless the capped metric surface is exhausted. Keep production labels, thresholds, registries/fingerprints, migrations, and scoring forbidden.

Production claims, label changes, threshold calibration, registry/fingerprint edits, artifact migrations, and production scoring remain forbidden.

## Files Changed

- `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_remaining_fetch_error_retry_20260521_162454Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_172900Z.json`
- `tools/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_stress.py`
- `tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`
