# Catalytic Earth Status

Generated from `work/progress_log.jsonl`.

## Time

- Entries: 62
- Measured elapsed time: 2464.1 minutes (41.07 hours)
- Estimated/planned time: 405 minutes (6.75 hours)
- Note: entries before timing instrumentation are estimates, not clock measurements.

## Time By Stage

- ops: 13.4 measured minutes (0.22 hours)
- post-v2: 2386.0 measured minutes (39.77 hours)
- v3: 64.8 measured minutes (1.08 hours)
- ops: 45 estimated minutes (0.75 hours)
- post-v2: 180 estimated minutes (3.00 hours)
- v0: 55 estimated minutes (0.92 hours)
- v1: 55 estimated minutes (0.92 hours)
- v2: 70 estimated minutes (1.17 hours)

## Progress Counters

- Artifact references logged: 640
- Evidence references logged: 532

## Recent Entries

### 2026-05-13T02:01:21.378176+00:00 - post-v2

- Task: Accept gated 975 and 1000 label batches
- Time mode: measured
- Measured minutes: 60.383
- Started: 2026-05-13T01:00:39Z
- Ended: 2026-05-13T02:01:02Z
- Artifacts: artifacts/v3_label_batch_acceptance_check_1000.json, artifacts/v3_label_factory_gate_check_1000.json, artifacts/v3_accepted_review_debt_deferral_audit_1000.json, work/label_preview_1000_notes.md
- Evidence: 206 unit tests passed, validate passed, git diff --check passed, compileall passed, JSON artifact parse passed, 679 countable labels, 0 hard negatives, 0 near misses, 0 out-of-scope false non-abstentions, 0 actionable in-scope failures
- Notes: Normal locked measured run. Accepted 975 and 1000; repaired m_csa:986 heme boundary deferral; documentation updated.

### 2026-05-13T03:55:19.973294+00:00 - post-v2

- Task: Open 1025 preview and scope external transfer
- Time mode: measured
- Measured minutes: 51.6
- Started: 2026-05-13T03:03:14Z
- Ended: 2026-05-13T03:54:50Z
- Artifacts: artifacts/v3_label_factory_gate_check_1025_preview.json, artifacts/v3_label_batch_acceptance_check_1025_preview.json, artifacts/v3_source_scale_limit_audit_1025.json, artifacts/v3_external_source_transfer_manifest_1025.json, artifacts/v3_external_source_query_manifest_1025.json, artifacts/v3_external_ood_calibration_plan_1025.json, artifacts/v3_external_source_candidate_sample_1025.json, artifacts/v3_external_source_candidate_sample_audit_1025.json, docs/external_source_transfer.md, work/label_preview_1025_notes.md
- Evidence: 217 unit tests passed, validate passed, git diff --check passed, compileall passed, JSON artifact parse passed, 21/21 1025 preview gate checks passed, 0 hard negatives, 0 near misses, 0 out-of-scope false non-abstentions, 0 actionable in-scope failures, 0 accepted new labels, 30 external candidates kept non-countable
- Notes: Normal locked measured run. Opened the 1025 preview, kept countable labels at 679, and added review-only external-source transfer scaffolding.

### 2026-05-13T04:55:52.608228+00:00 - post-v2

- Task: Harden external-source transfer gates
- Time mode: measured
- Measured minutes: 50.883
- Started: 2026-05-13T04:04:36Z
- Ended: 2026-05-13T04:55:29Z
- Artifacts: src/catalytic_earth/transfer_scope.py, src/catalytic_earth/cli.py, src/catalytic_earth/labels.py, artifacts/v3_external_source_candidate_manifest_1025.json, artifacts/v3_external_source_evidence_plan_1025.json, artifacts/v3_external_source_active_site_evidence_queue_1025.json, artifacts/v3_external_source_transfer_gate_check_1025.json, docs/external_source_transfer.md, work/handoff.md
- Evidence: 230 unit tests passed, validate passed, git diff check passed, 11/11 external transfer gates, 0 countable external labels, 25 active-site evidence queue rows, 5 deferred external rows
- Notes: Documentation checked and updated during wrap-up; external-source transfer remains gated review-only work.

### 2026-05-13T05:57:24.579339+00:00 - post-v2

