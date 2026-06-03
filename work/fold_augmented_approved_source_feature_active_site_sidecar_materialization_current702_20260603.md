# Fold-Augmented Approved Source-Feature Active-Site Sidecar Materialization - current702

Run: 2026-06-03T00:26:46Z

Approved source-feature active-site sidecar materialization surface for the three Lever 3 coordinate-available production blockers. This writes the approved sidecar surface for the next fixed-threshold combined geometry/fold rerun, but does not fetch coordinates, rerun Foldseek/TM, tune thresholds, or close deployment.

## Status

- fold_augmented_approved_source_feature_active_site_sidecar_materialization_ready_rerun_pending
- Materialized sidecar rows: 3
- Source-feature support rows: 18
- Ready for predicted-geometry scoring: 3
- P23007 coordinate fetch authorized now: 1
- P23007 coordinate fetched now: 0

## Materialized Rows

| row | accession | features | review status | rerun required |
| --- | --- | ---: | --- | --- |
| m_csa:531 | P31572 | 3 | approved_for_fixed_threshold_rerun | True |
| uniprot:P78549 | P78549 | 6 | approved_for_fixed_threshold_rerun | True |
| uniprot:Q3LXA3 | Q3LXA3 | 9 | approved_for_fixed_threshold_rerun | True |

## Guardrails

- Approved sidecar surface written for rerun input; no coordinate was fetched.
- No Foldseek/TM or combined-channel rerun was performed.
- No threshold, label, registry, ontology, import, split, model-weight, or heldout-training surface changed.

## Next Action

- Fetch the P00889 AFDB coordinate as the authorized ortholog surrogate, rerun the combined geometry/fold channel at the fixed threshold with these approved sidecars, and disclose the P10746 fold-only exception.
