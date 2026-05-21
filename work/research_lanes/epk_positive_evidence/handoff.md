# ePK Positive Evidence Handoff

Last updated: 2026-05-21T13:09:22Z

Primary outcome: `search_surface_exhausted`.

This run followed the prior handoff default: first rechecked the 2026-05-21 current-release exact-ligand surfaces and `23FC` publication metadata, then searched for fresh source-published non-peptide/full-length substrate positives. No fresh active-gamma or transition-analog candidate evidence row was emitted. Source context remains separate from source-free geometry, and every row remains review-only/non-countable.

No production labels, thresholds, registries, fingerprints, migrations, scoring paths, or production claims were changed.

## Files Changed

- `artifacts/research_lanes/epk_positive_evidence/current_release_epk_followup_post_handoff_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/nonpeptide_phosphosite_candidate_rows_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/source_site_alias_candidate_rows_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/source_published_nonpeptide_literature_followup_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/source_published_nonpeptide_adjudication_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/source_published_nonpeptide_literature_followup_2000_2014_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/source_published_nonpeptide_adjudication_2000_2014_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`
- `tools/research_lanes/epk_positive_evidence/nonpeptide_phosphosite_candidate_rows.py`
- `tools/research_lanes/epk_positive_evidence/source_site_alias_candidate_rows.py`
- `tools/research_lanes/epk_positive_evidence/source_published_nonpeptide_literature_followup.py`
- `tools/research_lanes/epk_positive_evidence/source_published_nonpeptide_adjudication.py`
- `work/research_lanes/epk_positive_evidence/handoff.md`

## Evidence For

- `current_release_epk_followup_post_handoff_20260521.json` rechecked 2026-05-21/current-recent exact-ligand surfaces and `23FC`; it found zero current/recent rows and `23FC` publication metadata is still absent.
- `nonpeptide_phosphosite_candidate_rows_20260521.json` searched 12 guarded RCSB source-rich non-peptide/full-length phosphosite surfaces. It returned 49 exact-context rows, but all were prior lane PDB IDs, so no fresh candidate row was emitted.
- `source_site_alias_candidate_rows_20260521.json` searched 13 named folded-substrate site alias surfaces under exact ligand/metal filters and returned zero rows.
- The source-published literature passes reviewed 77 compact article records and scanned 62 fresh mapped PDB rows with bounded CIF guards and no raw coordinate dumps.
- `source_published_nonpeptide_adjudication_*.json` convert those fresh mappings into review-only negative/source-surface adjudication rows.

## Evidence Against

- No fresh active-gamma or transition-analog candidate-level row was emitted.
- No fresh mapped PDB row contains a within-6-Angstrom heteromeric Ser/Thr/Tyr acceptor candidate.
- Fresh RAF/MEK source-published rows `9AXA`, `9AXC`, `9MMP`, and `9O0U` are geometry-negative rather than positive transfer states; `9MMP`/`9O0U` have donor analogs without local heteromeric acceptors.
- `6EAC` is a SelO pseudokinase AMPylation source mismatch, not canonical ePK substrate phosphorylation evidence.
- Older mapped donor rows `1UA2`, `4A06`, and `7L9P` lack local heteromeric acceptor geometry and do not support positive ePK transfer evidence.

## Candidate-Row Notes

- Candidate rows emitted this run: `0`.
- Coordinate states observed in fresh scanned rows: 6 active-gamma donor-without-heteromeric-acceptor rows and 56 no-active-donor/transition rows.
- Source review remains non-predictive context only; it must not become a coordinate feature.
- Prior lane PDB IDs were skipped by default to avoid re-adjudicating exhausted positives and the seven manually adjudicated rows.

## Blockers

- Startup `git fetch origin` failed with `Operation not permitted` while writing `.git/worktrees/catalytic-earth-epk-positive/FETCH_HEAD`.
- `git fetch --no-write-fetch-head origin` succeeded.
- `git pull --ff-only origin research/epk-positive-evidence` failed with the same `FETCH_HEAD` permission blocker.
- The local worktree branch remains stale/behind, with many prior lane artifacts untracked against local `HEAD`; use temporary-index/ref-safe commit handling and do not revert those files.

## Next Query

At the next RCSB weekly release, rerun current-date and 2026 canonical ePK exact-ligand surfaces plus the `23FC` publication metadata check.

If no new release or metadata appears, restrict follow-up to genuinely new PDB IDs or new publication metadata; do not revisit the exhausted non-peptide phosphosite, source-site alias, or 2000-2026 source-published literature surfaces unless new IDs appear.

Production claims/label changes remain forbidden: yes.
