# Mechanism-Feature Iron Sulfur Locus Sidecar - current702

Status: `iron_sulfur_locus_sidecar_ready_review_only`

## Counts

- rows: 702
- status_counts: {'no_iron_sulfur_context_detected': 654, 'proximal_iron_sulfur_context_available': 17, 'structure_wide_iron_sulfur_context_only': 11, 'unsupported_or_missing_geometry': 20}
- proximal_context_rows: 17
- structure_wide_only_rows: 11
- unsupported_or_missing_geometry_rows: 20
- sam_fe_s_copresence_counts: {'iron_sulfur_without_copresent_partner': 27, 'no_context_detected': 674, 'proximal_sam_and_fe_s_context': 1}
- ready_for_label_import_rows: 0
- predictive_use_allowed_rows: 0

## Interpretation

- The iron_sulfur locus is now materialized as a review-only current702 row sidecar with proximal, structure-wide-only, and SAM/Fe-S copresence semantics.
- Use these sidecars only under future train/cal split filtering; do not treat them as labels or import evidence.
