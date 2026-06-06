# Cofactor Presence Calibration (leakage-safe train/cal)

Run: 2026-06-04T14:47:18Z

## Guardrails

- Heads fit on the train split only; thresholds and backend selected on the
  calibration split only; heldout labels never read.
- Supervision is structural ligand context only (no mechanism fingerprint, EC,
  Rhea, mechanism text, or benchmark labels).

## Split Coverage

- Clean rows: 682; in-distribution clean: 547.
- Covered by split manifest: 513 ({'calibration': 103, 'train': 410}).
- Split-uncovered in-distribution: 34; heldout clean (scored, truth not read): 135.

## Per-class calibration operating points (selected backend)

| Class | Backend | Cal AUC | Cal AP | Thr | Prec | Recall | F1 | Cal pos | Low support |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| metal_ion | esm2_t6_8m | 0.76413 | 0.479608 | 0.823761 | 0.571429 | 0.521739 | 0.545455 | 23 | False |
| flavin | esm2_t12_35m | 0.935526 | 0.739809 | 0.689529 | 0.833333 | 0.625 | 0.714286 | 8 | False |
| plp | esm2_t6_8m | 0.992424 | 0.804167 | 0.660692 | 0.666667 | 1.0 | 0.8 | 4 | True |
| heme | esm2_t12_35m | 0.93 | 0.708333 | 0.730547 | 1.0 | 0.666667 | 0.8 | 3 | True |

## Predicted family counts by split

```json
{
  "heldout": {
    "flavin": 10,
    "heme": 8,
    "metal_ion": 26,
    "none_predicted": 93,
    "plp": 8,
    "rows": 140
  },
  "in_distribution": {
    "flavin": 39,
    "heme": 18,
    "metal_ion": 122,
    "none_predicted": 363,
    "plp": 25,
    "rows": 562
  }
}
```

## Next step (one-shot, not run here)

- These per-entry predictions are drop-in compatible with the router
  ligand_context injection in sequence_cofactor_channel. Applying them to
  the heldout mechanism router reads the one-shot heldout mechanism labels
  and must be explicitly authorized before it is run.
