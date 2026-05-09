# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.
The central artifact is a mechanism-first knowledge graph, benchmark suite, and
enzyme discovery pipeline that maps protein evidence to catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval. Geometry artifacts now cover
20-, 30-, 40-, 50-, 60-, 75-, 100-, 125-, 150-, and 175-entry slices.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
175 entries, including all entries in the 175-entry geometry slice.

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

- Added executable cofactor abstention policy sweeps and seed-family performance
  audits, with CLI commands, performance-suite coverage, and tests.
- Expanded the geometry benchmark from 150 to 175 fully labeled M-CSA entries.
- Added 25 curated labels for entries 151-175, raising the registry to 175
  labels: 59 seed-fingerprint positives and 116 out-of-scope controls.
- Regenerated 175-entry graph, benchmark, geometry, retrieval, calibration,
  evaluation, cofactor coverage, cofactor policy, seed-family, margin,
  hard-negative, label-candidate, structure-mapping, summary, and performance
  artifacts.
- Removed sodium and potassium from inferred metal-cofactor ligand families so
  alkali ions no longer create metal-hydrolase support.
- Added APC nucleotide-transfer context and tightened molybdenum-center heme
  counterevidence, reducing 175-entry near misses from 18 to 17 without
  introducing hard negatives or false non-abstentions.
- Extended hard-negative artifacts with near-miss family/evidence counts,
  closest near-miss metadata, counterevidence reason counts, and group-level
  near-miss gaps.

## Current Metrics

- Curated label registry: 175 labels; 59 local active-site seed-fingerprint
  positives and 116 out-of-scope controls.
- 20-entry slice: threshold `0.4104`, 20/20 evaluable, 7/7 in-scope positives
  retained, 0 false non-abstentions, 0 hard negatives.
- 125-entry slice: threshold `0.4236`, 124/125 evaluable, 38/38 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  score gap `0.103`.
- 150-entry slice: threshold `0.4236`, 148/150 evaluable, 43/44 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 0 near misses,
  1 in-scope failure, 0 actionable failures, correct-positive gap `0.103`.
- 175-entry slice: threshold `0.4236`, 173/175 evaluable, 58/59 in-scope
  positives retained, 0 false non-abstentions, 0 hard negatives, 17 near
  misses, 1 in-scope failure, 0 actionable failures, correct-positive gap
  `0.001`.
- The remaining in-scope failure is `m_csa:132`, an evidence-limited abstention
  where the selected `1LUC` structure lacks expected flavin/NAD evidence.
- Retained evidence-limited positives are `m_csa:41`, `m_csa:108`, and
  `m_csa:160`; the smallest retained evidence-limited margin is `0.0009`.
- Cofactor policy recommendation across all slices is
  `audit_only_or_separate_stratum`; no tested post-hoc cofactor penalty reduces
  evidence-limited retained positives without losing retained positives.
- The 175-entry near-miss set is 17 metal-dependent hydrolase hits: 9
  role-inferred and 8 ligand-supported. The closest is `m_csa:65`, `0.001`
  below the correct-positive floor.
- Seed-family audit: the largest 175-entry in-scope family is
  `metal_dependent_hydrolase` with 28 labels; weakest retained family is
  `flavin_monooxygenase` at 0.5 retained top3 accuracy.
- Label expansion queue: 0 unlabeled entries and 0 ready review candidates in
  the 175-entry slice.
- Structure mapping: 0 issues through 100 entries, 1 labeled out-of-scope issue
  at 125 entries, and 2 labeled out-of-scope issues at both 150 and 175 entries.
- Documentation was reviewed and updated across README, docs, scope, handoff,
  and status inputs before final status regeneration.

## Start Commands

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-in-scope-failures --retrieval artifacts/v3_geometry_retrieval_175.json --abstain-threshold 0.4236 --out artifacts/v3_in_scope_failure_analysis_175.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-cofactor-policy --retrieval artifacts/v3_geometry_retrieval_175.json --abstain-threshold 0.4236 --out artifacts/v3_cofactor_policy_175.json
PYTHONPATH=src python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_175.json --out artifacts/v3_hard_negative_controls_175.json
```

## Next Agent Start Here

Focus on reducing the 175-entry near-miss boundary while preserving the current
guardrails: 0 hard negatives, 0 out-of-scope false non-abstentions, 0 actionable
in-scope failures, and retention of the fragile `m_csa:160` evidence-limited
positive.

First bounded task:

1. Open `artifacts/v3_hard_negative_controls_175.json` and inspect the two
   `near_miss_groups`.
2. Start with the ligand-supported metal-hydrolase group:
   `m_csa:65`, `m_csa:151`, `m_csa:130`, `m_csa:126`, `m_csa:35`, `m_csa:95`,
   `m_csa:52`, and `m_csa:99`.
3. Test whether nucleotide-transfer, nonhydrolytic transfer, or redox ligand
   counterevidence can move these below the near-miss band without lowering
   retained positives, especially `m_csa:160`.
4. Regenerate retrieval/evaluation/failure/cofactor-policy/margin/
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

## Run Timing

- STARTED_AT: 2026-05-09T22:24:24Z
- ENDED_AT: 2026-05-09T23:20:06Z
- Measured elapsed time: 55.7 minutes
- Final verification before handoff: `git diff --check`,
  `PYTHONPATH=src python -m catalytic_earth.cli validate`, and
  `PYTHONPATH=src python -m unittest discover -s tests` passed.
