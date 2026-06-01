# Mechanism-Feature Cobalamin Locus Sidecar - current702

Status: `cobalamin_locus_sidecar_ready_review_only`

## Counts

- rows: 702
- status_counts: {'no_cobalamin_context_detected': 678, 'proximal_cobalamin_context_available': 4, 'unsupported_or_missing_geometry': 20}
- proximal_context_rows: 4
- structure_wide_only_rows: 0
- unsupported_or_missing_geometry_rows: 20
- top_proximal_cobalamin_codes: {'B12': 2, 'COB': 2, 'DCA': 1}
- ready_for_label_import_rows: 0
- predictive_use_allowed_rows: 0

## Interpretation

- The cobalamin locus is now materialized as a review-only current702 row sidecar with proximal versus structure-wide-only semantics.
- Repeat the pattern for radical_sam_locus and iron_sulfur_locus, preserving SAM/Fe-S copresence as a separate status.
