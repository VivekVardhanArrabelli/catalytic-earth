# Family Panel Packet Coverage Audit - current702

Run: 2026-06-01T15:23:54Z

Review-only coverage audit across family-expansion evidence packets after source-backed P0/P1 Foldseek/TM materialization and approved source-free predicted-geometry retrieval joins.

## Status

- coverage_audit_ready_review_only
- Panel packets: 7
- Candidate rows: 22
- Predicted geometry ok rows: 15
- Rows with predicted-structure fold hits: 21
- Packets with geometry gaps: 3

## Panels

| panel | status | rows | geometry ok | fold hits | missing geometry |
| --- | --- | ---: | ---: | ---: | --- |
| glycyl_radical_or_thiamine_radical_lyase_boundary | evidence_packet_ready_review_only | 2 | 2 | 2 | none |
| thiol_disulfide_oxidoreductase_isomerase_boundary | evidence_packet_ready_review_only | 1 | 1 | 1 | none |
| lipoamide_or_sulfur_transfer_redox_boundary | evidence_packet_ready_review_only | 2 | 2 | 2 | none |
| flavin_monooxygenase_and_flavin_oxygen_transfer | evidence_packet_ready_review_only | 4 | 4 | 3 | none |
| cobalamin_and_radical_rearrangement_panel | evidence_packet_ready_with_geometry_gaps | 3 | 2 | 3 | secondary_probe::cobalamin_radical_rearrangement |
| no_reliable_structure_metal_hydrolase_controls | evidence_packet_ready_with_geometry_gaps | 6 | 1 | 6 | mh_064, mh_065, mh_067, mh_068, mh_072 |
| near_orphan_glycoside_or_nucleoside_hydrolase_controls | evidence_packet_ready_with_geometry_gaps | 4 | 3 | 4 | external_glycoside_panel |

## Interpretation

- 15/22 family-panel rows now have predicted-geometry evidence; 21 have predicted-fold hits.
- Source-check newly non-abstained source-free geometry rows, then clear the remaining source-free locator blockers for packet rows still missing geometry.
