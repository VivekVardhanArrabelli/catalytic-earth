# Lever 2 Research Handoff

## Current Automation Run

- Automation ID: `catalytic-earth-lever-2-research-loop`
- Branch: `lever-2-research-track`
- STARTED_AT_UTC: `2026-06-05T19:31:39Z`
- STARTED_AT_LOCAL: `2026-06-05T14:31:39-0500 CDT`
- ENDED_AT_UTC: `2026-06-05T20:21:00Z`
- ENDED_AT_LOCAL: `2026-06-05T15:21:00-0500 CDT`
- ELAPSED_MINUTES: `49.35`
- Scope: Lever 2 mechanism-representation research only.
- Guardrails: source-free/deployment-valid feature discipline, no heldout tuning,
  no mechanism text, EC/Rhea IDs, labels, source IDs, target names, registry
  edits, ontology edits, import edits, production threshold edits, or heldout
  split edits.

## Run Ledger

### 2026-06-05 Lever 2 Research Run 29

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T19:31:39Z`
- STARTED_LOCAL: `2026-06-05T14:31:39-0500 CDT`
- ENDED_AT: `2026-06-05T20:21:00Z`
- ENDED_LOCAL: `2026-06-05T15:21:00-0500 CDT`
- ELAPSED_MINUTES: `49.35`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Start from the source-free approval/import smoke-review readout and make the
next measured readout that tests whether the direct source-free component
fields can be promoted from research-only smoke review toward an approved
train/cal sidecar operating-point gate while preserving the current primary
retention.

#### Work log

- Run opened from automation checkout
  `/Users/vivekvardhanarrabelli/.codex/worktrees/66f9/catalytic-earth`, which
  was a clean detached duplicate and not the dedicated Lever 2 branch worktree.
- Switched substantive work to the dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from Lever 3.
- Initial disk was below the 10 GiB guardrail at 7.1 GiB free. The clean
  detached duplicate checkout was removed with `git worktree remove`,
  restoring disk to 11 GiB free before research writes continued.
- Added
  `build-lever2-source-free-electron-flow-approval-import-smoke-materialization-readout`.
  This consumes the prior smoke-review readout and the current approved
  train/cal feature sidecar, simulates the 35-row protected smoke import in
  approved-sidecar shape, and reruns the fixed gate from that in-memory sidecar.
  It also expands the same collision-safe source-free event-field namespace to
  all 74 current-split rows and measures the full current-split gate in memory.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_approval_import_smoke_materialization_readout_current702_20260605.json`
  and
  `work/lever2_source_free_electron_flow_approval_import_smoke_materialization_readout_current702_20260605.md`.
  SHA-256:
  `362cdf57c439e177877ac7bd5902175ee09e7e37d0e061c8816c108e60b814a5`
  for the JSON and
  `4d5b85b0376c32b966989a506b542aabcc39fc6708f904e2a9819c0056cacff3`
  for the Markdown report.

#### Measured results

- Status:
  `lever2_source_free_electron_flow_approval_import_smoke_materialization_readout_research_only_collision_safe_namespaced_smoke_materialization_gate_positive_pending_protected_import`.
  Result class:
  `research_only_collision_safe_namespaced_smoke_materialization_gate_positive_pending_protected_import`.
- The direct generic import route found an exact protected-sidecar collision:
  existing approved row `m_csa:102` currently has
  `has_electron_transfer_event=true` and `electron_transfer_count=1`, while the
  source-free direct smoke row would set them to `false` and `0`. That is a
  protected import-contract collision, not an operating-point failure.
- The collision-safe namespaced route avoids that overwrite with
  `has_source_free_direct_electron_transfer_event` and
  `source_free_direct_electron_transfer_count`. The 35-row smoke gate is
  35/35 complete, has 0 current-primary positives, preserves primary retain
  recall `1.0`, abstains `m_csa:104`, matches the prior smoke-review gate, and
  has incremental OOS abstain recall `0.013333` with union OOS recall `0.48`.
- The full 74-row namespaced current-split gate is 74/74 complete, has 34
  current primary rows, 40 current-retained OOS rows, 0 current-primary
  positives, primary retain recall `1.0`, and retained-OOS positives
  `m_csa:104`, `m_csa:119`, and `m_csa:464`. Incremental OOS abstain recall
  vs the current geometry/fold denominator is `0.04`; union OOS recall is
  `0.506667`.
- Import/review delta: the 35-row smoke tranche would add 34 rows new to the
  approved sidecar and update 1 existing row; after smoke passes, the remaining
  39 current-split rows are all new to the approved sidecar and 39/39 complete.
  The selected namespaced route has 0 critical violations and 0 direct feature
  conflicts while preserving the generic-field collision as an explicit
  contract finding.
- Interpretation: direct source-free electron-flow fields now have a measured
  train/cal-disciplined operating-point readout in approved-sidecar shape that
  preserves primary retention and adds retained-OOS abstention beyond the
  current geometry/fold surface. The remaining gap is protected approval/import
  execution for the namespaced direct event fields, not missing source-free
  electron-flow evidence.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, heldout splits, or Lever
  3 files changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names,
  accessions, PDB IDs, coordinate paths, or provenance were used as predictive
  feature values. Entry IDs are used only for tranche membership, conflict
  accounting, and missing-evidence accounting.
- The selected gate uses only direct source-free electron-flow fields:
  `has_source_free_direct_electron_transfer_event`,
  `source_free_direct_electron_transfer_count`,
  `has_source_free_pqq_donor_acceptor_contact`,
  `source_free_pqq_donor_acceptor_contact_count`,
  `has_source_free_nad_family_donor_acceptor_distance`,
  `source_free_nad_family_donor_acceptor_distance_count`,
  `has_source_free_iron_sulfur_or_iron_donor_acceptor_distance`, and
  `source_free_iron_sulfur_or_iron_donor_acceptor_distance_count`.
- The readout remains research-only and does not approve, import, promote,
  write approved sidecars, or set `predictive_use_allowed=true`.
- Final pre-handoff disk check showed 12 GiB free, above the 10 GiB guardrail.

#### Validation

- Focused new tests:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_approval_import_smoke_materialization_readout tests/test_cli.py::CliTests::test_lever2_electron_flow_approval_import_smoke_materialization_parser_defaults tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_approval_import_smoke_materialization_current_counts -q`:
  3 passed.
- Touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  504 passed, 193 subtests passed.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q`: 1581 passed, 212 subtests passed, with
  the existing sklearn/SciPy L-BFGS-B deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests -q`: 1536 tests OK,
  with the same existing warning.
- Hash-seed stability: `PYTHONHASHSEED=1` through `PYTHONHASHSEED=10` full
  pytest and full unittest discovery all passed with the same existing warning.
- Touched-slice hash-seed stability: `PYTHONHASHSEED=1` through
  `PYTHONHASHSEED=4` touched-file pytest slice passed.
- `PYTHONPATH=src python -m compileall -q src tests`: passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 mechanism ontology families, and 702 curated
  labels validated.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- `git diff --check`: passed.
- Expanded artifact audit passed: normalized regeneration matched after
  deleting `created_utc`; selected namespaced smoke and full-74 rows contained
  only the eight allowed direct namespaced electron-flow keys; selected-route
  `critical_violation_total` is 0; generic collision accounting is exactly
  `m_csa:102` on `has_electron_transfer_event` and `electron_transfer_count`;
  protected-surface flags remained false.

#### Commit/push status

- Commit and push completed in this wrap-up; branch sync verified before
  returning.

#### Exact next action

- Execute protected approval/import only for the collision-safe 35-row smoke
  tranche with `has_source_free_direct_electron_transfer_event` and
  `source_free_direct_electron_transfer_count` as the direct event fields,
  rerun the written approved-sidecar-only smoke gate, and expand to the
  remaining 39 current-split rows only if primary retain recall remains `1.0`.

### 2026-06-05 Lever 2 Research Run 28

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T18:33:11Z`
- STARTED_LOCAL: `2026-06-05T13:33:11-0500 CDT`
- ENDED_AT: `2026-06-05T19:23:59Z`
- ENDED_LOCAL: `2026-06-05T14:23:59-0500 CDT`
- ELAPSED_MINUTES: `50.80`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Start from the source-free electron-flow approval/import dry-run readout and
try the next measured route toward deployable train/cal signal: preserve the
current fixed operating point and primary retention while testing whether the
direct source-free component fields can be audited against the protected
approved-sidecar shape and smoke tranche before any protected import is
requested.

#### Work log

- Run opened from automation checkout
  `/Users/vivekvardhanarrabelli/.codex/worktrees/95ac/catalytic-earth`, which
  was a clean detached duplicate and not the dedicated Lever 2 branch
  worktree.
- Switched substantive work to the dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from Lever 3.
- Initial disk was below the 10 GiB guardrail at 8.4 GiB free. The clean
  detached duplicate checkout was removed with `git worktree remove`,
  restoring disk to 12 GiB free before research writes continued.
- Added
  `build-lever2-source-free-electron-flow-approval-import-smoke-review-readout`.
  This consumes the committed approval/import dry-run artifact, filters the
  dry-run feature payload down to the eight direct source-free electron-flow
  fields only, isolates the smallest requested smoke tranche
  (`m_csa:104` plus the 34 current primary retention-gate rows), then measures
  both that 35-row smoke tranche and the full 74-row current split without
  writing approved sidecars, imports, predictive-use flags, production
  thresholds, labels, registries, ontologies, or heldout splits.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_approval_import_smoke_review_readout_current702_20260605.json`
  and
  `work/lever2_source_free_electron_flow_approval_import_smoke_review_readout_current702_20260605.md`.
  SHA-256:
  `aa6016d9ae3e19a0f854729c18249c9911c09187bbf9498fc7f06e219db67ab4`
  for the JSON and
  `9d94c0ff27f3d0f752a1a9e6efee2602ae328a62f4d506a840667c068c7c0aba`
  for the Markdown report.

#### Measured results

- Status:
  `lever2_source_free_electron_flow_approval_import_smoke_review_readout_research_only_smoke_review_positive_full_expansion_positive_pending_protected_import`.
  Result class:
  `research_only_smoke_review_positive_full_expansion_positive_pending_protected_import`.
- Smallest smoke tranche: 35/35 direct component rows complete, 34 current
  primary rows, 0 current-primary positives, primary retain recall `1.0`, and
  `m_csa:104` abstained as the only retained-OOS row. Incremental OOS abstain
  recall vs the current geometry/fold denominator is `0.013333`; union OOS
  recall is `0.48`.
- Full current-split expansion: 74/74 direct component rows complete, 34
  current primary rows, 40 current-retained OOS rows, 0 current-primary
  positives, primary retain recall `1.0`, and 3 retained-OOS positives:
  `m_csa:104`, `m_csa:119`, and `m_csa:464`. Incremental OOS abstain recall
  vs the current geometry/fold denominator is `0.04`; union OOS recall is
  `0.506667`.
- Import/review delta: the 35-row smoke tranche would add 34 rows new to the
  approved sidecar and update 1 existing row. The full 74-row expansion would
  add 73 current-split rows and update 1 existing current-split row; the full
  dry-run import set remains 78 rows, including 4 support rows.
- Interpretation: direct source-free electron-flow fields are now measured on
  the requested smallest smoke tranche and on the full current split while
  preserving primary retention. The remaining gap is protected approval/import,
  not missing source-free evidence or operating-point failure.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, heldout splits, or Lever
  3 files changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names,
  accessions, PDB IDs, coordinate paths, or provenance were used as predictive
  feature values. Entry IDs are used only for tranche membership and missing
  evidence accounting.
- The new smoke-review artifact filters row-specific payloads to the eight
  direct electron-flow fields only:
  `has_electron_transfer_event`, `electron_transfer_count`,
  `has_source_free_pqq_donor_acceptor_contact`,
  `source_free_pqq_donor_acceptor_contact_count`,
  `has_source_free_nad_family_donor_acceptor_distance`,
  `source_free_nad_family_donor_acceptor_distance_count`,
  `has_source_free_iron_sulfur_or_iron_donor_acceptor_distance`, and
  `source_free_iron_sulfur_or_iron_donor_acceptor_distance_count`.
- The readout remains research-only and does not approve, import, promote,
  write approved sidecars, or set `predictive_use_allowed=true`.
- Final pre-handoff disk check showed 11 GiB free, above the 10 GiB guardrail.

#### Validation

- Focused new tests:
  `PYTHONPATH=src python -m pytest tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_approval_import_smoke_review_readout tests/test_cli.py::CliTests::test_lever2_electron_flow_approval_import_smoke_review_parser_defaults tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_approval_import_smoke_review_current_counts -q`:
  3 passed.
- Touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  501 passed, 193 subtests passed.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q`: 1578 passed, 212 subtests passed, with
  the existing sklearn/SciPy L-BFGS-B deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests -q`: 1533 tests OK,
  with the same existing warning.
- Hash-seed stability: `PYTHONHASHSEED=1` through `PYTHONHASHSEED=16` full
  pytest and full unittest discovery all passed with the same existing warning
  where applicable.
- `PYTHONPATH=src python -m compileall -q src tests`: passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 mechanism ontology families, and 702 curated
  labels validated.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- `git diff --check`: passed.
- New artifact audit passed: normalized regeneration matched after deleting
  `created_utc`; source hash for the dry-run input matched
  `a7e9175362479df408e624e2bcd20bf90a2cfd63112af65d374d3513e6666276`;
  feature rows contained only the eight direct electron-flow keys; row-specific
  feature values contained no entry IDs, accessions, PDB/coordinate/path
  strings, mechanism text, labels, EC/Rhea tokens, source IDs, or target tokens;
  protected-surface flags remained false.

#### Commit/push status

- Commit and push completed in this wrap-up; branch sync verified before
  returning.

#### Exact next action

- Protected materialization/review of only the 35-row smoke tranche:
  approve the direct source-free PQQ/NAD/Fe-S component-field contract for
  train/cal use, materialize `m_csa:104` plus the 34 current primary
  retention-gate rows into the approved train/cal feature sidecar, rerun the
  approved-sidecar-only smoke gate unchanged, and expand to the remaining
  current-split rows only if primary retain recall remains `1.0`.

### 2026-06-05 Lever 2 Research Run 27

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T17:32:54Z`
- STARTED_LOCAL: `2026-06-05T12:32:54-0500 CDT`
- ENDED_AT: `2026-06-05T18:21:54Z`
- ENDED_LOCAL: `2026-06-05T13:21:54-0500 CDT`
- ELAPSED_MINUTES: `49.02`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Use the measured train/cal sidecar-candidate readout as the baseline, then
attempt the smallest train/cal-disciplined approval/import preflight that can
test whether the direct source-free PQQ/NAD/Fe-S component fields can be made
measurable from approved-sidecar-shaped evidence without touching protected
labels, registries, ontologies, imports, production thresholds, or heldout
splits.

#### Work log

- Run opened from automation checkout
  `/Users/vivekvardhanarrabelli/.codex/worktrees/6664/catalytic-earth`, which
  was a clean detached duplicate and not the dedicated Lever 2 branch
  worktree.
- Switched substantive work to the dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from Lever 3.
- Initial disk was below the 10 GiB guardrail at 9.4 GiB free. The clean
  detached duplicate checkout was removed with `git worktree remove`,
  restoring disk to 13 GiB free before research writes continued.
- Added
  `build-lever2-source-free-electron-flow-approval-import-dry-run-readout`.
  This consumes the measured train/cal sidecar-candidate readout, the current
  approved train/cal feature sidecar, and the train/cal input manifest, then
  overlays the candidate direct PQQ/NAD/Fe-S rows onto the approved-sidecar
  shape in memory. It proposes explicit calibration splits for selected Fe-S
  support rows `m_csa:127` and `m_csa:281`, reruns the fixed current-split
  gate, and reports split-policy sensitivity plus component ablations without
  editing protected approved sidecars, imports, predictive-use flags, labels,
  registries, ontologies, thresholds, or heldout splits.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_approval_import_dry_run_readout_current702_20260605.json`
  and
  `work/lever2_source_free_electron_flow_approval_import_dry_run_readout_current702_20260605.md`.

#### Measured results

- Status:
  `lever2_source_free_electron_flow_approval_import_dry_run_readout_research_only_approval_import_dry_run_closes_measurability_gap`.
  Result class:
  `research_only_approval_import_dry_run_closes_measurability_gap`.
- Approved-sidecar route before dry run: 43 approved sidecar rows, only 1/74
  current-split rows present, and 0/74 current-split rows with the direct
  PQQ/NAD/Fe-S component fields complete.
- Dry-run approved-sidecar overlay: 78/78 proposed import rows are source-free
  complete with direct component fields, 78/78 have explicit train/cal splits,
  and 74/74 current-split rows become direct-component complete. The overlay
  would add 75 rows new to the approved sidecar and update 3 existing approved
  rows; it would add 73 current-split rows and all current positive rows
  `m_csa:104`, `m_csa:119`, and `m_csa:464`.
- Fixed gate after dry run: 0/34 current primary positives, primary retain
  recall `1.0`, 3/40 current-retained OOS positives
  (`m_csa:104`, `m_csa:119`, `m_csa:464`), retained-OOS abstain recall
  `0.075`, incremental OOS abstain recall vs the current geometry/fold
  denominator `0.04`, and union OOS recall `0.506667`.
- Selected Fe-S split sensitivity: assigning both selected Fe-S support rows
  to `calibration` or both to `train` leaves the fixed current-split gate
  unchanged; 2/2 tested policies matched the primary dry-run gate.
- Component ablation after dry run: PQQ-only catches `m_csa:104`; NAD-only
  catches `m_csa:464`; Fe-S-only catches `m_csa:119`; PQQ+NAD catches
  `m_csa:104` and `m_csa:464`; PQQ+NAD+Fe-S catches all three rows. Fe-S
  therefore adds exactly `m_csa:119` beyond the PQQ+NAD dry-run surface.
- Interpretation: the approved-sidecar-only route is not intrinsically
  source-free or operating-point blocked. It becomes measurable in this
  research-only dry run once the exact protected import/approval/split steps
  are applied, while preserving primary retention.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, heldout splits, or Lever
  3 files changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names,
  accessions, PDB IDs, coordinate paths, or provenance were used as predictive
  feature values. Split, manifest, row ID, and dry-run provenance metadata
  remain outside `row_specific_event_features`.
- The dry-run remains research-only and does not approve, import, promote,
  write approved sidecars, or set `predictive_use_allowed=true`.
- Disk guardrail recovered from the initial detached-worktree low-disk state
  and remained above 10 GiB; final pre-wrap check showed 12 GiB free.

#### Validation

- Focused new tests:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::CliTests::test_lever2_electron_flow_approval_import_dry_run_parser_defaults tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_approval_import_dry_run_readout tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_approval_import_dry_run_current_counts -q`:
  3 passed.
- Touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  498 passed, 193 subtests passed.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q`: 1575 passed, 212 subtests passed, with
  the existing sklearn/SciPy L-BFGS-B deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests -q`: 1530 tests OK,
  with the same existing warning.
- Hash-seed stability: `PYTHONHASHSEED=1` through `PYTHONHASHSEED=12` full
  pytest and full unittest discovery all passed with the same existing warning
  where applicable.
- `PYTHONPATH=src python -m compileall -q src tests`: passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 mechanism ontology families, and 702 curated
  labels validated.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- `git diff --check`: passed.
- Repo JSON/JSONL parse sweep passed: 3595 JSON files and 27 JSONL files
  parsed with 0 errors.
- New dry-run artifact audit passed: source hashes current, normalized
  regeneration matched after normalizing `created_utc`, all 78 dry-run rows
  carried complete direct component fields, 0 forbidden row-feature key hits,
  row-specific feature payloads contained no coordinate paths, accessions,
  source IDs, target names, mechanism text, or label-type tokens, guardrails
  kept protected surfaces unmodified, and the Markdown report contained the
  status, fixed-gate result, split sensitivity, and component ablation.
- Protected changed-path audit passed.

#### Commit/push status

- Commit and push are pending for this wrap-up block.

#### Exact next action

- Run the protected sidecar materialization/review step using the 78 dry-run
  rows and exact direct component fields from the new artifact. Assign
  `m_csa:127` and `m_csa:281` to an explicit train/cal split (the dry-run gate
  is insensitive to all-calibration vs all-train for those support rows), set
  `predictive_use_allowed=true` for those two Fe-S support rows, then rerun the
  approved-sidecar-only gate unchanged. If protected materialization is not
  authorized, the smallest negative is now the protected approval/import gate,
  not missing source-free electron-flow evidence or operating-point failure.

### 2026-06-05 Lever 2 Research Run 26

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T16:31:49Z`
- STARTED_LOCAL: `2026-06-05T11:31:49-0500 CDT`
- ENDED_AT: `2026-06-05T17:22:09Z`
- ENDED_LOCAL: `2026-06-05T12:22:09-0500 CDT`
- ELAPSED_MINUTES: `50.33`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Use the candidate train/cal bundle readout as the measured baseline, then try
the smallest source-free route that can move the direct electron-flow fields
from research-only candidate evidence toward a train/cal-disciplined readout
without editing labels, registries, ontologies, imports, production thresholds,
or heldout splits.

#### Work log

- Run opened from automation checkout
  `/Users/vivekvardhanarrabelli/.codex/worktrees/031c/catalytic-earth`, which
  was a clean detached duplicate and not the dedicated Lever 2 branch
  worktree.
- Switched substantive work to the dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from Lever 3.
- Initial disk was below the 10 GiB guardrail at 9.5 GiB free. The clean
  detached duplicate checkout was removed with `git worktree remove`,
  restoring disk to 13 GiB free before research writes continued.
- Added
  `build-lever2-source-free-electron-flow-train-cal-sidecar-candidate-readout`.
  This consumes the measured candidate train/cal bundle and the currently
  approved train/cal feature sidecar, remaps the candidate bundle into
  sidecar-shaped row-specific direct electron-flow rows, reruns the fixed
  operating point, and separately attempts the approved-sidecar-only current
  split route without editing approved sidecars, imports, splits, labels,
  thresholds, registries, or ontologies.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_train_cal_sidecar_candidate_readout_current702_20260605.json`
  and
  `work/lever2_source_free_electron_flow_train_cal_sidecar_candidate_readout_current702_20260605.md`.

#### Measured results

- Status:
  `lever2_source_free_electron_flow_train_cal_sidecar_candidate_readout_research_only_train_cal_sidecar_candidate_measured_pending_protected_import`.
  Result class:
  `research_only_train_cal_sidecar_candidate_measured_pending_protected_import`.
- Candidate sidecar readout: 78/78 rows have complete sidecar-shaped direct
  source-free electron-flow fields and 0 forbidden predictive feature-key hits.
  All 78/78 rows are manifest-contained or explicitly train/cal split; 76/78
  rows have explicit `train`/`calibration` splits.
- Fixed current-split gate: 74/74 current rows are complete, 0/34 current
  primary rows are positive, primary retain recall is `1.0`, and 3/40
  current-retained OOS rows are positive: `m_csa:104`, `m_csa:119`, and
  `m_csa:464`. Incremental OOS abstain recall vs the current geometry/fold
  denominator is `0.04`, and union OOS recall is `0.506667`.
- Approved-sidecar-only attempt: the current approved train/cal feature
  sidecar contains only 1/74 current-split rows (`m_csa:102`) and 0/74
  current-split rows with the required direct PQQ/NAD/Fe-S component fields
  complete. It contains no current positive direct electron-flow rows and
  still contains only the two projection support rows `m_csa:59` and
  `m_csa:256`.
- Remaining protected gaps are exact: import/approve the six direct component
  fields, set `predictive_use_allowed=true` for selected Fe-S support rows
  `m_csa:127` and `m_csa:281`, assign those Fe-S rows explicit train/cal
  splits, and add approved sidecar rows for current positive direct
  electron-flow rows `m_csa:104`, `m_csa:119`, and `m_csa:464`.
- Interpretation: direct source-free electron-flow fields now have a measured
  train/cal-disciplined candidate readout that adds operating-point value
  beyond the current geometry/fold surface while preserving primary retention.
  Deployability remains false only because the protected import/approval/split
  steps are not yet performed and are outside this run's guardrails.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, heldout splits, or Lever
  3 files changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names,
  accessions, PDB IDs, coordinate paths, or provenance were used as predictive
  feature values. Split and manifest metadata remain outside
  `row_specific_event_features`.
- The sidecar candidate remains research-only and does not approve, import,
  promote, or set `predictive_use_allowed=true` for any row.
- Disk guardrail recovered from the initial detached-worktree low-disk state
  and remained at 13 GiB free during wrap.

#### Validation

- Focused new tests:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::CliTests::test_lever2_electron_flow_train_cal_sidecar_candidate_parser_defaults tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_train_cal_sidecar_candidate_readout tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_train_cal_sidecar_candidate_current_counts -q`:
  3 passed.
- Touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  495 passed, 193 subtests passed.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q`: 1572 passed, 212 subtests passed, with
  the existing sklearn/SciPy L-BFGS-B deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests -q`: 1527 tests OK,
  with the same existing warning.
- Hash-seed stability: `PYTHONHASHSEED=1` through `PYTHONHASHSEED=11` full
  pytest and full unittest discovery all passed with the same existing warning
  where applicable.
- `PYTHONPATH=src python -m compileall -q src tests`: passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 mechanism ontology families, and 702 curated
  labels validated.
- `git diff --check`: passed.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- Repo JSON/JSONL parse sweep passed: 3594 JSON files and 27 JSONL files
  parsed with 0 errors.
- New sidecar-candidate artifact targeted audit passed: source hashes current,
  normalized regeneration matched after normalizing `created_utc`, all 78
  feature rows carried the expected direct electron-flow schema, 0 forbidden
  predictive-key hits, 78/78 manifest-or-explicit train/cal containment, the
  approved-sidecar-only overlap was exactly `m_csa:102`, and 0 approved
  current-split rows had direct component fields complete.
- Report consistency audit passed for the generated Markdown report.
- Protected-surface changed-path audit passed.
- Broad electron-flow source file-hash audit found one older pre-existing
  stale source hash in
  `artifacts/v3_lever2_source_free_electron_flow_combined_direct_feature_sidecar_readout_current702_20260605.json`
  pointing at the relaxed non-PQQ readout. This was not used as a pass/fail
  gate for the new sidecar-candidate artifact, whose direct source hashes
  passed.

#### Commit/push status

- Primary research commit:
  `63d8278193aea0a11d8c507780e64f7e794e141c`
  (`Add Lever 2 electron-flow sidecar candidate readout`).
- Primary commit was pushed to `origin/lever-2-research-track`.
- Fetch/sync verification after the primary push matched local `HEAD` and
  `origin/lever-2-research-track` at
  `63d8278193aea0a11d8c507780e64f7e794e141c`.
- This final handoff status update is being committed and pushed separately as
  a handoff-only wrap-up change.

#### Exact next action

- Perform the protected approval/import step for the candidate direct
  source-free PQQ/NAD/Fe-S component fields, set `predictive_use_allowed=true`
  for `m_csa:127` and `m_csa:281`, assign those Fe-S support rows to explicit
  train/cal splits, add approved sidecar rows for `m_csa:104`, `m_csa:119`,
  and `m_csa:464`, then rerun the fixed train/cal sidecar-candidate gate
  without threshold changes or heldout use.

### 2026-06-05 Lever 2 Research Run 25

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T15:33:09Z`
- STARTED_LOCAL: `2026-06-05T10:33:09-0500 CDT`
- ENDED_AT: `2026-06-05T16:22:19Z`
- ENDED_LOCAL: `2026-06-05T11:22:19-0500 CDT`
- ELAPSED_MINUTES: `49.18`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Use the measured 74-row current-split source-free electron-flow baseline and
the Fe-S support-subset preflight to attempt the smallest next measured route
toward train/cal-supported direct electron-flow operating-point value.

#### Work log

- Run opened from automation checkout
  `/Users/vivekvardhanarrabelli/.codex/worktrees/e6e0/catalytic-earth`, which
  was a clean detached duplicate and not the dedicated Lever 2 branch
  worktree.
- Switched substantive work to the dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from Lever 3.
- Initial disk was below the 10 GiB guardrail at 9 GiB free. The clean
  detached duplicate checkout was removed with `git worktree remove`, restoring
  disk to 12 GiB free before research work continued.
- Added
  `build-lever2-source-free-electron-flow-candidate-train-cal-bundle-readout`.
  This consumes the measured approval-qualified `PQQ+NAD+Fe-S/iron` union, the
  Fe-S support-subset preflight, the relaxed non-PQQ/NAD projection scout, the
  currently approved train/cal feature sidecar, and the train/cal input
  manifest.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_candidate_train_cal_bundle_readout_current702_20260605.json`
  and
  `work/lever2_source_free_electron_flow_candidate_train_cal_bundle_readout_current702_20260605.md`.
- The new readout materializes a research-only candidate import bundle with the
  74 current-split direct component rows plus the smallest measured support
  rows: `m_csa:59` and `m_csa:256` for the projection-backed NAD-family
  support route, and `m_csa:127` and `m_csa:281` for the selected Fe-S/iron
  support subset.
- Hardened the builder so the candidate bundle is incomplete if any expected
  support row fails to materialize; added a negative synthetic test for that
  missing-support path.

#### Measured results

- Status:
  `lever2_source_free_electron_flow_candidate_train_cal_bundle_readout_research_only_candidate_train_cal_bundle_materialized_pending_approval_import`.
  Result class:
  `research_only_candidate_train_cal_bundle_materialized_pending_approval_import`.
- Candidate current-split readout: 74/74 current rows are complete with direct
  source-free PQQ, NAD-family, and Fe-S/iron component fields. The fixed gate
  has 0/34 current-primary positives, preserves primary retain recall at `1.0`,
  catches 3/40 current-retained OOS rows (`m_csa:104`, `m_csa:119`,
  `m_csa:464`), gives retained-OOS abstain recall `0.075`, incremental OOS
  recall `0.04`, and union OOS recall `0.506667`.
- Candidate support bundle: all 4/4 expected support rows materialize with
  direct source-free component fields and 0 forbidden predictive-key hits.
  PQQ+NAD support rows are `m_csa:59` and `m_csa:256`; selected Fe-S/iron
  support rows are `m_csa:127` and `m_csa:281`.
- Train/cal manifest preflight: the selected Fe-S support rows `m_csa:127` and
  `m_csa:281` are present in the train/cal input manifest, are
  `in_distribution`, and have `role_graph_status=ok`.
- Approved sidecar gap: the currently approved train/cal feature sidecar still
  has the two PQQ+NAD projection-support rows (`m_csa:59`, `m_csa:256`) but
  lacks all direct source-free component fields, lacks the selected Fe-S
  support rows, and lacks current positive rows (`m_csa:104`, `m_csa:119`,
  `m_csa:464`).
- Interpretation: this is not an operating-point failure. Direct source-free
  electron-flow component fields add operating-point value beyond the current
  geometry/fold surface while preserving primary retention in the candidate
  bundle, but deployability remains false because approval/import and explicit
  split assignment are still missing.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, heldout splits, or Lever
  3 files changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names,
  accessions, PDB IDs, coordinate paths, or provenance were used as predictive
  feature values. Candidate support evidence and split/manifest metadata remain
  outside `row_specific_event_features`.
- The candidate bundle remains research-only and does not approve, import,
  promote, or set `predictive_use_allowed=true` for any row.
- Disk guardrail recovered from the initial detached-worktree low-disk state
  and remained at 12 GiB free during validation.

#### Validation

- Focused candidate-bundle tests:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::CliTests::test_lever2_electron_flow_candidate_train_cal_bundle_parser_defaults tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_candidate_train_cal_bundle_readout tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_candidate_train_cal_bundle_requires_expected_support_rows tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_candidate_train_cal_bundle_current_counts -q`:
  passed.
- Touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  492 passed, 193 subtests passed.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q`: 1569 passed, 212 subtests passed, with
  the existing sklearn/SciPy L-BFGS-B deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests -q`: 1524 tests OK,
  with the same existing warning.
- Hash-seed stability checks:
  `PYTHONHASHSEED=1 PYTHONPATH=src python -m pytest -q`,
  `PYTHONHASHSEED=1 PYTHONPATH=src python -m unittest discover -s tests -q`,
  `PYTHONHASHSEED=2 PYTHONPATH=src python -m pytest -q`, and
  `PYTHONHASHSEED=2 PYTHONPATH=src python -m unittest discover -s tests -q`
  all passed with the same existing warning where applicable.
- Final touched-file slice after wrap-up edits:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  492 passed, 193 subtests passed.
- `PYTHONPATH=src python -m compileall -q src tests`: passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 mechanism ontology families, and 702 curated
  labels validated.
- `git diff --check`: passed.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- Repo JSON/JSONL parse sweep passed: 3593 JSON files and 27 JSONL files
  parsed with 0 errors.
- New candidate artifact normalized regeneration passed after normalizing
  `created_utc`; its 5 source artifact hashes are current.
- Candidate row/component consistency audit passed for 78 feature rows;
  support/manifest consistency audit passed; report consistency audit passed;
  forbidden predictive-key audit found 0 hits.
- Protected-surface path audit passed for tracked and untracked changed paths.
- A broad repository-wide source-artifact hash audit was attempted and found
  pre-existing unrelated stale/missing source records in older artifacts, so it
  was not used as a pass/fail gate for this Lever 2 electron-flow run.

#### Commit/push status

- Primary research commit
  `36580260cf9c148bfa1ab54c2a8e45dbce31ec36`
  (`Add Lever 2 electron-flow candidate bundle readout`) was pushed to
  `origin/lever-2-research-track`.
- Fetch/sync verification after the primary push matched local `HEAD` and
  `origin/lever-2-research-track` at
  `36580260cf9c148bfa1ab54c2a8e45dbce31ec36`.
- Actual elapsed time was `49.18` minutes from recorded start to final
  timestamp, shorter than the requested 55-minute work block but substantially
  longer than the prior short run. The ledger records measured time rather than
  inflating it.
- This final handoff status update is being committed and pushed separately as
  a handoff-only wrap-up change.

#### Exact next action

- Approve/import the candidate direct source-free component fields into the
  train/cal feature sidecar, set `predictive_use_allowed=true` for the selected
  Fe-S support rows `m_csa:127` and `m_csa:281`, and assign those Fe-S support
  rows to an explicit train/cal split. Then rerun the fixed
  `PQQ+NAD+Fe-S/iron` candidate bundle without threshold changes or heldout
  use.

