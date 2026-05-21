# ePK Positive Evidence Handoff

Last updated: 2026-05-21T01:42:09Z

Pushed commit: `e38b078ea035ab7b6c4b4609026403afd06aa6ee` (primary run artifact/ledger commit created with a temporary index because the linked local gitdir still blocks normal ref updates).

## Current Outcome

Primary outcome: `evidence_against`.

The default handoff next query was not re-run as a duplicate weekly-release sweep: the 2026-05-21 RCSB current-release and 2026 no-source exact-ligand surfaces had been checked minutes earlier, and no later weekly release exists yet. This run instead did a bounded source-validation follow-up for the `23FC` ATR-ATRIP/Chk1 singleton across RCSB, PDBe, Europe PMC, Crossref, and RCSB full-text aliases, then expanded only within the source-linked ATR-ATRIP article family exposed by Crossref.

`23FC` remains review-only. RCSB and PDBe still list the primary citation as To Be Published with no article DOI, PubMed ID, or publication year. Europe PMC exact/alias queries still do not recover a publication-metadata hit for the `23FC` title or ATR-ATRIP/Chk1 ATPgammaS aliases. Crossref confirms only the wwPDB dataset DOI `10.2210/pdb23fc/pdb` for the exact `23FC` title, which is deposition metadata rather than article source authority.

Crossref also exposed related ATR-ATRIP dataset/article context (`5YZ0` and `9L4F`). The bounded RCSB DOI/title family follow-up for the related 2025 Science Bulletin ATR-ATRIP article reviewed `5YZ0`, `9L40`, `9L43`, `9L45`, `9L46`, `9L4B`, `9L4C`, `9L4D`, and `9L4F`. All are donor-only or inhibitor/ATR-ATRIP context with no named Chk1/substrate polymer entity. A transient geometry scan of those nine rows found zero local-metal non-peptide substrate candidates: `9L46` and `9L4F` were donor/analog without heteromeric acceptor, and seven rows had no active donor or transition analog.

No production labels, thresholds, registries, fingerprints, migrations, scoring paths, or production claims were changed.

## Files Changed

- `artifacts/research_lanes/epk_positive_evidence/atr_chk1_publication_metadata_followup_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`
- `tools/research_lanes/epk_positive_evidence/atr_chk1_publication_metadata_followup.py`
- `work/research_lanes/epk_positive_evidence/handoff.md`

## Evidence For

- PDBe independently confirms the same `23FC` title, release date, deposition authors, hetero hexamer assembly, and associated EMDB map.
- Crossref confirms the PDB dataset DOI `10.2210/pdb23fc/pdb` for the deposited `23FC` structure; this is useful provenance but not article source authority.
- Crossref/RCSB mapped related source-published ATR-ATRIP donor-only negatives: `5YZ0` and `9L4F`, plus the compact 2025 ATR-ATRIP article family `5YZ0`, `9L40`, `9L43`, `9L45`, `9L46`, `9L4B`, `9L4C`, `9L4D`, and `9L4F`.

## Evidence Against

- RCSB and PDBe still report `23FC` as To Be Published with no article DOI, PubMed ID, or year.
- Europe PMC exact/alias queries returned no publication-metadata hit for the `23FC` title or ATR-ATRIP/Chk1 ATPgammaS aliases.
- Crossref only yielded the wwPDB dataset DOI for the exact `23FC` title; no article/preprint DOI matching the `23FC` ATR-ATRIP/Chk1 ATPgammaS title was found in the bounded top rows.
- RCSB full-text sibling aliases for the Chk1-containing title/aliases still return only `23FC`.
- The related ATR-ATRIP article family contains no named Chk1/substrate polymer entity.
- Transient geometry scan of that article family found zero local-metal non-peptide substrate candidates: status counts were `donor_or_analog_without_heteromeric_acceptor_review_only=2` and `no_active_donor_or_transition_analog_review_only=7`.

## Counterexamples

- No new production counterexample was promoted. The related ATR-ATRIP family is source-published donor-only negative context, not a distance/ownership false-positive requiring production exclusion logic.

## Blockers

- Startup `git fetch origin` still failed with `Operation not permitted` while writing `.git/worktrees/catalytic-earth-epk-positive/FETCH_HEAD`; `git fetch --no-write-fetch-head origin` succeeded.
- Normal local `git pull --ff-only` remains blocked by the stale/dirty linked worktree metadata. The remote branch content had already materialized locally, and exact comparison showed those prior untracked lane files matched `origin/research/epk-positive-evidence`.
- The primary commit was created and pushed with a temporary index. Because local `HEAD` is still stale, normal `git status` still shows prior remote files as untracked and the branch as behind even after remote push verification.
- Production claims, threshold calibration, label import, registry edits, fingerprint changes, migrations, and production helper fallback remain forbidden.

## Next Query

At the next RCSB weekly release, re-run the current-date and 2026 no-source canonical ePK exact-ligand surfaces plus the `23FC` publication metadata check. If `23FC` article metadata appears, source-map it before any upgrade. Otherwise, do not revisit the exhausted 2025 ATR-ATRIP Science Bulletin family unless new PDB IDs appear. Continue to source-map only new PDB IDs with non-peptide substrate entity length, explicit kinase-site ligand ownership, local MG/MN or transition-metal context, and an unmodified Ser/Thr/Tyr acceptor within 6 Angstrom.

Production claims/label changes remain forbidden: yes.
