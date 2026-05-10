# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.
The central artifact is a mechanism-first knowledge graph, benchmark suite, and
enzyme discovery pipeline that maps protein evidence to catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval and label-factory quality
automation. Geometry artifacts now cover
20-, 30-, 40-, 50-, 60-, 75-, 100-, 125-, 150-, 175-, 200-, 225-, 250-, 275-,
300-, 325-, 350-, 375-, 400-, 425-, 450-, 475-, and 500-entry curated slices.
The 500-entry slice is countable only through the label-factory batch checks.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
499 entries, with one uncounted 500-slice review candidate remaining. Labels now
carry explicit bronze/silver/gold tier, review status, confidence, evidence
score, and evidence provenance fields.

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

- Added countable review-batch tooling:
  `build-review-decision-batch`, `import-countable-label-review`, and
  `check-label-batch-acceptance`. `filter-countable-labels` exists only for
  registries that are already countable; do not use it to collapse a
  review-state batch.
- Processed the 500-entry queue through two factory decision batches. The
  first accepted 23 labels; the second accepted `m_csa:486` after scorer
  support for metal-phosphate hydrolysis text context.
- Regenerated canonical 500-slice retrieval, evaluation, hard-negative,
  cofactor, label-factory, active-learning, expert-review, guardrail, and
  performance artifacts from the 499-label registry.
- Preserved review provenance by keeping automation-curated imports separate
  from expert-reviewed imports; gold labels still require expert review.
- Tightened two batch-safety guardrails: cobalamin-radical automation labels
  require local ligand-supported cobalamin evidence, and
  `filter-countable-labels` refuses lossy review-state filtering unless
  explicitly overridden.
- Updated tests for countable review import, batch acceptance, 500-slice
  artifacts, and the metal-phosphate hydrolysis scorer support path.

## Current Metrics

- Curated label registry: 499 labels, with 131 seed-fingerprint positives and
  368 out-of-scope labels. Registry labels remain 499 bronze,
  automation-curated records; the applied-label artifact proposes 63 silver
  labels and 101 `needs_expert_review` labels without overwriting the registry.
- 20-entry slice: threshold `0.4104`, 20/20 evaluable, 7/7 in-scope positives
  retained, 0 false non-abstentions, 0 hard negatives.
- 125-entry slice: threshold `0.4115`, 124/125 evaluable, 38/38 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  score gap `0.0308`.
- 450-entry slice: threshold `0.4115`, 442/449 evaluable, 120/124 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  4 evidence-limited in-scope abstentions, 0 actionable failures.
- 475-entry slice: threshold `0.4115`, 467/474 evaluable, 123/127 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  4 evidence-limited in-scope abstentions, 0 actionable failures.
- 500-entry countable slice: threshold `0.4115`, 490/498 evaluated labeled
  rows evaluable, 127/131 in-scope positives retained, 0 false
  non-abstentions, 0 hard negatives, 0 near misses, 4 evidence-limited in-scope
  abstentions, 0 actionable failures.
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
- Label expansion queue: 499 geometry entries, 499 labeled entries, 1 unlabeled
  candidate row, and 1 ready label-review entry (`m_csa:494`).
- Label factory: 63 bronze-to-silver promotions proposed, 101
  abstention/review rows flagged, 100 adversarial negatives mined from 367
  out-of-scope candidates, 102 active-learning review rows queued, 26
  expert-review export items generated, the remaining unlabeled 500-slice
  candidate included in export, and 9/9 gate checks passing.
- Latest batch acceptance: 1 additional label accepted for counting, 6
  review-state decisions pending, 499 countable labels, 0 hard negatives,
  0 near misses, 0 out-of-scope false non-abstentions, and 0 actionable
  in-scope failures.
- Structure mapping: 0 issues through 100 entries, 1 labeled out-of-scope issue
  at 125 entries, 2 at 150 and 175 entries, 3 at 200 through 300 entries, 4 at
  325 entries, 5 at 350 entries, 7 at 375, 400, 425, 450, and 475 entries, and
  8 at 500 entries.
- Local performance was regenerated on 500 artifacts in `artifacts/perf_report.json`.

