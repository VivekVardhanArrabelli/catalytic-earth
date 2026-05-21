# ePK Positive Evidence Handoff

Last updated: 2026-05-21T01:13:53Z

Pushed commit: `43f330f4a67d9aa91be7b2f9de98edcb7483b3e6` (primary run artifact/ledger commit created with a temporary index because the linked local gitdir still blocks normal ref updates).

## Current Outcome

Primary outcome: `evidence_against`.

This run followed the handoff next query by re-checking `23FC` publication metadata and scanning current/future 2026 exact-ligand/date surfaces for canonical ePK-style entries with ATP/ANP/ACP/AGS plus MG/MN or ADP plus AF3/ALF/BEF/MGF. No canonical ePK rows were released on `2026-05-21`, and the narrow `2026-05-13..2026-05-21` backfill returned zero rows. `23FC` still has no DOI/PubMed/year in RCSB and no Europe PMC exact/alias metadata hit.

A broader 2026 no-source exact-ligand backfill reviewed 10 current-year rows. It recovered `23FC` as the only local-metal short-segment positive-style row and found zero local-metal non-peptide folded-substrate candidates. Non-`23FC` rows were MEK/ERK no-local-metal repeats, BRAF/MEK or receptor/CDK donor-without-acceptor contexts, or kinase-only states.

A bounded 2025-2026 Europe PMC source-text pass reviewed 50 articles and mapped 67 PDB IDs through RCSB DOI/title/direct-token checks. It found zero local-metal peptide or non-peptide substrate candidates. Targeted sparse article aliases then reviewed `6U2G`, `9AXX`, `9PCQ`, and `7O9K`; none had local transfer geometry.

The most useful fresh folded-protein evidence is negative: source-relevant BRAF/MEK structures `6U2G` and `9AXX` contain nucleotide analog states and local metal on at least one donor, but source-mapped or nearest heteromeric acceptors are outside the within-6-Angstrom local transfer window. No production labels, thresholds, registries, fingerprints, migrations, scoring paths, or production claims were changed.

## Files Changed

- `artifacts/research_lanes/epk_positive_evidence/current_release_epk_followup_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/canonical_epk_2026_no_source_backfill_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/europepmc_2026_source_text_followup_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/targeted_article_alias_followup_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/braf_mek_alias_source_review_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`
- `tools/research_lanes/epk_positive_evidence/current_release_epk_followup.py`
- `tools/research_lanes/epk_positive_evidence/europepmc_2026_source_text_followup.py`
- `tools/research_lanes/epk_positive_evidence/targeted_article_alias_followup.py`
- `work/research_lanes/epk_positive_evidence/handoff.md`

## Evidence For

- `23FC` remains review-only short-segment positive-style evidence: ATR-associated AGS/Mg places source-mapped Chk1 Ser317 OG 5.582 Angstrom from AGS PG, but the substrate entity length is 14 residues and publication metadata is still absent.
- `6U2G` and `9AXX` are source-relevant folded-protein BRAF/MEK complexes with nucleotide analogs and at least one local Mg-bearing donor state, making them useful folded-protein source-validation negatives.

## Evidence Against

- No current-date `2026-05-21` canonical release rows and no `2026-05-13..2026-05-21` canonical backfill rows were found.
- The 2026 no-source canonical backfill reviewed 10 structures and found zero local-metal non-peptide folded-substrate candidates; only `23FC` passed as a short-segment review-only hit.
- The expanded Europe PMC source-text route reviewed 50 articles and 67 mapped PDB IDs with zero local-metal substrate candidates; mapped rows were kinase-only, recruitment, non-ePK enzyme, or donor-without-heteromeric-acceptor contexts.
- `6U2G` BRAF-associated ACP/Mg donor is 8.270 Angstrom from source-mapped MEK1 Ser222, outside the within-6-Angstrom local transfer window.
- `9AXX` does not provide BRAF-to-MEK local transfer geometry: MEK Ser218/Ser222 are modeled as Ala in MEK chains, the BRAF-associated ANP lacks local Mg, and nearest heteromeric acceptors are 12.072-16.152 Angstrom away.

## Counterexamples

- No new counterexample was promoted. The BRAF/MEK rows are source-relevant geometry-negative folded-protein evidence, not ownership/context false positives requiring new exclusion logic.

## Blockers

- Startup `git fetch origin` and `git pull --ff-only origin research/epk-positive-evidence` failed with `Operation not permitted` while writing `.git/worktrees/catalytic-earth-epk-positive/FETCH_HEAD`.
- The linked local gitdir still blocks normal local ref advancement, so the primary commit was created and pushed with a temporary index.
- Because local `HEAD` is stale, normal `git status` still shows prior remote files as untracked and the branch as behind even after remote push verification.
- Production claims, threshold calibration, label import, registry edits, fingerprint changes, migrations, and production helper fallback remain forbidden.

## Next Query

At the next RCSB weekly release, re-run the current-date and 2026 no-source canonical ePK exact-ligand surfaces plus the `23FC` publication metadata check. Source-map only new PDB IDs with non-peptide substrate entity length, explicit kinase-site ligand ownership, local MG/MN or transition-metal context, and an unmodified Ser/Thr/Tyr acceptor within 6 Angstrom. Do not revisit the exhausted BRAF/MEK, CAK/CDK, aPKC/Lgl, mTORC2/Akt, eEF2K, or FN3K aliases unless new PDB IDs or publication metadata appear.

Production claims/label changes remain forbidden: yes.
