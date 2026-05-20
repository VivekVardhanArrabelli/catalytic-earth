# ePK policy harness handoff

Run started: 2026-05-20T09:17:14-05:00  
Run ended: 2026-05-20T09:30:41-05:00  
Primary outcome: `policy_frozen_review_only`

## What changed

- Added frozen review-only policy manifest: `artifacts/research_lanes/epk_policy_harness/epk_policy_v0_20260520.json`.
- Added compact 13-row diagnostic tranche: `artifacts/research_lanes/epk_policy_harness/epk_policy_diagnostic_tranche_20260520.json`.
- Added deterministic harness: `tools/research_lanes/epk_policy_harness/epk_policy_harness.py`.
- Wrote diagnostic result: `artifacts/research_lanes/epk_policy_harness/epk_policy_diagnostic_result_20260520T091714-0500.json`.
- Wrote run ledger: `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`.

## Policy result

The v0 policy is intentionally fail-closed. ATP/ANP/AMP-PNP can only produce a non-abstaining review-only candidate when terminal gamma-equivalent geometry, local metal context, catalytic-site locality, source-free acceptor/role features, and same-structure co-materialization are all true under a pre-accepted source-free role policy. No such source-free role policy is accepted in v0.

The diagnostic run reviewed 13 compact rows:

- `4EKK` primary diagnostic row.
- Regression/context counterexamples: `7ZE5`, `7B56`, `7ZDT`, `2JJ2`, `4HPU`, `9L3U`, `7T55`.
- Product/analog/repair tripwires: `3TM0`, `1TH8`, `5LI1`.
- Sibling-control tripwires: `1TZ6`, `1WKL`.

All 13 rows abstained. No production score, threshold, label import, fingerprint edit, registry edit, or held-out performance claim was made.

## How to rerun

```bash
python3 tools/research_lanes/epk_policy_harness/epk_policy_harness.py \
  --policy artifacts/research_lanes/epk_policy_harness/epk_policy_v0_20260520.json \
  --tranche artifacts/research_lanes/epk_policy_harness/epk_policy_diagnostic_tranche_20260520.json \
  --output artifacts/research_lanes/epk_policy_harness/epk_policy_diagnostic_result_20260520T091714-0500.json \
  --pretty
```

Targeted verification used:

```bash
python3 tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test
python3 -m py_compile tools/research_lanes/epk_policy_harness/epk_policy_harness.py
python3 -m json.tool artifacts/research_lanes/epk_policy_harness/epk_policy_v0_20260520.json >/dev/null
python3 -m json.tool artifacts/research_lanes/epk_policy_harness/epk_policy_diagnostic_tranche_20260520.json >/dev/null
```

## Blocker

`git fetch origin` only worked with `--no-write-fetch-head`; normal fetch, ff-only merge, commit, and push are blocked because this sandbox cannot write the linked worktree git metadata directory under `.git/worktrees/catalytic-earth-epk-policy-harness`. HEAD already matched `origin/research/epk-policy-harness` at run start, but the changes remain uncommitted until git metadata write access is available.

## Next query

`epk_fresh_nonconfounded_folded_substrate_role_identity_stress_v1_review_only`

This should be the next bounded ePK experiment only if ePK is reopened. It needs a fresh post-freeze tranche with source validation kept after local feature computation.
