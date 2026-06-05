# Lever 2 Research Handoff

## Current Automation Run

- Automation ID: `catalytic-earth-lever-2-research-loop`
- Branch: `lever-2-research-track`
- STARTED_AT_UTC: `2026-06-04T23:33:05Z`
- STARTED_AT_LOCAL: `2026-06-04T18:33:05-0500 CDT`
- ENDED_AT_UTC: `2026-06-05T00:28:35Z`
- ENDED_AT_LOCAL: `2026-06-04T19:28:35-0500 CDT`
- ELAPSED_MINUTES: `55.50`
- Scope: Lever 2 mechanism-representation research only.
- Guardrails: source-free/deployment-valid feature discipline, no heldout tuning,
  no mechanism text, EC/Rhea IDs, labels, source IDs, target names, registry
  edits, ontology edits, import edits, production threshold edits, or heldout
  split edits.

## Run Ledger

### 2026-06-04 Lever 2 Research Run 10

#### Wall-clock ledger

- STARTED_AT: `2026-06-04T23:33:05Z`
- STARTED_LOCAL: `2026-06-04T18:33:05-0500 CDT`
- ENDED_AT: `2026-06-05T00:28:35Z`
- ENDED_LOCAL: `2026-06-04T19:28:35-0500 CDT`
- ELAPSED_MINUTES: `55.50`

#### Intent

Continue Lever 2 mechanism-representation research only. Use the dedicated
`lever-2-research-track` branch, start from current `origin/main`, and test
whether the primary-controlled event-axis rescue signal survives an explicit
null control rather than only another neighboring-signature exclusion.

#### Work log

- Started in detached automation worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/aa98/catalytic-earth`; found
  the existing dedicated Lever 2 branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` and
  continued there for all branch work.
- Fetched `origin` and rebased `lever-2-research-track` onto current
  `origin/main` `bd0a57f6ccefbfcb7e90a7ebf63eb8f3bcddb80c`.
  Resolved the expected `src/catalytic_earth/cli.py` conflict by preserving
  both the latest Lever 3 command family and the Lever 2 mechanism command
  family.
- Added a deterministic primary-controlled event-axis null-control readout:
  `build-lever2-event-axis-primary-controlled-null-readout`. It regenerates
  the observed primary-controlled rescue result, then applies deterministic
  SHA256 permutations to non-baseline added-axis feature fields while keeping
  the fixed geometry/fold surface, target rows, baseline projected subset,
  primary-control filtering, and leave-target-out selection discipline.
- Added a narrower priority-event-axis null summary inside the same readout for
  `bond_change`, `electron_flow`, `event_topology`, and
  `all_priority_event_axes`, so the negative is not dependent only on locator
  or confidence-metadata axes in the broader frontier.
- Generated two measured readout artifacts/reports:
  `artifacts/v3_lever2_event_axis_primary_controlled_null_readout_current702_20260604.json`,
  `work/lever2_event_axis_primary_controlled_null_readout_current702_20260604.md`,
  `artifacts/v3_lever2_event_axis_primary_controlled_null_altseed_readout_current702_20260604.json`,
  and
  `work/lever2_event_axis_primary_controlled_null_altseed_readout_current702_20260604.md`.
- Added parser, synthetic unit, generated-artifact regression, and alternate
  null-seed regression coverage.

#### Measured results

- Default null seed result:
  `research_only_null_controlled_marginal_signal_not_distinguishable_from_null`.
  Observed primary-controlled rescue remains
  `source_free_projected_proton_role_subset+bond_change`, catching 7/13
  current-retained overlap rows with 2 marginal catches beyond the projected
  subset: `m_csa:256` and `m_csa:312`.
- The deterministic null distribution over 128 permutations and 6 searched
  added axes has max-marginal min/median/p90/p95/max = 0/4/6/6/8. 123/128
  permutations meet or exceed the observed 2 marginal catches; empirical
  p-value is `0.96124`.
- The narrower priority-event-axis null also rejects the signal: priority-null
  p95 is 6, max is 7, and 108/128 permutations meet or exceed the observed 2
  marginal catches.
- Alternate null seed stability readout agrees. Full null p95 is 7, max is 8,
  and 127/128 permutations meet or exceed the observed 2 marginal catches
  (`p=0.992248`). Priority-event null p95 is 5, max is 7, and 114/128
  permutations meet or exceed the observed signal.
- Temporary higher-permutation probes also agree and were kept in `/tmp`
  rather than committed because they did not change the decision. A 256-null
  probe had full-null p95/max = 6/7 with 250/256 permutations at or above the
  observed signal (`p=0.976654`); its priority-event null p95/max = 6/7 with
  229/256 at or above observed. A 512-null probe had full-null p95/max = 6/8
  with 495/512 permutations at or above observed (`p=0.966862`); its
  priority-event null p95/max = 6/8 with 450/512 at or above observed.
- Classification: measured research-only negative for the current
  primary-controlled event-axis rescue. The prior local marginal signal is not
  distinguishable from deterministic added-axis assignment nulls under the same
  split and primary-control discipline.
- Deployability: not deployable. The readouts do not add operating-point value
  beyond current geometry/fold, do not promote Lever 2, and still inherit the
  source-free current-split evidence gap for 34 current primary rows and 132
  current-retained OOS rows.

#### Guardrails

- Worked only on Lever 2 research.
- No labels, registries, ontologies, imports, production thresholds, heldout
  splits, model weights, deployment gates, or heldout rows changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, accessions,
  or source provenance were used as predictive features.
- Entry IDs were used only for split/overlap accounting, row diagnostics,
  deterministic null assignment bookkeeping, and missing-evidence accounting.
