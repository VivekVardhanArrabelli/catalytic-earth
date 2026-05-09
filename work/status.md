# Catalytic Earth Status

Generated from `work/progress_log.jsonl`.

## Time

- Entries: 13
- Measured elapsed time: 11.1 minutes (0.19 hours)
- Estimated/planned time: 390 minutes (6.50 hours)
- Note: entries before timing instrumentation are estimates, not clock measurements.

## Time By Stage

- ops: 1.6 measured minutes (0.03 hours)
- post-v2: 9.6 measured minutes (0.16 hours)
- ops: 45 estimated minutes (0.75 hours)
- post-v2: 165 estimated minutes (2.75 hours)
- v0: 55 estimated minutes (0.92 hours)
- v1: 55 estimated minutes (0.92 hours)
- v2: 70 estimated minutes (1.17 hours)

## Progress Counters

- Artifact references logged: 75
- Evidence references logged: 67

## Recent Entries

### 2026-05-09T14:03:45.516905+00:00 - post-v2

- Task: Add geometry-aware seed fingerprint retrieval baseline
- Time mode: estimate
- Estimated/planned minutes: 30
- Artifacts: src/catalytic_earth/geometry_retrieval.py, artifacts/v3_geometry_retrieval.json, tests/test_geometry_retrieval.py
- Evidence: 20 geometry entries ranked, 6 seed fingerprints scored, 25 tests passed
- Notes: Estimated/planned time; not measured clock time.

### 2026-05-09T14:10:40.717863+00:00 - post-v2

- Task: Add curated seed mechanism labels and geometry retrieval evaluation
- Time mode: estimate
- Estimated/planned minutes: 35
- Artifacts: data/registries/curated_mechanism_labels.json, src/catalytic_earth/labels.py, artifacts/v3_label_summary.json, artifacts/v3_geometry_label_eval.json, tests/test_labels.py
- Evidence: 20 curated labels, 4 in-scope seed-fingerprint labels, 16 out-of-scope labels, 28 tests passed, top3 in-scope accuracy 1.0, top1 in-scope accuracy 0.0
- Notes: Estimated/planned time; not measured clock time.

### 2026-05-09T14:13:21.398170+00:00 - ops

- Task: Update automation cadence to 55-minute hourly work blocks with mandatory push
- Time mode: estimate
- Estimated/planned minutes: 10
- Artifacts: work/README.md, work/handoff.md, work/scope.md
- Evidence: automation updated to hourly RRULE, mandatory push rule recorded
- Notes: Estimated/planned time; not measured clock time.

### 2026-05-09T14:18:10.779278+00:00 - ops

- Task: Require next-agent handoff update after every hourly block
- Time mode: estimate
- Estimated/planned minutes: 10
- Artifacts: work/handoff.md, work/README.md, work/scope.md
- Evidence: automation prompt updated, next-agent handoff section added, operating rule updated
- Notes: Estimated/planned time; not measured clock time.

### 2026-05-09T14:25:33.013901+00:00 - post-v2

- Task: Strengthen V2 retrieval calibration and performance checks
- Time mode: estimate
- Estimated/planned minutes: 55
- Artifacts: src/catalytic_earth/geometry_retrieval.py, src/catalytic_earth/labels.py, src/catalytic_earth/performance.py, artifacts/v3_abstention_calibration.json, artifacts/perf_report.json, docs/v2_strengthening_report.md
- Evidence: 30 tests passed, top1 in-scope accuracy 1.0, top3 in-scope accuracy 1.0, out-of-scope abstention 0.75, selected abstention threshold 0.8, 5 local performance benchmarks
- Notes: Estimated/planned time; not measured clock time.

### 2026-05-09T15:20:27.676203+00:00 - post-v2

- Task: Add mmCIF ligand/cofactor context to geometry features and retrieval scoring
- Time mode: measured
- Measured minutes: 5.217
- Started: 2026-05-09T15:15:06Z
- Ended: 2026-05-09T15:20:19Z
- Artifacts: src/catalytic_earth/structure.py, src/catalytic_earth/geometry_retrieval.py, tests/test_structure.py, tests/test_geometry_retrieval.py, artifacts/v3_geometry_features.json, artifacts/v3_geometry_retrieval.json, artifacts/v3_geometry_label_eval.json, artifacts/v3_abstention_calibration.json, artifacts/perf_report.json, docs/geometry_features.md, docs/v2_strengthening_report.md, work/handoff.md, work/scope.md
- Evidence: 33 tests passed, 11/20 entries with proximal ligands, 5/20 entries with inferred cofactors, top1 in-scope accuracy 1.0, top3 in-scope accuracy 1.0, selected abstention threshold 0.8, out-of-scope abstention 1.0 at selected threshold

### 2026-05-09T15:22:39.241656+00:00 - ops

- Task: Update README timeline and final handoff before next automation
- Time mode: measured
- Measured minutes: 1.583
- Started: 2026-05-09T15:20:55Z
- Ended: 2026-05-09T15:22:30Z
- Artifacts: README.md, work/handoff.md, work/scope.md
- Evidence: 33 tests passed, validate passed, README timeline recalibrated, current state and next automation task clarified

