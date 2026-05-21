# ePK Positive Evidence Handoff

Last updated: 2026-05-21T04:17:26Z

Pushed commit: `5f0c21c02e089f6cc8068107beaf7b9d2cc9e645` (primary run artifacts/ledger commit created with a temporary index because the linked local gitdir still blocks normal ref updates). A follow-up handoff commit should be the final remote head for this run.

## Current Outcome

Primary outcome: `candidate_evidence_rows_emitted`.

This run completed the handoff's guarded continuation for source-rich phrase rows, then converted prior compact hits into candidate-level evidence rows. The fresh guarded searches did not find a new clean folded-protein ePK transfer-state positive. The candidate-row backfill emitted 84 `epk_candidate_evidence_v1` rows for review-only adjudication and stress testing.

All candidate rows separate `source_free_geometry` from `source_context`. Source review fields are discovery context only and must not become predictive coordinate features. Every emitted row keeps `policy_decision=review_only_abstain`, `countable_label_candidate=false`, `production_claim_allowed=false`, and `ready_for_production_scoring=false`.

No production labels, thresholds, registries, fingerprints, migrations, scoring paths, or production claims were changed.

## Files Changed

- `artifacts/research_lanes/epk_positive_evidence/3rep_ilk_source_review_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/active_gamma_source_candidate_rows_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/bound_state_source_candidate_rows_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/guarded_phrase_candidate_rows_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/guarded_phrase_candidate_rows_include_prior_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/prior_candidate_evidence_rows_20260521.json`
- `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`
- `tools/research_lanes/epk_positive_evidence/guarded_phrase_candidate_rows.py`
- `tools/research_lanes/epk_positive_evidence/prior_candidate_evidence_row_backfill.py`
- `work/research_lanes/epk_positive_evidence/handoff.md`

## Evidence For

- `prior_candidate_evidence_rows_20260521.json` emitted 84 candidate-level rows from 121 prior compact source rows: 66 `active_gamma` and 18 `transition_analog`.
- The backfill includes 43 folded-protein or folded-protein-length-unknown candidate rows and 28 local-metal candidate rows for review-only source adjudication.
- The guarded helper now supports surface sets, pre-CIF exact ligand/metal filters, prior-PDB skipping, current-run prior ignores, row timeouts, CIF size guards, and candidate-row source/geometry separation.
- `3REP` was a fresh active-gamma source-term donor state: ILK/alpha-parvin with ATP/Mn on ILK.

## Evidence Against

- No fresh candidate-level positive row was emitted by the guarded searches.
- The phrase continuation returned 17 exact-context PDB IDs, all prior-seen; repeat-inclusive review found only donor-or-analog-without-heteromeric-acceptor rows.
- The active-gamma source-term set returned 324 rows across 13 surfaces; after skipping 192 prior-seen IDs, only fresh `3REP` was reviewed, and its nearest alpha-parvin Tyr306 hydroxyl was 14.923 Angstrom from ILK ATP PG.
- The bound-state wording set returned 487 rows across 12 surfaces and all IDs were prior-seen under the pre-CIF guard.
- `3REP` has no article DOI/PubMed metadata in RCSB, and Europe PMC exact-title/alias checks returned zero article rows.

## Candidate-Row Notes

- Candidate-level rows are not PDB-level assertions. A row binds one donor/analog site to one acceptor candidate where compact prior geometry existed.
- Discovery signal tags and `discovery_signal_score` are review triage only. They are not production scoring features.
- Product/transition-analog rows remain `review_only_abstain` unless a future frozen policy is preregistered and survives stress review.
- Rows with `source_mapping_pending`, `candidate_entity_length_unknown`, `no_local_mg_or_mn`, or `transition_or_product_analog_state_not_countable` should not be treated as countable positives.

## Blockers

- Startup `git fetch origin` and `git pull --ff-only origin research/epk-positive-evidence` failed with `Operation not permitted` while writing `.git/worktrees/catalytic-earth-epk-positive/FETCH_HEAD`.
- `git fetch --no-write-fetch-head origin research/epk-positive-evidence` succeeded.
- The local branch/worktree remains stale relative to `origin/research/epk-positive-evidence`; normal local ref/index updates may still fail. Use temporary-index `commit-tree` on top of `origin/research/epk-positive-evidence` and direct push verification if needed.
- Production claims, threshold calibration, label import, registry edits, fingerprint changes, migrations, scoring, and production helper fallback remain forbidden.

## Next Query

Source-adjudicate the `epk_candidate_evidence_v1` backfill rows by priority:

- First: local-metal `active_gamma` rows and folded-protein/folded-protein-length-unknown rows with `source_mapping_pending`.
- Then: known stress anchors `23FC`, `5HVK`, `9UUR`/`9UUX`, `3X2U`/`3X2V`/`3X2W`, `1QMZ`, `1L3R`, `5LIH`, and `1HE1` as a counterexample.
- At the next RCSB weekly release, re-run current-date/2026 exact-ligand surfaces and the `23FC` publication metadata check.

Production claims/label changes remain forbidden: yes.
