# Family Panel Source-Free Active-Site Locator Candidate Integrity Audit - current702

Run: 2026-06-01T13:16:42Z

Integrity audit for review-only source-free locator candidate sidecars. This checks file/payload/guardrail consistency and does not copy candidates into the audited locator directory.

## Status

- source_free_active_site_locator_candidate_integrity_passed_review_only
- Candidate sidecars expected: 10
- Candidate sidecar files present: 10
- Integrity-passed sidecars: 10
- Integrity-blocked sidecars: 0
- Ready for predicted-geometry scoring: 0
- Critical counts: {}

## Candidate Sidecars

| row | accession | candidate sidecar | status | locators | validated | violations |
| --- | --- | --- | --- | ---: | ---: | --- |
| external_glycoside_panel | uniprot:Q6NSJ0 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/external_glycoside_panel_Q6NSJ0.json | passed | 8 | 8 |  |
| mh_064 | uniprot:C7C422 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_064_C7C422.json | passed | 0 | 0 |  |
| mh_065 | uniprot:Q79MP6 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_065_Q79MP6.json | passed | 3 | 0 |  |
| mh_066 | uniprot:P52699 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_066_P52699.json | passed | 3 | 3 |  |
| mh_067 | uniprot:P00918 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_067_P00918.json | passed | 3 | 3 |  |
| mh_068 | uniprot:P15289 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_068_P15289.json | passed | 4 | 4 |  |
| mh_072 | uniprot:P0A6P9 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_072_P0A6P9.json | passed | 3 | 0 |  |
| mh_073 | uniprot:P01112 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/mh_073_P01112.json | passed | 2 | 2 |  |
| secondary_probe::cobalamin_radical_rearrangement | uniprot:Q59490 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/secondary_probe_cobalamin_radical_rearrangement_Q59490.json | passed | 0 | 0 |  |
| secondary_probe::radical_sam_enzyme | uniprot:A0A1M6T2I7 | artifacts/family_panel_source_free_active_site_locator_candidates_current702_20260601/secondary_probe_radical_sam_enzyme_A0A1M6T2I7.json | passed | 8 | 8 |  |

## Commands

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-family-panel-source-free-active-site-locator-candidate-integrity
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-family-panel-source-free-active-site-locator-schema
```

## Interpretation

- 10/10 candidate sidecars pass review-only integrity checks; 0 are scoring-ready.
- Use the review queue for manual scientific review; only after approval should any rewritten locator sidecar be copied into the audited locator directory and schema-audited.