- M-CSA row-specific mechanism features remain train/cal-only research
  evidence; no source-free rows were materialized or promoted.

#### Validation

- Generated default null readout:
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-event-axis-primary-controlled-null-readout`.
- Generated alternate-seed null readout:
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-event-axis-primary-controlled-null-readout --null-seed lever2_primary_controlled_event_axis_null_altseed_v0 --artifact-id v3_lever2_event_axis_primary_controlled_null_altseed_readout_current702_20260604 --out artifacts/v3_lever2_event_axis_primary_controlled_null_altseed_readout_current702_20260604.json --report work/lever2_event_axis_primary_controlled_null_altseed_readout_current702_20260604.md`.
- Focused parser/unit/artifact tests passed: `4 passed`.
- Broader Lever 2/CLI/regression slice passed: `164 passed, 159 subtests`.
- Full pytest passed on the final tree:
  `1483 passed, 1 warning, 203 subtests passed`; rerun later in the block also
  passed: `1483 passed, 1 warning, 203 subtests passed in 84.55s`. The warning
  is the existing sklearn/SciPy L-BFGS-B deprecation warning.
- Full unittest discovery passed on the final tree:
  `Ran 1438 tests in 42.613s OK`; rerun later in the block also passed:
  `Ran 1438 tests in 43.969s OK`, with the same existing warning.
- Focused Lever 2/CLI/artifact regression rerun passed:
  `416 passed, 184 subtests passed in 26.77s`.
