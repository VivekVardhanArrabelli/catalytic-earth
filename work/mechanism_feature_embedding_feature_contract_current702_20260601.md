# Mechanism-Feature Embedding Feature Contract - current702

Run: 2026-06-01T12:52:27Z

No-fit feature contract for the mechanism-feature embedding pilot. It enumerates train/cal feature rows and permitted feature groups while excluding labels and heldout rows from the feature surface.

## Status

- mechanism_feature_embedding_feature_contract_ready_no_model_fit
- Feature rows: 524
- Train rows: 418
- Calibration rows: 106
- Heldout excluded rows: 140
- Missing input records: 0

## Feature Groups

| group | fields | source |
| --- | --- | --- |
| active_site_role_graph | status, active_site_residue_count | mechanism_feature_active_site_role_graph_sidecar |
| reaction_center_template | status, reaction_chemical_operation | mechanism_feature_reaction_center_template_sidecar |
| organic_cofactor_scores | flavin_selected_score, heme_selected_score, plp_selected_score | selected_organic_cofactor_sidecar |
| inorganic_cofactor_loci | cobalamin_locus, iron_sulfur_locus, metal_ion_locus, radical_sam_locus | metal/cobalamin/radical-SAM/Fe-S locus sidecars |

## Excluded As Features

- entry_id
- fingerprint_id
- label_type
- stratum
- split_assignment
- assigned_embedding_split
- source_artifact_paths
- heldout_labels_or_outcomes

## Blockers Before Model Fit

- explicit_authorization_required_before_model_weights_are_fit
- feature_vector_materializer_not_written
- directed_electron_or_proton_transfer_edges_not_materialized
- row_specific_bond_change_mapping_not_materialized
- heldout_final_evaluation_must_remain_once_only

## Interpretation

- 524 train/cal rows have a label-stripped feature-row contract; no model was fit.
- If authorized, implement a materializer that consumes only these feature fields, fits on train rows, selects on calibration rows, and evaluates heldout once.
