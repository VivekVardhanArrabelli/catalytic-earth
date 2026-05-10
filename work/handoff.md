# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.
The central artifact is a mechanism-first knowledge graph, benchmark suite, and
enzyme discovery pipeline that maps protein evidence to catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval. Geometry artifacts now cover
20-, 30-, 40-, 50-, 60-, 75-, 100-, 125-, 150-, 175-, 200-, 225-, 250-, 275-,
300-, 325-, 350-, and 375-entry curated slices. A 400-entry candidate queue has
also been generated for the next curation pass, but it is not yet a curated
benchmark slice.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
375 entries, including all entries in the 375-entry source slice.

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

- Expanded the curated registry from 275 to 375 labels and generated 300-, 325-,
  350-, and 375-entry graph, benchmark, geometry, retrieval, calibration,
  evaluation, cofactor, seed-family, margin, hard-negative, label-candidate,
  mapping, slice-summary, and performance artifacts.
- Added retrieval counterevidence for thiamine carboligation, zinc
  methyltransfer, nonhydrolytic Ser/His acyl transfer, nonhydrolytic
  hydratase/dehydratase, alpha-ketoglutarate hydroxylation, heme dehydratase,
  and flavin mutase contexts.
- Generated a 400-entry unlabeled candidate queue with graph, benchmark,
  geometry, retrieval, label-expansion, and structure-mapping artifacts.
- Updated regression tests to lock the 375-entry stress slice, the expanded
  cross-slice summary, and the new counterevidence rules.
- Reviewed and updated README, docs, scope, handoff, and status inputs during
  wrap-up so current metrics and next steps no longer point at 275 as current.

## Current Metrics

- Curated label registry: 375 labels. The 375-entry geometry evaluation covers
  374 geometry entries, 367 evaluable active-site structures, 98 in-scope
  positives, and 276 evaluated out-of-scope controls.
- 20-entry slice: threshold `0.4104`, 20/20 evaluable, 7/7 in-scope positives
  retained, 0 false non-abstentions, 0 hard negatives.
- 125-entry slice: threshold `0.4115`, 124/125 evaluable, 38/38 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  score gap `0.0308`.
- 275-entry slice: threshold `0.4115`, 271/274 evaluable, 80/81 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 evidence-limited in-scope abstention, 0 actionable failures.
- 300-entry slice: threshold `0.4115`, 296/299 evaluable, 85/86 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 evidence-limited in-scope abstention, 0 actionable failures.
- 325-entry slice: threshold `0.4115`, 320/324 evaluable, 90/91 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 evidence-limited in-scope abstention, 0 actionable failures.
- 350-entry slice: threshold `0.4115`, 344/349 evaluable, 93/94 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 evidence-limited in-scope abstention, 0 actionable failures.
- 375-entry slice: threshold `0.4115`, 367/374 evaluable, 95/98 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  3 evidence-limited in-scope abstentions, 0 actionable failures.
- Evidence-limited abstentions in the 375 slice are `m_csa:132`, `m_csa:353`,
  and `m_csa:372`.
- Retained evidence-limited positives are `m_csa:41`, `m_csa:108`, and
  `m_csa:160`; the smallest retained evidence-limited margin is `0.013`.
- Cofactor policy recommendation across all slices is
  `audit_only_or_separate_stratum`; no tested post-hoc cofactor penalty reduces
  evidence-limited retained positives without losing retained positives.
- The closest below-floor out-of-scope control is `m_csa:65`, a
  metal-dependent hydrolase hit `0.0131` below the correct-positive floor.
- Label expansion queue: 0 unlabeled entries and 0 ready review candidates in
  the 375-entry slice. The separate 400-entry queue has 399 geometry entries,
  25 unlabeled candidate rows, and 22 ready label-review entries.
- Structure mapping: 0 issues through 100 entries, 1 labeled out-of-scope issue
  at 125 entries, 2 labeled out-of-scope issues at 150 and 175 entries, 3 at
  200 through 300 entries, 4 at 325 entries, 5 at 350 entries, and 7 at 375
  entries.

## Start Commands

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-in-scope-failures --retrieval artifacts/v3_geometry_retrieval_375.json --abstain-threshold 0.4115 --out artifacts/v3_in_scope_failure_analysis_375.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-cofactor-policy --retrieval artifacts/v3_geometry_retrieval_375.json --abstain-threshold 0.4115 --out artifacts/v3_cofactor_policy_375.json
PYTHONPATH=src python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_375.json --out artifacts/v3_hard_negative_controls_375.json
PYTHONPATH=src python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_400.json --retrieval artifacts/v3_geometry_retrieval_400.json --out artifacts/v3_label_expansion_candidates_400.json
```

## Next Agent Start Here

Focus on curating the generated 400-entry candidate queue while preserving the
current guardrails: 0 hard negatives, 0 near misses, 0 out-of-scope false
non-abstentions, 0 actionable in-scope failures, and audit visibility for
`m_csa:41`, `m_csa:108`, and `m_csa:160`.

First bounded task:

1. Review `artifacts/v3_label_expansion_candidates_400.json` and curate a
   small, high-confidence tranche from entries 376-400.
2. Obvious likely positives include `m_csa:376`, `m_csa:379`, `m_csa:381`,
   `m_csa:383`, `m_csa:395`, and `m_csa:399`; verify each against mechanism
   text before labeling.
3. Treat likely high-scoring controls carefully, including racemase,
   tRNA-ligase, vanadium bromoperoxidase, laccase, glycosidase, transferase,
   and phosphoribosyltransferase contexts in entries such as `m_csa:377`,
   `m_csa:384`, `m_csa:386`, `m_csa:390`, `m_csa:391`, `m_csa:393`,
   `m_csa:397`, and `m_csa:400`.
4. If labels are added through 400, add a 400-entry `GEOMETRY_SLICES` row,
   regenerate retrieval/evaluation/failure/cofactor-policy/margin/
   hard-negative artifacts, and update regression tests.
5. If 400 exposes hard negatives, prefer auditable chemistry counterevidence
   over label relaxation; preserve evidence-limited abstentions unless better
   selected-structure cofactor evidence appears.

Known blockers:

- Labels are provisional and not expert-reviewed; do not claim validated enzyme
  function.
- Geometry retrieval is heuristic, not learned.
- Ligand/cofactor evidence uses nearby and structure-wide mmCIF ligand atoms
  plus inferred roles; it does not model occupancy, alternate conformers,
  biological assembly, or substrate state.
- `m_csa:132`, `m_csa:353`, and `m_csa:372` are currently best treated as
  evidence-limited abstentions because selected structures lack expected local
  or structure-wide cofactor evidence.
- Full-database scalability has not been measured; `perf-suite` is local
  artifact timing only.

## Run Timing

- STARTED_AT: 2026-05-10T01:28:55Z
- ENDED_AT: 2026-05-10T02:23:10Z
- Measured elapsed time: 54.25 minutes
- Documentation checked and updated across README, docs, scope, handoff, and
  status inputs before final status regeneration.
- Final verification before handoff: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`, and
  `PYTHONPATH=src python -m unittest discover -s tests` passed with 105 tests.
