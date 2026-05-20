# Catalytic Earth Status

Generated from `work/progress_log.jsonl`.

## Time

- Entries: 215
- Measured elapsed time: 6792.6 minutes (113.21 hours)
- Estimated/planned time: 405 minutes (6.75 hours)
- Note: entries before timing instrumentation are estimates, not clock measurements.

## Time By Stage

- external-transfer-spof-hardening: 246.7 measured minutes (4.11 hours)
- infrastructure: 106.2 measured minutes (1.77 hours)
- leakage-risk closure: 11.8 measured minutes (0.20 hours)
- ops: 84.3 measured minutes (1.41 hours)
- post-infra-science: 1563.4 measured minutes (26.06 hours)
- post-mcsa-spof-hardening: 1764.6 measured minutes (29.41 hours)
- post-v2: 2950.7 measured minutes (49.18 hours)
- v3: 64.8 measured minutes (1.08 hours)
- ops: 45 estimated minutes (0.75 hours)
- post-v2: 180 estimated minutes (3.00 hours)
- v0: 55 estimated minutes (0.92 hours)
- v1: 55 estimated minutes (0.92 hours)
- v2: 70 estimated minutes (1.17 hours)

## Progress Counters

- Artifact references logged: 2546
- Evidence references logged: 2042

## Recent Entries

### 2026-05-20T08:39:33.652171+00:00 - post-infra-science

- Task: ePK MEK ERK source review and broad-role stress
- Time mode: measured
- Measured minutes: 48.517
- Started: 2026-05-20T07:50:46Z
- Ended: 2026-05-20T08:39:17Z
- Artifacts: src/catalytic_earth/labels.py, src/catalytic_earth/cli.py, tests/test_cli.py, tests/test_leakage_closure.py, artifacts/v3_epk_mek_erk_phosphosite_source_review_1025.json, artifacts/v3_epk_mek_erk_role_control_rerun_1025.json, artifacts/v3_epk_mek_erk_broad_role_stress_audit_1025.json, artifacts/v3_epk_mek_erk_context_counteraxis_stress_audit_1025.json, artifacts/v3_epk_precount_gate_status_1025.json, artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json, README.md, docs/label_factory.md, work/handoff.md, work/scope.md, work/progress_log.jsonl, work/status.md
- Evidence: startup 644-test unit discovery passed, startup validate passed with 682 labels, SSH deploy-key fetch pull ls-remote dry-run push passed, MEK ERK source review marked 9UUR and 9UUX measurement-ready and rejected 9UW4 same-chain topology, broad-role stress retained 9UUR and 9UUX but false-hit 8 nonpositive topology rows, review-context counteraxis blocked 6 prior counterexample repeats and left 7CAG and 8BMS residual false hits, pre-count gate remains blocked_review_only, counteraxis decision remains do_not_select_threshold, final 656-test unit discovery passed, validate passed with 682 labels and 8 fingerprints, artifact migration dry-run guard passed with 108 rows and removal_allowed=0, label invariants preserved 682 total 212 seed 470 out_of_scope and 3 external out_of_scope, compileall passed, JSON validation passed, git diff --check passed
- Notes: Direct locked automation run with no delegation. Phase 1 artifact migration remained guard-only and closed. No artifact upload deletion externalization Git-LFS migration history rewrite label import positive fingerprint registry edit external hard-negative production score or removal_allowed=true.

### 2026-05-20T09:40:52.064773+00:00 - post-infra-science

