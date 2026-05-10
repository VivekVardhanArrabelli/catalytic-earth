# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.
The central artifact is a mechanism-first knowledge graph, benchmark suite, and
enzyme discovery pipeline that maps protein evidence to catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval. Geometry artifacts now cover
20-, 30-, 40-, 50-, 60-, 75-, 100-, 125-, 150-, 175-, 200-, 225-, 250-, 275-,
300-, 325-, 350-, 375-, 400-, 425-, and 450-entry curated slices. A 475-entry
candidate queue has also been generated for the next curation pass, but it is
not yet a curated benchmark slice.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
450 entries, including all entries in the 450-entry source slice.

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

- Expanded the curated registry from 375 to 450 labels.
- Generated 400-, 425-, and 450-entry graph, benchmark, geometry, retrieval,
  calibration, evaluation, cofactor, seed-family, margin, hard-negative,
  label-candidate, mapping, slice-summary, and performance artifacts.
- Added M-CSA role synonym handling for catalytic coherence, aminoacyl-ligase
  and glycosidase counterevidence for metal-hydrolase false positives, and PLP
  text boosts for ligand-supported transaldimination and beta-elimination.
- Cleared the 400-, 425-, and 450-entry guardrails: 0 hard negatives, 0 near
  misses, 0 out-of-scope false non-abstentions, and 0 actionable in-scope
  failures.
- Generated a 475-entry unlabeled candidate queue with graph, benchmark,
  geometry, retrieval, label-expansion, and structure-mapping artifacts.
- Reviewed and updated README, docs, scope, handoff, and status inputs during
  wrap-up so current metrics and next steps point at the 450 curated slice and
  the 475 queue.

## Current Metrics

- Curated label registry: 450 labels, with 124 seed-fingerprint positives and
  326 out-of-scope labels.
- 20-entry slice: threshold `0.4104`, 20/20 evaluable, 7/7 in-scope positives
  retained, 0 false non-abstentions, 0 hard negatives.
- 125-entry slice: threshold `0.4115`, 124/125 evaluable, 38/38 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  score gap `0.0308`.
- 375-entry slice: threshold `0.4115`, 367/374 evaluable, 95/98 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  3 evidence-limited in-scope abstentions, 0 actionable failures.
- 400-entry slice: threshold `0.4115`, 392/399 evaluable, 103/106 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  3 evidence-limited in-scope abstentions, 0 actionable failures.
- 425-entry slice: threshold `0.4115`, 417/424 evaluable, 114/117 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  3 evidence-limited in-scope abstentions, 0 actionable failures.
- 450-entry slice: threshold `0.4115`, 442/449 evaluable, 120/124 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  4 evidence-limited in-scope abstentions, 0 actionable failures.
- Evidence-limited abstentions in the 450 slice are `m_csa:132`, `m_csa:353`,
  `m_csa:372`, and `m_csa:430`.
- Retained evidence-limited positives are `m_csa:41`, `m_csa:108`,
  `m_csa:160`, and `m_csa:446`; the smallest retained evidence-limited margin
  is `0.013`.
- Cofactor policy recommendation across all slices is
  `audit_only_or_separate_stratum`; no tested post-hoc cofactor penalty reduces
  evidence-limited retained positives without losing retained positives.
- The closest below-floor out-of-scope control is still `m_csa:65`, a
  metal-dependent hydrolase hit `0.0131` below the correct-positive floor.
- Label expansion queue: 0 unlabeled entries and 0 ready review candidates in
  the 450-entry slice. The separate 475-entry queue has 474 geometry entries,
  25 unlabeled candidate rows, and 23 ready label-review entries.
- Structure mapping: 0 issues through 100 entries, 1 labeled out-of-scope issue
  at 125 entries, 2 at 150 and 175 entries, 3 at 200 through 300 entries, 4 at
  325 entries, 5 at 350 entries, and 7 at 375, 400, 425, and 450 entries.
- Local performance was regenerated on 450 artifacts in `artifacts/perf_report.json`.

## Start Commands

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
PYTHONPATH=src python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_475.json --retrieval artifacts/v3_geometry_retrieval_475.json --out artifacts/v3_label_expansion_candidates_475.json
```

## Next Agent Start Here

Focus on curating the generated 475-entry candidate queue while preserving the
current guardrails: 0 hard negatives, 0 near misses, 0 out-of-scope false
non-abstentions, 0 actionable in-scope failures, and audit visibility for
`m_csa:41`, `m_csa:108`, `m_csa:160`, and `m_csa:446`.

First bounded task:

1. Review `artifacts/v3_label_expansion_candidates_475.json` and curate a
   high-confidence tranche from entries 451-476.
2. Obvious likely positives include `m_csa:453` and `m_csa:465` as Ser-His-Asp
   esterases, `m_csa:472` as a metal-dependent phosphatase, and `m_csa:473` as
   a heme nitric-oxide reductase candidate; verify each against mechanism text
   before labeling.
3. Treat likely high-scoring controls carefully, including transferase,
   dehydrogenase, nucleoside hydrolase, dehydratase/lyase, phosphatase,
   glycosidase, and mutase contexts in entries such as `m_csa:451`,
   `m_csa:457`, `m_csa:464`, `m_csa:471`, `m_csa:474`, and `m_csa:475`.
4. If labels are added through 475, add a 475-entry `GEOMETRY_SLICES` row,
   regenerate retrieval/evaluation/failure/cofactor-policy/margin/
   hard-negative artifacts, and update regression tests.
5. If 475 exposes hard negatives or near misses, prefer auditable chemistry
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

- STARTED_AT: 2026-05-10T02:30:25Z
- ENDED_AT: 2026-05-10T03:25:56Z
- Measured elapsed time: 55.517 minutes
- Documentation checked and updated across README, docs, scope, handoff, and
  status inputs before final status regeneration.
- Final verification before handoff: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`, and
  `PYTHONPATH=src python -m unittest discover -s tests` passed with 113 tests.
