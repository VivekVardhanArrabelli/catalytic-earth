# Catalytic Earth Status

Generated from `work/progress_log.jsonl`.

## Time

- Entries: 31
- Measured elapsed time: 684.6 minutes (11.41 hours)
- Estimated/planned time: 405 minutes (6.75 hours)
- Note: entries before timing instrumentation are estimates, not clock measurements.

## Time By Stage

- ops: 13.4 measured minutes (0.22 hours)
- post-v2: 671.2 measured minutes (11.19 hours)
- ops: 45 estimated minutes (0.75 hours)
- post-v2: 180 estimated minutes (3.00 hours)
- v0: 55 estimated minutes (0.92 hours)
- v1: 55 estimated minutes (0.92 hours)
- v2: 70 estimated minutes (1.17 hours)

## Progress Counters

- Artifact references logged: 281
- Evidence references logged: 204

## Recent Entries

### 2026-05-09T22:17:13.285127+00:00 - post-v2

- Task: Audit cofactor coverage and evidence-limited geometry failures
- Time mode: measured
- Measured minutes: 54.0
- Started: 2026-05-09T21:22:55Z
- Ended: 2026-05-09T22:16:55Z
- Artifacts: src/catalytic_earth/structure.py, src/catalytic_earth/labels.py, src/catalytic_earth/geometry_reports.py, src/catalytic_earth/cli.py, src/catalytic_earth/performance.py, data/registries/curated_mechanism_labels.json, artifacts/v3_cofactor_coverage_150.json, artifacts/v3_geometry_slice_summary.json, artifacts/v3_in_scope_failure_analysis_150.json, README.md, docs/geometry_features.md, docs/performance.md, docs/v2_strengthening_report.md, work/handoff.md, work/scope.md
- Evidence: 75 unit tests passed, validate passed, 150 labels, 44 in-scope positives, 106 out-of-scope controls, 0 hard negatives across slices, 0 out-of-scope false non-abstentions, 1 evidence-limited in-scope abstention, 0 actionable in-scope failures, cofactor coverage artifacts generated, evidence-limited retained positives flagged
- Notes: documentation reviewed and updated; final diff check, validate, and 75-test suite passed

### 2026-05-09T23:20:32.069816+00:00 - post-v2

- Task: Expand geometry benchmark to 175 labels and near-miss audits
- Time mode: measured
- Measured minutes: 55.7
- Started: 2026-05-09T22:24:24Z
- Ended: 2026-05-09T23:20:06Z
- Artifacts: src/catalytic_earth/labels.py, src/catalytic_earth/geometry_retrieval.py, src/catalytic_earth/structure.py, src/catalytic_earth/geometry_reports.py, src/catalytic_earth/cli.py, src/catalytic_earth/performance.py, data/registries/curated_mechanism_labels.json, artifacts/v1_graph_175.json, artifacts/v3_geometry_retrieval_175.json, artifacts/v3_geometry_label_eval_175.json, artifacts/v3_hard_negative_controls_175.json, artifacts/v3_cofactor_policy_175.json, artifacts/v3_seed_family_performance_175.json, artifacts/v3_geometry_slice_summary.json, artifacts/perf_report.json, README.md, docs/geometry_features.md, docs/performance.md, docs/v2_strengthening_report.md, docs/v2_report.md, work/handoff.md, work/scope.md
- Evidence: 79 unit tests passed, validate passed, 175 curated labels, 175 geometry entries, 173 evaluable structures, 59 in-scope positives, 116 out-of-scope controls, 0 hard negatives, 0 out-of-scope false non-abstentions, 17 near misses, 1 evidence-limited in-scope abstention, 0 actionable in-scope failures, cofactor policy recommends audit-only handling
- Notes: documentation reviewed and updated; final diff check, validate, and 79-test suite passed

### 2026-05-10T00:22:01.303388+00:00 - post-v2

- Task: Expand geometry benchmark to 225 labels and clear hard negatives
- Time mode: measured
- Measured minutes: 55.184
- Started: 2026-05-09T18:26:28.820122-05:00
- Ended: 2026-05-09T19:21:39.866381-05:00
- Artifacts: src/catalytic_earth/geometry_retrieval.py, src/catalytic_earth/labels.py, src/catalytic_earth/geometry_reports.py, src/catalytic_earth/structure.py, data/registries/curated_mechanism_labels.json, artifacts/v1_graph_225.json, artifacts/v3_geometry_features_225.json, artifacts/v3_geometry_retrieval_225.json, artifacts/v3_geometry_label_eval_225.json, artifacts/v3_hard_negative_controls_225.json, artifacts/v3_cofactor_policy_225.json, artifacts/v3_geometry_slice_summary.json, artifacts/perf_report.json, README.md, docs/geometry_features.md, docs/performance.md, docs/v2_strengthening_report.md, docs/v2_report.md, work/handoff.md, work/scope.md
- Evidence: 85 unit tests passed; validate passed; 225 curated labels; 224 geometry entries; 221 evaluable structures; 71 in-scope positives; 153 evaluated out-of-scope controls; 0 hard negatives; 0 near misses; 0 out-of-scope false non-abstentions; 1 evidence-limited in-scope abstention; 0 actionable in-scope failures