- Task: ePK MEK ERK topology counteraxis stress
- Time mode: measured
- Measured minutes: 48.367
- Started: 2026-05-20T08:52:03Z
- Ended: 2026-05-20T09:40:25Z
- Artifacts: src/catalytic_earth/labels.py, src/catalytic_earth/cli.py, tests/test_cli.py, tests/test_leakage_closure.py, artifacts/v3_epk_mek_erk_residual_false_hit_source_adjudication_1025.json, artifacts/v3_epk_mek_erk_source_free_topology_ambiguity_counteraxis_1025.json, artifacts/v3_epk_mek_erk_source_free_topology_broader_stress_audit_1025.json, artifacts/v3_epk_precount_gate_status_1025.json, artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json, README.md, docs/label_factory.md, docs/external_source_transfer.md, work/handoff.md, work/scope.md
- Evidence: startup 656-test unit discovery passed, startup validate passed with 682 labels, SSH deploy-key fetch pull ls-remote dry-run push passed, residual source adjudication terminally blocked 7CAG and 8BMS as transporter-context false hits, source-free topology ambiguity blocked 7CAG and 8BMS while retaining 9UUR and 9UUX, broader topology stress retained five positive controls but left 2JJ2 4HPU 7B56 and 7ZDT false hits, pre-count remains blocked_review_only, counteraxis decision remains do_not_select_threshold, final 665-test unit discovery passed, tests.test_cli plus tests.test_leakage_closure passed with 274 tests, validate passed with 682 labels and 8 fingerprints, artifact migration dry-run guard passed with 108 rows and removal_allowed=0, label invariants preserved 682 total 212 seed 470 out_of_scope and 3 external out_of_scope, compileall passed, JSON validation passed, git diff --check passed
- Notes: Direct locked automation run with no delegation. Phase 1 artifact migration remained guard-only and closed. No artifact upload deletion externalization Git-LFS migration history rewrite label import positive fingerprint registry edit external-hard-negative scored re-audit or removal_allowed=true.

### 2026-05-20T10:43:00+00:00 - post-infra-science

- Task: ePK MEK ERK substrate-mode counteraxis stress
- Time mode: measured
- Measured minutes: 50.5
- Started: 2026-05-20T09:52:30Z
- Ended: 2026-05-20T10:43:00Z
- Artifacts: src/catalytic_earth/labels.py, src/catalytic_earth/cli.py, tests/test_cli.py, tests/test_leakage_closure.py, artifacts/v3_epk_mek_erk_substrate_mode_counteraxis_audit_1025.json, artifacts/v3_epk_mek_erk_substrate_mode_fresh_stress_audit_1025.json, artifacts/v3_epk_mek_erk_substrate_mode_existing_scout_gap_audit_1025.json, artifacts/v3_epk_precount_gate_status_1025.json, artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json, README.md, docs/label_factory.md, work/handoff.md, work/scope.md, work/progress_log.jsonl, work/status.md
- Evidence: startup 665-test unit discovery passed, startup validate passed with 682 labels, SSH deploy-key fetch pull ls-remote dry-run push passed, substrate-mode counteraxis retained five positives and blocked residual false hits 2JJ2 4HPU 7B56 7ZDT, fresh MEK ERK stress found 7M0T 7M0W 9UW4 had zero substrate-mode rule hits but all topology-confounded, existing scout gap audit found ten remaining unreviewed topology hits all same-chain topology-confounded, pre-count remains blocked_review_only, counteraxis decision remains do_not_select_threshold, final 674-test unit discovery passed, tests.test_cli plus tests.test_leakage_closure passed with 283 tests, validate passed with 682 labels and 8 fingerprints, artifact migration dry-run guard passed with 108 rows and removal_allowed=0, label invariants preserved 682 total 212 seed 470 out_of_scope 3 external out_of_scope, compileall passed, JSON validation passed, git diff --check passed
- Notes: Direct locked automation run with no delegation. Phase 1 artifact migration remained guard-only and closed. No artifact upload deletion externalization Git-LFS migration history rewrite label import positive fingerprint registry edit external-hard-negative scored re-audit or removal_allowed=true.

### 2026-05-20T11:24:52.078372+00:00 - post-infra-science

