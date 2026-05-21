# ePK policy harness handoff

Last updated: 2026-05-21T03:19:10Z
Run started: 2026-05-21T02:30:02Z
Run ended: 2026-05-21T03:19:10Z
Measured minutes: 49.13
Primary outcome: `policy_frozen_review_only`
Pushed commit: `789cee388ab3dd255ab02a8b2768302cc4539c3b` (main run commit; this handoff/ledger metadata update is committed as a follow-up wrap commit).

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_fresh_adp_product_query_tripwire_surface.py`
- `tools/research_lanes/epk_policy_harness/epk_adp_chemcomp_continuation_synthesis.py`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_adp_low_geometry_priority_surface_round25_20260521T023349Z*.json` through `..._round40_20260521T025640Z*.json` (48 compact surface/tranche/result files)
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_adp_chemcomp_pagination_nonmaterialized_low_geometry_continuation_synthesis_20260521T025847Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy Status

Policy v0 remains frozen, review-only, and fail-closed. ATP/ANP/AMP-PNP may be predictive only when terminal gamma-equivalent geometry, local metal context, catalytic-site locality, source-free acceptor/role features, and same-structure co-materialization all hold under a preaccepted source-free role policy. No source-free role policy is accepted in v0.

This run adds a lane-local low-geometry continuation selector and synthesis invariant for ADP chem-comp pagination. ADP coordinate materialization, ADP product-state context, ADP product-phosphate local geometry summaries, nonmaterialized/skipped status, low-geometry priority status, query text, and source validation remain review-only. ADP/product rows are not admitted as predictive.

## Evidence

- Final synthesis artifact: `artifacts/research_lanes/epk_policy_harness/epk_fresh_adp_chemcomp_pagination_nonmaterialized_low_geometry_continuation_synthesis_20260521T025847Z.json` (`sha256 42be29c4fb7704f09faec52afe68e251ca629c2d079db575949ca9801dcf2702`).
- Query windows: [1360, 1420, 1480, 1540, 1600, 1660, 1720, 1780, 1840, 1900, 1960, 2020, 2080, 2140, 2200, 2260].
- Candidate IDs reviewed: 192 fresh IDs across 16 continuation surfaces.
- Coordinate-materialized ADP candidates: 188.
- ADP product-phosphate local geometry-like candidates: 182.
- Nonmaterialized/skipped ADP candidates: 4 (9N75, 9N76, 9N77, 9N74).
- Materialized ADP candidates without local geometry-like signal: 6 (9L9B, 9DVY, 9DGT, 9DGU, 9LBV, 9MSJ).
- Evaluated rows: 96.
- Decision counts: `{'review_only_abstain': 96}`.
- Expected-decision mismatches: 0.
- Counterexamples found: `[]`.
- Accepted-role/local-feature counterfactual: 96 review-only abstentions.
- Fault injection rejected 5 drift modes: duplicate windows, nonmonotone windows, priority-count tampering, priority shortfall, and source-validation review-only drift.
- Prior regression tranches reran cleanly: ADP repair, nonprefrozen blocker, AMP-PNP materialization guard, cross-ligand sibling-control, and ATP sibling-control.

## Blockers

- This is review-only harness pressure on bounded RCSB ADP chem-comp continuation windows, not clean held-out performance evidence and not production scoring evidence.
- The ADP chem-comp surface is not exhausted; continuation beyond query_rows 2260 remains open.
- Priority candidates were sparse: 10 across 192 fresh IDs, including several consecutive zero-priority windows.
- No accepted source-free folded substrate-role or acceptor-identity extractor exists in policy v0.
- No ADP/product-state activation policy is preregistered, frozen, or production-admissible.
- Normal `git fetch origin`, `git pull --ff-only`, `git add`, and local `HEAD` updates remain blocked by linked-worktree metadata permissions on `FETCH_HEAD`/`index.lock`; this run uses the alternate-index commit path.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/epk_policy_harness.py tools/research_lanes/epk_policy_harness/epk_fresh_adp_product_query_tripwire_surface.py tools/research_lanes/epk_policy_harness/epk_adp_chemcomp_continuation_synthesis.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- Fresh ADP low-geometry continuation results wrote and evaluated 16 result artifacts listed by the synthesis.
- Continuation validator accepted the final 16-surface aggregate and rejected 5 fault-injection cases.
- Accepted-role/local-feature counterfactual still yielded 96 review-only abstentions.
- Regression reruns wrote `/private/tmp/epk_policy_regression_low_geometry_continuation/*.json` and had zero mismatches/counterexamples.
- JSON/JSONL validation passed before this handoff write: 184 JSON files and 12 JSONL records parsed successfully.
- Main commit diff check passed: `git diff --check 594b147b568c27073791ddb9a792692365f1e0c0 789cee388ab3dd255ab02a8b2768302cc4539c3b`.

## Exact next query

`epk_fresh_adp_chemcomp_pagination_deep_sparse_priority_continuation_v2_review_only`

Continue ADP chem-comp pagination beyond the current bounded window (`query_rows` > 2260) with the frozen `low_geometry_first` selector. Predefine a compact stopping/flag rule before scanning, such as stopping after a bounded page block if consecutive windows contain zero nonmaterialized/skipped or materialized-no-geometry priority candidates. Keep candidate IDs frozen before compact coordinate review, keep ADP/product-state and query/source context review-only, admit no ADP/product row as predictive, and stop with compact artifacts only.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
