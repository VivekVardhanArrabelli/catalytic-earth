# Computable source-state transformations

M0187 mandelate racemase now has one executable transformation: the depicted
input of mechanism 1, Step 1, to the depicted intermediate entering Step 2.
It connects an official R-mandelate structure to source-panel atom locators
and supplies before/after covalent graphs plus explicit graph edits.

```sh
catalytic-earth atlas-transformations --mcsa-id M0187
```

The query runs offline with the dependency-free installed package. It returns
the complete transformation, source bindings, two symmetry-equivalent ligand
mappings, and the limits on what that transformation establishes. A query for
another M-CSA identifier returns an empty result; that means no reviewed
transformation is packaged for that identifier.

## The chemical result

The retained Step-1 graph matches R-mandelate (CHEBI:32382) with chirality
enabled. The raw source label says CHEBI:17756, which is S-mandelate and does
not match. The query preserves this conflict. Rhea master RHEA:13945 is
undirected; its record-level M-CSA cross-reference points to a directional
child opposite the proposal's stated R-to-S direction. That cross-reference
does not assign direction to the mechanism steps.

Four Step-1 arrows account for six bond edits and two formal-charge changes:

| Change | Source-panel atoms |
| --- | --- |
| Transfer the alpha hydrogen to His297 | break a9–a66; form a58–a66 |
| Form the intermediate C=C bond | a8–a9: single → double |
| Change the carbonyl bond | a8–a10: double → single |
| Transfer the Glu317 proton to the ligand oxygen | break a63–a65; form a10–a65 |
| Update the proton donor and acceptor charges | Glu317 a63: 0 → −1; His297 a58: 0 → +1 |

The ligand stays at net charge −1. Its alpha carbon changes from R
tetrahedral to sp2, losing that tetrahedral stereocenter. This does not claim
the absence of other geometric stereochemistry in the intermediate.

`apply_graph_edits(graph, edits)` executes the bond, charge and specified
stereochemistry edits. `replay_graph_edits(before, edits, after, atom_map)` checks that
the edited chemical projection equals the retained after graph. Component
membership is excluded from the chemical graph, and graph identifiers remain
panel context. The replay covers the ligand, His297 and Glu317. Metal coordinate
bonds and spectators are excluded explicitly; this is not a claim that the
ligand is physiologically free. Lys166 hydrogen a67 becomes explicit only in
Step 2 and is outside the replay, rather than an asserted newly created atom.

Atom IDs are local depiction locators, not physical atom identities or PDB
atom names. The reviewed Step-1/Step-2 locator alignment and computed graph
matches have separate provenance. Both phenyl orientations are retained at
the ligand topology level. Only one orientation preserves the exact depicted
Kekule bond orders; the second is not a second literal raw-graph replay.

## Evidence and reproduction

The [reviewed input](../data/atlas/transformations/m0187/transformations.json)
binds the retained M-CSA panels, official participant MOL files, the
[source inventory](../data/atlas/transformations/m0187/source_inventory.json)
and a computational audit. RDKit is required only to reproduce that optional
audit, using version 2025.03.3 (distribution `rdkit==2025.3.3`):

```sh
python data/atlas/transformations/m0187/audit_m0187.py
python scripts/build_atlas_transformations.py --check
python scripts/run_test_tier.py core/unit
```

The first command regenerates the audit from retained local source files;
the package builder checks its reviewed hash. Audit regeneration does not
approve changed scientific claims. The package builder uses the standard
library and retained sources. The installed runtime needs neither RDKit nor
raw MOL files, source acquisition or network access.
Source rights and transformations are recorded in the
[attribution](../data/atlas/transformations/m0187/SOURCE_ATTRIBUTION.md).

## Scope

Steps 3 and 4 omit mandelate, so there is no depicted S-product graph to
verify. This result establishes a replayable source-depiction transition. It
does not establish a complete racemization path, net-reaction atom map,
Step-2 product stereochemistry, inferred enzyme-return step, or observed
turnover. Source drawings and computed matches remain mechanistic evidence
at their declared scope; the correlated agent review does not constitute
independent human validation. Existing Atlas-10 results and benchmark labels
are unchanged.