- Task: ePK 4EKK source-mapped substrate-mode tranche
- Time mode: measured
- Measured minutes: 31.267
- Started: 2026-05-20T10:53:16Z
- Ended: 2026-05-20T11:24:32Z
- Artifacts: src/catalytic_earth/labels.py, src/catalytic_earth/cli.py, tests/test_cli.py, tests/test_leakage_closure.py, artifacts/v3_epk_substrate_mode_next_tranche_candidate_scout_amp_pnp_1025.json, artifacts/v3_epk_substrate_mode_next_tranche_source_validation_amp_pnp_1025.json, artifacts/v3_epk_substrate_mode_next_tranche_source_review_amp_pnp_1025.json, artifacts/v3_epk_substrate_mode_next_tranche_fresh_stress_amp_pnp_1025.json, artifacts/v3_epk_unified_prototype_broad_stress_with_next_tranche_amp_pnp_1025.json, artifacts/v3_epk_substrate_mode_next_tranche_candidate_scout_amp_pnp_broad40_1025.json, artifacts/v3_epk_substrate_mode_next_tranche_source_validation_amp_pnp_broad40_1025.json, artifacts/v3_epk_substrate_mode_next_tranche_source_review_amp_pnp_broad40_1025.json, artifacts/v3_epk_substrate_mode_next_tranche_candidate_scout_amp_pnp_broad41_80_1025.json, artifacts/v3_epk_substrate_mode_next_tranche_source_validation_amp_pnp_broad41_80_1025.json, artifacts/v3_epk_substrate_mode_next_tranche_candidate_scout_amp_pnp_broad81_92_1025.json, artifacts/v3_epk_substrate_mode_next_tranche_source_validation_amp_pnp_broad81_92_1025.json, artifacts/v3_epk_precount_gate_status_1025.json, artifacts/v3_epk_counteraxis_sufficiency_decision_1025.json, README.md, docs/label_factory.md, work/handoff.md, work/scope.md, work/progress_log.jsonl, work/status.md
- Evidence: startup 674-test unit discovery passed, startup validate passed with 682 labels, SSH deploy-key fetch pull ls-remote dry-run push passed, 4EKK maps to GSK3B P49841 Ser9 with AKT PKB phosphosite support and 3.228 Angstrom gamma distance, broad40 AMP-PNP scout rejects 7ZE5 as non-topology counterexample blocked by substrate-mode/source context, review-only external hard-negative score probe remains 0 non-abstentions, pre-count gate remains blocked_review_only, counteraxis decision remains do_not_select_threshold, final 676-test unit discovery passed, tests.test_cli plus tests.test_leakage_closure passed with 285 tests, validate passed with 682 labels and 8 fingerprints, artifact migration dry-run guard passed with 108 rows and removal_allowed=0, label invariants preserved 682 total 212 seed 470 out_of_scope 3 external out_of_scope, JSON validation passed, git diff --check passed, local ENOSPC blocked final broad41-80 and broad81-92 source-review writes
- Notes: Direct locked automation run with no delegation. Phase 1 migration remained guard-only and closed. No artifact upload deletion externalization Git-LFS migration history rewrite label import positive fingerprint registry edit external-hard-negative scored re-audit or removal_allowed=true. Stopped expansion early because local disk reached ENOSPC.

### 2026-05-20T12:19:46.938589+00:00 - post-infra-science

- Task: ePK substrate-mode recovery and folded-source stress
- Time mode: measured
- Measured minutes: 23.9
- Started: 2026-05-20T11:55:15Z
- Ended: 2026-05-20T12:19:09Z
- Artifacts: src/catalytic_earth/labels.py, src/catalytic_earth/cli.py, tests/test_cli.py, tests/test_leakage_closure.py, artifacts/v3_epk_substrate_mode_next_tranche_source_review_amp_pnp_broad41_80_1025.json, artifacts/v3_epk_substrate_mode_next_tranche_source_review_amp_pnp_broad81_92_1025.json, artifacts/v3_epk_substrate_mode_tranche_recovery_decision_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_candidate_scout_amp_pnp_protein_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_candidate_scout_amp_pnp_protein_rows41_67_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_candidate_scout_atp_protein_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_candidate_scout_anp_protein_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_candidate_scout_anp_protein_rows31_60_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_candidate_scout_anp_protein_rows61_90_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_candidate_scout_anp_protein_rows91_120_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_source_validation_amp_pnp_protein_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_source_validation_amp_pnp_protein_rows41_67_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_source_validation_atp_protein_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_source_validation_anp_protein_rows31_60_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_source_validation_anp_protein_rows61_90_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_source_review_amp_pnp_protein_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_source_review_amp_pnp_protein_rows41_67_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_source_review_atp_protein_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_source_review_anp_protein_rows31_60_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_source_review_anp_protein_rows61_90_1025.json, artifacts/v3_epk_substrate_mode_folded_source_stress_terminal_decision_1025.json, README.md, docs/label_factory.md, work/handoff.md, work/scope.md, work/progress_log.jsonl, work/status.md
- Evidence: recovered missing broad41-80 and broad81-92 source-review writes, 4EKK remains only source-mapped measurement-ready review row, 1O6K and 1O6L now carry explicit PKB GSK3 exact AKT1 or chain mapping blocker, folded protein-substrate stress reviewed 11 topology hits with 0 measurement-ready positives, 2JJ2 4HPU 7B56 and 7ZE5 rejected by substrate mode, six ATP-query rows topology-confounded, 1IR3 source-mapping unresolved under generic mapper, 680-test unit discovery passed, validate passed with 682 labels and 8 fingerprints, artifact migration dry-run guard passed with 108 rows and removal_allowed=0, label invariants preserved 682 total 212 seed 470 out_of_scope 3 external out_of_scope, compileall passed, JSON validation passed, git diff --check passed
- Notes: Direct locked automation run with no delegation. Phase 1 migration remained guard-only and closed. No artifact upload deletion externalization Git-LFS migration history rewrite label import positive fingerprint registry edit external-hard-negative scored re-audit or removal_allowed=true.

