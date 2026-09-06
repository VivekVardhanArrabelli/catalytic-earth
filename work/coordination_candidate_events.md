# Candidate event search board

Base: `ac4bb82105b9f5710eb9a8246ec8af13a74c825f` (PR #49), 2026-09-06.

## Objective and division of work

Make the twelve context-accepted, unreviewed candidates searchable by literal
element-aware bond/order and formal-charge changes. Both source and review
agents independently selected this over more representation ingestion because
it makes existing chemical evidence retrievable.

| Owner | Responsibility |
| --- | --- |
| Root | Query CLI, installed-wheel checks, integration tests, docs and publication |
| state_contracts | New candidate-event catalog derivation, validation and query module |
| source_ingestion | Reproducible builder, package assets, direct source-event audit |
| draft_integration_review | Independent adversarial tests and schema challenge |

Agents coordinate here and through direct messages. File ownership keeps edits
separate. All reviews are informed same-model computational checks, with
potentially correlated errors; no human-equivalence claim is made.

## Contract and decisive checks

Package exactly the twelve accepted context-mode payloads, content-bound to the
frozen 101-pair scan and original source bytes. Retain complete candidates,
scope, coverage, source flow witnesses and opaque context. Default matching uses
after-graph-confirmed edits; arrow-only support is explicitly selectable.

Exact bond and charge clauses are ANDed within one candidate. Undirected bond
endpoint elements are normalized; atom IDs and row ordering do not define a
signature. Duplicate clauses use set semantics. A conjunction does not imply
shared atoms, a shared source arrow, or mechanism equivalence.

Acceptance queries: C–C addition 0→1 returns M0219 mechanism 1 Steps 2→3 and
4→5; additionally requiring C charge −1→0 selects only 2→3. C–C addition plus
S–H removal must return nothing, despite separate candidates containing those
events. Renaming local IDs and reordering rows preserves semantic results;
changing chemical element/order/charge values must affect the corresponding
query. Tampered or stale catalog bytes must fail validation.

No inferred atom roles, ChEBI equivalence, stereochemical or coordination
interpretation, physical atom mapping, benchmark rescoring, reviewed-tier
promotion, or experimental validation. Empty results mean no matching retained
candidate. Frozen extraction algorithms and all earlier evidence stay pinned.

## Source and review findings

Root identified that generic candidate scope flags do not expose specific
source-inferred or protein-applicability limits. Source confirmed and bound
exact record/proposal context, mandatory abstentions and before/after step
witnesses from the three compiled source-draft bundles. M0106 Step 8 remains
explicitly inferred. Three terminal after-panels absent from those bundles are
identified from the original snapshot with unknown inference status.

Reviewer identified two distinct M0212 Step 15→16 O–H addition arrows sharing
one element/order signature. Repeated query clauses may be deduplicated, but
distinct source-edit witnesses must survive. Query conjunctions remain scoped
to one candidate, without implying shared atoms or a single concerted event.

The reviewer added nine decisive tests. They pass source-derived totals and
queries, support filtering and duplicate witnesses, same-record false joins,
atom-ID/row-order invariance, element/order/charge sensitivity, deep-copy
isolation, invalid filter types, stale catalogs, scope promotion and source
context false joins. Three CLI integration tests also pass. Root fixed invalid
filter reporting to use the retained parser; state restricted query symbols to
real elements and enforced inherited scope flags. The frozen module SHA256 is
`688a9a5ad9afb766f08a66080cf0b940581ab198b88cde349ae6526b5d33f7db`.

## Publication gate

Run focused query/integration tests, core tests, repository contracts, exact
catalog and scan reproduction, and fresh installed-wheel queries with network
blocked and RDKit absent. Merge only after all four CI jobs pass.

## Final local result

All 415 core tests and repository contracts passed. Fresh-wheel queries passed
from an empty directory with network connections blocked and RDKit absent,
including the 2/1/0 conjunction cases, support separation, source-inferred step
context and retained extraction regressions. Atlas-10 keeps runtime hash
`57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.

Independent source/context audit agrees with twelve candidates, 86 edit events
(65 graph-confirmed, 21 arrow-only), 43 source-flow bindings and five records.
The final catalog SHA256 is
`682e6f1a6d30f5328c2efcd3c8f85d661ffb068ef5ed3e31b2aac3f7bd3726e0`.
Builder reproduction passes. Earlier source packages, extraction algorithms,
scans, reviewed transformations, benchmark labels and historical release
manifest retain their original bytes. Four-job CI remains the publication gate.
