# Family Panel Packet Coverage Audit - current702

Run: 2026-06-01T08:07:00Z

Review-only coverage audit across all family-set expansion evidence packets generated for current702.

## Status

- coverage_audit_ready_review_only
- Panel packets: 7
- Candidate rows: 22
- Predicted geometry ok rows: 10
- Rows with predicted-structure fold hits: 9
- Packets ready without geometry gaps: 3
- Packets with geometry gaps: 4

## Panel Coverage

| Panel | rows | geometry ok | predicted-fold hits | missing geometry |
| --- | ---: | ---: | ---: | --- |
| glycyl_radical_or_thiamine_radical_lyase_boundary | 2 | 2 | 2 |  |
| thiol_disulfide_oxidoreductase_isomerase_boundary | 1 | 1 | 1 |  |
| lipoamide_or_sulfur_transfer_redox_boundary | 2 | 2 | 2 |  |
| flavin_monooxygenase_and_flavin_oxygen_transfer | 4 | 3 | 2 | m_csa:132 |
| cobalamin_and_radical_rearrangement_panel | 3 | 1 | 1 | secondary_probe::cobalamin_radical_rearrangement, secondary_probe::radical_sam_enzyme |
| no_reliable_structure_metal_hydrolase_controls | 6 | 0 | 0 | mh_064, mh_065, mh_066, mh_067, mh_068, mh_072 |
| near_orphan_glycoside_or_nucleoside_hydrolase_controls | 4 | 1 | 1 | m_csa:116, mh_073, external_glycoside_panel |

## Interpretation

- The review-only family expansion evidence set is complete for the seven proposed panels.
- Three panels are fully populated with current predicted-geometry evidence; four are materialization/source-evidence queues.
- Prioritize materialization for FMO `m_csa:132`, secondary radical/cobalamin probes, no-reliable-structure metal hydrolase controls, and near-orphan glycoside/nucleoside gaps before any family expansion gate.
