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

- Audited the 150-entry in-scope failures and reclassified `m_csa:139` and
  `m_csa:140` as out-of-scope for the current local active-site geometry
  benchmark.
- Added structure-wide ligand inventory to geometry features alongside the
  existing proximal ligand context.
- Added `analyze-cofactor-coverage`, generated
  `artifacts/v3_cofactor_coverage*.json`, and included the benchmark in the
  local performance suite.
- Split in-scope failure reporting into total failures, actionable failures,
  and evidence-limited abstentions.
- Regenerated geometry, retrieval, calibration, evaluation, failure, cofactor
  coverage, margin, hard-negative, label-candidate, mapping, slice-summary, and
  performance artifacts across all current slices.
- Updated regression tests for the new 150-entry boundary and cofactor coverage
  metrics.

## Current Metrics

- Curated label registry: 150 labels; 44 local active-site seed-fingerprint
  positives and 106 out-of-scope controls.
- 20-entry slice: threshold `0.4681`, 20/20 evaluable, 7/7 in-scope positives
  retained, 0 false non-abstentions, 0 hard negatives.
- 100-entry slice: threshold `0.4704`, 100/100 evaluable, 25/25 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives.
- 125-entry slice: threshold `0.4704`, 124/125 evaluable, 38/38 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  score gap `0.0562`.
- 150-entry slice: threshold `0.5144`, 148/150 evaluable, 43/44 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 in-scope failure, 0 actionable failures, correct-positive gap `0.0122`,
  broad score gap `-0.1222`.
- 150-entry failure cause: `m_csa:132` is
  `target_cofactor_absent_from_structure`; the selected `1LUC` structure lacks
  expected flavin/NAD evidence, so it remains an evidence-limited abstention.
- Cofactor coverage: 39/44 in-scope positives have local cofactor support, 1
  has expected cofactor support only elsewhere in the selected structure, 2
  require no cofactor, and 2 lack expected structure-wide cofactor evidence.
  One absent-expected-cofactor positive is retained (`m_csa:41`) and one is
  abstained (`m_csa:132`); the structure-only support case is `m_csa:108`.
- Evidence-limited retained positives are explicit in cofactor coverage
  metadata: `m_csa:41` and `m_csa:108`. This is an audit flag, not a score
  penalty, so the current clean out-of-scope boundary is unchanged.
- Label expansion queue: 0 unlabeled entries and 0 ready review candidates in
  the 150-entry slice.
- Structure mapping: 0 issues through 100 entries, 1 labeled out-of-scope issue
  at 125 entries, 2 labeled out-of-scope issues at 150 entries.
- Final verification before handoff: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`, and
  `PYTHONPATH=src python -m unittest discover -s tests` passed. Documentation
  was reviewed and updated across README, docs, scope, handoff, and status
  inputs before regenerating the progress status.

## Start Commands

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-in-scope-failures --retrieval artifacts/v3_geometry_retrieval_150.json --abstain-threshold 0.5144 --out artifacts/v3_in_scope_failure_analysis_150.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-cofactor-coverage --retrieval artifacts/v3_geometry_retrieval_150.json --abstain-threshold 0.5144 --out artifacts/v3_cofactor_coverage_150.json
```

## Remaining-Time Plan Executed

The initial assigned 150-entry failure audit reduced the actionable failure
count to 0 before the productive-work boundary. Remaining time was used to add
structure-wide ligand inventory, cofactor coverage analysis, evidence-limited
abstention accounting, explicit evidence-limited retained-positive metadata,
cross-slice summary fields, tests, regenerated artifacts, and documentation
updates.

Measured run time: 2026-05-09T21:22:55Z to 2026-05-09T22:16:55Z. The wrap-up
included documentation review, diff checks, validation, and repeated regression
test verification before the measured work log was written.

## Next Agent Start Here

Focus on whether evidence-limited retained positives should remain audit-only
flags or receive a scoring/abstention penalty, while preserving the current
clean out-of-scope boundary and keeping `m_csa:132` as an evidence-limited
abstention unless new structure evidence supports it.

First bounded task:

1. Open `artifacts/v3_cofactor_coverage_150.json` and compare
   `evidence_limited_retained_entry_ids` (`m_csa:41`, `m_csa:108`) with
   `evidence_limited_abstained_entry_ids` (`m_csa:132`).
2. Decide whether retained role-inferred or structure-only cofactor positives
   should be down-weighted, remain retained with audit flags, or become a
   separate calibration stratum.
3. If changing scoring, keep the 20- through 150-entry slices at 0 hard
   negatives and 0 out-of-scope false non-abstentions, and do not regress the
   audited 125-entry clean slice without recording the tradeoff.
4. Regenerate retrieval/evaluation/failure/cofactor-coverage/margin/
   hard-negative artifacts for all slices and rerun tests.

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