### 2026-06-05 Lever 2 Research Run 24

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T14:33:04Z`
- STARTED_LOCAL: `2026-06-05T09:33:04-0500 CDT`
- ENDED_AT: `2026-06-05T14:59:51Z`
- ENDED_LOCAL: `2026-06-05T09:59:51-0500 CDT`
- ELAPSED_MINUTES: `26.78`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Use the newly materialized source-free PQQ+NAD current-split smoke readout as
the measured baseline, then try the next direct source-free electron-flow
readout that can add operating-point signal beyond the current geometry/fold
surface while preserving primary retention.

#### Work log

- Run opened in the dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from Lever 3.
- The automation initially started in a clean detached duplicate checkout
  `/Users/vivekvardhanarrabelli/.codex/worktrees/99b9/catalytic-earth` with
  disk at 9.5 GiB free, below the 10 GiB guardrail. That duplicate checkout
  had no branch and no local changes, so it was removed with
  `git worktree remove` after switching all substantive work to the Lever 2
  branch worktree. Disk then returned to 13 GiB free.
- Added
  `build-lever2-source-free-electron-flow-iron-sulfur-support-subset-preflight-readout`.
  This consumes the measured Fe-S/iron tiny-tranche approval-readiness readout,
  the measured current-split smoke materialization readout, the fixed
  approval-qualified union readout, the projection-backed PQQ+NAD readout, and
  the currently approved train/cal feature sidecar.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_iron_sulfur_support_subset_preflight_readout_current702_20260605.json`
  and
  `work/lever2_source_free_electron_flow_iron_sulfur_support_subset_preflight_readout_current702_20260605.md`.
- The new readout tests whether the remaining Fe-S/iron increment
  (`m_csa:119`) is an operating-point failure or a support-contract/import gap.
  It also checks the approved train/cal sidecar directly so the base PQQ+NAD
  deployability gap is measured instead of inferred.
- No blocker packet was written; the run produced a measured electron-flow
  readout first, then continued through sidecar-presence and reproducibility
  audits.

#### Measured results

- Status:
  `lever2_source_free_electron_flow_iron_sulfur_support_subset_preflight_readout_research_only_fe_s_support_subset_preflight_positive_pending_predictive_import`.
  Result class:
  `research_only_fe_s_support_subset_preflight_positive_pending_predictive_import`.
- Current split: the direct source-free electron-flow surface remains complete
  on 74/74 rows, with 34 current-primary rows, 40 current-retained OOS rows,
  0 current-primary positives, and 2 supported-now PQQ+NAD retained-OOS
  positives (`m_csa:104`, `m_csa:464`).
- Fe-S/iron support subset: the selected tiny bundle-ready support subset is
  exactly `m_csa:127` and `m_csa:281`. Both are blocked only by
  `predictive_use_allowed=true` plus approved train/cal feature-sidecar rows.
  The larger 8-row bundle-ready fallback remains available:
  `m_csa:127`, `m_csa:281`, `m_csa:130`, `m_csa:398`, `m_csa:358`,
  `m_csa:108`, `m_csa:562`, and `m_csa:276`.
- Fixed approval-qualified union: if the selected Fe-S support subset were
  approved/imported, the fixed `PQQ+NAD+Fe-S/iron` union preserves primary
  retention (`0` current-primary positives, primary retain recall `1.0`) and
  catches 3 current-retained OOS rows (`m_csa:104`, `m_csa:119`, `m_csa:464`).
  The Fe-S increment beyond PQQ+NAD is exactly `m_csa:119`, adding `0.013333`
  OOS abstain recall beyond PQQ+NAD and raising union OOS recall from
  `0.493333` to `0.506667`.
- Approved train/cal sidecar preflight: the approved sidecar has 43 rows and
  includes the PQQ+NAD projection-support rows `m_csa:59` and `m_csa:256`,
  but only with generic `has_electron_transfer_event` and
  `electron_transfer_count` fields. It does not contain the selected Fe-S
  support rows, any current positive rows (`m_csa:104`, `m_csa:119`,
  `m_csa:464`), or any direct source-free PQQ/NAD/Fe-S component fields.
- Interpretation: the pending Fe-S/iron increment is not an operating-point
  failure. It is a support-contract/import gap for the `m_csa:119` increment,
  while full direct electron-flow deployability still also requires
  approval/import of the base projection-backed PQQ+NAD component contracts.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, heldout splits, or Lever
  3 files changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names,
  accessions, PDB IDs, coordinate paths, or provenance were used as predictive
  feature values. Accessions and coordinate paths remain outside
  `row_specific_event_features` as nonpredictive source-evidence accounting.
- The new readout remains research-only. It measures sidecar absence/presence
  and support-subset readiness but does not approve, import, or promote any
  direct electron-flow contract.
- Disk guardrail recovered from the initial detached-worktree low-disk state
  and remained at 13 GiB free during validation.

#### Validation

- Focused new-readout tests:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::CliTests::test_lever2_electron_flow_iron_sulfur_support_subset_preflight_parser_defaults tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_iron_sulfur_support_subset_preflight_readout tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_iron_sulfur_support_subset_preflight_current_counts -q`:
  3 passed.
- Touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  488 passed, 193 subtests passed.
- Full pytest after final sidecar-input change:
  `PYTHONPATH=src python -m pytest -q`: 1565 passed, 212 subtests passed,
  with the existing sklearn/SciPy L-BFGS-B deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests -q`: 1520 tests OK,
  with the same existing warning.
- `PYTHONPATH=src python -m compileall -q src tests`: passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 mechanism ontology families, and 702 curated
  labels validated.
- `git diff --check`: passed.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- Repo JSON/JSONL parse sweep passed: 3592 JSON files and 27 JSONL files
  parsed with 0 errors.
- New artifact normalized regeneration passed after normalizing `created_utc`.
  All 5 source artifacts were verified hash-current.
- Electron-flow chain normalized regeneration passed for the
  projection-backed PQQ+NAD readout, Fe-S approval-qualified union readout,
  Fe-S tiny-tranche approval-readiness readout, current-split smoke
  materialization readout, and the new Fe-S support-subset preflight readout.
- New artifact forbidden predictive-key audit found 0 hits inside
  `selected_support_feature_rows[*].row_specific_event_features`.
- Approved-sidecar absence audit passed: projection-support rows are present
  in the approved train/cal sidecar, direct source-free component fields are
  absent, selected Fe-S support rows are absent, and current positive rows are
  absent.
- Scope audit found the expected changed paths only and no protected-surface
  path changes.

#### Commit/push status

- Primary research commit
  `00c197b7eaab1073823ae5ecffd6f55add627a35`
  (`Add Lever 2 Fe-S support subset preflight`) was pushed to
  `origin/lever-2-research-track`.
- Fetch/sync verification after the primary push matched local `HEAD` and
  `origin/lever-2-research-track` at
  `00c197b7eaab1073823ae5ecffd6f55add627a35`.
- Actual elapsed time is shorter than the requested 55-minute work block; the
  ledger records measured time rather than inflating it.
- This final handoff status update is being committed and pushed separately as
  a handoff-only wrap-up change.

#### Exact next action

- Smallest next electron-flow experiment: approve/import the selected
  bundle-ready Fe-S/iron support subset (`m_csa:127`, `m_csa:281`) with
  `predictive_use_allowed=true` and explicit train/cal split assignment, and
  approve/import the base projection-backed PQQ+NAD direct component contracts
  into the train/cal feature sidecar. Then rerun the fixed
  `PQQ+NAD+Fe-S/iron` union without threshold changes or heldout use.
- If the approval contract requires the original 3-row tiny Fe-S tranche,
  first repair `m_csa:443` by resolving the mixed role-graph sequence-position
  accession evidence (`P13063:12`, `P13065:7`) into accession-compatible
  source-free positions, then import all three tiny rows.

### 2026-06-05 Lever 2 Research Run 23

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T13:32:10Z`
- STARTED_LOCAL: `2026-06-05T08:32:10-0500 CDT`
- ENDED_AT: `2026-06-05T14:22:35Z`
- ENDED_LOCAL: `2026-06-05T09:22:35-0500 CDT`
- ELAPSED_MINUTES: `50.42`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Measure whether direct source-free electron-flow fields can be materialized for
the current train/cal smoke tranche (`m_csa:104` plus the 34 current primary
retention-gate rows), preserving primary retention while testing incremental
OOS abstention beyond the current geometry/fold surface.

#### Work log

- Run opened in the dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from Lever 3.
- The automation initially started in a clean detached duplicate checkout
  `/Users/vivekvardhanarrabelli/.codex/worktrees/3c59/catalytic-earth` with
  disk at 9.0 GiB free, below the 10 GiB guardrail. That duplicate checkout had
  no branch and no local changes, so it was removed with `git worktree remove`
  after switching all substantive work to the Lever 2 branch worktree. Disk
  then returned to 13 GiB free.
- Added
  `build-lever2-source-free-electron-flow-current-split-smoke-materialization-readout`.
  This consumes the measured projection-backed `PQQ + NAD-family` direct
  electron-flow feature sidecar, the combined-direct feature sidecar, and the
  approval-qualified `PQQ + NAD + Fe-S/iron` union readout.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_current_split_smoke_materialization_readout_current702_20260605.json`
  and
  `work/lever2_source_free_electron_flow_current_split_smoke_materialization_readout_current702_20260605.md`.
- The readout measures the requested smallest smoke tranche first
  (`m_csa:104` plus 34 current primary retention-gate rows), then expands the
  same source-free PQQ+NAD fields to the 74-row current split and emits a
  40-row retained-OOS expansion matrix. No blocker packet was written.

#### Measured results

- Status:
  `lever2_source_free_electron_flow_current_split_smoke_materialization_readout_research_only_source_free_smoke_tranche_measured_expands_to_74row_current_split_pending_contract_approval`.
  Result class:
  `research_only_source_free_smoke_tranche_measured_expands_to_74row_current_split_pending_contract_approval`.
- Smoke tranche: 35/35 rows have complete direct source-free electron-flow
  fields, with 34/34 current primary rows retained, 0 current-primary
  positives, and exactly 1 current-retained OOS positive: `m_csa:104`.
  Smoke retained-OOS abstain recall is `1.0`; incremental OOS abstain recall
  vs the current geometry/fold OOS denominator is `0.013333`, and the union
  OOS recall is `0.48`.
- Full current split expansion: 74/74 rows have complete source-free PQQ+NAD
  fields, covering 34 current primary rows and 40 current-retained OOS rows.
  It preserves primary retention at `1.0`, has 0 current-primary positives,
  catches 2/40 current-retained OOS rows (`m_csa:104`, `m_csa:464`), and adds
  `0.026667` incremental OOS abstain recall beyond current geometry/fold with
  union OOS recall `0.493333`.
- Retained-OOS expansion matrix: all 40 current-retained OOS rows are emitted;
  PQQ+NAD positives are `m_csa:104` and `m_csa:464`, while the
  approval-qualified Fe-S/iron context adds `m_csa:119`.
- Fe-S/iron remains the next support gap: approval-qualified
  `PQQ + NAD + Fe-S/iron` catches 3 current-retained OOS rows
  (`m_csa:104`, `m_csa:119`, `m_csa:464`) with 0 current-primary positives,
  but `m_csa:119` remains research-only until the bundle-ready Fe-S/iron
  support subset is approved/imported.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, heldout splits, or Lever
  3 files changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names,
  accessions, PDB IDs, coordinate paths, or provenance were used as predictive
  feature values. Forbidden row-specific feature-key audit found 0 hits.
- The new readout remains research-only. It emits measured source-free feature
  rows and retained-OOS accounting but does not approve, import, or promote
  any direct electron-flow contract.
- Disk guardrail ended at 13 GiB free.

#### Validation

- Focused new-readout tests:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::CliTests::test_lever2_electron_flow_current_split_smoke_materialization_parser_defaults tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_current_split_smoke_materialization_readout tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_current_split_smoke_materialization_current_counts -q`:
  3 passed.
- Touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  485 passed, 193 subtests passed.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q`: 1562 passed, 212 subtests passed,
  with the existing sklearn/SciPy L-BFGS-B deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests -q`: 1517 tests OK,
  with the same existing warning.
- `PYTHONPATH=src python -m compileall -q src tests`: passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 mechanism ontology families, and 702 curated
  labels validated.
- `git diff --check`: passed.
- Repo JSON/JSONL parse sweep: 3591 JSON files and 27 JSONL files parsed with
  0 errors.
- New artifact regeneration/source audit passed after normalizing
  `created_utc`; all 3 source artifacts hash-current.
- New artifact forbidden predictive-key audit found 0 hits inside
  `row_specific_event_features`; protected-surface path audit found 8 expected
  changed paths and 0 protected-surface violations.

#### Commit/push status

- Primary research commit
  `c4e483ed3c62bb777c144773cf4b49a902ba2aee`
  (`Add Lever 2 electron-flow smoke materialization readout`) was pushed to
  `origin/lever-2-research-track`.
- Fetch/sync verification after the push matched local `HEAD` and
  `origin/lever-2-research-track` at
  `c4e483ed3c62bb777c144773cf4b49a902ba2aee`.
- This final handoff status update is being committed and pushed separately as
  a handoff-only wrap-up change.

#### Exact next action

- Treat the `m_csa:104` plus 34-primary source-free electron-flow smoke
  tranche as materialized and use the 74-row PQQ+NAD expansion in
  `artifacts/v3_lever2_source_free_electron_flow_current_split_smoke_materialization_readout_current702_20260605.json`
  as the current measured baseline.
- Next electron-flow experiment: approve/import the bundle-ready source-free
  Fe-S/iron support subset (`m_csa:127`, `m_csa:281`) with
  `predictive_use_allowed=true` and explicit train/cal split assignment, then
  rerun the fixed approval-qualified `PQQ + NAD + Fe-S/iron` union without
  threshold changes or heldout use. If the approval contract requires the
  original 3-row tiny tranche, first repair `m_csa:443` accession-compatible
  role-graph sequence-position evidence.

### 2026-06-05 Lever 2 Research Run 22

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T12:34:49Z`
- STARTED_LOCAL: `2026-06-05T07:34:49-0500 CDT`
- ENDED_AT: `2026-06-05T13:29:54Z`
- ENDED_LOCAL: `2026-06-05T08:29:54-0500 CDT`
- ELAPSED_MINUTES: `55.1`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Start from the measured projection-backed `PQQ + NAD-family` supported route
and approval-qualified Fe-S/iron union, then attempt the next source-free
electron-flow measured readout that can test incremental operating-point value
without labels, registry edits, threshold changes, heldout tuning, or Lever 3
work.

#### Work log

- Run opened in the dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from Lever 3.
- The automation initially started in a clean detached duplicate checkout
  `/Users/vivekvardhanarrabelli/.codex/worktrees/c6ec/catalytic-earth` with
  disk at 9.0 GiB free, below the 10 GiB guardrail. That duplicate checkout had
  no branch and no local changes, so it was removed with `git worktree remove`
  after switching all substantive work to the Lever 2 branch worktree. Disk
  then returned to 12 GiB free.
- Added
  `build-lever2-source-free-electron-flow-iron-sulfur-tiny-tranche-approval-readiness-readout`.
  This consumes the measured Fe-S/iron projection-support readout, the
  approval-qualified Fe-S union readout, the review-only Fe-S locus sidecar,
  the train/cal input manifest, the current train/cal feature sidecar, and the
  active-site role-graph sidecar.
