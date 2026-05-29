# Sequence Cofactor Channel

Run: 2026-05-29T23:02:13Z

## Label Set

- Frozen clean rows: 682.
- Split counts: {'in_distribution': 547, 'heldout': 135}.
- Class counts: {'heldout': {'flavin': 11, 'heme': 5, 'metal_ion': 29, 'none': 80, 'plp': 6}, 'in_distribution': {'flavin': 40, 'heme': 18, 'metal_ion': 146, 'none': 297, 'plp': 24}}.

## Trained Heads

| Backend | Class | ROC AUC | AP | TP | FP | FN | TN |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| esm2_t12_35m | metal_ion | 0.673715 | 0.364756 | 13 | 27 | 16 | 79 |
| esm2_t12_35m | flavin | 0.918622 | 0.732961 | 7 | 5 | 4 | 119 |
| esm2_t12_35m | plp | 0.981912 | 0.883333 | 5 | 3 | 1 | 126 |
| esm2_t12_35m | heme | 0.764615 | 0.38405 | 1 | 5 | 4 | 125 |
| esm2_t6_8m | metal_ion | 0.607027 | 0.307283 | 12 | 35 | 17 | 71 |
| esm2_t6_8m | flavin | 0.874633 | 0.635522 | 6 | 5 | 5 | 119 |
| esm2_t6_8m | plp | 0.990956 | 0.876623 | 5 | 3 | 1 | 126 |
| esm2_t6_8m | heme | 0.866154 | 0.525794 | 3 | 5 | 2 | 125 |

## Borrowed Predictor

- M-Ionic: {'status': 'complete', 'borrowed_predictor': 'M-Ionic', 'metrics': {'average_precision': 0.567376, 'expected_row_count': 135, 'heldout_metal_negative_count': 106, 'heldout_metal_positive_count': 29, 'roc_auc': 0.781067, 'scored_row_count': 135, 'status': 'complete'}, 'repository': 'https://github.com/TeamSundar/m-ionic'}.

## Selected Sources

{
  "flavin": {
    "average_precision": 0.732961,
    "roc_auc": 0.918622,
    "source": "trained:esm2_t12_35m"
  },
  "heme": {
    "average_precision": 0.525794,
    "roc_auc": 0.866154,
    "source": "trained:esm2_t6_8m"
  },
  "metal_ion": {
    "average_precision": 0.567376,
    "roc_auc": 0.781067,
    "source": "borrowed:mionic"
  },
  "plp": {
    "average_precision": 0.876623,
    "roc_auc": 0.990956,
    "source": "trained:esm2_t6_8m"
  }
}
