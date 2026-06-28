automation: ce-autonomous-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-17T03:09:49Z
started_local: Tue Jun 16 22:09:49 CDT 2026
closeout_at: 2026-06-17T03:58:51Z
elapsed_minutes: 49.0
remaining_minutes: 6.0
budget_minutes: 55
planned_closeout_minute: 50

state: run0310_source_transfer_all_vs_all_no_registry_apply
lock: acquired by this run at 2026-06-17T03:08:31Z
branch: main
origin_main_at_start: 8359eb6e5ef26a454494e6edb12195084b22ef56
base_at_start: 8359eb6e5ef26a454494e6edb12195084b22ef56
origin_main_pre_push_fetch: 8359eb6e5ef26a454494e6edb12195084b22ef56
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

validation:
  registry_validate: passed
  baseline_critical_suite: 525 passed, 14 subtests
  final_affected_suite: 536 passed, 14 subtests
  focused_all_vs_all_transfer_cli: 39 passed, 340 deselected
  final_full_pytest: 2404 passed, 1 warning, 244 subtests
  compileall: passed
  current_docs_reference_check: missing 0 / checked 2206 / ignored 14
  json_jsonl_parse: parsed 94 run0310 JSON artifacts and 693 progress JSONL records before final append
  git_diff_check: passed
  hard_limit_scan_over_90mb: none
  frozen_current702_sha_check: passed

coverage_state:
  combined_labels: 8728
  frozen_rows: 702
  expansion_rows: 8026
  positive_holes: 0
  floor_deficit: 0
  novelty_replay: admit 7565 / throttle 414 / reject 47
  ready_existing_lanes_ge150: 0
  top_projected_clean_admits: 77
  reviewed_swissprot_clean_projection: 9673
  gap_to_10k_positive_bronze: 327

work_completed:
  - acquired automation lock and fast-forward checked origin/main
  - recorded frozen current702 SHA before any apply
  - refreshed coverage, novelty, high-yield factory, evidence-handle, breadth, and source-scale state
  - generated reviewed biotin-dependent carboxylase broad-handle preview with 41 clean novelty-admitted rows, not applied
  - confirmed reviewed biotin offset-250 window fetched 0 rows
  - rebuilt current external source-transfer chain through import readiness, blocker matrix, pilot decisions, and normalized expert queue
  - added run0310 external all-vs-all sequence duplicate screen with real mmseqs2 backend and clean audit
  - refreshed artifact storage inventory, storage policy, migration dry-run, and admission guard
  - attempted bounded NAD/glycosyltransferase live scout; interrupted before preview due slow UniProt entry fetch latency

current_gate_state:
  registry_apply: not attempted
  import_ready_rows: 0
  countable_label_candidate_rows: 0
  transfer_candidate_rows: 47
  transfer_import_readiness_status: 21 active-site sourcing / 14 heuristic control / 9 representation control / 2 sequence holdout / 1 review-factory
  pilot_terminal_decisions: 6 deferred_requires_human_expert / 6 rejected_active_site_evidence_missing
  all_vs_all_duplicate_screen: 47 no-signal rows / 0 exact duplicate / 0 near duplicate / max identity 0.874
  sequence_reference_screen: fail-closed, 30 current-reference top-hit alignments incomplete
  storage_policy: blocked on 4 large unclassified artifacts at 50 MB policy threshold; no files over 90 MB
  registry_apply_blocker: no import-ready rows; active-site, representation, UniRef-wide duplicate, terminal review, factory, novelty, governor, and row-guardrail gates remain required

next_action: >
  Do not import the biotin preview or run0310 source-transfer review-only rows. Add or expose a
  current needs_review_resolution producer so run0310 mechanism-repair lanes and review-resolution
  gap replay can run, or directly resolve the remaining active-site sourcing, real representation
  backend/control, UniRef-wide duplicate, terminal review, full label-factory, novelty, governor,
  and row-guardrail gates before any import/apply.

## Automation run ce-nad-glyco-floor-expansion start
- started_at_utc: 2026-06-28T01:30:17Z
- started_local: Sat Jun 27 20:30:17 CDT 2026
- budget_minutes: 55
- planned_closeout_minute: 50
- frozen_current702_sha_before: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