- The readout measures whether the smallest Fe-S support tranche can make the
  current-split Fe-S OOS catch consumable without editing imports, labels,
  registries, ontologies, production thresholds, heldout splits, or predictive
  gates.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_iron_sulfur_tiny_tranche_approval_readiness_readout_current702_20260605.json`
  and
  `work/lever2_source_free_electron_flow_iron_sulfur_tiny_tranche_approval_readiness_readout_current702_20260605.md`.
- Expanded the smoke tranche accounting from the 3-row tiny support set to the
  12-row non-current Fe-S support set so the next approval tranche has both the
  smallest route and a larger source-free positive fallback.
- Added accession-position counts from the role-graph sidecar so the
  `m_csa:443` minimal-bundle gap is explicit in the artifact/report rather
  than only described as a generic role-graph failure.
- No blocker packet was written; the run produced a measured electron-flow
  readout first and continued through expanded-tranche and role-graph evidence
  checks.

#### Measured results

- Status:
  `lever2_source_free_electron_flow_iron_sulfur_tiny_tranche_approval_readiness_readout_research_only_tiny_tranche_source_free_positive_partial_bundle_ready_pending_predictive_gate`.
  Result class:
  `research_only_tiny_tranche_source_free_positive_partial_bundle_ready_pending_predictive_gate`.
- Tiny Fe-S support tranche: 3/3 rows are source-free complete and positive
  (`m_csa:443`, `m_csa:127`, `m_csa:281`), all 3 are nonheldout
  in-distribution rows, and 0/3 are currently `predictive_use_allowed` or
  present in the approved current train/cal feature sidecar.
- Tiny-tranche bundle readiness: 2/3 rows are minimal-bundle ready and
  accession-compatible (`m_csa:127`, `m_csa:281`). `m_csa:443` is blocked by
  `minimal_train_cal_feature_bundle_ready=false` and
  `accession_compatible_sequence_positions=false`; its role graph has accession
  `P13063` but sequence-position evidence split across `P13063:12` and
  `P13065:7`.
- Expanded non-current Fe-S tranche: 12/12 rows are source-free positive, and
  8/12 are bundle-ready/accession-compatible:
  `m_csa:127`, `m_csa:281`, `m_csa:130`, `m_csa:398`, `m_csa:358`,
  `m_csa:108`, `m_csa:562`, and `m_csa:276`. The expanded rows blocked by
  minimal-bundle/accession evidence are `m_csa:443`, `m_csa:208`,
  `m_csa:123`, and `m_csa:212`.
- Approval-qualified current-split context is unchanged but now has a precise
  support-readiness gate: supported-now `PQQ + NAD-family` catches 2
  current-retained OOS rows (`m_csa:104`, `m_csa:464`), while the
  approval-qualified `PQQ + NAD + Fe-S/iron` union catches 3
  current-retained OOS rows (`m_csa:104`, `m_csa:119`, `m_csa:464`) with 0
  current-primary positives and primary retain recall `1.0`.
- Fe-S/iron adds exactly 1 current-retained OOS row beyond supported PQQ+NAD:
  `m_csa:119`. The incremental OOS abstain-recall delta beyond PQQ+NAD is
  `0.013333` on the current geometry/fold OOS denominator.
- Decision: `m_csa:119` can join the supported route after the bundle-ready
  source-free Fe-S support subset is approved/imported, but train/cal support
  and deployment remain false now because the support rows have not been
  approved for predictive use or imported into the train/cal feature sidecar.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, heldout splits, or Lever 3
  files changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- Tiny and expanded Fe-S support rows were used only for train/cal/nonheldout
  support-readiness accounting; none were promoted or made predictive.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, accessions,
  PDB IDs, coordinate paths, or provenance were used as predictive feature
  values. Accessions and coordinate/provenance fields appear only outside
  `row_specific_event_features` as source-evidence accounting.
- The new readout remains research-only. No threshold was selected, tuned, or
  promoted by this run.
- Disk guardrail recovered from the initial detached-worktree low-disk state
  and ended at 12 GiB free.

#### Validation

- Focused new-readout tests:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::CliTests::test_lever2_electron_flow_iron_sulfur_tiny_tranche_approval_readiness_parser_defaults tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_iron_sulfur_tiny_tranche_approval_readiness_readout tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_iron_sulfur_tiny_tranche_approval_readiness_current_counts -q`:
  3 passed.
- Touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  482 passed, 193 subtests passed.
- Compile check: `PYTHONPATH=src python -m compileall -q src tests`: passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 mechanism ontology families, and 702 curated
  mechanism labels validated.
- `git diff --check`: passed.
- Full pytest: `PYTHONPATH=src python -m pytest -q`: 1559 passed, 212
  subtests passed, with the existing sklearn/SciPy deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests -q`: 1514 tests OK,
  with the same existing warning.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- Repo JSON/JSONL parse sweep passed: 3590 JSON files and 27 JSONL files
  parsed with 0 errors.
- New artifact source hash audit passed for all 6 source artifacts, including
  the role-graph sidecar.
- New artifact regeneration/source audit passed after normalizing
  `created_utc`.
- New artifact forbidden predictive-key audit found 0 hits inside
  `row_specific_event_features`.
- Scope audit found 8 expected changed paths and 0 protected-surface path
  changes.

#### Commit/push status

- Primary research commit
  `96abbfb2f4eab0523f2dafbddebc48592f25cb18`
  (`Add Lever 2 Fe-S approval readiness readout`) was pushed to
  `origin/lever-2-research-track`.
- Fetch/sync verification after the push matched local `HEAD` and
  `origin/lever-2-research-track` at
  `96abbfb2f4eab0523f2dafbddebc48592f25cb18`.
- This final handoff status update is being committed and pushed separately as
  a handoff-only wrap-up change.

#### Exact next action

- Smallest next electron-flow experiment: approve/import the bundle-ready
  source-free Fe-S support subset `m_csa:127` and `m_csa:281` with
  `predictive_use_allowed=true` and explicit train/cal split assignment, then
  rerun the fixed approval-qualified `PQQ + NAD + Fe-S/iron` union without any
  threshold changes or heldout use.
- If the approval contract requires the original 3-row tiny tranche, first
  repair `m_csa:443` by resolving the mixed role-graph sequence-position
  accession evidence (`P13063:12`, `P13065:7`) into accession-compatible
  source-free positions, then import all three tiny rows.
- If a broader support pool is required before approval, use the expanded
  8-row bundle-ready subset:
  `m_csa:127`, `m_csa:281`, `m_csa:130`, `m_csa:398`, `m_csa:358`,
  `m_csa:108`, `m_csa:562`, and `m_csa:276`.

### 2026-06-05 Lever 2 Research Run 21

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T11:32:43Z`
- STARTED_LOCAL: `2026-06-05T06:32:43-0500 CDT`
- ENDED_AT: `2026-06-05T12:26:07Z`
- ENDED_LOCAL: `2026-06-05T07:26:07-0500 CDT`
- ELAPSED_MINUTES: `53.4`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Start from the measured direct source-free electron-flow readouts and test the
smallest train/cal-disciplined route that can add Fe-S/iron support without
editing labels, registries, imports, production thresholds, or heldout splits.

#### Work log

- Run opened in the existing dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from Lever 3. Disk stayed above the
  10 GiB guardrail at 12 GiB free.
- Added
  `build-lever2-source-free-electron-flow-iron-sulfur-approval-qualified-union-readout`.
  This consumes the projection-backed `PQQ + NAD-family` sidecar, the relaxed
  non-PQQ direct sidecar, and the Fe-S/iron projection-support readout, then
  measures the supported-now route against an approval-qualified
  `PQQ + NAD + Fe-S/iron` union on the same 74-row current split.
- The readout also emits fixed family-ablation gates for PQQ-only, NAD-only,
  and Fe-S/iron-only direct source-free electron-flow fields so the Fe-S
  contribution is measured as a distinct component rather than only as a union
  side effect.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_iron_sulfur_approval_qualified_union_readout_current702_20260605.json`
  and
  `work/lever2_source_free_electron_flow_iron_sulfur_approval_qualified_union_readout_current702_20260605.md`.
- No blocker packet was written; the run produced a measured readout first and
  continued into component ablation plus source-chain validation.

#### Measured results

- Approval-qualified union status:
  `lever2_source_free_electron_flow_iron_sulfur_approval_qualified_union_readout_research_only_approval_qualified_iron_sulfur_adds_incremental_signal_pending_feature_sidecar_approval`.
  Result class:
  `research_only_approval_qualified_iron_sulfur_adds_incremental_signal_pending_feature_sidecar_approval`.
- Supported-now projection-backed `PQQ + NAD-family` direct route remains
  complete on 74/74 current-split rows, preserves primary retention with 0/34
  primary positives, and catches 2/40 current-retained OOS rows:
  `m_csa:104` and `m_csa:464`.
- Approval-qualified `PQQ + NAD + Fe-S/iron` union is complete on 74/74 rows,
  preserves primary retention with 0/34 primary positives, and catches 3/40
  current-retained OOS rows: `m_csa:104`, `m_csa:119`, and `m_csa:464`.
  Retained-OOS abstain recall is 0.075, incremental OOS recall vs current
  geometry/fold is 0.04, and union OOS recall is 0.506667.
- Fe-S/iron adds exactly 1 current-retained OOS row beyond supported PQQ+NAD:
  `m_csa:119`. The incremental OOS recall delta beyond PQQ+NAD is 0.013333
  vs the current geometry/fold OOS denominator.
- Family ablation measured three distinct primary-safe components:
  PQQ-only catches `m_csa:104`, NAD-only catches `m_csa:464`, and
  Fe-S/iron-only catches `m_csa:119`; all three component gates have 0 current
  primary positives.
- The tiny Fe-S/iron projection tranche remains 3/3 source-free positive
  (`m_csa:127`, `m_csa:281`, `m_csa:443`) and the expanded non-current
  tranche remains 12/12 source-free positive.
- Interpretation: `m_csa:119` can join the supported direct electron-flow
  route after the tiny Fe-S/iron projection tranche is approved/imported, but
  it is not train/cal-supported now because those support rows still have
  `predictive_use_allowed=false` and are not in an approved train/cal feature
  sidecar.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, heldout splits, or Lever 3
  files changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- The Fe-S support rows used in the tiny approval-qualified tranche are
  nonheldout/in-distribution but remain non-consumable because
  `predictive_use_allowed=false`.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, accessions,
  PDB IDs, or coordinate paths were used as predictive feature values. Entry
  IDs and source paths appear only outside `row_specific_event_features` for
  tranche/source-evidence accounting.
- The new approval-qualified union remains research-only and unapproved. No
  threshold was selected, tuned, or promoted by this run.

#### Validation

- Focused new-readout tests:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::CliTests::test_lever2_electron_flow_iron_sulfur_approval_qualified_union_parser_defaults tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_iron_sulfur_approval_qualified_union_readout tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_iron_sulfur_approval_qualified_union_readout_current_counts -q`:
  3 passed.
- Touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  479 passed, 193 subtests passed.
- Compile check:
  `PYTHONPATH=src python -m compileall -q src/catalytic_earth/lever2_mechanism_incremental_readout.py src/catalytic_earth/cli.py tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py`:
  passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 ontology families, and 702 curated labels
  validated.
- `git diff --check`: passed.
- Full pytest: `PYTHONPATH=src python -m pytest -q`: 1556 passed, 212 subtests
  passed, with the existing sklearn/SciPy deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests`: 1511 tests OK, with
  the same existing warning.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- Repo JSON/JSONL parse sweep passed: 3589 JSON files and 27 JSONL files parsed
  with 0 errors.
- New artifact regeneration/source audit passed after normalizing `created_utc`.
- Source-chain temporary regeneration passed for the direct electron-flow chain:
  PQQ 1 OOS catch, relaxed non-PQQ 2, combined direct 3, supported PQQ+NAD 2,
  Fe-S tiny projection 3/3, and approval-qualified union 3.
- New artifact source hash audit passed for all three source artifacts.
- New artifact feature-key guardrail audit found 0 forbidden keys across 74
  approval-qualified feature rows; repo-wide electron-flow artifact inventory
  found 14 electron-flow artifacts and 0 forbidden row-feature key hits.
- Scope audit found 0 protected-surface path changes.

#### Commit/push status

- Primary research commit
  `0ab17f087570112191bf1441ceaaa4082780f7e1`
  (`Add Lever 2 Fe-S electron-flow union readout`) was pushed to
  `origin/lever-2-research-track`.
- Fetch/sync verification after the push matched local `HEAD` and
  `origin/lever-2-research-track` at
  `0ab17f087570112191bf1441ceaaa4082780f7e1`.
- This final handoff status update is being committed and pushed separately as
  a handoff-only wrap-up change.

#### Exact next action

- Keep projection-backed `PQQ + NAD-family` as the supported measured route for
  now. The exact next Fe-S/iron action is approval/import of the 3-row tiny
  projection tranche (`m_csa:127`, `m_csa:281`, `m_csa:443`) into the
  train/cal source-free feature sidecar with `predictive_use_allowed=true`,
  then rerun the fixed approval-qualified union without threshold changes or
  heldout use to decide whether `m_csa:119` should join the supported route.

### 2026-06-05 Lever 2 Research Run 20

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T10:32:36Z`
- STARTED_LOCAL: `2026-06-05T05:32:36-0500 CDT`
- ENDED_AT: `2026-06-05T11:27:46Z`
- ENDED_LOCAL: `2026-06-05T06:27:46-0500 CDT`
- ELAPSED_MINUTES: `55.2`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Start from the measured combined direct source-free electron-flow sidecar and
try to resolve the remaining Fe-S/iron projection-support gap without editing
labels, registries, imports, production thresholds, or heldout splits.

#### Work log

- Run opened in the dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from Lever 3.
- Initial automation checkout was detached in another worktree; all substantive
  work was performed in the existing Lever 2 branch worktree. Disk stayed above
  the 10 GiB guardrail at 16 GiB free.
- Added
  `build-lever2-source-free-electron-flow-projection-backed-pqq-nad-feature-sidecar-readout`.
  This pulls the nested projection-backed `PQQ + NAD-family` subunion out of
  the combined direct readout and emits it as a standalone normal-shaped
  `row_specific_event_features` sidecar.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_projection_backed_pqq_nad_feature_sidecar_readout_current702_20260605.json`
  and
  `work/lever2_source_free_electron_flow_projection_backed_pqq_nad_feature_sidecar_readout_current702_20260605.md`.
- Added
  `build-lever2-source-free-electron-flow-iron-sulfur-projection-support-readout`.
  This measures the Fe-S/iron current-split family gate, the existing 43-row
  projection attempt, the non-heldout review-only iron-sulfur locus support
  pool, a 3-row tiny materialization tranche, and the expanded 12-row
  non-current materialization tranche.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_iron_sulfur_projection_support_readout_current702_20260605.json`
  and
  `work/lever2_source_free_electron_flow_iron_sulfur_projection_support_readout_current702_20260605.md`.

#### Measured results

- Projection-backed `PQQ + NAD-family` standalone sidecar status:
  `lever2_source_free_electron_flow_projection_backed_pqq_nad_feature_sidecar_readout_research_only_projection_backed_pqq_nad_operating_point_signal`.
  Result class:
  `research_only_projection_backed_pqq_nad_operating_point_signal`.
- Projection-backed sidecar rows are complete on 74/74 current-split rows,
  preserve primary retention with 0/34 primary positives, and catch 2/40
  current-retained OOS rows: `m_csa:104` through fixed PQQ donor/acceptor
  contact and `m_csa:464` through fixed 8 A NAD-family donor/acceptor distance.
  Retained-OOS abstain recall is 0.05, incremental OOS recall beyond current
  geometry/fold is 0.026667, and union OOS recall is 0.493333.
- Projection support for the standalone `PQQ + NAD-family` route remains
  train/cal positive through `m_csa:59` and `m_csa:256`; the unsupported
  Fe-S/iron positive `m_csa:119` is intentionally excluded from this supported
  route.
- Fe-S/iron projection-support readout status:
  `lever2_source_free_electron_flow_iron_sulfur_projection_support_readout_research_only_iron_sulfur_current_split_signal_tiny_materialization_support_gap`.
  Result class:
  `research_only_iron_sulfur_current_split_signal_tiny_materialization_support_gap`.
- The Fe-S/iron family gate remains measurable and primary-safe on the current
  split: 74/74 rows complete, 0/34 current primary positives, 1/40
  current-retained OOS positive (`m_csa:119`), retained-OOS abstain recall
  0.025, incremental OOS recall 0.013333, and union OOS recall 0.48.
- Existing approved/consumable train/cal projection support for Fe-S/iron is
  still absent: the existing 43-row projection attempt is 43/43 complete with
  0 positive rows.
- Non-heldout review-only iron-sulfur locus evidence exists outside the current
  split: 12 non-current proximal rows after excluding 140 heldout rows from the
  support scan. Predictive-use-allowed proximal rows remain 0.
- The tiny 3-row Fe-S/iron materialization tranche
  (`m_csa:443`, `m_csa:127`, `m_csa:281`) is 3/3 complete and 3/3 positive in
  research-only source-free coordinate fields; positive IDs sort as
  `m_csa:127`, `m_csa:281`, `m_csa:443`.
- The expanded 12-row non-current Fe-S/iron materialization tranche is 12/12
  complete and 12/12 positive:
  `m_csa:108`, `m_csa:123`, `m_csa:127`, `m_csa:130`, `m_csa:208`,
  `m_csa:212`, `m_csa:276`, `m_csa:281`, `m_csa:358`, `m_csa:398`,
  `m_csa:443`, and `m_csa:562`.
- Interpretation: Fe-S/iron source-free evidence can now be materialized in
  research-only mode, but it still cannot be counted as train/cal support
  because the rows remain outside the approved train/cal feature sidecar and
  `predictive_use_allowed` is false. The supported measured route remains
  projection-backed `PQQ + NAD-family` until the Fe-S/iron tiny tranche is
  approved/imported and rerun.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, heldout splits, or Lever 3
  files changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated. Heldout
  rows in the iron-sulfur locus sidecar were excluded from the support scan
  before materialization.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, accessions,
  PDB IDs, or coordinate paths were used as predictive feature values. Entry IDs
  and coordinate paths appear only outside `row_specific_event_features` for
  tranche/source-evidence accounting.
- The `PQQ + NAD-family`, Fe-S/iron tiny, and Fe-S/iron expanded surfaces remain
  research-only and unapproved/unimported. No threshold was selected or
  promoted by this run.

#### Validation

- Focused tests for the two new readouts and parser defaults: 6 passed.
- Touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  476 passed, 193 subtests passed.
- `PYTHONPATH=src python -m compileall -q src/catalytic_earth/lever2_mechanism_incremental_readout.py src/catalytic_earth/cli.py tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py`:
  passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 ontology families, and 702 curated labels
  validated.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- Repo JSON/JSONL parse sweep passed: 3588 JSON files and 27 JSONL files parsed
  with 0 errors.
- New artifact regeneration/source audit passed for both new artifacts after
  normalizing `created_utc`.
- New artifact feature-key guardrail audit found 0 forbidden keys across 74
  projection-backed `PQQ + NAD-family` feature rows and 15 Fe-S/iron
  materialization feature rows.
- `git diff --check`: passed.
- Full pytest on the final expanded Fe-S artifact state:
  `PYTHONPATH=src python -m pytest -q`: 1553 passed, 212 subtests passed, with
  the existing sklearn/SciPy deprecation warning.
