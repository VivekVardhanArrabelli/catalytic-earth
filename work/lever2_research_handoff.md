# Lever 2 Research Handoff

## Current Automation Run

- Automation ID: `catalytic-earth-lever-2-research-loop`
- Branch: `lever-2-research-track`
- STARTED_AT_UTC: `2026-06-04T15:32:01Z`
- STARTED_AT_LOCAL: `2026-06-04T10:32:01-0500 CDT`
- Scope: Lever 2 mechanism-representation research only.
- Guardrails: source-free/deployment-valid feature discipline, no heldout tuning,
  no mechanism text, EC/Rhea IDs, labels, source IDs, target names, registry
  edits, ontology edits, import edits, production threshold edits, or heldout
  split edits.

## Run Ledger

### 2026-06-04 Lever 2 Research Run 2

#### Wall-clock ledger

- STARTED_AT: `2026-06-04T15:32:01Z`
- STARTED_LOCAL: `2026-06-04T10:32:01-0500 CDT`
- ENDED_AT: `2026-06-04T15:55:00Z`
- ENDED_LOCAL: `2026-06-04T10:55:00-0500 CDT`
- ELAPSED_MINUTES: `23.0`

#### Intent

Continue Lever 2 mechanism-representation research only. Start with measured
train/cal readouts that test whether genuinely new source-free row-specific
mechanism evidence adds operating-point value beyond the current
geometry/fold/top1-style surface; use blocker artifacts only if measured routes
cannot be completed.

#### Work log

- Stayed on the isolated `lever-2-research-track` worktree/branch; it was clean
  and already up to date with `origin/main`.
- Added a reproducible Lever 2 CLI/readout:
  `build-lever2-source-free-electron-flow-split-alignment-readout`.
- Wrote the measured readout artifact and report:
  `artifacts/v3_lever2_source_free_electron_flow_split_alignment_readout_current702_20260604.json`
  and
  `work/lever2_source_free_electron_flow_split_alignment_readout_current702_20260604.md`.
- Added synthetic unit/parser coverage and a current-artifact regression test.
- Tried a second train/cal route using raw full-sidecar electron-transfer
  presence on current geometry/fold overlap rows and included it in the same
  artifact. Also checked the coordinate/source-feature redox route; the
  overlapping rows are source-feature/UniProt-derived draft sidecars, not
  source-free electron-flow predictive evidence, so they were not used.

#### Measured results

- Source-free electron-flow axis ceiling:
  - Current source-free projected subset: 4 fields, primary retain recall
    `1.0`, OOS abstain recall `0.642857`, AUC `0.794643`.
  - Current projection plus electron-flow fields:
    6 fields, primary retain recall `1.0`, OOS abstain recall `0.785714`,
    AUC `0.870536`, threshold `1.72848324`.
  - Delta versus current projected subset: `+0.142857` OOS abstain recall.
  - Full row-specific surface context: 19 fields, OOS abstain recall
    `0.857143`, AUC `0.875`.
- Split-aligned current-surface result:
  - Best single-axis new OOS catches: 4.
  - Best single-axis new OOS catches that overlap current geometry/fold
    calibration-OOS rows: 0/4.
  - Current source-free candidate projection overlap remains 0/34 current
    calibration-primary rows and 0/75 current calibration-OOS rows.
- Raw full-sidecar current-surface overlap diagnostic:
  - Valid current-primary calibration-feature overlap: 0 rows.
  - Current-primary rows excluded as mechanism train targets: 1 row.
  - Current-OOS calibration-feature overlap: 8 rows.
  - Current-retained OOS overlap rows with electron transfer: 1/5.

#### Classification

Research-only signal, not deployable and not a negative. Electron-flow is still
the best single missing source-free axis by train/cal ceiling, but current data
cannot support an integrated operating-point claim because split-aligned
source-free electron-flow evidence is absent on the current geometry/fold
calibration split.

#### Exact missing evidence

- Source-free electron-flow fields (`has_electron_transfer_event` and
  `electron_transfer_count`) for the 40 current-retained calibration-OOS rows
  first.
- Source-free electron-flow fields for the 34 current calibration-primary rows
  needed to measure retention cost.
