# ePK policy harness handoff

Last updated: 2026-05-21T12:27:55Z
Run started: 2026-05-21T05:35:31Z
Run ended: 2026-05-21T12:27:55Z
Measured minutes: 412.4
Primary outcome: `scoreboard_gate_created`
Pushed content commits: `f48ace7ef7eccd1482717a640b6e67302f855e18`, `6be5d732790f25b27d0e79d3bccdb5e65fe1dacb`. Verify the current remote ref directly because handoff/status-only commits may follow.

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_policy_harness.py`
- `tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py`
- `tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py`
- `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z*.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy status

Policy v0 remains frozen, review-only, and fail-closed. This run did not change production labels, thresholds, registries, fingerprints, migrations, scoring paths, or production claim readiness. The federated adapter smoke reads other ePK lane artifacts only through git object reads as review-only inputs and writes compact policy-harness artifacts only under this lane.

## Evidence

- Adapter report: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z.json` (`sha256 d9083c4b862c90ac8c2fbff5b3713c4a92e5d745d56c36db1886f7c4cfa0efe5`).
- Tranche: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z_tranche.json` (`sha256 edbd340ea9896c9f508329bcc3900c3b415170d001453a6eaa5460ea5079ef43`).
- Policy result: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z_result.json` (`sha256 9a8faf485a8149ebb3f482ff2168d06568d9a269edd0cf162c6dcf1e88ad934a`).
- Scoreboard gate: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z_scoreboard_gate.json` (`sha256 074803343edf2438b8088282aca92f0d1b58199afb8c6e58db88e50809ab156f`).
- `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z_negative_missing_candidate_identity_result.json` (`sha256 c966e21ed8c7f093cb3840d9486d2d5bd8b591fb2cc6cddb884b03f7d4a2f728`): missing_candidate_identity rejected.
- `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z_negative_duplicate_candidate_identity_result.json` (`sha256 1f739411bc3f79fda1e5f352130dd4fd3c7d7b854ad89a9001873e7c4ee4df1d`): duplicate_candidate_identity rejected.
- `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z_negative_source_context_copy_result.json` (`sha256 ebc8dd085caed42ebb562aa4f0dc7731441d4b905d7b28ffc592d1b21da5954c`): source_context_copy rejected.
- Adapted rows: 10 across 4 source lanes: epk_false_positive_hunter, epk_positive_evidence, epk_sibling_controls, epk_substrate_role_identity.
- Claim statuses: `{'review_only_abstain_analog_state': 1, 'review_only_abstain_missing_role_policy': 3, 'review_only_abstain_product_state': 1, 'review_only_abstain_sibling_control': 5}`.
- Coordinate states: `{'active_gamma': 7, 'adp_state': 1, 'product_state': 1, 'substrate_acceptor_analog_state': 1}`.
- Gate status: pass with zero forbidden source leakage, zero unsafe control nonabstention, and zero expected claim-status mismatches.
- Federated contract validation rejects missing candidate identity, duplicate candidate identity within a source lane, and copied source context/protein names.
- Source text/protein-name copy grep over new artifacts was clean for copied titles, protein names, citation titles, and `source_context` blobs outside the explicit expected-failure artifact name.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/*.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_bridge_status_coverage_fault_injection.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py --self-test`
- JSON validation parsed 206 JSON files and 16 JSONL records after final cleanup.
- `git diff --check` passed before commit.
- Non-writing frozen-v0 tranche stress remains 58/60 passing; the same two older interim ATP surface tranches fail the preexisting search-surface artifact citation validator.

## Blockers and notes

- Normal `git fetch origin` and `git pull --ff-only origin research/epk-policy-harness` remain blocked by linked-worktree metadata permissions on `FETCH_HEAD`.
- `git fetch --no-write-fetch-head origin research/epk-policy-harness` succeeds.
- Remote push succeeded via alternate-index commits; local linked-worktree `HEAD` update failed on `HEAD.lock`, so verify `origin/research/epk-policy-harness` directly.
- The normal index remains stale/noisy; use an alternate index seeded from `origin/research/epk-policy-harness` for validation and commit.
- The adapter smoke is compatibility/gate regression evidence only, not held-out biological performance evidence, not production scoring, and not claim readiness.

## Exact next query

`epk_federated_candidate_entry_rollup_contract_v1_review_only`

Add a compact entry-level rollup derivation from candidate decisions and expected-failure fixtures for any row that computes admissibility directly from PDB-level evidence instead of candidate-level policy decisions.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
