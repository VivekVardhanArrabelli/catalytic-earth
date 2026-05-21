# ePK Positive Evidence Handoff

Last updated: 2026-05-21T00:15:43Z

Pushed commit: `345e61e944ed6bd3000cf5016d476d990dfa66d4` (primary run artifact/ledger commit created with a temporary index/object directory). The final handoff-reference commit is reported in the automation summary because the linked local gitdir still blocks normal ref updates.

## Current Outcome

Primary outcome: `evidence_for`.

This run followed the previous `Next Query` by source-mapping `1L3R`, `5LIH`, `4NU1`, and `8VMF`, then scanning same-paper/title sibling structures for non-peptide folded-substrate transition-analog positives. That 15-structure seed-family surface is exhausted for this snapshot: `1L3R` and `5LIH` remain review-only peptide/pseudosubstrate positives, while `4NU1` and `8VMF` remain GSK-3 near-miss negatives with no clean unmodified heteromeric hydroxyl acceptor.

A second recent exact-ligand/date/source scout covered 2025-2026 canonical ePK EC/Pfam rows with ATP/ANP/ACP/AGS plus Mg/Mn and ADP plus AF3/ALF/BEF/MGF. It reviewed 19 unique structures and found zero local-metal non-peptide folded-substrate candidates. It did surface one fresh review-only short-segment positive-style row, `23FC`: human ATR-ATRIP with ATPgammaS/Mg and a 14-residue Chk1 segment. `23FC` maps Chk1 Ser317 by CIF sequence scheme, UniProtKB O14757 annotates Ser317 as a phosphoserine by ATM/ATR, and the modeled Ser317 OG is 5.582 Angstrom from ATR-associated AGS PG with local Mg.

The evidence remains review-only. No production labels, thresholds, registries, fingerprints, migrations, scoring paths, or production claims were changed.

## Files Changed

- `artifacts/research_lanes/epk_positive_evidence/transition_analog_seed_family_followup_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/recent_epk_exact_ligand_source_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/atr_chk1_23fc_source_review_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`
- `tools/research_lanes/epk_positive_evidence/transition_analog_seed_family_followup.py`
- `tools/research_lanes/epk_positive_evidence/recent_epk_exact_ligand_source_scout.py`
- `work/research_lanes/epk_positive_evidence/handoff.md`

## Evidence For

- Fresh review-only short-segment positive-style geometry: `23FC` ATR-associated AGS/Mg places source-mapped and UniProt phosphosite-mapped Chk1 Ser317 OG 5.582 Angstrom from AGS PG.
- `23FC` exact-title and ATR/Chk1/ATPgammS alias sibling checks returned only `23FC`, so it is a singleton lead for now.
- `1L3R` remains source-mapped review-only PKA/PKI-alpha peptide evidence: PKI-alpha Ser21 is 2.268 Angstrom from AF3 Al with local Mg.
- `5LIH` remains source-mapped review-only PKCiota/PKC-epsilon pseudosubstrate evidence: Ser11 is 2.419-2.624 Angstrom from active AF3 groups with local Mn.

## Evidence Against

- No clean non-topology-confounded folded-protein canonical ePK substrate positive was found.
- The 15-structure seed-family sibling surface for `1L3R`, `5LIH`, `4NU1`, and `8VMF` found no non-peptide folded-substrate transition-analog positive.
- The 19-structure recent exact ePK-family/date/ligand/source surface found zero local-metal non-peptide candidates; non-short rows were MEK/ERK no-local-metal repeats, RAF/MEK or mTOR/CAK/GRK/CDK kinase-only states, or donor/analog-without-heteromeric-acceptor contexts.
- `23FC` is not clean canonical ePK folded-substrate evidence: ATR is PIKK/atypical, the Chk1 substrate is only a 14-residue segment, and no DOI/PubMed/publication year is exposed yet by RCSB or Europe PMC exact/alias checks.
- `4NU1` remains a phosphorylated GSK-3 Ser9 autoinhibitory/product-state near miss; `8VMF` remains a beta-catenin S45D phosphomimetic near miss.

## Counterexamples

- No new counterexample was promoted in this run. `23FC` is recorded as review-only PIKK/short-segment stress evidence, not a false positive counterexample.

## Blockers

- Startup `git fetch origin` failed with `Operation not permitted` while writing `.git/worktrees/catalytic-earth-epk-positive/FETCH_HEAD`; the requested normal `git pull --ff-only` could not be completed.
- The linked local gitdir still blocks normal local ref advancement. Commits were created and pushed through a temporary index/object-directory workflow.
- Because the local ref is stale, normal `git status` may still show prior remote files as untracked and the branch as behind even after remote push verification.
- Production claims, threshold calibration, label import, registry edits, fingerprint changes, migrations, and production helper fallback remain forbidden.

## Next Query

Re-check `23FC` after publication metadata appears and scan future 2026 exact-ligand/date surfaces for canonical ePK kinase-domain entries with ATP/ANP/AGS/ADP plus MG/MN/AF3/MGF/BEF, requiring non-peptide substrate entity length, explicit kinase-site ligand ownership, and source-mapped unmodified Ser/Thr/Tyr acceptor before CIF source mapping.

Production claims/label changes remain forbidden: yes.
