# ePK policy harness handoff

Last updated: 2026-05-21T13:08:59Z
Run started: 2026-05-21T12:19:27Z
Run ended: 2026-05-21T13:08:59Z
Measured minutes: 49.53
Primary outcome: `scoreboard_gate_created`

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_policy_harness.py`
- `tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py`
- `tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py`
- `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z*.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy status

Policy v0 remains frozen, review-only, and fail-closed. This run did not change production labels, thresholds, registries, fingerprints, migrations, or scoring. The work promotes the federated candidate evidence adapter into a regression-style review-only gate; it does not activate production claims.

The schema draft now explicitly names `source_lane_id`, `source_artifact`, `source_row_key`, and `source_row_id` as federated provenance fields for `epk_candidate_evidence_v1`. Those fields are provenance/review context only and must not carry source text, protein names, PDB or paper titles, EC/Rhea, paper metadata, UniProt prose, or mechanism prose as predictive features.

## Evidence

- Adapter report: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z.json` (`sha256 d9083c4b862c90ac8c2fbff5b3713c4a92e5d745d56c36db1886f7c4cfa0efe5`).
- Tranche: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z_tranche.json` (`sha256 edbd340ea9896c9f508329bcc3900c3b415170d001453a6eaa5460ea5079ef43`).
- Policy result: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z_result.json` (`sha256 9a8faf485a8149ebb3f482ff2168d06568d9a269edd0cf162c6dcf1e88ad934a`).
- Scoreboard gate: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T053531Z_scoreboard_gate.json` (`sha256 074803343edf2438b8088282aca92f0d1b58199afb8c6e58db88e50809ab156f`).

The adapter smoke mapped 10 compact candidate rows from four independent source lanes:

- `epk_positive_evidence`: 2 rows.
- `epk_substrate_role_identity`: 3 rows.
- `epk_false_positive_hunter`: 3 rows.
- `epk_sibling_controls`: 2 rows.

Policy outcomes were review-only only: 3 `review_only_abstain_missing_role_policy`, 5 `review_only_abstain_sibling_control`, 1 `review_only_abstain_product_state`, and 1 `review_only_abstain_analog_state`. The scoreboard gate passed with 8 discovery-signal rows, zero forbidden source leakage, zero unsafe control nonabstention, zero expected decision mismatches, and zero expected claim-status mismatches.

Negative fixtures rejected:

- Missing candidate identity: `sha256 c966e21ed8c7f093cb3840d9486d2d5bd8b591fb2cc6cddb884b03f7d4a2f728`.
- Duplicate candidate identity within one source lane: `sha256 1f739411bc3f79fda1e5f352130dd4fd3c7d7b854ad89a9001873e7c4ee4df1d`.
- Copied protein/source context: `sha256 ebc8dd085caed42ebb562aa4f0dc7731441d4b905d7b28ffc592d1b21da5954c`.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/*.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py --self-test`
- Periodic hold-open validation reran the self-test trio through 2026-05-21T13:08:53Z.
- Non-writing tranche sweep: 60 tranches checked; 58 passed; the same two older interim `search_surface_exhausted` citation-validator failures remain unchanged.
- Final JSON validation parsed 206 JSON files and 17 JSONL records after wrap updates.

## Blockers and notes

- Normal `git fetch origin` and `git pull --ff-only origin research/epk-policy-harness` remain blocked by linked-worktree metadata permissions on `FETCH_HEAD`.
- `git fetch --no-write-fetch-head origin` succeeds.
- The normal local branch remains stale behind `origin/research/epk-policy-harness`; use an alternate index seeded from the remote branch for validation and commit/push.
- The smoke test is a compact federated adapter/gate regression, not clean held-out performance evidence, not production scoring, and not claim readiness.

## Exact next query

`epk_federated_lane_candidate_evidence_adapter_contract_cross_lane_expansion_v2_review_only`

Expand the federated adapter gate to additional compact candidate outputs only if they already expose source-free local fields and candidate identity. Keep source review/protein names/titles/EC/Rhea/paper metadata as review-only context or exclude them entirely from predictive rows. Continue to fail on forbidden source leakage, unsafe control nonabstention, missing candidate identity, duplicate candidate identity within source lane, and copied source context.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
