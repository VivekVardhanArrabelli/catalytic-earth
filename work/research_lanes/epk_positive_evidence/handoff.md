# ePK Positive Evidence Handoff

Last updated: 2026-05-21T14:10:30Z

Primary outcome: `search_surface_exhausted`.

This run followed the prior handoff constraint by avoiding broad exhausted surfaces unless new IDs or new publication metadata appeared. It added and ran a narrow post-handoff delta helper across current-date RCSB release/revision exact-ligand surfaces, same-day Europe PMC and Crossref publication metadata, and the `23FC` authority check. It also reran the expanded `23FC`/ATR-ATRIP publication-authority helper. No fresh active-gamma or transition-analog candidate evidence row was emitted.

No production labels, thresholds, registries, fingerprints, migrations, scoring paths, or production claims were changed.

## Files Changed

- `artifacts/research_lanes/epk_positive_evidence/post_handoff_delta_followup_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/atr_chk1_publication_metadata_delta_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`
- `tools/research_lanes/epk_positive_evidence/post_handoff_delta_followup.py`
- `work/research_lanes/epk_positive_evidence/handoff.md`

## Evidence For

- `post_handoff_delta_followup_20260521.json` makes the next-query delta check reproducible across RCSB current-date release/revision, Europe PMC same-day publication, Crossref same-day publication, and `23FC` metadata surfaces.
- `atr_chk1_publication_metadata_delta_20260521.json` reviewed 43 compact source/family rows for `23FC` and related ATR-ATRIP article-family structures.
- The related ATR-ATRIP family scan remains useful review-only negative context: 2 rows are donor/analog without heteromeric acceptor and 7 rows have no active donor/transition state.
- The new delta helper now guards Crossref direct PDB-token extraction so arbitrary DOI suffixes are not treated as PDB IDs unless the DOI is a wwPDB dataset DOI.

## Evidence Against

- No fresh active-gamma or transition-analog candidate-level row was emitted.
- Current-date RCSB initial-release and revision exact-ligand surfaces returned zero genuinely new canonical ePK PDB IDs.
- Europe PMC same-day source-publication surfaces returned zero articles.
- Crossref same-day publication-date top rows returned no guarded direct PDB IDs after DOI-suffix filtering.
- `23FC` remains publication-authority absent: RCSB and PDBe still report To Be Published with no article DOI, PubMed ID, or year; Europe PMC and Crossref exact/alias checks found no matching article authority.
- RCSB full-text sibling aliases still return only `23FC`; related ATR-ATRIP family geometry scan found zero local-metal non-peptide substrate candidates.

## Candidate-Row Notes

- Candidate rows emitted this run: `0`.
- Coordinate states observed in related ATR-ATRIP family rows: 2 donor/analog-without-heteromeric-acceptor rows and 7 no-active-donor/transition rows.
- Source review remains non-predictive context only; it must not become a coordinate feature.
- Product/analog/split/unavailable states remain review-only support or negative/source-surface evidence, not production labels.

## Blockers

- Startup `git fetch origin` failed with `Operation not permitted` while writing `.git/worktrees/catalytic-earth-epk-positive/FETCH_HEAD`.
- `git fetch --no-write-fetch-head origin` succeeded.
- `git pull --ff-only origin research/epk-positive-evidence` failed with the same `FETCH_HEAD` permission blocker.
- The local worktree branch remains stale/behind, with many prior lane artifacts untracked against local `HEAD`; use temporary-index/ref-safe commit handling and do not revert those files.

## Next Query

At the next RCSB weekly release, rerun current-date and 2026 canonical ePK exact-ligand surfaces plus the `23FC` publication metadata check.

If no new release or metadata appears, restrict follow-up to genuinely new PDB IDs or new publication metadata; do not revisit the exhausted non-peptide phosphosite, source-site alias, or 2000-2026 source-published literature surfaces unless new IDs appear.

Production claims/label changes remain forbidden: yes.
