# Current-57 Cofactor Precision Contract

Run: 2026-06-28T02:39:45Z
Status: `blocked_current57_cofactor_precision_contract_not_deployable`

## Done Bar

- Surface: calibration, out-of-sample for the sequence cofactor channel.
- Required primary recovery: >= 30/35.
- Required OOS FP ceiling: <= 8/26 at the trusted June 9 threshold dial.

## Current-57 Readout

- Exact current-57 fused at frozen threshold: threshold 0.4115: recall 13/35 (0.3714) · OOS FP 26/26 (1.0).
- Legacy-v1 metal-compatible fused at frozen threshold: threshold 0.4115: recall 26/35 (0.7429) · OOS FP 26/26 (1.0).
- Taxonomy-version recovered rows at frozen threshold: 13.
- Remaining recovery gap vs trusted bar: 4.
- Best compatible point under the trusted OOS FP ceiling: threshold 0.733: recall 20/35 (0.5714) · OOS FP 8/26 (0.3077).

## Decision

- Fail closed for atlas-engine fusion on the current-57 cofactor surface. Either pin/replay the intended June 9 router/fingerprint surface, or build a new precision channel/fusion rule with a new preregistered train/cal done bar before any heldout-facing read.

## Guardrails

- No heldout rows were scored or read.
- No production threshold, model weight, split, label, ontology, registry, or fingerprint-family change was made.