## Automation run ce-nad-glyco-floor-expansion closeout
- closeout_at_utc: 2026-06-28T01:49:00Z
- elapsed_minutes: 18.7
- remaining_minutes: 36.3
- state: predicted_geometry_atlas_prereg_blocked_current57_router_drift
- branch: main
- origin_main_at_start: ae6b313fed4d0c2f7e8952520c5251676a626b21
- registry_mutation: none
- frozen_current702_sha_after: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
- work_completed:
  - added and ran predicted-geometry atlas-engine full-env/preregistration artifact
  - added row-level train/cal diagnostics to cofactor-fusion operating-point builder
  - preserved current-57 cofactor precision rerun as a diagnostic artifact, not a replacement contract
  - updated project state, decision log, handoff, and docs artifact-reference check
- current_gate_state:
  - existing scored fold/TM surfaces reusable: true
  - new Foldseek/TM scoring runnable: false (foldseek missing)
  - current-router cofactor precision drift detected: true
  - cached atlas-engine readout allowed now: false
- validation:
  - registry_validate: passed
  - focused_recovery_precision_tests: 86 passed, 2 subtests
  - full_pytest: 2524 passed, 1 warning, 244 subtests
  - compileall: passed
  - current_docs_reference_check: missing 0
  - json_jsonl_parse: 4581 JSON files and 715 progress JSONL records parsed
  - git_diff_check: passed
- next_action: >
  Resolve the current-router/fingerprint-surface drift before atlas-engine fusion: either freeze/replay
  the intended June 9 cofactor precision router surface, or preregister a new current-57 train/cal
  precision rule. Install/expose foldseek before new Foldseek/TM scoring.

## Automation run 2026-06-28T02:31:07Z
- started_at_utc: 2026-06-28T02:31:07Z
- started_local: Sat Jun 27 21:31:07 CDT 2026
- budget_minutes: 55
- planned_closeout_minute: 50
- frozen_current702_sha_before: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
- status: in_progress

## Automation run ce-nad-glyco-floor-expansion closeout
- closeout_at_utc: 2026-06-28T02:51:33Z
- elapsed_minutes: 20.4
- remaining_minutes: 34.6
- state: current57_cofactor_precision_contract_fail_closed_atlas_prereg_updated
- branch: main
- origin_main_at_start: 60b17cdf2635843f3fc62beb71ad5e7ed26915e9
- registry_mutation: none
- frozen_current702_sha_after: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
- work_completed:
  - added current-57 cofactor precision contract builder and CLI
  - generated fail-closed current-57 precision contract artifact/report
  - integrated contract blocker into predicted-geometry atlas-engine preregistration
  - regenerated docs artifact-reference check and updated project state/decision log/handoff
- current_gate_state:
  - current57_precision_contract_status: blocked_current57_cofactor_precision_contract_not_deployable
  - current57_exact_fused_calibration: 13/35 recovery, 26/26 OOS FP
  - current57_v1_metal_compatible_calibration: 26/35 recovery, 26/26 OOS FP
  - best_under_trusted_oos_fp_ceiling: threshold 0.733, 20/35 recovery, 8/26 OOS FP
  - atlas_prereg_status: preregistered_cached_surface_blocked_current57_precision_contract_new_foldseek_backend_blocked
- validation:
  - focused_contract_prereg_tests: 8 passed, 242 deselected
  - focused_recovery_precision_suite: 89 passed, 2 subtests
  - registry_validate: passed
  - full_pytest_final: 2528 passed, 1 warning, 244 subtests
  - compileall: passed
  - current_docs_reference_check: missing 0
  - json_jsonl_parse: 10723 JSON files and 8336 JSONL records across 27 JSONL files
  - git_diff_check: passed
- next_action: >
  Do not run atlas-engine fusion or heldout on the current-57 cofactor surface. Pin/replay
  the intended June 9 router/fingerprint surface, or build a new preregistered current-57
  precision channel/fusion rule that clears a train/cal recovery/OOS done bar. Install/expose
  foldseek before any new Foldseek/TM scoring.

## Automation run 2026-06-28T03:32:44Z
- started_at_utc: 2026-06-28T03:32:44Z
- started_local: Sat Jun 27 22:32:44 CDT 2026
- budget_minutes: 55
- planned_closeout_minute: 50
- frozen_current702_sha_before: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
- status: in_progress

