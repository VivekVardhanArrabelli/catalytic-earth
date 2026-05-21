# ePK policy harness handoff

Last updated: 2026-05-21T01:17:22Z
Run started: 2026-05-21T00:27:26Z
Run ended: 2026-05-21T01:17:22Z
Measured minutes: 49.93
Primary outcome: `policy_frozen_review_only`
Pushed commit: `pending_main_run_commit` (will be updated after alternate-index push; normal git metadata writes are blocked).

## Files changed

This run:
- `tools/research_lanes/epk_policy_harness/epk_policy_harness.py`
- `tools/research_lanes/epk_policy_harness/epk_fresh_adp_product_query_tripwire_surface.py`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_adp_product_query_context_tripwire_surface_20260521T003830Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_adp_product_query_context_tripwire_surface_20260521T003830Z_tranche.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_adp_product_query_context_tripwire_surface_20260521T003830Z_result.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_adp_product_query_context_tripwire_surface_20260521T003846Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_adp_product_query_context_tripwire_surface_20260521T003846Z_tranche.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_adp_product_query_context_tripwire_surface_20260521T003846Z_result.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_adp_product_query_context_tripwire_surface_round2_20260521T004519Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_adp_product_query_context_tripwire_surface_round2_20260521T004519Z_tranche.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_adp_product_query_context_tripwire_surface_round2_20260521T004519Z_result.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_adp_product_query_context_tripwire_surface_round3_20260521T004731Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_adp_product_query_context_tripwire_surface_round3_20260521T004731Z_tranche.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_adp_product_query_context_tripwire_surface_round3_20260521T004731Z_result.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_adp_product_query_context_tripwire_surface_round4_20260521T004812Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_adp_product_query_context_tripwire_surface_round4_20260521T004812Z_tranche.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_adp_product_query_context_tripwire_surface_round4_20260521T004812Z_result.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_adp_product_query_context_tripwire_synthesis_20260521T004900Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy Status

Policy v0 remains frozen, review-only, and fail-closed. ATP/ANP/AMP-PNP may be predictive only when terminal gamma-equivalent geometry, local metal context, catalytic-site locality, source-free acceptor/role features, and same-structure co-materialization all hold under a preaccepted source-free role policy. No source-free role policy is accepted in v0.

This run adds an executable fresh ADP/product query-context tripwire contract. ADP query contexts, coordinate-materialized ADP product-state rows, ADP product-phosphate local geometry summaries, source text, query text, and source validation remain review-only. Candidate-specific repair rows are not admitted in this fresh query-context contract, and future ADP/product activation remains closed unless a separate preregistered frozen policy survives fresh stress.

## Evidence

- Synthesis artifact: `artifacts/research_lanes/epk_policy_harness/epk_fresh_adp_product_query_context_tripwire_synthesis_20260521T004900Z.json` (`sha256 598f1f82c87df973dedf7bf384280158422351d9384d296c353962e3a21ee800`).
- Candidate IDs reviewed: 42.
- Coordinate-materialized ADP candidates: 32.
- Evaluated rows: 25.
- Decision counts: `{'review_only_abstain': 25}`.
- Expected-decision mismatches: 0.
- Counterexamples found: `[]`.
- Accepted-ADP/accepted-role-policy counterfactual: 25 review-only abstentions.
- Fault injection rejected 9 representative ADP query-context contract violations.
- Prior ADP/product repair, nonprefrozen blocker, materialization guard, cross-ligand sibling-control, and ATP sibling-control regressions stayed clean.

## Surface Summary

- `full_text_substrate_adp`: 10 candidates, 1 ADP-materialized, 1 rows, {'review_only_abstain': 1}, result sha256 `3acfad1dd0f3b468901f42dc8736175488d814b21edd6eb212067bd20455a04f`
- `chemcomp_adp_round1`: 8 candidates, 8 ADP-materialized, 6 rows, {'review_only_abstain': 6}, result sha256 `f474ab81921e1876807ed45375b1a9ac6cd2c2904b2b074490dd1a535a10eb26`
- `chemcomp_adp_round2`: 8 candidates, 7 ADP-materialized, 6 rows, {'review_only_abstain': 6}, result sha256 `e50a0d0225556ac2964a6c134691c5818bd2d5dc31fb4bca02d5088a8e4e52bd`
- `chemcomp_adp_round3`: 8 candidates, 8 ADP-materialized, 6 rows, {'review_only_abstain': 6}, result sha256 `599ee1e0989a54ca8ad019e660f298c2fb07cb33d4b2e50f5a07f5c23e48c6cb`
- `chemcomp_adp_round4`: 8 candidates, 8 ADP-materialized, 6 rows, {'review_only_abstain': 6}, result sha256 `4fbdbdb6a667199063623df14324f3abf46eb18bd56ce2fe3217bf78f9613dc0`

## Blockers

- This is review-only harness pressure on bounded RCSB surfaces, not clean held-out performance evidence and not production scoring evidence.
- The surfaces do not exhaust all possible ADP/product-state structures.
- One alternate source-text probe (`protein kinase ADP bound magnesium`) scanned 10 IDs but had no materialized ADP rows and wrote no artifact.
- No accepted source-free folded substrate-role or acceptor-identity extractor exists in policy v0.
- No ADP/product-state activation policy is preregistered, frozen, or production-admissible.
- Normal `git fetch origin`, `git pull --ff-only`, and `git add` remain blocked by linked-worktree metadata permissions on `FETCH_HEAD`/`index.lock`; this run uses the alternate-index commit path.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/epk_policy_harness.py tools/research_lanes/epk_policy_harness/epk_fresh_adp_product_query_tripwire_surface.py tools/research_lanes/epk_policy_harness/epk_adp_product_repair_tripwire.py`
- Fresh ADP/product query-context results wrote five result artifacts listed above.
- Representative fault injection rejected 9 leak/activation/context tampering cases.
- Accepted-ADP/accepted-role-policy counterfactual still yielded 25 review-only abstentions.
- Regression reruns wrote `/private/tmp/epk_policy_regression_fresh_adp_query/adp_product_repair_result.json`, `/private/tmp/epk_policy_regression_fresh_adp_query/nonprefrozen_result.json`, `/private/tmp/epk_policy_regression_fresh_adp_query/materialization_guard_result.json`, `/private/tmp/epk_policy_regression_fresh_adp_query/cross_ligand_result.json`, and `/private/tmp/epk_policy_regression_fresh_adp_query/atp_sibling_result.json`.
- JSON/JSONL validation passed after this handoff write: 16 JSON files and 11 JSONL records parsed successfully.
- `git diff --check` passed with an alternate index after this handoff write.

## Exact next query

`epk_fresh_adp_chemcomp_pagination_continuation_product_tripwire_v1_review_only`

Continue coordinate-materialized ADP chem-comp pagination under the same frozen ADP/product query-context tripwire. Freeze candidate IDs before compact coordinate review, keep ADP product-state and ADP product-phosphate geometry summaries review-only, admit no ADP/product row as predictive, and stop with compact artifacts only.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
