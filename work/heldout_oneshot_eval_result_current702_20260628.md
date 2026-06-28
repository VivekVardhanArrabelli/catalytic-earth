# Held-Out One-Shot Evaluation Result

Run: 2026-06-28T21:52:37Z
Verdict: **PASS**  (`heldout_oneshot_eval_PASS`)

## Pre-Registration

- Artifact: v3_heldout_oneshot_preregistration_current702_20260628
- Frozen set sha256 verified: True.
- Pass criteria: heldout in-scope recovery rate >= 0.70 AND heldout OOS false-positive rate <= 0.40.

## Held-Out Result (June 9 router, 0.44 dial, run once)

- In-scope recovery: 35/47 (0.7447).
- OOS false positives: 15/79 (0.1899).
- Calibration reference: recovery 30/35 (0.857), OOS FP 8/26 (0.308).

## Coverage

- Frozen set: 126 (47 in-scope, 79 OOS).
- Scored: in-scope 47, OOS 79.

## Guardrails

- Ran once under the frozen rule; main-repo registry never mutated; no post-hoc threshold change.
