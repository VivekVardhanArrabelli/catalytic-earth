# External Source-Transfer UniRef Review Queue - Run1904

Date: 2026-06-16

Source artifacts:

- `artifacts/v3_external_source_pilot_decision_confidence_audit_t12_allvsall_uniref_current702_20260616_run1904.json`
- `artifacts/v3_external_source_pilot_human_expert_review_queue_normalized_t12_allvsall_uniref_current702_20260616_run1904.json`
- `artifacts/v3_external_source_pilot_mechanism_repair_lanes_t12_allvsall_uniref_current702_20260616_run1904_enriched.json`

This queue is review-only. It records the five rows that cleared the
all-vs-all plus UniRef/current-reference duplicate process screen but still
need explicit review/factory decisions before any import path can run.

| Accession | Lane | Confidence | Active-site / reaction context | Duplicate status | Representation status | Repair lane | Smallest next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C9JRZ8 | oxidoreductase long tail | needs_review | explicit active-site source; specific reaction context | current-reference/all-vs-all/UniRef no signal | adjudicated review-only | add_akr_nadp_redox_representation_axis | Build a bounded AKR/NADP contrast row using active-site and InterPro context before any new pilot decision. |
| O14756 | oxidoreductase long tail | needs_review | explicit active-site source; specific reaction context | current-reference/all-vs-all/UniRef no signal | stability changed requires review | add_sdr_nad_p_redox_representation_axis | Add a review-only SDR/NAD(P) contrast set from source-supported external rows and current countable references, then rerun representation/heuristic disagreement checks. |
| P06746 | lyase | needs_review | explicit active-site source; specific reaction context | current-reference/all-vs-all/UniRef no signal | adjudicated review-only | add_dna_pol_x_lyase_representation_axis | Map a DNA Pol X/5'-dRP lyase representation contrast control before treating high cosine alone as duplicate evidence. |
| Q8N0X4 | lyase | needs_review | explicit active-site source; specific reaction context | current-reference/all-vs-all/UniRef no signal | stability changed requires review | manual_source_mechanism_review_required | Inspect source-supported reaction and active-site context before adding another control. |
| P33025 | glycan chemistry | low_confidence | explicit active-site source; specific reaction context | current-reference/all-vs-all/UniRef no signal | representation near-duplicate holdout | split_glycoside_hydrolase_from_metal_hydrolase_control | Add a glycoside-hydrolase boundary control and rerun the glycan chemistry representation/heuristic comparison. |

## Remaining Shared Blockers

- `external_review_decision_artifact_not_built`
- `full_label_factory_gate_not_run`
- heuristic control still needs review for rows whose confidence audit flags
  heuristic/top1 mismatch or not-scored context
- representation-control review remains required for O14756, Q8N0X4, and P33025

## Lower-Priority Duplicate-Screen Residue

Seven pilot rows still carry `broader_duplicate_screening_required` in success
criteria, but they are not the highest-yield next action for import readiness:
P55263 is already a representation near-duplicate holdout, and A2RUC4, P00568,
P27144, O95050, P51580, and Q32P41 still lack explicit active-site source
resolution. Screening those seven further would not create import-ready rows
without first resolving stronger terminal/process blockers.

## Non-Decision Boundary

No row in this queue is accepted, countable, import-ready, or authorized for an
external-registry apply. The next run should use this as a routing note only:
build the necessary review/factory/control artifacts, then rerun success
criteria, import-safety adjudication, novelty, governor, and row guardrails.
