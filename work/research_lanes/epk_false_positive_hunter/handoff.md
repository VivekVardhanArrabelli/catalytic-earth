# ePK false-positive hunter handoff

- Last updated: 2026-05-20T21:11:08Z
- Started: 2026-05-20T20:22:29Z
- Ended: 2026-05-20T21:11:08Z
- Measured minutes: 48.65
- Primary outcome: counterexample_found
- Pushed commit: blocked; git add failed creating /Users/vivekvardhanarrabelli/Documents/Codex/2026-05-08/check-out-careflly-u-can-use-2/catalytic-earth/.git/worktrees/catalytic-earth-epk-false-positive/index.lock: Operation not permitted.
- Rule under attack: `epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0` plus `epk_mek_erk_source_free_topology_ambiguity_counteraxis_v0` and `build_epk_heteromeric_positive_coverage_candidate_scout`.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Executed an auth/label gamma-chain collision stress and ORC/Cdc6 replication-initiation expansion:

- Component surface: 24 fixed ATP-like/Mg RCSB component slices over ATP, ANP, ACP, DTP, AGS, and A3P plus 12 seed/pressure IDs; 960 unique IDs planned, 904 reviewed after retry, 56 unresolved transient DNS fetch failures.
- Targeted ORC/Cdc6 full-text surface: 45 reviewed, 0 fetch errors.
- Targeted ORC/MCM full-text surface: 8 reviewed, 0 fetch errors.
- Broader replication-initiation full-text surface: 70 reviewed, 58 transient DNS fetch failures.
- Summed reviewed rows/surface observations: 1027; unique reviewed IDs at least 968.
- No raw coordinate files were written; CIFs were fetched in memory and reduced to compact chain/entity/distance evidence.

## Result

Counterexamples found. The current review-only materializer emitted topology-clear non-ePK substrate-mode candidate rows for six DNA replication complexes:

- 7JGR, 7JGS, 7JK2, 7JK3, 7JK4: Drosophila ORC/Cdc6 DNA-bound structures. Actual materializer hits include TYR162 chain D near ATP PG chain A and TYR698 chain A near ATP PG chain G; neither pair is same-chain or reciprocal.
- 9BCX: S. cerevisiae ORC-Cdc6-Mcm2-7-DNA complex. Actual materializer hit: TYR232 chain E near ATP PG chain B; not same-chain or reciprocal.

These are non-ePK by title/keywords/entity context. Entity descriptions checked include Origin recognition complex subunits, Cell division control protein, DNA replication licensing factor MCM3, and ORC subunits.

## Evidence For

- Actual materializer topology-clear non-ePK counterexample IDs: 7JGR, 7JGS, 7JK2, 7JK3, 7JK4, 9BCX.
- Drosophila ORC/Cdc6 ATP PG to Tyr OH distances: 5.322-5.885 A, with nearest Mg 3.230-4.035 A.
- 9BCX ATP PG to TYR232 OH distance: 5.621 A, nearest Mg 4.153 A.
- Same-chain topology: false for all six. Reciprocal cross-chain topology: false for all six.
- Auth-only gamma mapping does not eliminate these rows; this is broader than only the auth/label collision hypothesis.

## Evidence Against / Boundaries

- Previous same-chain pressure IDs 1N56, 2DRA, 2Q66, 2ZH6, 7Z3N, and 7Z3O remained same-chain topology blocked.
- ORC/MCM expansion added no new ID beyond 9BCX.
- Broader replication-initiation expansion added no IDs beyond the six counterexamples, but retained 58 transient DNS fetch failures.
- This remains review-only research evidence; no production score, threshold, label import, registry edit, or fingerprint edit was made.

## Blockers

- `git fetch origin` and `git pull --ff-only` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git add` failed creating linked-worktree `index.lock`: Operation not permitted, so commit/push remain blocked.
- Some broad-surface RCSB fetches had transient DNS failures; the primary counterexample evidence was confirmed on zero-fetch-error targeted ORC/Cdc6 and ORC/MCM surfaces.

## Next Query

Test a source-free ORC/Cdc6/MCM/AAA+ replication-initiation counteraxis against the six counterexamples and known ePK positives: require a bounded guard that blocks ORC/MCM replication ATPase topology-clear Tyr hits without importing labels, changing registries/fingerprints, calibrating thresholds, or claiming production scoring.

Production claims, label changes, threshold calibration, registry/fingerprint edits, and artifact migrations remain forbidden.

## Files Changed

- `artifacts/research_lanes/epk_false_positive_hunter/auth_label_gamma_collision_stress_20260520_202229Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/auth_label_gamma_collision_stress_retry_fetch_errors_20260520_202229Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/auth_label_gamma_collision_orc_cdc6_cluster_20260520_202229Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/auth_label_gamma_collision_orc_mcm_cluster_20260520_202229Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/auth_label_gamma_collision_replication_initiation_cluster_20260520_202229Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/auth_label_gamma_collision_counterexample_summary_20260520_202229Z.json`
- `tools/research_lanes/epk_false_positive_hunter/auth_label_gamma_collision_stress.py`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`
- Pre-existing dirty lane files from earlier blocked wraps were retained and not reverted.