### 2026-05-09T15:30:17.008476+00:00 - post-v2

- Task: Add substrate-pocket descriptors and pocket-aware retrieval scoring
- Time mode: measured
- Measured minutes: 4.333
- Started: 2026-05-09T15:25:48Z
- Ended: 2026-05-09T15:30:08Z
- Artifacts: src/catalytic_earth/structure.py, src/catalytic_earth/geometry_retrieval.py, tests/test_structure.py, tests/test_geometry_retrieval.py, artifacts/v3_geometry_features.json, artifacts/v3_geometry_retrieval.json, artifacts/v3_geometry_label_eval.json, artifacts/v3_abstention_calibration.json, artifacts/perf_report.json, README.md, docs/geometry_features.md, docs/v2_strengthening_report.md, work/handoff.md, work/scope.md
- Evidence: 35 tests passed, 15/20 entries with substrate-pocket context, 11/20 entries with proximal ligands, 5/20 entries with inferred cofactors, top1 in-scope accuracy 1.0, top3 in-scope accuracy 1.0, selected abstention threshold 0.75, out-of-scope abstention 1.0 at selected threshold

## Expectation Updates

- 2026-05-09T13:40:20.355854+00:00: v0 completed in one active session, so the previous one-year v0-v2 timeline is too conservative and must be recalibrated from logged progress
- 2026-05-09T13:40:25.768544+00:00: Use observed artifact-per-hour rate to revise v1 and v2 estimates after each material chunk.
- 2026-05-09T13:54:30.954964+00:00: V1 completed much faster than the earlier days-to-weeks estimate because paginated M-CSA and UniProt TSV APIs were straightforward.
- 2026-05-09T13:54:31.022704+00:00: The completed V2 is a scaffold-level research artifact, not the final high-impact enzyme atlas; time estimates must distinguish scaffold completion from scientific validation.
- 2026-05-09T14:01:49.012481+00:00: Geometry extraction was implementable quickly for PDB-linked M-CSA entries; the harder next step is label quality and retrieval evaluation.
- 2026-05-09T14:03:45.516905+00:00: Next quality bottleneck is curated mechanism labels and evaluation, not baseline implementation.
- 2026-05-09T14:10:40.717863+00:00: The next bottleneck is improving ranking and abstention, not adding labels machinery.
- 2026-05-09T14:13:21.398170+00:00: Progress will now be measured per hourly block rather than per ad hoc milestone.
- 2026-05-09T14:18:10.779278+00:00: Continuity is now treated as a required output of each 55-minute work block.
- 2026-05-09T14:25:33.013901+00:00: The time overestimate came from confusing scaffold implementation with scientifically robust validation; current progress is fast but still small-label and artifact-scale.
- 2026-05-09T15:20:27.676203+00:00: Ligand/cofactor context integration from mmCIF was quick; next quality bottleneck shifts to substrate-pocket descriptors and larger curated labels.
- 2026-05-09T15:22:39.241656+00:00: README now states that scaffold work moved faster than first estimated; impact depends on scaling labels, harder benchmarks, expert review, and validation.
- 2026-05-09T15:30:17.008476+00:00: Substrate-pocket descriptors integrated quickly; next bottleneck is targeted failure analysis and label expansion rather than more feature plumbing.

## Scope Adjustments

- 2026-05-09T13:40:25.768544+00:00: Project management is now repository state, not chat state; future scope changes must be recorded in the ledger.
- 2026-05-09T13:54:30.954964+00:00: V1 criteria are satisfied by a bounded 50-entry graph slice; broader scale is now an expansion problem, not a schema blocker.
- 2026-05-09T13:54:31.022704+00:00: V2 scaffold criteria are satisfied; next work should increase scientific quality rather than add more dashboard-like surface area.
- 2026-05-09T14:01:49.012481+00:00: Post-V2 quality work now targets geometry-aware retrieval rather than more text-only scaffolding.
- 2026-05-09T14:03:45.516905+00:00: Geometry now affects retrieval scores through residue signature matching and catalytic-cluster compactness.
- 2026-05-09T14:10:40.717863+00:00: Curated labels are now explicit for the 20-entry geometry slice; retrieval quality is measurable and currently weak at top1.
- 2026-05-09T14:13:21.398170+00:00: Each automation run is now an hourly carry-forward block: 55 minutes work, 5 minutes break/overhead, commit and push every run.
- 2026-05-09T14:18:10.779278+00:00: Every automation run must now leave explicit next-agent start instructions before committing and pushing.
- 2026-05-09T14:25:33.013901+00:00: V2 is stronger: retrieval has cofactor-aware scoring, calibrated abstention, and local performance measurement; full scalability and ligand parsing remain future work.
- 2026-05-09T15:20:27.676203+00:00: Post-V2 quality scope now includes ligand-supported cofactor evidence in retrieval; substrate-pocket descriptors become the next bounded upgrade.
- 2026-05-09T15:22:39.241656+00:00: Next automation should continue from substrate-pocket descriptors and harder negative controls, not from v0-v2 scaffold planning.
- 2026-05-09T15:30:17.008476+00:00: Post-V2 retrieval now includes pocket-aware scoring; next bounded iteration should tune abstention and false-positive control using failure categories.
