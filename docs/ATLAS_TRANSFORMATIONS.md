# Computable source-state transformations

Two reviewed source-depiction transitions use the shared graph-edit engine.
M0187 mandelate racemase connects an official R-mandelate structure to a
depicted intermediate. M0173 trypsin forms a depicted enzyme–substrate
covalent bond, retaining generic peptide groups without asserting an exact
canonical peptide. Each set supplies before/after graphs and executable edits
with its own review and source bindings.

```sh
catalytic-earth atlas-transformations --mcsa-id M0187
catalytic-earth atlas-transformations --mcsa-id M0173
catalytic-earth atlas-transformations --all
```

The query runs offline with the dependency-free installed package. It returns
the complete selected transformation and its limits. With no options, the
command reproduces the original M0187 query. `--all` queries each reviewed
set separately and retains both results and their provenance; it accepts
`--mcsa-id` to filter the catalog. An empty result means no matching reviewed
transition is packaged, not absence of the chemistry.

## M0187: substrate to intermediate

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

## M0173: enzyme–substrate covalent addition

M0173 mechanism 1, Step 1, depicts His56 deprotonating Ser195 while the
serine oxygen attacks the substrate carbonyl carbon. The next input panel
contains the proposed tetrahedral oxyanion intermediate. Three source arrows
support four bond edits and two charge changes:

| Change | Source-panel nodes |
| --- | --- |
| Transfer the serine proton to histidine | break a44–a50; form a21–a50 |
| Form the enzyme–substrate covalent bond | add a44–a3 |
| Convert the carbonyl to an oxyanion | a3–a10: double → single; a10: 0 → −1 |
| Update histidine charge | a21: 0 → +1 |

Replay preserves all 50 depiction nodes, changes 42 bonds to 43, and merges
the substrate and serine fragments. Those nodes include two literal R-group
pseudoatoms and carbon tokens used as generic or residue-fragment placeholders.
The context preserves the source's labels and aliases, including disconnected
fragments with the same Ser195 label. These are not 50 resolved physical atoms
or a reconstructed protein. His56 is the source-panel numbering; no sequence
or structure atom mapping is added.

Both panels lack bond-stereochemistry assignments. The product of this
depicted addition has no asserted absolute configuration. Bond IDs and flow
IDs can be reused for different endpoints in later panels, so evidence binds
the step and endpoints. The atom-token alignment is project-reviewed source
continuity, not an upstream atom map or proof of unique physical atom identity.

This separately versioned source-only set carries no canonical participant
bridge or inferred phenyl-symmetry mappings. Its scope ends at the depicted
intermediate, before peptide cleavage or the complete catalytic cycle.

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

M0173 has a separate [reviewed input](../data/atlas/transformations/m0173/transformations.json),
[source inventory](../data/atlas/transformations/m0173/source_inventory.json),
and [attribution](../data/atlas/transformations/m0173/SOURCE_ATTRIBUTION.md).
Its audit parses the retained MRV directly using the standard library:

```sh
python data/atlas/transformations/m0173/audit_m0173.py --check
python scripts/build_atlas_transformations.py --check
```

The source audit derives both graphs and checks the six reviewed edits against
the original source arrows and after graph. The package builder validates
each set separately. New downloads, chemical toolkit installation and merged
review claims are not required to reproduce this addition.

## Scope

M0187 Steps 3 and 4 omit mandelate, so there is no depicted S-product graph to
verify. This result establishes a replayable source-depiction transition. It
does not establish a complete racemization path, net-reaction atom map,
Step-2 product stereochemistry, inferred enzyme-return step, or observed
turnover. Source drawings and computed matches remain mechanistic evidence
at their declared scope; the correlated agent review does not constitute
independent human validation. Existing Atlas-10 results and benchmark labels
are unchanged.