- Full unittest discovery on the final expanded Fe-S artifact state:
  `PYTHONPATH=src python -m unittest discover -s tests`: 1508 tests OK, with
  the same existing warning.

#### Commit/push status

- Primary research commit
  `0a9635ea0e7359fe5b610189f2db90dbfd9cc910`
  (`Add Lever 2 electron-flow support readouts`) was pushed to
  `origin/lever-2-research-track`.
- Sync verification after that push matched local `HEAD` and
  `origin/lever-2-research-track` at
  `0a9635ea0e7359fe5b610189f2db90dbfd9cc910`.
- The final ledger/status update was committed and pushed as a handoff-only
  wrap-up change; final fetch verification matched local `HEAD` and
  `origin/lever-2-research-track`.

#### Exact next action

- Keep the projection-backed `PQQ + NAD-family` sidecar as the supported
  research-only Lever 2 electron-flow route for now. The exact next Fe-S/iron
  action is approval/import of the 3-row tiny materialized projection tranche
  (`m_csa:443`, `m_csa:127`, `m_csa:281`) into the train/cal source-free
  feature sidecar, then rerun the same Fe-S/iron family gate without threshold
  changes or heldout use to decide whether `m_csa:119` can join the supported
  route.

### 2026-06-05 Lever 2 Research Run 19

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T08:38:48Z`
- STARTED_LOCAL: `2026-06-05T03:38:48-0500 CDT`
- ENDED_AT: `2026-06-05T09:36:52Z`
- ENDED_LOCAL: `2026-06-05T04:36:52-0500 CDT`
- ELAPSED_MINUTES: `58.07`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Start from the materialized source-free PQQ donor/acceptor feature sidecar and
attempt the smallest train/cal-disciplined relaxed non-PQQ electron-flow
distance readout that can preserve the 34 current primary retention-gate rows.

#### Work log

- Run opened in the dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from Lever 3.
- Initial automation checkout was detached and disk was below the 10 GiB
  guardrail at 9.1 GiB free. Removed three clean stale detached worktrees,
  restoring disk to 20 GiB free before substantive work.
- Wrap-up disk check showed 19 GiB free.
- Added
  `build-lever2-source-free-electron-flow-relaxed-non-pqq-donor-acceptor-feature-sidecar-readout`.
  This formalizes the prior scout into a fixed 8 A source-free non-PQQ
  donor/acceptor distance readout over NAD-family, Fe-S/iron-family, and other
  non-PQQ redox-center atoms while excluding heme, flavin, and PQQ from the
  feature contract.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_relaxed_non_pqq_donor_acceptor_feature_sidecar_readout_current702_20260605.json`
  and
  `work/lever2_source_free_electron_flow_relaxed_non_pqq_donor_acceptor_feature_sidecar_readout_current702_20260605.md`.
- Added
  `build-lever2-source-free-electron-flow-combined-direct-feature-sidecar-readout`.
  This consumes the measured PQQ donor/acceptor sidecar and the fixed relaxed
  non-PQQ sidecar, then remeasures both the broad combined direct
  electron-flow union and a projection-backed `PQQ + NAD-family` subunion.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_combined_direct_feature_sidecar_readout_current702_20260605.json`
  and
  `work/lever2_source_free_electron_flow_combined_direct_feature_sidecar_readout_current702_20260605.md`.
- Tightened the combined direct readout to report the mandated smallest smoke
  tranche explicitly: `m_csa:104` plus the 34 current primary retention-gate
  rows. The smoke gate is measured separately inside the combined artifact
  before the full retained-OOS current-split tranche.

#### Measured results

- Fixed relaxed non-PQQ donor/acceptor sidecar status:
  `lever2_source_free_electron_flow_relaxed_non_pqq_donor_acceptor_feature_sidecar_readout_research_only_fixed_relaxed_non_pqq_distance_operating_point_signal`.
  Result class:
  `research_only_fixed_relaxed_non_pqq_distance_operating_point_signal`.
- Fixed relaxed non-PQQ sidecar rows are complete on 74/74 current-split rows,
  preserve primary retention with 0/34 primary positives and primary retain
  recall 1.0, and catch 2/40 current-retained OOS rows:
  `m_csa:119` (Fe-S/iron, minimum distance 5.054 A) and `m_csa:464`
  (NAD-family, minimum distance 5.527 A). Retained-OOS abstain recall is 0.05,
  incremental OOS recall beyond current geometry/fold is 0.026667, and union
  OOS recall is 0.493333.
- Projection scout for the same fixed relaxed non-PQQ contract is complete on
  43/43 train/cal projection rows and has 2 calibration positives:
  `m_csa:59` and `m_csa:256`, both NAD-family. There are 0 train positives.
- Family split at the same fixed 8 A contract: `nad_family_only` has both
  current-split signal (`m_csa:464`) and projection support
  (`m_csa:59`, `m_csa:256`); `iron_sulfur_or_iron_only` has current-split
  signal (`m_csa:119`) but no positive train/cal projection rows and no finite
  Fe-S/iron projection distance examples in the available train/cal geometry;
  `other_non_pqq_only` has no signal.
- Combined direct electron-flow sidecar status:
  `lever2_source_free_electron_flow_combined_direct_feature_sidecar_readout_research_only_combined_direct_electron_flow_operating_point_signal`.
  Result class:
  `research_only_combined_direct_electron_flow_operating_point_signal`.
- Combined smoke tranche is complete on 35/35 rows (`m_csa:104` plus 34
  current primary rows), has 0/34 primary positives, catches `m_csa:104` as
  1/1 retained-OOS smoke row, and preserves primary retention.
- Combined direct source-free sidecar rows are complete on 74/74 current-split
  rows, preserve primary retention with 0/34 primary positives and catch 3/40
  current-retained OOS rows: `m_csa:104` from PQQ donor/acceptor,
  `m_csa:119` from Fe-S/iron relaxed non-PQQ, and `m_csa:464` from NAD-family
  relaxed non-PQQ. Retained-OOS abstain recall is 0.075, incremental OOS
  recall beyond current geometry/fold is 0.04, and union OOS recall is
  0.506667.
- Projection-backed `PQQ + NAD-family` subunion excludes the unsupported
  Fe-S/iron row and still preserves primary retention with 0/34 primary
  positives while catching 2/40 retained-OOS rows (`m_csa:104`, `m_csa:464`).
  Retained-OOS abstain recall is 0.05, incremental OOS recall is 0.026667, and
  union OOS recall is 0.493333.
- Exact row-feature-key guardrails found 0 forbidden keys in both new
  `row_specific_event_features` surfaces; source artifacts are present and the
  new artifacts regenerate identically after normalizing `created_utc`.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, heldout splits, or Lever 3
  files changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, accessions,
  PDB IDs, or coordinate paths were used as predictive feature values. Entry IDs
  and coordinate paths appear only outside `row_specific_event_features` for
  tranche/source-evidence accounting.
- The fixed 8 A distance contract and family split remain research-only and
  unapproved/unimported. No threshold was selected or promoted by this run.

#### Validation

- Focused parser/builder/regression tests for the two new readouts:
  6 passed.
- Touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  470 passed, 193 subtests passed.
- `PYTHONPATH=src python -m compileall -q src/catalytic_earth/lever2_mechanism_incremental_readout.py src/catalytic_earth/cli.py tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py`:
  passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 ontology families, and 702 curated labels
  validated.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- `git diff --check`: passed.
- Repo JSON/JSONL parse sweep passed: 3586 JSON files and 27 JSONL files parsed
  with 0 errors.
- New artifact exact feature-key/source/regeneration audit passed for both
  relaxed non-PQQ and combined direct electron-flow artifacts after normalizing
  `created_utc`.
- Full pytest after final artifact/source update:
  `PYTHONPATH=src python -m pytest -q`: 1547 passed, 212 subtests passed, with
  the existing sklearn/SciPy deprecation warning.
- Full unittest discovery after final artifact/source update:
  `PYTHONPATH=src python -m unittest discover -s tests`: 1502 tests OK, with
  the same existing warning.

#### Commit/push status

- Committed on `lever-2-research-track` and pushed to
  `origin/lever-2-research-track`; sync verified after push.

#### Exact next action

- Keep all outputs research-only. The next Lever 2 electron-flow action is to
  decide whether the fixed 8 A relaxed non-PQQ contract is acceptable as one
  primitive. If too broad, keep the projection-backed `PQQ + NAD-family`
  subunion as the supported measured route and run the smallest Fe-S/iron
  source-free train/cal evidence experiment needed to support or reject
  `m_csa:119`.

### 2026-06-05 Lever 2 Research Run 18

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T07:32:31Z`
- STARTED_LOCAL: `2026-06-05T02:32:31-0500 CDT`
- ENDED_AT: `2026-06-05T08:28:22Z`
- ENDED_LOCAL: `2026-06-05T03:28:22-0500 CDT`
- ELAPSED_MINUTES: `55.85`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Start from the measured direct source-free PQQ donor/acceptor result and close
the remaining current-split feature-row materialization gap without approving,
importing, or promoting the primitive.

#### Work log

- Continued in the dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from Lever 3.
- Initial automation checkout was detached and disk was below the 10 GiB
  guardrail at 9.5 GiB free. Removed one clean stale detached worktree,
  `/Users/vivekvardhanarrabelli/.codex/worktrees/2e22/catalytic-earth`,
  restoring disk to 13 GiB free before substantive work. Wrap-up disk check
  showed 12 GiB free.
- Added
  `build-lever2-source-free-electron-flow-pqq-donor-acceptor-current-split-feature-sidecar-readout`.
  The readout consumes the measured donor/acceptor contact artifact, emits
  standalone normal-shaped `feature_rows` for the 34 current primary rows and
  40 current-retained OOS rows, and remeasures the fixed operating point from
  `row_specific_event_features` instead of from the nested PQQ audit rows.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_pqq_donor_acceptor_current_split_feature_sidecar_readout_current702_20260605.json`
  and
  `work/lever2_source_free_electron_flow_pqq_donor_acceptor_current_split_feature_sidecar_readout_current702_20260605.md`.
- Added a fixed non-PQQ family-exclusion scout over the same measured broad
  donor/acceptor rows, then added a relaxed-distance scout so the next non-PQQ
  route has concrete row/cutoff evidence rather than another broad blocker.

#### Measured results

- Main sidecar readout status:
  `lever2_source_free_electron_flow_pqq_donor_acceptor_current_split_feature_sidecar_readout_research_only_materialized_feature_sidecar_operating_point_signal`.
  Result class:
  `research_only_materialized_feature_sidecar_operating_point_signal`.
- Standalone source-free current-split feature rows are now materialized:
  74/74 rows complete, with four row feature fields:
  `has_electron_transfer_event`, `electron_transfer_count`,
  `has_source_free_pqq_donor_acceptor_contact`, and
  `source_free_pqq_donor_acceptor_contact_count`.
- Fixed feature-sidecar operating point preserves primary retention:
  0/34 current primary positives, primary retain recall 1.0. It catches 1/40
  current-retained OOS rows (`m_csa:104`), retained-OOS abstain recall 0.025,
  incremental OOS recall 0.013333 beyond current geometry/fold OOS, and union
  OOS recall 0.48.
- The positive direct source-free feature row is still `m_csa:104`, supported
  by committed local `artifacts/v3_foldseek_coordinates_1000/pdb_1C9U.cif`
  where PQQ `O5` contacts `ARG 228 NH1` at 2.768 A.
- Exact row-feature-key guardrail found 0 forbidden keys inside
  `row_specific_event_features`; source records were present; critical
  violation total is 0.
- Fixed non-PQQ family-exclusion scout is negative at the 3.2 A
  donor/acceptor contact contract: non-PQQ all-redox leaks into 6 current
  primary rows and catches 0 retained-OOS rows; excluding heme/flavin ligation
  preserves primary retention but catches 0 retained-OOS rows. PQQ-only remains
  the only fixed-contact primary-safe retained-OOS signal.
- Relaxed-distance scout is positive only as scout evidence, not as an approved
  primitive: non-PQQ excluding heme/flavin at 8/12/25 A catches `m_csa:464`
  and `m_csa:119` with 0 current primary positives; NAD-only catches
  `m_csa:464`; Fe-S-only catches `m_csa:119`. Existing train/cal projection
  rows also have NAD/non-PQQ excluding-heme/flavin positives (`m_csa:59` at
  2.884 A and `m_csa:256` at 4.714 A), with `m_csa:256` already noted as a
  marginal electron-flow row in the signature-exclusion readout.
- Classification: the missing current-split source-free feature-row blocker is
  closed for the narrow PQQ donor/acceptor primitive, and the measured readout
  adds operating-point signal while preserving primary retention. The result
  remains research-only because the PQQ donor/acceptor primitive is still
  unapproved/unimported and has no positive PQQ train/cal projection rows. The
  relaxed non-PQQ distance signal is only a next-experiment scout, not a fixed
  donor/acceptor primitive.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, heldout splits, or Lever 3
  files changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, accessions,
  PDB IDs, or coordinate paths were used as predictive feature values. Entry IDs
  and coordinate paths appear only outside `row_specific_event_features` for
  tranche/source-evidence accounting.
- The fixed feature sidecar uses only the already-measured source-free PQQ
  donor/acceptor contact fields and a fixed operating gate. Relaxed non-PQQ
  cutoffs are explicitly scout-only and not selected, tuned, or promoted.

#### Validation

- Generated sidecar readout:
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-source-free-electron-flow-pqq-donor-acceptor-current-split-feature-sidecar-readout`.
- Focused parser/builder tests:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::CliTests::test_lever2_electron_flow_pqq_donor_acceptor_current_split_feature_sidecar_parser_defaults tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_pqq_donor_acceptor_current_split_feature_sidecar_readout -q`:
  2 passed.
- New artifact regression:
  `PYTHONPATH=src python -m pytest tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_pqq_donor_acceptor_current_split_feature_sidecar_readout_current_counts -q`:
  1 passed.
- Touched-file slice after final scout edit:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  464 passed, 193 subtests passed.
- Full pytest after final scout edit:
  `PYTHONPATH=src python -m pytest -q`: 1541 passed, 212 subtests passed, with
  the existing sklearn/SciPy deprecation warning.
- Full unittest discovery after final scout edit:
  `PYTHONPATH=src python -m unittest discover -s tests`: 1496 tests OK, with
  the same existing warning.
- `PYTHONPATH=src python -m compileall -q src/catalytic_earth/lever2_mechanism_incremental_readout.py src/catalytic_earth/cli.py tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py`:
  passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 ontology families, and 702 curated labels
  validated.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- Repo JSON/JSONL parse sweep passed: 3584 JSON files and 27 JSONL files parsed
  with 0 errors.
- New artifact exact source/feature guardrail audit passed: 74 feature rows,
  0 exact forbidden row-feature keys, 0 missing source records, and
  `critical_violation_total=0`.
- New artifact regeneration comparison passed after normalizing `created_utc`.
- `git diff --check`: passed.

#### Commit/push status

- Implementation/readout commit
  `896389c16ee32706242249e164523e0464b8495d` was pushed to
  `origin/lever-2-research-track`. Fetch verification after that push showed
  local `HEAD == origin/lever-2-research-track` at the same hash before this
  final handoff status edit. Final handoff status commit
  `4c90952bf1efa744b867a0ffbf23740bd79c7f84` was then pushed and
  fetch-verified equal to `origin/lever-2-research-track` before this ledger
  correction.

#### Exact next action

- Do not promote yet. The next Lever 2 electron-flow experiment should
  formalize a train/cal-disciplined relaxed non-PQQ distance primitive only if
  the contract can be predeclared without OOS tuning: start with NAD-family
  and Fe-S/iron-family source-free redox-center distance scouts excluding
  heme/flavin generic ligation, use existing projection positives
  `m_csa:59`/`m_csa:256` as train/cal support, and remeasure the 34-primary +
  40 retained-OOS current split with the fixed 8 A scout cutoff reported here.
  If that contract is rejected as too broad, the narrow PQQ donor/acceptor
  sidecar remains the only current primary-safe direct electron-flow feature.

### 2026-06-05 Lever 2 Research Run 17

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T06:33:08Z`
- STARTED_LOCAL: `2026-06-05T01:33:08-0500 CDT`
- ENDED_AT: `2026-06-05T07:29:09Z`
- ENDED_LOCAL: `2026-06-05T02:29:09-0500 CDT`
- ELAPSED_MINUTES: `56.02`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Start from the direct source-free PQQ current-split sidecar result and test the
next smallest atom-level donor/acceptor contact primitive that could separate
electron-flow topology from generic cofactor/redox-center contact while
preserving the current 34-row primary retention gate.

#### Work log

- Run opened in the dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from the active Lever 3 worktree.
- `origin/lever-2-research-track` was synced with local `HEAD`; `origin/main`
  had one newer commit, but this run initially stayed branch-isolated rather
  than rebasing into the active Lever 3 lane.