- Task: Advance external-source active-site controls
- Time mode: measured
- Measured minutes: 51.35
- Started: 2026-05-13T05:05:40Z
- Ended: 2026-05-13T05:57:01Z
- Artifacts: src/catalytic_earth/adapters.py, src/catalytic_earth/transfer_scope.py, src/catalytic_earth/cli.py, artifacts/v3_external_source_active_site_evidence_sample_1025.json, artifacts/v3_external_source_heuristic_control_queue_1025.json, artifacts/v3_external_source_structure_mapping_plan_1025.json, artifacts/v3_external_source_structure_mapping_sample_1025.json, artifacts/v3_external_source_heuristic_control_scores_1025.json, artifacts/v3_external_source_failure_mode_audit_1025.json, artifacts/v3_external_source_transfer_gate_check_1025.json, docs/external_source_transfer.md, work/handoff.md
- Evidence: 239 unit tests passed, validate passed, git diff check passed, compileall passed, 22/22 external transfer gates, 25 active-site evidence rows sampled, 15 active-site-supported candidates, 4/4 AlphaFold controls mapped, metal-hydrolase top1 collapse recorded, 0 countable external labels
- Notes: Documentation checked and updated during wrap-up; 12 repeated full-suite passes and final verification were clean.

### 2026-05-13T06:58:30.872167+00:00 - post-v2

- Task: Repair external-source transfer controls
- Time mode: measured
- Measured minutes: 51.133
- Started: 2026-05-13T06:06:38Z
- Ended: 2026-05-13T06:57:46Z
- Artifacts: src/catalytic_earth/transfer_scope.py, src/catalytic_earth/cli.py, artifacts/v3_external_source_structure_mapping_sample_1025.json, artifacts/v3_external_source_heuristic_control_scores_1025.json, artifacts/v3_external_source_control_repair_plan_1025.json, artifacts/v3_external_source_representation_control_manifest_1025.json, artifacts/v3_external_source_binding_context_repair_plan_1025.json, artifacts/v3_external_source_binding_context_mapping_sample_1025.json, artifacts/v3_external_source_sequence_holdout_audit_1025.json, artifacts/v3_external_source_reaction_evidence_sample_1025.json, artifacts/v3_external_source_transfer_gate_check_1025.json, docs/external_source_transfer.md, work/external_source_control_repair_1025_notes.md, work/handoff.md
- Evidence: 247 unit tests passed, validate passed, git diff --check passed, compileall passed, JSON artifact parse passed, 33/33 external transfer gates, 12/12 AlphaFold controls mapped, 25 review-only repair rows, 64 Rhea reaction rows, 2 exact-reference holdouts, 0 countable external labels
- Notes: Documentation checked and updated during wrap-up; all external artifacts remain review-only and ready_for_label_import=false.

### 2026-05-13T08:00:59.297672+00:00 - post-v2

- Task: Repair external-source transfer controls
- Time mode: measured
- Measured minutes: 52.083
- Started: 2026-05-13T07:08:09Z
- Ended: 2026-05-13T08:00:14Z
- Artifacts: src/catalytic_earth/transfer_scope.py, src/catalytic_earth/cli.py, tests/test_transfer_scope.py, tests/test_scaling_1025_artifacts.py, artifacts/v3_external_source_representation_control_comparison_1025.json, artifacts/v3_external_source_representation_control_comparison_audit_1025.json, artifacts/v3_external_source_broad_ec_disambiguation_audit_1025.json, artifacts/v3_external_source_active_site_gap_source_requests_1025.json, artifacts/v3_external_source_sequence_neighborhood_plan_1025.json, artifacts/v3_external_source_transfer_gate_check_1025.json, docs/external_source_transfer.md, docs/label_factory.md, docs/v2_strengthening_report.md, work/handoff.md, work/scope.md, work/external_source_control_repair_1025_notes.md, work/external_source_transfer_1025_notes.md, work/label_preview_1025_notes.md, work/label_factory_notes.md
- Evidence: 252 unit tests passed, validate passed, compileall passed, git diff --check passed, JSON artifact parse passed, 38/38 external transfer gates, 12 representation-control comparisons, 7 metal-hydrolase collapse flags, 3 broad-EC rows disambiguated to specific reaction context, 10 active-site gap source requests, 28 near-duplicate sequence search requests, 0 countable external labels
- Notes: Normal locked measured run with at least 50 minutes productive work before wrap-up. Documentation checked and updated; external transfer remains ready_for_label_import=false.

### 2026-05-13T09:00:39.138608+00:00 - post-v2

