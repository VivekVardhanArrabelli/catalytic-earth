# Mechanism Feature Row-Specific Bond-Change P0 Extraction Work Package - current702

Run: 2026-06-01T18:37:39Z

No-fit manual extraction work package for the balanced P0 row-specific bond-change pilot seed. It defines row-level required fields and acceptance criteria, but does not extract or materialize source evidence, mutate feature contracts, or fit a model.

## Status

- p0_row_specific_bond_change_extraction_work_package_ready_manual_only
- P0 seed rows: 15
- Manual extraction rows: 15
- Rows with Rhea targets: 11
- Rows requiring Rhea lookup: 4
- Required sidecar fields: 9
- Blocker counts: {'rhea_reaction_mapping_missing': 4, 'structured_bond_change_events_missing': 15}

## Extraction Rows

- m_csa:5 (ser_his_acid_hydrolase): rhea=0, lookup_required=True, status=manual_extraction_not_started
- m_csa:6 (flavin_dehydrogenase_reductase): rhea=1, lookup_required=False, status=manual_extraction_not_started
- m_csa:11 (metal_dependent_hydrolase): rhea=0, lookup_required=True, status=manual_extraction_not_started
- m_csa:15 (metal_dependent_hydrolase): rhea=1, lookup_required=False, status=manual_extraction_not_started
- m_csa:16 (metal_dependent_hydrolase): rhea=1, lookup_required=False, status=manual_extraction_not_started
- m_csa:37 (heme_peroxidase_oxidase): rhea=1, lookup_required=False, status=manual_extraction_not_started
- m_csa:66 (plp_dependent_enzyme): rhea=1, lookup_required=False, status=manual_extraction_not_started
- m_csa:68 (flavin_dehydrogenase_reductase): rhea=1, lookup_required=False, status=manual_extraction_not_started
- m_csa:94 (ser_his_acid_hydrolase): rhea=1, lookup_required=False, status=manual_extraction_not_started
- m_csa:102 (flavin_dehydrogenase_reductase): rhea=1, lookup_required=False, status=manual_extraction_not_started
- m_csa:124 (heme_peroxidase_oxidase): rhea=0, lookup_required=True, status=manual_extraction_not_started
- m_csa:133 (heme_peroxidase_oxidase): rhea=1, lookup_required=False, status=manual_extraction_not_started
- m_csa:147 (plp_dependent_enzyme): rhea=3, lookup_required=False, status=manual_extraction_not_started
- m_csa:169 (ser_his_acid_hydrolase): rhea=0, lookup_required=True, status=manual_extraction_not_started
- m_csa:186 (plp_dependent_enzyme): rhea=1, lookup_required=False, status=manual_extraction_not_started

## Required Fields

- source_record_id
- source_database
- source_record_version_or_date
- row_specific_reaction_participant_mapping
- row_specific_bond_change_events
- active_site_residue_role_support
- source_text_or_database_evidence_span
- extractor_id
- review_status

## Interpretation

- The balanced P0 pilot is ready for manual/source-backed extraction planning, not feature consumption: every row still needs approved row-specific participant mappings and bond-change events.
- Fill these templates from source-backed M-CSA/Rhea/mechanism evidence, run a strict sidecar audit, and only then consider a no-fit feature-contract refresh.