## Automation run ce-nad-glyco-floor-expansion closeout
- closeout_at_utc: 2026-06-28T03:55:47Z
- elapsed_minutes: 23.1
- remaining_minutes: 31.9
- state: current57_cofactor_fold_alignment_blocked_recompute_manifest_ready
- branch: main
- origin_main_at_start: b94d0e25e01cb4cc1680a15f2b9fc6992ff77a6b
- registry_mutation: none
- frozen_current702_sha_after: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
- work_completed:
  - added current-57 cofactor/fold row-alignment audit and CLI
  - generated fail-closed alignment artifact/report: 4/35 calibration in-scope overlap, 0/26 calibration OOS overlap
  - integrated alignment blocker into predicted-geometry atlas-engine preregistration
  - added no-score current-57 Fold/TM recompute input manifest and CLI
  - generated recompute manifest with 61/61 calibration query CIFs and 133/133 train target CIFs staged train/cal-safe
  - updated project state, decision log, handoff, and docs artifact-reference check
- current_gate_state:
  - cached_atlas_engine_fusion_runnable: false
  - current57_precision_contract_blocks: true
  - current57_fold_alignment_blocks: true
  - foldseek_available_for_new_scoring: false
  - recompute_manifest_status: current57_fold_tm_recompute_input_manifest_ready_foldseek_missing
  - heldout_rows_scored: false
- validation:
  - focused_alignment_recompute_prereg_cli_tests: 13 passed, 232 deselected
  - focused_recovery_precision_suite: 94 passed, 232 deselected, 2 subtests
  - compileall: passed
  - full_pytest_final: 2536 passed, 1 warning, 244 subtests
  - registry_validate: passed
  - current_docs_reference_check: missing 0
  - json_jsonl_parse: 10725 JSON files and 8338 JSONL records across 27 JSONL files
  - git_diff_check: passed
- next_action: >
  Install/expose foldseek, materialize the current-57 Fold/TM recompute manifest staging plan,
  run its recorded calibration-vs-train easy-search command, then build a current-57 fold/TM
  score readout before any cached atlas-engine fusion or heldout read. Alternative: pin/replay
  the intended June 9 router/fold row surface.

## Automation run 2026-06-28 (continuation: foldseek recompute + readout)
- started_from: origin last commit 79dc2d3a (branch claude/continue-last-commit-ytktge)
- registry_mutation: none
- frozen_current702_sha: unchanged
- state: current57_fold_tm_recomputed_row_alignment_resolved_fold_nn_separates_inscope_oos
- work_completed:
  - installed foldseek 718d42176d2f67d36a60866fedfb881f8d5a7ebf (user-authorized) and ran the manifest easy-search
  - produced calibration_vs_current57_train_atlas.tsv (4756 rows, 61 queries x 132 targets)
  - added current57_fold_tm_recompute_readout builder + CLI + tests
  - readout row-aligned: in-scope 35/35, OOS 26/26 (cached was 4/35, 0/26)
  - fold-NN separation: in-scope median alntm 0.743 vs OOS 0.566 (gap 0.177); fingerprint match 28/35
  - updated project_state, decision_log, handoff; regenerated docs reference check (missing 0)
- current_gate_state:
  - cofactor_fold_alignment_blocker: resolved
  - current57_precision_contract_blocks: true (OOS FP 26/26, deployment still gated)
  - fold_augmented_fusion_preregistered: false (next action)
  - heldout_rows_scored: false
  - threshold_selected_on_heldout: false
- validation:
  - focused_readout_and_cli_unittest: 241 passed
  - compileall: passed
  - registry_validate: passed
  - current_docs_reference_check: missing 0
  - git_diff_check: passed
- next_action: >
  Preregister a current-57 cofactor+fold fusion rule using the now row-aligned fold-NN surface as the
  OOS-rejection/abstention channel; test on train/cal against the trusted June 9 in-scope-recovery /
  OOS-FP bar before any heldout read. The current-57 cofactor precision contract still governs
  deployment; this readout alone does not authorize fusion.

