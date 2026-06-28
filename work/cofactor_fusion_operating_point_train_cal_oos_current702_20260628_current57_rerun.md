# Cofactor-Fusion Operating Point — Current-57 Rerun Diagnostic

Run: 2026-06-28T01:39:17Z

This is a current repo rerun after the scaling-era expansion to 57 fingerprint
families. It is **not** a replacement for the trusted June 9 cofactor precision
contract. The default router now scores against the expanded fingerprint
registry, so the old 30/35 calibration fused recall and 9/26 OOS FP surface is
not directly reproduced here. Treat this as a preregistration blocker/diagnostic
for atlas-engine fusion until the intended router/fingerprint surface is
explicitly frozen.

Closes the precision side of the Problem-2 step-4 operating-point question.
The recovery harness measured the recall side leakage-safe but had no OOS
rows; this scores the in-distribution train/cal OOS rows through the same
frozen cofactor-fusion router so the two precision dials can be compared.
Calibration is the out-of-sample (honest) surface; train is in-sample only;
heldout is never read.

## Coverage

- In-scope in-distribution rows: 171 (predicted-apo ok 168).
- OOS in-distribution rows: 342 (predicted-apo ok 128; coverage gaps 214 — staged train/cal-safe CIFs only, not true negatives).

## Operating points (in-scope recall | OOS false-positive rate)

| Surface | apo baseline | fused @ frozen | fused + suppression |
| --- | --- | --- | --- |
| calibration (out-of-sample) | recall 6/35 (0.1714) · FP 26/26 (1.0) | recall 13/35 (0.3714) · FP 26/26 (1.0) | recall 13/35 (0.3714) · FP 26/26 (1.0) |
| train (in-sample ref) | recall 24/133 (0.1805) · FP 101/102 (0.9902) | recall 64/133 (0.4812) · FP 101/102 (0.9902) | recall 64/133 (0.4812) · FP 101/102 (0.9902) |

## Dial comparison (calibration, out-of-sample)

- Threshold dial dominates suppression dial: **False**.
- Threshold and suppression dials are not cleanly separable on the calibration surface; read both and the train-reference surface.
- Lowest fused threshold matching suppression precision: 0.4115 -> recall 13/35, OOS FP 26/26.

## Complementary precision lever (Lever-2 electron-flow)

- Lever-2 electron-flow is measured on the geometry/fold combined gate, not the cofactor-fusion router scored here, so its numbers are not merged with this surface. It adds OOS abstention at primary retention 1.0 and is the natural precision complement to the cofactor channel (cofactor adds recall, electron-flow adds OOS abstention).
- Measured incremental OOS abstain-recall vs geometry/fold: 0.04.

## Discipline

- This is a research diagnostic only. It does not change the frozen production threshold and does not read the spent heldout one-shot. Choosing a deployable operating point remains a separately authorized decision and would need its own (not heldout-tuned) evaluation.

## How to read

- Each cell is `recall in-scope-correct/total (rate) · FP oos-fp/total (rate)`.
- Raw fusion buys in-scope recall at an OOS false-positive cost; the two dials are the levers that cut the cost back.
- The calibration row is the deployment-honest estimate; train over-states recall because the channel was fit on train.
