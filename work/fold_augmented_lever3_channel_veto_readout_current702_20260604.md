# Fold-Augmented Lever 3 Channel-Veto Readout - current702

Run: 2026-06-04T17:29:38Z

Lever 3 measured channel-veto readout over already selected train/cal source-free channel thresholds. It compares single channels and channel-union stress tests against calibration in-scope retention plus hard-confounded train/cal OOS proxy rows. It reads no heldout rows, stages no coordinates, scores no new rows, and does not change threshold 0.44155.

## Status

- fold_augmented_lever3_channel_veto_readout_ready_no_closure
- Calibration retention floor: 31/34
- Candidate/scored/missing train-cal OOS rows: 210/204/6
- Missing full-channel high/same-family overlap: 0/0
- Proxy row diagnostics: 4 high-cofactor, 59 same-family
- Baseline high-cofactor/same-family: 0/4 and 11/59
- Best single-channel high/same-family: 2/4 and 27/59
- Best overblock union high/same-family/in-scope retained: 3/4, 38/59, 22/34
- Blockers: ['no_retention_preserving_single_channel_closes_high_cofactor', 'no_retention_preserving_single_channel_closes_same_family', 'no_retention_preserving_channel_union_closes_both_axes', 'stronger_confounded_abstention_requires_overblocking_in_scope']

## Channel Readouts

| route | retained in-scope | train/cal OOS abstained | high-cofactor | same-family | closure |
| --- | ---: | ---: | ---: | ---: | --- |
| single_channel::cofactor_max_score | 31/34 | 54/204 | 0/4 | 18/59 | False |
| single_channel::combined_mean_geometry_cofactor_fold | 31/34 | 122/204 | 0/4 | 27/59 | False |
| single_channel::combined_mean_geometry_fold | 31/34 | 72/204 | 0/4 | 11/59 | False |
| single_channel::combined_min_geometry_fold | 31/34 | 26/204 | 2/4 | 0/59 | False |
| single_channel::fold_nearest_atlas_tm_score | 31/34 | 40/204 | 1/4 | 0/59 | False |
| single_channel::geometry_top1_score | 31/34 | 26/204 | 2/4 | 0/59 | False |

## Best Routes

- Same-family single-channel route: single_channel::combined_mean_geometry_cofactor_fold
- High-cofactor single-channel route: single_channel::combined_min_geometry_fold
- Best retention-preserving union: channel_union::combined_min_geometry_fold+geometry_top1_score
- Best overblock union: channel_union::cofactor_max_score+combined_mean_geometry_cofactor_fold+combined_min_geometry_fold+fold_nearest_atlas_tm_score

## Missing Tail Sensitivity

- The current six missing full-channel rows do not overlap the strict high-cofactor or same-family proxy row sets used by this readout; they can affect all-OOS coverage, but not the hard proxy-axis no-closure result.
- Missing full-channel rows: m_csa:204, m_csa:416, m_csa:562, m_csa:586, m_csa:604, m_csa:637

## Decision

- Current evidence sufficient for deployment closure: False
- Best single channel improves same-family without retention loss: True
- Best retention-preserving union closes both axes: False
- Missing full-channel tail hides proxy closure: False
- Stronger abstention requires overblocking in-scope: True
- Next gate: Existing source-free channel thresholds cannot close Lever 3: the same-family channel improvement still misses high-cofactor, and unions that catch more high-cofactor rows overblock calibration in-scope rows. Keep threshold 0.44155 fixed; obtain P07658 accepted predicted-coordinate provenance and acquire new strict high-cofactor train/cal OOS rows.

## Interpretation

- Existing train/cal-selected channel thresholds expose a measured same-family improvement but not a deployment-closing confounder veto.
- The best retention-preserving single channel for same-family abstains 27/59 rows, versus 11/59 at the baseline channel, but the best high-cofactor retention-preserving channel reaches only 2/4.
- Do not promote a channel-union veto from current evidence. The smallest productive path remains P07658 accepted prediction provenance plus strict high-cofactor row acquisition.