- Full geometry artifact regression file passed: `263 passed, 25 subtests`.
- `python -m py_compile src/catalytic_earth/lever2_mechanism_incremental_readout.py src/catalytic_earth/cli.py` passed.
- `PYTHONPATH=src python -m compileall -q src tests` passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed:
  12 source records, 8 mechanism fingerprints, 15 ontology families, and 702
  curated labels; rerun later in the block passed with the same counts.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`
  passed: `2 passed`.
- Repo JSON/JSONL parse sweep passed: 3564 JSON files and 27 JSONL files
  parsed with 0 errors.
- New artifact `source_artifacts` hashes checked: 10 checked across the 2 new
  Lever 2 null readouts, 0 stale.
- Default null readout regeneration matched committed JSON and Markdown after
  normalizing `created_utc`.
- Default and alternate-seed null readouts both regenerated into `/tmp` and
  matched the committed JSON/Markdown after normalizing `created_utc`.
- Temporary 256-null and 512-null stability probes completed and both remained
  null-controlled negatives.
- CLI help smoke for
  `build-lever2-event-axis-primary-controlled-null-readout --help` passed.
- Guardrail assertions passed across both new null artifacts: no heldout
  scoring/tuning, no mechanism text/source IDs as predictive features, no
  EC/Rhea/label/source/target fields as predictive features, not deployable,
  not promoted, and no operating-point value claim.
- `git diff --check` passed. Disk remained above the 10 GiB guardrail
  (about 13 GiB free during validation).

#### Commit/push status

- Implementation/readout commit
  `9af1748bc587c2c462c1d36a9df374adf5a39f35` was pushed to
  `origin/lever-2-research-track` with `--force-with-lease` after rebasing the
  dedicated branch onto current `origin/main`.
- Verified after `git fetch origin lever-2-research-track` that local `HEAD`
  matched `origin/lever-2-research-track` at
  `9af1748bc587c2c462c1d36a9df374adf5a39f35`.
- This final handoff verification update is committed and pushed as the
  follow-up bookkeeping commit; the exact final branch hash is recorded in
  automation memory and the final response.

#### Exact next action

Do not promote Lever 2 event-axis/bond-change from the current rescue result.
If source-free current-split event-axis rows are materialized, rerun the
primary-controlled frontier plus this null-control readout and require observed
marginal catches above the empirical null p95 before any heldout or deployment
claim.

### 2026-06-04 Lever 2 Research Run 9

#### Wall-clock ledger

- STARTED_AT: `2026-06-04T22:35:43Z`
- STARTED_LOCAL: `2026-06-04T17:35:43-0500 CDT`
- ENDED_AT: `2026-06-04T23:25:49Z`
- ENDED_LOCAL: `2026-06-04T18:25:49-0500 CDT`
- ELAPSED_MINUTES: `50.11`

#### Intent

Continue Lever 2 mechanism-representation research only on the dedicated
`lever-2-research-track` branch. Start from current `origin/main`, avoid
repeating the settled embedding/current-surface negative, and produce another
measured train/cal readout before any blocker conclusion.

#### Work log

- Started in detached automation worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/cca7/catalytic-earth`; found
  the existing dedicated Lever 2 branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` and
  continued there for all branch work.
- Initial filesystem free space was below the 10 GiB guardrail at 6.3 GiB.
  Removed the clean detached stale automation worktrees
  `/Users/vivekvardhanarrabelli/.codex/worktrees/7695/catalytic-earth` and
  `/Users/vivekvardhanarrabelli/.codex/worktrees/b316/catalytic-earth`,
  restoring free space to 13 GiB before substantive work.
- Fetched `origin` and rebased `lever-2-research-track` onto current
  `origin/main`. Resolved the expected `src/catalytic_earth/cli.py` conflict
  by keeping the newer Lever 3 post-bandpass commands and the Lever 2
  mechanism command family.
- Added a measured Lever 2 signature-excluded event-axis frontier builder/CLI:
  `build-lever2-event-axis-signature-excluded-frontier-readout`. For each
  current-overlap OOS target it selects train/cal event-axis rules after
  excluding the target row and calibration OOS rows sharing the configured
  mechanism-axis signature; mechanism calibration primaries remain the
  retention controls.
- Added a sensitivity builder/CLI:
  `build-lever2-event-axis-signature-exclusion-sensitivity-readout`, covering
  projected-subset, bond-change, electron-flow, and event-topology signature
  exclusions.
- Wrote the measured readout artifacts and reports:
  `artifacts/v3_lever2_event_axis_signature_excluded_frontier_readout_current702_20260604.json`,
  `work/lever2_event_axis_signature_excluded_frontier_readout_current702_20260604.md`,
  `artifacts/v3_lever2_event_axis_bond_signature_excluded_frontier_readout_current702_20260604.json`,
  `work/lever2_event_axis_bond_signature_excluded_frontier_readout_current702_20260604.md`,
  `artifacts/v3_lever2_event_axis_signature_exclusion_sensitivity_readout_current702_20260604.json`,
  and
  `work/lever2_event_axis_signature_exclusion_sensitivity_readout_current702_20260604.md`.
- Added regression and unit coverage for signature-neighbor exclusion,
  artifact counts, parser defaults, generic signature-exclusion guardrails,
  and empty sensitivity-axis input validation.

#### Measured results

- Projected-signature exclusion result:
  `research_only_signature_excluded_marginal_axis_signal_source_free_gap`.
  Baseline projected subset catches 5/13 current-retained overlap rows; the
  best pair `source_free_projected_proton_role_subset+bond_change` catches
  7/13 and adds 2 marginal current-retained OOS catches: `m_csa:256` and
  `m_csa:312`.
- The projected-signature best pair excludes 60 same-signature calibration OOS
  rows across 18 target rows, and all 21/21 target-selected rules pass the
  mechanism primary-control retention gate.
- Bond-signature exclusion is stricter for the bond-change path. Under
  `signature_axis_id=bond_change`, the best pair becomes
  `source_free_projected_proton_role_subset+electron_flow`, catching 6/13 with
  1 marginal row: `m_csa:256`. The bond-change pair itself falls to 0
  marginal catches under its own signature exclusion.
- Sensitivity matrix result:
  `research_only_signature_exclusion_sensitivity_signal_with_axis_caveat`.
  All 4 evaluated signature axes have some marginal signal, but the
  bond-change signal is axis-fragile: it survives projected-signature
  exclusion, collapses under bond-signature exclusion, and leaves one
  electron-flow marginal catch for `m_csa:256`.
- Result class is research-only, not deployable. It does not yet add
  source-free operating-point value beyond the current geometry/fold surface
  because current-split event-axis rows are still missing for 34 current
  primary rows and 132 current-retained OOS rows.

#### Guardrails

- Worked only on Lever 2 research.
- No labels, registries, ontologies, imports, production thresholds, heldout
  splits, model weights, deployment gates, or heldout rows changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, accession
  fields, or source provenance were used as predictive features.
- Entry IDs were used only for split/overlap accounting, row-level diagnostics,
  same-signature exclusion accounting, and missing-row queue accounting.
- M-CSA row-specific mechanism features remain train/cal-only research
  evidence; no source-free rows were materialized or promoted.
- Disk guardrail was restored before substantive work and remained above
  10 GiB available; final checked free space was 15 GiB.

#### Validation

- Generated artifacts:
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-event-axis-signature-excluded-frontier-readout`;
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-event-axis-signature-excluded-frontier-readout --signature-axis-id bond_change --artifact-id v3_lever2_event_axis_bond_signature_excluded_frontier_readout_current702_20260604 --out artifacts/v3_lever2_event_axis_bond_signature_excluded_frontier_readout_current702_20260604.json --report work/lever2_event_axis_bond_signature_excluded_frontier_readout_current702_20260604.md`;
  and
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-event-axis-signature-exclusion-sensitivity-readout`.
- Focused final guardrail test:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_event_axis_signature_excluded_frontier_removes_same_signature_oos -q`
  passed: `1 passed`.
- Touched Lever 2/CLI/regression cluster:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py tests/test_cli.py tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_signature_excluded_frontier_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_bond_signature_excluded_frontier_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_signature_exclusion_sensitivity_readout_counts -q`
  passed: `153 passed, 159 subtests passed`.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q` passed:
  `1474 passed, 1 warning, 201 subtests passed in 80.93s`. The warning is the
  existing sklearn/SciPy L-BFGS-B deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests` passed:
  `Ran 1429 tests in 43.025s OK`, with the same existing warning.
