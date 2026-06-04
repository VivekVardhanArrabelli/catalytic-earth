# Lever 2 Source-Free Partial Surface Current-Split Portability Readout - current702

Run: 2026-06-04T17:48:18Z

Lever 2 train/cal readout testing whether existing approved source-free partial-surface rows, locator sidecars, and event-axis linkers reduce the current geometry/fold primary or extended-OOS mechanism evidence gap. It uses entry IDs only for split accounting, does not score heldout rows, and does not apply or tune thresholds.

## Status

- lever2_source_free_partial_surface_current_split_portability_readout_research_only_reuse_negative
- Result class: research_only_reuse_negative
- Current surface: combined_mean_geometry_fold < 0.44155 abstains
- Existing partial-surface union rows: 53
- Union overlap with current primary rows: 0/34
- Union overlap with current-retained OOS rows: 0/132
- Union overlap with already-abstained OOS rows: 0/72
- Review-only locator candidate overlap with current primary rows: 1/34
- Review-only locator candidate overlap with current-retained OOS rows: 0/132

## Current Split Surface

| subset | rows |
| --- | ---: |
| current primary | 34 |
| current extended OOS candidates | 210 |
| current extended scored OOS | 204 |
| current-retained OOS | 132 |
| already-abstained OOS | 72 |

## Source-Free Partial-Surface Overlap

| surface | rows | primary overlap | retained OOS overlap | abstained OOS overlap |
| --- | ---: | ---: | ---: | ---: |
| source_free_projection_candidate_surface | 53 | 0 | 0 | 0 |
| source_free_event_axis_linkers | 14 | 0 | 0 | 0 |
| source_free_locator_sidecars | 53 | 0 | 0 | 0 |
| source_free_partial_surface_union | 53 | 0 | 0 | 0 |

## Review-Only Locator Candidate Diagnostic

| surface | rows | primary overlap | retained OOS overlap | abstained OOS overlap |
| --- | ---: | ---: | ---: | ---: |
| source_free_review_only_locator_candidates | 2 | 1 | 0 | 0 |

- Current primary rows with review-only locator candidates: m_csa:216
- Current-retained OOS rows with review-only locator candidates: none

## Missing Evidence

| gap | required | valid now | missing now | why it matters |
| --- | ---: | ---: | ---: | --- |
| current_primary_source_free_partial_surface_rows | 34 | 0 | 34 | Primary retention cost must be measurable on the current geometry/fold calibration-primary split before Lever 2 can claim operating-point value. |
| current_retained_oos_source_free_partial_surface_rows | 132 | 0 | 132 | These rows are current geometry/fold retained OOS cases; they are the direct path for source-free mechanism features to add OOS abstention value. |
| current_abstained_oos_source_free_partial_surface_rows | 72 | 0 | 72 | These complete the current extended OOS surface but are lower priority because geometry/fold already abstains. |

## Exact Missing Row Sets

