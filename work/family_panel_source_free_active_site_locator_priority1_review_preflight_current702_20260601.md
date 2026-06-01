# Family Panel Source-Free Active-Site Locator Priority-1 Review Preflight - current702

Run: 2026-06-01T14:01:08Z

Review-only preflight for the priority-1 source-free active-site locator candidates. This dry-runs schema compatibility, guardrails, and coordinate-contact plausibility without copying sidecars into the audited locator directory.

## Status

- source_free_active_site_locator_priority1_preflight_passed_pending_human_approval
- Priority-1 rows: 3
- Preflight-passed pending human approval: 3
- Schema dry-run passed rows: 3
- Guardrail preflight passed rows: 3
- Coordinate-contact preflight supported rows: 3
- Rows with preflight warnings: 1
- Copy to audited locator dir allowed now: 0
- Ready for predicted-geometry scoring: 0

## Priority-1 Rows

| row | accession | selected ligand | locators | status | warnings | planned audited path |
| --- | --- | --- | ---: | --- | --- | --- |
| mh_066 | uniprot:P52699 | ZN:A:503 | 3 | preflight_passed_pending_human_approval |  | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_066_P52699.json |
| mh_073 | uniprot:P01112 | MG:A:168 | 2 | preflight_passed_pending_human_approval | minimum_two_locator_floor_only | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_073_P01112.json |
| secondary_probe::radical_sam_enzyme | uniprot:A0A1M6T2I7 | SF4:A:501 | 8 | preflight_passed_pending_human_approval |  | artifacts/family_panel_source_free_active_site_locators_current702_20260601/secondary_probe_radical_sam_enzyme_A0A1M6T2I7.json |

## Commands

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-family-panel-source-free-active-site-locator-priority1-review-preflight
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-family-panel-source-free-active-site-locator-schema
```

## Interpretation

- 3/3 priority-1 candidate rows pass schema, guardrail, and coordinate-contact preflight, but 0 are copy-authorized.
- Human review should inspect the three preflight-passed rows and only then rewrite/copy approved locator sidecars into the audited directory before rerunning the schema audit.
