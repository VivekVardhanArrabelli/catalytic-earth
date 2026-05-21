# ePK policy harness handoff

Last updated: 2026-05-21T04:20:53Z
Run started: 2026-05-21T03:31:54Z
Run ended: 2026-05-21T04:20:53Z
Measured minutes: 48.98
Primary outcome: `scoreboard_gate_created`

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_policy_harness.py`
- `tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py`
- `artifacts/research_lanes/epk_policy_harness/epk_candidate_evidence_schema_drafts_v1_20260521T034010Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_*_20260521T034010Z_result.json` (4 compact bridge regression results)
- `artifacts/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate_20260521T034010Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy Status

Policy v0 remains frozen, review-only, and fail-closed. This run adds a candidate-level bridge schema layer on top of the existing harness output without changing production labels, thresholds, fingerprints, registries, migrations, or production scoring.

The bridge emits `claim_status`, `claim_admissibility`, and first-class `coordinate_state` fields while preserving the legacy `decision` field. The allowed claim-status enum is:

- `review_only_nonabstaining_candidate`
- `review_only_abstain_product_state`
- `review_only_abstain_analog_state`
- `review_only_abstain_split_state`
- `review_only_abstain_sibling_control`
- `review_only_abstain_topology_ambiguity`
- `review_only_abstain_missing_role_policy`
- `review_only_abstain_forbidden_context`
- `forbidden_source_leakage`

The coordinate-state enum is:

- `active_gamma`
- `product_state`
- `adp_state`
- `substrate_acceptor_analog_state`
- `split_state`
- `ligand_absent`
- `metal_absent`
- `unavailable_coordinate_state`
- `ambiguous_coordinate_state`

Source text, source queries, source validation, protein names, EC/Rhea, PDB/structure titles, paper titles, paper metadata, UniProt prose, mechanism text, and source ids are forbidden as predictive features. They remain review-only context only.

## Evidence

- Schema artifact: `artifacts/research_lanes/epk_policy_harness/epk_candidate_evidence_schema_drafts_v1_20260521T034010Z.json` (`sha256 eacc86b988a78495f0de5facb773a6615184361619e37569ba39ef8462ff34e1`).
- Scoreboard/gate artifact: `artifacts/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate_20260521T034010Z.json` (`sha256 3a57164eae0e6e1fa7b2efc97d1da6a2acec7f14906ebeb2340297d4e49d3727`).
- Compact bridge regression inputs: ADP low-geometry product-state tranche, cutoff expectation tranche, nonprefrozen GNP/GTP alias blocker negative control, and terminal-gamma sibling-control stress.
- Rows reviewed by the scoreboard gate: 31.
- Discovery-signal rows: 24.
- Aggregate claim-status counts: `{'review_only_abstain_product_state': 7, 'review_only_abstain_analog_state': 1, 'review_only_abstain_missing_role_policy': 9, 'review_only_abstain_topology_ambiguity': 8, 'review_only_abstain_sibling_control': 6}`.
- Aggregate coordinate-state counts: `{'product_state': 7, 'substrate_acceptor_analog_state': 1, 'active_gamma': 15, 'ambiguous_coordinate_state': 8}`.
- Gate result: pass, with zero forbidden source leakage, zero unsafe control non-abstention, zero expected-decision mismatches, zero expected-claim-status mismatches, and zero schema-missing rows.
- Self-tests cover source-leakage blocking, split-state status emission, topology ambiguity, sibling control, forbidden-context fallback, nonabstaining candidate emission, and scoreboard count-drift rejection.

## Blockers and Notes

- Normal `git fetch origin` and `git pull --ff-only origin research/epk-policy-harness` remain blocked by linked-worktree metadata permissions on `FETCH_HEAD`.
- `git fetch --no-write-fetch-head origin research/epk-policy-harness` succeeds.
- The normal index remains stale and reports older staged deletes; validation and commit use an alternate index seeded from `origin/research/epk-policy-harness`.
- A non-writing stress pass over 58 existing tranche artifacts found 56 validating under the updated bridge. Two older interim surface tranches still fail the preexisting `search_surface_exhausted` source-artifact citation validator; they were not scoreboard inputs.
- This remains review-only harness evidence, not clean held-out performance evidence and not production scoring evidence.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m py_compile tools/research_lanes/epk_policy_harness/*.py`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_policy_harness.py --self-test`
- `PYTHONDONTWRITEBYTECODE=1 python tools/research_lanes/epk_policy_harness/epk_candidate_policy_bridge_scoreboard_gate.py --self-test`
- Four compact bridge regression results regenerated with `epk_policy_harness.py`.
- Scoreboard/schema assertions passed for the generated gate artifact.
- JSON validation after wrap passed: 190 JSON files and 14 JSONL records parsed.
- Alternate-index `git diff --cached --check origin/research/epk-policy-harness` passed.
- Alternate-index scope check found only lane-local paths under `tools/`, `artifacts/`, and `work/research_lanes/epk_policy_harness/`.

## Exact next query

`epk_candidate_bridge_status_coverage_fault_injection_v2_review_only`

Use compact synthetic and existing lane rows to exercise every claim-status and coordinate-state enum value in a single review-only bridge gate, including explicit negative fixtures for `forbidden_source_leakage`, unsafe control non-abstention, missing schema fields, and metadata count drift. Keep negative fixtures out of production and keep discovery signal separate from claim admissibility.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
