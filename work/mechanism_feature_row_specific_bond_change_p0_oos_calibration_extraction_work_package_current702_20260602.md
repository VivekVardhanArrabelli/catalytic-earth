# Mechanism Feature Row-Specific Bond-Change P0 OOS Calibration Extraction Work Package - current702

Run: 2026-06-02T09:49:45Z

No-fit manual extraction work package for the split-safe OOS calibration rows staged by the P0 no-template gap packet. It defines required source-evidence fields only; it does not approve rows or materialize row-specific features.

## Status

- p0_oos_calibration_extraction_work_package_ready_manual_only
- Manual extraction rows: 30
- Calibration rows: 30
- Train rows: 0
- Rows with active-site role template: 30
- Critical violations: 0

## Extraction Rows

| entry | accession | split | residues | status |
| --- | --- | --- | ---: | --- |
| m_csa:2 | P62593 | calibration | 7 | manual_extraction_not_started |
| m_csa:17 | P00491 | calibration | 11 | manual_extraction_not_started |
| m_csa:23 | P13255 | calibration | 5 | manual_extraction_not_started |
| m_csa:25 | P32400 | calibration | 5 | manual_extraction_not_started |
| m_csa:40 | P07378 | calibration | 4 | manual_extraction_not_started |
| m_csa:49 | P00862 | calibration | 7 | manual_extraction_not_started |
| m_csa:59 | P07547 | calibration | 10 | manual_extraction_not_started |
| m_csa:70 | P52045 | calibration | 3 | manual_extraction_not_started |
| m_csa:76 | P26446 | calibration | 3 | manual_extraction_not_started |
| m_csa:78 | P23007 | calibration | 5 | manual_extraction_not_started |
| m_csa:85 | P0A731 | calibration | 7 | manual_extraction_not_started |
| m_csa:101 | P49789 | calibration | 4 | manual_extraction_not_started |
| m_csa:149 | P00488 | calibration | 6 | manual_extraction_not_started |
| m_csa:154 | P49888 | calibration | 3 | manual_extraction_not_started |
| m_csa:194 | P26276 | calibration | 9 | manual_extraction_not_started |
| m_csa:202 | P00969 | calibration | 3 | manual_extraction_not_started |
| m_csa:221 | Q9F4L3 | calibration | 4 | manual_extraction_not_started |
| m_csa:222 | P00883 | calibration | 7 | manual_extraction_not_started |
| m_csa:224 | Q12341 | calibration | 2 | manual_extraction_not_started |
| m_csa:241 | P12256 | calibration | 5 | manual_extraction_not_started |
| m_csa:246 | P06213 | calibration | 4 | manual_extraction_not_started |
| m_csa:253 | P08836 | calibration | 10 | manual_extraction_not_started |
| m_csa:256 | P00327 | calibration | 5 | manual_extraction_not_started |
| m_csa:263 | Q9K499 | calibration | 4 | manual_extraction_not_started |
| m_csa:273 | P08203 | calibration | 5 | manual_extraction_not_started |
| m_csa:287 | P08536 | calibration | 5 | manual_extraction_not_started |
| m_csa:292 | P0A953 | calibration | 6 | manual_extraction_not_started |
| m_csa:312 | Q9WYQ4 | calibration | 4 | manual_extraction_not_started |
| m_csa:317 | P14900 | calibration | 3 | manual_extraction_not_started |
| m_csa:318 | P27000 | calibration | 1 | manual_extraction_not_started |

## Required Fields

- source_record_id
- source_database
- source_record_version_or_date
- row_specific_reaction_participant_mapping
- row_specific_bond_change_events
- active_site_residue_role_support
- source_text_or_database_evidence_span
- extractor_id
- review_status

## Interpretation

- 30 OOS calibration rows now have manual source-evidence extraction templates; none are approved for feature consumption.
- Fill these templates from source-backed M-CSA/Rhea/mechanism evidence, approve only source-spanned calibration rows, then rerun the P0 train/cal feature sidecar and no-template artifact.
