# ePK Positive Evidence Handoff

Last updated: 2026-05-20T21:09:01Z

Pushed commit: pending primary run artifact commit; update this line after the
lane-only commit is pushed.

## Current Outcome

Primary outcome: `counterexample_found`.

This run completed the prior next query by following up `9IZ0` ATM/Tel1-CHK2
for missing Mg/Mn or sibling PIKK metal context, then ran bounded exact
ligand/Mg surfaces to test whether a cleaner local-metal ePK positive appears.
No fresh clean folded-protein ePK positive was found. The fresh source-mapped
result is instead a counterexample: `7ZDT` has local ATP/Mg-to-Ser geometry,
but source/title/entity mapping identifies CydDC ATP-binding/permease heme
transporter chains rather than kinase-substrate phosphorylation.

The evidence remains review-only. No production labels, thresholds, registries,
fingerprints, migrations, scoring paths, or production claims were changed.

## Files Changed

- `artifacts/research_lanes/epk_positive_evidence/pikk_atm_tel1_chk2_metal_context_followup_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/europepmc_pikk_metal_context_literature_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/recent_atp_mg_substrate_peptide_geometry_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/recent_atp_mg_substrate_peptide_rows21_40_geometry_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/recent_atp_mg_substrate_peptide_rows41_60_geometry_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/recent_atp_mg_substrate_peptide_rows61_80_geometry_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/phosphoacceptor_ligand_mg_exact_surface_review_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/full_length_ligand_mg_geometry_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`
- `tools/research_lanes/epk_positive_evidence/pikk_metal_followup.py`
- `work/research_lanes/epk_positive_evidence/handoff.md`

The worktree still shows staged deletions plus untracked re-creations inherited
from the previous run because the local branch ref is stale. Do not revert
those lane-only files; use a temporary index based on
`origin/research/epk-positive-evidence` for wrap commits.

## Evidence For

- Repeat review-only peptide positive recovered: `1QMZ` CDK2/Cyclin A
  substrate peptide `Ser5` `OG` is 3.416-3.680 Angstrom from ATP `PG` with
  local Mg. This was already in the lane ledger and is not fresh folded-protein
  evidence.
- `9IZ0` remains source-mapped review-only peptide evidence: CHK2 `Thr68`
  `OG1` is 4.383 Angstrom from ANP `PG`, but no local Mg/Mn is modeled or found
  in article/supplement checks.
- Repeat full-length positive-like geometry recovered: `5HVK` LIMK1/cofilin
  `Ser3` is 4.236 Angstrom from ANP `PG`, but lacks local metal under the lane
  scanner.

## Evidence Against

- The `9IZ0` source follow-up did not upgrade metal context. Article XML maps
  CHK2(63-74), `Thr68`, and AMP-PNP, while article XML and supplementary checks
  found no usable magnesium/Mg or manganese/Mn context and the 9IZ0 model has
  ANP as its only nonpolymer entity.
- Bounded ATM/Tel1/PIKK ligand surfaces reviewed 26 unique PDB IDs and found
  zero source-mappable local-metal gamma/acceptor candidates. Fresh
  nucleotide/metal siblings `6S8F` and `6SKY`/`6SKZ`/`6SL0`/`6SL1` have no
  substrate acceptor geometry.
- Exact full-length/folded substrate ligand/Mg surfaces reviewed 10 unique PDB
  IDs and added no fresh clean folded-protein positive. New rows were DnaK,
  Lon, Bcs1, ClpXP, or other ATPase-like negatives.
- Exact phosphoacceptor/protein-kinase/substrate ligand/Mg surfaces reviewed
  `4BIW`, `4JDI`, and `5LFK`; no strict `PG` local-metal acceptor candidate was
  added, with `4JDI` remaining only a known legacy ANP/`PB` review-only case.
- ATP/Mg text-first substrate-peptide pagination through rows 1-80 is noisy:
  most local-metal rows are ATPase/chaperone/transporter/pseudokinase contexts
  rather than ePK substrate transfer states.

## Counterexamples

- Fresh counterexample `7ZDT`: local ATP/Mg-to-Ser geometry in CydDC
  ATP-binding/permease heme transporter chains, not kinase-substrate
  phosphorylation evidence.
- Repeat CydDC counterexamples `7ZDU` and `7ZE5`: local ATP/ANP Mg geometry
  across transporter ATPase chains can mimic gamma/acceptor proximity.
- Additional ATP/Mg false-positive families in rows 1-80 include Msp1,
  Hsp70/DnaK/BiP, Lon/LONP1, Bcs1, ClpXP, PCAT1, and CydDC.

## Blockers

- Startup `git fetch origin` and `git pull --ff-only origin
  research/epk-positive-evidence` failed with `Operation not permitted` while
  writing `.git/worktrees/catalytic-earth-epk-positive/FETCH_HEAD`.
- `git fetch --no-write-fetch-head origin` succeeded, so
  `origin/research/epk-positive-evidence` was used as the commit base.
- The local branch remains behind the remote because the gitdir blocks normal
  ref updates. Wrap should use `commit-tree` plus direct push to
  `origin/research/epk-positive-evidence`, then verify with a temporary index.
- Production claims, threshold calibration, label import, registry edits,
  fingerprint changes, migrations, and production helper fallback remain
  forbidden.

## Next Query

Run a domain/EC-filtered canonical ePK ligand search instead of text-first
ATP/Mg pagination: combine RCSB kinase-domain or EC
`2.7.10*`/`2.7.11*` filters with ATP/ANP/ACP/AGS plus Mg/Mn, scan a bounded
first 50 unique structures for heteromeric acceptor <=6 Angstrom, and
source-map only fresh non-ATPase candidates.

Explicitly exclude ABC/AAA/Hsp70/Lon/Bcs1/ClpXP/CydDC transporter or chaperone
ATPase families plus exhausted PIKK no-metal sibling surfaces. Keep ANP `PB`
fallback review-only and explicit. Do not change production labels, thresholds,
registries, fingerprints, migrations, or scoring paths.
