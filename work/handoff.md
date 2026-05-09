# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.
The central artifact is a mechanism-first knowledge graph, benchmark suite, and
enzyme discovery pipeline that maps protein evidence to catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval. Geometry artifacts now cover
20-, 30-, 40-, 50-, 60-, 75-, 100-, 125-, and 150-entry slices.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
150 entries, including all entries in the 150-entry geometry slice.

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

- Expanded the graph, benchmark, geometry, retrieval, calibration, evaluation,
  failure-analysis, hard-negative, label-candidate, and mapping-issue artifacts
  through the 150-entry slice.
- Expanded curated labels from 125 to 150 entries.
- Added in-scope failure analysis as a CLI/performance workflow and artifact
  family (`artifacts/v3_in_scope_failure_analysis*.json`).
- Added cross-slice geometry summaries via
  `src/catalytic_earth/geometry_reports.py` and
  `artifacts/v3_geometry_slice_summary.json`.
- Tightened geometry counterevidence for hydrogenase/redox metal contexts,
  nonheme iron aromatic oxygenase-like contexts, nonflavin Fe-S/metal contexts,
  molybdenum-center contexts, and flavin monooxygenase substrate contexts.
- Added regression tests that keep the 125-entry slice clean and track the
  150-entry in-scope failure boundary.
- Updated README, geometry docs, performance docs, V2 report notes, and scope
  documentation for the 150-entry state.

## Current Metrics

- Curated label registry: 150 labels; 46 seed-fingerprint positives and 104
  out-of-scope controls.
- 20-entry slice: threshold `0.4681`, 20/20 evaluable, 7/7 in-scope positives
  retained, 0 false non-abstentions, 0 hard negatives.
- 100-entry slice: threshold `0.4704`, 100/100 evaluable, 25/25 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives.
- 125-entry slice: threshold `0.4704`, 124/125 evaluable, 38/38 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  score gap `0.0562`.
- 150-entry slice: threshold `0.5144`, 148/150 evaluable, 43/46 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  3 in-scope failures, correct-positive gap `0.0122`, broad score gap `-0.169`.
- 150-entry failure causes: 2 `target_cofactor_context_absent` rows and 1
  `target_absent_from_top_k` row.
- Remaining 150-entry in-scope failures:
  `m_csa:132` (`flavin_monooxygenase`), `m_csa:139`
  (`flavin_dehydrogenase_reductase`), and `m_csa:140`
  (`cobalamin_radical_rearrangement`).
- Label expansion queue: 0 unlabeled entries and 0 ready review candidates in
  the 150-entry slice.
- Structure mapping: 0 issues through 100 entries, 1 labeled out-of-scope issue
  at 125 entries, 2 labeled out-of-scope issues at 150 entries.
- Verification so far: `PYTHONPATH=src python -m unittest discover -s tests`
  passed with 74 tests; `PYTHONPATH=src python -m catalytic_earth.cli validate`
  passed with 150 curated labels.

## Start Commands

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-in-scope-failures --retrieval artifacts/v3_geometry_retrieval_150.json --abstain-threshold 0.5144 --out artifacts/v3_in_scope_failure_analysis_150.json
```

## Next Agent Start Here

Focus on the 3 evidence-limited in-scope failures in the 150-entry slice while
preserving the current clean out-of-scope boundary.

First bounded task:

1. Open `artifacts/v3_in_scope_failure_analysis_150.json`.
2. Inspect `m_csa:132`, `m_csa:139`, and `m_csa:140` against
   `artifacts/v3_geometry_features_150.json` and
   `artifacts/v3_geometry_retrieval_150.json`.
3. Decide whether each failure is a scoring problem, a missing local cofactor
   feature, a seed-family gap, or a label that should stay in scope but remain
   abstained.
4. Implement the smallest scoring, feature, or label-audit change that reduces
   a real failure without creating hard negatives in any slice.
5. Regenerate retrieval/evaluation/failure/margin/hard-negative artifacts for
   all slices and rerun tests.

Known blockers:

- Labels are provisional and not expert-reviewed; do not claim validated enzyme
  function.
- Geometry retrieval is heuristic, not learned.
- Ligand/cofactor evidence uses nearby mmCIF ligand atoms and inferred roles;
  it does not model occupancy, alternate conformers, biological assembly, or
  substrate state.
- The 150-entry failures may be legitimate abstentions if the local structure
  evidence lacks the expected cofactor context.
- Full-database scalability has not been measured; `perf-suite` is local
  artifact timing only.
