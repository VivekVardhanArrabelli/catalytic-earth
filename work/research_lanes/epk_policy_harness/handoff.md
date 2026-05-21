# ePK policy harness handoff

Last updated: 2026-05-21T15:14:00Z
Run started: 2026-05-21T14:22:20Z
Run ended: 2026-05-21T15:14:00Z
Measured minutes: 51.67
Primary outcome: `scoreboard_gate_created`

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_policy_harness.py`
- `tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py`
- `tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py`
- `tools/research_lanes/epk_policy_harness/epk_federated_entry_rollup_stress.py`
- `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_cross_lane_expansion_v2_20260521T143200Z*.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy status

Policy v0 remains frozen, review-only, and fail-closed. This run did not change production labels, thresholds, registries, fingerprints, migrations, or scoring.

This run made `entry_id` first-class in policy decision rows and scoreboard rollups. The scoreboard now groups by `entry_id` before falling back to `pdb_id` and `row_id`, which lets federated candidate rows roll up shared entries even when a lane has compact candidate evidence without a stable PDB field. `entry_id`, `source_lane_id`, `source_artifact`, `source_row_key`, and `source_row_id` remain review-only provenance and are not predictive features.

## Evidence

- Stress report: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_cross_lane_expansion_v2_20260521T143200Z.json` (`sha256 ebfad90696e7f683e47337ff51fa3f4bf1ca55e7ca5915bf0732c590a60da959`).
- Stress tranche: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_cross_lane_expansion_v2_20260521T143200Z_tranche.json` (`sha256 f040857d457051ec37f5f8584fcb9886d32d4550616d9ba796dd7c72a49ccf3e`).
- Policy result: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_cross_lane_expansion_v2_20260521T143200Z_result.json` (`sha256 f4a5320dcf88e659a028a10a1bfa7b19b5151ce82f66bd6cae38cc3b9deab42b`).
- Scoreboard gate: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_cross_lane_expansion_v2_20260521T143200Z_scoreboard_gate.json` (`sha256 5bd142bfea0285eab6baaf0e700b17e3d92ff2cecc697eaaf1841b292c212188`).

The compact stress fixture reviewed 16 candidate rows from four source lanes and produced 8 entry rollups. Candidate and entry coverage includes every non-forbidden claim status and every coordinate-state enum. Entry rollups show fail-closed precedence: product over active, analog over product, split over analog, sibling-control over active, topology ambiguity over active, forbidden-context over missing-role, missing-role only, and review-only nonabstaining-only.

The positive scoreboard gate passed with 0 forbidden source-leakage rows, 0 unsafe control nonabstentions, and `production_claim_allowed=false`. Negative fixtures rejected mixed-entry forbidden source leakage, mixed-entry unsafe control nonabstention, and missing candidate/source identity.

The federated adapter input pointer was updated to the latest false-positive compact gate `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_141548Z.json`; a dry run in `/private/tmp/epk_federated_adapter_latest_input_check` passed without adding extra repository artifacts.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/*.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_entry_rollup_stress.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_bridge_status_coverage_fault_injection.py --self-test`
- Latest false-positive adapter-input dry run wrote only to `/private/tmp/epk_federated_adapter_latest_input_check`.
- Eight hold-open validation rounds repeated policy, scoreboard, entry-rollup stress, adapter self-tests, and new-artifact JSON parsing through 2026-05-21T15:12:09Z.
- `git diff --check`
- JSON validation parsed 221 JSON files and 18 JSONL records before ledger append.
- Disk remained above the safety threshold: 28 GiB available before wrap.

## Blockers and notes

- Normal `git fetch origin` failed on linked-worktree `FETCH_HEAD` permissions.
- `git fetch --no-write-fetch-head origin` succeeded.
- `git pull --ff-only origin research/epk-policy-harness` failed on linked-worktree `FETCH_HEAD`.
- The local worktree/index remains stale and noisy because linked-worktree metadata blocks normal branch updates. Use an alternate index seeded from `origin/research/epk-policy-harness` for commit/push.
- Other-lane handoffs were read as review-only inputs. No additional remote ePK lane branch was available beyond positive evidence, substrate-role identity, false-positive hunter, and sibling controls.

## Exact next query

`epk_federated_candidate_entry_rollup_real_entry_overlap_v3_review_only`

Find real overlapping entries/candidates emitted independently by the federated lanes and feed them through the entry-id-first rollup. Keep source/protein/title/EC/Rhea/paper/prose fields out of predictive rows; source review remains discovery/review context only. Continue to fail on forbidden source leakage, unsafe control nonabstention, missing candidate/source identity, duplicate candidate identity within source lane, and any entry rollup that converts review-only signal into progress or production claims.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