- Task: Screen external sequence neighborhoods
- Time mode: measured
- Measured minutes: 50.9
- Started: 2026-05-13T03:08:55-05:00
- Ended: 2026-05-13T03:59:49-05:00
- Artifacts: src/catalytic_earth/transfer_scope.py, src/catalytic_earth/cli.py, tests/test_transfer_scope.py, tests/test_scaling_1025_artifacts.py, artifacts/v3_external_source_sequence_neighborhood_sample_1025.json, artifacts/v3_external_source_sequence_neighborhood_sample_audit_1025.json, artifacts/v3_external_source_import_readiness_audit_1025.json, artifacts/v3_external_source_transfer_gate_check_1025.json, docs/external_source_transfer.md, docs/label_factory.md, docs/v2_strengthening_report.md, work/handoff.md, work/scope.md, work/external_source_control_repair_1025_notes.md, work/external_source_transfer_1025_notes.md, work/label_preview_1025_notes.md, work/label_factory_notes.md
- Evidence: 256 unit tests passed, validate passed, compileall passed, git diff --check passed, JSON artifact parse passed, 41/41 external transfer gates, 30 external sequences screened, 733 countable M-CSA reference sequences screened, 0 high-similarity sequence alerts, 0 countable external labels, 0 import-ready external labels, 10 active-site gaps recorded, 9 heuristic scope/top1 mismatches recorded, 29 representation-control issues recorded
- Notes: Normal locked measured run with at least 50 minutes productive work before wrap-up. Documentation checked and updated; external transfer remains ready_for_label_import=false.

### 2026-05-13T10:03:45+00:00 - post-v2

