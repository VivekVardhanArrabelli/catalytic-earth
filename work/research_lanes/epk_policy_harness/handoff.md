# ePK policy harness handoff

Last updated: 2026-05-21T22:21:09Z
Run started: 2026-05-21T21:30:24Z
Run ended: 2026-05-21T22:21:09Z
Measured minutes: 50.75
Primary outcome: `next_query_defined`

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_real_missing_coordinate_state_adapter.py`
- `artifacts/research_lanes/epk_policy_harness/epk_federated_real_lane_missing_coordinate_state_adapter_v9_20260521T213723Z*.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy status

Policy v0 remains frozen, review-only, and fail-closed. This run did not change production labels, thresholds, registries, fingerprints, migrations, or scoring, and it makes no production ePK readiness claim.

This run added the v9 real-lane missing-coordinate-state adapter. It reads compact candidate rows from the fetched ePK source branches with `git show`, adapts only source-free candidate-level fields, and emits a review-only scoreboard/contract. The adapter found real rows for `adp_state`, `ligand_absent`, and `unavailable_coordinate_state`; it did not find a real `metal_absent` row in the current fetched source artifacts.

## Evidence

- Report: `artifacts/research_lanes/epk_policy_harness/epk_federated_real_lane_missing_coordinate_state_adapter_v9_20260521T213723Z.json` (`sha256 e0f40be370aeca949c0dc389ca47aa28c52bc24b1e9da8311f5698af74749a75`).
- Tranche: `artifacts/research_lanes/epk_policy_harness/epk_federated_real_lane_missing_coordinate_state_adapter_v9_20260521T213723Z_tranche.json` (`sha256 fcab455797fe8d9c0b3f84938a21051ba3200a56c90f64e5ec9c132251db0d63`).
- Result: `artifacts/research_lanes/epk_policy_harness/epk_federated_real_lane_missing_coordinate_state_adapter_v9_20260521T213723Z_result.json` (`sha256 9d715255f43a4d9395fa3c5b2d4624b5b40cc7e54c0bfe442e969ad952f7d884`).
- Scoreboard gate: `artifacts/research_lanes/epk_policy_harness/epk_federated_real_lane_missing_coordinate_state_adapter_v9_20260521T213723Z_scoreboard_gate.json` (`sha256 0e0803e5b634336335143b5bc3fd1dbe31069c18eb386505e89daaf18aac41a0`).
- Contract gate: `artifacts/research_lanes/epk_policy_harness/epk_federated_real_lane_missing_coordinate_state_adapter_v9_20260521T213723Z_contract_gate.json` (`sha256 2c3eeecf9e13a1f9c1753ae92242fe041b66146b22b3278ed34c0f9104bbfe23`).

The positive v9 tranche reviewed 3 real candidate rows across 2 source lanes and 3 entries. Selected coordinate-state counts were `{"adp_state": 1, "ligand_absent": 1, "unavailable_coordinate_state": 1}`. Claim-status counts were `{"review_only_abstain_missing_role_policy": 1, "review_only_abstain_product_state": 1, "review_only_abstain_sibling_control": 1}`. The source-lane inventory had available target counts `{"adp_state": 3, "ligand_absent": 2, "unavailable_coordinate_state": 222}`.

The scoreboard gate passed with zero forbidden source leakage, zero unsafe control nonabstentions, `production_claim_allowed=false`, and `labels_or_fingerprints_changed=false`. The v9 contract gate recorded `metal_absent` as the only missing real target and set next query to `epk_real_lane_metal_absent_candidate_evidence_v10_review_only`.

V9 fault injections rejected:

- `source_context_copy`
- `missing_present_null_ligand`
- `missing_candidate_identity`

The generic v7 entry-precedence fault injection was recorded as inapplicable for this tranche shape because v9 intentionally selects only real missing-coordinate-state rows and no product/analog pair.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/*.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_real_missing_coordinate_state_adapter.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_schema_contract_lock.py --self-test`
- JSON validation before ledger append parsed 268 JSON files and 25 JSONL records.
- `git diff --check` passed before ledger append.
- Ten hold-open validation rounds repeated v9/core self-tests, diff checks, and disk checks from 2026-05-21T21:38:17Z through 2026-05-21T22:18:30Z.
- Disk stayed above threshold: 29 GiB free at start and 28 GiB free at final validation.

## Blockers and notes

- Normal `git fetch origin` failed on linked-worktree `FETCH_HEAD` permissions.
- `git fetch --no-write-fetch-head origin` succeeded.
- `git pull --ff-only origin research/epk-policy-harness` failed on linked-worktree `FETCH_HEAD` permissions.
- `git merge --ff-only origin/research/epk-policy-harness` failed on linked-worktree `ORIG_HEAD.lock` permissions.
- The local worktree/index remains stale and noisy because linked-worktree metadata blocks normal branch updates. Alternate-index commit/push will be attempted after this handoff is written.
- Other-lane source artifacts were read from fetched Git refs only. No production files, registries, fingerprints, migrations, labels, thresholds, or Git history were changed.

## Exact next query

`epk_real_lane_metal_absent_candidate_evidence_v10_review_only`

Find or add compact review-only candidate evidence from independent ePK lanes that emits a real `metal_absent` coordinate-state row with `local_metal_context=false`, candidate/source provenance fields, and no source text/protein names/EC/Rhea/PDB titles/paper metadata copied into predictive rows.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
