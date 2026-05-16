# Catalytic Earth Status

Generated from `work/progress_log.jsonl`.

## Time

- Entries: 135
- Measured elapsed time: 4610.3 minutes (76.84 hours)
- Estimated/planned time: 405 minutes (6.75 hours)
- Note: entries before timing instrumentation are estimates, not clock measurements.

## Time By Stage

- external-transfer-spof-hardening: 186.5 measured minutes (3.11 hours)
- ops: 51.4 measured minutes (0.86 hours)
- post-mcsa-spof-hardening: 1764.6 measured minutes (29.41 hours)
- post-v2: 2542.9 measured minutes (42.38 hours)
- v3: 64.8 measured minutes (1.08 hours)
- ops: 45 estimated minutes (0.75 hours)
- post-v2: 180 estimated minutes (3.00 hours)
- v0: 55 estimated minutes (0.92 hours)
- v1: 55 estimated minutes (0.92 hours)
- v2: 70 estimated minutes (1.17 hours)

## Progress Counters

- Artifact references logged: 1559
- Evidence references logged: 1183

## Recent Entries

### 2026-05-16T11:15:09.904197+00:00 - external-transfer-spof-hardening

- Task: Complete external structural pair cache and split plan
- Time mode: measured
- Measured minutes: 13.667
- Started: 2026-05-16T11:01:29Z
- Ended: 2026-05-16T11:15:09Z
- Artifacts: artifacts/v3_external_structural_cluster_index_1025_all30.json, artifacts/v3_external_structural_tm_diverse_split_plan_1025_all30.json, src/catalytic_earth/transfer_scope.py, src/catalytic_earth/cli.py, tests/test_external_structural_holdout_artifact.py, tests/test_transfer_scope.py, README.md, docs/external_source_transfer.md, docs/label_factory.md, work/handoff.md, work/scope.md, work/foldseek_readiness_notes.md, work/external_source_transfer_1025_notes.md, work/label_preview_1025_notes.md
- Evidence: startup 354 unit tests passed, startup validate passed with 679 curated labels, Foldseek all-30 external cache completed 435/435 unordered nonself pairs with 900 directed rows, review-only external structural split assigned 6 test and 24 train rows, max cross-split TM-score 0.6963, 0 cross-split TM>=0.7 violations, 0 import-ready rows and 0 countable external labels, final 356 unit tests passed, final validate passed, compileall passed, git diff check passed
- Notes: Normal locked direct run with no delegation. M-CSA strict TM repair stayed closed; no external rows became countable or import-ready.

### 2026-05-16T12:15:25.647551+00:00 - external-transfer-spof-hardening

- Task: External pilot decision confidence audit
- Time mode: measured
- Measured minutes: 13.501
- Started: 2026-05-16T07:01:54.930663-05:00
- Ended: 2026-05-16T12:15:25Z
- Artifacts: artifacts/v3_external_source_pilot_decision_confidence_audit_1025.json, artifacts/v3_external_source_pilot_decisions_review_normalized_1025.json, artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_1025.json, src/catalytic_earth/transfer_scope.py, src/catalytic_earth/cli.py, tests/test_scaling_1025_artifacts.py, README.md, docs/external_source_transfer.md, work/handoff.md, work/scope.md
- Evidence: startup 356 unit tests passed, startup validate passed with 679 curated labels, final 357 unit tests passed, final validate passed, compileall passed, git diff check passed, 10 selected pilot terminal decisions audited, 3 weak representation-only duplicate rejections normalized to needs_review, 6 needs_review rows routed, 0 import-ready rows, 0 countable external labels
- Notes: Normal locked direct run with no delegation. M-CSA strict TM repair stayed closed; external pilot confidence was audited before any expansion or import.

### 2026-05-16T13:07:13+00:00 - external-transfer-spof-hardening