- Disk was at the 10 GiB guardrail after the previous run. Removed the clean
  stale detached worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/6a70/catalytic-earth`, which
  restored free space above the guardrail before substantive work. Wrap-up disk
  check showed 12 GiB available.
- Added
  `build-lever2-source-free-electron-flow-pqq-donor-acceptor-contact-readout`.
  This readout starts from the prior PQQ primitive-axis audit and asks whether
  the measured PQQ redox-center contact is specifically a fixed PQQ `O4`/`O5`
  to active-site `N`/`O`/`S` donor/acceptor-capable atom contact within a fixed
  3.2 A cutoff.
- Added
  `build-lever2-source-free-electron-flow-donor-acceptor-contact-readout`.
  This is the main measured artifact for the run. It consumes the source-free
  coordinate proxy readout, geometry features, the train/cal projection
  readout, and the existing train/cal feature sidecar. It materializes a direct
  source-free PQQ donor/acceptor candidate field and a research-only broad
  redox-center donor/acceptor control.
- Generated the measured artifacts/reports:
  `artifacts/v3_lever2_source_free_electron_flow_pqq_donor_acceptor_contact_readout_current702_20260604.json`,
  `work/lever2_source_free_electron_flow_pqq_donor_acceptor_contact_readout_current702_20260604.md`,
  `artifacts/v3_lever2_source_free_electron_flow_donor_acceptor_contact_readout_current702_20260605.json`,
  and
  `work/lever2_source_free_electron_flow_donor_acceptor_contact_readout_current702_20260605.md`.
- Added a projection-row donor/acceptor scout and broad-positive family audit
  to identify whether non-PQQ train/cal signal is heme, flavin, NAD, or another
  redox family. The audit is descriptive only; it does not tune thresholds or
  promote/import a feature route.

#### Measured results

- Main donor/acceptor readout status:
  `lever2_source_free_electron_flow_donor_acceptor_contact_readout_research_only_direct_pqq_donor_acceptor_operating_point_signal`.
  Result class: `research_only_direct_pqq_donor_acceptor_operating_point_signal`.
- Fixed direct PQQ donor/acceptor candidate: 35/35 smoke rows complete and
  74/74 full current-split rows complete. Smoke tranche is primary-safe with
  0/34 primary positives and 1/1 retained-OOS positive. Full current split is
  primary-safe with 0/34 primary positives and 1/40 retained-OOS positive
  (`m_csa:104`).
- Full current-split PQQ donor/acceptor operating point preserves primary
  retain recall 1.0, adds retained-OOS abstain recall 0.025, adds incremental
  OOS abstain recall 0.013333 beyond the current geometry/fold OOS surface,
  and yields union-or-gate OOS recall 0.48.
- Positive source-free evidence is the committed local CIF
  `artifacts/v3_foldseek_coordinates_1000/pdb_1C9U.cif`: PQQ `O5` contacts
  `ARG 228 NH1` at 2.768 A in `m_csa:104`.
- The narrow PQQ donor/acceptor comparison artifact is also 74/74 complete,
  primary-safe, and catches the same single row (`m_csa:104`). It adds 0 rows
  beyond the prior PQQ redox-center contact and loses 0 prior PQQ redox-center
  positives.
- Broad redox-center donor/acceptor control is complete on 74/74 rows but is
  not promotable: it hits 6/34 current primary rows and 1/40 retained-OOS rows,
  lowering primary retain recall to 0.823529. Current-split broad positives by
  family are heme 3, flavin 3, and PQQ 1; the retained-OOS gain remains only
  PQQ (`m_csa:104`).
- Organic redox family controls: NAD-family center only preserves primary
  retention but catches no retained-OOS rows; PQQ+NAD preserves primary
  retention but adds no rows beyond PQQ; PQQ+organic non-heme catches
  `m_csa:104` but leaks into 3 primary rows.
- Projection-row scout: 43/43 existing train/cal projection rows are complete
  for both PQQ and broad donor/acceptor measurement. PQQ donor/acceptor has
  0/43 positives. Broad redox donor/acceptor has 6/43 positives, split 3 train
  and 3 calibration, with families heme 3, flavin 2, and NAD 1. This confirms
  train/cal donor/acceptor signal exists outside PQQ, but the current broad
  primitive is primary-unsafe on the current split.
- PQQ cutoff sensitivity scout checked 10 fixed distances. Only one
  current-split PQQ donor/acceptor finite row exists; no audited cutoff adds
  rows beyond the fixed 3.2 A positive while preserving primary retention.
- Classification: measured direct source-free PQQ donor/acceptor fields add
  primary-safe operating-point value beyond the current geometry/fold surface,
  but the route remains research-only because the PQQ donor/acceptor primitive
  contract is unapproved/unimported and has no positive train/cal projection
  rows. Broad non-PQQ evidence exists, but the broad heme/flavin/NAD atomset
  control is not primary-safe.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, heldout splits, or Lever 3
  files changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, accessions,
  or provenance were used as predictive features. Entry IDs and coordinate
  paths were used only for tranche accounting, source-artifact lookup, and
  missing-evidence accounting.
- The new fields use fixed PQQ atom names, fixed broad redox atomsets for
  controls, fixed active-site donor/acceptor atom elements, committed local CIF
  atom sites, and fixed cutoffs. No threshold was selected or tuned.
- `critical_violation_total=0`; all source artifact records are present; exact
  forbidden row-feature-key audit returned 0 hits for both new artifacts.
- `deployable_now=false`; `candidate_direct_electron_flow_sidecar_materialized_by_this_artifact=true`;
  `approved_direct_electron_flow_axis_materialized_by_this_artifact=false`.

#### Validation

- Generated donor/acceptor contact readout:
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-source-free-electron-flow-donor-acceptor-contact-readout`.
- Generated PQQ donor/acceptor comparison readout:
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-source-free-electron-flow-pqq-donor-acceptor-contact-readout`.
- Focused parser/builder/artifact tests:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::CliTests::test_lever2_electron_flow_donor_acceptor_contact_parser_defaults tests/test_cli.py::CliTests::test_lever2_electron_flow_pqq_donor_acceptor_parser_defaults tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_donor_acceptor_contact_readout_controls_broad_redox tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_pqq_donor_acceptor_contact_readout_maps_strict_contact tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_donor_acceptor_contact_readout_current_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_pqq_donor_acceptor_contact_readout_current_counts -q`:
  6 passed.
- Broader touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  461 passed, 193 subtests passed.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q`: 1538 passed, 212 subtests passed, with
  the existing sklearn/SciPy deprecation warning. This was rerun post-push
  after the implementation commit and passed again: 1538 passed, 212 subtests,
  same warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests`: 1493 tests OK, with
  the same existing warning. This was rerun post-push and passed again:
  1493 tests OK, same warning.
- `PYTHONPATH=src python -m compileall -q src/catalytic_earth/lever2_mechanism_incremental_readout.py src/catalytic_earth/cli.py tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py`:
  passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 ontology families, and 702 curated labels
  validated.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- Repo JSON/JSONL parse sweep passed: 3583 JSON files and 27 JSONL files parsed
  with 0 errors.
- New artifact regeneration comparison passed after normalizing `created_utc`
  for both donor/acceptor artifacts.
- New artifact source/guardrail audit passed: 0 bad guardrail flags, 0 missing
  sources, and 0 exact forbidden row-feature keys.
- `git diff --check`: passed.
- Disk remained above the guardrail at 12 GiB free.

#### Commit/push status

- Implementation/readout commit
  `708f76dae5c00ed52f0787ac8036e60bf4a2edac` is pushed to
  `origin/lever-2-research-track` and verified equal to local `HEAD` before
  this handoff-only status commit.
- Handoff status commit `5a984c3d0a0dde930820f989c78ad8a7d88b42f5` was pushed
  to `origin/lever-2-research-track`. Fetch verification after that push showed
  local `HEAD == origin/lever-2-research-track` at the same hash before this
  final ledger edit. Final ledger correction commit is to be pushed after this
  update so the recorded wall clock reflects the actual 55+ minute run.

#### Exact next action

- Decide whether the fixed PQQ `O4`/`O5` to active-site `N`/`O`/`S`
  donor/acceptor contact contract is acceptable as a narrow primitive
  source-free electron-flow subaxis. If yes, materialize the two direct fields
  (`has_electron_transfer_event`, `electron_transfer_count`) in the normal
  train/cal source-free feature sidecar for the 74-row current split and rerun
  the fixed operating-point readout without heldout scoring or threshold
  tuning. If rejected as too narrow, the smallest next electron-flow experiment
  is a non-PQQ donor/acceptor primitive that predeclares how to exclude generic
  heme/flavin active-site ligation controls, because the broad control has
  train/cal positives but fails the primary retention gate.

### 2026-06-05 Lever 2 Research Run 16

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T05:34:30Z`
- STARTED_LOCAL: `2026-06-05T00:34:30-0500 CDT`
- ENDED_AT: `2026-06-05T06:29:33Z`
- ENDED_LOCAL: `2026-06-05T01:29:33-0500 CDT`
- ELAPSED_MINUTES: `55.05`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Start from the prior direct PQQ redox-center candidate and test whether it can
be materialized as a source-free current-split sidecar with measurable
operating-point value beyond the current geometry/fold surface.

#### Work log

- Continued in the dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from the active Lever 3 worktree.
- Fetched `origin` and rebased `lever-2-research-track` onto current
  `origin/main` without conflicts. This rewrote the local branch relative to
  the previous pushed Lever 2 history, so the implementation push needs
  `--force-with-lease`.
- Added
  `build-lever2-source-free-electron-flow-pqq-current-split-sidecar-readout`.
  The readout consumes the PQQ primitive-axis audit, maps complete PQQ
  redox-center contact rows to direct electron-flow fields
  `has_electron_transfer_event` and `electron_transfer_count`, and evaluates a
  fixed binary OR gate on the 34 current primary rows plus 40 current-retained
  OOS rows.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_pqq_current_split_sidecar_readout_current702_20260604.json`
  and
  `work/lever2_source_free_electron_flow_pqq_current_split_sidecar_readout_current702_20260604.md`.
- Added a projection-row scout inside the same readout to test whether the
  narrow PQQ primitive can reproduce the prior train/cal model-style
  electron-flow projection ceiling on the existing 43 train/cal feature-sidecar
  rows. The non-`ok` `m_csa:318` projection row is closed as a complete
  source-free PQQ-negative row using committed geometry ligand inventory
  (`ATP`, `MG`, `GLU`) with no PQQ.
- Kept the run open through a 55.05-minute wall-clock block before final
  handoff/commit/push wrap-up.

#### Measured results

- PQQ current-split sidecar readout status:
  `lever2_source_free_electron_flow_pqq_current_split_sidecar_readout_research_only_direct_pqq_sidecar_operating_point_signal`.
  Result class: `research_only_direct_pqq_sidecar_operating_point_signal`.
- Direct source-free current-split electron-flow rows are complete: 35/35 smoke
  rows and 74/74 full current-split rows.
- Fixed current-split operating point: 0/34 current primary positives and
  1/40 current-retained OOS positive (`m_csa:104`), preserving primary retain
  recall 1.0 and adding retained-OOS abstain recall 0.025. Relative to all 75
  current geometry/fold calibration OOS rows, this is an incremental OOS recall
  of 0.013333 and union-or-gate OOS recall 0.48.
- Positive source-free evidence remains the atom-level PQQ redox-center contact
  in committed local `artifacts/v3_foldseek_coordinates_1000/pdb_1C9U.cif`,
  with PQQ contact count 1.
- Projection-row scout: all 43 existing train/cal projection rows are now
  materializable with the narrow PQQ primitive, but they are 0/43 PQQ-positive.
  This means the narrow PQQ primitive can support the fixed current-split gate,
  but it would not reproduce the prior train/cal electron-flow projection
  ceiling by itself.
- Classification: measured direct source-free PQQ current-split sidecar signal
  exists and adds primary-safe operating-point value beyond the current
  geometry/fold retained surface, but remains research-only. It is not
  deployable because the PQQ/quinone redox-center primitive contract is still
  unapproved/unimported, and the train/cal projection-row scout shows no
  positive PQQ train/cal signal.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, heldout splits, or Lever 3
  files changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, accessions,
  or provenance were used as predictive features. Entry IDs and coordinate
  paths were used only for tranche accounting, source-artifact lookup, and
  missing-evidence accounting.
- The new readout uses fixed PQQ ligand atom names, fixed atom-contact cutoff,
  committed geometry/CIF evidence, and train/cal-only row accounting; it
  performs no downloads/provider calls and no threshold tuning.
- `critical_violation_total=0`; `deployable_now=false`;
  `candidate_direct_electron_flow_sidecar_materialized_by_this_artifact=true`;
  `approved_direct_electron_flow_axis_materialized_by_this_artifact=false`.

#### Validation

- Generated PQQ current-split sidecar readout:
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-source-free-electron-flow-pqq-current-split-sidecar-readout`.
- Focused parser/builder/artifact tests:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::CliTests::test_lever2_electron_flow_pqq_current_split_sidecar_parser_defaults tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_pqq_current_split_sidecar_readout_maps_direct_fields tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_pqq_current_split_sidecar_readout_current_counts -q`:
  3 passed.
- Broader touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  455 passed, 193 subtests passed.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q`: 1532 passed, 212 subtests passed, with
  the existing sklearn/SciPy deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests`: 1487 tests OK, with
  the same existing warning.
- `PYTHONPATH=src python -m compileall -q src/catalytic_earth/lever2_mechanism_incremental_readout.py src/catalytic_earth/cli.py tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py`:
  passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 ontology families, and 702 curated labels
  validated.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- Repo JSON/JSONL parse sweep passed: 3581 JSON files and 27 JSONL files parsed
  with 0 errors.
- New artifact regeneration comparison passed after normalizing `created_utc`.
- New artifact guardrail/source-record audit passed: 0 guardrail violations and
  all source records present.
- `git diff --check`: passed.
- Disk remained above the guardrail at about 14 GiB free.

#### Commit/push status

- Implementation/readout commit
  `64b4f6bd115d7f6b3b5d82936ae42efa695f2bf4` was pushed to
  `origin/lever-2-research-track` with `--force-with-lease` after the branch
  was rebased onto current `origin/main`.
- Fetch verification after the push showed local `HEAD ==
  origin/lever-2-research-track` at
  `64b4f6bd115d7f6b3b5d82936ae42efa695f2bf4` before this handoff-only status
  commit.

#### Exact next action

- If the PQQ/quinone redox-center contract is approved, promote it only as a
  narrow fixed current-split operating-point gate candidate first: it is
  measured source-free and primary-safe, but sparse (1/40 current-retained OOS).
  Do not expect it to reproduce the prior model-style train/cal electron-flow
  projection ceiling because the 43 projection rows are complete but
  PQQ-negative. The next electron-flow experiment should therefore be an
  atom-level donor/acceptor contact primitive that separates electron-flow
  topology from generic cofactor/redox-center contact.

### 2026-06-04 Lever 2 Research Run 15

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T04:31:57Z`
- STARTED_LOCAL: `2026-06-04T23:31:57-0500 CDT`
- ENDED_AT: `2026-06-05T05:27:38Z`
- ENDED_LOCAL: `2026-06-05T00:27:38-0500 CDT`
- ELAPSED_MINUTES: `55.68`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Start from the measured coordinate-only PQQ smoke signal and test whether the
PQQ/quinone coordinate subfield can be promoted from proxy evidence to a
source-free primitive electron-flow axis while preserving primary retention.

#### Work log

- Continued in the dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from the active Lever 3 worktree. Fetched
  `origin`, found `origin/main` had advanced by two Lever 3 commits, and
  rebased the Lever 2 branch onto current `origin/main` without conflicts.
- Added
  `build-lever2-source-free-electron-flow-pqq-primitive-axis-audit`. The readout
  consumes the coordinate-proxy readout and `artifacts/v3_geometry_features_1025.json`,
  materializes a candidate direct source-free PQQ/quinone redox-center contact
  field using fixed PQQ atom names (`C4`, `C5`, `O4`, `O5`), committed local
  CIF atom sites, active-site atom contacts, and a fixed 4.0 A atom-contact
  cutoff.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_pqq_primitive_axis_audit_current702_20260604.json`
  and
  `work/lever2_source_free_electron_flow_pqq_primitive_axis_audit_current702_20260604.md`.
- Expanded the 74-row retained-OOS current split inside the readout. The two
  non-`ok` coordinate rows from the prior run remain closed as source-free
  PQQ-negative rows through the committed CIF gap inventory; rows without
  proximal PQQ are carried as complete source-free negatives.
- Added a research-only union control that combines the direct PQQ redox-center
  contact field with the prior primary-safe generic coordinate redox-contact
  count threshold. This control is explicitly not treated as a primitive axis.
- Tried an alternate broader direct atom-level redox-center route using fixed
  redox-center atom sets for PQQ, FAD/FMN, NAD-family ligands, heme, and Fe-S
  clusters on the generic redox positives. At a fixed 4.0 A contact cutoff it
  hit 8/34 primary retention-gate rows and only `m_csa:104` among retained OOS,
  so it was not promoted or committed as a feature route.
- Kept the run open to a 55.68-minute wall-clock block before wrap, then
  rechecked disk and branch status.

#### Measured results

- PQQ primitive-axis audit status:
  `lever2_source_free_electron_flow_pqq_primitive_axis_audit_research_only_pqq_redox_center_candidate_axis_signal`.
  Result class: `research_only_pqq_redox_center_candidate_axis_signal`.
- The candidate direct PQQ redox-center fields are complete on the smoke tranche
  and the full 74-row retained-OOS current split: 35/35 smoke rows and 74/74
  full current-split rows complete.
- Smoke operating point: 0/34 primary positives and 1/1 retained-OOS positive
  (`m_csa:104`), preserving primary retain recall 1.0 and yielding smoke OOS
  abstain recall 1.0.
