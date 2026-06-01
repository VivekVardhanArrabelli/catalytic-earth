# Family Panel Source-Free Active-Site Locator Materialization Plan - current702

Run: 2026-06-01T11:54:14Z

Review-only plan for materializing source-free active-site locator sidecars for the 10 fold-scored family-panel rows. This creates no locator sidecars and does not score predicted geometry.

## Status

- source_free_active_site_locator_materialization_plan_ready_review_only
- Planned rows: 10
- Locator sidecars present before plan: 0
- Locator sidecars ready before plan: 0
- Suggested locator policy counts: {'structure_local_ligand_geometry_without_source_text_candidate_requires_validator': 8, 'train_cal_template_alignment_without_heldout_rows_candidate_requires_split_check': 2}

## Row Plans

| rank | row | accession | planned sidecar | suggested policy | blockers |
| ---: | --- | --- | --- | --- | --- |
| 1 | secondary_probe::cobalamin_radical_rearrangement | uniprot:Q59490 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/secondary_probe_cobalamin_radical_rearrangement_Q59490.json | structure_local_ligand_geometry_without_source_text_candidate_requires_validator | locator_sidecar_missing, forbidden_feature_audit_required, manual_or_algorithmic_source_free_locator_validation_required, predicted_geometry_scorer_must_consume_locator_sidecar_after_audit_passes |
| 2 | secondary_probe::radical_sam_enzyme | uniprot:A0A1M6T2I7 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/secondary_probe_radical_sam_enzyme_A0A1M6T2I7.json | structure_local_ligand_geometry_without_source_text_candidate_requires_validator | locator_sidecar_missing, forbidden_feature_audit_required, manual_or_algorithmic_source_free_locator_validation_required, predicted_geometry_scorer_must_consume_locator_sidecar_after_audit_passes |
| 3 | external_glycoside_panel | uniprot:Q6NSJ0 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/external_glycoside_panel_Q6NSJ0.json | structure_local_ligand_geometry_without_source_text_candidate_requires_validator | locator_sidecar_missing, forbidden_feature_audit_required, manual_or_algorithmic_source_free_locator_validation_required, predicted_geometry_scorer_must_consume_locator_sidecar_after_audit_passes |
| 4 | mh_073 | uniprot:P01112 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_073_P01112.json | structure_local_ligand_geometry_without_source_text_candidate_requires_validator | locator_sidecar_missing, forbidden_feature_audit_required, manual_or_algorithmic_source_free_locator_validation_required, predicted_geometry_scorer_must_consume_locator_sidecar_after_audit_passes |
| 5 | mh_064 | uniprot:C7C422 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_064_C7C422.json | structure_local_ligand_geometry_without_source_text_candidate_requires_validator | locator_sidecar_missing, forbidden_feature_audit_required, manual_or_algorithmic_source_free_locator_validation_required, predicted_geometry_scorer_must_consume_locator_sidecar_after_audit_passes |
| 6 | mh_065 | uniprot:Q79MP6 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_065_Q79MP6.json | structure_local_ligand_geometry_without_source_text_candidate_requires_validator | locator_sidecar_missing, forbidden_feature_audit_required, manual_or_algorithmic_source_free_locator_validation_required, predicted_geometry_scorer_must_consume_locator_sidecar_after_audit_passes |
| 7 | mh_066 | uniprot:P52699 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_066_P52699.json | structure_local_ligand_geometry_without_source_text_candidate_requires_validator | locator_sidecar_missing, forbidden_feature_audit_required, manual_or_algorithmic_source_free_locator_validation_required, predicted_geometry_scorer_must_consume_locator_sidecar_after_audit_passes |
| 8 | mh_067 | uniprot:P00918 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_067_P00918.json | train_cal_template_alignment_without_heldout_rows_candidate_requires_split_check | locator_sidecar_missing, forbidden_feature_audit_required, manual_or_algorithmic_source_free_locator_validation_required, predicted_geometry_scorer_must_consume_locator_sidecar_after_audit_passes |
| 9 | mh_068 | uniprot:P15289 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_068_P15289.json | train_cal_template_alignment_without_heldout_rows_candidate_requires_split_check | locator_sidecar_missing, forbidden_feature_audit_required, manual_or_algorithmic_source_free_locator_validation_required, predicted_geometry_scorer_must_consume_locator_sidecar_after_audit_passes |
| 10 | mh_072 | uniprot:P0A6P9 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_072_P0A6P9.json | structure_local_ligand_geometry_without_source_text_candidate_requires_validator | locator_sidecar_missing, forbidden_feature_audit_required, manual_or_algorithmic_source_free_locator_validation_required, predicted_geometry_scorer_must_consume_locator_sidecar_after_audit_passes |

## Commands

```bash
mkdir -p artifacts/family_panel_source_free_active_site_locators_current702_20260601
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-family-panel-source-free-active-site-locator-schema
```

## Interpretation

- 10 locator sidecars are planned; 0 are currently ready.
- Materialize the planned locator sidecars with only allowed source-free evidence, rerun the schema audit, then update the predicted-geometry manifest before any packet/readout refresh.
