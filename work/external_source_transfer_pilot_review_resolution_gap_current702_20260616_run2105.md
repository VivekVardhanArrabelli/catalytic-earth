# External Source-Transfer Review Resolution Gap - Run2105

Date: 2026-06-16

Frozen current702 SHA before work:

- `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`

## Scope

Run2105 mapped the five run2004 normalized source-transfer `needs_review`
rows into explicit review-only repair and decision gaps. No registry apply was
attempted or allowed.

## Artifacts

- `artifacts/v3_external_source_pilot_mechanism_repair_lanes_t12_allvsall_uniref_current702_20260616_run2105_enriched.json`
- `artifacts/v3_external_source_pilot_acyl_coa_lyase_thioesterase_control_t12_allvsall_uniref_current702_20260616_run2105.json`
- `artifacts/v3_external_source_pilot_acyl_coa_lyase_thioesterase_import_safety_adjudication_t12_allvsall_uniref_current702_20260616_run2105.json`
- `artifacts/v3_external_source_pilot_review_resolution_gap_audit_t12_allvsall_uniref_current702_20260616_run2105.json`
- `artifacts/v3_external_source_pilot_review_resolution_gap_audit_t12_allvsall_uniref_with_acyl_import_safety_current702_20260616_run2105.json`
- `artifacts/v3_external_source_pilot_review_resolution_gap_import_safety_current702_20260616_run2105.json`
- `artifacts/v3_external_source_pilot_review_resolution_gap_import_safety_with_acyl_current702_20260616_run2105.json`

## Outcome

- All five rows remain review-only held rows.
- Import-ready rows: **0**.
- Countable label candidates: **0**.
- Review-only import-safety audit after acyl-CoA adjudication replay:
  **safe=True**, **0** unsafe artifacts, **0** new countable labels.
- Q8N0X4 acyl-CoA lyase/thioesterase control:
  `review_only_acyl_coa_lyase_thioesterase_scope_ready` from source-traced active-site residue D320
  and Rhea context. It is now integrated into review-only import-safety adjudication as
  `acyl_coa_lyase_thioesterase_scope_control_repaired`, but remains blocked by explicit review
  decision, representation/heuristic review, and full label-factory gates.
- Latest gap replay status counts:
  **4** `review_decision_and_factory_gate_blocked_after_control_repair` and
  **1** `family_control_unresolved_after_adjudication`.
- Repair lanes are now:
  - C9JRZ8: `add_akr_nadp_redox_representation_axis`
  - O14756: `add_sdr_nad_p_redox_representation_axis`
  - P06746: `add_dna_pol_x_lyase_representation_axis`
  - Q8N0X4: `add_acyl_coa_lyase_thioesterase_scope_control`
  - P33025: `split_glycoside_hydrolase_from_metal_hydrolase_control`

## Gap Map

- C9JRZ8, O14756, P06746, and Q8N0X4 have family control repair recorded, but still
  require an explicit review decision plus duplicate/factory gates before any
  import.
- Q8N0X4 no longer has `family_import_safety_adjudication_missing`; its remaining blockers are
  review/factory/representation/heuristic process blockers, not missing source context.
- P33025 remains `glycoside_boundary_representation_conflict_not_repaired`;
  repair or replace the glycoside boundary control before any review decision.

## Next Action

Record explicit review decisions for the four control-repaired rows and rerun duplicate/factory
gates only after those decisions exist; separately repair or replace the P33025 glycoside-boundary
control. Do not import/apply from run2105 artifacts.