## Automation run 2026-06-28 (continuation: cofactor+fold fusion preregistration)
- started_from: prior commit a177f460 (branch claude/continue-last-commit-ytktge)
- registry_mutation: none
- frozen_current702_sha: unchanged
- state: current57_cofactor_fold_fusion_preregistered_fail_closed_router_recovery_ceiling_blocks_bar
- work_completed:
  - added current57_cofactor_fold_fusion_preregistration builder + CLI + tests
  - preregistered two-gate rule (cofactor score AND fold-NN TM OOS-rejection gate), calibration-only sweep
  - status blocked_current57_cofactor_fold_fusion_not_deployable; eligible points 0
  - fold marginal value: cofactor-only 20/35 @ FP6 -> fusion 23/35 @ FP8 (+3); max-precision 20/35 @ FP5
  - compatible recovery ceiling 26/35 (exact 13/35) < trusted 30/35 bar -> recovery is the binding constraint
  - updated project_state, decision_log, handoff; regenerated docs reference check (missing 0)
- current_gate_state:
  - cofactor_fold_alignment_blocker: resolved (prior run)
  - fold_nn_oos_rejection_signal: confirmed (+3 recovery at OOS-FP ceiling)
  - binding_constraint: current57_router_compatible_recovery_ceiling_26_of_35
  - eligible_fusion_points: 0
  - heldout_rows_scored: false
  - threshold_selected_on_heldout: false
- validation:
  - focused_fusion_readout_cli_unittest: passed
  - compileall: passed
  - registry_validate: passed
  - current_docs_reference_check: missing 0
  - git_diff_check: passed
- next_action: >
  Pin/replay the intended June 9 router/fingerprint surface so in-scope recovery clears the trusted
  bar, then re-apply this fold-NN OOS-rejection gate and promote one calibration operating point to a
  single heldout-final read. Router recovery (26/35 ceiling), not OOS FP, is the blocker; more
  fingerprint families will not move it.

## Automation run 2026-06-28 (continuation: June 9 router replay + fold fusion)
- started_from: prior commit 0079855d (branch claude/continue-last-commit-ytktge)
- registry_mutation: none (main repo); June 9 surface reproduced via isolated worktree registry pin
- frozen_current702_sha: unchanged; main-repo registry validated intact at 57 fingerprints
- state: june9_router_replay_reproduces_bar_fold_gate_no_pareto_improvement
- work_completed:
  - reproduced June 9 router per-row surface (isolated worktree, registry pinned to d567ee0d, 8 families)
  - exact reproduction of trusted June 9: fused 30/35 @ 9/26 frozen, 30/35 @ 8/26 at 0.44 dial
  - committed pinned per-row surface + added june9_router_fold_fusion_readout builder/CLI/tests
  - fold-NN gate on June 9: no Pareto improvement at 30/35 (stays 8/26); frontier 28/35@6, 23/35@1, 18/35@0
  - residual OOS FPs high-fold-similar (0.43-0.73); 7/8 are metal_dependent_hydrolase
  - corrected prior read: fold +3 recovery was specific to the drifted current-57 router
  - updated project_state, decision_log, handoff; regenerated docs reference check (missing 0)
- current_gate_state:
  - june9_router_reproducible: true (current code + pinned June 9 registry)
  - june9_dial_operating_point: 30/35 recovery, 8/26 OOS FP
  - fold_gate_pareto_improves_june9: false (precision/recall dial only)
  - main_repo_registry_mutated: false
  - heldout_rows_scored: false
- validation:
  - focused_june9_readout_fusion_cli_unittest: passed
  - compileall: passed
  - registry_validate: passed (57 fingerprints)
  - current_docs_reference_check: missing 0
  - git_diff_check: passed
- next_action: >
  Pick the deployment operating point on the June 9 router (default dial 30/35 @ 8/26, or a narrower
  near-zero-OOS-FP fold-dial regime) and spend the single heldout-final read to confirm it. Do not grow
  fingerprint families to chase recovery (the drift is a taxonomy-version artifact). Consider pinning
  the production cofactor-precision router to the June 9 fingerprint resolution.

