# Fold-Augmented Q43088 Locator Approval Packet - current702

Run: 2026-06-04T11:42:27Z

Explicit Q43088 source-free locator approval packet for Lever 3. It reviews positions 288, 286, 243, and 250 in priority order, approves the two positions that pass the conservative source-free predicted-coordinate checks, prepares a review-only locator sidecar, and does not rescore rows or change threshold 0.44155.

## Status

- fold_augmented_q43088_locator_approval_packet_cleared_review_only
- Approved locator positions: 2/2
- Active-site residue count after approval: 3/3
- Q43088 ready for row rescore now: True
- Fixed-threshold audit ready to rerun now: False
- Blockers: ['p07658_full_length_predicted_coordinate_missing', 'sixteen_row_high_cofactor_train_cal_probe_not_acquired', 'one_hundred_seventy_row_same_family_structural_acquisition_not_acquired', 'fixed_threshold_audit_not_ready_to_rerun']

## Reviewed Positions

| position | residue | distance to anchor CA (A) | mean pLDDT | decision | violations |
| ---: | --- | ---: | ---: | --- | --- |
| 288 | ASP | 3.824 | 93.69 | explicitly_approved_source_free_locator | none |
| 286 | GLN | 3.84 | 96.0 | explicitly_approved_source_free_locator | none |
| 243 | HIS | 5.918 | 97.12 | reviewed_not_selected_minimum_already_met | none |
| 250 | GLU | 7.177 | 80.44 | reviewed_not_selected_minimum_already_met | none |

## Sidecar

- Path: artifacts/v3_fold_augmented_q43088_source_free_locator_sidecar_current702_20260604.json
- Payload sha256: 67a70b904cf685344c6b38de3020a192242ea841da193cca21669cf921565157

## Decision

- Q43088 locator contract cleared now: True
- Deployment closure valid now: False
- Apply or change threshold now: False
- Next gate: Keep the Q43088 source-free locator sidecar staged for row-level scoring input. Do not rerun the fixed-threshold audit until P07658 has an approved full-length predicted coordinate; calibration closure still needs the 16-row high-cofactor probe and 170-row structural acquisition.

## Interpretation

- Q43088's locator blocker is cleared for review-only staging: positions 288 and 286 are approved as source-free locators from the local predicted coordinate, while 243 and 250 were reviewed but not needed for the minimum.
- Use this sidecar as Q43088's row-level geometry input only after the P07658 coordinate blocker is cleared; do not change threshold 0.44155.
