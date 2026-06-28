# Current-57 Cofactor/Fold Alignment Audit

Run: 2026-06-28T03:41:20Z
Status: `blocked_cached_fold_surface_not_row_aligned_with_current57_cofactor_surface`

## Alignment Gate

- Calibration in-scope overlap required: >= 0.9.
- Calibration OOS overlap required: >= 0.9.
- Calibration in-scope overlap observed: 4/35 (0.1143).
- Calibration OOS overlap observed: 0/26 (0.0).
- Decision: `fail_closed_cached_fold_rows_do_not_cover_current57_cofactor_surface`.

## Overlap-Only Probe

- Interpretable: False.
- Fold threshold: 0.44155.
- Compatible positives retained on overlap: 3.
- OOS false positives retained on overlap: 0.

## Decision

- Fail closed for cached atlas-engine fusion. Install/expose foldseek and recompute Fold/TM on the current-57 train/cal cofactor rows, or pin/replay the older router/fingerprint surface whose fold rows are already cached.

## Guardrails

- No heldout rows were scored or read.
- No new Foldseek/TM scores, model weights, thresholds, labels, registries, ontologies, or fingerprint families were changed.
