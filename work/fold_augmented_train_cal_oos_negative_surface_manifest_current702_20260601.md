# Fold-Augmented Train/Cal OOS Negative Surface Manifest - current702

Run: 2026-06-01T04:17:17Z

Bounded manifest for adding train/cal OOS negatives to the fold-augmented threshold contract. This does not score rows or change labels; it identifies which current702 in-distribution OOS rows could be used for threshold calibration.

## Status

- manifest_staged_missing_predicted_geometry_and_fold_scores_for_train_cal_oos
- In-distribution OOS candidates: 378
- Hash-selected calibration OOS candidates: 76
- Already in predicted atlas: 0
- Missing predicted-geometry retrieval: 378

## Blockers

- predicted_geometry_retrieval_missing_for_in_distribution_oos_candidates
- predicted_structure_fold_scores_missing_for_in_distribution_oos_candidates_vs_train_atlas
- threshold_contract_currently_selects_in_scope_retention_only

## Candidate Preview

First 40 hash-selected calibration OOS candidates:

`m_csa:4`, `m_csa:17`, `m_csa:22`, `m_csa:25`, `m_csa:35`, `m_csa:36`, `m_csa:39`, `m_csa:40`, `m_csa:52`, `m_csa:54`, `m_csa:57`, `m_csa:61`, `m_csa:65`, `m_csa:78`, `m_csa:82`, `m_csa:85`, `m_csa:93`, `m_csa:104`, `m_csa:106`, `m_csa:119`, `m_csa:126`, `m_csa:136`, `m_csa:140`, `m_csa:145`, `m_csa:149`, `m_csa:177`, `m_csa:178`, `m_csa:184`, `m_csa:189`, `m_csa:204`, `m_csa:222`, `m_csa:243`, `m_csa:244`, `m_csa:246`, `m_csa:262`, `m_csa:264`, `m_csa:271`, `m_csa:284`, `m_csa:285`, `m_csa:290`

## Interpretation

- There are enough non-heldout OOS rows to calibrate OOS abstention in principle, but none are currently present in the predicted-geometry atlas/fold channel.
- Implement or stage a predicted-geometry plus Foldseek scoring pass for the 76 hash-selected calibration OOS candidates before treating the fold-augmented threshold as OOS-optimized.
