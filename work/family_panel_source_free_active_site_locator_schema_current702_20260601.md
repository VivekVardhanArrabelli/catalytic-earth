# Family Panel Source-Free Active-Site Locator Schema - current702

Run: 2026-06-01T11:45:01Z

Strict schema contract for the source-free active-site locator sidecars needed before family-panel review rows can enter the predicted active-site geometry retrieval channel.

## Status

- source_free_active_site_locator_schema_ready_review_only
- Target rows: 10
- Required residue locator minimum: 2
- Allowed locator evidence classes: 4
- Forbidden predictive fields: 10

## Required Fields

- artifact_id
- schema_version
- created_utc
- entry_id
- source_accession
- locator_policy
- locator_evidence_class
- source_free_active_site_locator_status
- residue_locators
- forbidden_feature_audit
- split_protection
- ready_for_predicted_geometry_scoring

## Validation Rules

- entry_id must match one of the target review-only family-panel rows
- source_accession must match the already hashed AFDB coordinate accession
- at least two residue_locators are required before geometry scoring
- each residue locator must use sequence positions, not PDB chain residue numbers only
- locator_evidence_class must be one of the allowed classes
- forbidden_feature_audit must prove no entry names, EC/Rhea IDs, source prose, labels, benchmark roles, or panel IDs were used as predictive features
- split_protection must mark heldout/training/threshold-selection use as false until a future explicit import/split decision
- ready_for_predicted_geometry_scoring may be true only when all blockers are cleared and validation passes

## Target Rows

| row | accession | panel | current blockers |
| --- | --- | --- | --- |
| secondary_probe::cobalamin_radical_rearrangement | uniprot:Q59490 | cobalamin_and_radical_rearrangement_panel | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| secondary_probe::radical_sam_enzyme | uniprot:A0A1M6T2I7 | cobalamin_and_radical_rearrangement_panel | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| external_glycoside_panel | uniprot:Q6NSJ0 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| mh_073 | uniprot:P01112 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| mh_064 | uniprot:C7C422 | no_reliable_structure_metal_hydrolase_controls | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| mh_065 | uniprot:Q79MP6 | no_reliable_structure_metal_hydrolase_controls | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| mh_066 | uniprot:P52699 | no_reliable_structure_metal_hydrolase_controls | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| mh_067 | uniprot:P00918 | no_reliable_structure_metal_hydrolase_controls | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| mh_068 | uniprot:P15289 | no_reliable_structure_metal_hydrolase_controls | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |
| mh_072 | uniprot:P0A6P9 | no_reliable_structure_metal_hydrolase_controls | approved_source_free_active_site_locator_missing, not_current702_label_manifest_row, source_backed_sidecar_lacks_residue_locator, source_free_predicted_geometry_retrieval_missing |

## Interpretation

- The blocker now has an explicit schema: geometry scoring can proceed only after target rows have locator sidecars with at least two source-free sequence-position residue locators.
- Implement a validator/materializer for this schema and keep all target rows review-only until locator validation passes.
