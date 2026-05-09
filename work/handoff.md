# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.

The central artifact is not a dashboard. It is a mechanism-first knowledge graph,
benchmark suite, and enzyme discovery pipeline that maps protein evidence to
catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval. Geometry artifacts now cover
the 20-entry regression slice plus 30-entry and 40-entry expansion slices.

Curated seed labels live in
`data/registries/curated_mechanism_labels.json`. The registry currently covers
36 of the first 40 geometry entries: 9 in-scope metal-dependent hydrolase seed
positives and 27 out-of-scope controls.

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

Run started: `2026-05-09T16:16:10Z`.

What changed in this run:

- Expanded curated labels to 36 entries in the 40-entry geometry slice.
- Added auto abstention thresholds from observed top1 score boundaries and
  evaluable-aware metrics for retrieval evaluation and threshold selection.
- Added score-margin, hard-negative-control, label-expansion-candidate, and
  structure-mapping-issue analyses with CLI commands and tests.
- Strengthened retrieval scoring with mechanistic coherence for Ser-His-Asp/Glu
  fingerprints and clearer cofactor-evidence levels.
- Added missing-position diagnostics for unresolved catalytic residue mappings.
- Regenerated 20-, 30-, and 40-entry geometry/retrieval/evaluation/calibration
  artifacts plus hard-negative, score-margin, label-candidate, mapping-issue,
  and performance artifacts.
- Updated README, geometry docs, V2 report, performance docs, scope, tests, and
  reproducibility commands.

Current metrics:

- 20-entry regression slice: 20 evaluated labels, 13 evaluable entries, 3
  evaluable in-scope positives, selected zero-false threshold `0.5796`.
- 40-entry expansion slice: 36 evaluated labels, 26 evaluable entries, 7
  evaluable in-scope positives, selected zero-false threshold `0.587`.
- 40-entry top1/top3 in-scope accuracy on evaluable positives: `0.857` / `1.0`.
- 40-entry retained top3 accuracy on evaluable positives at `0.587`: `0.571`.
- 40-entry out-of-scope abstention at `0.587`: `1.0` on evaluable controls,
  with 0 false non-abstentions.
- Hard negatives: 2 role-inferred metal-like out-of-scope controls in the
  40-entry slice overlap the evaluable positive score floor.
- Label expansion queue: 4 unlabeled entries, 0 ready for label review by the
  current readiness checks.
- Structure mapping issues: 14 non-OK entries in the 40-entry slice, including
  10 labeled entries and 2 in-scope positives (`m_csa:15` on `1ZNB`, `m_csa:28`
  on `1DJX`).

Start commands:

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli calibrate-abstention --retrieval artifacts/v3_geometry_retrieval_40.json --out artifacts/v3_abstention_calibration_40.json
PYTHONPATH=src python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_40.json --out artifacts/v3_hard_negative_controls_40.json
PYTHONPATH=src python -m catalytic_earth.cli analyze-structure-mapping-issues --geometry artifacts/v3_geometry_features_40.json --out artifacts/v3_structure_mapping_issues_40.json
```

Next concrete task:

Separate the two 40-slice metal-like hard negatives from real
metal-dependent-hydrolase positives without losing retained positives. Start by
opening `artifacts/v3_hard_negative_controls_40.json` and comparing those rows
against the retained positives in `artifacts/v3_geometry_label_eval_40.json`;
then add one bounded scoring feature or penalty with a unit test and regenerate
the 40-entry artifacts.

Known blockers:

- Labels are still provisional and small; do not claim validated enzyme
  function.
- Geometry retrieval is still heuristic, not learned.
- Ligand/cofactor evidence uses nearby mmCIF ligand atoms and inferred roles;
  it does not model occupancy, alternate conformers, biological assembly, or
  substrate state.
- Four unlabeled 40-slice entries are not ready for review until structure
  mapping or evidence quality improves.
- Non-evaluable positives need alternate structure selection or residue
  numbering/chain repair before they can fairly influence scoring.