- Then fill the remaining 27 already-abstained current calibration-OOS rows to
  complete the split-aligned OOS surface.
- Do not use the draft UniProt/source-feature active-site sidecars for this
  Lever 2 predictive readout; they are not source-free electron-flow evidence.

#### Guardrails

- Worked only on Lever 2 research.
- No labels, registries, ontologies, imports, production thresholds, heldout
  splits, or model weights changed.
- No heldout M-CSA rows were trained on, tuned on, rescored, or evaluated by the
  new artifact.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, or
  source-feature sidecars were used as predictive signal.

#### Validation

- Focused tests:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py tests/test_cli.py -q`
  passed: `126 passed, 159 subtests passed`.
- Focused tests with current-artifact regression:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py tests/test_cli.py tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_split_alignment_readout_current_counts -q`
  passed: `127 passed, 159 subtests passed`.
- Final full pytest:
  `PYTHONPATH=src python -m pytest -q` passed:
  `1418 passed, 1 warning, 190 subtests passed in 82.89s`.
- Final unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests` passed:
  `Ran 1373 tests in 42.265s OK`.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed.
- `PYTHONPATH=src python -m compileall -q src tests` passed.
- `PYTHONPATH=src python -m catalytic_earth.cli build-current-docs-artifact-reference-check --out /tmp/lever2_docs_artifact_reference_check.json`
  passed with `missing: 0`; generated docs timestamp/count churn was restored.
- Repo-wide JSON parse passed: `3533` JSON files checked.
- `python -m json.tool` passed for the new JSON artifact.
- `git diff --check` passed.
- Disk guardrail: `df -h .` showed 12 GiB free.

#### Current status

Committed and pushed to `origin/lever-2-research-track`; final sync
verification matched local `HEAD` to `origin/lever-2-research-track`. The exact
final hash is recorded in the automation memory and final response.

#### Exact next action

Materialize a split-aligned source-free electron-flow sidecar for the 40
current-retained OOS rows and 34 current calibration-primary rows, then rerun
`build-lever2-source-free-electron-flow-split-alignment-readout` and the
fixed-threshold Lever 2 incremental readout before any heldout or deployment
claim.

### 2026-06-04 Lever 2 Research Run 1

#### Wall-clock ledger

- STARTED_AT: `2026-06-04T14:30:32Z`
- STARTED_LOCAL: `2026-06-04T09:30:32-0500 CDT`
- ENDED_AT: `2026-06-04T15:20:31Z`
- ENDED_LOCAL: `2026-06-04T10:20:31-0500 CDT`
- ELAPSED_MINUTES: `50.0`

#### Intent

Produce a measured train/cal-disciplined Lever 2 readout that tests whether a
genuinely new source-free row-specific mechanism feature surface adds operating
point value beyond the current geometry/fold/top1-style surface. Prefer a
measured negative over a blocker packet when current data can be evaluated.

#### Work log

- Created the isolated `lever-2-research-track` branch from `origin/main`.
- No prior Lever 2 automation memory was present.
- Added `build-lever2-mechanism-feature-incremental-readout` and a measured
  train/cal overlap artifact comparing the frozen row-specific mechanism
  residual surface against the current geometry/fold operating point.
- Added/regenerated the source-free train/cal projection readout for the
  follow-up row-specific bond-change/event-pair surface, including split
  alignment counts against the current geometry/fold calibration-primary and
  calibration-OOS rows.
- Kept all readouts train/cal-disciplined. No heldout rows were rescored or used
  for training/threshold selection; no labels, EC/Rhea IDs, source IDs, target
  names, or mechanism text were used as feature values.

#### Measured results

- Incremental overlap readout:
  - Artifact:
    `artifacts/v3_lever2_mechanism_feature_incremental_readout_current702_20260604.json`
  - Report:
    `work/lever2_mechanism_feature_incremental_readout_current702_20260604.md`
  - Current geometry/fold operating point:
    `combined_mean_geometry_fold < 0.44155` abstains.
  - Mechanism residual operating point:
    `row_specific_mechanism_out_of_atlas_span_residual > 3.21469422`
    abstains.
  - On the 8 overlapping calibration-OOS rows, current geometry/fold abstained
    3/8, mechanism residual abstained 6/8, and the OR union abstained 7/8.
  - Mechanism residual caught 4/5 current-retained OOS overlap rows.
  - Valid primary overlap is 0/34 because the 4 mechanism calibration primaries
    are current geometry/fold train targets; no integrated operating-point
    retention claim is valid yet.
- Source-free projection readout:
  - Artifact:
    `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_train_cal_projection_readout_current702_20260604.json`
  - Report:
    `work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_train_cal_projection_readout_current702_20260604.md`
  - The current source-free projection covers 4/19 frozen mechanism fields and
    gives residual OOS abstain recall 0.642857 at primary retain recall 1.0 on
    the 43-row mechanism train/cal sidecar.
  - This is +0.242857 versus the fold/geometry calibration-OOS context
    (0.4), but -0.214286 versus the full row-specific mechanism surface
    (0.857143).
  - Best single missing axis by train/cal ceiling is `electron_flow`; adding it
    raises OOS abstain recall to 0.785714 and catches 4 additional mechanism
    sidecar OOS rows.
  - Those 4 additional OOS catches have 0 overlap with the current geometry/fold
    calibration-OOS rows.
  - The current source-free candidate projection overlaps 0/34 current
    geometry/fold calibration-primary rows and 0/75 current geometry/fold
    calibration-OOS rows, so the split-aligned current-surface incremental
    readout is not measurable yet.

#### Classification

Research-only signal, not deployable and not a negative. Lever 2 shows local
OOS signal beyond geometry/fold on available train/cal overlap, but current data
are insufficient for a leakage-clean integrated operating-point claim because
the source-free projection is not split-aligned with the current geometry/fold
calibration rows.

#### Exact missing evidence

- Source-free row-specific mechanism feature sidecar for 34 current
  geometry/fold calibration-primary rows.
- Source-free row-specific mechanism feature sidecar for the 67 current
  geometry/fold calibration-OOS rows not already covered by the mechanism
  sidecar.
- Of those 67 missing calibration-OOS rows, 40 are retained by the current
  geometry/fold operating point and 27 are already abstained. Prioritize the 40
  retained rows first because they are the most direct route to incremental OOS
  value beyond geometry/fold.
- Existing materialized source-free active-site locator files cover 0/34
  missing primary rows and 0/67 missing OOS rows. Existing source-free active
  site planning artifacts only show partial overlap for `m_csa:216` and
  `m_csa:35`; they do not remove the need for split-aligned mechanism sidecar
  materialization.
- Missing frozen feature axes still required for source-free projection
  completeness: bond-change counts, electron-transfer counts, event-topology
  counts, confidence metadata counts, and active-site locator counts listed in
  the projection readout report.

#### Validation

- `PYTHONPATH=src python -m pytest tests/test_northstar_next_levers.py tests/test_lever2_mechanism_incremental_readout.py tests/test_cli.py -q`
  passed: `308 passed, 159 subtests passed`.
- `PYTHONPATH=src python -m pytest -q` passed:
  `1415 passed, 1 warning, 190 subtests passed in 81.33s`.
- `PYTHONPATH=src python -m unittest discover -s tests` passed:
  `Ran 1370 tests in 48.968s OK`.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed.
- `PYTHONPATH=src python -m compileall -q src tests` passed.
- `PYTHONPATH=src python -m catalytic_earth.cli build-current-docs-artifact-reference-check --out /tmp/lever2_docs_artifact_reference_check.json`
  passed with `missing: 0`; generated docs timestamp churn was restored.
- `python -m json.tool` passed for both new JSON artifacts.
- `git diff --check` passed.
- Disk guardrail: `df -h .` showed 12 GiB free.

#### Current status

Pushed to `origin/lever-2-research-track`; local `HEAD` and
`origin/lever-2-research-track` matched during final sync verification, and
`git status` reported a clean branch. The exact final hash is recorded in the
automation memory and final response for this run.

#### Exact next action

Next Lever 2 run should materialize the missing split-aligned source-free
mechanism sidecar rows/fields, starting with the `electron_flow` axis because it
has the best train/cal repair ceiling, before any heldout or deployment claim.
