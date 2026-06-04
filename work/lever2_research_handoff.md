# Lever 2 Research Handoff

## Current Automation Run

- Automation ID: `catalytic-earth-lever-2-research-loop`
- Branch: `lever-2-research-track`
- STARTED_AT_UTC: `2026-06-04T17:36:54Z`
- STARTED_AT_LOCAL: `2026-06-04T12:36:54-0500 CDT`
- Scope: Lever 2 mechanism-representation research only.
- Guardrails: source-free/deployment-valid feature discipline, no heldout tuning,
  no mechanism text, EC/Rhea IDs, labels, source IDs, target names, registry
  edits, ontology edits, import edits, production threshold edits, or heldout
  split edits.

## Run Ledger

### 2026-06-04 Lever 2 Research Run 4

#### Wall-clock ledger

- STARTED_AT: `2026-06-04T17:36:54Z`
- STARTED_LOCAL: `2026-06-04T12:36:54-0500 CDT`
- ENDED_AT: `2026-06-04T17:54:59Z`
- ENDED_LOCAL: `2026-06-04T12:54:59-0500 CDT`
- ELAPSED_MINUTES: `18.08`

#### Intent

Continue Lever 2 mechanism-representation research only. Start from the
rebased dedicated branch and produce a measured train/cal readout first,
preferably reducing the missing current-split mechanism/electron-flow evidence
gap identified in Run 3 before any blocker conclusion.

#### Work log

- Continued in the isolated Lever 2 worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth`.
- Removed one old clean detached Codex worktree outside this branch to restore
  disk above the 10 GiB guardrail before substantive work. The Lever 2 branch
  worktree and main Lever 3 worktree were not touched.
- Rebasing `lever-2-research-track` onto current `origin/main` hit the known
  CLI wiring conflict between Lever 2 and Lever 3 command families; resolved
  by keeping both command families, then continued the rebase successfully.
- Added a reproducible measured Lever 2 readout and CLI:
  `build-lever2-source-free-partial-surface-current-split-portability-readout`.
- Wrote the measured readout artifact and report:
  `artifacts/v3_lever2_source_free_partial_surface_current_split_portability_readout_current702_20260604.json`
  and
  `work/lever2_source_free_partial_surface_current_split_portability_readout_current702_20260604.md`.
- Tried a second reuse route by checking the broader review-only source-free
  locator candidate directory. It adds one current-primary candidate overlap
  (`m_csa:216`) but still zero approved/materialized current primary rows and
  zero current-retained OOS rows.
- Inspected the source-free train/cal projection readout for apparent current
  overlaps. The overlaps are existing scored-row diagnostics and best-axis rows
  already carried by the prior electron-flow/current-extended readouts, not a
  new approved current-split source-free mechanism surface.

#### Measured results

- Current split surface: 34 current calibration-primary rows, 210 current
  extended train/cal OOS candidates, 204 scored OOS rows, 132 retained OOS
  rows, and 72 already-abstained OOS rows at fixed threshold `0.44155`.
- Existing approved source-free partial surface:
  53 projection-candidate rows, 14 event-axis linker rows, 53 approved locator
  sidecar rows, and 53 union rows.
- Approved partial-surface current overlap is zero: 0/34 current primary,
  0/132 current-retained OOS, 0/72 already-abstained OOS, and 0/204 scored OOS.
- Review-only locator candidate diagnostic: 2 M-CSA candidate rows, with 1
  current-primary overlap (`m_csa:216`) and 0 current-retained OOS overlap.
- Classification: research-only reuse-route negative. The result does not make
  Lever 2 deployable and does not make Lever 2 overall negative because prior
  train/cal mechanism/electron-flow signal still exists; it shows the already
  approved partial source-free surface cannot reduce the current-split gap.
- Exact missing evidence now named by the artifact: source-free mechanism rows
  on the current split for 34 current primary rows and 132 current-retained OOS
  rows first; 72 already-abstained OOS rows are lower-priority completion rows.

#### Guardrails

- Worked only on Lever 2 research.
- No labels, registries, ontologies, imports, production thresholds, heldout
  splits, or model weights changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated by the new
  artifact.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, or
  source-feature sidecars were used as predictive signal.
- Entry IDs were used only for split-overlap accounting, not as predictive
  features.
- The new artifact does not materialize source-free rows, apply thresholds,
  promote a channel, or claim deployment closure.

#### Validation

- Focused tests:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py tests/test_cli.py tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_partial_surface_current_split_portability_readout_counts -q`
  passed: `133 passed, 159 subtests passed`.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q` passed:
  `1432 passed, 1 warning, 192 subtests passed in 83.56s`.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests` passed:
  `Ran 1387 tests in 43.122s OK`.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed:
  12 source records, 8 mechanism fingerprints, 15 ontology families, and 702
  curated mechanism labels.
