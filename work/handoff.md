# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.
The central artifact is a mechanism-first knowledge graph, benchmark suite, and
enzyme discovery pipeline that maps protein evidence to catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval and label-factory quality
automation. Geometry artifacts now cover
20-, 30-, 40-, 50-, 60-, 75-, 100-, 125-, 150-, 175-, 200-, 225-, 250-, 275-,
300-, 325-, 350-, 375-, 400-, 425-, 450-, 475-, 500-, 525-, 550-, 575-,
600-, 625-, and 650-entry curated slices. The 500-entry and larger slices are
countable only through the label-factory batch checks.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
618 countable labels. Review-state registries preserve pending
`needs_expert_review` rows separately so unresolved evidence gaps do not count
as benchmark labels.

## Repository

Local path:

```text
/Users/vivekvardhanarrabelli/Documents/Codex/2026-05-08/check-out-careflly-u-can-use-2/catalytic-earth
```

GitHub:

```text
https://github.com/VivekVardhanArrabelli/catalytic-earth
```

## Operating Rules

1. Acquire `.git/catalytic-earth-automation.lock` before work; the tested
   `automation-lock` CLI command can enforce the same atomic lock rules.
2. Sync with `git fetch origin` and `git pull --ff-only origin main`.
3. Read `README.md`, `work/scope.md`, `work/status.md`, and this file.
4. Run `PYTHONPATH=src python -m unittest discover -s tests`.
5. Work productively until 50 elapsed wall-clock minutes, then wrap.
6. During wrap, update stale docs, log measured time, regenerate status,
   commit, push, verify `HEAD == origin/main`, and release the lock only when
   the worktree is clean.

## Recent Project Progress

- Recovered a stale automation lock with a dirty worktree and finalized the
  coherent in-progress label-factory scaling work rather than starting a
  conflicting tranche.
- Accepted gated 625- and 650-entry label-factory batches. The 625 batch added
  20 countable labels; the 650 batch added 19 countable labels.
- Tightened provisional review rules so Ser-His mechanism text paired with a
  metal-dependent top hit stays `needs_expert_review` unless explicit metal
  catalysis evidence is present.
- Added an active-learning gate requiring all unlabeled candidate rows to be
  retained even when the ranked queue is capped.
- Added `artifacts/v3_label_factory_batch_summary.json` to aggregate accepted
  batches, review debt, gate status, and active-queue retention.
- Added `artifacts/v3_review_debt_summary_650.json` to rank 53 evidence-gap
  rows for the next review pass.
- Added preview triage artifacts
  `artifacts/v3_review_evidence_gaps_675_preview.json` and
  `artifacts/v3_review_debt_summary_675_preview.json` so the 675 promotion
  decision can inspect evidence gaps first.
- Added `artifacts/v3_label_factory_preview_summary_675.json` to summarize the
  unpromoted preview's acceptance, pending-review, gate, and queue-retention
  metrics.
- Added `artifacts/v3_label_preview_promotion_readiness_675.json`; it is
  mechanically ready but recommends review before promotion because preview
  review debt increased, and it carries new-debt entry ids and next-action
  counts for audit. The gate requires preview summary counts to match
  acceptance and explicit unlabeled-candidate retention.
- After the preview-readiness gate was in place, used the remaining productive
  work window to expose carried/new debt entry ids and next-action counts in
  durable artifacts and regression tests.
- Added `work/label_preview_675_notes.md` with the accepted-label profile and
  top evidence gaps to inspect before promotion.
- Extended geometry slice summaries, regression tests, and performance timing
  through the 650-entry countable slice.
- Reviewed the generated 675 preview artifacts and left them unpromoted because
  readiness recommends review before promotion.

## Current Metrics

- Curated label registry: 618 bronze automation-curated labels, with 151
  seed-fingerprint positives and 467 out-of-scope labels.
- 20-entry slice: threshold `0.4104`, 20/20 evaluable, 7/7 in-scope positives
  retained, 0 false non-abstentions, 0 hard negatives.
