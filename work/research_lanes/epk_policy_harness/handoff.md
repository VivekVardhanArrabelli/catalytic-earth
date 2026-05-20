# ePK policy harness handoff

Last updated: 2026-05-20T21:14:25Z
Run started: 2026-05-20T20:24:00Z
Run ended: 2026-05-20T21:14:25Z
Measured minutes: 50.42
Primary outcome: `policy_frozen_review_only`
Pushed commit: not pushed; `git add tools/research_lanes/epk_policy_harness artifacts/research_lanes/epk_policy_harness work/research_lanes/epk_policy_harness` failed with `fatal: Unable to create '/Users/vivekvardhanarrabelli/Documents/Codex/2026-05-08/check-out-careflly-u-can-use-2/catalytic-earth/.git/worktrees/catalytic-earth-epk-policy-harness/index.lock': Operation not permitted`.

## Files changed

- `tools/research_lanes/epk_policy_harness/epk_policy_harness.py`
- `tools/research_lanes/epk_policy_harness/epk_fresh_surface_scan.py`
- `tools/research_lanes/epk_policy_harness/epk_topology_sibling_control_stress.py`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_anp_terminal_gamma_search_surface_20260520T202756Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_anp_terminal_gamma_search_surface_page2_20260520T203608Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_fulltext_amp_pnp_materialized_anp_terminal_gamma_search_surface_20260520T202756Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_fulltext_amppnp_alias_materialized_anp_terminal_gamma_search_surface_20260520T202914Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_fulltext_amp_pnp_substrate_materialized_anp_terminal_gamma_search_surface_20260520T203337Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_anp_terminal_gamma_search_surface_20260520T202756Z_tranche.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_anp_terminal_gamma_search_surface_page2_20260520T203608Z_tranche.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_fulltext_amp_pnp_materialized_anp_terminal_gamma_search_surface_20260520T202756Z_tranche.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_fulltext_amppnp_alias_materialized_anp_terminal_gamma_search_surface_20260520T202914Z_tranche.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_fulltext_amp_pnp_substrate_materialized_anp_terminal_gamma_search_surface_20260520T203337Z_tranche.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_anp_terminal_gamma_search_surface_20260520T202756Z_result.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_rcsb_chemcomp_anp_terminal_gamma_search_surface_page2_20260520T203608Z_result.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_fulltext_amp_pnp_materialized_anp_terminal_gamma_search_surface_20260520T202756Z_result.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_fulltext_amppnp_alias_materialized_anp_terminal_gamma_search_surface_20260520T202914Z_result.json`
- `artifacts/research_lanes/epk_policy_harness/epk_fresh_fulltext_amp_pnp_substrate_materialized_anp_terminal_gamma_search_surface_20260520T203337Z_result.json`
- `artifacts/research_lanes/epk_policy_harness/epk_cross_ligand_terminal_gamma_sibling_control_contract_stress_20260520T203608Z.json`
- `artifacts/research_lanes/epk_policy_harness/epk_cross_ligand_terminal_gamma_sibling_control_contract_stress_20260520T203608Z_tranche.json`
- `artifacts/research_lanes/epk_policy_harness/epk_cross_ligand_terminal_gamma_sibling_control_contract_stress_20260520T203608Z_result.json`
- `artifacts/research_lanes/epk_policy_harness/epk_policy_harness_runs.jsonl`
- `work/research_lanes/epk_policy_harness/handoff.md`

## Policy status

Policy v0 remains frozen, review-only, and fail-closed. ATP/ANP/AMP-PNP may be predictive only when terminal gamma-equivalent geometry, local metal context, catalytic-site locality, source-free acceptor/role features, and same-structure co-materialization all hold under a preaccepted source-free role policy. No source-free role policy is accepted in v0.

This run adds an executable query-context review-only contract to the lane harness. Source query wording, including `AMP-PNP` and `AMPPNP`, is retrieval/review context only and cannot become a matching feature or predictive ligand-state repair. Coordinate-side ligand state remains derived from mmCIF ligand materialization; the reviewed AMP-PNP/AMPPNP query surfaces materialized as ANP terminal-gamma rows.

## Evidence

- Built five compact terminal-gamma source surfaces covering ANP chem-comp pages plus AMP-PNP/AMPPNP full-text query contexts; 56 compact candidate summaries were reviewed and no raw coordinate dumps were written.
- ANP chem-comp pages produced four cross-auth-chain geometry leads within the frozen 6.0 A cutoff: `9UUX`, `9UUR`, `9UW4`, and `9ZZR`.
- AMP-PNP/AMPPNP query-context surfaces produced terminal-gamma controls/exhaustion surfaces with zero cross-auth-chain geometry leads.
- Final sibling-control stress `artifacts/research_lanes/epk_policy_harness/epk_cross_ligand_terminal_gamma_sibling_control_contract_stress_20260520T203608Z.json` paired: 9UUX->9YAI, 9UUR->9ECU, 9UW4->9OAN, 9ZZR->9OMY.
- Final result `artifacts/research_lanes/epk_policy_harness/epk_cross_ligand_terminal_gamma_sibling_control_contract_stress_20260520T203608Z_result.json` reviewed 8 rows: 8 review-only abstentions, zero expected-decision mismatches, zero counterexamples, sibling-control contract enforced, and query-context review-only contract enforced.
- Fault injection rejected query-derived matching features, source-derived row matching features, premature same-structure co-materialization, non-review-only query contexts, and source-query predictive flags.
- Regression reruns for diagnostic, cutoff, and ATP sibling-control tranches stayed clean with zero expected-decision mismatches.

## Blockers

- This remains review-only harness stress, not clean held-out performance evidence or production scoring evidence.
- Query wording cannot expand the frozen ligand alias map; `AMP-PNP`/`AMPPNP` text hits reviewed here materialized as coordinate-side `ANP`.
- No accepted source-free folded substrate-role or acceptor-identity extractor exists in policy v0.
- The reviewed RCSB surfaces are bounded, not a global exhaustion of all ANP/AMP-PNP structures.
- Normal `git fetch origin` and `git pull --ff-only` still fail on linked-worktree `FETCH_HEAD`; `git add tools/research_lanes/epk_policy_harness artifacts/research_lanes/epk_policy_harness work/research_lanes/epk_policy_harness` failed on linked-worktree `index.lock` with `Operation not permitted`, so commit/push could not proceed.

## Exact next query

`epk_amp_pnp_query_context_coordinate_ligand_materialization_guard_v1_review_only`

Run a bounded AMP-PNP/AMPPNP synonym query-context guard that inventories coordinate-side ligand component ids before any local feature review. Treat query text as review-only, do not add post-hoc ligand aliases, admit only pre-frozen coordinate ligand codes to terminal-gamma evaluation, and record any non-ANP/ATP materializations as review-only alias-map blockers.

## Forbidden

Production claims and label changes remain forbidden. Do not edit production label registries, `data/registries/mechanism_fingerprints.json`, fingerprint registries, artifact migrations, or Git history. Do not import labels, calibrate production thresholds, or claim production scoring.
