# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.

The central artifact is not a dashboard. It is a mechanism-first knowledge graph,
benchmark suite, and enzyme discovery pipeline that maps protein evidence to
catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval. Geometry artifacts now cover
the 20-entry regression slice plus 30-, 40-, 50-, 60-, 75-, and 100-entry
expansion slices.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
125 entries, including all 125 entries in the expanded geometry slice.

## Repository

Local path:

```text
/Users/vivekvardhanarrabelli/Documents/Codex/2026-05-08/check-out-careflly-u-can-use-2/catalytic-earth
```

GitHub:

```text
https://github.com/VivekVardhanArrabelli/catalytic-earth
```

## Before Work

1. Read `README.md`.
2. Read `work/scope.md`.
3. Read `work/status.md` if it exists.
4. Run:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## During Work

- Confirm the automation is configured as `gpt-5.5` with `xhigh` reasoning.
- Treat each automation run as a measured hour with a strict 50-minute
  productive work requirement followed by about 5 minutes of wrap-up.
- From the real wall-clock start timestamp until 50 elapsed minutes, keep doing
  productive work that advances completion of the whole project.
- If the assigned task finishes early or becomes blocked, do not hand off
  immediately. Write a short plan for the remaining wall-clock time before the
  50-minute wrap-up boundary and execute the highest-value bounded unblocked
  item toward project completion.
- At 50 minutes elapsed, stop starting new implementation work and begin
  wrap-up: finish tests/artifacts/docs, update this handoff, log measured time,
  regenerate status, commit, and push.
- Prefer durable code and data schemas over prose.
- Keep outputs reproducible.
- Add tests for new normalization logic.
- Do not make wet-lab or deployment claims.
- End every automation block by updating `Next Agent Start Here` below with:
  what changed, where to continue, known blockers, the next concrete task, and
  first commands to run.

Log time and progress with:

```bash
PYTHONPATH=src python -m catalytic_earth.cli log-work --help
PYTHONPATH=src python -m catalytic_earth.cli progress-report --out work/status.md
```

Use measured time going forward:

```bash
PYTHONPATH=src python -m catalytic_earth.cli log-work \
  --stage post-v2 \
  --task "..." \
  --minutes 0 \
  --time-mode measured \
  --started-at "2026-05-09T00:00:00+00:00" \
  --ended-at "2026-05-09T00:55:00+00:00"
```

## Push Rule

Automation runs must commit and push every hour, even if progress is
incremental. Prefer meaningful progress such as:

- new source adapter
- graph schema or graph builder improvement
- benchmark machinery
- discovery pipeline component
- candidate dossier generation
- meaningful documentation that changes execution
- important bug fix with tests

Before handoff, git must be fully synced so the next agent starts from canonical
state:

1. `git fetch origin`
2. `git pull --ff-only origin main` (or verify already up to date)
3. `git push origin main`
4. Verify `git rev-parse HEAD` equals `git rev-parse origin/main`
5. Verify no merge is in progress (`test ! -f .git/MERGE_HEAD`)

## V2 Report Rule

Only report "v2 done" when every criterion in `work/scope.md` under `V2 Target`
is actually satisfied and reproducible from commands in the repository.

## UI Context Note

Computer Use was attempted against the Codex app for context inspection, but the
tool reported that it is not allowed to operate on `com.openai.codex` for safety
reasons. Treat repository state and this handoff file as the reliable recovery
surface.

## Next Agent Start Here

Run started: `2026-05-09T18:17:48Z`.
Run ended: `2026-05-09T19:35:11Z` (`77.383` measured minutes).

What changed in this run:

- Expanded curated labels from 63 to 125 entries, covering every entry in the
  current 125-entry geometry expansion slice.
- Added `cobalamin_radical_rearrangement` and
  `flavin_dehydrogenase_reductase` seed fingerprints, with curated positives
  and demo coverage.
- Added scoring counterevidence for carbon-transfer/SAM-like ligands,
  nucleotide-transfer ligands, aromatic/positive role-inferred pockets,
  heme-only and cobalamin-only metal-like contexts, histidine-only metal sites,
  molybdenum-center heme-like contexts, absent PLP anchors, absent B12 context,
  and flavin context without reductant support.