### 2026-05-20T13:17:20.692201+00:00 - post-infra-science

- Task: ePK subagent synthesis plus external mini-campaign and baseline comparison
- Time mode: measured
- Measured minutes: 21.033
- Started: 2026-05-20T12:55:46Z
- Ended: 2026-05-20T13:16:48Z
- Artifacts: artifacts/v3_epk_subagent_synthesis_20260520.json, artifacts/v3_prospective_external_minicampaign_candidate_freeze_20260520.json, artifacts/v3_prospective_external_minicampaign_backend_sequence_search_20260520.json, artifacts/v3_prospective_external_minicampaign_current_countable_structural_screen_20260520.json, artifacts/v3_prospective_external_minicampaign_terminal_decisions_20260520.json, artifacts/v3_prospective_external_minicampaign_inverse_gate_scores_20260520.json, artifacts/v3_prospective_external_minicampaign_decision_packet_20260520.json, artifacts/v3_modern_baseline_comparison_20260520.json, tests/test_automation_small_win_artifacts.py, work/handoff.md, work/scope.md
- Evidence: startup 680-test unit discovery passed, startup validate passed with 682 labels and 8 fingerprints, SSH deploy-key fetch pull ls-remote dry-run push passed, ePK subagent synthesis integrated and pushed in commit 45dec98, prospective external mini-campaign froze 12 rows across 3 lanes before scoring, MMseqs2 backend sequence search found 11 no-signal rows and one exact-reference holdout P07237, local Foldseek binary unavailable so structural screen incomplete and 11 rows are needs_review, inverse gate configured with 8 fingerprints at threshold 0.4115 but scored 0 rows due no structurally screened survivors, modern baseline comparison makes no superiority claim, focused artifact tests passed, full 683-test unit discovery passed, validate passed, artifact migration dry-run local-file guard passed with removal_allowed=0, label invariants preserved 682 total 212 seed 470 out_of_scope 3 external hard negatives unchanged, compileall passed, git diff --check passed
- Notes: No Phase 2 or 3 artifact migration, upload, deletion, externalization, Git-LFS migration, history rewrite, registry edit, label import, production fingerprint edit, external hard-negative production score, or removal_allowed=true occurred.

### 2026-05-20T14:14:08.715044+00:00 - post-infra-science

- Task: SDR readiness packet and mini-campaign sequence baseline
- Time mode: measured
- Measured minutes: 16.45
- Started: 2026-05-20T13:57:21Z
- Ended: 2026-05-20T14:13:48Z
- Artifacts: artifacts/v3_sdr_family_readiness_packet_20260520.json, artifacts/v3_prospective_external_minicampaign_sequence_baseline_diagnostic_20260520.json, artifacts/v3_prospective_external_minicampaign_current_countable_structural_screen_20260520.json, artifacts/v3_prospective_external_minicampaign_terminal_decisions_20260520.json, artifacts/v3_prospective_external_minicampaign_inverse_gate_scores_20260520.json, artifacts/v3_prospective_external_minicampaign_decision_packet_20260520.json, tests/test_automation_small_win_artifacts.py, docs/external_source_transfer.md, work/handoff.md, work/scope.md, work/progress_log.jsonl, work/status.md
- Evidence: startup 683-test unit discovery passed, startup validate passed with 682 labels and 8 fingerprints, SSH deploy-key fetch pull ls-remote dry-run push passed, subagent JSON packets validated, SDR readiness packet keeps O14756 review-only and no-go for production fingerprint expansion, SDR packet records 36 clean SDR abstentions and AKR/NADP counterfamily requirements, mini-campaign sequence baseline records P07237 terminal rejection and P31040 k-mer review-priority caveat, Foldseek restored at /private/tmp/catalytic-foldseek-env/bin/foldseek but candidate coordinate sidecars missing keep 11 rows needs_review, inverse gate scored 0 rows because no candidate cleared structural screening, focused artifact tests passed, final 685-test unit discovery passed, validate passed with 682 labels and 8 fingerprints, artifact migration dry-run local-file guard passed with 108 rows and removal_allowed=0, label invariants preserved 682 total 212 seed 470 out_of_scope 3 external hard negatives unchanged, compileall passed, JSON validation passed, git diff --check passed
- Notes: Direct locked automation run with no delegation. No artifact migration Phase 2/3 action, upload, deletion, externalization, Git-LFS migration, history rewrite, registry edit, label import, production fingerprint edit, external hard-negative production score, or removal_allowed=true occurred.

