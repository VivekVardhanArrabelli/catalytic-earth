# Fold-Augmented Lever 3 Current Measured Readout - current702

Run: 2026-06-04T15:03:18Z

Lever 3 measured readout for the current predicted-structure fold/geometry novelty gate. It reports the unchanged train/cal-selected operating point on the latest non-heldout OOS surface first, then names the remaining evidence gaps needed before deployment closure.

## Status

- fold_augmented_lever3_current_measured_readout_ready_evidence_insufficient
- Fixed channel: combined_mean_geometry_fold
- Fixed threshold: 0.44155
- Scored train/cal OOS rows: 204/210
- All train/cal OOS abstained/retained: 72/132
- Train/cal in-scope retained: 31/34
- Missing full-channel rows: 6

## Measured Readout

| subset | rows | abstained | retained | recall |
| --- | ---: | ---: | ---: | ---: |
| all train/cal OOS | 204 | 72 | 132 | 0.3529 |
| high-cofactor proxy | 4 | 0 | 4 | 0.0 |
| same-family structural proxy | 59 | 11 | 48 | 0.1864 |

## High-Cofactor Proxy Rows

| row | combined | margin | abstains | nearest train | top1 |
| --- | ---: | ---: | --- | --- | --- |
| m_csa:368 | 0.4537 | 0.01215 | False | m_csa:281 | heme_peroxidase_oxidase |
| m_csa:361 | 0.45695 | 0.0154 | False | m_csa:822 | metal_dependent_hydrolase |
| m_csa:298 | 0.5344 | 0.09285 | False | m_csa:275 | flavin_monooxygenase |
| m_csa:289 | 0.6398 | 0.19825 | False | m_csa:275 | flavin_dehydrogenase_reductase |

## Missing Full-Channel Rows In Scored Surface

These rows are missing from the latest scored surface artifact. The current-evidence packet narrows the live surface-completeness blocker before rerun to P07658.

| row | accession | predicted geometry status |
| --- | --- | --- |
| m_csa:204 | P10746 | missing |
| m_csa:416 | P07071 | predicted_structure_fetch_failed |
| m_csa:562 | P07658 | predicted_structure_fetch_failed |
| m_csa:586 | P00806 | predicted_structure_fetch_failed |
| m_csa:604 | Q43088 | missing |
| m_csa:637 | P04531 | predicted_structure_fetch_failed |

## Remaining Evidence

| gap | current count | smallest next experiment |
| --- | ---: | --- |
| p07658_surface_completeness | 1 | Clear P07658 with an exact full-length predicted coordinate from an approved runtime/provider, then run row scoring at unchanged threshold 0.44155. |
| high_cofactor_train_cal_oos_acquisition | 16 | Fill and score 16 new non-heldout train/cal high-cofactor OOS rows at unchanged threshold 0.44155. |
| same_family_structural_train_cal_oos_acquisition | 170 | Fill and score enough new non-heldout train/cal same-family structural OOS rows to close the 170-row lower-bound gap. |

## Decision

- Measured readout available: True
- Deployment-valid readout available: True
- Current evidence sufficient for deployment closure: False
- High-cofactor proxy target met: False
- Same-family structural proxy target met: False
- Next gate: Do not change threshold 0.44155. The current readout is measured and source-free, but it is not confounded-safe enough for deployment closure: P07658 still needs accepted full-length predicted-coordinate provenance, the high-cofactor axis needs 16 accepted train/cal OOS rows, and the same-family structural axis needs the larger 170-row acquisition.

## Interpretation

- At the unchanged fixed threshold, 72/204 scored train/cal OOS rows abstain while train/cal in-scope retention remains 31/34.
- The current source-free evidence is enough to measure the operating point, but not enough to close Lever 3: high-cofactor proxy abstention is 0/4 and same-family structural proxy abstention is 11/59.
- Run the P07658 prediction/provenance acceptance path first; then acquire and score the frozen high-cofactor train/cal OOS probe before the larger same-family structural acquisition.
