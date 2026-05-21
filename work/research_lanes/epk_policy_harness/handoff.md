# ePK policy harness handoff

Last updated: 2026-05-21T20:28:08Z
Run started: 2026-05-21T19:29:01Z
Run ended: 2026-05-21T20:28:08Z
Measured minutes: 59.12
Primary outcome: `schema_frozen_review_only`

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_federated_schema_contract_lock.py`
- `tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py`
- `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_schema_contract_lock_v7_20260521T192901Z*.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy status

Policy v0 remains frozen, review-only, and fail-closed. This run did not change production labels, thresholds, registries, fingerprints, migrations, or scoring, and it makes no production ePK readiness claim.

This run added the v7 federated schema-contract lock. It validates the v6 positive candidate/entry precedence bundle as a positive input and locks the schema around candidate identity, policy decision identity, coordinate-state enums, claim-status enums, claim admissibility, and entry rollups derived from candidate decisions.

The shared schema draft now makes `source_lane_id`, `source_artifact`, `source_row_key`, `source_row_id`, and `entry_id` explicit required fields for `epk_candidate_evidence_v1`, and adds required entry-rollup fields to `epk_scoreboard_row_v1`.

## Evidence

- Report: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_schema_contract_lock_v7_20260521T192901Z.json` (`sha256 81dfd6671da148ac08e218ef4e05fa66cef89d85d1b27816f51c9dea82ab34ea`).
- Gate: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_schema_contract_lock_v7_20260521T192901Z_gate.json` (`sha256 78cb454adbd6ca66dc190c934a356cffe096258cf30fecb58bdba3489463bbe6`).
- Schema: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_schema_contract_lock_v7_20260521T192901Z_schema.json` (`sha256 d394802c1616a5c5c859f08f59b3b945fe24e9135677fbc4ac02709a7226b3c3`).
- Source v6 tranche: `artifacts/research_lanes/epk_policy_harness/epk_federated_literal_product_split_entry_precedence_controls_v6_20260521T182727Z_tranche.json` (`sha256 c3e8a6217d04dd3af9eabe006e067f393da703c89acf425774211eaa1a5e04da`).
- Source v6 result: `artifacts/research_lanes/epk_policy_harness/epk_federated_literal_product_split_entry_precedence_controls_v6_20260521T182727Z_result.json` (`sha256 8f08d0328134a2c9b7b0dbd43d1cb41f74df8541579014dc35117a1e5e903d47`).
- Source v6 scoreboard gate: `artifacts/research_lanes/epk_policy_harness/epk_federated_literal_product_split_entry_precedence_controls_v6_20260521T182727Z_scoreboard_gate.json` (`sha256 9676bbafd767e88ce85fbffba21992fef3eda6217c6f6e60c578f50f4e679c38`).

The positive v7 contract reviewed 14 policy rows from 4 source lanes and preserved candidate coordinate-state counts: `{"active_gamma": 5, "ambiguous_coordinate_state": 1, "product_state": 5, "split_state": 1, "substrate_acceptor_analog_state": 2}`.

Entry rollups were recomputed from policy result rows and matched the v6 scoreboard for 8 entries with entry status counts `{"review_only_abstain_analog_state": 2, "review_only_abstain_sibling_control": 5, "review_only_abstain_topology_ambiguity": 1}`.

Expected fault rejections all passed:

- `missing_candidate_provenance`
- `copied_source_context`
- `source_derived_predictive_feature`
- `invalid_coordinate_state`
- `invalid_claim_admissibility`
- `metadata_count_drift`
- `entry_rollup_precedence_drift`

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/*.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_schema_contract_lock.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_entry_precedence_controls.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_literal_product_split_overlap_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_real_overlap_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_state_diversity_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_entry_rollup_stress.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_bridge_status_coverage_fault_injection.py --self-test`
- JSON validation before ledger append parsed 255 JSON files and 23 JSONL records.
- `git diff --check` passed before ledger append.
- Nine hold-open validation rounds repeated the v7 self-test, scoreboard self-test, v7 report JSON parsing, diff check, and disk check from 2026-05-21T19:39:45Z through 2026-05-21T20:19:46Z.
- Disk stayed above threshold: 30 GiB free at start and 29 GiB free at final validation.

## Blockers and notes

- Normal `git fetch origin` failed on linked-worktree `FETCH_HEAD` permissions.
- `git fetch --no-write-fetch-head origin` succeeded.
- `git pull --ff-only origin research/epk-policy-harness` failed on linked-worktree `FETCH_HEAD` permissions.
- The normal worktree/index remains stale and noisy because linked-worktree metadata blocks normal branch updates, so local `HEAD` is not expected to be clean or equal to the remote branch.
- Other-lane artifacts were used only through the prior v6 review-only bundle. No production files, registries, fingerprints, migrations, labels, thresholds, or Git history were changed.

## Exact next query

`epk_federated_schema_contract_missing_coordinate_state_fixture_v8_review_only`

Add a compact review-only v8 fixture/gate that exercises the coordinate states not positively observed in v7's source bundle (`adp_state`, `ligand_absent`, `metal_absent`, and `unavailable_coordinate_state`) while preserving the same source-leakage, provenance, and entry-rollup contract.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