- Full retained-OOS current split: 0/34 primary positives and 1/40 retained-OOS
  positives (`m_csa:104`), preserving primary retain recall 1.0 and adding a
  sparse OOS abstain recall 0.025 beyond the current geometry/fold surface.
- Atom-level evidence for the positive row: committed local
  `artifacts/v3_foldseek_coordinates_1000/pdb_1C9U.cif` contains PQQ redox-center
  atoms with a minimum PQQ-center-to-active-site atom distance of 2.768 A
  (`O5` to `ARG 228 NH1`).
- Research-only union control: PQQ redox-center contact OR the prior
  primary-safe generic redox-contact count threshold catches 3/40 retained-OOS
  rows (`m_csa:104`, `m_csa:368`, `m_csa:464`) with 0 primary positives, OOS
  recall 0.075. This is not an approved primitive axis because the generic-count
  side remains a coordinate proxy control.
- Broader direct atomset alternate probe was negative for preservation: fixed
  broad redox-center atom contacts hit 8/34 primary retention-gate rows
  (`m_csa:973`, `m_csa:399`, `m_csa:800`, `m_csa:277`, `m_csa:879`, `m_csa:319`,
  `m_csa:694`, `m_csa:473`) and only `m_csa:104` among retained OOS.
- Classification: measured source-free direct PQQ redox-center candidate signal
  exists and adds primary-safe operating-point value, but remains research-only.
  It is not deployable yet because the PQQ/quinone redox-center contract has not
  been explicitly approved/imported as a primitive source-free electron-flow
  axis.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, heldout splits, or Lever 3
  files changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, accessions,
  or provenance were used as predictive features. Entry IDs and coordinate paths
  were used only for tranche accounting, source-artifact lookup, and missing
  evidence accounting.
- The new readout uses fixed PQQ ligand atom names and active-site atom
  contacts from committed local CIF sidecars; it performs no downloads/provider
  calls and no threshold tuning.
- `critical_violation_total=0`; `deployable_now=false`;
  `approved_direct_electron_flow_axis_materialized_by_this_artifact=false`;
  `candidate_direct_electron_flow_fields_materialized_by_this_artifact=true`.

#### Validation

- Generated PQQ primitive-axis audit:
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-source-free-electron-flow-pqq-primitive-axis-audit`.
- Focused parser/builder/artifact tests:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::CliTests::test_lever2_electron_flow_pqq_primitive_axis_audit_parser_defaults tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_pqq_primitive_axis_audit_tracks_atom_contact tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_pqq_primitive_axis_audit_current_counts -q`:
  3 passed.
- Broader touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  448 passed, 191 subtests passed.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q`: 1523 passed, 210 subtests passed, with
  the existing sklearn/SciPy deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests`: 1478 tests OK, with
  the same existing warning.
- `PYTHONPATH=src python -m compileall -q src/catalytic_earth/lever2_mechanism_incremental_readout.py src/catalytic_earth/cli.py tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py`:
  passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 ontology families, and 702 curated labels
  validated.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- Repo JSON/JSONL parse sweep passed: 3578 JSON files and 27 JSONL files parsed
  with 0 errors.
- New artifact regeneration comparison passed after normalizing `created_utc`.
- New artifact guardrail/source-record audit passed: 0 guardrail violations and
  3 source CIF records present.
- The prior coordinate-proxy readout was regenerated to a temporary path to
  verify the shared renderer path still works.
- `git diff --check`: passed.
- Disk remained above the guardrail at about 17 GiB free.

#### Commit/push status

- Implementation/readout commit
  `f3805e8066ac3e81fdde669d2b424bcd742b81c5` was pushed to
  `origin/lever-2-research-track` with `--force-with-lease` after the branch
  was rebased onto current `origin/main`.
- Fetch verification after the push showed local `HEAD ==
  origin/lever-2-research-track` at
  `f3805e8066ac3e81fdde669d2b424bcd742b81c5` before this handoff-only status
  commit.

#### Exact next action

- Decide whether to approve the PQQ/quinone redox-center contact contract as a
  primitive source-free electron-flow subaxis. If yes, materialize
  `has_source_free_pqq_redox_center_contact` and
  `source_free_pqq_redox_center_contact_count` in the train/cal source-free
  feature sidecar for the 74-row current split and rerun fixed train/cal
  readouts without heldout scoring. If no, the smallest next experiment is a
  donor/acceptor contact primitive that distinguishes true electron-flow
  topology from generic cofactor active-site contact, because the broad
  atomset-contact route was not primary-safe.

### 2026-06-04 Lever 2 Research Run 14

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T03:31:31Z`
- STARTED_LOCAL: `2026-06-04T22:31:31-0500 CDT`
- ENDED_AT: `2026-06-05T04:26:54Z`
- ENDED_LOCAL: `2026-06-04T23:26:54-0500 CDT`
- ELAPSED_MINUTES: `55.38`

#### Intent

Continue Lever 2 electron-flow research only on `lever-2-research-track`.
Start from the measured 35-row smoke-tranche evidence gap and attempt to make
direct source-free electron-flow fields measurable before considering any
blocker artifact.

#### Work log

- Continued in the dedicated branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` on
  `lever-2-research-track`, isolated from the active Lever 3 worktree. Confirmed
  `origin/main` was already an ancestor of the branch and kept the work off
  `main`.
- Disk started close to the guardrail. Removed clean stale detached worktrees
  only, raising free space from about 10 GiB to about 21 GiB before substantive
  work.
- Added
  `build-lever2-source-free-electron-flow-coordinate-proxy-readout`. The readout
  consumes the electron-flow acquisition ceiling and
  `artifacts/v3_geometry_features_1025.json`, then measures coordinate-only
  redox/electron-flow proxy fields on the 35-row smoke tranche and the 74-row
  retained-OOS current-split tranche.
- Materialized two coordinate proxy variants for measurement only:
  `coordinate_redox_contact_binary` (proximal redox ligand code plus
  aromatic/HIS/CYS active-site or pocket residue contact within 5.0 A) and
  `coordinate_quinone_pqq_redox_binary` (proximal PQQ ligand code, tracked as a
  narrow redox-cofactor subfield rather than an approved primitive
  electron-flow axis). Also measured a primary-safe count threshold as a
  control.
- Hardened the proxy so non-`ok` geometry rows cannot contribute positive
  coordinate-proxy fields. Such rows are carried as explicit coordinate-feature
  gaps instead.
- Expanded toward the 74-row retained-OOS current split with a supplemental
  source-free CIF ligand-inventory probe for the two coordinate gaps:
  `m_csa:531` via `artifacts/v3_foldseek_coordinates_1000/pdb_1XVT.cif` and
  `uniprot:Q3LXA3` via
  `artifacts/v3_external_hard_negative_next_candidate_structural_coordinates_1025/afdb_Q3LXA3.cif`.
  This probe closes absent-PQQ inventory as negative evidence only; it does not
  infer active-site proximity and does not promote a primitive electron-flow
  axis.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_coordinate_proxy_readout_current702_20260604.json`
  and
  `work/lever2_source_free_electron_flow_coordinate_proxy_readout_current702_20260604.md`.
- Added CLI parser coverage, synthetic builder coverage for the PQQ smoke signal
  plus non-`ok` geometry handling, and artifact-count regression coverage.

#### Measured results

- Coordinate proxy readout status:
  `lever2_source_free_electron_flow_coordinate_proxy_readout_research_only_coordinate_proxy_smoke_signal`.
  Result class: `research_only_coordinate_proxy_smoke_signal`.
- Smoke tranche coverage is now measurable with source-free coordinate fields:
  35/35 rows have `ok` coordinate features; 0/35 are missing geometry.
- Generic coordinate redox contact is not usable at the smoke operating point:
  10 primary rows and 1 retained-OOS row are positive, so primary retain recall
  would drop to 0.705882.
- PQQ coordinate subfield preserves primary retention and adds smoke OOS
  abstention: 0 primary positives and 1/1 retained-OOS positive (`m_csa:104`),
  primary retain recall 1.0, smoke retained-OOS abstain recall 1.0.
- Full retained-OOS current-split tranche: 72/74 rows have `ok` coordinate
  geometry and two retained-OOS rows are coordinate-feature gaps:
  `m_csa:531` (`insufficient_resolved_residues`, diagnostic PDB `1XVT`) and
  `uniprot:Q3LXA3` (`missing_geometry_row`).
- Supplemental gap CIF probe parsed both gap sidecars. `m_csa:531` had
  structure ligand inventory `COA, MSE`; `uniprot:Q3LXA3` had no non-water
  ligand inventory. Neither gap row had configured redox or PQQ ligand codes,
  so full-tranche PQQ inventory coverage is 74/74.
- Full retained-OOS current-split PQQ readout remains sparse but primary-safe:
  0 primary positives and 1 retained-OOS positive, OOS abstain recall 0.025.
  The generic primary-safe count threshold caught 2 retained-OOS rows at
  primary retain recall 1.0, but it did not catch the smoke row and is not the
  promoted signal.
- Classification: measured source-free coordinate proxy signal exists and adds
  operating-point value on the smoke tranche beyond the current retained-OOS
  surface, but it remains research-only. It is not deployable because the
  coordinate PQQ subfield has not been reviewed/materialized as an approved
  primitive source-free electron-flow axis.

#### Guardrails

- Worked only on Lever 2 electron-flow research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, or heldout splits changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, accessions,
  or provenance were used as predictive features. Entry IDs and coordinate paths
  were used only for tranche accounting, gap accounting, and source-artifact
  lookup.
- The CIF gap probe used only committed local mmCIF atom-site ligand inventory
  for the two explicit full-tranche gaps. It did not infer proximity, tune a
  threshold, or approve a direct electron-flow axis.
- `critical_violation_total=0`; `deployable_now=false`;
  `approved_direct_electron_flow_axis_materialized_by_this_artifact=false`.

#### Validation

- Generated coordinate proxy readout:
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-source-free-electron-flow-coordinate-proxy-readout`.
- Focused parser/builder/artifact tests:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::CliTests::test_lever2_electron_flow_coordinate_proxy_parser_defaults tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_coordinate_proxy_tracks_pqq_smoke_signal tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_coordinate_proxy_readout_current_counts -q`:
  3 passed.
- Broader touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  439 passed, 188 subtests passed.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q`: 1511 passed, 207 subtests passed, with
  the existing sklearn/SciPy deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests`: 1466 tests OK, with
  the same existing warning.
- `PYTHONPATH=src python -m compileall -q src/catalytic_earth/lever2_mechanism_incremental_readout.py src/catalytic_earth/cli.py tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py`:
  passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 ontology families, and 702 curated labels
  validated.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- Repo JSON/JSONL parse sweep passed: 3574 JSON files and 27 JSONL files parsed
  with 0 errors.
- New artifact guardrail/source-record audit passed: both supplemental CIF
  source records exist; heldout scoring is false; production thresholds are
  unchanged; model weights were not fit/refit; direct electron-flow axis
  materialization remains false.
- Artifact regeneration comparison passed after normalizing `created_utc`.
- `git diff --check`: passed.
- Disk remained above the guardrail at about 21 GiB free.

#### Commit/push status

- Implementation/readout commit
  `b17ca2f253cf309c7457578734633cb687c59c73` was pushed to
  `origin/lever-2-research-track`.
- A follow-up handoff status commit records this pushed implementation hash.

#### Exact next action

Review whether the PQQ/quinone coordinate subfield can be promoted from
coordinate-only proxy to an approved primitive source-free electron-flow axis.
If yes, materialize the approved axis for all 74 retained-OOS current-split
rows using the current coordinate/CIF evidence and rerun fixed train/cal
readouts without heldout scoring. If no, define the smallest source-free
electron-flow primitive that distinguishes direct electron-transfer evidence
from generic redox ligand inventory, starting with `m_csa:104` and the current
34 primary retention-gate rows.

### 2026-06-04 Lever 2 Research Run 13

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T02:31:31Z`
- STARTED_LOCAL: `2026-06-04T21:31:31-0500 CDT`
- ENDED_AT: `2026-06-05T03:26:38Z`
- ENDED_LOCAL: `2026-06-04T22:26:38-0500 CDT`
- ELAPSED_MINUTES: `55.12`

#### Intent

Continue Lever 2 mechanism-representation research only on
`lever-2-research-track`, starting from current `origin/main`. Follow the prior
run's electron-flow acquisition next action, but do a measured source-free
evidence scan first rather than writing a blocker packet.

#### Work log

- Started in detached automation worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/a502/catalytic-earth`; found
  the dedicated Lever 2 branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` and
  continued all branch work there.
- Initial disk check was below the 10 GiB guardrail at about 9.8 GiB free.
  Removed the clean stale detached worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/80ee/catalytic-earth`,
  restoring free space to about 13 GiB before substantive work.
- Fetched `origin` and rebased `lever-2-research-track` onto current
  `origin/main` `e68e70889cde28c1de04da8b8d6948141055b0f3`.
  Resolved the recurring `src/catalytic_earth/cli.py` conflicts by preserving
  both the current Lever 3 P07658/safe-abstention command family and the Lever 2
  mechanism command family.
- Added
  `build-lever2-source-free-electron-flow-smoke-tranche-evidence-scan`.
  It consumes the source-free electron-flow acquisition ceiling, the existing
  source-free projection repair candidate surface, the partial-surface
  current-split portability readout, the review-only locator candidate
  directory, the materialized locator gate, and the event-axis linker gate. It
  checks the 35-row smoke tranche for the two direct electron-flow fields
  (`has_electron_transfer_event`, `electron_transfer_count`) and separately
  counts source-free scaffold evidence without treating that scaffold as a
  predictive electron-flow feature.
- Generated the measured artifact/report:
  `artifacts/v3_lever2_source_free_electron_flow_smoke_tranche_evidence_scan_current702_20260604.json`
  and
  `work/lever2_source_free_electron_flow_smoke_tranche_evidence_scan_current702_20260604.md`.
- Added CLI parser coverage, synthetic builder coverage, and artifact-count
  regression coverage for the smoke-tranche scan.
- Checked an alternate source-free cofactor/locus proxy route. Existing organic
  cofactor score sidecars cover all 35 smoke rows for flavin/heme records and
  have 10 rows at score >= 0.5 (`m_csa:102`, `m_csa:277`, `m_csa:319`,
  `m_csa:320`, `m_csa:399`, `m_csa:473`, `m_csa:694`, `m_csa:800`,
  `m_csa:879`, `m_csa:973`), but this is sequence/cofactor-channel evidence,
  not direct electron-flow evidence. Review-only locus sidecars had 0 proximal
  Fe-S smoke rows, 0 proximal radical-SAM smoke rows, and 12 proximal metal
  smoke rows; all had `predictive_use_allowed_rows=0`. No cofactor/locus proxy
  was promoted into the electron-flow feature surface.

#### Measured results

- Smoke-tranche evidence scan:
  `lever2_source_free_electron_flow_smoke_tranche_evidence_scan_research_only_smoke_tranche_evidence_gap`.
  The prior measured train/cal electron-flow signal is retained
  (`train_cal_electron_flow_oos_recall_delta=0.142857`), but the current
  source-free evidence is still insufficient to measure the smoke tranche.
- Direct source-free electron-flow field coverage is 0/35 rows: 0/1 retained
  OOS row (`m_csa:104`) and 0/34 current primary retention-gate rows have both
  required direct fields. Both `has_electron_transfer_event` and
  `electron_transfer_count` are missing on all 35 smoke rows.
- Current source-free projection candidate overlap with the smoke tranche is
  0/35 rows; partial-surface missing coverage is 35/35 rows.
- Source-free scaffold coverage is not enough for a mechanism feature claim:
  exactly 1/35 smoke rows (`m_csa:216`) has a review-only locator candidate;
  0/35 have materialized source-free locators; 0/35 have source-free event-axis
  linker rows; 0/35 have source-free pair support or event-axis references in
  the candidate surface.
- Classification: research-only measured evidence gap, not deployable, not a
  negative against electron-flow as a train/cal signal, and no Lever 2
  promotion.

#### Guardrails

- Worked only on Lever 2 research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, or heldout splits changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, or source
  provenance were used as predictive features.
- Entry IDs were used only for tranche, split, artifact-overlap, scaffold, and
  missing-evidence accounting.
- The new artifact did not materialize source-free electron-flow rows and did
  not authorize partial locator/proton/cofactor support as an electron-flow
  substitute.

#### Validation

- Generated smoke-tranche evidence scan:
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-source-free-electron-flow-smoke-tranche-evidence-scan`.
- Focused parser/builder/artifact tests:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::CliTests::test_lever2_electron_flow_smoke_tranche_scan_parser_defaults tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_electron_flow_smoke_tranche_scan_requires_direct_fields tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_electron_flow_smoke_tranche_evidence_scan_counts -q`:
  3 passed.
- Broader touched-file slice:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  436 passed, 188 subtests passed.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q`: 1508 passed, 207 subtests passed, with
  the existing sklearn/SciPy deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests`: 1463 tests OK, with
  the same existing warning.
- `PYTHONPATH=src python -m compileall -q src tests`: passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 ontology families, and 702 curated labels
  validated.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- `git diff --check`: passed.
- Repo JSON/JSONL parse sweep passed: 3569 JSON files and 27 JSONL files parsed
  with 0 errors.
- New artifact source-record audit passed: all source artifacts/directories
  exist, `critical_violation_total=0`, heldout scoring is false, and the
  artifact did not materialize source-free electron-flow rows.
- Artifact regeneration comparison passed after normalizing `created_utc`.
- Disk remained above the guardrail at about 13 GiB free.

#### Commit/push status

- Implementation/readout commit
  `49cde114e325196ca1f781db63fa4131fb0d56c7` was pushed to
  `origin/lever-2-research-track` with `--force-with-lease` after the rebase.
  Fetch verification showed local `HEAD == origin/lever-2-research-track` at
  `49cde114e325196ca1f781db63fa4131fb0d56c7` before this handoff-only commit.

#### Exact next action

Materialize direct source-free electron-flow fields for the exact 35-row smoke
tranche first: `m_csa:104` plus the 34 current primary retention-gate rows
listed in
`artifacts/v3_lever2_source_free_electron_flow_smoke_tranche_evidence_scan_current702_20260604.json`.
Do not use organic cofactor scores, metal/Fe-S/radical-SAM review-only locus
sidecars, locator-only rows, or proton/pair support as substitutes for
`has_electron_transfer_event` and `electron_transfer_count`. After those two
fields exist for all 35 rows, rerun the train/cal source-free projection and
fixed-threshold incremental readouts. Expand to the 74-row retained-OOS
current-split tranche only if the smoke tranche preserves primary retention and
adds incremental OOS abstention.

### 2026-06-04 Lever 2 Research Run 12

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T01:33:02Z`
- STARTED_LOCAL: `2026-06-04T20:33:02-0500 CDT`
- ENDED_AT: `2026-06-05T02:00:18Z`
- ENDED_LOCAL: `2026-06-04T21:00:18-0500 CDT`
- ELAPSED_MINUTES: `27.27`