### 2026-05-20T15:32:22.885905+00:00 - post-infra-science

- Task: Close prospective mini-campaign structural duplicates
- Time mode: measured
- Measured minutes: 33.017
- Started: 2026-05-20T14:58:48Z
- Ended: 2026-05-20T15:31:49Z
- Artifacts: artifacts/v3_prospective_external_minicampaign_coordinate_materialization_20260520.json, artifacts/v3_prospective_external_minicampaign_structural_coordinates_20260520, artifacts/v3_prospective_external_minicampaign_current_countable_structural_screen_20260520.json, artifacts/v3_prospective_external_minicampaign_terminal_decisions_20260520.json, artifacts/v3_prospective_external_minicampaign_inverse_gate_scores_20260520.json, artifacts/v3_prospective_external_minicampaign_decision_packet_20260520.json, artifacts/v3_prospective_external_minicampaign_sequence_baseline_diagnostic_20260520.json, tests/test_automation_small_win_artifacts.py, docs/external_source_transfer.md, work/handoff.md, work/scope.md, work/progress_log.jsonl, work/status.md
- Evidence: startup 685-test unit discovery passed, startup validate passed with 682 labels and 8 fingerprints, SSH deploy-key fetch pull ls-remote dry-run push passed, subagent JSON packets and synthesis JSON validated, 11 frozen mini-campaign AlphaFold coordinate sidecars materialized with 0 fetch failures, Foldseek current-countable structural screen completed 7392/7392 query-target pairs against 672 current coordinate groups, all 11 sequence-clean rows rejected by current-countable structural duplicate signal, P07237 remains exact-reference terminal rejection, inverse gate scored 0 rows because no row survived structural duplicate screening, focused small-win artifact tests passed, final 686-test unit discovery passed, validate passed with 682 labels and 8 fingerprints, artifact migration dry-run local-file guard passed with 108 rows and removal_allowed=0, label invariants preserved 682 total 212 seed 470 out_of_scope and 3 external hard negatives unchanged, compileall passed, JSON validation passed, git diff --check passed
- Notes: Direct locked automation run with no delegation. No artifact migration Phase 2/3 action, upload, deletion, externalization, Git-LFS migration, history rewrite, registry edit, label import, production fingerprint edit, external hard-negative production score, or removal_allowed=true occurred.

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
- 2026-05-16T21:00:19.989175+00:00: Next direct work should integrate the P34949 sugar-phosphate isomerase control into import-safety adjudication or complete duplicate/review/factory blockers for repaired O14756 and Q6NSJ0.
- 2026-05-16T21:04:56.234887+00:00: Next run should reacquire the lock, verify local-ahead state, and push the remaining handoff/status correction after GitHub credentials are usable.
- 2026-05-16T22:05:28.138975+00:00: Next direct work should complete duplicate/review/factory blockers for repaired external rows or continue C9JRZ8 AKR/NADP repair without broadening generic gates.
- 2026-05-16T23:03:05.000429+00:00: Next direct work should complete duplicate/review/factory blockers for repaired external rows or implement the remaining P06746 DNA Pol X/5'-dRP lyase repair lane without broadening generic gates.
- 2026-05-17T02:10:05.048551+00:00: External out-of-scope import requires all-8 inverse gate plus duplicate review and factory gates; O14756 and Q6NSJ0 are blocked despite inverse-gate pass.
- 2026-05-17T04:14:25+00:00: Fresh external sourcing and the first current-countable structural screen are complete; Q13087 is the only sequence-clean row without a high-TM current-countable signal, but pair-cache completion, UniRef-wide screening, terminal review, and factory gates still block import.
- 2026-05-17T05:01:18.923988+00:00: Fresh sourced hard-negative tranche is closed by current-countable structural duplicate signals; next work needs new external candidate sourcing or genuinely new evidence.
- 2026-05-17T07:42:26.961418+00:00: Next-candidate UniRef current-reference duplicate blocker is removed for P22830 P78549 Q3LXA3; terminal review and full factory gates are now the active blockers.
- 2026-05-17T09:08:30+00:00: First external out-of-scope hard-negative import succeeded for P78549; next work should decide whether P22830 or Q3LXA3 should enter a later single-import cycle after litmus remains green.
- 2026-05-17T09:41:38.959359+00:00: Post-import litmus remains green after P78549; Q3LXA3 is the next review-only candidate if a later explicit single-import cycle is opened.
- 2026-05-17T10:50:16.595786+00:00: Second external out-of-scope hard-negative import succeeded for Q3LXA3; P22830 remains review-only and should require its own explicit cycle or broader sourcing decision.
- 2026-05-17T13:25:17.879225+00:00: Broader external sourcing now has one surviving no-current-structural-signal row, P06744; terminal review and full factory/import gates are the active blockers.
- 2026-05-17T13:49:27.020292+00:00: P06744 is now a countable external out-of-scope hard negative; next work should not retry broader duplicate-signal rejects without new evidence.
- 2026-05-17T17:13:28.332690+00:00: candidate-specific pilot repairs are development evidence only; next external tranche requires frozen preregistration
- 2026-05-18T04:13:16.733717+00:00: Phase 1 artifact-migration instrumentation is complete; next action is human approval for Phase 2 upload target and subset.
- 2026-05-18T07:51:37.415598+00:00: ePK now has review-only local axes, acceptor threshold hypotheses, gamma-distance samples, and a blocked pre-count gate; positive-universe expansion still requires true acceptor identity, ATP-state repair, threshold calibration, external re-audit, and label-factory extension.
- 2026-05-18T13:55:35.875542+00:00: ePK threshold selection is now blocked on negative-control distance distributions and non-ready row repair rather than threshold design itself.
- 2026-05-18T15:03:10.233611+00:00: ePK threshold selection is now blocked by observed sibling-family gamma-distance overlap plus incomplete non-ready row repair.
- 2026-05-18T17:05:01.231831+00:00: ePK threshold selection is now blocked by negative-control calibration and complete gamma geometry rather than non-ready-row ambiguity.
- 2026-05-18T18:01:10.526233+00:00: ePK threshold selection remains blocked after measured sibling alternate controls; next work needs missing ATP-grasp NDK PfkA and PfkB controls or a non-distance-only axis.
- 2026-05-18T19:01:23.160128+00:00: ePK threshold selection now has explicit ATP-grasp NDK PfkA and PfkB source requests; next work should repair or source one missing sibling family at a time before any score or threshold.
- 2026-05-18T20:03:10.553576+00:00: ePK PfkB mapping ambiguity is narrowed but threshold selection remains blocked because PfkB still lacks a metal-supported gamma-capable sibling control.
- 2026-05-18T21:12:49.756080+00:00: ePK direct graph-linked sibling-control repair is exhausted for ATP-grasp NDK PfkA and PfkB; threshold selection now needs external or homolog gamma-capable controls rather than another direct repair review.
- 2026-05-18T22:05:23.696999+00:00: ePK NDK now has homolog gamma-metal source candidates but threshold selection remains blocked until catalytic-residue mapping succeeds.
- 2026-05-18T23:06:35.869912+00:00: ePK NDK mapping is no longer the active blocker; next work should measure mapped NDK homolog controls review-only before threshold selection.
- 2026-05-19T00:13:47.867615+00:00: ePK gamma distance alone remains unsafe; NDK histidine counter-axis evidence and fail-closed external-negative abstentions make family-specific mapping for PfkB PfkA and ATP-grasp the next bounded step before any scorer or threshold claim.
- 2026-05-19T00:38:30.189051+00:00: ePK remaining sibling controls now need family-specific homolog mappers from seeded source templates before any distance measurement or threshold claim.
- 2026-05-19T01:44:03.576487+00:00: ePK distance-only thresholding is now explicitly falsified by 16 family-specific sibling controls plus NDK phosphohistidine controls; next useful work needs a substrate-acceptor or family-disambiguation rule or the 3TM0 ANP/B31 m_csa:640 gamma-geometry review before any score.
- 2026-05-19T02:44:02.632801+00:00: ePK has a sharper fail-closed review-only counteraxis, but the simplest text-free acceptor feature is blocked by sibling-control false hits; next work should add chain/substrate or ligand-class disambiguation before any score or external scored re-audit.
- 2026-05-19T03:46:56.310139+00:00: ePK chain/ligand context is promising review-only disambiguation, but production scoring remains blocked by calibration, text-free feature admissibility, negative-control distribution readiness, and scored external hard-negative re-audit.
- 2026-05-19T12:03:38.595849+00:00: Current bounded ePK source-repair candidates are exhausted as review-only negatives; next useful work needs new mapped protein-substrate evidence or an inactive policy draft promoted only after sibling and external hard-negative re-audits.
- 2026-05-19T13:17:33.402946+00:00: ePK analog/product-state and 5LI1 evidence are now explicit fail-closed review-only blockers; source triage still has no new protein-substrate candidate, so production expansion needs genuinely new source evidence or a pre-frozen calibrated policy path.
- 2026-05-19T14:18:17.427495+00:00: External reviewed kinase source evidence can produce mapped active-state Q8IVT5 structures, but current acceptor-like geometry is not source-mapped; production ePK expansion remains blocked until an exact source-mapped protein-substrate acceptor and calibrated scorer controls exist.
- 2026-05-19T15:19:23.015183+00:00: Ligand-specific substrate/co-complex querying can produce concrete review leads; next work should manually validate 5HVK source evidence before any measurement or scoring.
- 2026-05-19T16:05:05.942310+00:00: 5HVK is now source-valid review evidence, but ePK production scoring remains blocked until the queued prototype/control rerun, threshold calibration, and real external hard-negative scored re-audit exist.
- 2026-05-19T17:07:27.421941+00:00: 5HVK reduces the ligand-analog dependency for ePK scorer development, but production scoring remains blocked by source-authority chain-role dependence, threshold calibration, broader controls, and real external hard-negative scored re-audit.
- 2026-05-19T18:22:33.619263+00:00: Source-free local topology alone false-hits same-accession phosphosite controls, but a heteromeric author-chain polymer entity counter-axis separates current hits; production remains blocked by one-positive coverage, threshold calibration, real external hard-negative scored re-audit, and registry/factory extension.
- 2026-05-19T19:16:16.071899+00:00: ePK heteromeric topology now has measured source-valid review leads beyond 5HVK, but scorer threshold external re-audit and registry gates remain closed.
- 2026-05-19T20:23:20.534717+00:00: ePK heteromeric topology now has a review-only local counteraxis that clears the current six-row review surface, but production scoring still needs broader controls thresholds and a real external scored re-audit.
- 2026-05-19T21:26:22.348537+00:00: ePK heteromeric role direction is stronger after broader counteraxis and ligand-asymmetry controls, but generic hydroxyl residue identity is too weak for production; next work needs a non-generic local acceptor-identity signal before thresholding or external scored re-audit.
- 2026-05-19T22:26:42.259225+00:00: A short peptide-like acceptor-chain rule is useful current-control evidence for heteromeric ePK review, but it is narrow; production scoring still needs general substrate identity, threshold calibration, real external scored re-audit, and registry/factory extension.
- 2026-05-19T23:28:59.207385+00:00: The exact ANP/Mg source is exhausted and outside-query sourcing can find PKB/GSK3 peptide review leads but the decision surface still needs a source-free substrate-role or general acceptor-identity axis before any scorer or label gate.
- 2026-05-20T00:30:20.032873+00:00: ePK peptide-mode coverage now includes outside-query PKB/GSK3 leads but production scoring remains blocked by missing unified source-free substrate identity threshold calibration real external scored re-audit and registry gates.
- 2026-05-20T02:33:19.307966+00:00: ePK unified review-only prototype is current-control clean, but broad-stress counterexamples 9L3M/9L3U and uncalibrated thresholds keep production scoring closed; next work should execute the preregistered broad-stress tranche before threshold or real external scored re-audit.
- 2026-05-20T03:33:14.995937+00:00: ePK broad-stress execution found more source-context counterexamples but the peptide-role counterevidence rule blocks them without changing production gates; next work should seek a more general source-free substrate identity axis or a qualitatively new positive source before threshold work.
- 2026-05-20T04:34:07.290642+00:00: A relaxed polymer identity rule is unsafe because 7B56 false-hits; a length-band counteraxis repairs that bounded source-expansion false hit but remains too scoped for production, so ePK still needs broader substrate-identity stress or new positive source evidence before thresholding.
- 2026-05-20T05:33:51.904993+00:00: ePK protein-role evidence is current-control clean but not general: 7B56 blocks relaxed folded-protein generalization and the fourth external source pass adds no measurement-ready positives.
- 2026-05-20T06:36:57.763104+00:00: The mid-length rule repairs the current 7B56 failure but has no broad source-valid protein-substrate positive; the first 100 ligand-specific active-query hits add counterexamples but no new positive source, so ePK thresholding and production fingerprint expansion remain closed.
- 2026-05-20T07:35:18.172497+00:00: Broad active-query routes now look negative for clean ePK protein-substrate sourcing; next progress needs MEK ERK source-authority review or a curated kinase-substrate source rather than thresholding current query hits.
- 2026-05-20T08:39:33.652171+00:00: MEK ERK now provides two source-authoritative review controls but broad protein-role geometry is unsafe; source-free substrate identity or source adjudication for 7CAG and 8BMS is the next blocker before scorer calibration.
- 2026-05-20T09:40:52.064773+00:00: MEK ERK residual false hits are now closed in a bounded source-free topology probe, but broader stress leaves four false hits; the next useful ePK work needs an additional source-free acceptor or substrate-identity axis before thresholding.
- 2026-05-20T11:24:52.078372+00:00: 4EKK is useful source-mapped ePK review evidence, but production remains blocked by source-context dependence, uncalibrated substrate-mode logic, external scored re-audit, and local disk capacity before broader source-review recovery.
- 2026-05-20T12:19:46.938589+00:00: Folded protein-substrate sourcing is still negative under the current source-free substrate-mode surface; next work needs a fresh bounded tranche with stronger source-free substrate identity or pair-specific source mapping kept outside predictive scoring.
- 2026-05-20T13:17:20.692201+00:00: Next external mini-campaign blocker is restoring or configuring Foldseek before current-countable structural screen and inverse-gate scoring can produce import decisions
- 2026-05-20T14:14:08.715044+00:00: Next mini-campaign work should materialize the 11 candidate coordinate sidecars before rerunning Foldseek; next SDR work should freeze a 10-20 row SDR/AKR control tranche before scoring.
- 2026-05-20T15:32:22.885905+00:00: Next external mini-campaign work needs genuinely new preregistered sourcing or a different frozen surface; do not rerun this structurally duplicated set for import.

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
- 2026-05-16T21:00:19.989175+00:00: Q6NSJ0 boundary repair is now an import-safety adjudication; P34949 sugar-phosphate isomerase is the next staged review-only control, not an import.
- 2026-05-16T22:05:28.138975+00:00: P34949 and Q9BXD5 now have review-only import-safety adjudications; Q9BXD5 still preserves the representation near-duplicate holdout as an import blocker.
- 2026-05-17T02:10:05.048551+00:00: First external hard-negative import attempt is closed without count growth; next external work starts tranche-2 review-only candidates P33025 Q13907 P35914.
- 2026-05-17T04:14:25+00:00: Next hard-negative work should complete the missing current-countable pair cache for Q13087/sequence-clean rows, then continue UniRef-wide duplicate and terminal review gates before any import attempt.
- 2026-05-17T17:13:28.332690+00:00: leakage-risk closure complete; next milestone is infrastructure/artifact strategy before ePK or broad scale-up
- 2026-05-18T05:26:10.455344+00:00: ePK is ready for draft fingerprint specification but not positive-universe expansion; external hard negatives require scored ePK re-audit before any future counting claim.
- 2026-05-18T06:29:09.711385+00:00: ePK now has a review-only draft spec and local evidence audit but remains blocked from positive-universe expansion until scorer threshold external re-audit terminal review and factory gates pass.
- 2026-05-20T13:17:20.692201+00:00: ePK remains review-only; main loop pivoted to external mini-campaign and baseline comparison small wins
- 2026-05-20T14:14:08.715044+00:00: Main loop now has a non-ePK SDR readiness packet and a mini-campaign sequence baseline; Foldseek binary is restored but candidate coordinate sidecars are the active external-screen blocker.
- 2026-05-20T15:32:22.885905+00:00: Frozen prospective mini-campaign is now closed as terminal review-only duplicate evidence rather than blocked by missing coordinate sidecars.
