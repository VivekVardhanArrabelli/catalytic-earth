# Heldout One-Shot — Cofactor Fusion Blind Pass

Run: 2026-06-04 (single authorized blind pass; nothing refit/retuned in response)

Applied the FROZEN leakage-safe cofactor-presence channel
(`v3_cofactor_presence_calibration_current702_20260604`, heads fit on train,
thresholds/backend selected on calibration) to the heldout rows via raw cofactor
fusion at the frozen router threshold 0.4115. The channel's heldout predictions
were emitted out-of-sample when the channel was built; this is pure application.

## Result (canonical 45-primary mask)

| Surface | Primary | Abstained | Wrong (non-abstained) | OOS/sec FP rate |
| --- | ---: | ---: | ---: | ---: |
| Baseline predicted-apo (no channel) | 23/45 | 17 | 5 | 0.1235 |
| Raw cofactor fusion (frozen channel) | 37/45 | 2 | 6 | 0.2593 |

- Net primary recovery: +14 (14 of the 22 apo-lost primaries = 63.6%).
- Abstentions 17 -> 2; wrong non-abstained primaries 5 -> 6 (+1).
- Precision cost: OOS/secondary false-positive rate roughly doubled
  (0.1235 -> 0.2593).

## Reading

- The baseline reproduces the known 23/45 exactly, confirming the harness.
- The out-of-sample calibration recovery (70.6%) accurately predicted the heldout
  recovery (63.6%); the projected ~38/45 landed at 37/45. The leakage-safe
  in-distribution surface was a faithful proxy.
- Raw fusion buys large primary recovery at a genuine precision cost (OOS
  over-opening) that the in-distribution surface could not measure (no OOS rows
  in-distribution).

## Discipline

This is a recorded result only. No threshold, policy, channel, or label was
changed in response to it. Any operating-point that trades recovery for precision
(the pre-built sequence-supported suppression dial, or a recalibrated abstention
threshold) is a SEPARATE decision and must not be tuned against this one-shot.

Reference: `artifacts/v3_heldout_oneshot_cofactor_fusion_blind_pass_current702_20260604.json`
