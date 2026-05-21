# ePK false-positive hunter handoff

- Last updated: 2026-05-21T16:11:22Z
- Started: 2026-05-21T15:22:51Z
- Ended: 2026-05-21T16:11:22Z
- Measured minutes: 48.52
- Primary outcome: regression_rows_emitted
- Commit/push status: attempted after this handoff; linked-worktree metadata may still prevent local HEAD from matching origin.
- Rule under attack: biological-assembly/deposited-coordinate split sufficiency for review-only ePK materialization, with non-ORC deposited-v4 / assembly-below-floor traps and the lane regression gate for ATPase/transporter/ORC-MCM/motor/same-chain/internal-fragment/ligand-materialization controls.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Ran a bounded retry/generalization pass for the requested `1Y64` retry and non-ORC deposited-v4 / biological-assembly-below-floor split traps. CIFs were fetched in memory and reduced to compact metrics; no raw coordinate dumps were written.

- Main split artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress_non_orc_split_retry_20260521_152251Z.json`
- Fetch-error recovery artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_fetch_error_recovery_20260521_160625Z.json`
- Refreshed regression gate: `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_160349Z.json`
- Helpers used: `tools/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress.py`, `tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- Main pass reviewed 481 unique PDB IDs, 254 successful entry rows, and 562 coordinate contexts.
- Main pass fetch errors: 227, from a transient DNS failure resolving `data.rcsb.org`.
- Explicit retry seed `1Y64` fetched successfully, had no deposited-v4 hit, and did not enter the split-risk set.
- Materialized 20 selected split/control contexts; materializer context errors were zero.
- Recovery pass retried the first 20 failed IDs, reviewed 20 entry rows and 48 coordinate contexts, and had zero fetch errors.
- Raw coordinate files written: false.

## Result

No new unsafe expected-policy ePK non-abstention was found.

- Main split-risk entries were `1A49`, `1A5U`, and `5UJ7`.
- The only split context with pre-materializer heteromeric-entity local geometry was the already-known `5UJ7:biological_assembly_1` ORC residual.
- Effective non-ORC deposited-v4 / assembly-below-floor / heteromeric-local-geometry split contexts: zero on the successfully reviewed main-pass subset.
- The 20-ID recovery subset had zero split-risk entries and zero selected materializer contexts.
- The refreshed gate emitted 343 `epk_candidate_evidence_v1` rows from 13 source artifacts.
- `unsafe_nonabstention_after_expected_policy_count` stayed 0.
- The pinned `5UJ7:biological_assembly_1` context-v4-only biological-assembly split failure remains present as the unique context-v4-only unsafe non-abstention.
- The broad surface is not exhausted because 207 main-pass fetch-error IDs remain unretried after the 20-ID recovery sample.

## Evidence For / Against

Evidence for the regression gate extension:

- The latest assembly-split retry artifact is included in the gate through the lane latest-only split artifact glob.
- Preserved coordinate state, context, guard hit/miss, expected policy decision, observed materializer decision, local geometry, and acceptor/gamma entity mapping for split contexts.
- Kept `5UJ7:biological_assembly_1` as an explicit regression fixture while reporting unique context-v4-only failure contexts.

Evidence against new non-ORC split counterexamples on this run's reviewed surface:

- Zero effective non-ORC split contexts had pre-materializer heteromeric-entity local geometry.
- `1A49` and `1A5U` split contexts again had no local substrate geometry and no materializer hit.
- `1Y64` retried cleanly and did not enter the split-risk set.
- The first 20 failed IDs recovered cleanly and had zero split-risk entries.
- Expected-policy unsafe non-abstentions remained zero across 343 regression rows.

## Verification

- `python -m py_compile tools/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress.py tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- `python -m json.tool artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress_non_orc_split_retry_20260521_152251Z.json >/dev/null`
- `python -m json.tool artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_fetch_error_recovery_20260521_160625Z.json >/dev/null`
- `python -m json.tool artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_160349Z.json >/dev/null`
- `git diff --check -- tools/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress.py tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress_non_orc_split_retry_20260521_152251Z.json artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_fetch_error_recovery_20260521_160625Z.json artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_160349Z.json artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl work/research_lanes/epk_false_positive_hunter/handoff.md`

## Blockers

- `git fetch origin` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git pull --ff-only origin research/epk-false-positive-hunter` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git fetch --no-write-fetch-head origin` succeeded.
- Normal linked-worktree index operations remain unreliable because `.git/worktrees/catalytic-earth-epk-false-positive/index.lock` cannot be created.
- Local checked-out HEAD remains behind origin because linked-worktree metadata writes are denied.
- Main pass had 227 transient DNS fetch errors against `data.rcsb.org`; 20 sampled failures recovered cleanly, leaving 207 unretried failed IDs.

## Next Query

Retry the remaining 207 main-pass fetch-error IDs from `v4_entry_level_assembly_guard_stress_non_orc_split_retry_20260521_152251Z.json`, then continue metric-seeded non-ORC deposited-v4 / assembly-below-floor traps without relying on broad text buckets. Prioritize entries with deposited v4-positive metrics, biological assemblies below the v4 chain floor, no ORC/MCM role tokens, polymer_entity_count > 1, and pre-materializer heteromeric-entity local geometry. Keep `1A49` and `1A5U` as no-hit split controls and keep production labels, thresholds, registries/fingerprints, migrations, and scoring forbidden.

Production claims, label changes, threshold calibration, registry/fingerprint edits, artifact migrations, and production scoring remain forbidden.

## Files Changed

- `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress_non_orc_split_retry_20260521_152251Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_fetch_error_recovery_20260521_160625Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_160349Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`
