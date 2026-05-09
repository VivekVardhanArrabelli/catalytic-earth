# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.

The central artifact is not a dashboard. It is a mechanism-first knowledge graph,
benchmark suite, and enzyme discovery pipeline that maps protein evidence to
catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval. Geometry artifacts now cover
the 20-entry regression slice plus 30-, 40-, 50-, and 60-entry expansion slices.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
63 entries, including all 60 entries in the expanded geometry slice.

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

Run started: `2026-05-09T17:16:40Z`.

What changed in this run:

- Expanded curated labels from 36 to 63 entries, covering all 60 entries in the
  current geometry expansion slice.
- Expanded source/benchmark artifacts to a 75-entry graph slice and geometry
  artifacts to a 60-entry slice.
- Fixed mmCIF structure mapping by matching catalytic residue positions against
  both `auth_*` and `label_*` chain/residue identifiers.
- Added geometry scoring counterevidence for metal-like false positives:
  transfer/redox context, heme-only context, cobalamin-only context, weak
  role-inferred pocket support, and metal-heavy Ser-His assignments.
- Added cobalamin ligand-family inference for B12/CNC/COB proximal ligands.
- Added hard-negative near-miss rows and CLI `--near-margin` support.
- Regenerated 20-, 30-, 40-, 50-, and 60-entry retrieval/evaluation/calibration
  artifacts, plus 60-entry hard-negative, score-margin, label-candidate,
  mapping-issue, and performance artifacts.
- Updated README, geometry docs, V2 report, performance docs, scope, tests, and
  reproducibility commands.

Current metrics:

- 20-entry regression slice: threshold `0.5682`, 20/20 evaluable, 4/4 in-scope
  positives retained, 0 out-of-scope false non-abstentions.
- 40-entry expansion slice: threshold `0.5777`, 40/40 evaluable, 12/12
  in-scope positives retained, 0 out-of-scope false non-abstentions.
- 50-entry graph slice: threshold `0.5777`, 50/50 evaluable, 13/13 in-scope
  positives retained, 0 out-of-scope false non-abstentions.
- 60-entry expanded slice: threshold `0.5931`, 60/60 evaluable, 5/13 in-scope
  positives retained, 0 out-of-scope false non-abstentions.
- 60-entry pre-abstention top1/top3 in-scope accuracy: `1.0` / `1.0`.
- 60-entry hard negatives: `m_csa:52` and `m_csa:53`; cobalamin-only context
  moved `m_csa:62` and `m_csa:63` below the positive score floor.
- 60-entry near misses within 0.01 below the positive floor: `m_csa:34` and
  `m_csa:2`.
- Label expansion queue: all 60 geometry entries are provisionally labeled; 0
  unlabeled entries remain in the current 60-entry slice.
- Structure mapping issues: 0 non-OK entries in the 40-, 50-, and 60-entry
  slices after auth/label residue fallback.

Start commands:

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli calibrate-abstention --retrieval artifacts/v3_geometry_retrieval_60.json --out artifacts/v3_abstention_calibration_60.json
PYTHONPATH=src python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_60.json --out artifacts/v3_hard_negative_controls_60.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-geometry-score-margins --retrieval artifacts/v3_geometry_retrieval_60.json --out artifacts/v3_geometry_score_margins_60.json
```

Next concrete task:

Separate the two remaining 60-slice ligand-supported metal-like hard negatives
(`m_csa:52` class II fructose-bisphosphate aldolase and `m_csa:53` malate
synthase) from real metal-dependent-hydrolase positives without lowering the
retained positive count. Start by comparing
`artifacts/v3_hard_negative_controls_60.json` against retained positives in
`artifacts/v3_geometry_label_eval_60.json`; add one bounded scoring feature or
fingerprint split with unit tests, then regenerate the 60-entry artifacts.

Known blockers:

- Labels are still provisional and small; do not claim validated enzyme
  function.
- Geometry retrieval is still heuristic, not learned.
- Ligand/cofactor evidence uses nearby mmCIF ligand atoms and inferred roles;
  it does not model occupancy, alternate conformers, biological assembly, or
  substrate state.
- The current label queue is empty for the 60-entry slice, so label expansion
  now requires enlarging the geometry slice or adding a new seed fingerprint
  family.
- Full-database scalability has not been measured; `perf-suite` is local
  artifact timing only.
