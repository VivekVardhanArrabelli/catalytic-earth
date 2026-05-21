# ePK policy harness handoff

Last updated: 2026-05-21T12:22:54Z
Run started: 2026-05-21T05:35:31Z
Run ended: 2026-05-21T12:22:54Z
Measured minutes: 407.38
Primary outcome: `scoreboard_gate_created`

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

- Adapter report: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z.json` (`sha256 74d2ee7f7022e6299441ada30e632354c5fc030ec78532dc83eab9b214680a78`).
- Tranche: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z_tranche.json` (`sha256 7dd3ddd0d8fd961425aadfc80a9c4c4ea31a8fa06d0ca81957e8328f8f1eef87`).
- Policy result: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z_result.json` (`sha256 f4e7ecda9c8dbba081a7cfe990dec2246170f31a6f6d2498e68c10818a8fd026`).
- Scoreboard gate: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z_scoreboard_gate.json` (`sha256 38e65b551331391a2af2e6a946655b6c01aa55e11d24665fa183454ce75fe7c9`).
- Negative missing-identity fixture: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z_negative_missing_candidate_identity_result.json` (`sha256 e529033a42364b9b7f6973af3fcf4bcf57d07625db32647df83820be8c76eaa7`).
- Adapted rows: 10 across 4 source lanes: epk_false_positive_hunter, epk_positive_evidence, epk_sibling_controls, epk_substrate_role_identity.
- Claim statuses: `{'review_only_abstain_analog_state': 1, 'review_only_abstain_missing_role_policy': 3, 'review_only_abstain_product_state': 1, 'review_only_abstain_sibling_control': 5}`.
- Coordinate states: `{'active_gamma': 7, 'adp_state': 1, 'product_state': 1, 'substrate_acceptor_analog_state': 1}`.
- Gate status: pass with zero forbidden source leakage, zero unsafe control nonabstention, and zero expected claim-status mismatches.
- Missing candidate identity fault was rejected with missing `candidate_id`, `source_lane_id`, and `source_artifact`.
- Source text/protein-name copy grep over new artifacts was clean for copied titles, protein names, citation titles, and `source_context` blobs.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/*.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_bridge_status_coverage_fault_injection.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py --self-test`
- JSON validation before ledger append parsed 204 JSON files and 15 JSONL records.
- `git diff --check` passed.
- Non-writing frozen-v0 tranche stress remains 58/60 passing; the same two older interim ATP surface tranches fail the preexisting search-surface artifact citation validator.

## Blockers and notes

- Normal `git fetch origin` and `git pull --ff-only origin research/epk-policy-harness` remain blocked by linked-worktree metadata permissions on `FETCH_HEAD`.
- `git fetch --no-write-fetch-head origin research/epk-policy-harness` succeeds.
- The normal index remains stale/noisy; use an alternate index seeded from `origin/research/epk-policy-harness` for validation and commit.
- The adapter smoke is compatibility/gate regression evidence only, not held-out biological performance evidence, not production scoring, and not claim readiness.

## Exact next query

`epk_federated_candidate_adapter_schema_contract_expand_v1_review_only`

Expand the federated adapter schema contract to require lane-native schema provenance and a compact entry-level rollup derivation, then add expected-failure fixtures for missing source-lane provenance and entry-level status computed directly from PDB-level rows.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