### 2026-05-10T01:18:40.670377+00:00 - post-v2

- Task: Expand geometry benchmark to 275 labels and text counterevidence
- Time mode: measured
- Measured minutes: 50.45
- Started: 2026-05-10T00:27:55Z
- Ended: 2026-05-10T01:18:22Z
- Artifacts: data/registries/curated_mechanism_labels.json, artifacts/v3_geometry_retrieval_275.json, artifacts/v3_geometry_label_eval_275.json, artifacts/v3_geometry_slice_summary.json, artifacts/perf_report.json
- Evidence: 96 unit tests passed, validate passed, 275 labels, 0 hard negatives, 0 near misses, 0 out-of-scope false non-abstentions, 0 actionable in-scope failures
- Notes: Added mechanism-text counterevidence and propagated entry names/snippets into review artifacts.

### 2026-05-10T02:23:20.695520+00:00 - post-v2

- Task: Expand geometry benchmark to 375 labels and queue 400
- Time mode: measured
- Measured minutes: 54.25
- Started: 2026-05-10T01:28:55Z
- Ended: 2026-05-10T02:23:10Z
- Artifacts: data/registries/curated_mechanism_labels.json, src/catalytic_earth/geometry_retrieval.py, src/catalytic_earth/geometry_reports.py, artifacts/v3_geometry_retrieval_375.json, artifacts/v3_geometry_label_eval_375.json, artifacts/v3_geometry_slice_summary.json, artifacts/v3_label_expansion_candidates_400.json, artifacts/perf_report.json, README.md, docs/geometry_features.md, work/handoff.md, work/scope.md
- Evidence: 105 unit tests passed, validate passed, 375 curated labels, 374 geometry entries in 375 slice, 367 evaluable structures, 98 in-scope positives, 276 out-of-scope controls, 0 hard negatives, 0 near misses, 0 out-of-scope false non-abstentions, 0 actionable in-scope failures, 400-entry queue has 22 ready label-review candidates
- Notes: Documentation checked and updated during wrap-up; normal measured run.

### 2026-05-10T03:26:17.876722+00:00 - post-v2

- Task: Expand geometry benchmark to 450 labels
- Time mode: measured
- Measured minutes: 55.517
- Started: 2026-05-10T02:30:25Z
- Ended: 2026-05-10T03:25:56Z
- Artifacts: data/registries/curated_mechanism_labels.json, src/catalytic_earth/geometry_retrieval.py, src/catalytic_earth/geometry_reports.py, artifacts/v3_geometry_label_eval_450.json, artifacts/v3_hard_negative_controls_450.json, artifacts/v3_geometry_slice_summary.json, artifacts/v3_label_expansion_candidates_475.json, artifacts/perf_report.json, README.md, docs/geometry_features.md, docs/v2_strengthening_report.md, docs/performance.md, docs/v2_report.md, work/handoff.md, work/scope.md
- Evidence: 113 unit tests passed, validate passed, 450 curated labels, 449 geometry entries in 450 slice, 442 evaluable structures, 124 in-scope positives, 325 out-of-scope controls, 0 hard negatives, 0 near misses, 0 out-of-scope false non-abstentions, 0 actionable in-scope failures, 475-entry queue has 23 ready label-review candidates
- Notes: Documentation reviewed and updated during wrap-up; normal measured run.

### 2026-05-10T04:23:35.521223+00:00 - post-v2

- Task: Expand geometry benchmark to 475 labels and queue 500
- Time mode: measured
- Measured minutes: 51.767
- Started: 2026-05-10T03:31:20Z
- Ended: 2026-05-10T04:23:06Z
- Artifacts: data/registries/curated_mechanism_labels.json, src/catalytic_earth/geometry_retrieval.py, src/catalytic_earth/geometry_reports.py, src/catalytic_earth/structure.py, artifacts/v3_geometry_label_eval_475.json, artifacts/v3_hard_negative_controls_475.json, artifacts/v3_geometry_slice_summary.json, artifacts/v3_label_expansion_candidates_500.json, artifacts/perf_report.json, work/label_queue_500_notes.md, README.md, docs/geometry_features.md, work/handoff.md, work/scope.md
- Evidence: 116 unit tests passed, validate passed, 475 curated labels, 474 geometry entries in 475 slice, 467 evaluable structures, 127 in-scope positives, 347 out-of-scope controls, 0 hard negatives, 0 near misses, 0 out-of-scope false non-abstentions, 0 actionable in-scope failures, 500-entry queue has 21 ready label-review candidates
- Notes: Documentation reviewed and updated during wrap-up; normal measured run.

### 2026-05-10T05:25:09.634817+00:00 - post-v2