- 125-entry slice: threshold `0.4115`, 124/125 evaluable, 38/38 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  score gap `0.0308`.
- 500-entry countable slice: threshold `0.4115`, 490/498 evaluated labeled
  rows evaluable, 127/131 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and `m_csa:494` preserved as non-countable.
- 525-entry countable slice: threshold `0.4115`, 514/522 evaluated labeled
  rows evaluable, 135/139 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 0 ready label candidates.
- 550-entry countable slice: threshold `0.4115`, 535/545 evaluated labeled
  rows evaluable, 140/144 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 0 ready label candidates.
- 575-entry countable slice: threshold `0.4115`, 552/562 evaluated labeled
  rows evaluable, 142/146 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 0 ready label candidates.
- 600-entry countable slice: threshold `0.4115`, 568/578 evaluated labeled
  rows evaluable, 143/147 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 0 ready label candidates.
- 625-entry countable slice: threshold `0.4115`, 584/598 evaluated labeled
  rows evaluable, 144/148 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 25 ready label candidates before the accepted
  batch decisions.
- 650-entry countable slice: threshold `0.4115`, 601/617 evaluated labeled
  rows evaluable, 147/151 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited
  in-scope abstentions, and 31 ready label candidates before the accepted
  batch decisions.
- Evidence-limited abstentions remain `m_csa:132`, `m_csa:353`, `m_csa:372`,
  and `m_csa:430`.
- Retained evidence-limited positives remain `m_csa:41`, `m_csa:108`,
  `m_csa:160`, `m_csa:446`, and `m_csa:486`; the smallest retained
  evidence-limited margin is `0.013`.
- Cofactor policy recommendation across all slices is
  `audit_only_or_separate_stratum`; no tested post-hoc cofactor penalty reduces
  evidence-limited retained positives without losing retained positives.
- The closest below-floor out-of-scope control is still `m_csa:65`, a
  metal-dependent hydrolase hit `0.0131` below the correct-positive floor.
- Label factory at 650: 75 bronze-to-silver promotions proposed, 144 active
  learning review rows queued, 100 adversarial negatives mined, 56
  expert-review export items generated, and 10/10 gate checks passing.
- Label batch summary: 7/7 accepted batches, 0 blockers, 0 hard negatives,
  0 near misses, 0 false non-abstentions, 0 actionable in-scope failures, and
  all active queues retained their unlabeled candidates.
- Latest accepted batch acceptance: 19 additional labels accepted for counting, 37
  review-state decisions pending, 618 countable labels, 0 hard negatives,
  0 near misses, 0 out-of-scope false non-abstentions, and 0 actionable
  in-scope failures.
- 650 post-batch active-learning queue: all 32 unlabeled candidates are
  retained; no unlabeled rows are omitted by the queue limit.
- Review debt summary: 53 evidence-gap rows, 37 `needs_more_evidence`
  decisions, 42 rows linked back to active-learning ranks, and `m_csa:494`
  remains the highest-priority local/structure-wide cofactor gap.
- 675 preview debt summary: 61 evidence-gap rows, 44 `needs_more_evidence`
  decisions, 44 rows linked back to active-learning ranks, 37 carried rows,
  24 new rows, full carried/new entry-id lists plus next-action counts by debt
  status in metadata, and `m_csa:494` remains the top-ranked debt row.
- 675 preview summary: 18 countable additions if promoted, 44 pending
  review-state rows, 10/10 gates passing, all unlabeled preview rows retained,
  and 0 blockers.
- 675 promotion readiness: mechanically ready, 0 blockers, but
  `review_before_promoting` with review-debt delta `+8` and
  needs-more-evidence delta `+7`.
- Structure mapping: 17 total mapping issues at 650.
- Local performance was regenerated on 650 artifacts in `artifacts/perf_report.json`.

