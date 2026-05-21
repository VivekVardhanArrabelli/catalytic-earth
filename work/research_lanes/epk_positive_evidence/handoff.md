# ePK Positive Evidence Handoff

Last updated: 2026-05-21T12:19:56Z

Primary outcome: `evidence_for`.

Pushed commit: `8f703cf9df9347c4c964c137f8399264adf240ca`.

This run manually adjudicated the seven `source_mapped_but_source_claim_unconfirmed_review_only` candidate rows from the prior all-row adjudication, then ran a bounded same-day exact-ligand/23FC metadata probe and a small Europe PMC source-text rerun. The new source-claim artifact keeps source context separate from source-free geometry and keeps every row review-only/non-countable.

No production labels, thresholds, registries, fingerprints, migrations, scoring paths, or production claims were changed.

## Files Changed

- `artifacts/research_lanes/epk_positive_evidence/manual_source_claim_adjudication_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/current_release_epk_followup_manual_adjudication_rerun_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/europepmc_source_text_manual_adjudication_rerun_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`
- `tools/research_lanes/epk_positive_evidence/manual_source_claim_adjudication.py`
- `work/research_lanes/epk_positive_evidence/handoff.md`

## Evidence For

- `manual_source_claim_adjudication_20260521.json` reviews all seven previously source-claim-unconfirmed rows:
  - 6 `active_gamma`
  - 1 `transition_analog`
- Source-supported review-only positives:
  - `1L3R:transition_analog:AF3:E:400:I:21:1` is now source-supported as a PKA transition-state/pseudosubstrate SP20/PKI-derived peptide row.
  - `4DFX:active_gamma:ANP:E:402:I:21:1` and `4DG0:active_gamma:ANP:E:402:I:21:1` are now source-supported as PKA/SP20/AMP-PNP local-metal peptide rows.
- The artifact records compact RCSB entry/polymer metadata, Europe PMC DOI/title/PDB-token checks, PMC term counts, and UniProt site checks without storing raw article text or raw coordinate dumps.

## Evidence Against

- `4EKK:active_gamma:ANP:B:associated_entity_1:D:6:3` maps to GSK3-beta `Thr8`, adjacent to source-supported `Ser9`, and has no local Mg/Mn.
- `7KL1` candidate rows map the acceptor to CaMKII `Thr176`, while source context supports GluN2B `S1303D`; these are wrong acceptor/donor-ownership counterexamples.
- `7B56` remains source-absent for alpha-actinin `Ser822`: exact `Ser822`/CaMKII-actinin surfaces returned zero source claims, and RCSB still has no article DOI/PubMed metadata for the entry.
- Same-day current-release exact-ligand rerun returned zero 2026-05-21/current-recent rows, and `23FC` publication metadata remains absent.
- Bounded Europe PMC source-text rerun reviewed 12 articles and 20 mapped PDB IDs with no local-metal peptide or non-peptide ePK substrate candidate.
- No folded-protein local-metal active-gamma row was upgraded to countable or production-ready evidence.

## Candidate-Row Notes

- Source support is review context only. It must not become a predictive coordinate feature.
- `1L3R`, `4DFX`, and `4DG0` are useful peptide/transition stress evidence, not production labels.
- `7KL1` and `4EKK` D6 should be retained as candidate-level exclusion pressure for residue/ownership specificity.
- `7B56` should not be revisited unless new article metadata or exact alpha-actinin `Ser822` source evidence appears.

## Blockers

- Startup `git fetch origin` failed with `Operation not permitted` while writing `.git/worktrees/catalytic-earth-epk-positive/FETCH_HEAD`.
- `git fetch --no-write-fetch-head origin` succeeded.
- `git pull --ff-only origin research/epk-positive-evidence` failed with the same `FETCH_HEAD` permission blocker.
- Temporary-index/ref-safe commit and push succeeded; `refs/heads/research/epk-positive-evidence` on origin resolves to `8f703cf9df9347c4c964c137f8399264adf240ca`.
- The local worktree `HEAD` remains `8fed206e29064b1fdb1e0597773cc8c7af926241` and still reports behind because the local linked-worktree branch ref was not advanced.

## Next Query

At the next RCSB weekly release, rerun current-date and 2026 canonical ePK exact-ligand surfaces plus the `23FC` publication metadata check.

If no new release or metadata appears, prioritize new PDB IDs with source-published non-peptide substrate phosphoacceptor mapping and exact ATP/ANP/ACP/AGS+MG/MN or ADP+AF3/ALF/BEF/MGF context. Do not revisit the seven manually adjudicated rows unless new source metadata appears.

Production claims/label changes remain forbidden: yes.
