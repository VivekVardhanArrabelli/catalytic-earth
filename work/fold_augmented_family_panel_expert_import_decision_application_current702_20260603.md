# Fold-Augmented Family-Panel Expert Import Decision Application - current702

Run: 2026-06-03T11:08:29Z

Fail-closed application gate for Lever 4 family-panel expert import decisions. It verifies row-context hashes and exposes accepted rows that may enter a separate import-preview artifact. It does not write an import preview, run label-factory gates, edit labels, change registries, or make rows countable.

## Status

- family_panel_expert_import_decision_application_blocked
- Packet stubs: 22
- Decision records: 22
- Reviewed decision records: 0
- Pending decision rows: 22
- Accepted import-preview candidates: 0
- Accepted but still blocked rows: 0
- Critical violations: 0
- Blockers: ['explicit_expert_import_decisions_missing', 'accepted_import_preview_candidate_rows_missing']

## Decision

- Explicit expert decisions recorded: False
- Import preview can run now: False
- Label-factory gate ready: False
- New countable labels authorized: False
- Next gate: If import_preview_can_run_now is true, build a separate family-panel import-preview artifact for the accepted rows and then run the label-factory gate. Otherwise, record missing expert decisions or clear the remaining locator, primary-channel, or family-promotion blockers first.

## Row Decisions

| row | panel | decision | accepted candidate | still blocked | violations |
| --- | --- | --- | ---: | ---: | --- |
| m_csa:750 | cobalamin_and_radical_rearrangement_panel | pending_review | 0 | 0 | none |
| secondary_probe::cobalamin_radical_rearrangement | cobalamin_and_radical_rearrangement_panel | pending_review | 0 | 0 | none |
| secondary_probe::radical_sam_enzyme | cobalamin_and_radical_rearrangement_panel | pending_review | 0 | 0 | none |
| m_csa:131 | flavin_monooxygenase_and_flavin_oxygen_transfer | pending_review | 0 | 0 | none |
| m_csa:132 | flavin_monooxygenase_and_flavin_oxygen_transfer | pending_review | 0 | 0 | none |
| m_csa:551 | flavin_monooxygenase_and_flavin_oxygen_transfer | pending_review | 0 | 0 | none |
| m_csa:973 | flavin_monooxygenase_and_flavin_oxygen_transfer | pending_review | 0 | 0 | none |
| m_csa:30 | glycyl_radical_or_thiamine_radical_lyase_boundary | pending_review | 0 | 0 | none |
| m_csa:31 | glycyl_radical_or_thiamine_radical_lyase_boundary | pending_review | 0 | 0 | none |
| m_csa:267 | lipoamide_or_sulfur_transfer_redox_boundary | pending_review | 0 | 0 | none |
| m_csa:448 | lipoamide_or_sulfur_transfer_redox_boundary | pending_review | 0 | 0 | none |
| external_glycoside_panel | near_orphan_glycoside_or_nucleoside_hydrolase_controls | pending_review | 0 | 0 | none |
| m_csa:10 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | pending_review | 0 | 0 | none |
| m_csa:116 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | pending_review | 0 | 0 | none |
| mh_073 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | pending_review | 0 | 0 | none |
| mh_064 | no_reliable_structure_metal_hydrolase_controls | pending_review | 0 | 0 | none |
| mh_065 | no_reliable_structure_metal_hydrolase_controls | pending_review | 0 | 0 | none |
| mh_066 | no_reliable_structure_metal_hydrolase_controls | pending_review | 0 | 0 | none |
| mh_067 | no_reliable_structure_metal_hydrolase_controls | pending_review | 0 | 0 | none |
| mh_068 | no_reliable_structure_metal_hydrolase_controls | pending_review | 0 | 0 | none |
| mh_072 | no_reliable_structure_metal_hydrolase_controls | pending_review | 0 | 0 | none |
| m_csa:191 | thiol_disulfide_oxidoreductase_isomerase_boundary | pending_review | 0 | 0 | none |

## Interpretation

- 0 accepted family-panel rows are ready for a separate import-preview artifact.
- The gate keeps current family-panel rows fail-closed unless an explicit accepted decision is present with the unchanged row-context hash and no remaining source-free locator, primary channel, or family-promotion blocker.
- Review and apply expert decisions with hashes unchanged; then build a separate import-preview artifact only for accepted rows marked accepted_import_preview_candidate.
