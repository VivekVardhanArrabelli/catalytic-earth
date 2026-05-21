# ePK false-positive hunter handoff

- Last updated: 2026-05-21T02:29:09Z
- Started: 2026-05-21T01:29:56Z
- Ended: 2026-05-21T02:29:09Z
- Measured minutes: 59.22
- Primary outcome: evidence_for
- Pushed commits: evidence commit `6383dc6f94eeb59e138591157faf94a06a99285a`; handoff/ledger annotation commit `e037cb2cee5176c7ceb31e0745ec3ef04356c632`. Both used alternate-index commit/push because normal linked-worktree gitdir writes remain blocked.
- Rule under attack: assembly-context `v4_oligomeric_atp_terminals_no_mg_required` sufficiency for review-only ePK substrate-mode/source-free topology false-positive control.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Executed the prior handoff next query as a deposited/biological-assembly split generalization and entry-level guard stress.

- Helper: `tools/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress.py`
- Initial pass: 360 PDB entries, 777 coordinate contexts, 0 fetch errors.
- Deep pass: 520 PDB entries, 1,132 coordinate contexts, 0 fetch errors.
- Query sources: fixed controls, prior assembly artifacts, ORC/OCCM/MCM ATP/ANP component-text queries, non-ORC AAA+/ATPase ATP/ANP component-text queries, and ePK peptide/substrate/MAPK/mTOR safety queries.
- Biological assemblies: reviewed deposited atom_site plus declared assemblies, capped at 12 assemblies per entry. One entry hit the cap: `3HQP`, assemblies 1-12 of 16; it was not split-risk.
- Materializer: 20 selected split-risk/control contexts, 0 materializer context errors.
- Raw coordinate files written: false.

## Result

Primary outcome is `evidence_for` for the review-only entry-level guard variant.

- Reconfirmed the known current assembly-context v4 residual: `5UJ7` biological assembly 1 has a topology-clear ORC substrate-mode hit, Tyr174 chain C OH to ATP PG associated with chain A at 5.822 A, while context-level v4 is false.
- The entry-level any-context v4 variant closes that residual because deposited atom_site v4 is true for `5UJ7`.
- No new split residual was found beyond `5UJ7` on the 520-entry / 1,132-coordinate-context deep surface.
- Split-risk IDs were exactly `1A49`, `1A5U`, and `5UJ7`. `1A49` and `1A5U` had four below-chain-floor assembly contexts, all with no substrate-mode materializer hit.

## Evidence For / Against

Evidence for the entry-level guard variant:

- `5UJ7:biological_assembly_1` moves from current context-v4 residual to `non_epk_counterexample_closed_by_entry_level_guard_review_only`.
- Context-v4 still blocks 14 prior deposited ORC/OCCM/MCM counterexample contexts.
- The entry-level variant had 0 residual non-ePK counterexamples and 0 known ePK positive losses among selected materializer contexts.

Evidence against overclaiming:

- This is still review-only evidence. It is not production scoring, label import, threshold calibration, or registry/fingerprint evidence.
- The ePK overblock safety panel here is bounded and selected; the next run should expand source-valid high-order ePK biological assemblies before any sufficiency claim.
- `3HQP` had 16 declared assemblies and only assemblies 1-12 were reviewed by cap; it was not split-risk in the reviewed contexts.

## Blockers

- Normal `git fetch origin` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git fetch --no-write-fetch-head origin` succeeded and local `HEAD` matched `origin/research/epk-false-positive-hunter` before this run.
- Direct writes to `/Users/vivekvardhanarrabelli/Documents/Codex/2026-05-08/check-out-careflly-u-can-use-2/catalytic-earth/.git/worktrees/catalytic-earth-epk-false-positive/` fail with Operation not permitted, so normal `git add`/`git commit` is expected to fail creating `index.lock`.
- Alternate-index commit/push succeeded for evidence commit `6383dc6f94eeb59e138591157faf94a06a99285a`.
- Alternate-index commit/push also succeeded for handoff/ledger annotation commit `e037cb2cee5176c7ceb31e0745ec3ef04356c632`.
- Normal `git status` remains unreliable/dirty in this linked worktree because the worktree index cannot be refreshed; use origin branch state or an alternate index for committed-content verification.

## Next Query

Target entry-level guard overblock risk on source-valid high-order ePK biological assemblies beyond the fixed positive panel: expand kinase/substrate-peptide assembly contexts with deposited-or-assembly v4 true and force the materializer per context, then separately probe non-ORC ATPase split-risk entries with later RCSB offsets. Keep production labels, thresholds, registries/fingerprints, migrations, and scoring forbidden.

Production claims, label changes, threshold calibration, registry/fingerprint edits, artifact migrations, and production scoring remain forbidden.

## Files Changed

- `tools/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress.py`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress_20260521_013529Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_entry_level_assembly_guard_stress_deep_20260521_015936Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`

Existing uncommitted prior lane artifacts from earlier runs are still present and were not reverted.
