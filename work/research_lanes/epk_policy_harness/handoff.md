# ePK policy harness handoff

Last updated: 2026-05-21T19:16:54Z
Run started: 2026-05-21T18:27:27Z
Run ended: 2026-05-21T19:16:54Z
Measured minutes: 49.45
Primary outcome: `scoreboard_gate_created`

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_federated_entry_precedence_controls.py`
- `tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py`
- `artifacts/research_lanes/epk_policy_harness/epk_federated_literal_product_split_entry_precedence_controls_v6_20260521T182727Z*.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy status

Policy v0 remains frozen, review-only, and fail-closed. This run did not change production labels, thresholds, registries, fingerprints, migrations, or scoring. It does not claim production ePK readiness.

This run added the v6 entry-precedence regression gate. It reuses the v5 literal product/split real-overlap rows, adds compact topology/contact and control rows from existing review-only lane outputs, and verifies that entry-level status is derived from candidate-level decisions without losing candidate-state visibility.

The shared scoreboard self-test now also covers split/topology precedence and forbidden-over-sibling precedence. This keeps the entry-rollup behavior in the common gate rather than only in the v6 generator.

## Evidence

- Report: `artifacts/research_lanes/epk_policy_harness/epk_federated_literal_product_split_entry_precedence_controls_v6_20260521T182727Z.json` (`sha256 646cf922f2bf4c1f9f00aab31ef6832a878bdbb12ed44afbff19ddf341a21ac9`).
- Tranche: `artifacts/research_lanes/epk_policy_harness/epk_federated_literal_product_split_entry_precedence_controls_v6_20260521T182727Z_tranche.json` (`sha256 c3e8a6217d04dd3af9eabe006e067f393da703c89acf425774211eaa1a5e04da`).
- Policy result: `artifacts/research_lanes/epk_policy_harness/epk_federated_literal_product_split_entry_precedence_controls_v6_20260521T182727Z_result.json` (`sha256 8f08d0328134a2c9b7b0dbd43d1cb41f74df8541579014dc35117a1e5e903d47`).
- Scoreboard gate: `artifacts/research_lanes/epk_policy_harness/epk_federated_literal_product_split_entry_precedence_controls_v6_20260521T182727Z_scoreboard_gate.json` (`sha256 9676bbafd767e88ce85fbffba21992fef3eda6217c6f6e60c578f50f4e679c38`).

The positive v6 scoreboard reviewed 14 candidate rows across 8 entries and passed with zero forbidden source leakage, zero unsafe control nonabstentions, and `production_claim_allowed=false`.

Candidate-level coordinate-state counts stayed visible: `{"active_gamma": 5, "ambiguous_coordinate_state": 1, "product_state": 5, "split_state": 1, "substrate_acceptor_analog_state": 2}`.

Entry-level precedence assertions passed:

- `3QHR` and `3QHW`: product + analog rows roll up to `review_only_abstain_analog_state`.
- `4HPU`: split + topology rows roll up to `review_only_abstain_topology_ambiguity`.
- `1E4E`, `3FGU`, `4KFT`, `5UJ7`, and `9NBO`: control rows roll up to `review_only_abstain_sibling_control`.

Expected-failure gates:

- Forbidden-source leakage result: `artifacts/research_lanes/epk_policy_harness/epk_federated_literal_product_split_entry_precedence_controls_v6_20260521T182727Z_negative_forbidden_source_leakage_result.json`.
- Forbidden-source leakage scoreboard: `artifacts/research_lanes/epk_policy_harness/epk_federated_literal_product_split_entry_precedence_controls_v6_20260521T182727Z_negative_forbidden_source_leakage_scoreboard_gate.json` failed as expected with one `forbidden_source_leakage` row.
- Unsafe-control nonabstention result: `artifacts/research_lanes/epk_policy_harness/epk_federated_literal_product_split_entry_precedence_controls_v6_20260521T182727Z_negative_unsafe_control_nonabstention_result.json`.
- Unsafe-control nonabstention scoreboard: `artifacts/research_lanes/epk_policy_harness/epk_federated_literal_product_split_entry_precedence_controls_v6_20260521T182727Z_negative_unsafe_control_nonabstention_scoreboard_gate.json` failed as expected with five unsafe control nonabstentions.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/*.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_entry_precedence_controls.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_literal_product_split_overlap_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_real_overlap_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_state_diversity_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_entry_rollup_stress.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_bridge_status_coverage_fault_injection.py --self-test`
- JSON validation before ledger append parsed 252 JSON files and 22 JSONL records.
- `git diff --check` passed for the changed v6/gate files and artifacts before ledger append.
- Eight hold-open validation rounds repeated the v6 self-test, scoreboard self-test, v6 JSON parsing, diff check, and disk check from 2026-05-21T18:40:02Z through 2026-05-21T19:15:03Z.
- Disk stayed above threshold: 29 GiB free at start and 30 GiB free at final validation.

## Blockers and notes

- Normal `git fetch origin` failed on linked-worktree `FETCH_HEAD` permissions.
- `git fetch --no-write-fetch-head origin` succeeded.
- `git pull --ff-only origin research/epk-policy-harness` failed on linked-worktree `FETCH_HEAD`.
- The normal worktree/index remains stale and noisy because linked-worktree metadata blocks normal branch updates, so local `HEAD` is not expected to be clean or equal to the remote branch.
- Other-lane artifacts were read as review-only inputs. No production files, registries, fingerprints, migrations, labels, thresholds, or Git history were changed.

## Exact next query

`epk_federated_candidate_entry_rollup_schema_contract_lock_v7_review_only`

Lock the schema/scoreboard contract around the candidate identity, coordinate-state, claim-status, and entry-rollup fields that v3-v6 now depend on. The goal is a compact schema-contract gate that rejects missing candidate provenance, copied source context, source-derived predictive fields, invalid coordinate states, invalid claim admissibility, metadata count drift, and entry-rollup precedence drift.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
