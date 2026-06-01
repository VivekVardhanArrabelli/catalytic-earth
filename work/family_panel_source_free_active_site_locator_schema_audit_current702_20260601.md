# Family Panel Source-Free Active-Site Locator Schema Audit - current702

Run: 2026-06-01T14:24:29Z

Validation audit for source-free active-site locator sidecars. This checks schema compliance only; it does not score predicted geometry or alter family-panel labels/readouts.

## Status

- source_free_active_site_locator_schema_audit_blocked_missing_sidecars
- Target rows: 10
- Locator sidecars present: 3
- Locator sidecars missing: 7
- Locator sidecars schema-passed: 3
- Ready for predicted geometry scoring: 3
- Critical counts: {'locator_sidecar_missing': 7}

## Row Audits

| row | sidecar | status | violations |
| --- | --- | --- | --- |
| secondary_probe::cobalamin_radical_rearrangement | artifacts/family_panel_source_free_active_site_locators_current702_20260601/secondary_probe_cobalamin_radical_rearrangement_Q59490.json | missing | locator_sidecar_missing |
| secondary_probe::radical_sam_enzyme | artifacts/family_panel_source_free_active_site_locators_current702_20260601/secondary_probe_radical_sam_enzyme_A0A1M6T2I7.json | passed |  |
| external_glycoside_panel | artifacts/family_panel_source_free_active_site_locators_current702_20260601/external_glycoside_panel_Q6NSJ0.json | missing | locator_sidecar_missing |
| mh_073 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_073_P01112.json | passed |  |
| mh_064 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_064_C7C422.json | missing | locator_sidecar_missing |
| mh_065 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_065_Q79MP6.json | missing | locator_sidecar_missing |
| mh_066 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_066_P52699.json | passed |  |
| mh_067 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_067_P00918.json | missing | locator_sidecar_missing |
| mh_068 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_068_P15289.json | missing | locator_sidecar_missing |
| mh_072 | artifacts/family_panel_source_free_active_site_locators_current702_20260601/mh_072_P0A6P9.json | missing | locator_sidecar_missing |

## Interpretation

- 3/10 locator sidecars are ready for predicted-geometry scoring.
- Materialize locator sidecars under the audited directory, rerun this audit, then rerun the predicted-geometry sidecar manifest before refreshing family-panel packets/readout.
