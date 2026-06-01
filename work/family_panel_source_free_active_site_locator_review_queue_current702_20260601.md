# Family Panel Source-Free Active-Site Locator Review Queue - current702

Run: 2026-06-01T13:00:07Z

Review queue for the source-free active-site locator candidates. This ranks candidate sidecars for manual validation but does not copy anything into the audited locator directory.

## Status

- source_free_active_site_locator_review_queue_ready_review_only
- Queue rows: 10
- Ready for manual forbidden-feature review: 3
- Review class counts: {'blocked_needs_new_coordinate_or_nonlabel_locator': 2, 'needs_ligand_specificity_review': 1, 'needs_split_safe_template_check': 2, 'needs_uniprot_position_validation': 2, 'ready_for_manual_forbidden_feature_review': 3}

## Queue

| priority | row | accession | class | locators | validated | next action |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 1 | mh_066 | uniprot:P52699 | ready_for_manual_forbidden_feature_review | 3 | 3 | Manual review may start; copy to the audited locator directory only after forbidden-feature and scientific checks pass. |
| 1 | mh_073 | uniprot:P01112 | ready_for_manual_forbidden_feature_review | 2 | 2 | Manual review may start; copy to the audited locator directory only after forbidden-feature and scientific checks pass. |
| 1 | secondary_probe::radical_sam_enzyme | uniprot:A0A1M6T2I7 | ready_for_manual_forbidden_feature_review | 8 | 8 | Manual review may start; copy to the audited locator directory only after forbidden-feature and scientific checks pass. |
| 2 | external_glycoside_panel | uniprot:Q6NSJ0 | needs_ligand_specificity_review | 8 | 8 | Review whether the selected coordinate ligand is biologically relevant before any audited sidecar copy. |
| 3 | mh_067 | uniprot:P00918 | needs_split_safe_template_check | 3 | 3 | Verify same-accession train/cal template use is split-safe before any audited sidecar copy. |
| 3 | mh_068 | uniprot:P15289 | needs_split_safe_template_check | 4 | 4 | Verify same-accession train/cal template use is split-safe before any audited sidecar copy. |
| 4 | mh_065 | uniprot:Q79MP6 | needs_uniprot_position_validation | 3 | 0 | Validate candidate sequence positions against UniProt mapping before any audited sidecar copy. |
| 4 | mh_072 | uniprot:P0A6P9 | needs_uniprot_position_validation | 3 | 0 | Validate candidate sequence positions against UniProt mapping before any audited sidecar copy. |
| 5 | mh_064 | uniprot:C7C422 | blocked_needs_new_coordinate_or_nonlabel_locator | 0 | 0 | Find an alternate source-free locator path; current selected coordinate has fewer than two candidate locators. |
| 5 | secondary_probe::cobalamin_radical_rearrangement | uniprot:Q59490 | blocked_needs_new_coordinate_or_nonlabel_locator | 0 | 0 | Find an alternate source-free locator path; current selected coordinate has fewer than two candidate locators. |

## Commands

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-family-panel-source-free-active-site-locator-review-queue
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-family-panel-source-free-active-site-locator-schema
```

## Interpretation

- 3 candidate rows are ready for manual forbidden-feature review; no row is scoring-ready.
- Start with priority-1 rows, review the candidate sidecar contents, and copy only approved sidecars into the audited locator directory.