- Task: External pilot confidence audit verification
- Time mode: measured
- Measured minutes: 4.733
- Started: 2026-05-16T13:02:29Z
- Ended: 2026-05-16T13:07:13Z
- Artifacts: artifacts/v3_external_source_pilot_decision_confidence_audit_1025.json, artifacts/v3_external_source_pilot_decisions_review_normalized_1025.json, artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_1025.json, docs/external_source_transfer.md, work/handoff.md
- Evidence: startup 357 unit tests passed, startup validate passed with 679 curated labels, confidence and normalization CLIs reran idempotently, normalized six needs_review rows verified, 0 import-ready rows and 0 countable external labels, final 357 unit tests passed, final validate passed, compileall passed, git diff check passed
- Notes: Normal locked direct run with no delegation. Latest pushed audit already satisfied the immediate confidence-audit instruction; this run verified it, updated stale next-work guidance, and kept M-CSA strict TM repair closed.

### 2026-05-16T14:26:15.956789+00:00 - external-transfer-spof-hardening

- Task: External all-vs-all duplicate screen
- Time mode: measured
- Measured minutes: 22.317
- Started: 2026-05-16T09:03:56-05:00
- Ended: 2026-05-16T09:26:15-05:00
- Artifacts: artifacts/v3_external_source_all_vs_all_sequence_search_1025.json, artifacts/v3_external_source_all_vs_all_sequence_search_audit_1025.json, artifacts/v3_external_source_pilot_decision_confidence_audit_1025.json, artifacts/v3_external_source_pilot_decisions_review_normalized_1025.json, artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_1025.json, src/catalytic_earth/transfer_scope.py, src/catalytic_earth/cli.py, tests/test_transfer_scope.py, tests/test_scaling_1025_artifacts.py, README.md, docs/external_source_transfer.md, docs/label_factory.md, work/handoff.md, work/scope.md
- Evidence: startup 357 unit tests passed, startup validate passed with 679 curated labels, all-vs-all MMseqs2 searched 30 external candidates, 0 external all-vs-all near-duplicate pairs, max external-external identity 0.647, confidence audit remains 6 needs_review and 0 import-ready rows, external transfer gate 68/68, final 358 unit tests passed, final validate passed, compileall passed, git diff check passed
- Notes: Normal locked direct run with no delegation. M-CSA strict TM repair stayed closed; no external rows became countable or import-ready.

### 2026-05-16T15:22:11.987493+00:00 - external-transfer-spof-hardening

- Task: Resolve external pilot needs_review rows
- Time mode: measured
- Measured minutes: 17.783
- Started: 2026-05-16T15:04:24Z
- Ended: 2026-05-16T15:22:11Z
- Artifacts: artifacts/v3_external_source_pilot_needs_review_resolution_1025.json, artifacts/v3_external_source_pilot_decisions_review_resolved_1025.json, artifacts/v3_external_source_pilot_human_expert_review_queue_resolved_1025.json, tests/test_scaling_1025_artifacts.py, README.md, docs/external_source_transfer.md, work/handoff.md, work/scope.md, work/external_source_transfer_1025_notes.md
- Evidence: startup 358 unit tests passed, startup validate passed with 679 curated labels, targeted UniRef90/50 mapping found 0 shared nearest-reference clusters, 6 needs_review rows resolved as rejected_representation_conflict, 0 import-ready rows and 0 countable external labels, final 359 unit tests passed, final validate passed, compileall passed, git diff check passed
- Notes: Normal locked direct run with no delegation. M-CSA strict TM repair stayed closed; no external rows became countable or import-ready.

### 2026-05-16T16:17:35.092187+00:00 - external-transfer-spof-hardening

- Task: Assign external pilot mechanism repair lanes
- Time mode: measured
- Measured minutes: 12.617
- Started: 2026-05-16T16:04:57Z
- Ended: 2026-05-16T16:17:34Z
- Artifacts: artifacts/v3_external_source_pilot_mechanism_repair_lanes_1025.json, src/catalytic_earth/transfer_scope.py, src/catalytic_earth/cli.py, tests/test_transfer_scope.py, tests/test_scaling_1025_artifacts.py, README.md, docs/external_source_transfer.md, work/handoff.md, work/scope.md, work/external_source_transfer_1025_notes.md
- Evidence: startup 359 unit tests passed, startup validate passed with 679 curated labels, 6 resolved representation conflicts assigned to review-only mechanism repair lanes, 0 needs_review rows, 0 import-ready rows, 0 countable external labels, final 360 unit tests passed, final validate passed, compileall passed, git diff check passed
- Notes: Normal locked direct run with no delegation. M-CSA strict TM repair stayed closed; docs/label_factory.md checked unchanged.

