# Catalytic Earth Status

Generated from `work/progress_log.jsonl`.

## Time

- Entries: 20
- Measured elapsed time: 205.6 minutes (3.43 hours)
- Estimated/planned time: 390 minutes (6.50 hours)
- Note: entries before timing instrumentation are estimates, not clock measurements.

## Time By Stage

- ops: 13.1 measured minutes (0.22 hours)
- post-v2: 192.5 measured minutes (3.21 hours)
- ops: 45 estimated minutes (0.75 hours)
- post-v2: 165 estimated minutes (2.75 hours)
- v0: 55 estimated minutes (0.92 hours)
- v1: 55 estimated minutes (0.92 hours)
- v2: 70 estimated minutes (1.17 hours)

## Progress Counters

- Artifact references logged: 123
- Evidence references logged: 104

## Recent Entries

### 2026-05-09T15:30:17.008476+00:00 - post-v2

- Task: Add substrate-pocket descriptors and pocket-aware retrieval scoring
- Time mode: measured
- Measured minutes: 4.333
- Started: 2026-05-09T15:25:48Z
- Ended: 2026-05-09T15:30:08Z
- Artifacts: src/catalytic_earth/structure.py, src/catalytic_earth/geometry_retrieval.py, tests/test_structure.py, tests/test_geometry_retrieval.py, artifacts/v3_geometry_features.json, artifacts/v3_geometry_retrieval.json, artifacts/v3_geometry_label_eval.json, artifacts/v3_abstention_calibration.json, artifacts/perf_report.json, README.md, docs/geometry_features.md, docs/v2_strengthening_report.md, work/handoff.md, work/scope.md
- Evidence: 35 tests passed, 15/20 entries with substrate-pocket context, 11/20 entries with proximal ligands, 5/20 entries with inferred cofactors, top1 in-scope accuracy 1.0, top3 in-scope accuracy 1.0, selected abstention threshold 0.75, out-of-scope abstention 1.0 at selected threshold

### 2026-05-09T15:42:05.002091+00:00 - ops

- Task: Tighten automation early-completion and git sync rules
- Time mode: measured
- Measured minutes: 1.033
- Started: 2026-05-09T15:40:56Z
- Ended: 2026-05-09T15:41:58Z
- Artifacts: automation:catalytic-earth-work-loop, work/handoff.md, work/scope.md
- Evidence: automation requires remaining-time plan after early task completion, automation requires final git sync verification, 35 tests passed, validate passed

### 2026-05-09T16:02:34.920556+00:00 - post-v2

- Task: Add out-of-scope failure analysis artifact and threshold hint
- Time mode: measured
- Measured minutes: 2.883
- Started: 2026-05-09T15:59:35Z
- Ended: 2026-05-09T16:02:28Z
- Artifacts: src/catalytic_earth/labels.py, src/catalytic_earth/cli.py, tests/test_labels.py, artifacts/v3_geometry_failure_analysis.json, README.md, docs/geometry_features.md, work/handoff.md, work/scope.md
- Evidence: 37 tests passed, validate passed, 16 out-of-scope entries evaluated at threshold 0.7, 4 false non-abstentions, all failures near_threshold, recommended threshold 0.75

### 2026-05-09T16:03:37.698226+00:00 - ops

- Task: Pin automations to GPT-5.5 xhigh
- Time mode: measured
- Measured minutes: 2.017
- Started: 2026-05-09T16:01:14Z
- Ended: 2026-05-09T16:03:15Z
- Artifacts: automation:catalytic-earth-work-loop, automation:overnight-batch-driver, work/README.md, work/handoff.md, work/scope.md
- Evidence: all automation TOML files with model fields now show gpt-5.5, all automation TOML files with reasoning fields now show xhigh, 37 tests passed, validate passed

### 2026-05-09T16:14:49.435851+00:00 - ops

- Task: Require full 50-minute productive automation work
- Time mode: measured
- Measured minutes: 8.517
- Started: 2026-05-09T16:06:10Z
- Ended: 2026-05-09T16:14:41Z
- Artifacts: automation:catalytic-earth-work-loop, work/README.md, work/handoff.md, work/scope.md
- Evidence: automation requires productive project work until 50 elapsed wall-clock minutes, automation forbids early handoff idle time or reporting-only time before wrap, 37 tests passed, validate passed

### 2026-05-09T17:07:37.625326+00:00 - post-v2

