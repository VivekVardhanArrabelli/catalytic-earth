# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.
The central artifact is a mechanism-first knowledge graph, benchmark suite, and
enzyme discovery pipeline that maps protein evidence to catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval and label-factory quality
automation. Geometry artifacts now cover
20-, 30-, 40-, 50-, 60-, 75-, 100-, 125-, 150-, 175-, 200-, 225-, 250-, 275-,
300-, 325-, 350-, 375-, 400-, 425-, 450-, and 475-entry curated slices. A
500-entry candidate queue has also been generated for the next curation pass,
but it is not yet a curated benchmark slice.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
475 entries, including all entries in the 475-entry source slice. Labels now
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

- Migrated all 475 labels to explicit tier/review/evidence fields while keeping
  the curated registry bronze and automation-curated.
- Added `data/registries/mechanism_ontology.json` and loader validation for
  mechanism-family hierarchy and fingerprint coverage.
- Added label-factory commands for deterministic promotion/demotion audit,
  applying audit actions to a review artifact, active-learning queue ranking,
  adversarial negative mining, family-propagation guardrails, expert-review
  export/import, and gate checking.
- Added tested code-level automation lock helpers in
  `src/catalytic_earth/automation.py` and exposed them through
  `python -m catalytic_earth.cli automation-lock`.
- Generated current label-factory artifacts:
  `artifacts/v3_label_factory_audit_475.json`,
  `artifacts/v3_label_factory_applied_labels_475.json`,
  `artifacts/v3_adversarial_negative_controls_475.json`,
  `artifacts/v3_active_learning_review_queue_500.json`,
  `artifacts/v3_expert_review_export_500.json`,
  `artifacts/v3_expert_review_import_preview_500.json`,
  `artifacts/v3_family_propagation_guardrails_500.json`, and
  `artifacts/v3_label_factory_gate_check_500.json`.
- Expanded performance checks to include label-factory audit, adversarial
  negative mining, and active-learning queue generation.
- Added `docs/label_factory.md` and refreshed README/docs/work scope so label
  scaling is gated by factory checks before new labels count.

## Current Metrics

- Curated label registry: 475 labels, with 127 seed-fingerprint positives and
  348 out-of-scope labels. Registry labels remain 475 bronze,
  automation-curated records; the applied-label artifact proposes 61 silver
  labels and 98 `needs_expert_review` labels without overwriting the registry.
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
- Evidence-limited abstentions remain `m_csa:132`, `m_csa:353`, `m_csa:372`,
  and `m_csa:430`.
- Retained evidence-limited positives remain `m_csa:41`, `m_csa:108`,
  `m_csa:160`, and `m_csa:446`; the smallest retained evidence-limited margin
  is `0.013`.
- Cofactor policy recommendation across all slices is
  `audit_only_or_separate_stratum`; no tested post-hoc cofactor penalty reduces
  evidence-limited retained positives without losing retained positives.
- The closest below-floor out-of-scope control is still `m_csa:65`, a
  metal-dependent hydrolase hit `0.0131` below the correct-positive floor.
- Label expansion queue: 0 unlabeled entries and 0 ready review candidates in
  the 475-entry slice. The separate 500-entry queue has 499 geometry entries,
  25 unlabeled candidate rows, and 21 ready label-review entries.
- Label factory: 61 bronze-to-silver promotions proposed, 98
  abstention/review rows flagged, 100 adversarial negatives mined from 347
  out-of-scope candidates, 123 active-learning review rows queued, 50
  expert-review export items generated, all 25 unlabeled 500-slice candidates
  included in export, and 9/9 gate checks passing.
- Structure mapping: 0 issues through 100 entries, 1 labeled out-of-scope issue
  at 125 entries, 2 at 150 and 175 entries, 3 at 200 through 300 entries, 4 at
  325 entries, 5 at 350 entries, and 7 at 375, 400, 425, 450, and 475 entries.
