# Cofactor-Fusion Operating Point — Train/Cal OOS Precision (leakage-safe)

Run: 2026-06-09T20:38:49Z

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
| calibration (out-of-sample) | recall 17/35 (0.4857) · FP 9/26 (0.3462) | recall 30/35 (0.8571) · FP 9/26 (0.3462) | recall 23/35 (0.6571) · FP 8/26 (0.3077) |
| train (in-sample ref) | recall 76/133 (0.5714) · FP 41/102 (0.402) | recall 132/133 (0.9925) · FP 49/102 (0.4804) | recall 123/133 (0.9248) · FP 30/102 (0.2941) |

## Dial comparison (calibration, out-of-sample)

- Threshold dial dominates suppression dial: **True**.
- On the out-of-sample calibration surface, the recalibrated-threshold dial reaches the suppression dial's OOS precision while retaining more in-scope recall.
- Lowest fused threshold matching suppression precision: 0.44 -> recall 30/35, OOS FP 8/26.

## Complementary precision lever (Lever-2 electron-flow)

- Lever-2 electron-flow is measured on the geometry/fold combined gate, not the cofactor-fusion router scored here, so its numbers are not merged with this surface. It adds OOS abstention at primary retention 1.0 and is the natural precision complement to the cofactor channel (cofactor adds recall, electron-flow adds OOS abstention).
- Measured incremental OOS abstain-recall vs geometry/fold: 0.04.

## Discipline

- This is a research diagnostic only. It does not change the frozen production threshold and does not read the spent heldout one-shot. Choosing a deployable operating point remains a separately authorized decision and would need its own (not heldout-tuned) evaluation.

## How to read

- Each cell is `recall in-scope-correct/total (rate) · FP oos-fp/total (rate)`.
- Raw fusion buys in-scope recall at an OOS false-positive cost; the two dials are the levers that cut the cost back.
- The calibration row is the deployment-honest estimate; train over-states recall because the channel was fit on train.
