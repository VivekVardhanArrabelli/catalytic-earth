# Source-scoped deposit context

The retained 3CSM structure supplies a useful M0081 template limitation: its
bound ligand is a deposited bicyclic inhibitor, and its P32178 reference
link includes unresolved sequence conflicts. It does not supply a deposited
chorismate reaction state. This is one new source annotation of an existing
panel candidate, with zero new compiled mechanisms, protein records or
experimental observations (CE-023).

## What 3CSM actually contains

The [data specification](../data/atlas/deposit_context/m0081/spec.json) selects
source rows and ten coordinate distances without inferring a chemical
identity from the three-letter ligand code:

| Context | Retained evidence | Transfer limit |
| --- | --- | --- |
| Inhibitor | TSA at label chains D/F, author A/B residue 400; the title identifies an endooxabicyclic inhibitor and the keywords say TRANSITION STATE ANALOG | No chorismate, prephenate or transition-state atom mapping |
| Component definition | C10 H12 O6; all 28 atom and 29 bond rows, including stereochemical tokens | Definition hydrogens and bond orders are not observations of the bound protonation state |
| Regulatory ligand | TRP at label chains C/E, author A/B residue 300; source entity details identify a regulatory site | Keep separate from TSA and polymer tryptophan residues |
| Reference sequence | A/B each align to P32178 positions 1–256; positions 218–221 declare ERRI versus reference NESG, all unmodeled in both chains | The source calls these conflicts; the coordinates cannot resolve the sequence and no engineered variant or cause is established |
| Experimental context | X-ray model; reported high-resolution limit 3.0 Å; crystal-growth pH 8.0 | No hydrogen-position, protonation, kinetic or solution-population claim |
| Assembly | Author-defined assembly 1 uses identity operator 1 and A,B,C,D,E,F; two PISA alternatives remain visible | Only the declared assembly 1 coordinates are projected; solution assembly is not independently validated |

The source also retains `BAR` as the author monomer name in the TSA nonpolymer
scheme, while its coordinate atom rows use TSA. Exact namespaces remain in
the output; the code does not treat those strings as a substrate identity.
The archive snapshot's latest internal revision is 2024-05-22. This work does
not assert that it is the latest deposit or the exact model analyzed in the
1997 primary paper. The paper's citation is retained; its body was not inspected.

The selected inhibitor neighborhood is reproducible but has a narrow meaning:

| Deposited atom pair | Chain A distance (Å) | Chain B distance (Å) |
| --- | ---: | ---: |
| TSA O7 – Lys168 NZ | 3.231 | 3.231 |
| TSA O7 – Glu246 OE1 | 3.133 | 3.133 |
| TSA O7 – Glu246 OE2 | 3.176 | 3.177 |
| TSA O5 – Glu198 OE1 | 4.765 | 4.765 |
| TSA O5 – Glu198 OE2 | 2.666 | 2.666 |

The selected residues occur in the deposit software's TSA binding-site rows
AC3/AC4; the atom pairs are project selections. Both glutamate oxygen names
remain present rather than selecting only the nearer oxygen.

These separations describe the deposited inhibitor model. They do not establish
catalytic roles, hydrogen bonds, proton donation, catalytic distance tolerances
or a transition-state energy. The two coordinate copies are not independent
experimental replicates. The deposited component graph, atom-specific
occupancies and B factors accompany the geometry; no preferred alternative or
coordinate uncertainty is invented. TSA heavy-atom B factors span
84.37–96.69 Å², compared with the reported overall mean of 38.6 Å². An
occupancy token of 1.00 does not establish precise localization, and neither
the B factors nor the 3.0 Å refinement limit is converted into a calibrated
atom-error model.

The TRP binding-site rows AC1/AC2 include symmetry labels 12_555 and 4_555.
They are retained as source evidence; the assembly-1 projection does not
claim to reconstruct the complete regulatory interface.

## Reproduce and inspect

```bash
python scripts/build_atlas_deposit_context.py --packet data/atlas/deposit_context/m0081 --check
```

The [projection](../data/atlas/deposit_context/m0081/projection.json) is a
repository dataset, separate from the installed source-draft query and frozen
Atlas-10 kernel. It contains complete selected parsed source rows, assembly-qualified
atom coordinates, calculated distances and separately labeled interpretations.
Every interpretation cites declared row selections or geometric pairs.

The shared builder accepts a source hash, exact row selectors, expected row
counts and an optional assembly specification. It reuses the existing mmCIF
parser and assembly projector. Source identity, selector spelling, cardinality,
references and stale review pins are checked. These checks establish extraction
integrity; they do not adjudicate chemistry or make the interpretation true.
Source and adversarial computational review supplies the bounded interpretation,
without claiming independent human review. All case-specific facts stay in data.

The previous structural-context adapter requires a frozen Atlas-10 Tier-2
record, and the assay-context adapter requires an engineered substitution and
observations. Neither describes this annotation. The new adapter removes that
particular coupling without changing their existing contracts or pretending
that the M0081 source mechanism has been compiled.

## Scope and the remaining bottleneck

A competent PDB inspection can obtain these facts. The atlas contribution is a
reproducible chemical-state boundary beside the proposed template, preserving
ligand definition, sequence conflict and exact coordinate identity together.
No speedup, comparative superiority, new design success or inferred mechanism
is claimed. The atom rows and generic assembly projector were reused; a second
real packet using the new wrapper has not been demonstrated.

The [accounting recovery](../data/atlas/deposit_context/m0081/acquisition_recovery.json)
found that the inherited 28 requests / 1,474,405 bytes are only a metered lower
bound. Historical browser traffic is missing. No new source request was made,
and neither remaining capacity nor a new batch balance was inferred. The
[attribution](../data/atlas/deposit_context/m0081/SOURCE_ATTRIBUTION.md) describes
local source reuse.

M0081 remains a transcription-only panel candidate for mechanism admission.
Its concerted rearrangement, source-residue roles and substrate-to-inhibitor
correspondence need direct mechanistic evidence and evidence-linked
adjudication before a source-scoped draft. More 3CSM geometry cannot supply
those missing source statements.
