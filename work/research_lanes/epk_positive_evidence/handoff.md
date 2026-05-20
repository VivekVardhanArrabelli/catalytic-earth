# ePK Positive Evidence Handoff

Last updated: 2026-05-20T20:11:27Z

Pushed commit: `47f355422204754e0b1f1f8e346174f456b36968` (primary run
artifact commit). Final branch HEAD after this handoff-reference update is
reported in the automation summary.

## Current Outcome

Primary outcome: `evidence_for`.

This run completed the prior handoff next query: audit legacy ANP/PB terminal-
phosphate atom naming across prior lane scout artifacts, then source-map any
within-6-Angstrom candidates. It also ran a bounded recent-literature/title
follow-up, which produced one fresh source-mapped peptide lead, `9IZ0`.

The evidence remains review-only. No production labels, thresholds, registries,
fingerprints, migrations, scoring paths, or production claims were changed.

## Files Changed

- `artifacts/research_lanes/epk_positive_evidence/legacy_anp_pb_prior_scout_audit_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/legacy_anp_pb_prior_scout_source_review_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/legacy_anp_pb_distance_negative_source_checks_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/legacy_anp_pb_global_phrase_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/fresh_global_phrase_pg_followup_source_check_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/europepmc_recent_amp_pnp_kinase_substrate_literature_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/recent_literature_title_followup_rcsb_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/recent_cdk_cak_title_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/recent_cdk_cak_title_source_review_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/recent_exact_title_no_ligand_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/atm_tel1_chk2_peptide_amp_pnp_source_review_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`
- `tools/research_lanes/epk_positive_evidence/legacy_anp_pb_audit.py`
- `tools/research_lanes/epk_positive_evidence/epk_evidence_search.py`
- `work/research_lanes/epk_positive_evidence/handoff.md`

The worktree also carried uncommitted lane-only artifacts from the preceding
run; those remain lane-scoped and should be committed with this wrap rather
than reverted.

## Evidence For

- Fresh review-only peptide lead: `9IZ0` ATM/Tel1 bound to CHK2 peptide.
  Europe PMC full text for `PMC11933327` maps CHK2 substrate peptide, AMP-PNP,
  and `Thr68`; modeled CHK2 `Thr68` `OG1` is 4.383 Angstrom from ANP `PG`.
  Caveat: no local Mg/Mn is modeled near the ANP `PG`, and the article text
  check found AMP-PNP wording but no magnesium/Mg or manganese/Mn wording.
- Legacy ANP/PB prior-scout audit covered 971 prior unique PDB IDs and 221
  RCSB ANP intersections. Only two ANP `PB`/no-`PG` structures had a
  heteromeric acceptor within 6 Angstrom: `3O7L` PKA/phospholamban `Ser21`
  `OG` 5.930 Angstrom from ANP `PB` with two local Mg ions, and `4JDI`
  PAK4/Paktide `Ser0` `OG` 5.862 Angstrom from ANP `PB` with two local Mg ions.
- A bounded global AMP-PNP/AMPPNP phrase scout reviewed 100 unique RCSB IDs and
  88 ANP-containing structures. It found no fresh PB-within-6 candidates
  outside the prior lane scout surface.

## Evidence Against

- No fresh clean folded-protein substrate positive was found. New positives
  are peptide-only and review-only.
- Seven legacy ANP `PB`/no-`PG` prior-scout structures had no strict within-6
  heteromeric acceptor. `4HPT` and `4HPU` are product-state phosphoryl-transfer
  structures, `5LI1` is an inhibitory/access-control near miss at 6.053
  Angstrom, and `5HVK` remains positive-like only through a separate ANP `PG`
  group rather than PB fallback.
- Recent CDK/CAK exact-title structures are source-relevant but geometry-
  negative: four lack an active gamma donor, while `9QCV` and `9SKQ` have
  ANP/Mg but nearest heteromeric hydroxyls at about 9.7-12.5 Angstrom.
- Fresh CASK/CaMK (`9M5Y`, `9M6G`) and CRAF/MEK (`9O0V`) phrase hits are
  geometry-negative. `9O0V` places ANP on MEK1 chains and nearest RAF hydroxyls
  10.481-14.860 Angstrom away.
- Recent Europe PMC metadata scout exposed no concrete positive PDB lead beyond
  source-reviewed negatives and an irrelevant EGFR docking metadata hit
  (`2EB3`).

## Blockers

- Startup `git fetch origin` and `git pull --ff-only origin
  research/epk-positive-evidence` failed with `Operation not permitted` while
  writing `.git/worktrees/catalytic-earth-epk-positive/FETCH_HEAD`.
- `git fetch --no-write-fetch-head origin` succeeded later, and start/wrap
  remote equality was verified before local wrap changes at
  `a56e3c3362b6629d67fd6927da955bb2e1e51f8c`.
- The worktree began with staged deletions plus untracked re-creations for
  lane-only files from the previous run. Do not revert those; stage lane paths
  coherently during wrap.
- Production claims, threshold calibration, label import, registry edits,
  fingerprint changes, and production helper fallback remain forbidden.

## Next Query

Follow up `9IZ0` ATM/Tel1-CHK2: verify whether supplementary/model metadata or
sibling PIKK/ATM/Tel1 substrate structures include local Mg/Mn or equivalent
transition-state metal context. Search ATM/Tel1/CHK2 and broader PIKK substrate
peptide/full-length CHK2 exact-title and ligand surfaces, then source-map only
candidates with local metal/gamma geometry.

Keep ANP `PB` fallback review-only and explicit. Do not change production
labels, thresholds, registries, fingerprints, migrations, or scoring paths.
