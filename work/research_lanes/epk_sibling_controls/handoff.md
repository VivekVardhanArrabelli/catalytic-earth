# ePK sibling controls handoff

Last updated: 2026-05-20T21:13:43Z
Run started: 2026-05-20T20:25:00Z
Run ended: 2026-05-20T21:13:43Z
Measured minutes: 48.7

Pushed commit: not pushed; linked-worktree Git metadata writes are blocked in this sandbox.
Primary outcome: `evidence_for`

## What changed

Consolidated the expanded review-only sibling blockers into a lane-local scorer-design test matrix. The new matrix de-duplicates the expanded counteraxis artifacts into 91 review-only cases:

- 72 gamma-proximity controls across ASKHA, dNK, GHKL, GHMP, NDK, PfkA, PfkB, and ATP-grasp.
- 57 gamma weak-rule cases with expected review-only blockers and 0 expected-unblocked weak gamma cases.
- 19 strict product controls across ATP-grasp, dNK, PfkA, and PfkB.
- 19 strict product weak-rule cases with expected review-only blockers and 0 expected-unblocked product cases.
- The existing 16-case scorer-design panel is represented as a subset for smoke-style future tests.

The new fixture is `artifacts/research_lanes/epk_sibling_controls/review_only_counteraxis_scorer_test_matrix_20260520.json`. It is review-only scorer-design input, not production labels, not production scoring, and not threshold calibration.

## Files changed

New in this run:

- `tools/research_lanes/epk_sibling_controls/build_counteraxis_scorer_test_matrix.py`
- `artifacts/research_lanes/epk_sibling_controls/review_only_counteraxis_scorer_test_matrix_20260520.json`
- `artifacts/research_lanes/epk_sibling_controls/epk_sibling_controls_runs.jsonl`
- `work/research_lanes/epk_sibling_controls/handoff.md`

Inherited uncommitted lane artifacts from prior runs were present at start and were left intact.

## Controls added

Controls added: 0 new sourced controls.

Controls adjudicated: 91 de-duplicated expanded controls.

- Gamma matrix: 72 unique cases; 57 expected-block weak cases, 15 no-weak-hit controls.
- Product matrix: 19 unique strict product cases; all 19 expected-block weak product cases.
- Expected unblocked weak cases: 0.

## Evidence notes

- Evidence for review-only separation: the defined expanded sibling surface is fully covered by source-free expected blockers in the matrix.
- Evidence against naive rules remains: the matrix still contains 57 gamma and 19 product proximity sibling counterexamples, so distance/proximity-only ePK rules remain unsafe without source-free substrate-identity and family-boundary blockers.
- The matrix keeps all cases `production_claim_allowed=false`, `production_scoring_admissible=false`, `epk_score_computed=false`, and `labels_or_fingerprints_changed=false`.
- No new RCSB queries, mmCIF fetches, raw coordinate files, production labels, registries, fingerprints, migrations, thresholds, or production scoring changes were made.

## Blockers

`git fetch origin` failed before work began while opening linked-worktree `FETCH_HEAD` with `Operation not permitted`, so `git pull --ff-only origin research/epk-sibling-controls` could not be safely completed.

Final `git add artifacts/research_lanes/epk_sibling_controls work/research_lanes/epk_sibling_controls tools/research_lanes/epk_sibling_controls` failed creating linked-worktree `index.lock` with `Operation not permitted`, so commit and push could not be completed from this sandbox.

## Safety notes

Production claims remain forbidden. Production label registries, `data/registries/mechanism_fingerprints.json`, artifact migration files, labels, thresholds, and Git history were not changed. No labels were imported, no production score was claimed, and no raw coordinate dumps were written.

## Next query

Use `artifacts/research_lanes/epk_sibling_controls/review_only_counteraxis_scorer_test_matrix_20260520.json` as the future source-free scorer-design fixture; only reopen sibling sourcing if a specific curated seed set appears.

Production claims, label changes, fingerprint edits, registry edits, and threshold calibration remain forbidden.
