# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.
The central artifact is a mechanism-first knowledge graph, benchmark suite, and
enzyme discovery pipeline that maps protein evidence to catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval. Geometry artifacts now cover
20-, 30-, 40-, 50-, 60-, 75-, 100-, 125-, 150-, 175-, 200-, 225-, 250-, and
275-entry slices.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
275 entries, including all entries in the 275-entry source slice.

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

- Expanded the curated registry from 225 to 275 labels and generated 250- and
  275-entry graph, benchmark, geometry, retrieval, calibration, evaluation,
  cofactor, seed-family, margin, hard-negative, label-candidate, mapping, slice
  summary, and performance artifacts.
- Added provisional labels for entries 226-275. The 275-entry label queue is now
  empty.
- Added mechanism-text-derived counterevidence for prenyl carbocation,
  NAD-linked redox, nonhydrolytic isomerase/lyase, phosphoryl-transfer, and
  methylcobalamin transfer contexts.
- Propagated entry names and mechanism snippets from geometry features into
  retrieval, label-evaluation, in-scope failure, hard-negative, cofactor
  coverage, score-margin, label-candidate, and structure-mapping review
  artifacts.
- Updated regression tests to lock the 275-entry stress slice and regenerated
  public docs to match the current metrics.

## Current Metrics

- Curated label registry: 275 labels. The 275-entry geometry evaluation covers
  274 geometry entries, 271 evaluable active-site structures, 81 in-scope
  positives, and 193 evaluated out-of-scope controls.
- 20-entry slice: threshold `0.4104`, 20/20 evaluable, 7/7 in-scope positives
  retained, 0 false non-abstentions, 0 hard negatives.
- 125-entry slice: threshold `0.4115`, 124/125 evaluable, 38/38 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  score gap `0.0308`.
- 150-entry slice: threshold `0.4115`, 148/150 evaluable, 43/44 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 in-scope failure, 0 actionable failures, correct-positive gap `0.0308`.
- 175-entry slice: threshold `0.4115`, 173/175 evaluable, 58/59 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 in-scope failure, 0 actionable failures, correct-positive gap `0.0131`.
- 200-entry slice: threshold `0.4115`, 197/200 evaluable, 64/65 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 in-scope failure, 0 actionable failures.
- 225-entry slice: threshold `0.4115`, 221/224 evaluable, 70/71 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 in-scope failure, 0 actionable failures.
- 250-entry slice: threshold `0.4115`, 246/249 evaluable, 77/78 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 in-scope failure, 0 actionable failures.
- 275-entry slice: threshold `0.4115`, 271/274 evaluable, 80/81 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 in-scope failure, 0 actionable failures.
- The remaining in-scope failure is `m_csa:132`, an evidence-limited abstention
  where the selected `1LUC` structure lacks expected flavin/NAD evidence.
- Retained evidence-limited positives are `m_csa:41`, `m_csa:108`, and
  `m_csa:160`; the smallest retained evidence-limited margin is `0.013`.
- Cofactor policy recommendation across all slices is
  `audit_only_or_separate_stratum`; no tested post-hoc cofactor penalty reduces
  evidence-limited retained positives without losing retained positives.
- The closest below-floor out-of-scope control is `m_csa:65`, a
  metal-dependent hydrolase hit `0.0131` below the correct-positive floor.
- Seed-family audit: the largest 275-entry in-scope family is
  `metal_dependent_hydrolase` with 35 labels; weakest retained family is
  `flavin_monooxygenase` at 0.5 retained top3 accuracy.
- Label expansion queue: 0 unlabeled entries and 0 ready review candidates in
  the 275-entry slice.
- Structure mapping: 0 issues through 100 entries, 1 labeled out-of-scope issue
  at 125 entries, 2 labeled out-of-scope issues at 150 and 175 entries, and 3
  labeled out-of-scope issues at 200, 225, 250, and 275 entries.
- Documentation reviewed and updated across README, docs, scope, handoff, and
  status inputs before final status regeneration.

## Start Commands

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-in-scope-failures --retrieval artifacts/v3_geometry_retrieval_275.json --abstain-threshold 0.4115 --out artifacts/v3_in_scope_failure_analysis_275.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-cofactor-policy --retrieval artifacts/v3_geometry_retrieval_275.json --abstain-threshold 0.4115 --out artifacts/v3_cofactor_policy_275.json
PYTHONPATH=src python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_275.json --out artifacts/v3_hard_negative_controls_275.json
```

## Next Agent Start Here

Focus on extending or stress-testing the now-clean 275-entry benchmark while
preserving the current guardrails: 0 hard negatives, 0 near misses, 0
out-of-scope false non-abstentions, 0 actionable in-scope failures, and
retention of the fragile `m_csa:160` evidence-limited positive.

First bounded task:

1. Build a 300-entry graph/benchmark/geometry/retrieval candidate queue.
2. Run label expansion candidates for 300 and curate only the highest-readiness
   bounded tranche if time permits.
3. Regenerate retrieval/evaluation/failure/cofactor-policy/margin/
   hard-negative artifacts for all slices, including any new slice added to
   `GEOMETRY_SLICES`.
4. If 300 exposes hard negatives, prefer auditable chemistry counterevidence
   over label relaxation; preserve `m_csa:132` as evidence-limited unless
   better selected-structure cofactor evidence appears.
5. Rerun `PYTHONPATH=src python -m unittest discover -s tests` and validate.

Known blockers:

- Labels are provisional and not expert-reviewed; do not claim validated enzyme
  function.
- Geometry retrieval is heuristic, not learned.
- Ligand/cofactor evidence uses nearby and structure-wide mmCIF ligand atoms
  plus inferred roles; it does not model occupancy, alternate conformers,
  biological assembly, or substrate state.
- `m_csa:132` is currently best treated as a legitimate abstention because the
  selected structure lacks expected flavin/NAD evidence.
- Full-database scalability has not been measured; `perf-suite` is local
  artifact timing only.

## Run Timing

- STARTED_AT: 2026-05-10T00:27:55Z
- ENDED_AT: 2026-05-10T01:18:22Z
- Measured elapsed time: 50.45 minutes
- Documentation checked and updated across README, docs, scope, handoff, and
  status inputs before final status regeneration.
- Final verification before handoff: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`, and
  `PYTHONPATH=src python -m unittest discover -s tests` passed with 96 tests.
