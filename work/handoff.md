# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.
The central artifact is a mechanism-first knowledge graph, benchmark suite, and
enzyme discovery pipeline that maps protein evidence to catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval. Geometry artifacts now cover
20-, 30-, 40-, 50-, 60-, 75-, 100-, 125-, 150-, 175-, 200-, and 225-entry
slices.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
225 entries, including all entries in the 225-entry source slice.

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

- Cleared the 175-entry near-miss boundary while preserving 0 hard negatives,
  0 out-of-scope false non-abstentions, and 0 actionable in-scope failures.
- Added auditable counterevidence penalty details to retrieval and hard-negative
  artifacts.
- Expanded the curated registry from 175 to 225 labels and generated 200- and
  225-entry graph, benchmark, geometry, retrieval, calibration, evaluation,
  cofactor, seed-family, margin, hard-negative, label-candidate, mapping, slice
  summary, and performance artifacts.
- Added 25 provisional labels for entries 201-225. The 225-entry label queue is
  now empty.
- Added ligand/cofactor context fixes for `PLV` and `PDD` PLP variants, clearing
  PLP-dependent `m_csa:186` and `m_csa:213` as evidence-limited abstentions.
- Added counterevidence for ThDP/phosphomutase/biotin transfer contexts,
  nonflavin Fe-S electron-transfer contexts, and nonhydrolytic Ser/His
  electrophile contexts; these clear new 200- and 225-entry hard negatives.
- Updated regression tests to lock the 225-entry stress slice and regenerated
  public docs to match the current metrics.

## Current Metrics

- Curated label registry: 225 labels. The 225-entry geometry evaluation covers
  224 geometry entries, 221 evaluable active-site structures, 71 in-scope
  positives, and 153 evaluated out-of-scope controls.
- 20-entry slice: threshold `0.4104`, 20/20 evaluable, 7/7 in-scope positives
  retained, 0 false non-abstentions, 0 hard negatives.
- 125-entry slice: threshold `0.4115`, 124/125 evaluable, 38/38 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  score gap `0.0308`.
- 150-entry slice: threshold `0.4145`, 148/150 evaluable, 43/44 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 in-scope failure, 0 actionable failures, correct-positive gap `0.0278`.
- 175-entry slice: threshold `0.4145`, 173/175 evaluable, 58/59 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 in-scope failure, 0 actionable failures, correct-positive gap `0.0101`.
- 200-entry slice: threshold `0.4145`, 197/200 evaluable, 64/65 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 in-scope failure, 0 actionable failures.
- 225-entry slice: threshold `0.4145`, 221/224 evaluable, 70/71 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 in-scope failure, 0 actionable failures.
- The remaining in-scope failure is `m_csa:132`, an evidence-limited abstention
  where the selected `1LUC` structure lacks expected flavin/NAD evidence.
- Retained evidence-limited positives are `m_csa:41`, `m_csa:108`, and
  `m_csa:160`; the smallest retained evidence-limited margin is `0.01`.
- Cofactor policy recommendation across all slices is
  `audit_only_or_separate_stratum`; no tested post-hoc cofactor penalty reduces
  evidence-limited retained positives without losing retained positives.
- The closest below-floor out-of-scope control is `m_csa:134`, a
  metal-dependent hydrolase hit `0.0101` below the correct-positive floor.
- Seed-family audit: the largest 225-entry in-scope family is
  `metal_dependent_hydrolase` with 32 labels; weakest retained family is
  `flavin_monooxygenase` at 0.5 retained top3 accuracy.
- Label expansion queue: 0 unlabeled entries and 0 ready review candidates in
  the 225-entry slice.
- Structure mapping: 0 issues through 100 entries, 1 labeled out-of-scope issue
  at 125 entries, 2 labeled out-of-scope issues at 150 and 175 entries, and 3
  labeled out-of-scope issues at 200 and 225 entries.
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
PYTHONPATH=src python -m catalytic_earth.cli analyze-in-scope-failures --retrieval artifacts/v3_geometry_retrieval_225.json --abstain-threshold 0.4145 --out artifacts/v3_in_scope_failure_analysis_225.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-cofactor-policy --retrieval artifacts/v3_geometry_retrieval_225.json --abstain-threshold 0.4145 --out artifacts/v3_cofactor_policy_225.json
PYTHONPATH=src python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_225.json --out artifacts/v3_hard_negative_controls_225.json
```

## Next Agent Start Here

Focus on extending or stress-testing the now-clean 225-entry benchmark while
preserving the current guardrails: 0 hard negatives, 0 near misses, 0
out-of-scope false non-abstentions, 0 actionable in-scope failures, and
retention of the fragile `m_csa:160` evidence-limited positive.

First bounded task:

1. Build a 250-entry graph/benchmark/geometry/retrieval candidate queue.
2. Run label expansion candidates for 250 and curate only the highest-readiness
   bounded tranche if time permits.
3. Regenerate retrieval/evaluation/failure/cofactor-policy/margin/
   hard-negative artifacts for all slices, including any new slice added to
   `GEOMETRY_SLICES`.
4. If 250 exposes hard negatives, prefer auditable chemistry counterevidence
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

- STARTED_AT: 2026-05-09T18:26:28.820122-05:00
- ENDED_AT: 2026-05-09T19:21:39.866381-05:00
- Measured elapsed time: 55.2 minutes
- Final verification before handoff: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`, and
  `PYTHONPATH=src python -m unittest discover -s tests` passed with 85 tests.