### 2026-05-16T17:21:15.343286+00:00 - external-transfer-spof-hardening

- Task: Stage SDR redox repair control
- Time mode: measured
- Measured minutes: 19.667
- Started: 2026-05-16T17:06:39Z
- Ended: 2026-05-16T17:26:19Z
- Artifacts: artifacts/v3_external_source_pilot_sdr_redox_repair_control_1025.json, src/catalytic_earth/transfer_scope.py, src/catalytic_earth/cli.py, tests/test_transfer_scope.py, tests/test_scaling_1025_artifacts.py, README.md, docs/external_source_transfer.md, work/handoff.md, work/scope.md, work/external_source_transfer_1025_notes.md, local main commit ahead of origin/main
- Evidence: startup 360 unit tests passed, startup validate passed with 679 curated labels, SDR/NAD(P) O14756 repair lane staged as review-only sequence-derived control, candidate has TGxxxGxG and source-active-site-overlapping YxxxK proxies, conflicting current-reference neighbors lack complete SDR axis, 0 import-ready rows and 0 countable external labels, final 361 unit tests passed, final validate passed, compileall passed, git diff check passed, push blocked: invalid local GitHub credential
- Notes: Normal locked direct run with no delegation. M-CSA strict TM repair stayed closed; docs/label_factory.md checked unchanged. Push blocked by invalid local GitHub credential; coherent local commit remains ahead of origin/main for recovery.

### 2026-05-16T20:03:03.218017+00:00 - external-transfer-spof-hardening