- `PYTHONPATH=src python -m compileall -q src tests` passed.
- `git diff --check` passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed:
  12 source records, 8 mechanism fingerprints, 15 ontology families, and 702
  curated mechanism labels.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`
  passed: `2 passed`.
- Repo JSON/JSONL parse sweep passed: 3560 JSON files and 27 JSONL files
  parsed with 0 errors.
- New artifact `source_artifacts` hashes checked: 15 checked across 3 new
  Lever 2 readouts, 0 stale.
- Regenerated the 3 new readouts and markdown reports into a temporary
  directory and confirmed they match the committed files after normalizing
  `created_utc`.
- Artifact leakage/guardrail assertions passed across the 3 new artifacts:
  research-only, no deploy/apply, no heldout use, no production changes, and
  no EC/Rhea-style identifiers in the 6 new artifact/report files.

#### Commit/push status

- Implementation/readout commit
  `077e10fd82902c27e54c4facb834af4aace5a48c` was pushed to
  `origin/lever-2-research-track` with `--force-with-lease` after rebasing the
  dedicated branch onto current `origin/main`.
- Verified after `git fetch origin lever-2-research-track` that local `HEAD`
  matched `origin/lever-2-research-track` at
  `077e10fd82902c27e54c4facb834af4aace5a48c`.
- This final handoff verification update is committed and pushed as the
  follow-up bookkeeping commit; the exact final branch hash is recorded in
  automation memory and the final response.

#### Exact next action

- Do not promote Lever 2 yet. Materialize source-free current-split event-axis
  rows for current primary controls and signature-excluded marginal rows, then
  rerun the signature-excluded frontier before any heldout or deployment claim.
- Prioritize `m_csa:256` first because it remains marginal under the stricter
  bond-signature exclusion through electron-flow. Treat `m_csa:312` as a
  secondary smoke row only if the projected-signature bond-change path remains
  primary-controlled after source-free materialization.

### 2026-06-04 Lever 2 Research Run 8

#### Wall-clock ledger

- STARTED_AT: `2026-06-04T21:32:02Z`
- STARTED_LOCAL: `2026-06-04T16:32:02-0500 CDT`
- ENDED_AT: `2026-06-04T22:05:19Z`
- ENDED_LOCAL: `2026-06-04T17:05:19-0500 CDT`
- ELAPSED_MINUTES: `33.28`

#### Intent

Continue Lever 2 mechanism-representation research only on the dedicated
`lever-2-research-track` branch. Rebase onto current `origin/main`, then
produce another measured train/cal readout before any blocker conclusion.

#### Work log

- Started in detached automation worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/d8db/catalytic-earth`; found
  the existing dedicated Lever 2 branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` and
  continued there for all branch work.
- Initial filesystem free space was below the 10 GiB guardrail at 7.1 GiB.
  Removed the clean, detached, stale automation worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/53b8/catalytic-earth`,
  restoring free space to 11 GiB before running tests or writing new artifacts.
- Fetched `origin main` and `origin/lever-2-research-track`; rebased
  `lever-2-research-track` onto current `origin/main`
  (`7a0c90041d55d795fe33e2973c76b7ed806672c1`). Resolved the expected
  `src/catalytic_earth/cli.py` command-dispatch conflict by keeping both the
  newer Lever 3 cofactor-context command and the prior Lever 2 mechanism
  command. `python -m py_compile src/catalytic_earth/cli.py` passed after the
  conflict fix, and the rebase completed.
- Added a measured Lever 2 primary-controlled event-axis rescue builder/CLI:
  `build-lever2-event-axis-primary-controlled-rescue-readout`.
- Wrote the measured readout artifact and report:
  `artifacts/v3_lever2_event_axis_primary_controlled_rescue_readout_current702_20260604.json`
  and
  `work/lever2_event_axis_primary_controlled_rescue_readout_current702_20260604.md`.
- The readout keeps the current geometry/fold operating point fixed, excludes
  each measured OOS target row from its own mechanism-axis rule selection, and
  filters event-axis rules against all mechanism calibration primary controls.
  It reads no heldout rows, changes no production threshold, and uses entry IDs
  only for split/overlap/missing-evidence accounting.
- Continued after the measured signal by embedding a source-free coverage
  diagnostic for the exact 40-row primary-controlled smoke tranche. Existing
  partial source-free surfaces cover only 1/40 tranche rows, and existing
  event-axis linkers cover 0/40.

#### Measured results

- Primary-controlled rescue result:
  `research_only_primary_controlled_marginal_axis_signal_source_free_gap`.
- Best primary-controlled axis:
  `source_free_projected_proton_role_subset+bond_change`.
- Baseline projected subset catches 5/13 current-retained overlap rows.
  The primary-controlled bond-change pair catches 7/13, adding 2 marginal
  current-retained OOS catches: `m_csa:256` and `m_csa:312`.
- The rescued bond-change rule uses a stricter added-axis rule
  `bond_change low 0.0` for the marginal rows and retains all 4 mechanism
  primary controls: `m_csa:6`, `m_csa:133`, `m_csa:147`, and `m_csa:186`.
  This directly resolves the prior permissive `low 3.0` control failure for
  `m_csa:133` at the train/cal research readout level.
- Target selections passing primary control: 21/21 current-overlap rows.
- The result is still research-only, not deployable: current-split
  source-free event-axis rows are still missing for 34 current primary rows and
  132 current-retained OOS rows, and the M-CSA row-specific mechanism features
  remain train/cal-only research evidence.
- Exact smallest next smoke tranche from this rescue readout is 40 unique rows:
  34 current primary rows, 4 mechanism primary-control rows, and the 2
  primary-controlled marginal OOS rows. Existing partial source-free coverage
  covers only `m_csa:216`; 39/40 tranche rows remain missing, with 0 event-axis
  linker coverage.

#### Guardrails

- Worked only on Lever 2 research.
- No labels, registries, ontologies, imports, production thresholds, heldout
  splits, model weights, deployment gates, or heldout rows changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, accession
  fields, or source provenance were used as predictive features.
- Entry IDs were used only for split/overlap accounting, row-level diagnostics,
  and missing-row queue accounting.
- M-CSA row-specific mechanism features remain train/cal-only research
  evidence; no source-free rows were materialized or promoted.
- Disk guardrail was restored before substantive work and ended above 10 GiB
  available (`10.281` GiB exact check before handoff write).

#### Validation

- Rebase conflict sanity:
  `python -m py_compile src/catalytic_earth/cli.py` passed.
- Generated artifact:
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-event-axis-primary-controlled-rescue-readout`.
- Focused new-readout tests:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_event_axis_primary_controlled_rescue_recovers_bond_signal tests/test_cli.py::CliTests::test_lever2_event_axis_primary_controlled_rescue_parser_defaults tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_primary_controlled_rescue_readout_counts -q`
  passed: `3 passed`.
