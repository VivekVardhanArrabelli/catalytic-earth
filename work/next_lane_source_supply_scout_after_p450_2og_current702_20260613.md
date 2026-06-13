# Next-lane source-supply scout after P450 + 2OG applies

Run: 2026-06-13T00:33:32Z

Non-destructive live UniProt scout for remaining named 10k-path lanes. No registry write, no labels emitted.

| rank | family | reviewed supply | distinct full ECs / 200 | cap | reaction-poor warning |
| --- | --- | ---: | ---: | ---: | --- |
| 1 | `coa_acyltransferase` | 7728 | 82 | 250 | False |
| 2 | `cofactor_independent_isomerase` | 5273 | 51 | 250 | True |
| 3 | `molybdopterin_oxidoreductase` | 460 | 33 | 250 | True |
| 4 | `copper_oxidoreductase` | 222 | 12 | 250 | True |

## Recommendation

- Next lane: `coa_acyltransferase`.
- Rationale: it is floor-reachable, has the strongest current reviewed supply and EC diversity among the remaining named lanes, and should be wired as a new fingerprint universe change with scope-only EC and mechanism corroborators kept in excluded_context.