- Task: Integrate SDR import-safety adjudication and stage glycoside boundary control
- Time mode: measured
- Measured minutes: 17.6
- Started: 2026-05-16T19:45:17Z
- Ended: 2026-05-16T20:02:53Z
- Artifacts: artifacts/v3_external_source_pilot_sdr_redox_import_safety_adjudication_1025.json, artifacts/v3_external_source_pilot_glycoside_hydrolase_boundary_control_1025.json, src/catalytic_earth/transfer_scope.py, src/catalytic_earth/cli.py, tests/test_transfer_scope.py, tests/test_scaling_1025_artifacts.py, README.md, docs/external_source_transfer.md, work/handoff.md, work/scope.md, work/external_source_transfer_1025_notes.md
- Evidence: startup 361 unit tests passed, startup validate passed with 679 curated labels, O14756 SDR/NAD(P) import-safety adjudication repaired representation conflict, post-repair O14756 status remains needs_review, Q6NSJ0 glycoside hydrolase boundary control staged as review-only non-text evidence, 0 import-ready rows and 0 countable external labels, final 363 unit tests passed, final validate passed, compileall passed, git diff check passed
- Notes: Normal locked direct run with no delegation. M-CSA strict TM repair stayed closed; docs/label_factory.md checked unchanged. O14756 is no longer blocked by representation conflict alone, but duplicate review and full factory gates still block import.

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
- 2026-05-13T12:55:17.737175+00:00: The next useful milestone is pilot import readiness for named external candidates, not a higher external-transfer gate count.
- 2026-05-13T13:02:54.457092+00:00: The next run should implement holdout/generalization evaluation first; external pilot work resumes after that signal or in parallel only when directly unblocking import readiness.
- 2026-05-13T17:47:33.256358+00:00: External pilot now has per-candidate review dossiers; next work should fill decisions and missing evidence, not add generic gates.
- 2026-05-13T18:44:44.009443+00:00: External pilot import remains blocked; next work should fill real active-site and sequence evidence decisions rather than expanding gate count.
- 2026-05-13T19:39:20.606270+00:00: External pilot import remains blocked; high-fan-in gate maintenance is reduced, but active-site source decisions and complete near-duplicate search remain the next blockers.
- 2026-05-13T20:51:07.000000+00:00: Geometry retrieval predictive evidence is now explicitly text-free; PLP positive signal uses local ligand-anchor context
- 2026-05-13T22:04:23.805937+00:00: M-CSA-only growth remains stopped; next external-pilot work should fill real sequence-search and active-site decisions rather than add generic gates.
- 2026-05-13T22:34:16.818554+00:00: External transfer remains non-countable; complete UniRef/all-vs-all sequence search and active-site evidence decisions still block import.
- 2026-05-13T23:52:26.926762+00:00: external pilot can proceed to review decisions only after active-site sources and complete sequence search; no external import is ready
- 2026-05-14T00:43:19.772463+00:00: Artifact graph consistency still matters at count-decision boundaries; next work should fill external pilot evidence decisions rather than add generic gates.
- 2026-05-14T03:08:19.594666+00:00: External pilot remains review-only; next highest-value work is coordinate staging for TM-score only if it directly unblocks pilot import readiness, plus active-site source decisions and complete near-duplicate search.
- 2026-05-14T04:23:49.348241+00:00: Next useful external-pilot work is active-site source decisions and representation repair for selected rows; M-CSA-only count growth remains stopped.
- 2026-05-14T05:08:05.672183+00:00: Full TM-score split remains blocked until remaining selected coordinates are staged and a Foldseek-backed split builder is added; partial staged25 TM signal is review-only evidence.
- 2026-05-14T05:12:09.497043+00:00: Foldseek artifacts now have regression coverage; full TM-score split remains blocked until the remaining selected coordinates and split builder are implemented.
- 2026-05-14T09:28:41.519786+00:00: Expanded40 Foldseek raw-name mapping is no longer a blocker, but the partial staged-coordinate TM signal still fails the <0.7 target and full TM-score split remains blocked on full coordinate coverage plus a split builder.
- 2026-05-14T10:16:36.145071+00:00: Requested 650M representation remains blocked by local cache/disk/CPU limits; largest feasible cached ESM-2 150M now gives a real review-only control signal while Foldseek remains partial and fails the <0.7 target.
- 2026-05-14T11:07:34.295381+00:00: Next work should run a full Foldseek/TM-score split only after resolving missing selected structures and should advance pilot rows through broader duplicate screening, representation review, and review decisions without countable import.
- 2026-05-14T12:34:37.036864+00:00: Next agent should retry the all-materializable Foldseek TM-score signal as delegated backend work or emit a bounded larger-than-40 completed signal without false full-holdout claims.
- 2026-05-14T12:50:26.982940+00:00: Sequence-distance holdout is real backend evidence; next generalization blocker remains full Foldseek/TM-score split and external import blockers.
- 2026-05-14T14:10:21.275491+00:00: Expanded60 removes the expanded40 partial-signal ceiling, but full TM-score split remains blocked by two missing selected structures, the capped-out staged coordinates, and the failed <0.7 computed-subset target.
- 2026-05-14T15:07:52.876846+00:00: External pilot now has measurable success criteria and remains needs_more_work; Foldseek selected-structure blocker is narrowed to explicit coordinate exclusions plus the unrun full TM-score split.
- 2026-05-14T16:15:30.855586+00:00: Expanded80 removes the expanded60 partial-signal ceiling, but full TM-score split remains blocked by two coordinate exclusions, the capped-out staged coordinates, and the failed <0.7 computed-subset target.
- 2026-05-14T17:29:09.455993+00:00: Expanded100 removes the expanded80 partial-signal ceiling, but full TM-score split remains blocked by two coordinate exclusions, the capped-out staged coordinates, and the failed <0.7 computed-subset target.
- 2026-05-14T19:04:21.441130+00:00: Next Foldseek work should apply/regenerate the repaired split and rerun downstream metrics before any full TM-score claim
- 2026-05-14T19:08:48.002960+00:00: Next Foldseek work should rebuild downstream evaluation from the candidate split and run an uncapped all-materializable Foldseek signal when feasible
- 2026-05-14T20:34:07.608397+00:00: Repaired expanded100 removes the projection-only computed-subset blocker, but full TM-score split remains blocked by the cap, two coordinate exclusions, and the uncomputed all-materializable signal
- 2026-05-14T21:29:26.788448+00:00: Uncapped all-materializable Foldseek exact TM-score search exceeds the normal automation window; next work needs a longer run budget or chunk/resume support, not another routine capped increment
- 2026-05-14T22:36:14.676450+00:00: Resumable Foldseek query chunks remove the all-at-once-only runtime SPOF but show the repaired candidate split still fails the <0.7 TM-score target beyond the expanded100 cap
- 2026-05-14T23:22:21.551765+00:00: Foldseek query chunk aggregation is now durable; next work should adjudicate target-violating chunk blockers or change the chunk-2 runtime/slice strategy before routine chunk continuation
- 2026-05-15T00:19:07.369532+00:00: Full TM-score holdout remains blocked by target-violating completed chunks, held-out in-scope split blockers, incomplete query coverage, and two coordinate exclusions
- 2026-05-15T01:39:52.871051+00:00: Round-2 split redesign clears Foldseek chunk 0 only; next work should continue chunk 1 under the round-2 candidate and stop on any new target violation
- 2026-05-15T02:47:11.394945+00:00: Round-3 split redesign clears Foldseek chunks 0-1 only; next work should continue chunk 2 and stop on any new target violation
- 2026-05-15T03:40:39.370706+00:00: Round-3 Foldseek chunks 0-2 clear the completed-chunk target, but chunk 3 is now the runtime blocker; retry or split chunk 3 before continuing coverage
- 2026-05-15T04:56:18.692987+00:00: Cluster-first Foldseek split design replaces blind 56-chunk continuation; next work should verify bounded subchunks from the round-3 cluster-first readiness and fold in any new high-TM blockers before continuing.
- 2026-05-15T05:48:11.759711+00:00: Cluster-first round4 clears the latest failing verification unit; continue bounded round4 subchunks and fold in any new high-TM blockers before claiming full TM-score holdout.
- 2026-05-15T06:49:36.549572+00:00: Cluster-first round6 clears subchunk 009; next work should continue bounded round6 verification from subchunk 010 and fold in any new high-TM blocker before broad coverage claims
- 2026-05-15T08:46:02.937530+00:00: Round-8 cluster-first split folds in the new m_csa:68/m_csa:750 blocker; next work should continue single-query verification from staged index 68 under round-8 readiness.
- 2026-05-15T13:32:19.332566+00:00: Round-9 cluster-first split folds in the m_csa:80 high-TM blocker; next work should continue single-query verification from staged index 84 under round-9 readiness.
- 2026-05-15T14:31:01.833373+00:00: Round-9 cluster-first verification now clears staged indices 79-95; next work should continue from staged index 96 and stop on any TM>=0.7 blocker
- 2026-05-15T16:41:11.445104+00:00: Full TM-score holdout remains blocked by incomplete round-16 verification coverage and two coordinate exclusions.
- 2026-05-15T17:34:47.871028+00:00: Round-19 cluster-first split is the active Foldseek handoff; next work should verify staged index 112 under round-19 readiness.
- 2026-05-15T19:16:47.231347+00:00: Full TM-score holdout remains blocked by incomplete round-24 verification coverage and two coordinate exclusions.
- 2026-05-15T22:46:27.435996+00:00: Full TM-score holdout remains blocked by round32 index 145 timeout, incomplete query coverage, candidate-only split status, and two coordinate exclusions.
- 2026-05-16T06:10:48.154425+00:00: Next useful work is external pilot blockers or external structure index/nearest-neighbor cache, not more M-CSA strict-TM repair.
- 2026-05-16T07:15:23.155977+00:00: Next work should route the 3 deferred external pilot rows to human/expert review or start external structural clustering; do not resume M-CSA round repair.
- 2026-05-16T08:06:00.835318+00:00: Next work should prepare human/expert decisions for O14756 P34949 and Q6NSJ0 or start external structural clustering; do not resume M-CSA round repair.
- 2026-05-16T09:14:46.363953+00:00: Next work should prepare human/expert decisions for O14756 P34949 and Q6NSJ0 or expand the broader external structural candidate surface before any strict TM-diverse split assignment.
- 2026-05-16T10:14:24.266801+00:00: Next work should prepare human/expert decisions for O14756 P34949 and Q6NSJ0 or complete/cache the missing all-30 external structural pairs before strict TM-diverse split assignment.
- 2026-05-16T11:15:09.904197+00:00: Next work should prepare human/expert decisions for O14756 P34949 and Q6NSJ0 or broaden external structural candidates beyond the current review-only 30-row split before import claims.
- 2026-05-16T12:15:25.647551+00:00: Next external pilot work should resolve the six needs_review rows or broaden external structural candidates; do not treat representation-only duplicate signals as hard rejections unless evidence is stable.
- 2026-05-16T13:07:13+00:00: Next external pilot work should resolve the six needs_review rows or broaden external structural candidates; no local-evidence-only decision update was defensible.
- 2026-05-16T14:26:15.956789+00:00: External candidate all-vs-all duplicate screen is now complete for the current 30-row sample; UniRef-wide screening plus review decisions still block import.
- 2026-05-16T15:22:11.987493+00:00: Selected-pilot needs_review is no longer the active blocker; next external work should repair representation or heuristic controls or broaden the external structural surface.
- 2026-05-16T20:03:03.218017+00:00: Next direct work should integrate the Q6NSJ0 glycoside-hydrolase boundary control into import-safety adjudication or complete O14756 duplicate review and full factory gate path before import.

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
- 2026-05-13T11:04:16.318492+00:00: External transfer remains non-countable; next import readiness depends on sourcing explicit active-site evidence, completing near-duplicate sequence search, and running real representation controls before any external decision.
- 2026-05-13T12:05:19.086868+00:00: External transfer remains non-countable; next import readiness depends on primary literature/PDB active-site source review, complete near-duplicate sequence search, and replacing deterministic k-mer controls with real learned or structure-language representation controls before any external decision.
- 2026-05-13T12:55:17.737175+00:00: Post-M-CSA work now prioritizes a 5-10 candidate external-source pilot over additional abstract transfer gates or M-CSA-only tranche growth.
- 2026-05-13T13:02:54.457092+00:00: Agent work is now instruction-only redirected toward sequence/fold-distance holdout evaluation before external import or further abstract gates.
- 2026-05-13T14:08:28.620965+00:00: External transfer remains non-countable; next pilot readiness work should use the holdout metrics and learned-vs-heuristic disagreements to rank candidates before active-site source review, complete sequence search, selected-PDB override repairs, and full factory gates.
- 2026-05-13T16:04:03.062604+00:00: External pilot now has leakage-provenance ranking and no-decision review packets; next work should fill active-site and sequence evidence for selected candidates, not increase M-CSA-only count.
- 2026-05-13T16:37:11.331979+00:00: External pilot packets now have consolidated review-only source targets; next work should fill evidence decisions, not increase M-CSA count.
- 2026-05-13T17:47:33.256358+00:00: External transfer gate now fails fast on mixed-slice artifact paths across supplied gate artifacts.
- 2026-05-13T18:44:44.009443+00:00: External pilot review-decision path now fails if selected rows are ineligible, pilot decisions are completed prematurely, required review prerequisites are missing, or pilot dossier evidence blockers are stale.
- 2026-05-13T19:39:20.606270+00:00: External transfer gate input typing and CLI loading are now contract-based; next pilot work should fill real active-site and sequence evidence, not add generic gate count.
- 2026-05-13T20:51:07.000000+00:00: No M-CSA-only growth or external import; SPOF text-leakage hardening only
- 2026-05-13T22:04:23.805937+00:00: External transfer remains non-countable; current-reference sequence screen blocker is cleared, but complete UniRef/all-vs-all near-duplicate search and active-site evidence still block import.
- 2026-05-13T22:34:16.818554+00:00: Artifact-lineage SPOF hardening now includes the external sequence-holdout audit in row-level candidate lineage checks.
- 2026-05-13T23:52:26.926762+00:00: selected-pilot representation coverage is now a direct review-only gate input rather than stale mapped-control evidence
- 2026-05-14T00:43:19.772463+00:00: Label batch acceptance and scaling-quality audits now fail fast on mixed slice lineage before count/import decisions.
- 2026-05-14T01:50:53.503582+00:00: High-fan-in external pilot builders now fail fast on mixed-slice lineage before artifact write; selected-PDB ready overrides must match graph slice provenance.
- 2026-05-14T03:08:19.594666+00:00: Real sequence-distance holdout replaces proxy-only generalization signal; Foldseek/TM-score split now depends on coordinate materialization rather than tool availability alone.
- 2026-05-14T04:23:49.348241+00:00: External pilot sequence-search work now uses real MMseqs2 current-reference backend evidence before review decisions; import remains blocked by active-site, representation, broader duplicate-screening, review, and factory gates.
- 2026-05-14T11:07:34.295381+00:00: Unstaged selected-coordinate sidecar blocker is removed, but full TM-score split remains blocked by two missing selected structures and the unrun Foldseek split builder; selected-pilot active-site source status is classified but import remains blocked.
- 2026-05-14T12:34:37.036864+00:00: No project scope change; full TM-score split remains blocked by two missing selected structures and the unrun all-materializable Foldseek signal.
- 2026-05-14T14:10:21.275491+00:00: Foldseek TM-score evidence is stronger but still review-only and non-countable; do not treat expanded60 as a full holdout split.
- 2026-05-14T15:07:52.876846+00:00: Do not count external pilot evidence as success until terminal decisions and import criteria pass; report m_csa:372 and m_csa:501 as coordinate exclusions before any full TM-score holdout claim.
- 2026-05-14T16:15:30.855586+00:00: Foldseek TM-score evidence is stronger but still review-only and non-countable; do not treat expanded80 as a full holdout split.
- 2026-05-14T17:29:09.455993+00:00: Foldseek TM-score evidence is stronger but still review-only and non-countable; do not treat expanded100 as a full holdout split.
- 2026-05-14T19:04:21.441130+00:00: Foldseek target failure now has a concrete unapplied repair candidate and computed-subset projection; full holdout still requires regenerated sequence metrics and uncapped Foldseek split
- 2026-05-14T19:08:48.002960+00:00: Foldseek split repair now has an unapplied candidate sequence holdout copy; canonical holdout and downstream artifacts still need regeneration before any claim
- 2026-05-14T20:34:07.608397+00:00: Foldseek split repair now has an actual repaired expanded100 signal under the candidate holdout; canonical holdout remains unchanged and no full holdout claim is permitted.
- 2026-05-14T22:36:14.676450+00:00: Full TM-score holdout remains blocked by incomplete chunk aggregation new target-violating pairs and two coordinate exclusions
- 2026-05-14T23:22:21.551765+00:00: Full TM-score holdout remains blocked by target-violating completed chunks a timed-out chunk-2 range incomplete query coverage and two coordinate exclusions
- 2026-05-15T04:56:18.692987+00:00: Foldseek/TM-score work now uses observed high-TM structural clusters as partition constraints before verification chunks.
- 2026-05-15T15:32:34.144335+00:00: Cluster-first Foldseek verification now preserves real sequence-identity components before structural assignment; next work should rerun staged index 105 under round-13 readiness.
- 2026-05-15T16:41:11.445104+00:00: Round-16 cluster-first split is the active Foldseek handoff; next work should verify staged index 110 under round-16 readiness.
- 2026-05-15T18:36:22.139127+00:00: Round-22 cluster-first split is the active Foldseek handoff; next work should continue from staged index 119 under round-22 readiness.
- 2026-05-15T19:16:47.231347+00:00: Round-24 cluster-first split is the active Foldseek handoff; next work should continue single-query verification from staged index 123 under round-24 readiness.
- 2026-05-16T06:10:48.154425+00:00: Do not resume M-CSA round33 or staged-index-145 partition repair as normal progress; strict TM-diverse holdouts now move to external fold-diverse structural data before split assignment.
- 2026-05-16T06:25:28.404682+00:00: No scope change; latest pushed repo state supersedes stale prompt Foldseek continuation and keeps external structural pilot as next direct work
- 2026-05-16T07:15:23.155977+00:00: M-CSA strict pairwise TM <0.7 is closed/deferred for the curated M-CSA surface; strict TM-diverse holdouts move to external fold-diverse structural data.
- 2026-05-16T08:06:00.835318+00:00: Deferred external pilot rows are now routed to human/expert review packets; external import remains blocked by expert decisions broader duplicate screening and full factory gates.
- 2026-05-16T09:14:46.363953+00:00: Selected-pilot external structural clustering is now a review-only cache, not a train/test split or import authorization.
- 2026-05-16T10:14:24.266801+00:00: External fold-diverse structural work now starts from the all-30 UniProtKB/Swiss-Prot candidate surface rather than only the selected 10-row pilot; strict split claims remain blocked until pair-cache and review/import blockers are resolved.
- 2026-05-16T11:15:09.904197+00:00: External structural TM-diverse split assignment is now available only as review-only all-30 Swiss-Prot/AFDB evidence; import and benchmark claims remain blocked by terminal review decisions and broader duplicate/factory gates.