- Broader touched Lever 2/CLI/regression cluster:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py tests/test_cli.py tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_current_extended_oos_mechanism_overlap_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_current_extended_frontier_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_loo_current_extended_frontier_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_primary_safe_frontier_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_primary_controlled_rescue_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_partial_surface_current_split_portability_readout_counts -q`
  passed: `150 passed, 159 subtests passed`.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q` passed:
  `1457 passed, 1 warning, 195 subtests passed in 80.02s`. The warning is the
  existing sklearn/SciPy L-BFGS-B deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests` passed:
  `Ran 1412 tests in 42.492s OK`, with the same existing warning.
- `PYTHONPATH=src python -m compileall -q src tests` passed.
- `git diff --check` passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed:
  12 source records, 8 mechanism fingerprints, 15 ontology families, and 702
  curated mechanism labels.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`
  passed: `2 passed`.
- Repo JSON/JSONL parse sweep passed: 3551 JSON files and 27 JSONL files
  parsed with 0 errors.
- New artifact `source_artifacts` hashes checked: 5 checked, 0 stale.

#### Commit/push status

- Implementation/readout commit
  `492a48638804414639e89d0830fe01f8a76bc772` was pushed to
  `origin/lever-2-research-track` with `--force-with-lease` after rebasing the
  dedicated branch onto current `origin/main`.
- Verified after `git fetch origin lever-2-research-track` that local `HEAD`
  matched `origin/lever-2-research-track` at
  `492a48638804414639e89d0830fe01f8a76bc772`.
- This final handoff status update is committed and pushed as the follow-up
  bookkeeping commit; the exact final branch hash is recorded in automation
  memory and the final response.

#### Exact next action

- Do not promote Lever 2 yet. Materialize source-free current-split event-axis
  rows for the 40-row primary-controlled rescue smoke tranche: 34 current
  primary rows, mechanism primary controls `m_csa:6`, `m_csa:133`,
  `m_csa:147`, `m_csa:186`, and marginal OOS rows `m_csa:256` and
  `m_csa:312`. Rerun the primary-controlled rescue readout and require the
  `bond_change low 0.0` rescue to preserve all primary controls with nonzero
  marginal current-retained OOS value before any heldout or deployment claim.

### 2026-06-04 Lever 2 Research Run 7

#### Wall-clock ledger

- STARTED_AT: `2026-06-04T20:32:00Z`
- STARTED_LOCAL: `2026-06-04T15:32:00-0500 CDT`
- ENDED_AT: `2026-06-04T21:27:51Z`
- ENDED_LOCAL: `2026-06-04T16:27:51-0500 CDT`
- ELAPSED_MINUTES: `55.85`

#### Intent

Continue Lever 2 mechanism-representation research only. Start from the
dedicated `lever-2-research-track` branch/worktree, rebase it onto current
`origin/main`, and produce a measured train/cal readout before any blocker
conclusion.

#### Work log

- Started in detached automation worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/53b8/catalytic-earth`; found
  the existing dedicated Lever 2 branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` and
  continued there for all branch work.
- Initial branch worktree was clean. Fetched `origin main`; `origin/main` was
  at `9ae48be57c2870c837740d73c01b168e91719ec4`.
- Rebased `lever-2-research-track` onto current `origin/main`. Resolved the
  expected `src/catalytic_earth/cli.py` command-dispatch conflict by keeping
  both the newer Lever 3 residual-safety command and the prior Lever 2
  mechanism-readout command. `python -m py_compile src/catalytic_earth/cli.py`
  passed after the conflict fix, and the rebase completed.
- Added a measured Lever 2 primary-safe event-axis frontier builder/CLI:
  `build-lever2-event-axis-primary-safe-frontier-readout`.
- Wrote the measured readout artifact and report:
  `artifacts/v3_lever2_event_axis_primary_safe_frontier_readout_current702_20260604.json`
  and
  `work/lever2_event_axis_primary_safe_frontier_readout_current702_20260604.md`.
- The readout jointly selects projected-subset-plus-added-axis OR rules on
  mechanism calibration rows while excluding each measured target row from its
  own rule selection. It then asks whether any genuinely new event axis adds
  marginal current-retained OOS catches beyond the projected subset while also
  passing leave-one-primary-out control.
- Continued after the strict primary-safe negative by adding a measured
  primary-retention floor sensitivity table to the same artifact. This checks
  1.0, 0.9, and 0.75 primary-retain floors without reading heldout rows or
  changing any production threshold.
- Added row-level control diagnostics for the failing primary-control row so
  the artifact names the selected rule and feature scores for the row that
  blocks promotion.

#### Measured results

- Strict primary-safe frontier: no projected-subset-plus-added-axis surface
  passes primary LOO control while adding marginal current-retained OOS value.
  Classification:
  `research_only_primary_safe_marginal_axis_negative`.
- Best marginal axis before primary control remains
  `source_free_projected_proton_role_subset+bond_change`: it catches 7/13
  current-retained overlap rows, with 2 marginal rows beyond the projected
  subset (`m_csa:256`, `m_csa:312`).
- The best marginal axis fails the primary LOO control, retaining 3/4
  mechanism primaries and abstaining `m_csa:133`.
- Detailed primary-control diagnostic for `m_csa:133`: baseline-axis score
  3.0, added-axis score 3.0, selected baseline rule `high 3.0`, selected
  added-axis rule `low 3.0`. This makes the current bond-change marginal path
  research-only until a source-free surface can distinguish that known
  in-atlas primary control from the marginal OOS rows.
- Primary-retention floor sensitivity:
  - At 1.0 and 0.9, primary-safe marginal catches remain 0 and no
    projected-subset-plus-axis surface passes primary control.
  - At 0.75, 2 surfaces pass primary control; the best primary-safe surface is
    `source_free_projected_proton_role_subset+electron_flow`, with 1 marginal
    current-retained OOS catch (`m_csa:256`). This confirms the signal only
    survives below the 90% primary-retention standard.
