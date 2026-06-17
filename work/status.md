automation: ce-autonomous-bronze-scaleout-pipeline
automation_id: ce-nad-glyco-floor-expansion
started_at: 2026-06-17T02:08:10Z
started_local: Tue Jun 16 21:08:10 CDT 2026
closeout_at: 2026-06-17T02:40:32Z
elapsed_minutes: 32.4
remaining_minutes: 22.6
budget_minutes: 55
planned_closeout_minute: 50

state: run0210_closed_no_registry_apply_scale_wall_blocked
lock: acquired by this run at 2026-06-17T02:08:10Z
branch: main
origin_main_at_start: a11ee18680aaa74c1959798434dcb5b4a29dcb30
base_at_start: a11ee18680aaa74c1959798434dcb5b4a29dcb30
registry_mutation: none
frozen_sha_before_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505
frozen_sha_after_apply: 5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505

validation:
  registry_validate: passed
  baseline_critical_suite: 448 passed, 160 subtests
  final_affected_suite: 428 passed, 160 subtests
  final_full_pytest: 2404 passed, 1 warning, 244 subtests
  compileall: passed
  current_docs_reference_check: missing 0
  git_diff_check: passed
  hard_limit_scan_over_90mb: none
  frozen_current702_sha_check: unchanged

coverage_state:
  combined_labels: 8728
  frozen_rows: 702
  expansion_rows: 8026
  positive_holes: 0
  floor_deficit: 0
  novelty_replay:
    admit: 7565
    throttle: 414
    reject: 47
  over_cap:
    - metal_dependent_hydrolase

work_completed:
  - acquired automation lock and fast-forward checked origin/main
  - recorded frozen current702 SHA before any apply
  - added terminal-review/factory replay audit builder, CLI wiring, and tests
  - consumed five terminal decisions from the run0009 replay queue; all remain human-expert deferred
  - added bounded fetch support to the NAD(P)/glycosyltransferase runner and writer
  - refreshed high-yield lane, evidence-handle, breadth-feasibility, source-scale, coverage, and novelty audits
  - generated no-apply probes for glycosyltransferase, NAD(P) dehydrogenase, biotin carboxylase, terpene cyclase, protein kinase, and SDR
  - ran row-guardrail audits for each generated preview
  - updated durable project state, scaling plan, handoff, status, and progress log

current_gate_state:
  registry_apply: not attempted
  import_ready_rows: 0
  countable_label_candidate_rows: 0
  terminal_review_factory_replay_rows: 5
  terminal_review_decision_recorded_rows: 5
  terminal_review_decision_accepted_rows: 0
  terminal_review_status_counts:
    deferred_requires_human_expert: 5
  no_apply_probe_summary:
    glycosyltransferase_admitted: 0
    nad_p_dehydrogenase_mechanism_corroborated: 21
    nad_p_dehydrogenase_held_at_cap: 17
    biotin_dependent_carboxylase_novelty_admitted_subthreshold: 8
    terpene_cyclase_admitted: 0
    protein_kinase_admitted: 0
    short_chain_dehydrogenase_reductase_admitted: 0

early_closeout_reason: >
  After terminal replay and current-state source probes, the remaining safe scaling choices were
  concretely blocked: there are no holes or floor deficits, no ready existing lane projected at
  >=150 clean admits, terminal decisions remain deferred for human/expert review, and all probed
  lanes were capped, already-at-floor subthreshold, or zero-yield. Applying tiny fragments would
  violate the scale-wall policy.

next_action: >
  Do not import the five terminal-deferred rows, the biotin fragment, or cap-probe rows. Resolve
  the human/expert terminal-review blocker for Q6NSJ0/C9JRZ8/O14756/P06746/Q8N0X4, or formalize
  a higher-yield external source-transfer/source-handle lane beyond reviewed Swiss-Prot with
  duplicate screening, active-site/source resolution, full label-factory, novelty, governor, and
  row-guardrail gates.
