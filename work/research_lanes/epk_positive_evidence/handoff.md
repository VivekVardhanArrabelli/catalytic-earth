# ePK Positive Evidence Handoff

Last updated: 2026-05-21T03:19:00Z

Pushed commit: `6b4f1c0ce1359dcda079d66654c4709bd2438c21` (primary run artifact/ledger commit created with a temporary index because the linked local gitdir still blocks normal ref updates). A follow-up handoff commit should be the final remote head for this run.

## Current Outcome

Primary outcome: `search_surface_exhausted`.

The default next query required waiting for the next RCSB weekly release or new `23FC` publication metadata. No later release/metadata was available during this cycle, so this run used a bounded same-lane follow-up: paged previously unreviewed RCSB phrase offsets for transition/phosphoryl-transfer wording and added substrate-trapping, nonhydrolyzable ATP, precatalytic, and substrate-bound AMP-PNP phrase surfaces.

The primary phrase-pagination artifact reviewed 140 structures, including 118 PDB IDs not previously seen in lane artifacts, from 393 returned rows across seven surfaces. It found zero fresh local-metal peptide or non-peptide substrate candidates. The only local-metal non-peptide row was `1HE1`, already rejected by the lane as an ExoS/Rac GTPase transition-state false hit rather than ePK kinase-substrate evidence.

No production labels, thresholds, registries, fingerprints, migrations, scoring paths, or production claims were changed.

## Files Changed

- `artifacts/research_lanes/epk_positive_evidence/phosphoryl_transfer_phrase_pagination_followup_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/phosphoryl_transfer_phrase_pagination_guarded_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/phosphoryl_transfer_phrase_timeout_metadata_followup_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`
- `tools/research_lanes/epk_positive_evidence/phosphoryl_transfer_phrase_pagination_followup.py`
- `work/research_lanes/epk_positive_evidence/handoff.md`

## Evidence For

- The paged phrase scout recovered only the prior local-metal non-peptide geometry in `1HE1`; this confirms the search still surfaces known non-ePK transition-state ownership risk.
- The new helper records prior-lane PDB exposure and supports max-CIF/row-timeout guards for future broad phrase surfaces.

## Evidence Against

- No fresh clean folded-protein ePK transfer-state positive was found.
- The 140-structure primary cap found zero fresh local-metal peptide or non-peptide substrate candidates.
- The only local-metal non-peptide row, `1HE1`, is a repeat ExoS/Rac GTPase false hit.
- Fresh donor/analog-without-heteromeric-acceptor rows included non-ePK/ATPase or channel/transporter contexts such as `2F43` F1-ATPase, `8DUJ`/`8DVE` RyR1, and `7TBW` ABCA1.
- Guarded timeout/source metadata checks showed fresh timeout row `8JDL` is a human cytoplasmic ribosome/tRNA/mRNA structure; repeat timeout rows `9QQL` and `9QSA` are mouse ribosome translocation-state structures.

## Counterexamples

- No new counterexample was promoted. `1HE1` remains a repeat GTPase ownership/context false hit from prior lane review.

## Blockers

- Startup `git fetch origin` and `git pull --ff-only origin research/epk-positive-evidence` still failed with `Operation not permitted` while writing `.git/worktrees/catalytic-earth-epk-positive/FETCH_HEAD`.
- `git fetch --no-write-fetch-head origin` succeeded, but normal local `git merge --ff-only` failed on `ORIG_HEAD.lock`; the local branch/worktree remains stale even though remote refs can be read.
- Wrap uses temporary-index `commit-tree` commits on top of `origin/research/epk-positive-evidence` and direct push verification instead of normal local ref updates.
- Production claims, threshold calibration, label import, registry edits, fingerprint changes, migrations, scoring, and production helper fallback remain forbidden.

## Next Query

Run a guarded continuation only on source-rich unreviewed phrase rows after adding pre-CIF filters: require a canonical ePK EC/Pfam or explicit protein-kinase polymer plus exact `ATP`/`ANP`/`ACP`/`AGS` + `MG`/`MN` or `ADP` + `AF3`/`ALF`/`BEF`/`MGF` ligand context before CIF parsing. Prioritize remaining `protein_kinase_precatalytic_substrate_atp` and `protein_kinase_substrate_bound_amp_pnp` rows not previously seen in lane artifacts. Continue the next-week `23FC` publication/current-release check when a new RCSB release or metadata appears.

Production claims/label changes remain forbidden: yes.
