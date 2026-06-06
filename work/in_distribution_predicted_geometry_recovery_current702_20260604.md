# In-Distribution Predicted-Apo Recovery (leakage-safe)

Run: 2026-06-04T14:35:51Z

Leakage-safe analog of the heldout 45/45 -> predicted 23/45 drop, scored on
in-distribution rows. Calibration is the honest out-of-sample readout for the
cofactor channel; train is an in-sample reference only; heldout is never read.

- Atlas target rows: 171; predicted-geometry ok:
  168; threshold 0.4115.
- Reconstruction context: cofactor; channel:
  v3_cofactor_presence_calibration_current702_20260604.

## Recovery by split

| Split | OOS? | N | exp ok | apo ok | apo drop | fused ok | recovered/lost | regressed |
| --- | --- | ---: | ---: | ---: | ---: | ---: | :---: | ---: |
| calibration | yes | 35 | 34 | 17 | 17 | 30 | 12/17 | 0 |
| train | no | 136 | 135 | 76 | 59 | 132 | 56/59 | 0 |

## How to read

- `apo drop` = experimental-correct minus apo-correct (the coordinate-source cost).
- `recovered/lost` = apo-lost primaries that the cofactor-fused router brings back.
- `regressed` = rows correct under apo that fusion breaks (the over-opening cost).
- The calibration row is the deployment-honest estimate; train over-states recovery
  because the channel was fit on those rows.