- `PYTHONPATH=src python -m compileall -q src tests` passed.
- `python -m json.tool` passed for the new JSON artifact.
- Docs artifact-reference check to `/tmp` passed with `missing: 0`; tracked
  timestamp churn was restored.
- Repo-wide JSON parse passed: 3542 JSON files parsed.
- `git diff --check` passed.
- Disk guardrail after cleanup and validation: 11.4 GiB available.

#### Commit/push status

Committed and pushed to `origin/lever-2-research-track`; final fetch/sync
verification matched local `HEAD` and `origin/lever-2-research-track`. Exact
final hash is recorded in the automation memory and final response.

#### Exact next action

Do not rerun or retune heldout. Materialize source-free mechanism evidence on
the current split itself: start with the 34 current calibration-primary rows
and the 132 current-retained OOS rows named in
`artifacts/v3_lever2_source_free_partial_surface_current_split_portability_readout_current702_20260604.json`,
then rerun the fixed train/cal mechanism overlap and electron-flow readouts.

### 2026-06-04 Lever 2 Research Run 3

#### Wall-clock ledger

- STARTED_AT: `2026-06-04T16:31:37Z`
- STARTED_LOCAL: `2026-06-04T11:31:37-0500 CDT`
- ENDED_AT: `2026-06-04T17:26:51Z`
- ENDED_LOCAL: `2026-06-04T12:26:51-0500 CDT`
- ELAPSED_MINUTES: `55.2`

#### Intent

Continue Lever 2 mechanism-representation research only. First rebase the
dedicated branch onto current `origin/main`, then produce another measured
train/cal readout if available before any blocker conclusion. Current focus:
test whether the frozen row-specific mechanism residual adds signal on the
newer Lever 3 current train/cal OOS surface beyond the geometry/fold operating
point, without using heldout rows or new predictive labels.

#### Work log

