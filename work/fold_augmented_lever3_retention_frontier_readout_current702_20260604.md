# Fold-Augmented Lever 3 Retention Frontier Readout - current702

Run: 2026-06-04T18:17:18Z

Lever 3 measured retention-frontier readout over train/cal-selected source-free channel thresholds. It asks whether any current fixed single-channel or channel-union route can catch the strict high-cofactor and same-family proxy rows at an operating point, and quantifies the in-scope retention cost. It reads no heldout rows, scores no new rows, stages no coordinates, and does not select or change thresholds.

## Status

- fold_augmented_lever3_retention_frontier_readout_ready_no_closure
- Fixed baseline threshold: 0.44155
- Calibration retention floor: 31/34
- Routes evaluated: 63 (6 single, 57 unions)
- Strict high-cofactor/same-family rows: 4/59
- Routes closing both axes at 90pct/any retention: 0/0
- P07658 provider attempt coordinate returned: False (BioLM ESMFold, HTTP 401)

## Frontier

| floor | retained rows | eligible routes | closing routes | best route | high | same | shortfall |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| retain_100pct | 34 | 0 | 0 | n/a | n/a | n/a | n/a |
| retain_95pct | 33 | 0 | 0 | n/a | n/a | n/a | n/a |
| retain_90pct | 31 | 7 | 0 | single_channel::combined_mean_geometry_cofactor_fold | 0/4 | 27/59 | 25 |
| retain_85pct | 29 | 8 | 0 | channel_union::combined_mean_geometry_cofactor_fold+combined_mean_geometry_fold | 0/4 | 27/59 | 25 |
| retain_80pct | 28 | 25 | 0 | channel_union::cofactor_max_score+combined_mean_geometry_cofactor_fold | 0/4 | 38/59 | 14 |
| retain_75pct | 26 | 30 | 0 | channel_union::cofactor_max_score+combined_mean_geometry_cofactor_fold+combined_mean_geometry_fold | 0/4 | 38/59 | 14 |
| no_in_scope_floor | 0 | 63 | 0 | channel_union::cofactor_max_score+combined_mean_geometry_cofactor_fold+combined_mean_geometry_fold+combined_min_geometry_fold+fold_nearest_atlas_tm_score | 3/4 | 38/59 | 11 |

## Best Current Route

- Route: channel_union::cofactor_max_score+combined_mean_geometry_cofactor_fold+combined_mean_geometry_fold+combined_min_geometry_fold+fold_nearest_atlas_tm_score
- In-scope retained/lost: 20/14
- High-cofactor abstained/target: 3/4
- Same-family abstained/target: 38/48
- Proxy shortfall rows: 11
- Unabstained high-cofactor rows under best route: m_csa:289
- Unabstained same-family rows under best route: m_csa:25, m_csa:52, m_csa:74, m_csa:84, m_csa:89, m_csa:135, m_csa:190, m_csa:223, m_csa:229, m_csa:256, m_csa:289, m_csa:308, m_csa:451, m_csa:463, m_csa:464, m_csa:468, m_csa:488, m_csa:502, m_csa:503, m_csa:638, m_csa:646

## P07658 Provider Attempt

- Provider: BioLM ESMFold
- Endpoint: https://biolm.ai/api/v3/esmfold/predict/
- HTTP status: 401
- Coordinate returned: False
- Response: {"detail":"Authentication credentials were not provided."}

## Decision

- Current source-free channels close both axes at 90pct floor: False
- Current source-free channels close both axes at any retention: False
- Fresh P07658 provider attempt returned coordinate: False
- Exact missing evidence: ['new source-free channel evidence or newly scored hard-proxy train/cal rows; current fixed channel unions do not reach the 80pct abstention target for both strict proxy axes even with no in-scope retention floor', 'accepted full-length P07658 predicted coordinate provenance before fixed-threshold surface rerun']
- Next gate: Do not change threshold 0.44155. Current fixed source-free channels do not provide a deployable hard-confounder operating point; continue with accepted P07658 prediction provenance and new strict high-cofactor train/cal acquisition.

## Interpretation

- Current source-free fixed channel unions do not close the hard proxy axes at the 90pct in-scope retention floor.
- At the best no-floor route, high-cofactor abstention is 3/4 and same-family abstention is 38/59; proxy shortfall remains 11 rows.
- Treat current predicted-structure/source-free evidence as insufficient for Lever 3 closure; obtain P07658 accepted coordinate provenance, then add strict high-cofactor train/cal rows before retrying the operating-point readout.