- Task: Build label factory automation gate
- Time mode: measured
- Measured minutes: 51.383
- Started: 2026-05-10T04:33:25Z
- Ended: 2026-05-10T05:24:48Z
- Artifacts: src/catalytic_earth/labels.py, src/catalytic_earth/cli.py, src/catalytic_earth/ontology.py, src/catalytic_earth/automation.py, src/catalytic_earth/performance.py, data/registries/curated_mechanism_labels.json, data/registries/mechanism_ontology.json, artifacts/v3_label_factory_audit_475.json, artifacts/v3_label_factory_applied_labels_475.json, artifacts/v3_adversarial_negative_controls_475.json, artifacts/v3_active_learning_review_queue_500.json, artifacts/v3_expert_review_export_500.json, artifacts/v3_expert_review_import_preview_500.json, artifacts/v3_family_propagation_guardrails_500.json, artifacts/v3_label_factory_gate_check_500.json, artifacts/perf_report.json, docs/label_factory.md, README.md, work/handoff.md, work/scope.md, work/label_factory_notes.md
- Evidence: 130 unit tests passed, validate passed, 475 explicit tiered labels, 61 silver promotions proposed, 98 review labels proposed, 100 adversarial negatives mined, 123 active-learning rows queued, all 25 unlabeled candidates exported for review, 9 label-factory gates passed, automation-lock CLI tested, documentation reviewed and updated
- Notes: documentation reviewed and updated; normal measured run

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
- 2026-05-09T19:52:34.146667+00:00: The main 125-entry bottleneck is no longer hidden heme-absent overlap; remaining controls concentrate in metal-like and Ser-His-like groups.
- 2026-05-09T20:12:10.878697+00:00: End-of-run quality now includes documentation freshness, not only code artifacts and git cleanliness.
- 2026-05-09T21:11:49.565784+00:00: Hard-negative separation is clean through the 150-entry slice; next quality bottleneck is evidence-limited in-scope positives with missing local cofactor context.
- 2026-05-09T22:17:13.285127+00:00: The main 150-entry bottleneck is retained positives without selected-structure cofactor evidence, not hard-negative separation
- 2026-05-09T23:20:32.069816+00:00: The 175-entry bottleneck is now near-miss metal-hydrolase controls and fragile evidence-limited retained positives, not hard-negative separation.
- 2026-05-10T00:22:01.303388+00:00: The 225-entry bottleneck is now the selected-structure cofactor gap for m_csa:132 or the next label expansion, not hard-negative separation.
- 2026-05-10T01:18:40.670377+00:00: Next bottleneck is expanding beyond 275 labels or resolving m_csa:132 selected-structure cofactor absence.
- 2026-05-10T02:23:20.695520+00:00: The benchmark can expand in 25-entry curation tranches while preserving guardrails; the next bottleneck is 400-entry label quality and evidence-limited cofactor gaps.
- 2026-05-10T03:26:17.876722+00:00: The benchmark can continue expanding in curated 25-entry tranches, but the next bottleneck is 475-entry label quality and evidence-limited cofactor gaps.
- 2026-05-10T04:23:35.521223+00:00: The benchmark can keep expanding in 25-entry curation tranches; next bottleneck is 500-entry label quality and evidence-limited cofactor gaps.
- 2026-05-10T05:25:09.634817+00:00: Next bottleneck is importing decisions from the 500 queue through the label factory rather than expanding labels directly.

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
- 2026-05-09T19:52:34.146667+00:00: 125-entry hard-negative controls are now grouped and anchored to correctly ranked positives; next scorer work should target the largest grouped control clusters.
- 2026-05-09T20:12:10.878697+00:00: Every automation wrap-up must update stale README/docs/work files or explicitly record that documentation was checked and unchanged.
- 2026-05-09T21:11:49.565784+00:00: Post-V2 geometry scope now tracks 150 labeled entries with cross-slice summary artifacts and in-scope failure analysis.
- 2026-05-09T22:17:13.285127+00:00: 150-entry geometry scope now separates local active-site positives from enzyme-level labels and tracks cofactor coverage explicitly
- 2026-05-09T23:20:32.069816+00:00: Post-V2 geometry scope now tracks 175 fully labeled entries with cofactor policy and seed-family audits.
- 2026-05-10T00:22:01.303388+00:00: Post-V2 geometry scope now tracks a fully labeled 225-entry source slice with 12 cross-slice summaries and clean hard-negative guardrails.
- 2026-05-10T01:18:40.670377+00:00: Post-V2 geometry scope now tracks a fully labeled 275-entry source slice.
- 2026-05-10T02:23:20.695520+00:00: Post-V2 geometry scope now tracks a fully labeled 375-entry source slice and a generated 400-entry candidate queue.
- 2026-05-10T03:26:17.876722+00:00: Post-V2 geometry scope now tracks a fully labeled 450-entry source slice and a generated 475-entry candidate queue.
- 2026-05-10T04:23:35.521223+00:00: Post-V2 geometry scope now tracks a fully labeled 475-entry source slice and a generated 500-entry candidate queue.
- 2026-05-10T05:25:09.634817+00:00: Label scaling is now factory-gated; new labels must pass promotion, demotion, adversarial-negative, active-learning, expert-review, family-propagation, validation, and test checks before counting.