#### Intent

Continue Lever 2 mechanism-representation research only on
`lever-2-research-track`, starting from current `origin/main`. Avoid repeating
the settled current-surface embedding and event-axis/motif null negatives; run
a measured source-free mechanism-evidence follow-up if the available artifacts
support one.

#### Work log

- Started in detached automation worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/80ee/catalytic-earth`; found
  the existing dedicated Lever 2 branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` and
  continued there for all branch work.
- Fetched `origin main` and `origin lever-2-research-track`; confirmed current
  `origin/main` `f599ef4126e8f86aaf415093f56f979c554d81ce` is already an
  ancestor of `lever-2-research-track`; `git rebase origin/main` reported the
  branch was up to date.
- Disk started at the guardrail edge and dipped to about 9.8 GiB after tests.
  Removed clean stale detached worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/a14d/catalytic-earth`,
  restoring free space to about 13 GiB without touching main or the Lever 2
  branch worktree.
- Added `build-lever2-source-free-electron-flow-acquisition-ceiling-readout`.
  It consumes the prior source-free electron-flow split-alignment readout and
  measures the current-split source-free row tranches needed to make the
  electron-flow operating-point readout measurable.
- Added `build-lever2-source-free-mechanism-axis-acquisition-ranking-readout`.
  It consumes the train/cal projection readout and candidate-surface field
  coverage, ranks missing source-free axes by measured train/cal value and
  evidence burden, and separates genuine mechanism axes from non-mechanism
  confidence/locator support axes.
- Generated two committed measured artifacts/reports:
  `artifacts/v3_lever2_source_free_electron_flow_acquisition_ceiling_readout_current702_20260604.json`,
  `work/lever2_source_free_electron_flow_acquisition_ceiling_readout_current702_20260604.md`,
  `artifacts/v3_lever2_source_free_mechanism_axis_acquisition_ranking_readout_current702_20260604.json`,
  and
  `work/lever2_source_free_mechanism_axis_acquisition_ranking_readout_current702_20260604.md`.
- Added CLI parser coverage, synthetic builder coverage, and generated-artifact
  regressions for both readouts.
- Checked the adjacent source-free partial-surface reuse route as a second
  Lever 2 attempt. The existing measured artifact remains a current-split
  reuse negative with 0/34 primary overlap and 0/132 current-retained OOS
  overlap, so it reinforces the new source-free electron-flow acquisition gate
  rather than opening a separate deployable path.

#### Measured results

- Electron-flow acquisition-ceiling readout:
  `lever2_source_free_electron_flow_acquisition_ceiling_readout_research_only_acquisition_ceiling`.
  The measured train/cal electron-flow gain is retained:
  OOS abstain recall improves from 0.642857 to 0.785714 at primary retain
  recall 1.0, delta 0.142857.
- Current source-free candidate coverage is still 0/40 retained-OOS priority
  rows and 0/34 current primary retention-gate rows. The smallest measurable
  smoke tranche is 35 rows: top 1 retained-OOS row (`m_csa:104`) plus all
  34 current primary rows. The full retained-OOS current-split tranche is
  74 rows: all 40 retained-OOS priority rows plus all 34 primary rows.
- Best-axis current-extended retained-OOS catches remain 2, but 0 of those
  catches are already in the current acquisition-priority queue, so no
  split-aligned operating-point value can be claimed now.
- Mechanism-axis acquisition-ranking readout:
  `lever2_source_free_mechanism_axis_acquisition_ranking_readout_research_only_axis_ranked_evidence_gap`.
  Among genuine mechanism axes, electron-flow ranks first by measured train/cal
  OOS-recall delta and value density: electron-flow delta 0.142857 with
  2 added fields; bond-change delta 0.107143 with 5 added fields; event
  topology delta 0.071429 with 2 added fields.
- Confidence metadata ties electron-flow on raw OOS recall delta (0.142857) but
  is explicitly classified as non-mechanism/review metadata and not a promotion
  axis. Active-site locator count is also non-event support, with delta 0.035714.
- No genuine mechanism axis is source-free ready now: 0/3 ready. The best axis,
  electron-flow, still lacks both direct source-free fields
  (`electron_transfer_count`, `has_electron_transfer_event`) across all
  53 candidate-surface rows and current-split row coverage.
- Classification: research-only measured evidence gap, not deployable and not
  a negative against electron-flow as a train/cal signal. The current data are
  insufficient for Lever 2 promotion because source-free, split-aligned
  electron-flow rows do not yet exist for the current primary and retained-OOS
  rows.

#### Guardrails

- Worked only on Lever 2 research.
- No labels, registries, ontologies, imports, production thresholds,
  production gates, model weights, deployment routes, or heldout splits changed.
- No heldout rows were trained on, tuned on, rescored, or evaluated.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, or source
  provenance were used as predictive features.
- Entry IDs were used only for split accounting, row-tranche accounting,
  deterministic diagnostics, and missing-evidence accounting.
- M-CSA row-specific mechanism features remain train/cal-only research
  evidence; no source-free current-split rows were materialized or promoted.

#### Validation

- Generated electron-flow acquisition-ceiling readout:
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-source-free-electron-flow-acquisition-ceiling-readout`.
- Generated mechanism-axis acquisition-ranking readout:
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-source-free-mechanism-axis-acquisition-ranking-readout`.
- Focused new parser/builder/artifact tests passed:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::CliTests::test_lever2_source_free_axis_acquisition_ranking_parser_defaults tests/test_lever2_mechanism_incremental_readout.py::Lever2MechanismIncrementalReadoutTests::test_source_free_mechanism_axis_acquisition_ranking_prefers_electron_flow tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_source_free_axis_acquisition_ranking_readout_current_counts -q`:
  3 passed.
- Focused combined parser/builder/artifact tests for both new readouts passed:
  6 passed before the second readout and 3 passed after the second readout.
- Broader touched-file slice after both readouts:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  429 passed, 186 subtests passed.
- Full pytest:
  `PYTHONPATH=src python -m pytest -q`: 1498 passed, 205 subtests passed, with
  the existing sklearn/SciPy deprecation warning.
- Full unittest discovery:
  `PYTHONPATH=src python -m unittest discover -s tests`: 1453 tests OK, with
  the same existing warning.
- `PYTHONPATH=src python -m compileall -q src tests`: passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate`: 12 source records,
  8 mechanism fingerprints, 15 ontology families, and 702 curated labels
  validated.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`:
  2 passed.
- `git diff --check`: passed.
- Repo JSON/JSONL parse sweep passed: 3570 JSON files and 27 JSONL files parsed
  with 0 errors.
- New artifact source records were manually checked: all referenced source
  artifacts exist and have recorded hashes; both new artifacts report
  `critical_violation_total` 0 and `heldout_rows_scored_by_this_artifact`
  false.
- Disk ended above the guardrail at about 13 GiB free.

#### Commit/push status

- Implementation/readout commit
  `32e5f8dd80369ae629183789eaae2c948b090fd9` was pushed to
  `origin/lever-2-research-track`.
- After `git fetch origin lever-2-research-track`, local `HEAD` matched
  `origin/lever-2-research-track` at
  `32e5f8dd80369ae629183789eaae2c948b090fd9`; this final handoff-status
  update is committed and pushed as a follow-up bookkeeping commit, with the
  final branch hash recorded in automation memory and the final response.

#### Exact next action

Materialize direct source-free electron-flow fields first for the 35-row smoke
tranche: `m_csa:104` plus all 34 current primary retention-gate rows. Then
rerun the train/cal projection and fixed-threshold incremental readouts. Only
expand to the 74-row retained-OOS current-split tranche if the smoke tranche
preserves primary retention and adds incremental OOS abstention. Do not spend
promotion effort on confidence metadata, and do not evaluate heldout until the
current train/cal split is measurable.

### 2026-06-04 Lever 2 Research Run 11

#### Wall-clock ledger

- STARTED_AT: `2026-06-05T00:31:33Z`
- STARTED_LOCAL: `2026-06-04T19:31:33-0500 CDT`
- ENDED_AT: `2026-06-05T01:27:10Z`
- ENDED_LOCAL: `2026-06-04T20:27:10-0500 CDT`
- ELAPSED_MINUTES: `55.62`

#### Intent

Continue Lever 2 mechanism-representation research only. Start from current
`origin/main`, keep all work on `lever-2-research-track`, and run another
measured train/cal readout that does not repeat the settled current-surface
embedding negative.

#### Work log

- Started in detached automation worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/a14d/catalytic-earth`; found
  the existing dedicated Lever 2 branch worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/88bb/catalytic-earth` and
  continued there for all branch work.
- Initial disk free space was below the 10 GiB guardrail at about 9.9 GiB.
  Removed the clean stale detached worktree
  `/Users/vivekvardhanarrabelli/.codex/worktrees/d8db/catalytic-earth`,
  restoring free space to about 13 GiB before substantive branch work.
- Fetched `origin` and rebased `lever-2-research-track` onto current
  `origin/main` `f599ef4126e8f86aaf415093f56f979c554d81ce`.
  Resolved the expected `src/catalytic_earth/cli.py` conflict by preserving
  both the latest Lever 3 deployment-input audit command family and the Lever 2
  mechanism command family.
- Added a measured event-motif interaction null-control readout:
  `build-lever2-event-motif-interaction-null-readout`. It derives coupled
  motif fields from row-specific event primitives such as bond+proton,
  bond+electron, all-three event axes, and multi-event topology, then tests
  projected-subset-plus-motif surfaces under the same leave-target-out,
  primary-control rule-selection discipline used by the prior Lever 2 event
  readouts.
- Generated committed default and alternate-seed measured artifacts/reports:
  `artifacts/v3_lever2_event_motif_interaction_null_readout_current702_20260604.json`,
  `work/lever2_event_motif_interaction_null_readout_current702_20260604.md`,
  `artifacts/v3_lever2_event_motif_interaction_null_altseed_readout_current702_20260604.json`,
  and
  `work/lever2_event_motif_interaction_null_altseed_readout_current702_20260604.md`.
- Added parser and artifact-regression coverage for the motif-null command and
  both generated readouts.
- Ran disposable follow-up probes that were not committed: an all-interaction
  motif union probe, an event-axis-richness-only probe, a completed
  256-permutation motif-null probe in `/tmp`, and optional 8192/2048
  high-permutation probes stopped during wrap because the committed artifacts
  and completed 256-probe had already preserved the negative decision.

#### Measured results

- Default motif-null result:
  `research_only_event_motif_weak_marginal_not_distinguishable_from_null`.
  Baseline projected subset catches 5/13 current-retained overlap rows. The
  best coupled motif surface is
  `source_free_projected_proton_role_subset+multi_event_bond_topology`, catching
  6/13 current-retained overlap rows with 1 marginal catch (`m_csa:256`).
- The default deterministic motif null over 128 permutations and 6 motif axes
  has max-marginal min/median/p90/p95/max = 1/3/5/6/7. All 128/128
  permutations meet or exceed the observed 1 marginal catch; empirical p-value
  is `1.0`.
- Alternate seed agrees: observed marginal remains 1, null p95 is 6, null max
  is 8, and 127/128 permutations meet or exceed observed
  (`p=0.992248`).
- A completed temporary 256-permutation probe also agrees: null p95/max = 5/8,
  256/256 permutations meet or exceed observed, and p-value is `1.0`.
- Disposable combined-surface probes did not rescue the route:
  all event-motif interaction fields caught 5/13 current-retained overlap rows
  with 0 marginal catches, and event-axis richness alone also caught 5/13 with
  0 marginal catches.
- Classification: measured research-only negative for event-motif interaction
  features. The route does not add null-controlled operating-point value beyond
  the current geometry/fold/projected-subset surface.
- Deployability: not deployable. The current split still has 0/34 current
  primary rows and 0/132 current-retained OOS rows with source-free
  event-motif rows, so no integrated operating-point claim or Lever 2 promotion
  is supported.

#### Guardrails

- Worked only on Lever 2 research.
- No labels, registries, ontologies, imports, production thresholds, heldout
  splits, model weights, deployment gates, or heldout rows changed.
- No mechanism text, EC/Rhea IDs, labels, source IDs, target names, accessions,
  or source provenance were used as predictive features.
- Entry IDs were used only for split/overlap accounting, deterministic null
  assignment bookkeeping, row diagnostics, and missing-evidence accounting.
- M-CSA row-specific mechanism features remain train/cal-only research
  evidence; no source-free current-split rows were materialized or promoted.

#### Validation

- Generated default motif-null readout:
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-event-motif-interaction-null-readout`.
- Generated alternate-seed motif-null readout:
  `PYTHONPATH=src python -m catalytic_earth.cli build-lever2-event-motif-interaction-null-readout --null-seed lever2_event_motif_interaction_null_altseed_v0 --artifact-id v3_lever2_event_motif_interaction_null_altseed_readout_current702_20260604 --out artifacts/v3_lever2_event_motif_interaction_null_altseed_readout_current702_20260604.json --report work/lever2_event_motif_interaction_null_altseed_readout_current702_20260604.md`.
- Focused parser/artifact tests passed:
  `PYTHONPATH=src python -m pytest tests/test_cli.py::CliTests::test_lever2_event_motif_interaction_null_parser_defaults tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_motif_interaction_null_readout_counts tests/test_geometry_artifact_regression.py::GeometryArtifactRegressionTests::test_lever2_event_motif_interaction_null_altseed_readout_counts -q`:
  3 passed.
- Broader touched Lever 2/CLI/artifact slice passed:
  `PYTHONPATH=src python -m pytest tests/test_cli.py tests/test_lever2_mechanism_incremental_readout.py tests/test_geometry_artifact_regression.py -q`:
  423 passed, 186 subtests passed.
- Full pytest passed:
  `PYTHONPATH=src python -m pytest -q`: 1492 passed, 1 existing sklearn/SciPy
  deprecation warning, 205 subtests passed.
- Full unittest discovery passed:
  `PYTHONPATH=src python -m unittest discover -s tests`: 1447 tests OK, with
  the same existing warning.
- `python -m py_compile src/catalytic_earth/lever2_mechanism_incremental_readout.py src/catalytic_earth/cli.py tests/test_cli.py tests/test_geometry_artifact_regression.py`
  passed.
- `PYTHONPATH=src python -m compileall -q src tests` passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed: 12 source
  records, 8 mechanism fingerprints, 15 ontology families, and 702 curated
  labels.
- `PYTHONPATH=src python -m pytest tests/test_doc_reference_check.py -q`
  passed: 2 passed.
- `git diff --check` passed.
- Repo JSON/JSONL parse sweep passed: 3568 JSON files and 27 JSONL files
  parsed with 0 errors.
- New motif-null artifact `source_artifacts` hashes checked: 10 checked across
  2 artifacts, 0 stale.
- Disk stayed above the 10 GiB guardrail after cleanup and through wrap, ending
  around 14 GiB free.

#### Commit/push status

- Implementation/readout commit
  `72cf0f0fb51f509a87fad9e9f27afee6cdaca54f` was pushed to
  `origin/lever-2-research-track` with `--force-with-lease` after rebasing the
  dedicated branch onto current `origin/main`.
- Verified after `git fetch origin lever-2-research-track` that local `HEAD`
  matched `origin/lever-2-research-track` at
  `72cf0f0fb51f509a87fad9e9f27afee6cdaca54f`.
- This final handoff verification update is committed and pushed as a
  follow-up bookkeeping commit; the exact final branch hash is recorded in
  automation memory and the final response.

#### Exact next action

- Do not promote Lever 2 event-motif interactions. If source-free current-split
  event rows are materialized later, rerun the event-motif null readout and
  require marginal catches above the empirical null p95 before any heldout or
  deployment claim. Otherwise prioritize acquiring source-free mechanism/event
  evidence for the 34 current primary rows and 132 current-retained OOS rows
  before more event-surface modeling.

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
