# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.
The central artifact is a mechanism-first knowledge graph, benchmark suite, and
enzyme discovery pipeline that maps protein evidence to catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval and label-factory quality
automation. Geometry artifacts now cover
20-, 30-, 40-, 50-, 60-, 75-, 100-, 125-, 150-, 175-, 200-, 225-, 250-, 275-,
300-, 325-, 350-, 375-, 400-, 425-, 450-, 475-, 500-, 525-, and 550-entry
curated slices. The 500-, 525-, and 550-entry slices are countable only through
the label-factory batch checks.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
546 countable labels. Review-state registries preserve pending
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

- Added targeted review-decision batches and review-resolution checks so one
  candidate can be deferred without reopening the whole queue.
- Added `analyze-review-evidence-gaps` to audit accepted/deferred decisions
  against retrieval, expected cofactor families, local versus structure-wide
  support, score thresholds, rank, and counterevidence.
- Documented `m_csa:494` as a non-countable cobalamin evidence gap because B12
  evidence is structure-wide only and 8.349 A from the selected active-site
  residues.
- Accepted gated 525- and 550-entry label-factory batches. The 525 batch added
  24 countable labels; the 550 batch added 23 countable labels.
- Fixed provisional Ser-His hydrolase review logic so strong hydrolase/lipase
  triad evidence is not rejected solely because local metal context is present.
- Extended geometry slice summaries to include the 525- and 550-entry artifacts.
- Regenerated canonical 525/550 graph, benchmark, geometry, retrieval,
  evaluation, hard-negative, cofactor, label-factory, active-learning,
  expert-review, guardrail, status, and performance artifacts.

## Current Metrics

- Curated label registry: 546 bronze automation-curated labels, with 144
  seed-fingerprint positives and 402 out-of-scope labels.
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
- Label factory at 550: 70 bronze-to-silver promotions proposed, 106 active
  learning review rows queued, 100 adversarial negatives mined, 25
  expert-review export items generated, and 9/9 gate checks passing.
- Latest batch acceptance: 23 additional labels accepted for counting, 9
  review-state decisions pending, 546 countable labels, 0 hard negatives,
  0 near misses, 0 out-of-scope false non-abstentions, and 0 actionable
  in-scope failures.
- Structure mapping: 10 total mapping issues at 550, 8 of them in labeled rows.
- Local performance was regenerated on 550 artifacts in `artifacts/perf_report.json`.

## Start Commands

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m catalytic_earth.cli automation-lock --lock-dir .git/catalytic-earth-automation.lock status
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
PYTHONPATH=src python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_550.json --retrieval artifacts/v3_geometry_retrieval_550.json --out artifacts/v3_label_expansion_candidates_550.json
PYTHONPATH=src python -m catalytic_earth.cli check-label-factory-gates --label-factory-audit artifacts/v3_label_factory_audit_550.json --applied-label-factory artifacts/v3_label_factory_applied_labels_550.json --active-learning-queue artifacts/v3_active_learning_review_queue_550.json --adversarial-negatives artifacts/v3_adversarial_negative_controls_550.json --expert-review-export artifacts/v3_expert_review_export_550.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_550.json --out artifacts/v3_label_factory_gate_check_550.json
```

## Next Agent Start Here

Open the next bounded tranche from the 550 review-state registry, not from the
plain countable registry, so pending rows remain explicitly reviewed rather than
rediscovered as unlabeled candidates.

First bounded task:

1. Read `docs/label_factory.md`, `work/label_factory_notes.md`,
   `work/label_queue_550_notes.md`, and
   `artifacts/v3_imported_labels_batch_550.json`.
2. Build the 575-entry graph/benchmark/geometry/retrieval artifacts, then build
   `artifacts/v3_label_expansion_candidates_575_pre_batch.json` against the
   550 review-state registry if the CLI path supports an alternate labels file.
   If it does not, add that support before generating the queue.
3. Run a provisional decision batch only for ready 575 candidates. Keep
   cobalamin candidates deferred unless local ligand-supported B12 evidence is
   present, and preserve review-state placeholders for unresolved rows.
4. Import countable accepted decisions against the 546-label baseline, generate
   the countable registry preview, and run batch acceptance with a baseline
   count of `546`.
5. Regenerate evaluation, hard negatives, in-scope failures, adversarial
   negatives, label-factory audit, active-learning queue, expert-review export,
   family-propagation guardrails, gate check, performance report if the slice is
   accepted, docs, and tests before counting labels.

Alternative bounded task if 575 setup is blocked: work down pending
review-state evidence gaps (`m_csa:494`, `m_csa:510`, `m_csa:529`,
`m_csa:534`, `m_csa:535`, `m_csa:536`, `m_csa:539`, `m_csa:541`, and
`m_csa:548`) with `analyze-review-evidence-gaps`, but do not mark any row
countable without local evidence or expert-review provenance.

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

- STARTED_AT: 2026-05-10T06:37:00Z
- ENDED_AT: 2026-05-10T07:28:08Z
- Measured elapsed time: 51.133 minutes
- Documentation checked and updated across README, docs, scope, handoff,
  label-factory notes, label-queue notes, and status inputs before final status
  regeneration.
- Final verification passed: `git diff --check`, `PYTHONPATH=src python -m
  catalytic_earth.cli validate`, and `PYTHONPATH=src python -m unittest
  discover -s tests` passed with 135 tests.
