# ePK policy harness handoff

Last updated: 2026-05-21T00:14:43Z
Run started: 2026-05-20T23:26:23Z
Run ended: 2026-05-21T00:14:43Z
Measured minutes: 48.33
Primary outcome: `policy_frozen_review_only`
Pushed commit: pending at handoff write time; final automation summary records the pushed branch tip after the alternate-index commit/push.

## Files changed

This run:
- `tools/research_lanes/epk_policy_harness/epk_policy_harness.py`
- `tools/research_lanes/epk_policy_harness/epk_adp_product_repair_tripwire.py`
- `artifacts/research_lanes/epk_policy_harness/epk_adp_product_state_candidate_repair_tripwire_20260520T233843Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_adp_product_state_candidate_repair_tripwire_20260520T233843Z_tranche.json`
- `artifacts/research_lanes/epk_policy_harness/epk_adp_product_state_candidate_repair_tripwire_20260520T233843Z_result.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy Status

Policy v0 remains frozen, review-only, and fail-closed. ATP/ANP/AMP-PNP may be predictive only when terminal gamma-equivalent geometry, local metal context, catalytic-site locality, source-free acceptor/role features, and same-structure co-materialization all hold under a preaccepted source-free role policy. No source-free role policy is accepted in v0.

This run adds an executable ADP/product-state/candidate-repair tripwire contract. ADP/product-state rows, substrate/acceptor analog contexts, split-state repair rows, and candidate-specific source repairs remain review-only blockers even when local geometry-like fields are present. Candidate-specific source repair cannot be marked predictive, row-declared tripwire contexts must match actual row fields, and future policy activation is closed unless a separate preregistered frozen policy survives fresh stress.

## Evidence

- Final tripwire artifact: `artifacts/research_lanes/epk_policy_harness/epk_adp_product_state_candidate_repair_tripwire_20260520T233843Z.json` (`sha256 a58ec0a785b3d5d4195d15d23f1f22819975ab3d0df19b7f1ef6fba2e1bf921c`).
- Final tranche: `artifacts/research_lanes/epk_policy_harness/epk_adp_product_state_candidate_repair_tripwire_20260520T233843Z_tranche.json` (`sha256 9157232884c29860b781cf057725401a93d568cbcd4c3366937c976e33fc83d5`).
- Final result: `artifacts/research_lanes/epk_policy_harness/epk_adp_product_state_candidate_repair_tripwire_20260520T233843Z_result.json` (`sha256 7e6b854b405e2ca074f69a2c0234ae1ab865b416c21ffb39cead3f1a9d8c21fe`).
- Rows reviewed: 10.
- Decision counts: `{'review_only_abstain': 10}`.
- Context coverage: `{'ADP': 4, 'PRODUCT_STATE': 4, 'SUBSTRATE_ACCEPTOR_ANALOG': 1, 'CANDIDATE_SPECIFIC_SOURCE_REPAIR': 5, 'SPLIT_STATE': 2}`.
- Geometry-like tripwire rows: 7.
- Counterfactual local-feature rows: 3.
- Expected-decision mismatches: 0.
- Counterexamples found: `[]`.
- Fault injection rejected 9 representative contract violations and 30 rowwise tampering cases.
- In-memory accepted-role-policy counterfactual still produced 10 review-only abstentions.
- Prior materialization guard, nonprefrozen blocker, cross-ligand sibling-control, and ATP sibling-control regressions stayed clean.

## Blockers

- This is review-only harness pressure, not clean held-out performance evidence and not production scoring evidence.
- The counterfactual local-feature rows are policy QA rows, not biological coordinate measurements.
- No accepted source-free folded substrate-role or acceptor-identity extractor exists in policy v0.
- No ADP/product-state activation policy is preregistered, frozen, or production-admissible.
- Normal `git fetch origin`, `git pull --ff-only`, and `git add` are still blocked by linked-worktree metadata permissions on `FETCH_HEAD`/`index.lock`.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/epk_policy_harness.py tools/research_lanes/epk_policy_harness/epk_adp_product_repair_tripwire.py`
- Final tripwire harness run wrote `artifacts/research_lanes/epk_policy_harness/epk_adp_product_state_candidate_repair_tripwire_20260520T233843Z_result.json`.
- Representative fault injection rejected 9 tripwire leak classes.
- Rowwise tripwire fault matrix rejected 30 tampering cases.
- Regression reruns wrote `/private/tmp/epk_policy_regression_adp_tripwire_materialization_guard_result.json`, `/private/tmp/epk_policy_regression_adp_tripwire_nonprefrozen_result.json`, `/private/tmp/epk_policy_regression_adp_tripwire_cross_ligand_result.json`, and `/private/tmp/epk_policy_regression_adp_tripwire_atp_sibling_result.json`.
- JSON and JSONL validation are rerun after this handoff write.
- `git diff --check` is rerun with an alternate index after this handoff write.

## Exact next query

`epk_fresh_adp_product_query_context_tripwire_surface_v1_review_only`

Run a bounded fresh ADP/product-state query-context surface under the frozen tripwire contract. Freeze candidate ids before local feature review, keep query text and source validation review-only, admit no ADP/product-state or candidate-specific repair row as predictive, and stop with compact artifacts only.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
