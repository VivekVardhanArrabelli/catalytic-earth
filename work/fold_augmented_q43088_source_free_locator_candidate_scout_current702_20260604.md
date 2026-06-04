# Fold-Augmented Q43088 Source-Free Locator Candidate Scout - current702

Run: 2026-06-04T09:22:59Z

Review-only Q43088 locator candidate scout. It uses the local AFDB-v6 predicted structure and the single known train/cal source-free locator anchor to list nearby residue positions for future review. It approves no locators, writes no sidecar, scores no row, and does not change threshold 0.44155.

## Status

- fold_augmented_q43088_source_free_locator_candidate_scout_pending_review_no_approval
- Anchor locators: 1
- Candidate locator rows: 12
- Candidate locators approved now: 0
- Additional approved locator positions needed: 2
- Blockers: ['q43088_candidate_locators_pending_review', 'q43088_two_additional_source_free_locator_positions_not_approved', 'fixed_threshold_audit_not_ready_to_rerun']

## Anchor Locators

| position | residue | mean pLDDT | roles |
| ---: | --- | ---: | --- |
| 287 | TYR | 95.19 | activator, proton_acceptor, proton_donor |

## Candidate Locators

| rank | position | residue | distance to anchor CA (A) | mean pLDDT | status |
| ---: | ---: | --- | ---: | ---: | --- |
| 1 | 288 | ASP | 3.824 | 93.69 | pending_review |
| 2 | 286 | GLN | 3.84 | 96.0 | pending_review |
| 3 | 243 | HIS | 5.918 | 97.12 | pending_review |
| 4 | 285 | ILE | 6.267 | 96.94 | pending_review |
| 5 | 289 | LEU | 7.069 | 94.56 | pending_review |
| 6 | 250 | GLU | 7.177 | 80.44 | pending_review |
| 7 | 244 | SER | 8.154 | 96.44 | pending_review |
| 8 | 242 | ASN | 8.316 | 97.94 | pending_review |
| 9 | 291 | LYS | 8.699 | 96.88 | pending_review |
| 10 | 224 | PHE | 9.0 | 93.44 | pending_review |
| 11 | 296 | LEU | 9.004 | 98.44 | pending_review |
| 12 | 247 | VAL | 9.143 | 94.12 | pending_review |

## Decision

- Q43088 ready for rescore now: False
- Candidate scout clears locator contract: False
- Fixed-threshold audit ready to rerun now: False
- Apply or change threshold now: False
- Next gate: Review at least two Q43088 candidate locator positions and explicitly approve or reject them under the source-free locator contract. Do not rescore Q43088 until two additional positions or an equivalent geometry sidecar are approved.

## Interpretation

- Q43088 now has concrete source-free locator candidates for review, but zero additional locators are approved. The row therefore remains blocked for combined-channel rescore.
- Have a reviewer accept or reject at least two candidate positions, or supply an equivalent approved geometry sidecar; then regenerate the Q43088 contract and rescore only after the four coordinate-source blockers are also cleared.
