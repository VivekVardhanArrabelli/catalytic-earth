# ePK policy harness handoff

Last updated: 2026-05-21T18:17:48Z
Run started: 2026-05-21T17:27:00Z
Run ended: 2026-05-21T18:17:48Z
Measured minutes: 50.80
Primary outcome: `scoreboard_gate_created`

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py`
- `tools/research_lanes/epk_policy_harness/epk_federated_literal_product_split_overlap_gate.py`
- `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_literal_product_split_real_overlap_v5_20260521T172700Z*.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy status

Policy v0 remains frozen, review-only, and fail-closed. This run did not change production labels, thresholds, registries, fingerprints, migrations, or scoring. It does not claim production ePK readiness.

This run added a real-overlap literal product/split v5 gate. It uses the newer substrate-role phosphoproduct audit as a review-only emitting-lane input, keeps candidate rows visible, and admits literal `product_state` and `split_state` only as review-only policy decisions.

The adapter now preserves terminal-gamma-absent nucleotide codes and nearest source-free distances for substrate-role phosphoproduct rows. Product/split chemistry remains an abstaining coordinate state, not a production substrate-role rule.

## Evidence

- Report: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_literal_product_split_real_overlap_v5_20260521T172700Z.json` (`sha256 aa58862ea879872633c87eebbd2ed835d7fc07b0bd9badf7d2b6c4d63d6a0c27`).
- Tranche: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_literal_product_split_real_overlap_v5_20260521T172700Z_tranche.json` (`sha256 3a15368fa3545ed4de7c4a32967c8cbe15be4b156616797ce32fe92644cdb04d`).
- Policy result: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_literal_product_split_real_overlap_v5_20260521T172700Z_result.json` (`sha256 4a092f922998de0a41a6d5e99fd7e141749f0980cbc93f754761f829c8e4729c`).
- Scoreboard gate: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_literal_product_split_real_overlap_v5_20260521T172700Z_scoreboard_gate.json` (`sha256 647ad143128d7fa5acb4b362e531c9a9baeadfe39d59fcfe03fcc4599eefc993`).

The scanner found 41 available cross-lane overlapping entries and 5 literal product/split overlap rows in the newer substrate-role audit. It selected `3QHW`, `3QHR`, and `4HPU`, each with independent `epk_positive_evidence` plus `epk_substrate_role_identity` support.

Selected coordinate-state counts: `{"active_gamma": 1, "product_state": 4, "split_state": 1, "substrate_acceptor_analog_state": 2}`. Claim-status counts: `{"review_only_abstain_analog_state": 2, "review_only_abstain_missing_role_policy": 1, "review_only_abstain_product_state": 4, "review_only_abstain_split_state": 1}`.

The scoreboard passed with zero forbidden source-leakage rows, zero unsafe control nonabstentions, zero expected claim-status mismatches, and `production_claim_allowed=false`.

Negative fixtures rejected:

- Single-lane entry drift: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_literal_product_split_real_overlap_v5_20260521T172700Z_negative_single_lane_entry_result.json`.
- Missing literal split-state coverage: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_literal_product_split_real_overlap_v5_20260521T172700Z_negative_missing_literal_state_result.json`.
- Literal product/split nonabstention: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_literal_product_split_real_overlap_v5_20260521T172700Z_negative_literal_state_nonabstention_result.json`.
- Copied source/protein context: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_literal_product_split_real_overlap_v5_20260521T172700Z_negative_source_context_copy_result.json`.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/*.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_literal_product_split_overlap_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_state_diversity_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_real_overlap_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_entry_rollup_stress.py --self-test`
- Nine hold-open validation rounds repeated v5, policy, and scoreboard checks plus new artifact JSON parsing through 2026-05-21T18:17:31Z.
- JSON validation before ledger append parsed 244 JSON files and 21 JSONL records.
- `git diff --check` passed before ledger append.
- Disk stayed above threshold: 24 GiB available at start and 28 GiB available in the final hold-open round.

## Blockers and notes

- Normal `git fetch origin` failed on linked-worktree `FETCH_HEAD` permissions.
- `git fetch --no-write-fetch-head origin` succeeded.
- `git pull --ff-only origin research/epk-policy-harness` failed on linked-worktree `FETCH_HEAD`.
- The normal worktree/index remains stale and noisy because linked-worktree metadata blocks normal branch updates, so local `HEAD` is not expected to be clean or equal to the remote branch.
- Other-lane artifacts were read as review-only inputs. No production files, registries, fingerprints, migrations, labels, thresholds, or Git history were changed.

## Exact next query

`epk_federated_literal_product_split_entry_precedence_controls_v6_review_only`

Stress entry-level precedence when literal product/split candidate rows coexist with analog, sibling-control, topology, and forbidden-source contexts. Candidate-level product/split rows should remain visible and review-only, while forbidden source leakage and unsafe control nonabstention must still block progress claims.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