- Local performance was regenerated on 475 artifacts in `artifacts/perf_report.json`.

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
PYTHONPATH=src python -m catalytic_earth.cli build-adversarial-negatives --retrieval artifacts/v3_geometry_retrieval_475.json --abstain-threshold 0.4115 --out artifacts/v3_adversarial_negative_controls_475.json
PYTHONPATH=src python -m catalytic_earth.cli build-label-factory-audit --retrieval artifacts/v3_geometry_retrieval_475.json --hard-negatives artifacts/v3_hard_negative_controls_475.json --adversarial-negatives artifacts/v3_adversarial_negative_controls_475.json --abstain-threshold 0.4115 --out artifacts/v3_label_factory_audit_475.json
PYTHONPATH=src python -m catalytic_earth.cli apply-label-factory-actions --label-factory-audit artifacts/v3_label_factory_audit_475.json --out artifacts/v3_label_factory_applied_labels_475.json
PYTHONPATH=src python -m catalytic_earth.cli build-active-learning-queue --geometry artifacts/v3_geometry_features_500.json --retrieval artifacts/v3_geometry_retrieval_500.json --label-factory-audit artifacts/v3_label_factory_audit_475.json --abstain-threshold 0.4115 --max-rows 150 --out artifacts/v3_active_learning_review_queue_500.json
PYTHONPATH=src python -m catalytic_earth.cli export-label-review --queue artifacts/v3_active_learning_review_queue_500.json --out artifacts/v3_expert_review_export_500.json
PYTHONPATH=src python -m catalytic_earth.cli import-label-review --review artifacts/v3_expert_review_export_500.json --out artifacts/v3_expert_review_import_preview_500.json
PYTHONPATH=src python -m catalytic_earth.cli build-family-propagation-guardrails --geometry artifacts/v3_geometry_features_500.json --retrieval artifacts/v3_geometry_retrieval_500.json --out artifacts/v3_family_propagation_guardrails_500.json
PYTHONPATH=src python -m catalytic_earth.cli check-label-factory-gates --label-factory-audit artifacts/v3_label_factory_audit_475.json --applied-label-factory artifacts/v3_label_factory_applied_labels_475.json --active-learning-queue artifacts/v3_active_learning_review_queue_500.json --adversarial-negatives artifacts/v3_adversarial_negative_controls_475.json --expert-review-export artifacts/v3_expert_review_export_500.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_500.json --out artifacts/v3_label_factory_gate_check_500.json
```

## Next Agent Start Here

Focus on using the label-factory workflow to process the generated 500-entry
candidate queue. Do not add labels directly from
`artifacts/v3_label_expansion_candidates_500.json`; route decisions through
`artifacts/v3_active_learning_review_queue_500.json` and
`artifacts/v3_expert_review_export_500.json`, then import accepted decisions
into a registry copy before counting them.

First bounded task:

1. Read `docs/label_factory.md`, `work/label_factory_notes.md`,
   `work/label_queue_500_notes.md`, and
   `artifacts/v3_expert_review_export_500.json`.
2. Fill a small first decision batch in a copy of the expert-review export.
   Prioritize the 25 unlabeled rows plus high-impact boundary controls; likely
   positives remain `m_csa:482`, `m_csa:486`, `m_csa:495`, and `m_csa:497`,
   with `m_csa:494` requiring caution because B12 evidence is structure-only.
3. Import decisions with `import-label-review` to a registry copy; do not
   overwrite `data/registries/curated_mechanism_labels.json` until the batch
   artifact passes validation and review.
4. If a batch is accepted, regenerate graph/geometry/retrieval/evaluation,
   factory audit, adversarial negatives, active-learning queue, expert export,
   family-propagation guardrails, gate check, performance report, docs, and
   tests before counting labels.
5. Preserve the current guardrails: 0 hard negatives, 0 near misses,
   0 out-of-scope false non-abstentions, 0 actionable in-scope failures, and
   audit visibility for `m_csa:41`, `m_csa:108`, `m_csa:160`, and `m_csa:446`.

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

- STARTED_AT: 2026-05-10T04:33:25Z
- ENDED_AT: 2026-05-10T05:24:48Z
- Measured elapsed time: 51.38 minutes
- Documentation checked and updated across README, docs, scope, handoff,
  label-factory notes, label-queue notes, and status inputs before final status
  regeneration.
- Final verification passed: `git diff --check`, `PYTHONPATH=src python -m
  catalytic_earth.cli validate`, `PYTHONPATH=src python -m unittest discover
  -s tests` passed with 130 tests, and the label-factory gate regenerated at
  9/9 passing gates.
