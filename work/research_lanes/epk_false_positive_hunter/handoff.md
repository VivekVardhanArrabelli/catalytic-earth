# ePK false-positive hunter handoff

- Last updated: 2026-05-21T15:22:40Z
- Started: 2026-05-21T14:21:56Z
- Ended: 2026-05-21T15:22:40Z
- Measured minutes: 60.73
- Primary outcome: regression_rows_emitted
- Pushed evidence commit: 2ae54774aeb8552aef8261c828a1f83be9b16996 via alternate-index commit/push.
- Rule under attack: biological-assembly context-v4 sufficiency, entry-level any-context v4 review blocker, and the lane regression gate for ATPase/transporter/ORC-MCM/motor/same-chain/internal-fragment/ligand-materialization controls.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Ran the requested `1Y64` retry and a broadened deposited-v4 / biological-assembly-below-floor split stress. The helper now preserves compact pre-materializer local Tyr or N-terminal Ser/Thr/Tyr geometry plus acceptor/gamma entity mapping for split contexts. CIFs were fetched in memory and reduced to compact metrics; no raw coordinate dumps were written.

- Split helper artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress_non_orc_split_20260521_142619Z.json`
- Refreshed regression gate: `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_152108Z.json`
- Helpers: `tools/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress.py`, `tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- Reviewed 421 unique PDB IDs, 421 entry rows, and 906 coordinate contexts.
- Explicit retry seed: `1Y64`; it fetched successfully, had one biological assembly, and had no deposited-v4 or split-risk context.
- Materialized 20 selected split/control contexts.
- Fetch errors: zero.
- Materializer context errors: zero.
- Raw coordinate files written: false.

## Result

No new unsafe expected-policy ePK non-abstention was found on this bounded surface.

- Split-risk entries were `1A49`, `1A5U`, and `5UJ7`.
- `1A49` and `1A5U` are pyruvate kinase split controls: deposited v4-positive with biological assemblies below the chain floor, but no compact local Tyr or N-terminal Ser/Thr/Tyr substrate geometry and no materializer hit.
- The only split context with pre-materializer heteromeric-entity local geometry was the already-known `5UJ7:biological_assembly_1` ORC residual.
- Effective non-ORC deposited-v4 / assembly-below-floor / heteromeric-local-geometry split contexts: zero after excluding known ORC/MCM controls and ORC role-token entries.
- The refreshed gate emitted 343 `epk_candidate_evidence_v1` rows from 13 source artifacts.
- `unsafe_nonabstention_after_expected_policy_count` stayed 0.
- The pinned `5UJ7:biological_assembly_1` context-v4-only biological-assembly split failure remains present as the unique context-v4-only unsafe non-abstention.

## Evidence For / Against

Evidence for the regression gate extension:

- Added the latest assembly-split artifact to the gate through a latest-only lane artifact glob.
- Preserved coordinate state, context, guard hit/miss, expected policy decision, observed materializer decision, local geometry, and acceptor/gamma entity mapping for split contexts.
- Kept `5UJ7:biological_assembly_1` as an explicit regression fixture while reporting unique context-v4-only failure contexts.

Evidence against new non-ORC split counterexamples on this run's surface:

- Zero effective non-ORC split contexts had pre-materializer heteromeric-entity local geometry.
- `1A49` and `1A5U` split contexts had no local substrate geometry and no materializer hit.
- `1Y64` did not reproduce the prior fetch error and did not enter the split-risk set.
- Expected-policy unsafe non-abstentions remained zero across 343 regression rows.

## Verification

- `python -m py_compile tools/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress.py tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- `python -m json.tool artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress_non_orc_split_20260521_142619Z.json >/dev/null`
- `python -m json.tool artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_152108Z.json >/dev/null`
- `git diff --check -- tools/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress.py tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress_non_orc_split_20260521_142619Z.json artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_152108Z.json`

## Blockers

- `git fetch origin` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git pull --ff-only origin research/epk-false-positive-hunter` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git fetch --no-write-fetch-head origin` succeeded.
- Normal linked-worktree index operations have been unreliable in this worktree because `.git/worktrees/catalytic-earth-epk-false-positive/index.lock` cannot be created.
- Local checked-out HEAD was already behind origin at run start because linked-worktree metadata writes are denied.

## Next Query

Search for true non-ORC deposited-v4 / assembly-below-floor split traps without relying on broad text buckets that can pull in ORC controls: seed from entries with deposited v4-positive metrics, biological assemblies below the v4 chain floor, no ORC/MCM role tokens, polymer_entity_count > 1, and pre-materializer heteromeric-entity local geometry. Prioritize ATP-grasp/pyruvate-kinase-like oligomeric enzymes, ABC/transporter ATPases, dynein/VCP/proteasome, and helicase/clamp-loader assemblies; keep `1A49` and `1A5U` as no-hit split controls. Keep production labels, thresholds, registries/fingerprints, migrations, and scoring forbidden.

Production claims, label changes, threshold calibration, registry/fingerprint edits, artifact migrations, and production scoring remain forbidden.

## Files Changed

- `tools/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress.py`
- `tools/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_regression_gate.py`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress_non_orc_split_20260521_142619Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_152108Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`
