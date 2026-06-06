# Fold-Augmented Q43088 Locator Review Priority Packet - current702

Run: 2026-06-04T10:28:45Z

Review-priority packet for the remaining Q43088 Lever 3 locator/geometry blocker. It uses only source-free predicted-structure proximity, residue code, and pLDDT from the prior candidate scout to narrow manual adjudication. It approves no locator, writes no sidecar, scores no row, and does not change threshold 0.44155.

## Status

- fold_augmented_q43088_locator_review_priority_packet_ready_no_approvals
- Anchor locator rows: 1
- Candidate locator rows: 12
- Priority candidate rows: 4
- Minimum additional locator positions needed: 2
- Locator positions approved now: 0
- Blockers: ['q43088_priority_candidates_pending_human_or_policy_review', 'q43088_two_additional_source_free_locator_positions_not_approved', 'fixed_threshold_audit_not_ready_to_rerun']

## Priority Candidate Rows

| rank | position | residue | distance to anchor CA (A) | mean pLDDT | priority score | review flags |
| ---: | ---: | --- | ---: | ---: | ---: | --- |
| 1 | 288 | ASP | 3.824 | 93.69 | 12.113 | within_6a_of_anchor_ca, within_8a_of_anchor_ca, polar_or_charged_residue_code, charged_residue_code, mean_plddt_at_least_80 |
| 2 | 286 | GLN | 3.84 | 96.0 | 11.12 | within_6a_of_anchor_ca, within_8a_of_anchor_ca, polar_or_charged_residue_code, mean_plddt_at_least_80 |
| 3 | 243 | HIS | 5.918 | 97.12 | 10.053 | within_6a_of_anchor_ca, within_8a_of_anchor_ca, polar_or_charged_residue_code, charged_residue_code, mean_plddt_at_least_80 |
| 4 | 250 | GLU | 7.177 | 80.44 | 7.627 | within_8a_of_anchor_ca, polar_or_charged_residue_code, charged_residue_code, mean_plddt_at_least_80 |

## Review Rule

- Recommended review order: 288, 286, 243, 250
- Pass condition: A reviewer explicitly approves at least two additional source-free locator positions, or approves an equivalent source-free geometry sidecar. This packet alone cannot approve any position.
- Fail condition: No two candidates can be source-free approved or mapped to the local predicted coordinate frame.

## Decision

- Q43088 ready for rescore now: False
- Priority packet clears locator contract: False
- Fixed-threshold audit ready to rerun now: False
- Apply or change threshold now: False
- Smallest next experiment: Review the priority positions in order and explicitly approve or reject at least two source-free locators; if none pass, approve an equivalent source-free geometry sidecar or leave Q43088 blocked.

## Interpretation

- Q43088 now has a smaller source-free review queue: four high-priority positions should be adjudicated before the other eight candidates, but none are approved by this packet.
- Reviewer or policy step: approve/reject at least two of the priority positions, then materialize the locator/geometry sidecar and rerun fixed-threshold scoring only after P07658 also clears.
