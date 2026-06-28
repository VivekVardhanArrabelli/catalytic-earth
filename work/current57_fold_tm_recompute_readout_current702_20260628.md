# Current-57 Fold/TM Recompute Readout

Run: 2026-06-28T11:40:22Z
Status: `current57_fold_tm_recompute_readout_row_aligned`

## Row Alignment

- Cached overlap (prior, alignment audit): in-scope 4/35, OOS 0/26.
- Recomputed overlap: in-scope 35/35, OOS 26/26.
- Resolves alignment blocker: True.

## Coverage

- Calibration in-scope: 35/35 (1.0).
- Calibration OOS: 26/26 (1.0).

## Fold-NN TM Separation (calibration-only diagnostic)

- In-scope best-alntmscore median: 0.743 (mean 0.7282, n 35).
- OOS best-alntmscore median: 0.5661 (mean 0.5802, n 26).
- In-scope minus OOS median gap: 0.1769 (abstention signal present: True).

## Fold-NN Fingerprint Consistency

- In-scope fold-NN true-fingerprint match: 28/35 (0.8).

## Decision

- Row alignment is resolved, so the cofactor/fold alignment blocker no longer applies. This readout does not authorize a fused atlas-engine readout on its own: the current-57 cofactor precision contract still governs deployment, and any fold-augmented fusion must be preregistered with a heldout-final selection rule.

## Guardrails

- Scores are calibration-vs-train only; no heldout rows were scored or read.
- No threshold was selected on heldout rows; no supervised model was trained.
- No production threshold, model weight, registry, ontology, label, or fingerprint-family change was made.
