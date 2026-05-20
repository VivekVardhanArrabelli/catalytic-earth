# ePK Positive Evidence Handoff

Last updated: 2026-05-20T17:04:49Z

Pushed commit: `480b0eec74559fcca4e610fed0cc287e360328ae` (primary run artifact
commit). Final branch HEAD after this handoff self-reference update is reported
in the automation summary. Normal linked-worktree Git metadata writes are
blocked in this sandbox.

## Current Outcome

Primary outcome: `evidence_against`.

This run executed the handoff next query:

`"kinase-substrate complex" "full-length" "ATP" "phosphorylation site"`

The exact RCSB phrase route reviewed 110 unique PDB IDs from 261 returned rows
and found only repeat folded-protein positive-like evidence (`5HVK`). The
PubMed-style route used Europe PMC after NCBI E-utilities returned HTTP 429;
it reviewed 68 rows across three bounded query surfaces and produced several
paper/family leads, but none became a fresh clean folded-protein positive.

Additional bounded alias surfaces were also run while staying within the same
lane:

- PubMed-family targeted RCSB scout: 16 unique PDB IDs, 0 heteromeric
  gamma/acceptor candidates.
- PubMed-family broader title scout: 100 unique PDB IDs, 0 heteromeric
  gamma/acceptor candidates.
- PubMed top-paper targeted scout: 60 unique PDB IDs, 0 heteromeric
  gamma/acceptor candidates.
- Dephosphorylated/unphosphorylated substrate scout: 18 unique PDB IDs, 0
  heteromeric gamma/acceptor candidates.
- Michaelis/transition substrate scout: 17 unique PDB IDs, repeat peptide
  positives `3X2U`/`3X2V`/`3X2W` and repeat folded `5HVK`.
- ATP-analog/gamma-transfer alias scout: 402 unique PDB IDs, repeat peptide
  positives `1IR3`/`2PHK`/`4IAC`, counterexamples `7ZDU`/`7ZE5`, and 2
  timeout fetch failures (`5BK2`, `5BS8`).

Across the source-review artifact, the RCSB scouts cover 700 unique PDB IDs and
954 returned RCSB rows, plus 61 unique Europe PMC/PubMed-style PMIDs. The
source review has 22 reviewed candidate rows: 1 repeat folded-protein positive,
6 repeat peptide positives, and 15 rejected/counterexample rows. Fresh clean
folded-protein positive count remains 0.

## Files Changed

- `artifacts/research_lanes/epk_positive_evidence/rcsb_full_length_atp_phosphosite_phrase_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/pubmed_full_length_atp_phosphosite_phrase_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/rcsb_pubmed_family_targeted_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/rcsb_pubmed_family_broad_title_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/rcsb_pubmed_top_paper_targeted_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/rcsb_dephosphorylated_substrate_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/rcsb_michaelis_transition_substrate_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/rcsb_atp_analog_gamma_transfer_alias_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/rcsb_pubmed_full_length_atp_phosphosite_source_review_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`
- `work/research_lanes/epk_positive_evidence/handoff.md`

## Evidence For

- Repeat folded-protein positive-like evidence: `5HVK` LIMK1/cofilin Ser3
  remains source-valid review-only evidence with Ser3 near ANP PG.
- Repeat peptide positives recovered for review-only stress coverage:
  `3X2U`/`3X2V`/`3X2W` PKA/SP20 Ser621 at 3.517-3.529 Angstrom from ATP PG;
  `1IR3` insulin receptor peptide Tyr10 at 5.082 Angstrom from ANP PG; `2PHK`
  phosphorylase kinase peptide Ser5 at 3.610 Angstrom from ATP PG; and `4IAC`
  PKA/SP20 Ser621 at 3.486 Angstrom from ACP PG.

## Evidence Against

- The exact full-length/ATP/phosphorylation-site route recovered no fresh
  folded-protein positive beyond repeat `5HVK`.
- PINK1/ubiquitin remains split-state: `6EQI` has kinase-substrate context but
  0 active gamma donors, while `5YJ9`/`8UYH` have AMP-PNP on PINK1 without
  ubiquitin substrate in the same structure.
- PKA/CFTR entries `9DW5`/`9DW7`/`9DW8`/`9DW9` have source-context complexes
  but no CFTR acceptor within the 6 Angstrom gamma-transfer window; sampled
  nearest heteromeric acceptors are 27-38 Angstrom away or absent.
- aPKC/Par6/Lgl `8R3Y` has ANP on aPKC but the nearest Lgl hydroxyl is 12.560
  Angstrom from ANP PG.
- mTORC2/Akt recruitment/ATP-state rows lack active gamma in the recruitment
  structure or place heteromeric acceptors at least 25.9 Angstrom from ATP PG.
- Broad ATP-analog/gamma-transfer aliases still false-hit non-ePK transporter
  rows `7ZDU`/`7ZE5`; they remain counterexamples for text plus geometry.

## Blockers

- `git fetch origin` failed at start with `Operation not permitted` while
  writing `.git/worktrees/catalytic-earth-epk-positive/FETCH_HEAD`; branch
  sync could not be verified before research.
- Normal `git add` failed at wrap with `Operation not permitted` while creating
  `.git/worktrees/catalytic-earth-epk-positive/index.lock`; use an alternate
  index under `/tmp` for commit/push from this worktree.
- NCBI E-utilities returned HTTP 429 on the bounded PubMed ESearch/ESummary
  call; Europe PMC fallback completed.
- ATP-analog alias scout had two timeout fetch failures (`5BK2`, `5BS8`), but
  the surface still completed with compact failure records.
- Production claims, threshold calibration, label import, registry edits, and
  fingerprint changes remain forbidden.

## Next Query

The current RCSB/PubMed full-length ATP/phosphorylation-site route is exhausted
for this lane. Next useful query should target exact recent PDB-backed paper
sets where the source claims a kinase-substrate transfer state but the current
scout saw only split-state or long-distance geometry. Recommended next query:

`RCSB/PubMed source review: "PKA CFTR" "ANP" "dephosphorylated" "phosphorylation" site-specific acceptor mapping`

Start with `9DW4`/`9DW5`/`9DW7`/`9DW8`/`9DW9`, read the paper-level site map
only, and record whether any modeled CFTR phosphorylation-site residue is
absent, disordered, or intentionally distant from PKA gamma. Do not score or
import labels.

Production claims and label/fingerprint changes remain forbidden.
