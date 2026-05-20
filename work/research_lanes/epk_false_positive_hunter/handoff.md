# ePK false-positive hunter handoff

- Last updated: 2026-05-20T22:11:22Z
- Started: 2026-05-20T21:23:00Z
- Ended: 2026-05-20T22:11:22Z
- Measured minutes: 48.37
- Primary outcome: counterexample_found
- Pushed commit: blocked for final ledger/handoff update; last observed pushed HEAD before this update was `6ed3ae4`. Final `git add` failed creating linked-worktree `index.lock`: Operation not permitted.
- Rule under attack: `epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0` plus `epk_mek_erk_source_free_topology_ambiguity_counteraxis_v0` and `build_epk_heteromeric_positive_coverage_candidate_scout`.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Executed source-free ORC/Cdc6/MCM/AAA+ guard stress and repair-variant sweeps against actual materializer output:

- Fixed controls: prior six ORC/Cdc6/MCM counterexamples plus known ePK positives `1IR3`, `1O6K`, `1O6L`, `2PHK`, `3TM0`, `5HVK`, `6Z3R`, `8OXM`, `8OXO`, `9UUR`, `9UUX`.
- ORC/MCM profile: 82 reviewed, 0 fetch errors.
- ORC motor-module profile: 62 reviewed, 0 fetch errors.
- ORC CDK-keyword profile: 43 reviewed, 0 fetch errors.
- Broad ATPase profile: 103 reviewed plus 60 retry rows; fetch errors resolved on retry, but `walker_a_oligomer` and `p_loop_oligomer` search slices returned JSON decode errors.
- Transport/motor profile: initial 173-ID fetch outage, then 173 retry rows reviewed with 0 fetch errors.
- Summed review observations: 523. CIFs were fetched in memory only; no raw coordinate files were written.

## Result

Counterexamples found. Actual materializer topology-clear non-ePK substrate-mode rows now cover 13 ORC/OCCM/MCM replication complexes:

- `5UJ7`, `5UJM`: human ORC ATPase motor module rows; TYR174 near ATP PG chain A; neither same-chain nor reciprocal.
- `6RQC`: MCM loading intermediate; TYR232 chain D near ATP PG chain A; topology-clear.
- `7JGR`, `7JGS`, `7JK2`, `7JK3`, `7JK4`: prior Drosophila ORC/Cdc6 rows, reconfirmed.
- `7JPO`: human ORC-O1AAA row; TYR174 chain D near ATP PG chain A; topology-clear.
- `7TJF`, `7TJH`: S. cerevisiae ORC/ORC-Cdc6 rows; TYR232 chain D near ATP PG chain A; topology-clear.
- `9BCX`: prior S. cerevisiae ORC-Cdc6-Mcm2-7-DNA row, reconfirmed.
- `9GJW`: OCCM maturation intermediate; TYR232 chain D near ATP PG chain A; topology-clear and missed by Mg-site guards because no terminal ATP PG had Mg within 4.5 A.

## Guard Stress Findings

- Strict Mg-site multisite guard `v0` blocks the prior six but misses `5UJ7`, `5UJM`, and `9GJW` on targeted ORC/OCCM surfaces.
- Relaxed Mg-site guards `v1`/`v2` cover `5UJ7` and `5UJM` but still miss `9GJW`.
- Too-broad two-site-only guard `v3` loses known ePK positives `8OXM` and `8OXO`.
- ATP-terminal oligomer guard `v4_oligomeric_atp_terminals_no_mg_required` blocks the bounded ORC/OCCM false positives without losing bounded ePK positives in the current sweeps, but this is still only review-only bounded evidence.
- `9I3I` is a likely ORC/MCM context confound but was not counted because the local probable-ePK heuristic flags a deposited `CDK` keyword; next run should adjudicate this explicitly.

## Evidence Against / Boundaries

- The current review-only materializer remains broken for non-ePK ORC/OCCM/MCM discovery under topology-clear Tyr substrate-mode hits.
- Broad ATPase and transport/motor retry surfaces did not add non-ORC topology-clear non-ePK residuals, but the broad Walker/P-loop query slices had search API JSON decode failures and remain unresolved.
- The `v4` guard has not been stressed on component-level ATP/ADP/no-Mg surfaces or broad kinase-dimer positives; it must not be promoted to production or calibration.

## Blockers

- Normal `git fetch origin` / `git pull --ff-only` paths failed writing linked-worktree `FETCH_HEAD`; `git fetch --no-write-fetch-head origin` succeeded and HEAD matched origin at start.
- During the run the branch advanced to pushed commits `65ceca5` and `6ed3ae4`; final wrap commit/push was attempted after this handoff update and blocked by linked-worktree `index.lock`: Operation not permitted.
- `walker_a_oligomer` and `p_loop_oligomer` broad ATPase search slices returned non-JSON responses.

## Next Query

Stress `v4_oligomeric_atp_terminals_no_mg_required` on component-level ATP/ADP/no-Mg structures and kinase-dimer positives, and manually adjudicate ORC/MCM CDK-keyword cases such as `9I3I`. Keep production labels, threshold calibration, registry/fingerprint edits, production scoring, and artifact migrations forbidden.

Production claims, label changes, threshold calibration, registry/fingerprint edits, and artifact migrations remain forbidden.

## Files Changed

- `tools/research_lanes/epk_false_positive_hunter/orc_mcm_multisite_guard_stress.py`
- `tools/research_lanes/epk_false_positive_hunter/orc_mcm_guard_variant_sweep.py`
- `artifacts/research_lanes/epk_false_positive_hunter/orc_mcm_multisite_guard_stress_20260520_212300Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/orc_mcm_guard_variant_sweep_20260520_212300Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/orc_motor_module_multisite_guard_stress_20260520_212300Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/orc_motor_module_guard_variant_sweep_20260520_212300Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/orc_cdk_keyword_multisite_guard_stress_20260520_212300Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/orc_cdk_keyword_guard_variant_sweep_20260520_212300Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/oligomeric_atpase_multisite_guard_stress_20260520_212300Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/oligomeric_atpase_multisite_guard_retry_fetch_errors_20260520_212300Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/oligomeric_atpase_guard_variant_sweep_20260520_212300Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/oligomeric_atpase_guard_variant_retry_fetch_errors_20260520_212300Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/transport_motor_multisite_guard_stress_20260520_212300Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/transport_motor_multisite_guard_retry_fetch_errors_20260520_212300Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/transport_motor_guard_variant_retry_fetch_errors_20260520_212300Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`