- Current split evidence gap remains unchanged: 34 current primary
  retention-gate rows and 132 current-retained OOS rows still require
  source-free current-split event-axis rows. Best marginal axis fields require
  5 new non-projected fields beyond the 4 projected source-free-compatible
  fields.
- Result: research-only negative for promotion. A genuinely new mechanism axis
  has local marginal train/cal signal before primary control, but no
  primary-safe train/cal operating-point value beyond the current
  geometry/fold surface can be claimed.

#### Guardrails

- Worked only on Lever 2 research.
- No labels, registries, ontologies, imports, production thresholds, heldout
  splits, model weights, deployment gates, or heldout rows changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, accession
  fields, or source provenance were used as predictive features.
- Entry IDs were used only for split/overlap accounting, row-level diagnostics,
  and missing-row queue accounting.
- M-CSA row-specific mechanism features remain train/cal-only research
  evidence; no source-free rows were materialized or promoted.

#### Validation

- Rebase conflict sanity:
  `python -m py_compile src/catalytic_earth/cli.py` passed.
- Initial focused primary-safe tests:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_event_axis_primary_safe_frontier_reports_controlled_signal tests/test_cli.py::CliTests::test_lever2_event_axis_primary_safe_frontier_parser_defaults -q`
  passed: `2 passed`.
- Focused primary-safe artifact regression after sensitivity/control-detail
  refresh:
  `PYTHONPATH=src python -m pytest tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_primary_safe_frontier_readout_counts tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_event_axis_primary_safe_frontier_reports_controlled_signal -q`
  passed: `2 passed`.
- Broader touched Lever 2/CLI/regression cluster after the final control
  diagnostic:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py tests/test_cli.py tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_current_extended_oos_mechanism_overlap_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_current_extended_frontier_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_loo_current_extended_frontier_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_primary_safe_frontier_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_partial_surface_current_split_portability_readout_counts -q`
  passed: `146 passed, 159 subtests passed`.
- Final full pytest after the final control-diagnostic artifact refresh:
  `PYTHONPATH=src python -m pytest -q` passed:
  `1451 passed, 1 warning, 194 subtests passed in 81.26s`. The warning is the
  existing sklearn/SciPy L-BFGS-B deprecation warning.
- Final unittest discovery after the final artifact refresh:
  `PYTHONPATH=src python -m unittest discover -s tests` passed:
  `Ran 1406 tests in 44.766s OK`, with the same existing warning.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed:
  12 source records, 8 mechanism fingerprints, 15 ontology families, and 702
  curated mechanism labels.
- `PYTHONPATH=src python -m compileall -q src tests` passed.
- `git diff --check` passed.
- Repo-wide artifact JSON parse passed: 3545 JSON files parsed with 0 errors.
- New artifact `source_artifacts` hashes checked: 5 checked, 0 stale.
- Current-docs artifact-reference check to `/tmp` passed with `missing: 0`.
- Disk guardrail remained just above 10 GiB available.

#### Commit/push status

- Implementation/readout commit
  `95a11b499e4666d1ce1af67f3ab896ca8374cb2f` was pushed to
  `origin/lever-2-research-track` with `--force-with-lease` after rebasing the
  dedicated branch onto current `origin/main`.
- Verified after `git fetch origin lever-2-research-track` that local `HEAD`
  matched `origin/lever-2-research-track` at
  `95a11b499e4666d1ce1af67f3ab896ca8374cb2f`.
- This final handoff status update is committed and pushed as the follow-up
  bookkeeping commit; the exact final branch hash is recorded in automation
  memory and the final response.

#### Exact next action

Do not promote Lever 2 bond-change/event-axis surfaces yet. The smallest next
Lever 2 experiment is to materialize source-free current-split event-axis rows
for the 34 current primary retention-gate rows plus marginal OOS rows
`m_csa:256` and `m_csa:312`, with `m_csa:133` included as an explicit
primary-control check. Rerun the primary-safe frontier and require marginal
OOS value at the 0.9/1.0 primary-retention floor before any heldout or
deployment claim.

### 2026-06-04 Lever 2 Research Run 6

#### Wall-clock ledger

- STARTED_AT: `2026-06-04T19:32:33Z`
- STARTED_LOCAL: `2026-06-04T14:32:33-0500 CDT`
- ENDED_AT: `2026-06-04T20:01:56Z`
- ENDED_LOCAL: `2026-06-04T15:01:56-0500 CDT`
- ELAPSED_MINUTES: `29.38`

#### Intent

Continue Lever 2 mechanism-representation research only. Use the existing
dedicated `lever-2-research-track` branch/worktree, confirm it is current with
`origin/main`, and produce a measured train/cal readout before any blocker
conclusion.

#### Work log

- Started in detached automation worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/7695/catalytic-earth`; found
  the existing dedicated Lever 2 branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` and
  continued there for all branch work.
- Fetched `origin`. `lever-2-research-track` was clean, already contained
  current `origin/main`, and `git rebase origin/main` reported the branch was
  up to date.
- Added a measured Lever 2 leave-one-out event-axis frontier builder/CLI:
  `build-lever2-event-axis-loo-current-extended-frontier-readout`.
- Wrote the measured readout artifact and report:
  `artifacts/v3_lever2_event_axis_loo_current_extended_frontier_readout_current702_20260604.json`
  and
  `work/lever2_event_axis_loo_current_extended_frontier_readout_current702_20260604.md`.
