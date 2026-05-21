# ePK policy harness handoff

Last updated: 2026-05-21T23:20:01Z
Run started: 2026-05-21T22:31:00Z
Run ended: 2026-05-21T23:20:01Z
Measured minutes: 49.02
Primary outcome: `candidate_class_terminal_no_go`

## Files changed

- `artifacts/research_lanes/epk_policy_harness/epk_active_gamma_folded_tyr_terminal_blocker_decision_20260521T223100Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy status

Policy v0 remains frozen, review-only, and fail-closed. This run did not create a new schema version, harness version, federation layer, scoreboard field, adapter, or regression gate. It did not change production labels, thresholds, registries, fingerprints, migrations, scoring, or Git history, and it makes no countable ePK readiness claim.

The planned missing-coordinate-state fixture path was stopped for this run because it would not change a candidate, blocker class, or regression decision. Existing v7/v0 review-only outputs were sufficient for a blocker decision.

## Strongest active-gamma candidate

The strongest cross-lane active-gamma row reviewed was `8OXM|gamma=B:ANP3101:PG|acceptor=F:SER15:OG`.

Why it is strong review-only input:

- ANP terminal-gamma distance is 3.482 A, within the frozen 6.0 A cutoff.
- The positive-evidence compact row has local Mg context.
- The substrate-role identity row has ordered-like coordinate certainty, cross-chain topology, strict auth-terminal candidate role, gamma-facing orientation, and `blocker_class=none`.
- The acid/base row also keeps `source_blocker_class=none`.

Why it is not admissible under current policy:

- `epk_policy_v0_20260520.json` has `accepted_source_free_acceptor_role_policy_ids=[]`.
- Source support remains review-only and explicitly non-predictive.
- The positive-evidence row remains `candidate_review_only_non_countable` with `production_policy_abstain` and `review_only_lane` blockers.
- No production/import/countable readiness claim is allowed.

## Terminal blocker decision

`folded_tyr_reciprocal_context` moved from `review_only_abstain_topology_ambiguity_review_required` to `terminal_no_go_source_free_under_current_policy`.

This is not a global active-gamma rejection. It is a class-scoped terminal no-go for active-gamma candidates whose apparent acceptor role depends on reciprocal folded Tyr or same-chain/autophosphorylation-like topology under the current source-free policy.

Evidence:

- `9UUX|gamma=A:ANP501:PG|acceptor=B:TYR204:OH` is active-gamma, ordered-like, cross-chain, 3.968 A, gamma-facing, and still `topology_ambiguity` with no unblocked candidate in the conflict decision row.
- `9UUR|gamma=A:ANP501:PG|acceptor=B:TYR204:OH` is active-gamma, ordered-like, cross-chain, 4.181 A, gamma-facing, and still `topology_ambiguity` with no unblocked candidate in the conflict decision row.
- `9UW4|gamma=A:ANP501:PG|acceptor=B:TYR204:OH` is the counterexample anchor: same reciprocal folded Tyr role class, active-gamma, ordered-like, 4.194 A, gamma-facing, and `topology_ambiguity`.
- Candidate conflict rows for `9UUR`, `9UUX`, and `9UW4` all use `source_free_decision_class=abstain_biology_topology_review_required`.
- Acid/base proximity did not clear the biology blocker because reciprocal Tyr positives and the counterexample both carry gamma-coupled carboxylate context.

Artifact: `artifacts/research_lanes/epk_policy_harness/epk_active_gamma_folded_tyr_terminal_blocker_decision_20260521T223100Z.json` (`sha256 56740b787a5585f2c34f8f4121c157e24033b3848eae4a163766f97b76deb7a7`).

## Regression gate status

No regression gate changed. The latest false-positive hunter handoff and gate reported `unsafe_nonabstention_after_expected_policy_count=0`; sibling-control inputs supplied review-only counteraxis context but no new unsafe non-abstention route.

## Verification

- Disk stayed above threshold: 29 GiB free at start; 26 GiB free at final pre-write check.
- `python -m json.tool artifacts/research_lanes/epk_policy_harness/epk_active_gamma_folded_tyr_terminal_blocker_decision_20260521T223100Z.json` passed before ledger append.
- `git diff --check -- artifacts/research_lanes/epk_policy_harness/epk_active_gamma_folded_tyr_terminal_blocker_decision_20260521T223100Z.json` passed before ledger append.
- Final JSON/JSONL validation passed after ledger append: 27 JSONL records parsed and the last record has `primary_outcome=candidate_class_terminal_no_go`.
- Final lane diff check passed for the decision artifact, run ledger, and handoff.
- No helper self-tests were run because no code changed.

## Git blockers and notes

- Normal `git fetch origin` failed on linked-worktree `FETCH_HEAD` permissions.
- `git fetch --no-write-fetch-head origin` succeeded.
- `git pull --ff-only origin research/epk-policy-harness` failed on linked-worktree `FETCH_HEAD` permissions.
- Local worktree/index were already stale/noisy from prior linked-worktree metadata blockers. Do not revert unrelated lane files.
- Final commit/push uses normal Git if possible; otherwise use the prior temporary-index remote-tip workflow and record the result in the assistant final response.

## Exact next query

`epk_active_gamma_nonreciprocal_role_policy_gate_design_review_only`

Do not pursue folded Tyr reciprocal active-gamma context as a source-free admission route under policy v0/v7. If this class is revisited, require a genuinely new preregistered source-free biology modality. Otherwise route reciprocal folded Tyr cases to source/biological review and use `8OXM`-like non-reciprocal active-gamma rows for future gate design.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
