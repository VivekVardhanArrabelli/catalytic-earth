# ePK false-positive hunter handoff

- Last updated: 2026-05-21T23:25:15Z
- Started: 2026-05-21T22:33:01Z
- Ended: 2026-05-21T23:25:15Z
- Measured minutes: 52.23
- Primary outcome: search_surface_certified
- Pushed evidence commit: `b867e2644822b96872045102d5507c05fed3c4be` via alternate-index commit/push.
- Local checked-out HEAD remains behind origin because linked-worktree metadata writes are blocked.
- Rule under attack: metric-seeded ATP/ANP deposited-v4 / biological-assembly-below-floor split trap sufficiency for fake ePK active-gamma positives.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Froze and searched older ATP/ANP metric-seeded ligand-component pages after excluding all prior metric-seeded artifacts. CIFs were fetched in memory only and reduced to compact evidence; no raw coordinate dumps were written.

- ATP/ANP older artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_atp_anp_older_20260521_223301Z.json`
- ATP/ANP older2 artifact: `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_atp_anp_older2_20260521_225930Z.json`
- Refreshed regression gate: `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_232500Z.json`

Reviewed surface this run:

- Older shard 1: 260 IDs, 529 coordinate contexts, 0 fetch errors, 79 deposited-v4 entries, 66 metric non-ORC prefilter entries, 0 split contexts.
- Older shard 2: 220 IDs, 445 coordinate contexts, 0 fetch errors, 76 deposited-v4 entries, 53 metric non-ORC prefilter entries, 0 split contexts.
- Combined: 480 entry rows, 974 coordinate contexts, 155 deposited-v4 entries, 119 metric non-ORC prefilter entries, 0 split contexts, 0 materializer context inputs, 0 fetch errors.

## Result

Outcome: `search_surface_certified` for the older ATP/ANP metric-seeded split-trap surface under the configured atom-site caps.

No new unsafe expected-policy ePK non-abstention was found.

- The two ATP/ANP shards produced zero biological-assembly-below-floor split contexts and zero metric-seeded non-ORC split contexts.
- The materializer was not invoked for these shards because no split context reached selection.
- The refreshed regression gate emits 355 rows from 28 source artifacts.
- `unsafe_nonabstention_after_expected_policy_count` remains 0.
- `5UJ7:biological_assembly_1` remains the pinned context-v4-only biological-assembly split failure.
- The prior metric-seeded split abstention controls remain `9FXK`, `6TXC`, `6TXE`, and `3PKP`.

## Exact Missing Data

No fetch errors occurred. The following oversized deposited contexts were skipped by the pre-parse atom-site cap and are the only bounded missing coordinate data in this run:

- 8ANY:deposited_atom_site, 8BQS:deposited_atom_site, 8OM2:deposited_atom_site, 8OM3:deposited_atom_site, 8OM4:deposited_atom_site, 8PTK:deposited_atom_site, 8RRI:deposited_atom_site, 9E5C:deposited_atom_site, 9E78:deposited_atom_site, 9ED4:deposited_atom_site

These skipped contexts did not become materializer inputs because no biological-assembly split context was found in the reviewed surface. If this route is reopened, inspect those IDs with a smaller assembly-only metadata pass before adding broader ligand pages.

## Evidence For / Against

Evidence against this bounded ATP/ANP split-trap route:

- 480 entry rows and 974 coordinate contexts produced zero split contexts.
- 155 deposited-v4 entries and 119 metric non-ORC prefilter entries produced zero metric-seeded non-ORC split contexts.
- Both shards had zero fetch errors and zero materializer context errors.
- The 355-row regression gate kept expected-policy unsafe non-abstention at zero.

Evidence for continued caution:

- `5UJ7:biological_assembly_1` still falsifies context-v4-only sufficiency and must stay pinned.
- Large deposited contexts skipped by the atom-site cap remain explicitly named: 8ANY, 8BQS, 8OM2, 8OM3, 8OM4, 8PTK, 8RRI, 9E5C, 9E78, 9ED4.
- The gate refresh included the two new ATP/ANP artifacts as zero-row metric source artifacts; it did not add new regression rows.

## Verification

- `python -m json.tool` for the two new ATP/ANP artifacts and refreshed regression gate.
- JSONL parse validation for `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`.
- `git diff --check` over lane files changed this run.

## Blockers

- `git fetch origin` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git pull --ff-only origin research/epk-false-positive-hunter` failed writing linked-worktree `FETCH_HEAD`: Operation not permitted.
- `git fetch --no-write-fetch-head origin` succeeded.
- Normal `git add --dry-run` failed creating linked-worktree `index.lock`: Operation not permitted.
- Local checked-out HEAD is expected to remain behind origin if linked-worktree metadata writes stay denied; use alternate-index commit/push if normal index writes fail.

## Next Query

If continuing this route, target the atom-site-cap skipped ATP/ANP IDs with a smaller assembly-only metadata pass before adding broader ligand pages. Otherwise move to same-chain/entity-reuse or internal-fragment N-terminal mimic probes with a frozen named surface. Keep `5UJ7` pinned and preserve `9FXK`, `6TXC`/`6TXE`, and `3PKP` as abstention controls.

Production claims, label changes, threshold calibration, registry/fingerprint edits, artifact migrations, and production scoring remain forbidden.

## Files Changed

- `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_atp_anp_older_20260521_223301Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/v4_metric_seeded_ligand_assembly_split_atp_anp_older2_20260521_225930Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_candidate_evidence_v1_regression_gate_20260521_232500Z.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `work/research_lanes/epk_false_positive_hunter/handoff.md`
