# Search candidate bond and charge changes

The offline `atlas-candidate-events` command searches literal chemical edits
in the twelve unreviewed candidates accepted by the
[opaque-context extractor](ATLAS_OPAQUE_CONTEXT.md). It answers a bounded
question: which retained adjacent drawings contain these proposed changes?

```bash
# Both transketolase candidates: mechanism 1, Steps 2→3 and 4→5.
catalytic-earth atlas-candidate-events --bond C C 0 1

# Only Step 2→3 also changes a carbon formal charge from -1 to 0.
catalytic-earth atlas-candidate-events --bond C C 0 1 --charge C -1 0

# No candidate contains both changes, although separate candidates contain each.
catalytic-earth atlas-candidate-events --bond C C 0 1 --bond S H 1 0

# Inspect proposals supported only by the before-panel source arrow.
catalytic-earth atlas-candidate-events --bond O H 0 1 --support source_arrow_only

# List the retained candidates and eligible edits for one source record.
catalytic-earth atlas-candidate-events --mcsa-id M0219
```

Bond clauses specify two exact element symbols and integer before/after bond
orders; zero means no bond. Charge clauses specify one element and exact
integer formal charges. The supported ordinary bond orders are 1, 2 and 3.
Bond endpoint order is irrelevant, so `O H` and `H O` match the same edit.
No atom roles, isotope equivalences, wildcard matching, ChEBI identities or
stereochemical/coordination interpretations are inferred.

Every clause must match inside one candidate. Different clauses may match
different source arrows and different atoms; their conjunction does not assert
a shared atom or concerted event. Repeating an identical clause does not require
multiple occurrences. Distinct edit witnesses with the same signature remain
separate, including the two O–H addition proposals in M0212 Step 15→16.

The default `--support after_graph_confirmed` requires every matching edit to
have support from the mapped after-graph as well as a source arrow. Use
`--support source_arrow_only` for edits whose after-graph evidence is absent,
or `--support any` to search both classes. The support filter applies to each
matching witness; it does not upgrade the other edits in a returned candidate.
Without change clauses, the query lists candidates with at least one edit of
the requested support class. `--output` creates a new JSON file and refuses to
overwrite an existing file.

## Evidence carried with each match

The catalog contains 43 source-flow bindings and 86 edits across twelve
candidates: 65 after-graph-confirmed and 21 arrow-only. These are source-drawing
objects, not counts of distinct catalytic mechanisms or validated reactions.
The source inventory still has 101 adjacent pairs; 89 remain outside this
catalog. The two M0222 pairs withheld by context mode are excluded.

Each selected row retains its complete candidate, original snapshot/panel
hashes, local atom references, correspondence, graph coverage, source-flow
witnesses, opaque annotations and scope flags. A candidate hash binds those
bytes to the frozen context scan. Literal signatures omit local atom IDs for
retrieval, while witnesses retain them for inspection.

Each row also carries source context from the matching record and mechanism
proposal in a hashed source-draft bundle: source scope, mandatory abstentions,
and exact before/after step summaries, inference flags and panel hashes.
M0106 Step 8→9 therefore exposes the source's inferred-return status, while
M0219 retains the proposal-specific reaction and protein-applicability limits.
No event or step witness from another proposal is joined into a match;
record-level scope may describe conflicts between proposals.
Terminal-state panels absent from the compiled step list are identified as
original M-CSA terminal states; their inference status remains unknown rather
than being supplied from a neighboring step.

Graph confirmation is narrower than scientific confirmation. Source-inferred
steps remain inferred. Lone-pair states, omitted proton inventories, metal
electronic states, complete pathways, exact protein applicability and physical
atom identity remain outside the claim. Matching edits do not establish
mechanism equivalence. An empty result means no matching retained candidate;
it does not establish the absence of that chemistry.

## Reproduction

```bash
python scripts/build_atlas_candidate_events.py --check
python scripts/run_test_tier.py core/unit
python scripts/validate_repository_contracts.py
```

The builder reproduces the frozen context scan, binds the source registry and
implementation hashes, verifies every accepted candidate hash, and derives the
packaged event rows. Package loading checks the catalog and attribution hashes;
validation rederives event rows from the retained candidates. Installed queries
require neither the checkout nor raw source snapshots, network access or RDKit.
The reviewed transformation catalog, source extractors and earlier scan reports
remain unchanged. See the [coordination board](../work/coordination_candidate_events.md)
for the computational review and its limits.