- Started from detached `origin/main` in the automation worktree, found the
  existing `lever-2-research-track` checked out at
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth`, and
  continued in that isolated branch worktree.
- Rebasing `lever-2-research-track` onto current `origin/main` hit a single
  CLI wiring conflict between Lever 2 and Lever 3 commands; resolved by keeping
  both command families. Rebase completed successfully.
- Disk was initially below the 10 GiB guardrail at 9.0 GiB available. Cleared
  cache-only directories, not worktrees or project artifacts, and restored
  available disk to 12 GiB before heavier validation.
- Added a reproducible Lever 2 current-extended OOS overlap readout and CLI:
  `build-lever2-current-extended-oos-mechanism-overlap-readout`.
- Wrote the measured readout artifact and report:
  `artifacts/v3_lever2_current_extended_oos_mechanism_overlap_readout_current702_20260604.json`
  and
  `work/lever2_current_extended_oos_mechanism_overlap_readout_current702_20260604.md`.
- Checked whether the older heldout-oriented source-free locator/coordinate
  candidate artifacts could reduce the new current-split evidence gap. The
  126 candidate coordinate-anchor files have 0 overlap with the 34 current
  primary rows, 0 overlap with the 119 missing current-retained OOS rows, and
  0 overlap with the 64 missing already-abstained OOS rows.
- Refreshed the existing electron-flow split-alignment artifact/report so it
  still reports the old 75-row current-contract overlap, but now also reports
  best-axis overlap against the newer current extended OOS surface:
  `artifacts/v3_lever2_source_free_electron_flow_split_alignment_readout_current702_20260604.json`
  and
  `work/lever2_source_free_electron_flow_split_alignment_readout_current702_20260604.md`.

#### Measured results

- Current extended train/cal OOS surface: 210 candidate rows, 204 scored at
  the fixed `combined_mean_geometry_fold` threshold `0.44155`.
- Frozen full row-specific mechanism residual overlap on that current surface:
  21 scored OOS rows. Current geometry/fold abstains 8/21; the mechanism
  residual at fixed threshold `3.21469422` abstains 18/21; an OR gate abstains
  19/21.
- Incremental overlap signal: 13/21 overlap rows are current-retained OOS, and
  the mechanism residual catches 11/13 of those current-retained rows. The
  overlap union-minus-current abstain-recall delta is `+0.52381`.
- Source-free best-axis carry-forward from the train/cal projection readout:
  electron-flow remains the best single missing axis. Its 4 train/cal new OOS
  catches now overlap 3 current-extended OOS rows, including 2 rows retained
  by the current geometry/fold threshold (`m_csa:221`, `m_csa:256`).
- The older electron-flow split-alignment view still has 0/4 best-axis catches
  on the 75-row current geometry/fold calibration-OOS contract, but the new
  current-extended diagnostic adds the 3/4 and 2 retained-row counts above.
- Primary retention gate remains unmeasurable: valid current calibration-primary
  mechanism overlap is 0/34. Classification remains research-only, not
  deployable and not a negative.
- Exact missing evidence for the current-extended route: source-free
  mechanism fields for 34 current calibration-primary rows and 119
  current-retained OOS rows first; 64 already-abstained OOS rows remain lower
  priority completion rows.

#### Guardrails

- Worked only on Lever 2 research.
- No labels, registries, ontologies, imports, production thresholds, heldout
  splits, or model weights changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated by the new
  artifact.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, or
  source-feature sidecars were used as predictive signal. Accessions are
  carried only as row metadata in missing-evidence tables.
- The new artifact uses fixed train/cal-selected thresholds only and does not
  promote or apply a deployment gate.

#### Validation

- Focused tests:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py tests/test_cli.py tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_current_extended_oos_mechanism_overlap_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_split_alignment_readout_current_counts -q`
  passed: `131 passed, 159 subtests passed`.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q` passed:
  `1426 passed, 1 warning, 191 subtests passed in 83.34s`.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests` passed:
  `Ran 1381 tests in 42.918s OK`.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed:
  12 source records, 8 mechanism fingerprints, 15 ontology families, and 702
  curated mechanism labels.
- `PYTHONPATH=src python -m compileall -q src tests` passed.
- `python -m json.tool` passed for the new JSON artifact.
- Docs artifact-reference check to `/tmp` passed with `missing: 0`; tracked
  timestamp churn was restored.
- Repo-wide JSON parse passed: 3540 JSON files parsed.
- `git diff --check` passed.
- Disk guardrail after cache cleanup: 11 GiB available.

#### Commit/push status

Committed and pushed to `origin/lever-2-research-track`; final fetch/sync
verification matched local `HEAD` and `origin/lever-2-research-track`.

#### Exact next action

Materialize split-aligned source-free mechanism/electron-flow fields for the
34 current calibration-primary rows and the 119 current-retained OOS rows
identified in the new artifact, then rerun
`build-lever2-current-extended-oos-mechanism-overlap-readout` and
`build-lever2-source-free-electron-flow-split-alignment-readout` before any
heldout or deployment claim. Existing heldout-oriented locator candidate
sidecars do not cover these rows.

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
