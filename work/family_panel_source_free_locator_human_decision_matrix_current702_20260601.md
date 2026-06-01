# Source-Free Locator Human Decision Matrix - current702

Run: 2026-06-01T17:16:51Z

Compact decision matrix for the seven source-free locator blockers after automation discovery completed. This summarizes existing blocker artifacts only and authorizes no locator copy, coordinate fetch, or predicted-geometry scoring.

## Status

- source_free_locator_human_decision_matrix_ready_review_only
- Blocked rows tracked: 7
- Decision classes: 5
- Ready for predicted-geometry scoring: 0

## Decision Classes

| priority | class | rows | decision needed |
| ---: | --- | --- | --- |
| 1 | human_locator_copy_approval_after_split_safe_pass | mh_067, mh_068 | Approve or reject copying the vetted mh_067/mh_068 candidate locators into the audited locator directory. |
| 2 | accession_equivalence_or_matching_coordinate_required | mh_065, mh_072 | Approve representative-accession equivalence for mh_065/mh_072 or provide matching frozen coordinates. |
| 3 | ligand_specificity_validator_or_substrate_coordinate_required | external_glycoside_panel | Define a glycoside/NAG specificity validator for 7QQF or approve a substrate-complex coordinate. |
| 4 | alternate_coordinate_fetch_approval_required | mh_064 | Approve or reject fetching mh_064 frozen alternate coordinates 3RKJ/3RKK/3SBL/3SFP/3SPU. |
| 5 | nonlabel_locator_strategy_or_alternate_source_required | secondary_probe::cobalamin_radical_rearrangement | Choose a nonlabel locator strategy for Q59490 or authorize a frozen alternate source row/coordinate. |

## Interpretation

- All seven source-free locator blockers are now policy or human-review decisions, not automation-discovery tasks.
- Approve or reject mh_067/mh_068 locator copy, because their split-safe template check already passed and no coordinate fetch is needed.
- Pick exactly one decision class, record the approval/rejection, then rerun the relevant locator schema or candidate audit before any scoring.
