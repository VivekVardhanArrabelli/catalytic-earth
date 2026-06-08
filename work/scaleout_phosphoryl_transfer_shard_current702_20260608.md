# Phosphoryl-Transfer Boundary Scale-Out Shard

- Artifact: `artifacts/v3_scaleout_phosphoryl_transfer_shard_current702_20260608.json`
- Candidate rows: `1281`
- STARTED_AT_UTC: `2026-06-08T15:11:23Z`
- STARTED_AT_LOCAL: `2026-06-08T10:11:23-0500`
- Lock: `/tmp/ce_scaleout_phosphoryl_transfer.lock`
- Lane: candidate/evidence only; no registry, ontology, import, threshold, split, weight, heldout training, or tuning changes.

## Terminal State Counts

- `blocked_coordinate`: `16`
- `blocked_family_decision`: `142`
- `blocked_locator`: `33`
- `countable_candidate_preflight_only`: `1`
- `reject/OOS_preserve_signal`: `885`
- `review_only_evidence`: `204`

## Subfamily Counts

- `amp_adp_product_state_discriminator`: `5`
- `askha_sugar_acetate_kinase`: `6`
- `atp_grasp_phosphointermediate_ligase`: `21`
- `dnk_deoxynucleoside_kinase`: `2`
- `epk_atp_gamma_transfer`: `906`
- `ghkl_bergerat_histidine_or_pdk_kinase`: `2`
- `hard_oos_nonhydrolytic_metal_nucleotide_control`: `116`
- `ndk_phosphohistidine_nucleotide_exchange`: `8`
- `ntpase_atpase_hydrolysis_boundary`: `17`
- `nuclease_phosphodiesterase_nontransfer_control`: `22`
- `pfka_phosphofructokinase`: `11`
- `pfkb_ribokinase_like`: `13`
- `phosphatase_phosphoesterase_hydrolysis_boundary`: `41`
- `phosphoryl_transfer_general_review_queue`: `86`
- `sugar_phosphate_nontransfer_control`: `23`
- `sulfate_adenylyltransferase_aps_kinase`: `2`

## Evidence Coverage

- `candidate_rows`: `1281`
- `active_site_or_locator_evidence_present`: `909`
- `coordinate_or_structure_provenance_available`: `993`
- `ligand_or_nucleotide_context_present`: `213`
- `duplicate_screen_or_internal_merge_present`: `1281`
- `source_hashes_present`: `1281`
- `machine_actionable_next_step_present`: `1281`

## Review Queues

Top blocked-family candidates are the ePK/PDB topology and current UniProt kinase rows that need source-free substrate-mode or family-lane decisions.
Top reject/OOS candidates preserve ADP/product-state, non-transfer, current-hydrolase-control, and no-topology hard-negative signal.
Locator repair is concentrated in gamma-to-hydroxyl measurements and family-specific homolog rows where acceptor identity or mapping is not measurement-ready.

## Guardrail Notes

Mechanism text, names, labels, EC/Rhea IDs, target names, and source IDs are retained only as provenance/rationale when already present in source artifacts; they are not scoring features in this lane.
