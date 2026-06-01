# Family Panel Packet Coverage Audit - current702

Run: 2026-06-01T11:05:32Z

Review-only coverage audit across family-expansion evidence packets after source-backed P0/P1 Foldseek/TM materialization.

## Status

- coverage_audit_ready_review_only
- Panel packets: 7
- Candidate rows: 22
- Predicted geometry ok rows: 12
- Rows with predicted-structure fold hits: 21
- Packets with geometry gaps: 3

## Panels

| panel | status | rows | geometry ok | fold hits | missing geometry |
| --- | --- | ---: | ---: | ---: | --- |
| glycyl_radical_or_thiamine_radical_lyase_boundary | evidence_packet_ready_review_only | 2 | 2 | 2 | none |
| thiol_disulfide_oxidoreductase_isomerase_boundary | evidence_packet_ready_review_only | 1 | 1 | 1 | none |
| lipoamide_or_sulfur_transfer_redox_boundary | evidence_packet_ready_review_only | 2 | 2 | 2 | none |
| flavin_monooxygenase_and_flavin_oxygen_transfer | evidence_packet_ready_review_only | 4 | 4 | 3 | none |
| cobalamin_and_radical_rearrangement_panel | evidence_packet_ready_with_geometry_gaps | 3 | 1 | 3 | secondary_probe::cobalamin_radical_rearrangement, secondary_probe::radical_sam_enzyme |
| no_reliable_structure_metal_hydrolase_controls | evidence_packet_ready_with_geometry_gaps | 6 | 0 | 6 | mh_064, mh_065, mh_066, mh_067, mh_068, mh_072 |
| near_orphan_glycoside_or_nucleoside_hydrolase_controls | evidence_packet_ready_with_geometry_gaps | 4 | 2 | 4 | mh_073, external_glycoside_panel |

## Interpretation

- 12/22 family-panel rows now have predicted-geometry evidence; 21 have predicted-fold hits.
- Materialize source-free predicted-geometry sidecars for the 10 source-backed fold-scored rows, starting with Q59490, A0A1M6T2I7, and Q6NSJ0.
