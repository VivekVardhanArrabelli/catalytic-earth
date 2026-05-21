# ePK policy harness handoff

Last updated: 2026-05-21T14:15:22Z
Run started: 2026-05-21T13:20:56Z
Run ended: 2026-05-21T14:15:22Z
Measured minutes: 54.43
Primary outcome: `scoreboard_gate_created`

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py`
- `tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py`
- `artifacts/research_lanes/epk_policy_harness/epk_candidate_evidence_schema_drafts_v1_20260521T132555Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T132555Z*.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy status

Policy v0 remains frozen, review-only, and fail-closed. This run did not change production labels, thresholds, registries, fingerprints, migrations, or scoring.

This run hardened the federated candidate scoreboard by making entry-level status an explicit derived rollup from candidate decisions. Candidate rows remain the source of truth. The rollup keeps candidate claim-status counts visible and applies fail-closed precedence: source leakage, forbidden context, sibling/control blockers, topology ambiguity, split, analog, product, missing-role policy, then review-only nonabstaining candidate. `progress_claim_allowed=false` and `production_claim_allowed=false` remain fixed.

## Evidence

- Schema draft: `artifacts/research_lanes/epk_policy_harness/epk_candidate_evidence_schema_drafts_v1_20260521T132555Z.json` (`sha256 965358cf336d6b3eecedc9fcd32357763de4ef57cc6d0a282e59fe535648736a`).
- Adapter report: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T132555Z.json` (`sha256 d2dcba092cff9bf2444f4b46aa4e9077d7d83a85ca41d247afc6770a3790c67d`).
- Tranche: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T132555Z_tranche.json` (`sha256 880c6acc53105f4e3154e2156110d690795eac3c54faaa62e0c17d82c4619235`).
- Policy result: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T132555Z_result.json` (`sha256 2ac1acbc12d8bf8ecf37bc99bf04aa079f949acec7afc8d68b1f56bf13ba8d1d`).
- Scoreboard gate: `artifacts/research_lanes/epk_policy_harness/epk_federated_lane_candidate_evidence_adapter_smoke_v1_20260521T132555Z_scoreboard_gate.json` (`sha256 605b5736885023291d9afb1f22323156ddf7aa35dec4acfd1166a85d45c3f6ef`).

The compact adapter smoke still maps 10 candidate rows from four independent source lanes: `epk_positive_evidence` (2), `epk_substrate_role_identity` (3), `epk_false_positive_hunter` (3), and `epk_sibling_controls` (2).

Candidate and entry claim statuses both remain review-only: 3 `review_only_abstain_missing_role_policy`, 5 `review_only_abstain_sibling_control`, 1 `review_only_abstain_product_state`, and 1 `review_only_abstain_analog_state`. The gate passed with 10 entry rollups, 8 discovery-signal rows, zero forbidden source leakage, zero unsafe control nonabstention, and zero expected claim-status mismatches.

Negative fixtures rejected:

- Missing candidate identity: `sha256 6ea76cd31ac5a81864d22073029a3b138d49f7978da45f672fc0e86ded14754b`.
- Duplicate candidate identity within one source lane: `sha256 c633409ed78eefbed51eba48f5b78adf53ed54c0286c11e3f675fffb5991ceed`.
- Copied protein/source context: `sha256 65cd79bd609c5fc07ab58b306f6a854e96be7bfbdab7c6215209b5ab56fb7d4a`.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/*.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_federated_candidate_adapter_smoke.py --self-test`
- Periodic hold-open validation repeated the self-test trio through 2026-05-21T14:14:02Z.
- `git diff --check`
- JSON validation parsed 214 JSON files and 17 JSONL records before ledger append.
- Disk remained above the safety threshold: 26 GiB available at final validation.

## Blockers and notes

- Normal `git fetch origin` failed on linked-worktree `FETCH_HEAD` permissions.
- `git fetch --no-write-fetch-head origin` succeeded.
- `git pull --ff-only origin research/epk-policy-harness` failed on linked-worktree `FETCH_HEAD`; direct `git merge --ff-only origin/research/epk-policy-harness` failed on linked-worktree `ORIG_HEAD.lock`.
- The local worktree/index remains stale and noisy because linked-worktree metadata blocks normal branch updates. Use an alternate index seeded from `origin/research/epk-policy-harness` for commit/push.
- Only four remote ePK research lane branches are currently available, and all four are already included in the federated adapter smoke.

## Exact next query

`epk_federated_candidate_entry_rollup_cross_lane_expansion_v2_review_only`

Use the entry-rollup gate as the compatibility layer for any additional compact lane outputs. Add a new lane only if it exposes candidate identity and source-free local fields without copied source text, protein names, titles, EC/Rhea, paper metadata, or prose. Continue to fail on forbidden source leakage, unsafe control nonabstention, missing candidate identity, duplicate candidate identity within source lane, and any entry rollup that attempts to convert review-only signal into progress or production claims.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
