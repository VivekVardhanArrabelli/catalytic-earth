# External Source-Transfer Review/Factory Closure - Run2004

Date: 2026-06-16

Frozen current702 SHA before work:

- `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`

## Scope

Run2004 advanced the external source-transfer pilot review/factory path for the five
run1904 normalized `needs_review` rows. No registry apply was attempted or allowed.

## Artifacts

- Planning and source state:
  - `artifacts/v3_coverage_redundancy_audit_current702_20260616_run2004_pre_lane.json`
  - `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run2004_pre_lane.json`
  - `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run2004_pre_lane.json`
  - `artifacts/v3_evidence_handle_expansion_current702_20260616_run2004_pre_lane.json`
  - `artifacts/v3_breadth_feasibility_scout_current702_20260616_run2004_pre_lane.json`
  - `artifacts/v3_source_scale_limit_audit_current702_20260616_run2004.json`
- Review/factory replay:
  - `artifacts/v3_external_source_pilot_review_decision_export_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_evidence_packet_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_evidence_dossiers_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_active_site_evidence_decisions_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_success_criteria_t12_allvsall_uniref_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_terminal_decisions_t12_allvsall_uniref_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_decision_confidence_audit_t12_allvsall_uniref_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_decisions_review_normalized_t12_allvsall_uniref_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_t12_allvsall_uniref_current702_20260616_run2004.json`
- Review-only guardrails:
  - `artifacts/v3_external_source_pilot_review_only_import_safety_t12_allvsall_uniref_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_mechanism_repair_lanes_t12_allvsall_uniref_current702_20260616_run2004_enriched.json`
  - `artifacts/v3_external_source_pilot_akr_nadp_repair_control_t12_allvsall_uniref_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_sdr_redox_repair_control_t12_allvsall_uniref_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_dna_pol_x_lyase_repair_control_t12_allvsall_uniref_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_glycoside_hydrolase_boundary_control_t12_allvsall_uniref_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_akr_nadp_import_safety_adjudication_t12_allvsall_uniref_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_sdr_redox_import_safety_adjudication_t12_allvsall_uniref_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_dna_pol_x_lyase_import_safety_adjudication_t12_allvsall_uniref_current702_20260616_run2004.json`
  - `artifacts/v3_external_source_pilot_glycoside_hydrolase_import_safety_adjudication_t12_allvsall_uniref_current702_20260616_run2004.json`

## Outcome

- Coverage stayed **8728** combined labels = **702** frozen + **8026** expansion.
- Open holes: **0**. Floor deficit: **0**. Only `metal_dependent_hydrolase` remains over cap.
- Novelty replay stayed **7565** admit / **414** throttle / **47** reject.
- High-yield factory still has **0** ready existing lanes >=150; top projected clean admits **77**.
- Evidence-handle expansion still shows reachable positive-bronze uplift **741**.
- Breadth feasibility still projects **9673** reviewed-Swiss-Prot clean positives, gap **327** to 10k.
- Source scale audit still recommends `stop_m_csa_only_tranche_growth_and_scope_external_source_transfer`.

The run2004 success replay remains `needs_more_work`:

- `review_decision_not_terminal`: **12**
- `full_label_factory_gate_not_passed`: **12**
- `broader_duplicate_screening_unresolved`: **7**
- `active_site_source_unresolved`: **6**
- `representation_control_unresolved`: **2**
- import-ready rows: **0**
- countable label candidates: **0**

The normalized review queue still has **5** rows: C9JRZ8, O14756, P06746,
Q8N0X4, and P33025. The queue's remaining non-human blockers are
`external_review_decision_artifact_not_built` and `full_label_factory_gate_not_run`
for all five rows.

## Gate Notes

`audit-review-only-import-safety` passed for the normalized run1904 queue and
normalized decisions. A direct `check-label-factory-gates` attempt was blocked by
lineage validation because the required label-factory baseline artifacts are from
slice `500` while this review-only source-transfer audit is slice `20260616`.
No bypass was used, and no registry apply was attempted.

The terminal-decision CLI had a stale optional default for
`--external-structural-tm-holdout-path`. Run2004 fixed it to default to `None`
and added a parser regression so current-slice source-transfer replays are not
silently mixed with the old `1025` structural artifact.

## Next Action

Do not import/apply from run2004 artifacts. The next run should either:

1. Build a source-supported expert review decision artifact for the five queued
   `needs_review` rows, then rerun success criteria and full label-factory gates
   with same-slice baseline inputs; or
2. If no expert-decision artifact can be produced autonomously, continue the
   approved source-transfer path by resolving the remaining seven duplicate-screen
   residue rows only after their stronger active-site/representation blockers are
   addressed.
