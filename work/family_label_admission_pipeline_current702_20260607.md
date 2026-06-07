# Family Label Admission Pipeline

Artifact: `v3_family_label_admission_pipeline_current702_20260607`
Status: `family_label_admission_pipeline_ready_review_only`

## Row States

| State | Rows |
| --- | ---: |
| `blocked_coordinate` | 3 |
| `blocked_family_decision` | 6 |
| `blocked_locator` | 2 |
| `countable_candidate` | 0 |
| `oos_hard_negative` | 0 |
| `reject_preserve_signal` | 0 |
| `review_only_evidence` | 11 |

## Admission Table

| Entry | Panel | State | Next action class |
| --- | --- | --- | --- |
| m_csa:750 | cobalamin_and_radical_rearrangement_panel | `review_only_evidence` | preserve_review_only_evidence |
| secondary_probe::radical_sam_enzyme | cobalamin_and_radical_rearrangement_panel | `review_only_evidence` | preserve_review_only_evidence |
| m_csa:131 | flavin_monooxygenase_and_flavin_oxygen_transfer | `review_only_evidence` | preserve_review_only_evidence |
| m_csa:132 | flavin_monooxygenase_and_flavin_oxygen_transfer | `review_only_evidence` | preserve_review_only_evidence |
| m_csa:551 | flavin_monooxygenase_and_flavin_oxygen_transfer | `review_only_evidence` | preserve_review_only_evidence |
| m_csa:267 | lipoamide_or_sulfur_transfer_redox_boundary | `review_only_evidence` | preserve_review_only_evidence |
| m_csa:116 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | `review_only_evidence` | preserve_review_only_evidence |
| mh_073 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | `review_only_evidence` | preserve_review_only_evidence |
| mh_066 | no_reliable_structure_metal_hydrolase_controls | `review_only_evidence` | preserve_review_only_evidence |
| mh_067 | no_reliable_structure_metal_hydrolase_controls | `review_only_evidence` | preserve_review_only_evidence |
| mh_068 | no_reliable_structure_metal_hydrolase_controls | `review_only_evidence` | preserve_review_only_evidence |
| m_csa:973 | flavin_monooxygenase_and_flavin_oxygen_transfer | `blocked_family_decision` | record_expert_family_admission_decision |
| m_csa:30 | glycyl_radical_or_thiamine_radical_lyase_boundary | `blocked_family_decision` | record_expert_family_admission_decision |
| m_csa:31 | glycyl_radical_or_thiamine_radical_lyase_boundary | `blocked_family_decision` | record_expert_family_admission_decision |
| m_csa:448 | lipoamide_or_sulfur_transfer_redox_boundary | `blocked_family_decision` | record_expert_family_admission_decision |
| m_csa:10 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | `blocked_family_decision` | record_expert_family_admission_decision |
| m_csa:191 | thiol_disulfide_oxidoreductase_isomerase_boundary | `blocked_family_decision` | record_expert_family_admission_decision |
| secondary_probe::cobalamin_radical_rearrangement | cobalamin_and_radical_rearrangement_panel | `blocked_locator` | resolve_source_free_locator_policy |
| external_glycoside_panel | near_orphan_glycoside_or_nucleoside_hydrolase_controls | `blocked_locator` | resolve_source_free_locator_policy |
| mh_064 | no_reliable_structure_metal_hydrolase_controls | `blocked_coordinate` | resolve_coordinate_or_mapping |
| mh_065 | no_reliable_structure_metal_hydrolase_controls | `blocked_coordinate` | resolve_coordinate_or_mapping |
| mh_072 | no_reliable_structure_metal_hydrolase_controls | `blocked_coordinate` | resolve_coordinate_or_mapping |

## Preserved Evidence

- Evidence packet context is preserved for 22 rows.
- Source-check provenance is preserved for 11 rows.
- Source-check catalytic/locator detail is preserved for 11 rows.
- Locator provenance is preserved for 5 rows.
- Mechanism text, source prose, labels, IDs, accessions, coordinates, and provenance remain review context only, not predictive feature values.

## Outputs

- Review packet rows: 17
- Import-preview rows: 0
- Reject/OOS-signal rows: 22
- Blocked rows: 11

## Machinery

- `family_panel_countability_gate_preflight`
- `family_panel_import_preview_blocker_gate`
- `family_panel_expert_import_decision_packet`
- `family_panel_evidence_packets`
- `source_check_completion_reconciliation`
- `source_free_locator_human_decision_matrix`
- `accepted_import_preview_blocker_check`
- `label_factory_gate_readiness_blocker_check`

## Next Task

Resolve the accession-equivalence or matching-coordinate locator decision for mh_065 and mh_072 by providing frozen coordinates that map to Q79MP6/P0A6P9 or an explicitly approved remapped locator; then rerun the import-preview blocker gate.

No labels, registries, ontology, mechanism fingerprints, thresholds, production scoring, heldout evaluation, or imports were changed.