## Start Commands

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m catalytic_earth.cli automation-lock --lock-dir .git/catalytic-earth-automation.lock status
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
PYTHONPATH=src python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_650.json --retrieval artifacts/v3_geometry_retrieval_650.json --labels artifacts/v3_imported_labels_batch_650.json --out artifacts/v3_label_expansion_candidates_650.json
PYTHONPATH=src python -m catalytic_earth.cli check-label-factory-gates --label-factory-audit artifacts/v3_label_factory_audit_650.json --applied-label-factory artifacts/v3_label_factory_applied_labels_650.json --active-learning-queue artifacts/v3_active_learning_review_queue_650.json --adversarial-negatives artifacts/v3_adversarial_negative_controls_650.json --expert-review-export artifacts/v3_expert_review_export_650_post_batch.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_650.json --out artifacts/v3_label_factory_gate_check_650.json
PYTHONPATH=src python -m catalytic_earth.cli summarize-review-debt --review-evidence-gaps artifacts/v3_review_evidence_gaps_675_preview.json --active-learning-queue artifacts/v3_active_learning_review_queue_675_preview_batch.json --baseline-review-debt artifacts/v3_review_debt_summary_650.json --max-rows 35 --out artifacts/v3_review_debt_summary_675_preview.json
PYTHONPATH=src python -m catalytic_earth.cli check-label-preview-promotion --preview-acceptance artifacts/v3_label_batch_acceptance_check_675_preview.json --preview-summary artifacts/v3_label_factory_preview_summary_675.json --preview-review-debt artifacts/v3_review_debt_summary_675_preview.json --current-review-debt artifacts/v3_review_debt_summary_650.json --out artifacts/v3_label_preview_promotion_readiness_675.json
```

## Next Agent Start Here

Start from the accepted 650 state. Do not reopen the accepted 625/650 batches.

1. Inspect `artifacts/v3_active_learning_review_queue_650.json`,
   `artifacts/v3_expert_review_export_650_post_batch.json`,
   `artifacts/v3_review_evidence_gaps_650.json`,
   `artifacts/v3_review_debt_summary_650.json`,
   `artifacts/v3_label_batch_acceptance_check_675_preview.json`,
   `artifacts/v3_label_factory_preview_summary_675.json`,
   `artifacts/v3_label_preview_promotion_readiness_675.json`,
   `artifacts/v3_review_debt_summary_675_preview.json`,
   `work/label_preview_675_notes.md`, and the generated
   `artifacts/v1_graph_675.json` / `artifacts/v2_benchmark_675.json` scaffold.
2. Decide whether to promote the existing 675 preview or first do an
   evidence-quality pass on the persistent review-state rows. Promotion should
   only happen after inspecting the readiness/debt artifacts; do not rerun the
   accepted 625/650 batches.
3. Keep `m_csa:650` in review unless explicit metal-catalysis evidence is
   added; it is the new regression case for Ser-His text with a metal-dependent
   top retrieval hit.

Known blockers:

- Labels are provisional and not expert-reviewed; do not claim validated enzyme
  function.
- Bronze/silver/gold tiers are evidence-management tiers, not wet-lab
  validation status.
- Geometry retrieval is heuristic, not learned.
- Ligand/cofactor evidence uses nearby and structure-wide mmCIF ligand atoms
  plus inferred roles; it does not model occupancy, alternate conformers,
  biological assembly, or substrate state.
- `m_csa:132`, `m_csa:353`, `m_csa:372`, and `m_csa:430` are currently best
  treated as evidence-limited abstentions because selected structures lack
  expected local or structure-wide cofactor evidence.
- Full-database scalability has not been measured; `perf-suite` is local
  artifact timing only.

## Run Timing

- STARTED_AT: 2026-05-10T13:45:58Z
- ENDED_AT: 2026-05-10T14:37:04Z
- Measured elapsed time: 51.100 minutes
- Documentation checked and updated across README, docs, scope, handoff,
  label-factory notes, preview notes, and status inputs before final status
  regeneration.
- Final verification passed: `git diff --check`, `PYTHONPATH=src python -m
  catalytic_earth.cli validate`, and `PYTHONPATH=src python -m unittest
  discover -s tests` passed with 146 tests.
- Note: stale-lock recovery continued from the accepted 650 state and left the
  675 preview unpromoted; the next scheduled run should inspect the preview
  readiness/debt artifacts before any promotion.
