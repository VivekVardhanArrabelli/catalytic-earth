# ePK policy harness handoff

Run started: 2026-05-20T10:18:16-05:00
Run ended: 2026-05-20T11:10:44-05:00
Primary outcome: `policy_frozen_review_only`

## What changed

- Tightened `tools/research_lanes/epk_policy_harness/epk_policy_harness.py` so policy validation requires a numeric positive frozen `candidate_distance_cutoff_angstrom`.
- Added per-row cutoff enforcement for terminal-gamma rows: missing or above-cutoff `nearest_gamma_acceptor_distance_angstrom` now causes explicit abstention.
- Added predeclared expected-decision checking. Any mismatch changes the run outcome to `policy_falsified`.
- Added policy/tranche SHA-256 hashes to result metadata.
- Added compact invariant stress tranche: `artifacts/research_lanes/epk_policy_harness/epk_policy_cutoff_expectation_tranche_20260520T151816Z.json`.
- Added stress result: `artifacts/research_lanes/epk_policy_harness/epk_policy_cutoff_expectation_result_20260520T151816Z.json`.
- Appended the run ledger: `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`.

## Policy result

The v0 policy remains intentionally fail-closed. ATP/ANP/AMP-PNP are still predictive only when all local features and a pre-accepted source-free role policy co-materialize in the same structure. No source-free role policy is accepted in v0.

This run stressed frozen harness invariants, not biological performance. The 5 synthetic QA rows covered over-cutoff ATP, missing-distance ANP, AMP-PNP alias normalization with missing role features, ADP/product-state blocking, and substrate-analog blocking. All 5 rows abstained, expected-decision mismatches were 0, counterexamples were 0, and no production score, threshold, label import, fingerprint edit, registry edit, or held-out performance claim was made.

The prior 13-row diagnostic tranche also reran cleanly under the stricter harness with all rows abstaining and 0 expected-decision mismatches.

## How to rerun

```bash
python3 tools/research_lanes/epk_policy_harness/epk_policy_harness.py \
  --policy artifacts/research_lanes/epk_policy_harness/epk_policy_v0_20260520.json \
  --tranche artifacts/research_lanes/epk_policy_harness/epk_policy_cutoff_expectation_tranche_20260520T151816Z.json \
  --output artifacts/research_lanes/epk_policy_harness/epk_policy_cutoff_expectation_result_20260520T151816Z.json \
  --pretty
```

Targeted verification used:

```bash
python3 tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test
PYTHONPYCACHEPREFIX=/private/tmp/epk_policy_harness_pycache python3 -m py_compile tools/research_lanes/epk_policy_harness/epk_policy_harness.py
python3 -m json.tool artifacts/research_lanes/epk_policy_harness/epk_policy_cutoff_expectation_tranche_20260520T151816Z.json >/dev/null
python3 -m json.tool artifacts/research_lanes/epk_policy_harness/epk_policy_cutoff_expectation_result_20260520T151816Z.json >/dev/null
jq -c . artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl >/dev/null
git diff --check
```

## Blocker

`git fetch origin` only worked with `--no-write-fetch-head`; normal `git pull --ff-only` failed writing `FETCH_HEAD`. `git add` also failed writing `.git/worktrees/catalytic-earth-epk-policy-harness/index.lock`. The branch started with `HEAD` equal to `origin/research/epk-policy-harness`, but these lane changes remain uncommitted until linked-worktree git metadata write access is available.

## Next query

`epk_fresh_nonconfounded_folded_substrate_role_identity_stress_v1_review_only`

This remains the next bounded ePK experiment only if ePK is reopened. It needs a fresh post-freeze tranche with source validation kept after local feature computation.
