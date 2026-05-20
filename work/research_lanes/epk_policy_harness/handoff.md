# ePK policy harness handoff

Last updated: 2026-05-20T23:16:32Z
Run started: 2026-05-20T22:25:28Z
Run ended: 2026-05-20T23:16:32Z
Measured minutes: 51.07
Primary outcome: `policy_frozen_review_only`
Pushed commit: pending at handoff write time. Normal `git add` is blocked by linked-worktree `index.lock`; the final automation summary records whether the alternate commit/push workaround succeeded.

## Files changed

This run:
- `tools/research_lanes/epk_policy_harness/epk_policy_harness.py`
- `tools/research_lanes/epk_policy_harness/epk_nonprefrozen_alias_blocker_negative_control.py`
- `artifacts/research_lanes/epk_policy_harness/epk_nonprefrozen_gnp_gtp_terminal_gamma_alias_blocker_negative_control_20260520T223103Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_nonprefrozen_gnp_gtp_terminal_gamma_alias_blocker_negative_control_20260520T223103Z_tranche.json`
- `artifacts/research_lanes/epk_policy_harness/epk_nonprefrozen_gnp_gtp_terminal_gamma_alias_blocker_negative_control_20260520T223103Z_result.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

Prior dirty wrap metadata from the previous run is preserved in the JSONL ledger.

## Policy Status

Policy v0 remains frozen, review-only, and fail-closed. ATP/ANP/AMP-PNP may be predictive only when terminal gamma-equivalent geometry, local metal context, catalytic-site locality, source-free acceptor/role features, and same-structure co-materialization all hold under a preaccepted source-free role policy. No source-free role policy is accepted in v0.

This run adds an executable nonprefrozen alias-blocker negative-control contract. GNP/GTP terminal-gamma coordinate materializations observed from AMP-PNP query contexts are admitted only as review-only blocker rows. They cannot be promoted by query wording, cannot be declared pre-frozen unless already present in the frozen policy ligand map, and cannot carry same-structure co-materialization under policy v0.

## Evidence

- Final negative-control artifact: `artifacts/research_lanes/epk_policy_harness/epk_nonprefrozen_gnp_gtp_terminal_gamma_alias_blocker_negative_control_20260520T223103Z.json` (`sha256 ec29b3bf383b3d040ef7f863bcbbc4c6f92711b7e2389c1d6f05d02ed773dc75`).
- Final tranche: `artifacts/research_lanes/epk_policy_harness/epk_nonprefrozen_gnp_gtp_terminal_gamma_alias_blocker_negative_control_20260520T223103Z_tranche.json` (`sha256 63f201250e382b880e7a435d2f038724277a63c2c9ab8db259b997a41765cb23`).
- Final result: `artifacts/research_lanes/epk_policy_harness/epk_nonprefrozen_gnp_gtp_terminal_gamma_alias_blocker_negative_control_20260520T223103Z_result.json` (`sha256 6bd85f3e053bfcb9c16c3f16725e0a663ce6b926182207ac5427b9c76d82620c`).
- Source guard artifact: `artifacts/research_lanes/epk_policy_harness/epk_amp_pnp_query_context_coordinate_ligand_materialization_guard_20260520T213835Z.json` (`sha256 4f8322191f8ea0d7c1a13c949e7bc4dcb63da854be30ba1d304a1f2707dc9f72`).
- Blocker observations reviewed from source guard: 13.
- Selected terminal-gamma blocker rows: 9YA5:GTP, 9O65:GNP, 8UTP:GTP, 8UTQ:GTP, 8UTO:GTP, 8UTN:GTP, 9YAI:GTP, 9YMG:GTP.
- Coordinate-side blocker codes observed: `GNP, GTP`.
- Pre-frozen admitted coordinate codes remained: `ANP, ATP`.
- Final harness result: 8 rows, decision counts `{'review_only_abstain': 8}`, zero expected-decision mismatches, zero counterexamples, query-context contract enforced, topology contract enforced, and nonprefrozen alias-blocker contract enforced.
- Fault injection rejected blocker pre-freezing, policy-map blocker reuse, query-synonym materialization, missing blocker metadata, source-query predictive leakage, blocker co-materialization, and non-blocker context-observed codes.
- Regression reruns for the prior AMP-PNP materialization guard, cross-ligand sibling control, and ATP sibling control stayed clean.

## Blockers

- This is review-only harness pressure, not clean held-out performance evidence and not production scoring evidence.
- The negative-control rows come from a bounded prior AMP-PNP materialization-guard surface, not a global exhaustion of every GNP/GTP or AMP-PNP route.
- No accepted source-free folded substrate-role or acceptor-identity extractor exists in policy v0, so all rows continue to abstain.
- GNP/GTP remain blocker evidence only; no alias-map expansion, label import, threshold calibration, or production scoring claim is allowed.
- Normal `git fetch origin`, `git pull --ff-only`, and `git add` are blocked by linked-worktree metadata permissions on `FETCH_HEAD`/`index.lock`.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- Final negative-control harness run wrote `artifacts/research_lanes/epk_policy_harness/epk_nonprefrozen_gnp_gtp_terminal_gamma_alias_blocker_negative_control_20260520T223103Z_result.json`.
- Fault injection script rejected seven nonprefrozen blocker leak classes.
- Regression reruns wrote `/private/tmp/epk_policy_regression_nonprefrozen_guard/materialization_guard_result.json`, `/private/tmp/epk_policy_regression_nonprefrozen_guard/cross_ligand_sibling_result.json`, and `/private/tmp/epk_policy_regression_nonprefrozen_guard/atp_sibling_result.json`.
- `git diff --check` passed before ledger/handoff writing.
- JSON validation passed for the final negative-control artifact, tranche, result, and JSONL ledger before commit attempt.

## Exact next query

`epk_adp_product_state_and_candidate_repair_tripwire_contract_v1_review_only`

Use prior ADP/product-state and candidate-specific source-repair artifacts to add a review-only tripwire contract. Prove ADP/product-state rows, substrate/acceptor analog contexts, and candidate-specific source repairs cannot become predictive even if local geometry-like fields are present, and remain blocked without a future preregistered policy that survives fresh stress.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
