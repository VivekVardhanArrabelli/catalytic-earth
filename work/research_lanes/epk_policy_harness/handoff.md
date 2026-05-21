# ePK policy harness handoff

Last updated: 2026-05-21T16:14:59Z
Run started: 2026-05-21T15:24:22Z
Run ended: 2026-05-21T16:14:59Z
Measured minutes: 50.62
Primary outcome: `scoreboard_gate_created`

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_federated_real_overlap_gate.py`
- `tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py`
- `tools/research_lanes/epk_policy_harness/epk_federated_entry_rollup_stress.py`
- `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_entry_overlap_v3_20260521T152422Z*.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy status

Policy v0 remains frozen, review-only, and fail-closed. This run did not change production labels, thresholds, registries, fingerprints, migrations, or scoring. It does not claim production ePK readiness.

This run created a real-overlap federated entry gate. It scans existing review-only artifacts from positive evidence, substrate-role identity, false-positive hunter, and sibling controls; finds entries shared by at least two independent lanes; adapts one compact candidate row per represented lane/entry into the shared candidate schema; then evaluates the rows through the policy bridge and scoreboard rollup.

`entry_id` is required for this real-overlap gate. The gate fails if any selected entry has candidate rows from only one source lane. Source lane provenance remains review-only context and is not predictive.

## Evidence

- Report: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_entry_overlap_v3_20260521T152422Z.json` (`sha256 60f6321568f3377de85a6d312f65139017eb4b1d166915f635d7cbe7ba491ca4`).
- Tranche: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_entry_overlap_v3_20260521T152422Z_tranche.json` (`sha256 2b0dcdb23a33796c8126d391972372ef7622c50979c6db7b1eb4b3fb2e6fb300`).
- Policy result: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_entry_overlap_v3_20260521T152422Z_result.json` (`sha256 2915ed5a34c596c146f305e52f85e341e59ba27334fcee5cf53723260e9ff8b1`).
- Scoreboard gate: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_entry_overlap_v3_20260521T152422Z_scoreboard_gate.json` (`sha256 16b21973b0ba8944ccd8acbcfdf3b582a750f01b971684bd73763d35cd100662`).

The scanner found 41 entries overlapping across at least two independent lane outputs and selected 12 compact entries: 6U1D, 6U1E, 9NBW, 4EKK, 7ZDU, 9UUR, 9UUX, 9UW4, 2JJ2, 5C1O, 8W2J, 1QHA. The selected tranche reviewed 26 candidate rows and 12 entry rollups. `6U1D` and `6U1E` were covered by substrate-role, false-positive, and sibling-control lanes; the remaining selected entries were two-lane overlaps.

The scoreboard passed with claim-status counts `{"review_only_abstain_missing_role_policy": 18, "review_only_abstain_sibling_control": 8}` and coordinate-state counts `{"active_gamma": 26}`. It had zero forbidden source-leakage rows, zero unsafe control nonabstentions, zero expected-decision mismatches, zero expected-claim-status mismatches, and `production_claim_allowed=false`.

Negative fixtures rejected:

- Single-lane entry drift: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_entry_overlap_v3_20260521T152422Z_negative_single_lane_entry_result.json`.
- Missing `entry_id`: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_entry_overlap_v3_20260521T152422Z_negative_missing_entry_id_result.json`.
- Copied source/protein context: `artifacts/research_lanes/epk_policy_harness/epk_federated_candidate_entry_rollup_real_entry_overlap_v3_20260521T152422Z_negative_source_context_copy_result.json`.

The federated adapter and synthetic entry-rollup provenance pointers now reference the latest false-positive regression gate `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_152108Z.json`. A dry run wrote only to `/private/tmp/epk_federated_adapter_latest_152108_check`.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/*.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_real_overlap_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_bridge_status_coverage_fault_injection.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_entry_rollup_stress.py --self-test`
- Latest false-positive adapter-input dry run wrote only to `/private/tmp/epk_federated_adapter_latest_152108_check`.
- Eight hold-open validation rounds repeated real-overlap, policy, and scoreboard self-tests plus real-overlap JSON parsing through 2026-05-21T16:10:18Z.
- Final validation at 2026-05-21T16:13:29Z parsed 228 JSON files and 19 JSONL records before ledger append, then `git diff --check` passed.
- Disk stayed above the safety threshold: 28 GiB available at start, 27 GiB available at final validation.

## Blockers and notes

- Normal `git fetch origin` failed on linked-worktree `FETCH_HEAD` permissions.
- `git fetch --no-write-fetch-head origin` succeeded.
- `git pull --ff-only origin research/epk-policy-harness` failed on linked-worktree `FETCH_HEAD`.
- The local worktree/index remains stale and noisy because linked-worktree metadata blocks normal branch updates. Use an alternate index seeded from `origin/research/epk-policy-harness` for commit/push.
- Other-lane handoffs were read as review-only inputs. No production files, registries, fingerprints, migrations, labels, thresholds, or Git history were changed.

## Exact next query

`epk_federated_candidate_entry_rollup_real_overlap_state_diversity_v4_review_only`

Find real cross-lane overlapping entries that exercise product/ADP/analog/split/topology coordinate states, not just active-gamma and sibling/missing-role cases. Preserve the real-overlap requirement that every selected entry has at least two independent source lanes, and keep source/protein/title/EC/Rhea/paper/prose fields out of predictive candidate rows.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
