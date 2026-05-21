# ePK policy harness handoff

Last updated: 2026-05-21T21:19:45Z
Run started: 2026-05-21T20:29:30Z
Run ended: 2026-05-21T21:19:45Z
Measured minutes: 50.25
Primary outcome: `scoreboard_gate_created`

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py`
- `tools/research_lanes/epk_policy_harness/epk_federated_schema_contract_lock.py`
- `tools/research_lanes/epk_policy_harness/epk_federated_missing_coordinate_state_fixture.py`
- `artifacts/research_lanes/epk_policy_harness/epk_federated_schema_contract_missing_coordinate_state_fixture_v8_20260521T202930Z*.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy status

Policy v0 remains frozen, review-only, and fail-closed. This run did not change production labels, thresholds, registries, fingerprints, migrations, or scoring, and it makes no production ePK readiness claim.

This run added the v8 missing-coordinate-state fixture/gate. It exercises `adp_state`, `ligand_absent`, `metal_absent`, and `unavailable_coordinate_state`, the four coordinate states not positively observed in the v7 source bundle, while preserving candidate-level provenance, claim admissibility, and entry rollup checks.

The shared schema draft now includes coordinate-state-specific field rules: `ligand_absent` and `unavailable_coordinate_state` require the field `ligand_code_from_structure` to be present but may carry `null`, `metal_absent` requires `local_metal_context=false`, and `adp_state` remains a product-state abstention class.

## Evidence

- Report: `artifacts/research_lanes/epk_policy_harness/epk_federated_schema_contract_missing_coordinate_state_fixture_v8_20260521T202930Z.json` (`sha256 b169c74670fd0499ad6c2e6a5d549b07407d4e2abe91646c5e38a078aeb043ff`).
- Tranche: `artifacts/research_lanes/epk_policy_harness/epk_federated_schema_contract_missing_coordinate_state_fixture_v8_20260521T202930Z_tranche.json` (`sha256 bf73d5ac28cc756b3a295d29a05c31dac2946998b489b6f7183f2115fe334908`).
- Result: `artifacts/research_lanes/epk_policy_harness/epk_federated_schema_contract_missing_coordinate_state_fixture_v8_20260521T202930Z_result.json` (`sha256 14ada7f40838da13924f96b8c5f1dcbddd0ee2643b2969ca80ac952f87604264`).
- Scoreboard gate: `artifacts/research_lanes/epk_policy_harness/epk_federated_schema_contract_missing_coordinate_state_fixture_v8_20260521T202930Z_scoreboard_gate.json` (`sha256 c26be3f45dff45bcfb712951f7f563816946ae698cc562d4733695ebbb9ae23d`).
- Contract gate: `artifacts/research_lanes/epk_policy_harness/epk_federated_schema_contract_missing_coordinate_state_fixture_v8_20260521T202930Z_contract_gate.json` (`sha256 88948595ed69226bbf01874d8cce1621c22bc0d09b3d2a41282a11e5f3d74fc5`).

The positive v8 fixture reviewed 6 candidate rows from 4 source lanes across 5 entries. Coordinate-state counts were `{"adp_state": 1, "ligand_absent": 1, "metal_absent": 1, "product_state": 1, "substrate_acceptor_analog_state": 1, "unavailable_coordinate_state": 1}`. Claim-status counts were `{"review_only_abstain_analog_state": 1, "review_only_abstain_missing_role_policy": 2, "review_only_abstain_product_state": 2, "review_only_abstain_topology_ambiguity": 1}`. Entry status counts were `{"review_only_abstain_analog_state": 1, "review_only_abstain_missing_role_policy": 2, "review_only_abstain_product_state": 1, "review_only_abstain_topology_ambiguity": 1}`.

The scoreboard gate passed with zero forbidden source leakage, zero unsafe control nonabstentions, `production_claim_allowed=false`, and `labels_or_fingerprints_changed=false`. The product+analog anchor entry retained both candidate rows while rolling up to `review_only_abstain_analog_state` under fail-closed entry precedence.

The contract gate rejected all expected faults:

- `missing_candidate_provenance`
- `copied_source_context`
- `source_derived_predictive_feature`
- `invalid_coordinate_state`
- `invalid_claim_admissibility`
- `metadata_count_drift`
- `entry_rollup_precedence_drift`

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/*.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_missing_coordinate_state_fixture.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_schema_contract_lock.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_bridge_status_coverage_fault_injection.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_entry_precedence_controls.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_entry_rollup_stress.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_literal_product_split_overlap_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_real_overlap_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_state_diversity_gate.py --self-test`
- JSON validation before ledger append parsed 260 JSON files and 24 JSONL records.
- `git diff --check` passed before ledger append.
- Nine hold-open validation rounds repeated the v8 self-test, v7 schema self-test, scoreboard self-test, v8 report JSON parse, diff check, and disk check from 2026-05-21T20:39:46Z through 2026-05-21T21:17:59Z.
- Disk stayed above threshold: 29 GiB free at start and 29 GiB free at final validation.

## Blockers and notes

- Normal `git fetch origin` failed on linked-worktree `FETCH_HEAD` permissions.
- `git fetch --no-write-fetch-head origin research/epk-policy-harness` succeeded.
- `git pull --ff-only origin research/epk-policy-harness` failed on linked-worktree `FETCH_HEAD` permissions.
- The normal worktree/index remains stale and noisy because linked-worktree metadata blocks normal branch updates, so local `HEAD` is not expected to be clean or equal to the remote branch.
- Other-lane artifacts were not copied. No production files, registries, fingerprints, migrations, labels, thresholds, or Git history were changed.

## Exact next query

`epk_federated_real_lane_missing_coordinate_state_adapter_v9_review_only`

Look for compact existing lane outputs or safe adapters that can provide real review-only candidate rows for the newly fixture-locked coordinate-state rules, especially present-but-null ligand codes for ligand-absent or unavailable coordinate states, without copying source text/protein names/EC/Rhea/PDB titles/paper metadata.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