- Task: Calibrate geometry abstention and expand labels
- Time mode: measured
- Measured minutes: 51.233
- Started: 2026-05-09T16:16:10Z
- Ended: 2026-05-09T17:07:24Z
- Artifacts: artifacts/v3_geometry_features_40.json, artifacts/v3_geometry_retrieval_40.json, artifacts/v3_abstention_calibration_40.json, artifacts/v3_hard_negative_controls_40.json, artifacts/v3_structure_mapping_issues_40.json, artifacts/v3_label_expansion_candidates.json, artifacts/perf_report.json
- Evidence: 39 unit tests passed, validate passed, 36 curated labels, 40-entry geometry slice, selected thresholds 0.5796 and 0.587, 2 hard negatives, 14 mapping issues

### 2026-05-09T18:08:06.495922+00:00 - post-v2

- Task: Expand geometry labels, hard-negative controls, and cobalamin counterevidence
- Time mode: measured
- Measured minutes: 51.433
- Started: 2026-05-09T17:16:40Z
- Ended: 2026-05-09T18:08:06Z
- Artifacts: artifacts/v1_graph_75.json, artifacts/v3_geometry_features_60.json, artifacts/v3_geometry_retrieval_60.json, artifacts/v3_hard_negative_controls_60.json
- Evidence: PYTHONPATH=src python -m unittest discover -s tests; PYTHONPATH=src python -m catalytic_earth.cli validate

### 2026-05-09T19:35:11+00:00 - post-v2

- Task: Expand geometry benchmark to 125 labels and expose hard negatives
- Time mode: measured
- Measured minutes: 77.383
- Started: 2026-05-09T18:17:48Z
- Ended: 2026-05-09T19:35:11Z
- Artifacts: src/catalytic_earth/geometry_retrieval.py, src/catalytic_earth/performance.py, data/registries/mechanism_fingerprints.json, data/registries/curated_mechanism_labels.json, artifacts/v3_geometry_retrieval_100.json, artifacts/v3_geometry_label_eval_100.json, artifacts/v3_hard_negative_controls_100.json, artifacts/v3_abstention_calibration_100.json, artifacts/v3_geometry_retrieval_125.json, artifacts/v3_geometry_label_eval_125.json, artifacts/v3_abstention_calibration_125.json, artifacts/v3_geometry_failure_analysis_125.json, artifacts/v3_geometry_score_margins_125.json, artifacts/v3_hard_negative_controls_125.json, artifacts/perf_report.json, docs/geometry_features.md, work/handoff.md
- Evidence: 61 unit tests passed, validate passed, 125 curated labels, 125 geometry entries, 38 in-scope positives, 87 out-of-scope controls, 100-entry slice retains all positives with zero false non-abstentions, 125-entry zero-false threshold 0.5877, 125-entry retained positives 29/38, 125-entry hard negatives 74, 125-entry score gap -0.1404

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
- 2026-05-09T15:42:05.002091+00:00: Future runs should consume the full 55-minute wall-clock block by rolling into the next highest-value bounded task when assigned work finishes early.
- 2026-05-09T16:02:34.920556+00:00: Current out-of-scope errors are threshold-margin cases; next gain likely comes from abstention policy refinement and harder negatives.
- 2026-05-09T16:03:37.698226+00:00: Automation model selection is now treated as an operating invariant, not an implicit app default.
- 2026-05-09T16:14:49.435851+00:00: Automation runs now distinguish productive work time from wrap-up time; normal runs should spend at least 50 measured minutes advancing the project.
- 2026-05-09T17:07:37.625326+00:00: Next priority is hard-negative scorer separation and structure mapping repair, not more scaffold work
- 2026-05-09T18:08:06.495922+00:00: remaining bottleneck is separating two ligand-supported metal-like controls without losing retained positives
- 2026-05-09T19:35:11+00:00: The 100-entry slice is clean, but full 125-entry labeling exposes hard redox and metal-like controls; robustness now depends on hard-negative separation and seed-family splits.

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
- 2026-05-09T15:42:05.002091+00:00: Automation handoff now requires origin/main sync verification before the next agent starts.
- 2026-05-09T16:02:34.920556+00:00: Failure analysis is now explicit and reproducible; next bounded step is threshold-policy tuning with guardrails.
- 2026-05-09T16:03:37.698226+00:00: Catalytic Earth automation documentation now forbids downgrading below gpt-5.5 with xhigh reasoning.
- 2026-05-09T16:14:49.435851+00:00: If assigned work finishes or blocks early, agents must switch to the highest-value bounded unblocked task until the 50-minute work boundary.
- 2026-05-09T17:07:37.625326+00:00: 40-entry slice now has 36 labels, 26 evaluable structures, and explicit hard-negative plus structure-mapping blockers
- 2026-05-09T18:08:06.495922+00:00: expanded geometry slice to 60 fully labeled entries with 63 labels
- 2026-05-09T19:35:11+00:00: Expanded the audited geometry slice to 125 fully labeled entries; next scope is reducing 125-entry hard negatives without regressing the clean 20-100 slices.
