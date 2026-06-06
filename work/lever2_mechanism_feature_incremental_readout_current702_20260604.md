# Lever 2 Mechanism Feature Incremental Readout - current702

Run: 2026-06-04T15:05:13Z

Lever 2 train/cal readout for a genuinely row-specific mechanism surface: row-specific bond-change/proton/electron/event-topology features scored by the frozen residual contract, compared against the current geometry/fold operating point on overlapping non-heldout rows. The mechanism features remain train/cal-only and are not a deployment-valid source-free heldout projection.

## Status

- lever2_mechanism_feature_incremental_readout_research_only_overlap_blocked
- Result class: research_only
- Current surface: combined_mean_geometry_fold < 0.44155 abstains
- Mechanism residual > 3.21469422 abstains
- Valid primary overlap: 0/34
- OOS overlap: 8/75

## Measured Readout

| surface | rows | abstained or retained | recall |
| --- | ---: | ---: | ---: |
| current OOS overlap abstain | 8 | 3 | 0.375 |
| mechanism OOS overlap abstain | 8 | 6 | 0.75 |
| union OOS overlap abstain | 8 | 7 | 0.875 |
| union primary overlap retain | 0 | 0 | None |

## OOS Overlap Rows

| row | current score | current abstains | mechanism residual | mechanism abstains | union abstains | caught retained OOS |
| --- | ---: | --- | ---: | --- | --- | --- |
| m_csa:17 | 0.45885 | False | 6.02277599 | True | True | True |
| m_csa:25 | 0.6241 | False | 3.67227966 | True | True | True |
| m_csa:40 | 0.41725 | True | 3.63849194 | True | True | False |
| m_csa:78 | 0.4054 | True | 2.33596541 | False | True | False |
| m_csa:85 | 0.49955 | False | 4.96150995 | True | True | True |
| m_csa:149 | 0.37655 | True | 3.55609944 | True | True | False |
| m_csa:222 | 0.52675 | False | 5.21496062 | True | True | True |
| m_csa:246 | 0.5171 | False | 1.71494092 | False | False | False |

## Missing Evidence

| gap | required | valid now | why it matters |
| --- | ---: | ---: | --- |
| current_calibration_primary_source_free_mechanism_features | 34 | 0 | Incremental value cannot be claimed without measuring primary retention on rows that are calibration/evaluation rows for the current geometry/fold surface. |
| current_calibration_oos_source_free_mechanism_features | 75 | 8 | The local OOS lift is measured on the available overlap, but the coverage is too sparse to represent the current train/cal OOS surface. |
| single_split_aligned_lever2_operating_contract | 109 | 8 | The current mechanism sidecar and the current geometry/fold threshold contract use different train/cal partitions. |

## Exact Missing Row Sets

- Current calibration primary rows still requiring source-free mechanism features (34): m_csa:27, m_csa:38, m_csa:41, m_csa:87, m_csa:102, m_csa:160, m_csa:165, m_csa:173, m_csa:216, m_csa:233, m_csa:277, m_csa:305, m_csa:319, m_csa:320, m_csa:338, m_csa:387, m_csa:399, m_csa:410, m_csa:473, m_csa:482, m_csa:556, m_csa:630, m_csa:694, m_csa:754, m_csa:800, m_csa:837, m_csa:865, m_csa:879, m_csa:900, m_csa:912, m_csa:922, m_csa:933, m_csa:973, m_csa:988
- Current calibration OOS rows still requiring source-free mechanism features (67): m_csa:4, m_csa:22, m_csa:35, m_csa:36, m_csa:39, m_csa:52, m_csa:54, m_csa:57, m_csa:61, m_csa:65, m_csa:82, m_csa:93, m_csa:104, m_csa:106, m_csa:119, m_csa:126, m_csa:136, m_csa:140, m_csa:145, m_csa:177, m_csa:178, m_csa:184, m_csa:189, m_csa:243, m_csa:244, m_csa:262, m_csa:264, m_csa:271, m_csa:284, m_csa:285, m_csa:290, m_csa:295, m_csa:299, m_csa:301, m_csa:303, m_csa:314, m_csa:325, m_csa:342, m_csa:345, m_csa:347, m_csa:368, m_csa:390, m_csa:408, m_csa:414, m_csa:415, m_csa:422, m_csa:426, m_csa:439, m_csa:462, m_csa:464, m_csa:471, m_csa:483, m_csa:490, m_csa:496, m_csa:499, m_csa:503, m_csa:525, m_csa:531, m_csa:537, m_csa:542, m_csa:547, m_csa:565, m_csa:575, m_csa:622, m_csa:646, uniprot:P78549, uniprot:Q3LXA3

## Missing OOS Priority

- Current-retained missing OOS rows: 40
- Already-abstained missing OOS rows: 27
- Prioritize current-retained rows first because they are the direct route to incremental OOS value beyond geometry/fold.

| retained OOS row | accession | current score |
| --- | --- | ---: |
| m_csa:104 | P13650 | 0.6498 |
| m_csa:483 | A9CEQ8 | 0.6341 |
| m_csa:52 | P0AB71 | 0.6154 |
| m_csa:464 | P11766 | 0.60295 |
| m_csa:415 | P22643 | 0.58595 |
| m_csa:471 | Q9GPQ4 | 0.5853 |
| m_csa:39 | Q27546 | 0.58215 |
| m_csa:271 | P56839 | 0.5757 |
| m_csa:622 | P31677 | 0.5615 |
| m_csa:54 | P24670 | 0.55665 |
| m_csa:503 | B9JNP7 | 0.55265 |
| m_csa:65 | P0A7D4 | 0.5474 |
| m_csa:646 | P31939 | 0.54185 |
| m_csa:542 | P38677 | 0.5365 |
| m_csa:243 | P0A794 | 0.53445 |
| m_csa:36 | Q60099 | 0.51785 |
| m_csa:136 | P22337 | 0.51505 |
| m_csa:126 | P12944 | 0.5127 |
| m_csa:285 | P21332 | 0.50825 |
| m_csa:106 | P21873 | 0.50535 |

## Decision

- Local OOS signal measured: True
- Valid integrated operating point measurable: False
- Adds operating-point value beyond current surface: False
- Deployable now: False
- Research-only: True
- Next experiment: Materialize the same source-free mechanism feature contract for the 34 current geometry/fold calibration-primary rows and the 67 current train/cal OOS negative rows not already covered by the mechanism sidecar, then rerun this fixed-threshold union readout without reading or tuning on heldout.

## Interpretation

- Mechanism features catch 4/5 current-surface retained OOS rows on the available overlap, but valid primary overlap is 0 rows.
- Research-only: the train/cal row-specific mechanism surface shows local OOS signal beyond geometry/fold, but the current data cannot measure the in-scope retention cost because the mechanism calibration primaries are current geometry/fold train targets.
- Build a split-aligned source-free mechanism sidecar for the current geometry/fold calibration-primary and train/cal OOS rows.
