# D11 Mechanism Relationship Evaluation Cofactor Augmented

Run created: `2026-05-31T00:57:13Z`

## Decision

The row-level sidecar blocker is cleared for a bounded D11 rerun. This artifact evaluates a cofactor-augmented predicted-geometry query representation using fixed persisted sidecar scores, without refitting models or tuning thresholds on heldout rows.

No labels, registries, ontologies, imports, production scoring, global thresholds, heldout splits, or model weights were changed.

## Sidecar Gate

- Row-class records: 2106.
- Entries with flavin/heme/PLP scores: 702.
- Source counts: {'trained:esm2_t30_150m_existing_track': 2106}.
- Caveat: Organic cofactor scores are the documented ESM2-150M fallback source, not a strict reproduction of the missing original t6/t12 selected heads.

## Relationship Rank Metrics

| Surface | Variant | Queries | Exact top1 | Family top3 any | Family MRR | Notes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Predicted geometry score query vs experimental atlas score vector rerun | `cosine` | 45 | 0.666667 | 0.8 | 0.756312 | No model was trained for this surface; robust_l2 scaling was fit on candidate in-distribution vectors only. |
| Predicted geometry score query vs experimental atlas score vector rerun | `robust_l2` | 45 | 0.622222 | 0.688889 | 0.676188 | No model was trained for this surface; robust_l2 scaling was fit on candidate in-distribution vectors only. |
| Predicted geometry score query plus selected organic cofactor sidecar vs experimental atlas | `cosine` | 45 | 0.822222 | 0.866667 | 0.859739 | No model was trained for this surface; robust_l2 scaling was fit on candidate in-distribution vectors only. |
| Predicted geometry score query plus selected organic cofactor sidecar vs experimental atlas | `robust_l2` | 45 | 0.777778 | 0.844444 | 0.828889 | No model was trained for this surface; robust_l2 scaling was fit on candidate in-distribution vectors only. |
| Predicted geometry score query plus selected organic cofactor sidecar vs experimental atlas | `cosine` | 39 | 0.923077 | 0.948718 | 0.938197 | No model was trained for this surface; robust_l2 scaling was fit on candidate in-distribution vectors only. |
| Predicted geometry score query plus selected organic cofactor sidecar vs experimental atlas | `robust_l2` | 39 | 0.846154 | 0.897436 | 0.877558 | No model was trained for this surface; robust_l2 scaling was fit on candidate in-distribution vectors only. |

## Headline Delta

- Cosine family top3 any rate changed from 0.8 to 0.866667 (delta 0.066667).
- Non-tuning-adjacent augmented cosine family top3 any rate: 0.948718.

## Next Gate

Use this artifact as the first cofactor-augmented D11 rerun. A stricter reproduction still requires the original t6/t12 sidecars, but the row-level blocker is no longer blocking D11 iteration.
