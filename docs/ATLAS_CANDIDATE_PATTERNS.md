# Match changes on the same depicted atom

`atlas-candidate-patterns` searches the existing twelve unreviewed candidates
using named before-panel source atoms. Reusing a variable requires edits to
involve the same depicted atom. It adds no source candidates or evidence tiers.

```bash
# C-C addition and a charge change on that same carbon:
# M0219 mechanism 1 Step 2→3, x=a10 and y=a28.
catalytic-earth atlas-candidate-patterns --bond C:x C:y 0 1 --charge C:x -1 0

# No match: the carbonyl carbon and charge-changing carbon are different nodes.
catalytic-earth atlas-candidate-patterns --bond C:x O:y 2 1 --charge C:x -1 0

# Two candidates, four assignments: both orientations of each symmetric C-C edit.
catalytic-earth atlas-candidate-patterns --bond C:x C:y 0 1

# Two O-H addition assignments in one nitrogenase source panel, both arrow-only.
catalytic-earth atlas-candidate-patterns --bond O:x H:y 0 1 --support source_arrow_only --mcsa-id M0212
```

The [event query](ATLAS_CANDIDATE_EVENTS.md) intentionally permits different
clauses to match different atoms in one candidate. For example, C–O order 2→1
and carbon charge −1→0 occur together in M0219 Step 2→3. The bond uses source
nodes a28–a29, while the charge changes at a10. The second pattern above rejects
that combination because `x` must identify the same carbon in both clauses.
The first pattern matches bond a10–a28 and the charge change at a10.

## Query semantics

- Write atoms as `ELEMENT:VARIABLE`, using exact element symbols and variable
  names of 1–32 ASCII letters, digits or underscores, beginning with a letter.
- A variable always has one element. Reusing its name binds the same
  before-panel source node; different names must bind distinct nodes.
- Bond endpoints are undirected. Element and variable stay paired when
  endpoints are reversed. Both element-compatible orientations are considered.
- Every clause must match within one candidate. No variable joins across
  candidates, source steps or mechanism proposals.
- Repeating an identical clause does not require another occurrence. Distinct
  edit/flow witnesses are retained even when they share a signature or assignment.
- Support filtering occurs before joining. The default is
  `after_graph_confirmed`; `source_arrow_only` and `any` are explicit options.
  A matching pattern does not upgrade any other edit's support.

`candidate_count` counts selected adjacent-panel candidates. `binding_count`
counts variable assignments. Symmetry can increase the latter without adding
evidence or distinct reactions. Each match includes its complete candidate row,
source context, original hashes, scope and coverage; each assignment identifies
the exact edit and source-flow witnesses for every clause.

At least one clause is required. Queries allow up to eight distinct clauses
and twelve variables. Search is bounded to 100,000 option/join work units; an
exhausted budget raises an error and returns no partial answer. `--output`
creates a new JSON file and refuses to overwrite one that already exists.

Variables describe source drawings. They do not establish physical atom
identity, canonical participants, a concerted event, mechanism equivalence or
experimental validation. Source-inferred steps, unknown terminal-state
inference status, protein-applicability limits and all other candidate
abstentions remain visible. An empty result means no matching retained pattern,
not absence of the chemistry.

## Reproduction

```bash
python scripts/build_atlas_candidate_events.py --check
python scripts/run_test_tier.py core/unit
python scripts/validate_repository_contracts.py
```

This query validates and reads the existing catalog without regenerating it.
Its SHA256 remains
`682e6f1a6d30f5328c2efcd3c8f85d661ffb068ef5ed3e31b2aac3f7bd3726e0`.
The previous event query implementation, builder, catalog and extraction
algorithms keep their original bytes. Fresh-wheel checks exercise the shared-atom positive,
disjoint negative, symmetric assignments and arrow-only witnesses with network
connections blocked and RDKit absent. The [coordination board](../work/coordination_candidate_patterns.md)
records the computational review and its limits.
