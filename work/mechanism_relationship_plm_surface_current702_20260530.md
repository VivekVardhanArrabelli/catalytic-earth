# D11 Mechanism Relationship PLM Surface

Run: 2026-05-30T21:02:04Z

D11 hygiene-tier relationship faithfulness: add a real PLM sequence surface alongside the k-mer control under one identical rank-based pipeline. Comparative claim only.

## Relationship Rank Metrics (robust_cosine)

| Surface | Queries | Exact top1 | Family top3 any | Family MRR | Cofactor top3 any |
| --- | ---: | ---: | ---: | ---: | ---: |
| ESM2-150M whole-sequence pooled embedding (real PLM) | 48 | 0.4375 | 0.8125 | 0.713581 | 0.8125 |
| Deterministic sequence k-mer control vector | 48 | 0.333333 | 0.708333 | 0.563161 | 0.708333 |

## PLM vs k-mer

- Verdict: `plm_organizes_relationship_space_better`.
- PLM-better metrics: 24; PLM-worse: 0.

## Real D11 pass

- Status: `blocked_missing_row_level_cofactor_channel_scores`.
- This adds a sequence-PLM hygiene surface. The real D11 pass still requires row-level selected organic-cofactor scores (flavin/heme/PLP) and a cofactor-augmented predicted-geometry query representation.
