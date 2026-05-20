# ePK Positive Evidence Handoff

Last updated: 2026-05-20T18:20:53Z

Pushed commit: pending alternate-index commit for this run.

## Current Outcome

Primary outcome: `evidence_against`.

This run executed the prior handoff query:

`RCSB/PubMed source review: "PKA CFTR" "ANP" "dephosphorylated" "phosphorylation" site-specific acceptor mapping`

It reviewed the PKA/CFTR source family `9DW4`/`9DW5`/`9DW7`/`9DW8`/`9DW9`
against the final PNAS/PMC article, RCSB exact-family surfaces, Europe PMC
exact-title/DOI metadata, and transient mmCIF atom/sequence-scheme scans. The
family is strong folded-protein substrate context, but it is not clean
gamma-transfer positive evidence because the source-mapped CFTR PKA sites are
absent, unobserved, or lack a modeled phosphoacceptor oxygen near PKA gamma.

The compact artifact records 5 reviewed PDB entries, 3 RCSB exact-family rows,
2 Europe PMC exact-title rows, and 0 fetch failures. It stores only compact
metadata, mapped-site statuses, and distances; no coordinate dumps were written.

## Files Changed

- `artifacts/research_lanes/epk_positive_evidence/pka_cftr_source_mapped_site_review_20260520.json`
- `tools/research_lanes/epk_positive_evidence/pka_cftr_source_map.py`
- `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`
- `work/research_lanes/epk_positive_evidence/handoff.md`

## Evidence For

- The PNAS/PMC source article maps PKA-C bound to full-length CFTR and reports
  two catalytic-station docking sites for phosphorylating eleven CFTR PKA sites:
  `S422`, `S660`, `S670`, `S686`, `S700`, `S712`, `S737`, `S753`, `S768`,
  `S795`, and `S813`.
- RCSB exact-family search recovered `9DW5`, `9DW7`, and `9DW8`; the fixed PDB
  family source review covered `9DW4`, `9DW5`, `9DW7`, `9DW8`, and `9DW9`.
- `9DW5`, `9DW7`, `9DW8`, and `9DW9` contain PKA-associated ANP or ATP gamma
  donors with local magnesium, making them useful review-only negative controls
  for source-rich kinase-substrate context without local transfer geometry.

## Evidence Against

- `9DW4` is source-relevant but has no modeled PKA gamma-transfer donor.
- `9DW5` and `9DW7` have PKA ANP/Mg, but all eleven source-mapped CFTR sites are
  unobserved/zero-occupancy with no modeled acceptor oxygen.
- `9DW8` has PKA ANP/Mg, but ten mapped sites are unobserved and `S813` is only
  partially modeled (`C`, `CA`, `CB`, `N`, `O`) without `OG`; the nearest
  mapped-site atom is 25.471 Angstrom from PKA ANP `PG`, and no mapped-site
  acceptor exists.
- `9DW9` has PKA ATP/Mg, but all eleven mapped sites lack modeled acceptor
  oxygen. `S813` is present in the sequence scheme but has no modeled atoms.
- Nearest nonmapped CFTR Ser/Thr/Tyr acceptors to PKA gamma in `9DW5`, `9DW8`,
  and `9DW9` are 38.178, 27.427, and 27.299 Angstrom away respectively;
  `9DW7` has no modeled CFTR acceptor atom in the scan.

## Blockers

- `git fetch origin` failed at start with `Operation not permitted` while
  writing `.git/worktrees/catalytic-earth-epk-positive/FETCH_HEAD`.
- `git pull --ff-only origin research/epk-positive-evidence` failed for the
  same `FETCH_HEAD` permission reason.
- Branch equality at start was verified by `git fetch --no-write-fetch-head
  origin`, `git rev-parse HEAD`, `git rev-parse origin/research/epk-positive-evidence`,
  and `git ls-remote`; all matched `6ae8a6fb29eff298315731a698a3522aa87bf12e`.
- Normal linked-worktree index writes remain blocked; use an alternate index
  under `/tmp` for clean status, commit, and push.
- Production claims, threshold calibration, label import, registry edits, and
  fingerprint changes remain forbidden.

## Next Query

The PKA/CFTR family source-review surface is exhausted for clean folded-protein
transfer-state positives. Recommended next query:

`Source-map processive/multisite kinase-substrate complexes 2V55 ROCK-I/RhoE and 3BEG SRPK1/ASF/SF2 using paper-level acceptor residue maps plus transient CIF geometry; record whether the substrate acceptors are absent, disordered, docking-only, or distant from ANP/Mg gamma before any broader processive-phosphorylation search.`

Start from the existing geometry-scout observation that `2V55` and `3BEG` both
have ANP-bound kinase source context but no heteromeric acceptor hit within the
current scout window.

Production claims and label/fingerprint changes remain forbidden.