- Expanded graph, benchmark, geometry, retrieval, evaluation, calibration,
  hard-negative, margin, label-candidate, and mapping-issue artifacts through
  the 125-entry slice.
- Updated the performance suite so label-evaluation timing uses the calibrated
  abstention threshold instead of the stale default.
- Updated README, geometry docs, V2 strengthening report, performance docs,
  scope, tests, and reproducibility commands.

Current metrics:

- Curated label registry: 125 labels; 38 seed-fingerprint positives and 87
  out-of-scope controls.
- 20-entry regression slice: threshold `0.565`, 20/20 evaluable, 5/5 in-scope
  positives retained, 0 out-of-scope false non-abstentions, 0 hard negatives,
  and 0 near misses.
- 40-entry expansion slice: threshold `0.565`, 40/40 evaluable, 14/14
  in-scope positives retained, 0 out-of-scope false non-abstentions.
- 50-entry graph slice: threshold `0.565`, 50/50 evaluable, 16/16 in-scope
  positives retained, 0 out-of-scope false non-abstentions.
- 60-entry expanded slice: threshold `0.5653`, 60/60 evaluable, 18/18
  in-scope positives retained, 0 out-of-scope false non-abstentions.
- 75-entry expanded slice: threshold `0.5653`, 75/75 evaluable, 20/20
  in-scope positives retained, 0 out-of-scope false non-abstentions.
- 100-entry expanded slice: threshold `0.5653`, 100/100 evaluable, 25/25
  in-scope positives retained, 0 out-of-scope false non-abstentions.
- 100-entry score margins: minimum in-scope top1 `0.5777`, maximum
  out-of-scope top1 `0.5652`, gap `0.0125`.
- 100-entry hard negatives: 0 score-overlap controls and 0 near misses within
  0.01 below the positive floor.
- 125-entry expanded slice: threshold `0.5877`, 124/125 evaluable, 29/38
  in-scope positives retained, 0 out-of-scope false non-abstentions, 74 hard
  negatives, 0 near misses, and score gap `-0.1404`.
- Label expansion queue: 0 unlabeled entries and 0 ready review candidates in
  the current 125-entry slice.
- Structure mapping issues: 0 non-OK entries in the 40-, 50-, 60-, 75-, and
  100-entry slices after auth/label residue fallback; 1 labeled out-of-scope
  insufficient-residue issue remains in the 125-entry slice (`m_csa:105`).
- Verification this run: 61 unit tests passed, registry validation passed, and
  local performance report regenerated.

Start commands:

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_125.json --out artifacts/v3_hard_negative_controls_125.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-geometry-score-margins --retrieval artifacts/v3_geometry_retrieval_125.json --out artifacts/v3_geometry_score_margins_125.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-geometry-failures --retrieval artifacts/v3_geometry_retrieval_125.json --abstain-threshold 0.5877 --out artifacts/v3_geometry_failure_analysis_125.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-structure-mapping-issues --geometry artifacts/v3_geometry_features_125.json --out artifacts/v3_structure_mapping_issues_125.json
```

Next concrete task:

Analyze and reduce the 125-entry hard-negative set without breaking the clean
20- through 100-entry regression slices. Start with
`artifacts/v3_hard_negative_controls_125.json` and
`artifacts/v3_geometry_score_margins_125.json`; group the 74 controls by top1
fingerprint and cofactor evidence, then add one bounded fingerprint split or
counterevidence rule with tests. The likely first target is separating generic
heme/flavin redox or metal-like oxidoreductase controls from true heme
peroxidase/oxidase, flavin dehydrogenase/reductase, and metal-dependent
hydrolase positives.

Known blockers:

- Labels are still provisional and small; do not claim validated enzyme
  function.
- Geometry retrieval is still heuristic, not learned.
- Ligand/cofactor evidence uses nearby mmCIF ligand atoms and inferred roles;
  it does not model occupancy, alternate conformers, biological assembly, or
  substrate state.
- The current label queue is empty for the 125-entry slice; quality work should
  focus on hard-negative separation before more label expansion.
- Full-database scalability has not been measured; `perf-suite` is local
  artifact timing only.
