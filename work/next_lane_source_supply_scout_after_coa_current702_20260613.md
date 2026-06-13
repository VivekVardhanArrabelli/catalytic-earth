# Next-lane source-supply scout after CoA apply

Run: 2026-06-13T01:19:02Z

Non-destructive live UniProt scout after the CoA acyltransferase 18fp apply. No registry write, no labels emitted.

## Candidate summary

| candidate | reviewed supply | distinct full ECs in 200-row sample | reaction-poor warning | top ECs |
| --- | ---: | ---: | --- | --- |
| `molybdopterin_oxidoreductase` | 460 | 33 | True | 1.9.6.1 (107), 1.17.1.4 (11), 1.2.3.1 (11), 1.17.3.2 (6), 1.7.1.1 (6) |
| `copper_oxidoreductase` | 222 | 12 | True | 1.10.3.2 (79), 1.4.3.21 (29), 1.4.3.13 (26), 1.10.3.1 (15), 1.4.3.22 (6) |
| `cofactor_independent_isomerase` | 5273 | 51 | False | 5.3.4.1 (47), 5.3.3.8 (25), 4.2.1.17 (16), 5.3.99.3 (12), 1.1.1.35 (12) |

## Recommendation

- Recommended next lane: `cofactor_independent_isomerase`.
- Rationale: rank favors floor-reachable supply with higher sampled EC diversity and no/reduced reaction-poor warning; final admission still needs mechanism-first handles and a fresh preview.
- Exact next action: add fingerprint spec + ontology node, wire mechanism corroborators and guards, re-freeze OOS preregistration to 19fp, add offline leakage/trust-tier tests, preview, then apply only if novelty/governor/dedup/trust-tier gates pass.
