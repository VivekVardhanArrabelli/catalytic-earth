# ePK policy harness handoff

Last updated: 2026-05-21T02:18:16Z
Run started: 2026-05-21T01:29:25Z
Run ended: 2026-05-21T02:18:16Z
Measured minutes: 48.85
Primary outcome: `policy_frozen_review_only`
Pushed commit: `a4e8a8264b026744215e305aab59e4d3013ed71b` (main run commit; this handoff metadata update is committed as a follow-up wrap commit).

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_adp_chemcomp_continuation_synthesis.py`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_adp_chemcomp_pagination_continuation_synthesis_20260521T015503Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_adp_product_query_context_tripwire_surface_round5_20260521T013228Z*.json` through `..._round24_20260521T015401Z*.json` (60 compact surface/tranche/result files)
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy Status

Policy v0 remains frozen, review-only, and fail-closed. ATP/ANP/AMP-PNP may be predictive only when terminal gamma-equivalent geometry, local metal context, catalytic-site locality, source-free acceptor/role features, and same-structure co-materialization all hold under a preaccepted source-free role policy. No source-free role policy is accepted in v0.

This run adds a lane-local ADP chem-comp continuation synthesis validator and stresses the existing frozen ADP/product query-context tripwire across deeper fresh pagination. ADP coordinate materialization, ADP product-state context, ADP product-phosphate local geometry summaries, query text, and source validation remain review-only. ADP/product rows are not admitted as predictive.

## Evidence

- Final synthesis artifact: `artifacts/research_lanes/epk_policy_harness/epk_fresh_adp_chemcomp_pagination_continuation_synthesis_20260521T015503Z.json` (`sha256 58b7e52cd599dda9d560d307593dc761899e7caa016f3e5c3651825550286126`).
- Query windows: [160, 220, 280, 340, 400, 460, 520, 580, 640, 700, 760, 820, 880, 940, 1000, 1060, 1120, 1180, 1240, 1300].
- Candidate IDs reviewed: 240 fresh IDs across 20 continuation surfaces.
- Coordinate-materialized ADP candidates: 227.
- ADP product-phosphate local geometry-like candidates: 205.
- Nonmaterialized/skipped ADP candidates: 13.
- Materialized ADP candidates without local geometry-like signal: 22.
- Evaluated rows: 117.
- Decision counts: `{'review_only_abstain': 117}`.
- Expected-decision mismatches: 0.
- Counterexamples found: `[]`.
- Accepted-ADP/accepted-role-policy counterfactual: 117 review-only abstentions.
- Continuation fault injection rejected 5 drift modes: duplicate IDs, nonmonotone query windows, source-query leakage, production-claim drift, and raw-coordinate flags.
- Prior regression tranches reran cleanly: ADP repair, nonprefrozen blocker, AMP-PNP materialization guard, cross-ligand sibling-control, and ATP sibling-control.

## Blockers

- This is review-only harness pressure on bounded RCSB ADP chem-comp continuation windows, not clean held-out performance evidence and not production scoring evidence.
- The ADP chem-comp surface is not exhausted; continuation beyond query_rows 1300 remains open.
- No accepted source-free folded substrate-role or acceptor-identity extractor exists in policy v0.
- No ADP/product-state activation policy is preregistered, frozen, or production-admissible.
- Normal `git fetch origin`, `git pull --ff-only`, `git reset`, `git add`, and local `HEAD` updates remain blocked by linked-worktree metadata permissions on `FETCH_HEAD`/`index.lock`; this run uses the alternate-index commit path.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/epk_policy_harness.py tools/research_lanes/epk_policy_harness/epk_fresh_adp_product_query_tripwire_surface.py tools/research_lanes/epk_policy_harness/epk_adp_chemcomp_continuation_synthesis.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- Fresh ADP continuation results wrote and evaluated 20 result artifacts listed by the synthesis.
- Continuation validator accepted the final 20-surface aggregate and rejected 5 fault-injection cases.
- Accepted-ADP/accepted-role-policy counterfactual still yielded 117 review-only abstentions.
- Regression reruns wrote `/private/tmp/epk_policy_regression_adp_continuation/*.json` and had zero mismatches/counterexamples.
- JSON/JSONL validation passed before this handoff write: 135 JSON files and 11 JSONL records parsed successfully.
- Final wrap validation reran JSON/JSONL parsing after this handoff write: 135 JSON files and 12 JSONL records parsed successfully.
- Alternate-index `git diff --check` passed for the final metadata wrap.

## Exact next query

`epk_fresh_adp_chemcomp_pagination_nonmaterialized_low_geometry_continuation_v1_review_only`

Continue ADP chem-comp pagination beyond the current bounded window (`query_rows` > 1300), prioritizing candidate pages likely to contain nonmaterialized ADP, skipped-large structures, or coordinate-materialized ADP without local ADP product-phosphate geometry-like signal. Keep candidate IDs frozen before compact coordinate review, keep ADP/product-state and query/source context review-only, admit no ADP/product row as predictive, and stop with compact artifacts only.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
