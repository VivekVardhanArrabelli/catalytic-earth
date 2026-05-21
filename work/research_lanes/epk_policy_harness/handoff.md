# ePK policy harness handoff

Last updated: 2026-05-21T17:14:46Z
Run started: 2026-05-21T16:24:56Z
Run ended: 2026-05-21T17:14:46Z
Measured minutes: 49.83
Primary outcome: `scoreboard_gate_created`

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_federated_state_diversity_gate.py`
- `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_overlap_state_diversity_v4_20260521T162456Z*.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy status

Policy v0 remains frozen, review-only, and fail-closed. This run did not change production labels, thresholds, registries, fingerprints, migrations, or scoring. It does not claim production ePK readiness.

This run added a real-overlap state-diversity v4 gate. It scans existing independent ePK lane outputs, selects compact candidate rows only for entries emitted by at least two source lanes, and requires the selected tranche to cover the coordinate states currently present in real-overlap representative rows.

## Evidence

- Report: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_overlap_state_diversity_v4_20260521T162456Z.json` (`sha256 6746c47ef5e51cc950af25ef6de0be942355bc333f1104ac0a93a480876b53bf`).
- Tranche: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_overlap_state_diversity_v4_20260521T162456Z_tranche.json` (`sha256 9037e844031c4cf775df5bd00f13ceb8fcc062de9505403e8bde60a35dba8798`).
- Policy result: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_overlap_state_diversity_v4_20260521T162456Z_result.json` (`sha256 4a50bf8740e7227a725d89949d9f65165e218177784a36ba7b6c88a8baec409a`).
- Scoreboard gate: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_overlap_state_diversity_v4_20260521T162456Z_scoreboard_gate.json` (`sha256 add4f64f4ab532837f56c6590d59397ab8c2cbd017434aad9f6901723152296e`).

The scanner found 41 real cross-lane overlapping entries and selected 3QHW, 9NBW, 4HPU. The selected tranche reviewed 6 candidate rows across 3 entry rollups.

Selected coordinate-state counts: `{"active_gamma": 2, "adp_state": 1, "ambiguous_coordinate_state": 1, "substrate_acceptor_analog_state": 1, "unavailable_coordinate_state": 1}`. Claim-status counts: `{"review_only_abstain_analog_state": 1, "review_only_abstain_missing_role_policy": 2, "review_only_abstain_product_state": 1, "review_only_abstain_sibling_control": 1, "review_only_abstain_topology_ambiguity": 1}`.

The scoreboard passed with zero forbidden source-leakage rows, zero unsafe control nonabstentions, zero expected claim-status mismatches, and `production_claim_allowed=false`.

Negative fixtures rejected:

- Single-lane entry drift: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_overlap_state_diversity_v4_20260521T162456Z_negative_single_lane_entry_result.json`.
- Missing required state diversity: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_overlap_state_diversity_v4_20260521T162456Z_negative_missing_state_diversity_result.json`.
- Copied source/protein context: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_overlap_state_diversity_v4_20260521T162456Z_negative_source_context_copy_result.json`.
- Unsafe control nonabstention: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_overlap_state_diversity_v4_20260521T162456Z_negative_unsafe_control_nonabstention_result.json`.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/*.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_state_diversity_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_real_overlap_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_entry_rollup_stress.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_bridge_status_coverage_fault_injection.py --self-test`
- Nine hold-open validation rounds repeated v4, policy, and scoreboard checks plus new artifact JSON parsing through 2026-05-21T17:12:56Z.
- JSON validation before ledger append parsed 236 JSON files and 20 JSONL records.
- Final JSON validation after ledger append parsed 236 JSON files and 21 JSONL records.
- `git diff --check` passed before and after ledger append.
- Disk stayed above threshold: 27 GiB available at start and final check.

## Blockers and notes

- Normal `git fetch origin` failed on linked-worktree `FETCH_HEAD` permissions.
- `git fetch --no-write-fetch-head origin` succeeded.
- `git pull --ff-only origin research/epk-policy-harness` failed on linked-worktree `FETCH_HEAD`.
- The normal worktree/index remains stale and noisy because linked-worktree metadata blocks normal branch updates. Preserve coherent lane outputs and use alternate-index commit/push if normal Git remains blocked.
- Other-lane artifacts were read as review-only inputs. No production files, registries, fingerprints, migrations, labels, thresholds, or Git history were changed.

## Exact next query

`epk_federated_candidate_entry_rollup_literal_product_split_real_overlap_v5_review_only`

Find real cross-lane overlapping entries that include literal `product_state` and `split_state` coordinate rows across independent emitting lanes. Keep ADP/product-state rows review-only, preserve candidate-level evidence, and keep source/protein/title/EC/Rhea/paper/prose fields out of predictive rows.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