- The readout selects simple event-axis rules on mechanism calibration rows
  while excluding each measured current-overlap OOS target from its own rule
  selection. It then measures the current extended train/cal OOS overlap under
  the fixed geometry/fold surface.
- Added projected-subset-plus-axis marginal analysis, existing source-free
  partial-surface reuse checks for caught rows, and a leave-one-primary-out
  control for each projected-subset-plus-axis rule.
- Continued after the artifact by comparing the LOO result against the prior
  full-calibration event-axis frontier and by checking whether the two marginal
  rows have any reusable approved source-free partial-surface rows.

#### Measured results

- Current overlap remeasured under target-row exclusion: 21 current extended
  train/cal OOS rows with row-specific M-CSA train/cal mechanism features; 13
  are retained by the fixed current geometry/fold surface and 8 are already
  abstained.
- Baseline projected subset
  `source_free_projected_proton_role_subset` catches 5/13 current-retained
  overlap rows under leave-one-out selection and raises OR abstentions to
  13/21 overlap rows.
- Best projected-subset-plus-axis frontier is
  `source_free_projected_proton_role_subset+bond_change`; it catches 7/13
  current-retained overlap rows and raises OR abstentions to 15/21.
- Marginal catches beyond the projected subset are 2 rows:
  `m_csa:256` and `m_csa:312`.
- The best pair needs 5 new bond-change fields beyond the 4 projected
  source-free-compatible fields. Existing approved source-free partial-surface
  reuse covers 0/7 best-pair caught rows and 0/2 marginal rows.
- Primary-control caveat: no projected-subset-plus-axis surface passes the
  stricter 0.9 primary leave-one-out control. The best pair retains only 3/4
  mechanism primaries under leave-one-primary-out control, abstaining
  `m_csa:133`.
- Classification:
  `research_only_loo_marginal_axis_signal_primary_control_caveat`. This is a
  real local train/cal mechanism-axis signal beyond the projected subset and
  current geometry/fold surface, but it is not deployable and does not clear an
  integrated operating-point gate.
- Exact missing evidence remains: 34 current primary retention-gate rows and
  132 current-retained OOS rows require source-free current-split event-axis
  rows. The smallest smoke tranche is 36 rows (34 current primaries plus the 2
  marginal OOS rows); the best-pair verification tranche is 41 rows (34
  current primaries plus all 7 best-pair caught OOS rows).

#### Guardrails

- Worked only on Lever 2 research.
- No labels, registries, ontologies, imports, production thresholds, heldout
  splits, model weights, or deployment gates changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, or heldout
  split information were used as predictive features.
- Entry IDs were used only for split/overlap accounting and missing-row queue
  accounting.
- M-CSA row-specific mechanism features remain train/cal-only research
  evidence; no source-free rows were materialized or promoted.

#### Validation

- Focused new-readout tests:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_event_axis_loo_frontier_finds_marginal_axis_signal tests/test_cli.py::CliTests::test_lever2_event_axis_loo_current_extended_frontier_parser_defaults tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_loo_current_extended_frontier_readout_counts -q`
  passed: `3 passed`.
- Broader Lever 2/CLI regression cluster:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py tests/test_cli.py tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_current_extended_oos_mechanism_overlap_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_current_extended_frontier_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_loo_current_extended_frontier_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_partial_surface_current_split_portability_readout_counts -q`
  passed: `142 passed, 159 subtests passed`.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q` passed:
  `1445 passed, 1 warning, 193 subtests passed in 80.89s`.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests` passed:
  `Ran 1400 tests in 42.083s OK`.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed:
  12 source records, 8 mechanism fingerprints, 15 ontology families, and 702
  curated mechanism labels.
- `PYTHONPATH=src python -m compileall -q src tests` passed.
- `python -m json.tool` passed for the new JSON artifact.
- Repo-wide JSON parse passed: 3547 JSON files parsed with 0 errors.
- New artifact `source_artifacts` hashes checked: 5 checked, 0 stale.
- Docs artifact-reference check to `/tmp` passed with `missing: 0`.
- `git diff --check` passed.
- Disk guardrail after validation: 14 GiB available.

#### Commit/push status

- Implementation/readout commit
  `8c721d80a9942811b8ba9a5f5ec67610d6a728cf` was pushed to
  `origin/lever-2-research-track`. Local `HEAD` matched
  `origin/lever-2-research-track` after fetch verification before this handoff
  status update.
- This handoff status update is committed and pushed as the final follow-up;
  the exact final branch hash is recorded in automation memory and the final
  response.

#### Exact next action

Materialize source-free current-split event-axis rows for
`source_free_projected_proton_role_subset+bond_change` before any heldout or
deployment claim. Start with the 36-row smoke tranche: all 34 current primary
retention-gate rows plus marginal OOS rows `m_csa:256` and `m_csa:312`.
Then run this LOO frontier again and require both marginal OOS value and the
primary LOO control to clear before expanding to the 41-row best-pair tranche
or full 166-row current primary/current-retained completion.

### 2026-06-04 Lever 2 Research Run 5

#### Wall-clock ledger

- STARTED_AT: `2026-06-04T18:31:33Z`
- STARTED_LOCAL: `2026-06-04T13:31:33-0500 CDT`
- ENDED_AT: `2026-06-04T18:58:23Z`
- ENDED_LOCAL: `2026-06-04T13:58:23-0500 CDT`
- ELAPSED_MINUTES: `26.83`

#### Intent

Continue Lever 2 mechanism-representation research only. Start from the
dedicated `lever-2-research-track` branch, rebase it onto current `origin/main`,
and produce a measured train/cal readout before any blocker conclusion.

#### Work log

- Started in detached automation worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/b316/catalytic-earth`; found
  existing branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` and
  continued there for all branch work.
