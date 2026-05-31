# D11 Mechanism Relationship Evaluation Cofactor Augmented

Run created: `2026-05-31T01:37:13Z`

## Decision

The row-level sidecar blocker is cleared for a bounded D11 rerun. This artifact evaluates a cofactor-augmented predicted-geometry query representation using fixed persisted sidecar scores, without refitting models or tuning thresholds on heldout rows.

No labels, registries, ontologies, imports, production scoring, global thresholds, heldout splits, or model weights were changed.

## Sidecar Gate

- Row-class records: 2106.
- Entries with flavin/heme/PLP scores: 702.
- Source counts: {'trained:esm2_t12_35m': 702, 'trained:esm2_t6_8m': 1404}.
- Caveat: Organic cofactor scores use the strict original selected t6/t12 ESM heads with row-level sidecars retained.

## Relationship Rank Metrics

| Surface | Variant | Queries | Exact top1 | Family top3 any | Family MRR | Notes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Predicted geometry score query vs experimental atlas score vector rerun | `cosine` | 45 | 0.666667 | 0.8 | 0.756312 | No model was trained for this surface; robust_l2 scaling was fit on candidate in-distribution vectors only. |
| Predicted geometry score query vs experimental atlas score vector rerun | `robust_l2` | 45 | 0.622222 | 0.688889 | 0.676188 | No model was trained for this surface; robust_l2 scaling was fit on candidate in-distribution vectors only. |
| Predicted geometry score query plus selected organic cofactor sidecar vs experimental atlas | `cosine` | 45 | 0.822222 | 0.866667 | 0.860455 | No model was trained for this surface; robust_l2 scaling was fit on candidate in-distribution vectors only. |
| Predicted geometry score query plus selected organic cofactor sidecar vs experimental atlas | `robust_l2` | 45 | 0.822222 | 0.844444 | 0.850723 | No model was trained for this surface; robust_l2 scaling was fit on candidate in-distribution vectors only. |
| Predicted geometry score query plus selected organic cofactor sidecar vs experimental atlas | `cosine` | 39 | 0.897436 | 0.923077 | 0.91485 | No model was trained for this surface; robust_l2 scaling was fit on candidate in-distribution vectors only. |
| Predicted geometry score query plus selected organic cofactor sidecar vs experimental atlas | `robust_l2` | 39 | 0.897436 | 0.897436 | 0.90385 | No model was trained for this surface; robust_l2 scaling was fit on candidate in-distribution vectors only. |

## Headline Delta

- Cosine family top3 any rate changed from 0.8 to 0.866667 (delta 0.066667).
- Non-tuning-adjacent augmented cosine family top3 any rate: 0.923077.

## Next Gate

Use this artifact as the current cofactor-augmented D11 rerun. The row-level cofactor sidecar blocker is no longer blocking D11 iteration.
