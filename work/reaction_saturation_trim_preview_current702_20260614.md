# Reaction-Saturation Trim (non-destructive preview)

Run: 2026-06-14T03:31:59Z

Backward cleanup of the lowest-quality organic growth: families that grew deep on organism/sequence breadth but NOT reaction/mechanism diversity. Trims each reaction-saturated family down to its reaction-aware cap (`clamp(rate * distinct_reactions, floor, ceiling)`, rate 8, floor 100, ceiling 250) by keeping a reaction- and sequence-diverse subset. PREVIEW ONLY -- writes no registry; the frozen 702 benchmark is never touched.

- Families trimmed: 9; rows demoted: 429; expansion 7363 -> 6934; combined 8065 -> 7636.
- Near-saturated held (over reaction-aware cap but below ratio 10.0): 3.

## Selection

- diversity-ranked: >=1 row per distinct reaction first (reaction diversity fully preserved), then maximize organism/length/cluster spread via the (fingerprint, full-EC, organism, length-bin) near-dup proxy; near-duplicate orthologs demoted first. Never recency-ranked. Local mmseqs sequence clustering is the stronger dedup when available.

## Per-family keep / demote

| family | current | distinct rxn | labels/rxn now | reaction-aware cap | kept | demoted | labels/rxn after | rxn diversity preserved |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| askha_sugar_acetate_kinase | 150 | 9 | 16.67 | 100 | 100 | 50 | 11.11 | True |
| biotin_dependent_carboxylase | 150 | 8 | 18.75 | 100 | 100 | 50 | 12.5 | True |
| deoxynucleoside_kinase | 150 | 7 | 21.43 | 100 | 100 | 50 | 14.29 | True |
| ghmp_small_molecule_kinase | 150 | 4 | 37.5 | 100 | 100 | 50 | 25.0 | True |
| manganese_iron_superoxide_dismutase | 166 | 1 | 166.0 | 100 | 100 | 66 | 100.0 | True |
| nucleoside_diphosphate_kinase | 150 | 10 | 15.0 | 100 | 100 | 50 | 10.0 | True |
| pfka_phosphofructokinase | 150 | 2 | 75.0 | 100 | 100 | 50 | 50.0 | True |
| protein_kinase_ser_thr_tyr | 150 | 10 | 15.0 | 100 | 100 | 50 | 10.0 | True |
| zinc_lyase_hydratase | 113 | 6 | 18.83 | 100 | 100 | 13 | 16.67 | True |

### Near-saturated (over reaction-aware cap, below ratio threshold -- not trimmed)

| family | current | distinct rxn | labels/rxn | reaction-aware cap |
| --- | --- | --- | --- | --- |
| cobalamin_radical_rearrangement | 141 | 15 | 9.4 | 120 |
| pfkb_ribokinase_family | 150 | 16 | 9.38 | 128 |
| radical_sam_enzyme | 213 | 23 | 9.26 | 184 |

## Projected diversity (combined per-fingerprint)

- Fingerprint Gini: 0.1352 -> 0.1874.
- Normalized entropy: 0.99 -> 0.9836.
- Note: Fingerprint Gini measures COUNT evenness, not mechanism diversity. It rises after the trim BY DESIGN: single-reaction families are bounded to the floor while reaction-rich families keep their earned depth, so label depth becomes proportional to reaction diversity (the goal). The true quality metric is labels-per-distinct-reaction, which drops to the reaction-aware cap in every trimmed family (see projected_labels_per_distinct_reaction per family).

## Separate honest counters (before -> after; never merged)

- positive_bronze_count: 6352 -> 5923.
- oos_bronze_count: 1696 -> 1696.
- silver_ready_count: 0 -> 0.
- silver_confirmed_count: 17 -> 17.
- projected_provisional_count: 0 -> 0.

## Guardrails

- Frozen benchmark written: False.
- Expansion registry written: False.
- Demoted rows are bronze, never frozen; demotion is a diversity-quality lever, not reconstruction.
- Metadata-only: no network, no mmseqs, no embeddings.
