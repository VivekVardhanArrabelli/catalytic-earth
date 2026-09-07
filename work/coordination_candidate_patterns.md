# Candidate atom-pattern query board

Base: `c1b2ccb5902fa26e71fb53ea7473a1d7fc561906` (PR #50), 2026-09-07.

## Objective and owners

Add an opt-in query requiring multiple edits to involve the same named
before-panel source node. Existing event queries and the packaged catalog stay
byte-identical. No source ingestion or evidence promotion is part of this work.

| Owner | Responsibility |
| --- | --- |
| Root | CLI, installed-wheel checks, integration tests, docs and publication |
| state_contracts | New atom-pattern query module only |
| draft_integration_review | Independent adversarial tests and contract challenge |
| source_ingestion | Direct retained-source witness audit and query examples |

Agents coordinate here and by direct messages. Reviews use the same model
family and can share errors; they are not independent human review.

## Contract and acceptance

`atlas-candidate-patterns --bond C:x C:y 0 1 --charge C:x -1 0` requires the
bond and charge edits to share carbon `x`. Variables identify before-panel
source nodes only. Different variable names require different nodes. Every
clause must match inside one candidate; support filtering precedes joining.
Bond endpoints are undirected; symmetric orientations and distinct source edit
witnesses remain explicit. Repeated identical clauses use set semantics.

Negative control: C:x–O:y order 2→1 plus charge C:x −1→0 must return zero.
The existing event query returns M0219 mechanism 1 Step 2→3, whose bond uses
a28–a29 while the charge uses a10. Positive control: C:x–C:y addition 0→1
plus charge C:x −1→0 returns that step with x=a10 and y=a28.

Renaming atom IDs and reversing bond endpoints preserves semantic matches.
No variables cross candidates, steps or proposals. Unshared changes remain
searchable through the unchanged event command. No physical/canonical atom
identity, mechanism equivalence, concerted event, stereochemical or coordination
interpretation, or experimental validation is inferred.

## Focused review

Eight adversarial tests and three CLI integration tests pass. They cover the
positive and disjoint-negative controls, symmetric and reversed endpoints,
distinct-variable constraints, candidate/proposal isolation, support-before-join,
two M0212 arrow-only witnesses, atom-ID/row-order invariance, deep-copy isolation,
malformed inputs and hard failure after the finite search budget is exhausted.
The module is frozen at SHA256
`55d90f1655deec702241707493eff1e7c4951d27ceb8a343b62f17cc5c59814f`.

Independent raw-XML inspection confirms the M0219 negative/positive distinction:
o55 changes a28–a29, while o60 adds a10–a28 and changes charge at a10. The two
C–C additions produce four source-variable orientations. M0212 arrows o51 and
o53 add a33–a84 and a32–a81; the terminal panel omits both hydrogen nodes, so
their support remains arrow-only. Distinct carbon variables cannot both reuse
the single a10 charge change. M0106 events from different steps cannot join.
The audit preserves lone-pair/electronic-state limitations and M0219's
proposal/protein/metal applicability abstentions.

All 426 core tests and repository contracts pass. The event catalog still
reproduces byte-for-byte; reviewed records, old source extractors and the
historical release manifest remain unchanged.

Fresh-wheel checks also pass from an empty directory with network connections
blocked and RDKit absent, including positive/negative atom joins, four symmetric
assignments, two arrow-only assignments and the existing extraction/query
regressions. Atlas-10 retains runtime hash
`57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.

## Publication gate

Run focused challenge/integration checks, core tests, repository contracts,
frozen catalog reproduction and fresh-wheel offline queries with network
blocked and RDKit absent. Merge only after all four CI jobs pass.
