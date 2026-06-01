# Family Panel Source-Free Locator Remaining Blocker Action Queue - current702

Run: 2026-06-01T15:58:19Z

Review-only action queue for the seven family-panel rows still blocked on approved source-free active-site locator sidecars after the three source-free geometry source checks.

## Status

- source_free_locator_remaining_blocker_action_queue_ready_review_only
- Blocked rows: 7
- Action classes: {'alternate_coordinate_fetch_requires_manual_approval': 1, 'ligand_specificity_review_required': 1, 'new_nonlabel_locator_strategy_required': 1, 'split_safe_template_check_required': 2, 'uniprot_position_validation_required': 2}

## Queue

| rank | row | accession | review class | candidate locators | action class | next action |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | secondary_probe::cobalamin_radical_rearrangement | uniprot:Q59490 | blocked_needs_new_coordinate_or_nonlabel_locator | 0 | new_nonlabel_locator_strategy_required | No selected-coordinate non-water ligand or metal site is available and no frozen alternate PDB exists; design a nonlabel locator strategy or request explicit alternate-source authorization. |
| 3 | external_glycoside_panel | uniprot:Q6NSJ0 | needs_ligand_specificity_review | 8 | ligand_specificity_review_required | Review whether the selected coordinate ligand is scientifically acceptable for source-free active-site localization; do not copy acetate-derived locators until approved. |
| 5 | mh_064 | uniprot:C7C422 | blocked_needs_new_coordinate_or_nonlabel_locator | 0 | alternate_coordinate_fetch_requires_manual_approval | If approved, fetch the five frozen alternate PDB coordinates, rerun coordinate-only candidate extraction, then repeat integrity/schema audit before any locator copy. |
| 6 | mh_065 | uniprot:Q79MP6 | needs_uniprot_position_validation | 3 | uniprot_position_validation_required | Validate candidate residue sequence positions against structure-to-UniProt mapping, then rerun candidate integrity and schema audit before scoring. |
| 8 | mh_067 | uniprot:P00918 | needs_split_safe_template_check | 3 | split_safe_template_check_required | Run a split-safe same-accession train/cal template check and approve only residue locators that do not leak heldout or label information. |
| 9 | mh_068 | uniprot:P15289 | needs_split_safe_template_check | 4 | split_safe_template_check_required | Run a split-safe same-accession train/cal template check and approve only residue locators that do not leak heldout or label information. |
| 10 | mh_072 | uniprot:P0A6P9 | needs_uniprot_position_validation | 3 | uniprot_position_validation_required | Validate candidate residue sequence positions against structure-to-UniProt mapping, then rerun candidate integrity and schema audit before scoring. |

## Guardrails

- Review-only queue. No locator sidecars were copied, no coordinates fetched, no predicted geometry scored, and no labels/imports/thresholds changed.

## Interpretation

- 7 rows remain blocked on approved source-free locator sidecars; all have source-backed fold scores and AFDB coordinate hashes, but none is scoring-ready.
- Start with the least ambiguous blocker class: validate UniProt positions for mh_065 and mh_072, then run split-safe template checks for mh_067/mh_068, ligand-specificity review for external_glycoside_panel, and manual policy decisions for mh_064/Q59490.
