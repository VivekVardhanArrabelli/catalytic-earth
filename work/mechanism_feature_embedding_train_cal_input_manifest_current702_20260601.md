# Mechanism-Feature Embedding Train/Cal Input Manifest - current702

Run: 2026-06-01T11:51:27Z

Leakage-safe input manifest for a future mechanism-feature embedding pilot. This enumerates in_distribution/train-cal candidate rows and feature sidecar availability only; it does not fit model weights or evaluate heldout rows.

## Status

- train_cal_input_manifest_ready_no_model_fit
- Train/cal candidate rows: 562
- Heldout excluded rows: 140
- Minimal feature bundle ready rows: 524
- Role graph status counts: {'missing_accession_compatible_sequence_positions': 34, 'missing_catalytic_residue_nodes': 1, 'not_m_csa_no_curated_active_site_roles': 3, 'ok': 524}
- Reaction template status counts: {'no_mechanism_fingerprint_oos_or_unlabeled': 378, 'template_available': 184}
- Inorganic completion status: inorganic_cofactor_locus_completion_audit_passed_review_only

## Locus Status Counts

- cobalamin_locus: {'no_cobalamin_context_detected': 544, 'proximal_cobalamin_context_available': 3, 'unsupported_or_missing_geometry': 15}
- iron_sulfur_locus: {'no_iron_sulfur_context_detected': 525, 'proximal_iron_sulfur_context_available': 13, 'structure_wide_iron_sulfur_context_only': 9, 'unsupported_or_missing_geometry': 15}
- metal_ion_locus: {'no_metal_context_detected': 332, 'proximal_metal_context_available': 146, 'structure_wide_metal_context_only': 69, 'unsupported_or_missing_geometry': 15}
- radical_sam_locus: {'no_radical_sam_context_detected': 540, 'proximal_radical_sam_context_available': 5, 'structure_wide_radical_sam_context_only': 2, 'unsupported_or_missing_geometry': 15}

## Interpretation

- 524/562 in_distribution rows have the minimal no-fit feature bundle for an embedding pilot.
- If a model pilot is authorized, split only the in_distribution rows into train/cal folds, fit on train, choose any threshold on calibration only, and evaluate heldout once.
