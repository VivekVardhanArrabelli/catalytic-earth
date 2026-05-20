# ePK Positive Evidence Handoff

Last updated: 2026-05-20T19:07:33Z

Pushed commit: pending first commit for this run. A follow-up self-reference
commit should replace this line with the pushed artifact commit and final
branch HEAD.

## Current Outcome

Primary outcome: `evidence_for`.

This run began from the PKA/CFTR handoff, but the branch advanced during the
run to include the PKA/CFTR, PINK1, aPKC/Lgl, and mTORC2/Akt negative-scout
commits. After integrating that upstream lane state, the run executed the
latest handoff next query for processive/multisite kinase-substrate complexes
and ran a bounded peptide/legacy-ANP evidence search.

The primary positive result is peptide-only review evidence, not a folded-
protein substrate positive and not production evidence. No registries, labels,
fingerprints, migrations, production thresholds, or scoring paths were changed.

## Files Changed

- `artifacts/research_lanes/epk_positive_evidence/rcsb_akt_gsk3_peptide_amp_pnp_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/akt_gsk3_peptide_amp_pnp_source_review_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/rcsb_peptide_amp_pnp_anp_positive_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/pka_sp20_amp_pnp_source_review_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/europepmc_amp_pnp_full_length_substrate_literature_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/processive_multisite_source_mapped_site_review_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/mtorc2_akt_source_mapped_site_review_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/rcsb_pka_cav_rad_peptide_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/rcsb_pka_phospholamban_peptide_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/pka_phospholamban_amp_pnp_source_review_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/legacy_anp_pb_rescue_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/pak4_paktide_legacy_anp_source_review_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`
- `work/research_lanes/epk_positive_evidence/handoff.md`

## Evidence For

- Fresh review-only peptide positives: `1O6K` and `1O6L` Akt/PKB ternary
  complexes with GSK3 peptide `Ser9` `OG` 3.566 and 3.542 Angstrom from ANP
  `PG`, plus two local Mn ions.
- Fresh review-only peptide positive: `4DG0` PKA/SP20 `Ser21` `OG` 3.463
  Angstrom from ANP `PG`, plus two local Mg ions.
- Legacy atom-name peptide positives: `3O7L` PKA/phospholamban `Ser21` `OG`
  5.930 Angstrom from source-declared AMP-PNP/ANP `PB`, and `4JDI`
  PAK4/Paktide `Ser0` `OG` 5.862 Angstrom from legacy ANP `PB`.
- Repeat review-only positives recovered by the broad peptide scout: `1IR3`
  insulin receptor peptide `Tyr10` and `5HVK` LIMK1/full-length cofilin `Ser3`.

## Evidence Against

- No fresh clean folded-protein substrate positive was found in this cycle.
- Processive/multisite source review rejected `2V55` and `3BEG` as clean
  positives. In `2V55`, ROCK-I/RhoE nearest RhoE acceptors are 19.728 and
  20.033 Angstrom from ANP `PG`, and source-relevant terminal phosphorylation
  regions are absent from modeled RhoE. In `3BEG`, SRPK1/ASF/SF2 nearest
  substrate `Ser133` is 11.109 Angstrom from ANP `PG` in a docking/sliding
  state.
- mTORC2/Akt remains split/recruitment evidence: `9ZBK` contains Akt1 but no
  active gamma donor and has `Cys473` in the Akt hydrophobic-motif position;
  `9T7J` and `9T94` contain ATP on mTOR but no Akt chain and no heteromeric
  acceptor within 6 Angstrom.
- PKA/CaV/Rad `8UKN`/`8UKO`/`8UKP` did not add positive evidence. `8UKN` has
  ANP on PKA but no substrate chain, while `8UKO` and `8UKP` are peptide
  complexes without an active gamma donor under the current scan.
- Broad peptide surface still recovered false-positive/counterexample rows:
  `7B56` CaMKII-actinin source-insufficient proximity and `7ZE5` CydDC
  transporter/non-ePK context.

## Blockers

- `git fetch origin` and `git pull --ff-only origin research/epk-positive-evidence`
  failed at start with `Operation not permitted` while writing
  `.git/worktrees/catalytic-earth-epk-positive/FETCH_HEAD`.
- `git fetch --no-write-fetch-head origin` succeeded. Start-of-run equality was
  verified against remote at `6ae8a6fb29eff298315731a698a3522aa87bf12e`, but
  the branch advanced during the run to `e82379f22bc80ed28d427472c7c655a386fb477d`.
- Normal linked-worktree index writes remain blocked; use an alternate index
  under `/tmp` for clean status, commit, and push.
- Legacy ANP atom naming is now a known review issue: some source-declared
  AMP-PNP structures have ANP `PB` and no `PG`. `3O7L` and `4JDI` are recorded
  as explicit review-only legacy-terminal-atom positives, but helper behavior
  was not changed in production or label paths.
- Production claims, threshold calibration, label import, registry edits, and
  fingerprint changes remain forbidden.

## Next Query

Audit legacy ANP/PB terminal-phosphate atom naming across all prior lane scout
artifacts, not just peptide seeds. Source-map any within-6-Angstrom candidates,
then decide whether a review-only helper fallback for ANP lacking `PG` is
warranted. Do not change production labels, thresholds, registries, or
fingerprints.

Production claims and label/fingerprint changes remain forbidden.
