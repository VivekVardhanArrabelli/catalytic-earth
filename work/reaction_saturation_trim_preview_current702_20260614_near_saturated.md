# Reaction-Saturation Trim (non-destructive preview)

Run: 2026-06-14T07:13:23Z

Backward cleanup of the lowest-quality organic growth: families that grew deep on organism/sequence breadth but NOT reaction/mechanism diversity. Trims each reaction-saturated family down to its reaction-aware cap (`clamp(rate * distinct_reactions, floor, ceiling)`, rate 8, floor 100, ceiling 250) by keeping a reaction- and sequence-diverse subset. PREVIEW ONLY -- writes no registry; the frozen 702 benchmark is never touched.

- Families trimmed: 3; rows demoted: 72; expansion 6934 -> 6862; combined 7636 -> 7564.
- Near-saturated held (over reaction-aware cap but below ratio 9.0): 0.

## Selection

- diversity-ranked: >=1 row per distinct reaction first (reaction diversity fully preserved), then maximize organism/length/cluster spread via the (fingerprint, full-EC, organism, length-bin) near-dup proxy; near-duplicate orthologs demoted first. Never recency-ranked. Local mmseqs sequence clustering is the stronger dedup when available.

## Per-family keep / demote

| family | current | distinct rxn | labels/rxn now | reaction-aware cap | kept | demoted | labels/rxn after | rxn diversity preserved |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cobalamin_radical_rearrangement | 141 | 15 | 9.4 | 120 | 120 | 21 | 8.0 | True |
| pfkb_ribokinase_family | 150 | 16 | 9.38 | 128 | 128 | 22 | 8.0 | True |
| radical_sam_enzyme | 213 | 23 | 9.26 | 184 | 184 | 29 | 8.0 | True |

## Projected diversity (combined per-fingerprint)

- Fingerprint Gini: 0.1874 -> 0.1891.
- Normalized entropy: 0.9836 -> 0.9833.
- Note: Fingerprint Gini measures COUNT evenness, not mechanism diversity. It rises after the trim BY DESIGN: single-reaction families are bounded to the floor while reaction-rich families keep their earned depth, so label depth becomes proportional to reaction diversity (the goal). The true quality metric is labels-per-distinct-reaction, which drops to the reaction-aware cap in every trimmed family (see projected_labels_per_distinct_reaction per family).

## Separate honest counters (before -> after; never merged)

- positive_bronze_count: 5923 -> 5851.
- oos_bronze_count: 1696 -> 1696.
- silver_ready_count: 0 -> 0.
- silver_confirmed_count: 17 -> 17.
- projected_provisional_count: 0 -> 0.

## Guardrails

- Frozen benchmark written: False.
- Expansion registry written: False.
- Demoted rows are bronze, never frozen; demotion is a diversity-quality lever, not reconstruction.
- Metadata-only: no network, no mmseqs, no embeddings.