## Start Commands

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m catalytic_earth.cli automation-lock --lock-dir .git/catalytic-earth-automation.lock status
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
PYTHONPATH=src python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_500.json --retrieval artifacts/v3_geometry_retrieval_500.json --out artifacts/v3_label_expansion_candidates_500.json
PYTHONPATH=src python -m catalytic_earth.cli build-adversarial-negatives --retrieval artifacts/v3_geometry_retrieval_500.json --abstain-threshold 0.4115 --out artifacts/v3_adversarial_negative_controls_500.json
PYTHONPATH=src python -m catalytic_earth.cli build-label-factory-audit --retrieval artifacts/v3_geometry_retrieval_500.json --hard-negatives artifacts/v3_hard_negative_controls_500.json --adversarial-negatives artifacts/v3_adversarial_negative_controls_500.json --abstain-threshold 0.4115 --out artifacts/v3_label_factory_audit_500.json
PYTHONPATH=src python -m catalytic_earth.cli apply-label-factory-actions --label-factory-audit artifacts/v3_label_factory_audit_500.json --out artifacts/v3_label_factory_applied_labels_500.json
PYTHONPATH=src python -m catalytic_earth.cli build-active-learning-queue --geometry artifacts/v3_geometry_features_500.json --retrieval artifacts/v3_geometry_retrieval_500.json --label-factory-audit artifacts/v3_label_factory_audit_500.json --abstain-threshold 0.4115 --max-rows 150 --out artifacts/v3_active_learning_review_queue_500.json
PYTHONPATH=src python -m catalytic_earth.cli export-label-review --queue artifacts/v3_active_learning_review_queue_500.json --out artifacts/v3_expert_review_export_500.json
PYTHONPATH=src python -m catalytic_earth.cli import-label-review --review artifacts/v3_expert_review_export_500.json --out artifacts/v3_expert_review_import_preview_500.json
PYTHONPATH=src python -m catalytic_earth.cli build-review-decision-batch --review artifacts/v3_expert_review_export_500.json --batch-id 500_batch_next --reviewer automation_label_factory --out artifacts/v3_expert_review_decision_batch_500.json
PYTHONPATH=src python -m catalytic_earth.cli import-countable-label-review --review artifacts/v3_expert_review_decision_batch_500.json --labels data/registries/curated_mechanism_labels.json --out artifacts/v3_countable_labels_batch_500.json
PYTHONPATH=src python -m catalytic_earth.cli build-family-propagation-guardrails --geometry artifacts/v3_geometry_features_500.json --retrieval artifacts/v3_geometry_retrieval_500.json --out artifacts/v3_family_propagation_guardrails_500.json
PYTHONPATH=src python -m catalytic_earth.cli check-label-factory-gates --label-factory-audit artifacts/v3_label_factory_audit_500.json --applied-label-factory artifacts/v3_label_factory_applied_labels_500.json --active-learning-queue artifacts/v3_active_learning_review_queue_500.json --adversarial-negatives artifacts/v3_adversarial_negative_controls_500.json --expert-review-export artifacts/v3_expert_review_export_500.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_500.json --out artifacts/v3_label_factory_gate_check_500.json
```

## Next Agent Start Here

Focus on resolving the single remaining 500-entry review candidate through the
label-factory workflow. Do not open a 525-entry tranche until `m_csa:494` is
either accepted, rejected, or intentionally preserved as a documented
non-countable evidence gap.

First bounded task:

1. Read `docs/label_factory.md`, `work/label_factory_notes.md`,
   `work/label_queue_500_notes.md`, and
   `artifacts/v3_expert_review_export_500.json`.
2. Inspect `m_csa:494` in the review export, retrieval artifact, cofactor
   coverage, and source geometry. The key issue is that B12 evidence is
   structure-wide only, 8.349 A from the selected active-site residues.
3. If evidence is strong enough, create a one-row decision batch and import it
   with `import-countable-label-review`; otherwise use
   `mark_needs_more_evidence` and document why it remains non-countable.
   For any new acceptance check, use `--baseline-label-count 499`; the existing
   `artifacts/v3_label_batch_acceptance_check_500.json` used baseline 498 only
   because it records the prior `m_csa:486` batch.
4. If a batch is accepted, regenerate graph/geometry/retrieval/evaluation,
   factory audit, adversarial negatives, active-learning queue, expert export,
   family-propagation guardrails, gate check, performance report, docs, and
   tests before counting labels.
5. Preserve the current guardrails: 0 hard negatives, 0 near misses,
   0 out-of-scope false non-abstentions, 0 actionable in-scope failures, and
   audit visibility for `m_csa:41`, `m_csa:108`, `m_csa:160`, `m_csa:446`,
   and `m_csa:486`.

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

- STARTED_AT: 2026-05-10T05:35:25Z
- ENDED_AT: 2026-05-10T06:26:21Z
- Measured elapsed time: 50.93 minutes
- Documentation checked and updated across README, docs, scope, handoff,
  label-factory notes, label-queue notes, and status inputs before final status
  regeneration.
- Final verification passed: `git diff --check`, `PYTHONPATH=src python -m
  catalytic_earth.cli validate`, `PYTHONPATH=src python -m unittest discover
  -s tests` passed with 132 tests, and the label-factory gate verified at 9/9
  passing gates.
