# ePK policy harness handoff

Last updated: 2026-05-21T05:25:06Z
Run started: 2026-05-21T04:33:31Z
Run ended: 2026-05-21T05:25:06Z
Measured minutes: 51.58
Primary outcome: `scoreboard_gate_created`

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py`
- `tools/research_lanes/epk_policy_harness/epk_candidate_bridge_status_coverage_fault_injection.py`
- `artifacts/research_lanes/epk_policy_harness/epk_candidate_evidence_schema_drafts_v1_20260521T043924Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_candidate_bridge_status_coverage_fault_injection_v2_20260521T043924Z*.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy Status

Policy v0 remains frozen, review-only, and fail-closed. This run did not change production labels, thresholds, registries, fingerprints, migrations, or scoring. The synthetic accepted role policy id exists only inside the coverage fixture so the bridge can prove it can emit `review_only_nonabstaining_candidate`; it is not a production role policy and not evidence of real claim admissibility.

The refined schema draft keeps candidate rows candidate-level rather than PDB-level, adds candidate identity fields for federated lanes, names all coordinate-state and claim-status enums, separates all forbidden predictive flags from the source-leakage subset, and records the compact-artifact rule.

## Evidence

- Coverage report: `artifacts/research_lanes/epk_policy_harness/epk_candidate_bridge_status_coverage_fault_injection_v2_20260521T043924Z.json` (`sha256 eb18d5ba4a09a925283b98eefc0c39f06f42437b21124ad45fe4e1ffe6c78987`).
- Positive scoreboard gate: `artifacts/research_lanes/epk_policy_harness/epk_candidate_bridge_status_coverage_fault_injection_v2_20260521T043924Z_scoreboard_gate.json` (`sha256 081b83f3d901bf7e63180e3a149b4fdf7bce770afdb1991856e9c60693b3b5f1`).
- Refined schema draft: `artifacts/research_lanes/epk_policy_harness/epk_candidate_evidence_schema_drafts_v1_20260521T043924Z.json` (`sha256 89969cc2fab6dd1dfe063add08db79555b61eab8966c3d8d015742baac55165d`).
- Positive coverage rows reviewed: 11; negative fixture rows: 4; total rows reviewed for this run record: 15.
- Positive coverage includes all eight non-forbidden claim statuses and all nine coordinate states.
- Negative fixtures reject `forbidden_source_leakage`, unsafe control non-abstention, missing schema fields, and metadata count drift.
- Source-leakage audit covered all 14 source-leakage flags and each emitted `forbidden_source_leakage` with forbidden admissibility.
- Broad non-writing v0 tranche stress remains 56/58 passing; the same two older interim ATP search-surface tranches fail the preexisting search-surface artifact citation validator.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/*.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_bridge_status_coverage_fault_injection.py --self-test`
- Coverage report assertions passed: full claim-status coverage, full coordinate-state coverage, 14 source-leakage flags audited, all negative fixtures rejected.
- JSON validation before ledger append passed: 199 JSON files and 14 JSONL records parsed.
- Alternate-index precheck passed: lane-local add/modify set only and `git diff --cached --check origin/research/epk-policy-harness` passed.

## Blockers and Notes

- Normal `git fetch origin` and `git pull --ff-only origin research/epk-policy-harness` remain blocked by linked-worktree metadata permissions on `FETCH_HEAD`.
- `git fetch --no-write-fetch-head origin research/epk-policy-harness` succeeds.
- The normal index remains stale and reports older staged deletes/untracked replacements; use an alternate index seeded from `origin/research/epk-policy-harness` for validation and commit.
- The coverage fixture is synthetic review-only harness pressure, not held-out performance evidence, not production scoring, and not claim readiness.

## Exact next query

`epk_federated_lane_candidate_evidence_adapter_smoke_v1_review_only`

Use compact outputs from at least two independent ePK lanes to map lane-native candidate rows into `epk_candidate_evidence_v1`, then run the policy bridge and scoreboard gate without adding labels, thresholds, source-derived predictive features, or large coordinate dumps.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
