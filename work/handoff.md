# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.
The central artifact is a mechanism-first knowledge graph, benchmark suite, and
enzyme discovery pipeline that maps protein evidence to catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval. Geometry artifacts now cover
20-, 30-, 40-, 50-, 60-, 75-, 100-, 125-, 150-, 175-, 200-, 225-, 250-, 275-,
300-, 325-, 350-, 375-, 400-, 425-, 450-, and 475-entry curated slices. A
500-entry candidate queue has also been generated for the next curation pass,
but it is not yet a curated benchmark slice.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
475 entries, including all entries in the 475-entry source slice.

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

1. Acquire `.git/catalytic-earth-automation.lock` before work.
2. Sync with `git fetch origin` and `git pull --ff-only origin main`.
3. Read `README.md`, `work/scope.md`, `work/status.md`, and this file.
4. Run `PYTHONPATH=src python -m unittest discover -s tests`.
5. Work productively until 50 elapsed wall-clock minutes, then wrap.
6. During wrap, update stale docs, log measured time, regenerate status,
   commit, push, verify `HEAD == origin/main`, and release the lock only when
   the worktree is clean.

## What Changed In This Run

- Expanded the curated registry from 450 to 475 labels and corrected
  `m_csa:39` from a metal-hydrolase seed to out-of-scope nucleoside-hydrolase
  chemistry.
- Added the 475-entry slice to cross-slice geometry reporting and regenerated
  retrieval, calibration, evaluation, failure, cofactor, margin,
  hard-negative, label-candidate, slice-summary, and performance artifacts.
- Added metal-hydrolase counterevidence for phosphoenolpyruvate transfer and
  zinc/metal-bound dehydrogenase contexts, extended glycosidase/nucleoside
  hydrolase text controls, and added purine/ribose analog ligand context.
- Generated a 500-entry graph, benchmark, geometry, retrieval, label-candidate,
  and structure-mapping queue for the next curation pass.
- Improved the 500-entry queue before labeling: `5PA` now maps to PLP context,
  and `FII` plus farnesyltransferase text now trigger prenyl-transfer
  counterevidence for the `m_csa:484` metal-hydrolase lookalike.
- Added `work/label_queue_500_notes.md` with a bounded curation plan for the
  next 25 unlabeled candidates.

## Current Metrics

- Curated label registry: 475 labels, with 127 seed-fingerprint positives and
  348 out-of-scope labels.
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
- Structure mapping: 0 issues through 100 entries, 1 labeled out-of-scope issue
  at 125 entries, 2 at 150 and 175 entries, 3 at 200 through 300 entries, 4 at
  325 entries, 5 at 350 entries, and 7 at 375, 400, 425, 450, and 475 entries.
- Local performance was regenerated on 475 artifacts in `artifacts/perf_report.json`.

## Start Commands

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
PYTHONPATH=src python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_500.json --retrieval artifacts/v3_geometry_retrieval_500.json --out artifacts/v3_label_expansion_candidates_500.json
```

## Next Agent Start Here

Focus on curating the generated 500-entry candidate queue while preserving the
current guardrails: 0 hard negatives, 0 near misses, 0 out-of-scope false
non-abstentions, 0 actionable in-scope failures, and audit visibility for
`m_csa:41`, `m_csa:108`, `m_csa:160`, and `m_csa:446`.

First bounded task:

1. Read `work/label_queue_500_notes.md` and
   `artifacts/v3_label_expansion_candidates_500.json`.
2. Verify the high-confidence likely positives before adding labels:
   `m_csa:482` as PLP, `m_csa:486` and `m_csa:495` as metal hydrolases,
   `m_csa:497` as flavin dehydrogenase/reductase, and cautiously `m_csa:494`
   as cobalamin radical rearrangement with a known structure-only B12 gap.
3. Treat the likely controls in `m_csa:477`-`m_csa:502` as out-of-scope unless
   mechanism text supports a current seed fingerprint; `m_csa:492` may be a
   future thiol-hydrolase seed, but it is outside the current seeds.
4. If labels are added through the queue, add a 500-entry `GEOMETRY_SLICES`
   row, regenerate all slice artifacts so label counts are consistent, refresh
   regression expectations, and rerun the full tests.
5. If 500 exposes hard negatives or near misses, prefer auditable chemistry
   counterevidence over label relaxation; preserve evidence-limited
   abstentions unless better selected-structure cofactor evidence appears.

Known blockers:

- Labels are provisional and not expert-reviewed; do not claim validated enzyme
  function.
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

- STARTED_AT: 2026-05-10T03:31:20Z
- ENDED_AT: 2026-05-10T04:23:06Z
- Measured elapsed time: 51.77 minutes
- Documentation checked and updated across README, docs, scope, handoff, and
  status inputs before final status regeneration.
- Final verification passed: `git diff --check`, `python -m
  catalytic_earth.cli validate`, and `PYTHONPATH=src python -m unittest
  discover -s tests` passed with 116 tests.