- Current primary rows still requiring source-free partial-surface mechanism evidence (34): m_csa:27, m_csa:38, m_csa:41, m_csa:87, m_csa:102, m_csa:160, m_csa:165, m_csa:173, m_csa:216, m_csa:233, m_csa:277, m_csa:305, m_csa:319, m_csa:320, m_csa:338, m_csa:387, m_csa:399, m_csa:410, m_csa:473, m_csa:482, m_csa:556, m_csa:630, m_csa:694, m_csa:754, m_csa:800, m_csa:837, m_csa:865, m_csa:879, m_csa:900, m_csa:912, m_csa:922, m_csa:933, m_csa:973, m_csa:988
- Current-retained OOS rows still requiring source-free partial-surface mechanism evidence (132): m_csa:7, m_csa:8, m_csa:17, m_csa:21, m_csa:23, m_csa:25, m_csa:35, m_csa:36, m_csa:39, m_csa:48, m_csa:52, m_csa:54, m_csa:59, m_csa:60, m_csa:61, m_csa:65, m_csa:70, m_csa:74, m_csa:75, m_csa:82, m_csa:84, m_csa:85, m_csa:89, m_csa:90, m_csa:91, m_csa:95, m_csa:99, m_csa:104, m_csa:106, m_csa:107, m_csa:119, m_csa:126, m_csa:127, m_csa:135, m_csa:136, m_csa:138, m_csa:143, m_csa:150, m_csa:151, m_csa:182, m_csa:187, m_csa:190, m_csa:194, m_csa:200, m_csa:206, m_csa:207, m_csa:214, m_csa:215, m_csa:221, m_csa:222, m_csa:223, m_csa:229, m_csa:231, m_csa:234, m_csa:236, m_csa:237, m_csa:240, m_csa:243, m_csa:244, m_csa:246 ...
- Already-abstained OOS rows still requiring source-free partial-surface mechanism evidence (72): m_csa:4, m_csa:22, m_csa:24, m_csa:40, m_csa:51, m_csa:57, m_csa:72, m_csa:78, m_csa:88, m_csa:93, m_csa:105, m_csa:130, m_csa:134, m_csa:137, m_csa:139, m_csa:140, m_csa:145, m_csa:146, m_csa:149, m_csa:177, m_csa:178, m_csa:179, m_csa:184, m_csa:189, m_csa:209, m_csa:224, m_csa:251, m_csa:259, m_csa:262, m_csa:263, m_csa:264, m_csa:265, m_csa:273, m_csa:276, m_csa:282, m_csa:287, m_csa:288, m_csa:290, m_csa:301, m_csa:303, m_csa:309, m_csa:314, m_csa:318, m_csa:326, m_csa:327, m_csa:332, m_csa:342, m_csa:345, m_csa:347, m_csa:350, m_csa:359, m_csa:408, m_csa:414, m_csa:426, m_csa:439, m_csa:441, m_csa:450, m_csa:466, m_csa:496, m_csa:505 ...

## Top Missing Current-Retained OOS Rows

| row | current score |
| --- | ---: |
| m_csa:367 | 0.72395 |
| m_csa:308 | 0.68115 |
| m_csa:601 | 0.67005 |
| m_csa:99 | 0.66455 |
| m_csa:187 | 0.65175 |
| m_csa:269 | 0.65065 |
| m_csa:104 | 0.6498 |
| m_csa:348 | 0.649 |
| m_csa:468 | 0.64225 |
| m_csa:488 | 0.64045 |
| m_csa:289 | 0.6398 |
| m_csa:206 | 0.63845 |
| m_csa:268 | 0.63655 |
| m_csa:190 | 0.6365 |
| m_csa:483 | 0.6341 |
| m_csa:652 | 0.6333 |
| m_csa:25 | 0.6241 |
| m_csa:500 | 0.61935 |
| m_csa:256 | 0.61925 |
| m_csa:421 | 0.61545 |
| m_csa:52 | 0.6154 |
| m_csa:74 | 0.61305 |
| m_csa:215 | 0.61095 |
| m_csa:59 | 0.60775 |
| m_csa:272 | 0.6054 |

## Decision

- Existing partial surface reduces current primary gap: False
- Existing partial surface reduces current-retained OOS gap: False
- Route negative for existing partial-surface reuse: True
- Adds operating-point value beyond current surface: False
- Deployable now: False
- Research-only: True
- Next gate: Materialize source-free mechanism rows on the current split: 34 primary retention-gate rows and 132 current-retained OOS rows before rerunning the fixed train/cal mechanism readouts.

## Interpretation

- Existing approved source-free partial-surface rows overlap 0 current primary rows and 0 current-retained OOS rows.
- Research-only route negative: the prior approved partial source-free surface does not reduce the current train/cal primary or retained-OOS mechanism-evidence gaps, so it cannot make the integrated Lever 2 operating point measurable.
- Build source-free mechanism evidence directly for the current primary rows and current-retained OOS rows, rather than reusing the heldout-oriented partial surface.