- Task: Tighten external sequence and active-site gates
- Time mode: measured
- Measured minutes: 52.85
- Started: 2026-05-13T09:10:54Z
- Ended: 2026-05-13T10:03:45Z
- Artifacts: src/catalytic_earth/transfer_scope.py, src/catalytic_earth/cli.py, tests/test_transfer_scope.py, tests/test_scaling_1025_artifacts.py, artifacts/v3_external_source_sequence_alignment_verification_1025.json, artifacts/v3_external_source_sequence_alignment_verification_audit_1025.json, artifacts/v3_external_source_active_site_sourcing_queue_1025.json, artifacts/v3_external_source_active_site_sourcing_queue_audit_1025.json, artifacts/v3_external_source_import_readiness_audit_1025.json, artifacts/v3_external_source_transfer_gate_check_1025.json, docs/external_source_transfer.md, docs/label_factory.md, docs/v2_strengthening_report.md, work/handoff.md, work/scope.md, work/external_source_control_repair_1025_notes.md, work/external_source_transfer_1025_notes.md, work/label_preview_1025_notes.md, work/label_factory_notes.md
- Evidence: 259 unit tests passed, validate passed, compileall passed, git diff --check passed, JSON artifact parse passed, CLI help checks passed, 45/45 external transfer gates, 90 sequence-neighborhood top-hit pairs alignment-checked, 2 exact-reference holdouts alignment-confirmed, 10 active-site gaps prioritized, 7 mapped-binding-context sourcing rows, 3 primary active-site source rows, 0 countable external labels, 0 import-ready external labels
- Notes: Normal locked measured run with at least 50 minutes productive work before wrap-up. Documentation checked and updated; external transfer remains ready_for_label_import=false.

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
- 2026-05-10T06:26:21.995107+00:00: The active bottleneck is cobalamin local cofactor evidence for m_csa:494 and preserving countable/review-state separation.
- 2026-05-10T07:28:17.575433+00:00: The active bottleneck moved from the 500 cobalamin deferral to preserving review-state labels while opening a 575-entry tranche.
- 2026-05-10T08:36:59.402518+00:00: The active bottleneck is reviewing the accepted 625 preview before promoting it to canonical labels.
- 2026-05-10T13:59:54.901465+00:00: The active bottleneck is reviewing the accepted 675 preview before promoting it to canonical labels.
- 2026-05-10T14:37:36.208242+00:00: The active bottleneck is auditing the 24 new 675-preview review-debt rows before promotion.
- 2026-05-10T15:39:13.368774+00:00: The active bottleneck is deciding whether to promote m_csa:666 alone or resolve the 61 pending 675-preview review-state rows first.
- 2026-05-10T16:41:45.028412+00:00: Stop further tranche growth at 624 countable labels until 81 review-state rows are triaged or stronger evidence is added.
- 2026-05-10T17:43:34.382296+00:00: Count growth remains stopped at 624 countable labels until accepted-700 review debt has local evidence or explicit expert resolution.
- 2026-05-10T18:46:18.139775+00:00: Next bottleneck is auditing m_csa:577 m_csa:592 and m_csa:641 remap-local leads against counterevidence before any further gated scaling.
- 2026-05-10T19:48:49.955298+00:00: Next bottleneck is deciding whether kinase/phosphoryl-transfer mismatch rows need an ontology-family rule or expert reaction/substrate export before more count growth.
- 2026-05-10T20:50:01.204415+00:00: Next bottleneck shifts from detecting reaction/substrate mismatch lanes to reducing review-only debt without expert-authority count growth.
- 2026-05-10T22:51:19.534178+00:00: Next bottleneck is reducing expert-label decision review-only debt with evidence repair, not opening 725+ count growth.
- 2026-05-10T23:56:45.965586+00:00: Next run should reduce expert-label repair debt or harden local-evidence checks before opening any 725+ tranche.
- 2026-05-11T03:12:54.274263+00:00: Next bottleneck is resolving one local-evidence repair lane from the 21-row plan before count growth.
- 2026-05-12T15:04:26.275853+00:00: After prioritized scientific expansion is implemented and guardrail-clean, agents should resume factory-gated label expansion while preserving label quality and import-safety controls.
- 2026-05-12T16:42:24.970333+00:00: Keep ATP families as boundary evidence; stop scaling if next gate exposes quality drift.
- 2026-05-12T17:48:03.708741+00:00: Next run should repair or explicitly defer the accepted-725 review-debt surface before blind 750 scaling.
- 2026-05-12T18:52:33.655337+00:00: Next run should repair or explicitly defer the 18 new 750-preview review-debt rows before promoting seven clean candidates.
- 2026-05-12T20:14:45.382801+00:00: 750 review debt can be explicitly deferred without weakening countable-label gates; resume bounded scaling toward 1,000 labels.
- 2026-05-12T21:46:07.698000+00:00: Countable registry is 642 labels; the label factory remains below the 1000-label milestone and should continue bounded batches with quality repair on any gate failure.
- 2026-05-12T22:58:26.440004+00:00: Countable registry is 652 labels; next bounded work is an 875 preview while post-850 gate stays clean.
- 2026-05-13T00:50:52.831198+00:00: Countable registry is 673 labels; next bounded work is a 975 preview while post-950 gate stays clean.
- 2026-05-13T02:01:21.378176+00:00: Low-score local heme boundary rows now defer instead of becoming countable out-of-scope negatives.
- 2026-05-13T03:55:19.973294+00:00: The 1,025 preview is guardrail-clean but non-promotable; 10k progress now depends on external-source transfer rather than another M-CSA-only tranche.
- 2026-05-13T04:55:52.608228+00:00: Next bounded work should use the active-site evidence queue for external candidates while keeping all external rows non-countable.
- 2026-05-13T05:57:24.579339+00:00: External transfer remains review-only; repair active-site feature gaps and heuristic metal-hydrolase collapse before any label import.
- 2026-05-13T06:58:30.872167+00:00: External transfer remains non-countable; next bounded work should source active-site evidence for 10 gaps, disambiguate 3 broad-EC rows, and prototype representation controls for 12 mapped controls.

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
- 2026-05-10T06:26:21.995107+00:00: 500-slice label scaling now has countable batch import and acceptance checks; next scope is resolving m_csa:494, not opening a 525-label tranche.
- 2026-05-10T07:28:17.575433+00:00: Label-factory scaling can continue from the 550 review-state registry; next tranche should use 546 as the countable baseline.
- 2026-05-10T08:36:59.402518+00:00: Post-V2 geometry scope now tracks accepted 600-entry countable labels and a generated 625-entry preview batch.
- 2026-05-10T13:59:54.901465+00:00: Post-V2 geometry scope now tracks accepted 650-entry countable labels and a generated 675 preview batch.
- 2026-05-10T14:37:36.208242+00:00: Post-V2 label-factory scope now separates preview mechanical acceptance from promotion readiness with carried/new review-debt metadata.
- 2026-05-10T15:39:13.368774+00:00: Post-V2 label-factory scope now blocks accepted review-gap labels, attaches scaling-quality audits to preview summaries, and records the missing sequence-cluster artifact before promotion.
- 2026-05-10T16:41:45.028412+00:00: 700-entry slice is guardrail-clean for clean labels; next bounded work is review-debt repair, not blind expansion.
- 2026-05-10T17:43:34.382296+00:00: Review-debt repair now separates alternate-structure cofactor leads from local active-site evidence before any further gated scaling.
- 2026-05-10T18:46:18.139775+00:00: Alternate-PDB residue remapping now produces review-only local evidence leads but does not reopen count growth.
- 2026-05-10T19:48:49.955298+00:00: 700 scaling remains stopped at 624 countable labels until reaction/substrate mismatch lanes are resolved by ontology rule or expert review.
- 2026-05-10T20:50:01.204415+00:00: 700 scaling remains stopped at 624 countable labels; reaction/substrate mismatch lanes now require complete expert-review export before more count growth.
- 2026-05-10T22:51:19.534178+00:00: 700 scaling remains at 624 countable labels; active expert-label decision lanes now require complete non-countable review export and repair-candidate coverage before any further gated growth.
- 2026-05-10T23:56:45.965586+00:00: 700 scaling remains at 624 countable labels; this run added repair guardrails and discovery-facing controls instead of count growth because review debt remains the limiting gate.
- 2026-05-11T03:12:54.274263+00:00: 700 factory gate now requires local-evidence gap audit and review-only export before count growth.
- 2026-05-12T15:04:26.275853+00:00: Expert-reviewed ATP/phosphoryl-transfer mismatch lanes now drive aggressive fingerprint-family ontology expansion for ePK ASKHA ATP-grasp GHKL dNK NDK PfkA PfkB and GHMP before returning to 10k gated label scaling.
- 2026-05-12T16:42:24.970333+00:00: Nine-family ATP/phosphoryl-transfer expansion is complete; next bounded work can resume factory-gated scaling toward 725.
- 2026-05-12T17:48:03.708741+00:00: Accepted 725 as the latest gated countable slice: 630 countable labels and 100 review-state rows kept non-countable.
- 2026-05-12T18:52:33.655337+00:00: Accepted-725 review debt is explicitly deferred; 750 preview is open but not canonical.
- 2026-05-12T20:14:45.382801+00:00: Accepted 750 as latest gated countable slice; next bounded work is a 775 preview only while the 750 post-batch gate stays clean.
- 2026-05-12T21:46:07.698000+00:00: Accepted 775 as latest gated countable slice; next bounded work is an 800 preview only while the 775 post-batch gate stays clean.
- 2026-05-12T22:58:26.440004+00:00: Accepted 850 as latest gated countable slice; geometry row reuse added for tranche scaling.
- 2026-05-13T00:50:52.831198+00:00: Accepted 950 as latest gated countable slice; review-debt deferral remains mandatory before 1,000-label milestone.
- 2026-05-13T02:01:21.378176+00:00: Accepted 1000 as latest gated countable slice; next bounded tranche is 1025 only while post-1000 gates stay clean.
- 2026-05-13T03:55:19.973294+00:00: M-CSA-only scaling is source-limited at 1,003 observed records; next work should build external-source transfer with all imported candidates non-countable until full factory gates pass.
- 2026-05-13T04:55:52.608228+00:00: M-CSA-only scaling remains stopped at 1,003 observed source records; external-source transfer is review-only evidence collection until active-site evidence OOD sequence holdouts heuristic controls decisions and factory gates pass.
- 2026-05-13T05:57:24.579339+00:00: M-CSA-only count growth remains stopped at 1,003 observed records; post-M-CSA scaling now depends on active-site-supported external controls plus representation or ontology repairs.
- 2026-05-13T06:58:30.872167+00:00: M-CSA-only count growth remains stopped at 1,003 observed records; post-M-CSA scaling still depends on review-only external-source repair and representation controls before label import.
- 2026-05-13T08:00:59.297672+00:00: Post-M-CSA scaling remains review-only; next import readiness depends on active-site sourcing, near-duplicate sequence search, and real representation controls before any external label decision.
- 2026-05-13T09:00:39.138608+00:00: External transfer remains non-countable; next import readiness depends on active-site sourcing, complete near-duplicate sequence search, and real representation controls before any external decision.
- 2026-05-13T10:03:45+00:00: External transfer remains non-countable; next import readiness depends on sourcing explicit active-site evidence, completing near-duplicate sequence search, and replacing feature-proxy representation controls before any external decision.
