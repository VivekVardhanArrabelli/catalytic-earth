# Fold-Augmented Blocker Human Decision Application - current702

Run: 2026-06-03T00:11:35Z

Human decision application for the five Lever 3 production blocker rows. This records approval/policy decisions and authorizes the next materialization steps; it does not edit labels, registries, ontologies, imports, thresholds, model weights, or heldout tuning.

## Status

- fold_augmented_blocker_human_decision_application_ready_materialization_pending
- Approved source-feature sidecars: 3
- P23007 replacement authorized now: 1
- P10746 keep-fold-only policy rows: 1
- Human/policy decision blockers remaining: 0

## Sidecar Decisions

| row | accession | decision | features |
| --- | --- | --- | ---: |
| m_csa:531 | P31572 | approve_source_feature_sidecar | 3 |
| uniprot:P78549 | P78549 | approve_source_feature_sidecar | 6 |
| uniprot:Q3LXA3 | Q3LXA3 | approve_source_feature_sidecar | 9 |

## P23007

- Selected alternate accession: P00889
- Decision: authorize_ortholog_surrogate_replacement
- Note: Use P00889 pig heart citrate synthase as the ortholog surrogate for P23007. The four mammalian citrate synthase candidates are interchangeable on recorded fields; P00889 is the canonical, structurally characterized choice. Record as an ortholog surrogate, not as P23007 itself.

## P10746

- Decision: keep_fold_only_no_non_residue_sidecar
- Note: Keep P10746 fold-only. No source-feature rows or curated residue nodes exist, and mechanism text is forbidden as a predictive anchor. Do not fabricate a non-residue sidecar.

## Next Action

- Materialize the approved source-feature sidecars, fetch the P00889 AFDB coordinate as an ortholog surrogate, rerun the combined geometry/fold channel at the fixed threshold, and keep P10746 fold-only with the policy caveat disclosed.