## Automation run 2026-06-28 (continuation: off-M-CSA fold abstention generalization)
- started_from: prior commit ffb970df (branch claude/continue-last-commit-ytktge)
- registry_mutation: none; main-repo registry validated intact at 57 fingerprints
- trigger: heldout is M-CSA-only (699/702), so it cannot probe the deployment distribution
- state: fold_nn_abstention_signal_generalizes_off_mcsa
- work_completed:
  - fold-scored 52 external non-M-CSA hard negatives vs the M-CSA train in-scope atlas (foldseek, 4117 rows)
  - added external_offmcsa_fold_abstention_readout builder/CLI/tests
  - external negative fold-NN median 0.574 ~= M-CSA OOS 0.566, << in-scope 0.743 (only 2/52 reach in-scope median)
  - frontier: fold>=0.70 leaves 3/52 external negatives un-abstained (M-CSA OOS 4/26 in step), in-scope 20/35
  - verdict: fold-NN OOS-rejection generalizes off M-CSA (the cofactor channel's missing property)
  - updated project_state, decision_log, handoff; regenerated docs reference check (missing 0)
- current_gate_state:
  - fold_offmcsa_oos_rejection_signal: confirmed
  - fold_offmcsa_inscope_recovery: not yet tested (needs non-M-CSA positives)
  - main_repo_registry_mutated: false
  - heldout_rows_scored: false
- validation:
  - focused_offmcsa_readout_cli_unittest: passed
  - compileall: passed
  - registry_validate: passed (57 fingerprints)
  - current_docs_reference_check: missing 0
  - git_diff_check: passed
- next_action: >
  Assemble a non-M-CSA positive surface (known mechanism class + AlphaFold structure, off M-CSA) and
  measure off-M-CSA in-scope recovery via the same fold-NN-to-M-CSA-atlas retrieval, so both halves of
  the deployment question (recovery and abstention) are characterized off-distribution. The fold
  channel, not more fingerprint families, is the lever.

## Automation run 2026-06-28 (continuation: off-M-CSA recovery feasibility)
- started_from: prior commit 8b6566dc (branch claude/continue-last-commit-ytktge)
- registry_mutation: none; read-only feasibility, no download
- state: offmcsa_recovery_data_blocked_no_trusted_labeled_nonmcsa_structures
- work_completed:
  - added offmcsa_recovery_feasibility builder/CLI/tests; inventoried 42 structured surfaces
  - 248 non-M-CSA structured accessions locally, 0 production-label-ready (wave2: 0 ready, 600 in review)
  - trusted bronze positives have labels but no local structures -> recovery test blocked
  - fixed accession regex bug ([A-NR-Z0-9] dropped O/P/Q; -> 248 not 11)
  - updated project_state, decision_log, handoff; regenerated docs reference check (missing 0)
- current_gate_state:
  - offmcsa_abstention_half: done (generalizes)
  - offmcsa_recovery_half: data-blocked (needs trusted-labeled non-M-CSA structures)
  - download_decision_pending: true (bounded AlphaFold fetch OR promote wave2 candidates via import gates)
  - registry_mutated: false; heldout_rows_scored: false
- validation:
  - focused_feasibility_cli_unittest: passed
  - compileall: passed
  - registry_validate: passed (57 fingerprints)
  - current_docs_reference_check: missing 0
  - git_diff_check: passed
- next_action: >
  Get user decision: authorize a bounded AlphaFold download for a sample of trusted bronze positives,
  or authorize promoting structured wave2 candidates through the import/label-factory gates. Then run
  the off-M-CSA in-scope recovery readout (fold-NN vs the M-CSA train atlas). Do not grow families.

## Automation run 2026-06-28 (continuation: fold-NN recovery harness + M-CSA baseline)
- started_from: prior commit 3f94b35b (branch claude/continue-last-commit-ytktge)
- registry_mutation: none; no download; off-M-CSA run remains gated on a user decision
- state: fold_nn_recovery_harness_ready_mcsa_baseline_28_of_35
- work_completed:
  - added fold_nn_mechanism_recovery_readout harness (module/CLI/tests), surface-agnostic
  - M-CSA in-distribution baseline: recovery 28/35 (0.80) no abstention (reproduces recompute match)
  - confidence-gated precision-on-retained: fold>=0.65 24/25 (0.96), fold>=0.74 17/18 (0.94)
  - harness ready to run off-M-CSA via --positives + off-M-CSA TSV once a labelled positive set exists
  - updated project_state, decision_log, handoff; regenerated docs reference check (missing 0)
- current_gate_state:
  - fold_nn_recovery_harness_ready: true
  - mcsa_baseline_recovery: 28/35 (0.80); precision-gated 0.96 at fold>=0.65
  - offmcsa_recovery_run: still gated on trusted-labeled non-M-CSA structures (user decision)
  - registry_mutated: false; downloads_performed: false; heldout_rows_scored: false
- validation:
  - focused_recovery_harness_cli_unittest: passed
  - compileall: passed
  - registry_validate: passed (57 fingerprints)
  - current_docs_reference_check: missing 0
  - git_diff_check: passed
- next_action: >
  On the user's decision, materialize/promote a trusted-labeled non-M-CSA positive set with structures,
  foldseek it vs the M-CSA train atlas, and run build-fold-nn-mechanism-recovery-readout --positives ...
  to compare off-M-CSA recovery against the 28/35 M-CSA baseline. Do not grow families.

## Automation run 2026-06-28 (continuation: held-out one-shot pre-registration)
- started_from: prior commit eea36c59 (branch claude/continue-last-commit-ytktge)
- registry_mutation: none; no held-out scoring; locked contract only
- state: heldout_oneshot_preregistered_not_yet_run
- work_completed:
  - verified session leakage status: no training, no heldout scoring, no data/ mutation
  - added heldout_oneshot_preregistration builder/CLI/tests
  - locked June 9 router @ 0.44 dial; 126-row heldout set (47 in-scope + 79 OOS) content-hashed 45632519...
  - pre-committed PASS bar: recovery >= 0.70 AND OOS-FP rate <= 0.40 (calibration 0.857/0.308 minus ~2 SE)
  - one-shot guardrail; heldout labels used only to freeze the set; bar from calibration only
  - updated project_state, decision_log, handoff; regenerated docs reference check (missing 0)
- current_gate_state:
  - heldout_preregistration_locked: true (sha256 45632519..., deterministic)
  - heldout_test_executed: false (separately authorized one-shot)
  - heldout_execution_path_implemented: false (must match frozen sha when built)
  - registry_mutated: false; heldout_rows_scored: false
- validation:
  - focused_prereg_cli_unittest: passed
  - compileall: passed
  - registry_validate: passed (57 fingerprints)
  - current_docs_reference_check: missing 0
  - git_diff_check: passed
- next_action: >
  Decide whether to authorize the frozen held-out one-shot (certifies M-CSA generalization only) and/or
  the still-pending off-M-CSA recovery data decision. The pre-registration is locked; execution is a
  separate authorized step that must match sha256 45632519... Do not grow families.

## Automation run 2026-06-28 (continuation: off-M-CSA recovery download manifest)
- started_from: prior commit 862a13e9 (branch claude/continue-last-commit-ytktge)
- registry_mutation: none; no download performed
- state: offmcsa_recovery_download_manifest_ready_awaiting_authorization
- work_completed:
  - located expansion positives (external_bronze_labels shards, 9299 rows)
  - added offmcsa_recovery_download_manifest builder/CLI/tests
  - selected 162 trusted high-confidence non-M-CSA atlas-family positives (~97 MB, 4 families)
  - accession-list sha256 1887478a...; AFDB v4 URL pattern recorded; fetch procedure documented
  - updated project_state, decision_log, handoff; regenerated docs reference check (missing 0)
- current_gate_state:
  - download_manifest_ready: true (162 CIFs, ~97 MB)
  - download_performed: false (awaiting sign-off)
  - disk_free_gib: 25 (above 10 GiB floor)
  - heldout_oneshot: locked, unspent
  - registry_mutated: false
- validation:
  - focused_download_manifest_cli_unittest: passed
  - compileall: passed
  - registry_validate: passed (57 fingerprints)
  - current_docs_reference_check: missing 0
  - git_diff_check: passed
- next_action: >
  On sign-off, fetch the 162 manifest CIFs (skip-if-exists, stop below 10 GiB), foldseek vs the M-CSA
  train atlas, and run build-fold-nn-mechanism-recovery-readout --positives <map> to compare off-M-CSA
  recovery against the 28/35 baseline. Do not grow families.