- Initial disk was below the 10 GiB guardrail at 8.0 GiB available. Removed
  three clean stale detached Codex worktrees with `git worktree remove`,
  leaving the main Lever 3 worktree, the Lever 2 branch worktree, and the
  current detached automation worktree in place. Disk recovered to 18 GiB
  available before fetch/rebase and substantive work.
- Fetched `origin` and rebased `lever-2-research-track` onto current
  `origin/main`. Resolved the expected `src/catalytic_earth/cli.py` conflict
  by keeping both the Lever 2 command handler and the newer Lever 3 channel
  veto/retention frontier command handlers.
- Added a measured Lever 2 event-axis frontier builder/CLI:
  `build-lever2-event-axis-current-extended-frontier-readout`.
- Wrote the measured readout artifact and report:
  `artifacts/v3_lever2_event_axis_current_extended_frontier_readout_current702_20260604.json`
  and
  `work/lever2_event_axis_current_extended_frontier_readout_current702_20260604.md`.
- The new readout selects simple mechanism event-axis abstention rules on the
  mechanism calibration split only, then applies them to the current extended
  train/cal OOS overlap from the prior Lever 2 mechanism/current readout. It
  evaluates single axes and calibrated pair unions without scoring heldout rows
  or changing the fixed geometry/fold threshold.

#### Measured results

- Current overlap measured: 21 current extended train/cal OOS rows with
  row-specific M-CSA train/cal mechanism features, of which 13 are retained by
  the fixed current geometry/fold surface and 8 are already abstained.
- Single-axis frontier: best single axis is
  `source_free_projected_proton_role_subset`; it retains 4/4 calibration
  primaries, abstains 9/28 calibration OOS rows, catches 5/13 current-retained
  overlap rows (`m_csa:17`, `m_csa:59`, `m_csa:85`, `m_csa:194`,
  `m_csa:222`), and raises the fixed-current OR abstentions to 13/21 overlap
  rows.
- Pair frontier: best pair is
  `source_free_projected_proton_role_subset+bond_change`; it retains 4/4
  calibration primaries, abstains 13/28 calibration OOS rows, catches 7/13
  current-retained overlap rows (`m_csa:17`, `m_csa:59`, `m_csa:85`,
  `m_csa:194`, `m_csa:222`, `m_csa:256`, `m_csa:312`), and raises the fixed
  current OR abstentions to 15/21 overlap rows.
- Classification: research-only local signal. The event-axis frontier adds
  signal on the current extended train/cal OOS overlap, but it is not
  deployable and cannot claim integrated operating-point value because valid
  current-primary calibration-feature overlap remains 0/34 and approved
  source-free current-split event-axis rows remain missing.
- Exact missing evidence carried by the artifact: 34 current primary rows and
  132 current-retained OOS rows require source-free event-axis/mechanism rows.
  The artifact also names the 5 best-single and 7 best-pair retained-overlap
  rows to use as the first verification tranche after source-free
  materialization.

#### Guardrails

- Work is restricted to Lever 2 research.
- No labels, registries, ontologies, imports, production thresholds, heldout
  splits, or heldout tuning changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, or heldout
  split information were used as predictive features.
- Labels/`is_primary` flags were used only for calibration threshold selection
  and metric accounting; entry IDs were used only for split/overlap accounting.
- M-CSA row-specific mechanism features remain train/cal-only research
  evidence; no source-free rows were materialized or promoted.

#### Validation

- Rebase conflict sanity check: `python -m py_compile src/catalytic_earth/cli.py`
  passed.
- Focused new-readout tests:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_event_axis_frontier_selects_calibrated_current_overlap_rule tests/test_cli.py::CliTests::test_lever2_event_axis_current_extended_frontier_parser_defaults tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_current_extended_frontier_readout_counts -q`
  passed: `3 passed`.
- Broader Lever 2/CLI regression cluster:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py tests/test_cli.py tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_axis_current_extended_frontier_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_current_extended_oos_mechanism_overlap_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_partial_surface_current_split_portability_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_split_alignment_readout_current_counts -q`
  passed: `140 passed, 159 subtests passed`.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q` passed:
  `1442 passed, 1 warning, 193 subtests passed in 80.95s`.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests` passed:
  `Ran 1397 tests in 42.004s OK`.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed:
  12 source records, 8 mechanism fingerprints, 15 ontology families, and 702
  curated mechanism labels.
- `PYTHONPATH=src python -m compileall -q src tests` passed.
- `python -m json.tool` passed for the new JSON artifact.
- Repo-wide JSON parse passed: 3546 JSON files parsed.
- Docs artifact-reference check to `/tmp` passed with `missing: 0`; tracked
  timestamp churn from the report side effect was restored.
- New artifact `source_artifacts` hashes checked: 5 checked, 0 stale.
- `git diff --check` passed.
- Disk guardrail after validation: 18 GiB available.

#### Commit/push status

- Implementation/readout commit
  `be1bf9339d29119689fca7500963dca4d866963f` was pushed to
  `origin/lever-2-research-track` with `--force-with-lease` after the branch
  rebase. Final fetch/sync verification matched local `HEAD` and
  `origin/lever-2-research-track` at that hash before this handoff status
  update. This status update is committed and pushed as the final follow-up;
  the exact final hash is recorded in automation memory and the final response.

#### Exact next action

Materialize source-free current-split event-axis rows, starting with the 34
current primary retention-gate rows and the 132 current-retained OOS rows. Use
the 7 best-pair retained-overlap rows named in the new artifact as the first
verification tranche, then rerun
`build-lever2-event-axis-current-extended-frontier-readout` and the existing
current-extended mechanism/electron-flow readouts before any deployable or
heldout claim.

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
