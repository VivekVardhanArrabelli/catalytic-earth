# Source-Free Locator Copy Decision: mh_067/mh_068 - current702

Run: 2026-06-02T19:11:47Z

Explicit review-only decision for the highest-priority source-free locator class: copy or reject the split-safe mh_067/mh_068 candidate locators into the audited locator directory before any source-free predicted-geometry scoring.

## Status

- source_free_locator_copy_decision_mh067_mh068_approved_review_only
- Decision class: human_locator_copy_approval_after_split_safe_pass
- Operator decision: approve
- Target rows: 2
- Approved locator-copy rows: 2
- Rejected locator-copy rows: 0
- Blocked preflight rows: 0
- Ready for predicted-geometry scoring after copy: 2
- Predicted-model sequence-position repairs: 3

## Row Decisions

| row | candidate | approved sidecar | decision | violations | locators | repairs |
| --- | --- | --- | --- | --- | ---: | ---: |
| mh_067 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_067_P00918.json | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_067_P00918.json | approved_for_audited_locator_copy_review_only |  | 3 | 3 |
| mh_068 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_068_P15289.json | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_068_P15289.json | approved_for_audited_locator_copy_review_only |  | 4 | 0 |

## Guardrails

- Review-only locator-copy decision.
- No labels, registries, ontologies, imports, thresholds, training data, source fetches, coordinate downloads, or model weights changed.
- Predicted-geometry scoring is a downstream review-only step and is not performed by this decision artifact.

## Interpretation

- 2/2 mh_067/mh_068 candidate locators are approved for audited review-only copy.
- Rerun the locator schema audit, then the source-free predicted-geometry manifest/retrieval. Keep the rows review-only and outside import, training, threshold, or label-factory use.
