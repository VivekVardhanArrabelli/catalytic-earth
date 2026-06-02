# Family Panel Source-Free Predicted-Geometry Source-Check Preflight - current702

Run: 2026-06-02T19:15:47Z

Review-only source-check preflight for the family-panel rows that became non-abstained after approved source-free predicted-geometry scoring. This packages local frozen evidence and blockers; it does not adjudicate family membership.

## Status

- source_free_predicted_geometry_source_check_preflight_ready_review_only
- Preflight rows: 5
- Geometry/fold agreement rows: 3
- Geometry/fold disagreement rows: 2

## Rows

| rank | row | name | geometry top1 | fold fingerprint | combined mean | decision | risk flags |
| ---: | --- | --- | --- | --- | ---: | --- | --- |
| 1 | mh_068 | Arylsulfatase A | metal_dependent_hydrolase | metal_dependent_hydrolase | 0.6903 | hold_review_only_pending_source_check | external_no_decision_review_only, external_panel_row_not_countable, geometry_fold_fingerprint_agreement_needs_duplicate_screen, label_import_not_authorized, source_backed_sidecar_review_context_only, source_check_required_before_family_decision |
| 2 | mh_067 | Carbonic anhydrase 2 | metal_dependent_hydrolase | metal_dependent_hydrolase | 0.6897 | hold_review_only_pending_source_check | external_no_decision_review_only, external_panel_row_not_countable, geometry_fold_fingerprint_agreement_needs_duplicate_screen, label_import_not_authorized, source_backed_sidecar_review_context_only, source_check_required_before_family_decision |
| 3 | mh_066 | Metallo-beta-lactamase IMP-1 | metal_dependent_hydrolase | metal_dependent_hydrolase | 0.6633 | hold_review_only_pending_source_check | external_no_decision_review_only, external_panel_row_not_countable, geometry_fold_fingerprint_agreement_needs_duplicate_screen, label_import_not_authorized, source_backed_sidecar_review_context_only, source_check_required_before_family_decision |
| 9 | mh_073 | GTPase HRas | ser_his_acid_hydrolase | metal_dependent_hydrolase | 0.4878 | hold_review_only_pending_source_check | external_no_decision_review_only, external_panel_row_not_countable, geometry_fold_fingerprint_disagreement, label_import_not_authorized, source_backed_sidecar_review_context_only, source_check_required_before_family_decision |
| 10 | secondary_probe::radical_sam_enzyme | Radical SAM cyclopropyl synthase TigE (EC 4.1.-.-) (Ribosomally synthesized and post-translationally modified peptide-modifying enzyme TigE) (RiPP-modifying enzyme TigE) (TigB maturase) | metal_dependent_hydrolase | plp_dependent_enzyme | 0.4833 | hold_review_only_pending_source_check | geometry_fold_fingerprint_disagreement, label_import_not_authorized, source_backed_sidecar_review_context_only, source_check_required_before_family_decision |

## Interpretation

- 5 newly scored source-free rows are queued for review-only source checks; none is import-ready.
- Start with `mh_066` because it has the largest positive margin, then source-check `mh_073` and `secondary_probe::radical_sam_enzyme` for mechanism locus and duplicate/leakage status.

## Guardrails

- Review-only preflight. No labels, registries, ontologies, imports, thresholds, training data, source fetching, or production scoring changed.
