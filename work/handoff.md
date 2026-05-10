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
600-, and 625-preview entry curated slices. The 500-entry and larger slices are
countable only through the label-factory batch checks.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
579 countable labels. Review-state registries preserve pending
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

## What Changed In This Run

- Accepted gated 575- and 600-entry label-factory batches. The 575 batch added
  17 countable labels; the 600 batch added 16 countable labels.
- Tightened provisional review rules so high-scoring metal-boundary,
  non-abstaining out-of-scope, unresolved-geometry seed, and Ser-His synthase
  boundary cases remain `needs_expert_review` instead of becoming countable
  labels.
- Extended geometry slice summaries and regression tests through the 600-entry
  countable slice.
- Generated a 625-entry preview scaffold through geometry, retrieval,
  pre-batch queue, provisional decisions, preview import, and preview
  acceptance. It is intentionally not promoted to the canonical registry yet.
- Regenerated canonical 575/600 graph, benchmark, geometry, retrieval,
  evaluation, hard-negative, cofactor, label-factory, active-learning,
  expert-review, guardrail, status, and performance artifacts.

## Current Metrics

- Curated label registry: 579 bronze automation-curated labels, with 147
  seed-fingerprint positives and 432 out-of-scope labels.
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
- Label factory at 600: 72 bronze-to-silver promotions proposed, 106 active
  learning review rows queued, 100 adversarial negatives mined, 25
  expert-review export items generated, and 9/9 gate checks passing.
- Latest accepted batch acceptance: 16 additional labels accepted for counting, 26
  review-state decisions pending, 579 countable labels, 0 hard negatives,
  0 near misses, 0 out-of-scope false non-abstentions, and 0 actionable
  in-scope failures.
- 625 preview: 20 additional labels would be accepted, 31 review-state
  decisions would remain pending, and the preview has 0 hard negatives,
  0 near misses, and 0 out-of-scope false non-abstentions. It is not counted
  until the next run promotes it.
- Structure mapping: 11 total mapping issues at 600. The 625 preview has 15.
- Local performance was regenerated on 600 artifacts in `artifacts/perf_report.json`.

## Start Commands

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m catalytic_earth.cli automation-lock --lock-dir .git/catalytic-earth-automation.lock status
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
PYTHONPATH=src python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_600.json --retrieval artifacts/v3_geometry_retrieval_600.json --labels artifacts/v3_imported_labels_batch_600.json --out artifacts/v3_label_expansion_candidates_600.json
PYTHONPATH=src python -m catalytic_earth.cli check-label-factory-gates --label-factory-audit artifacts/v3_label_factory_audit_600.json --applied-label-factory artifacts/v3_label_factory_applied_labels_600.json --active-learning-queue artifacts/v3_active_learning_review_queue_600.json --adversarial-negatives artifacts/v3_adversarial_negative_controls_600.json --expert-review-export artifacts/v3_expert_review_export_600_post_batch.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_600.json --out artifacts/v3_label_factory_gate_check_600.json
```

## Next Agent Start Here

Review the 625 preview before doing any new scaling. The preview artifacts are
already generated:

1. Inspect `artifacts/v3_expert_review_decision_batch_625_preview.json`,
   `artifacts/v3_label_batch_acceptance_check_625_preview.json`, and
   `artifacts/v3_review_evidence_gaps_600.json`.
2. If the preview decisions are acceptable, promote
   `artifacts/v3_countable_labels_batch_625_preview.json` to
   `data/registries/curated_mechanism_labels.json`, rename/regenerate the
   canonical 625 artifacts without the `_preview` suffix, extend
   `GEOMETRY_SLICES` and tests to include 625, regenerate docs/status, and run
   validation/tests before committing.
3. If the preview decisions are not acceptable, leave the canonical registry at
   579 labels and record which 625 rows need deferral or rule changes before
   any labels are counted.

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

- STARTED_AT: 2026-05-10T07:37:59.343957Z
- ENDED_AT: 2026-05-10T08:36:35Z
- Measured elapsed time: 58.594 minutes
- Documentation checked and updated across README, docs, scope, handoff,
  label-factory notes, geometry/performance reports, and status inputs before
  final status regeneration.
- Final verification passed: `git diff --check`, `PYTHONPATH=src python -m
  catalytic_earth.cli validate`, and `PYTHONPATH=src python -m unittest
  discover -s tests` passed with 139 tests.
