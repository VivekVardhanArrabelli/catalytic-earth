# Family Panel Source-Free Active-Site Locator Candidate Audit - current702

Run: 2026-06-01T12:56:54Z

Review-only source-free locator candidate audit for the 10 fold-scored family-panel rows. Candidate sidecars are written outside the audited locator directory and are never scoring-ready.

## Status

- source_free_active_site_locator_candidates_staged_review_only
- Target rows: 10
- Candidate sidecars staged: 10
- Rows with >=2 candidate residue locators: 8
- Ready for predicted-geometry scoring: 0
- Rows requiring split-safe template check: 2
- Rows with all candidate sequence positions validated: 6
- Candidate status counts: {'candidate_contacts_blocked_minimum_not_met': 2, 'candidate_contacts_staged_review_required': 8}

## Row Candidates

| rank | row | accession | candidate sidecar | selected ligand | locators | UniProt-validated locators | blockers |
| ---: | --- | --- | --- | --- | ---: | ---: | --- |
| 1 | secondary_probe::cobalamin_radical_rearrangement | uniprot:Q59490 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/secondary_probe_cobalamin_radical_rearrangement_Q59490.json | none | 0 | 0 | candidate_sidecar_not_in_audited_locator_dir, insufficient_candidate_residue_locators, manual_review_required_before_copy_to_audited_dir, no_nonwater_ligand_or_metal_site_detected |
| 2 | secondary_probe::radical_sam_enzyme | uniprot:A0A1M6T2I7 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/secondary_probe_radical_sam_enzyme_A0A1M6T2I7.json | SF4:A:501 | 8 | 8 | candidate_sidecar_not_in_audited_locator_dir, manual_review_required_before_copy_to_audited_dir |
| 3 | external_glycoside_panel | uniprot:Q6NSJ0 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/external_glycoside_panel_Q6NSJ0.json | ACT:B:805 | 8 | 8 | candidate_sidecar_not_in_audited_locator_dir, coordinate_ligand_specificity_review_required, manual_review_required_before_copy_to_audited_dir |
| 4 | mh_073 | uniprot:P01112 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_073_P01112.json | MG:A:168 | 2 | 2 | candidate_sidecar_not_in_audited_locator_dir, manual_review_required_before_copy_to_audited_dir |
| 5 | mh_064 | uniprot:C7C422 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_064_C7C422.json | none | 0 | 0 | candidate_sidecar_not_in_audited_locator_dir, insufficient_candidate_residue_locators, manual_review_required_before_copy_to_audited_dir, no_nonwater_ligand_or_metal_site_detected |
| 6 | mh_065 | uniprot:Q79MP6 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_065_Q79MP6.json | ZN:A:500 | 3 | 0 | candidate_sidecar_not_in_audited_locator_dir, manual_review_required_before_copy_to_audited_dir, uniprot_sequence_position_validation_required |
| 7 | mh_066 | uniprot:P52699 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_066_P52699.json | ZN:A:503 | 3 | 3 | candidate_sidecar_not_in_audited_locator_dir, manual_review_required_before_copy_to_audited_dir |
| 8 | mh_067 | uniprot:P00918 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_067_P00918.json | ZN:A:262 | 3 | 3 | candidate_sidecar_not_in_audited_locator_dir, manual_review_required_before_copy_to_audited_dir, split_safe_train_cal_template_check_required |
| 9 | mh_068 | uniprot:P15289 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_068_P15289.json | MG:A:603 | 4 | 4 | candidate_sidecar_not_in_audited_locator_dir, manual_review_required_before_copy_to_audited_dir, split_safe_train_cal_template_check_required |
| 10 | mh_072 | uniprot:P0A6P9 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_072_P0A6P9.json | MG:C:1429 | 3 | 0 | candidate_sidecar_not_in_audited_locator_dir, manual_review_required_before_copy_to_audited_dir, uniprot_sequence_position_validation_required |

## Commands

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-family-panel-source-free-active-site-locator-candidate-audit
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-family-panel-source-free-active-site-locator-schema
```

## Interpretation

- 8/10 rows now have at least two coordinate-only candidate locators, but none are approved for predicted-geometry scoring.
- Review candidate sidecars for UniProt sequence-position validity and forbidden-feature cleanliness; copy only approved sidecars into the audited locator directory, then rerun the schema audit.
