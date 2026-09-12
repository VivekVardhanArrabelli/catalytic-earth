# RA95 parent function and deposited chemical states

The measured RA95.5-8F parent can be linked to both source-named crystal
structures by the full 258-residue canonical sequence. The inhibitor complex
still has an unresolved complete covalent graph and conflicting crystallization
pH. These are separate conclusions. The atlas exposes them together instead of
turning a matching sequence or structure title into a productive template.

```sh
python scripts/query_atlas_perturbations.py --state-link ra95_2017:RA95.5-8F-states
```

The query returns the existing parent kcat 10.8 ± 0.6 s^-1, KM 320 ± 36
micromolar and printed efficiency 33,800 M^-1 s^-1, with their source-defined
(R)-methodol assay at 29°C/pH7.5. These observations are not copied or
reinterpreted as rates of a crystal or inhibited specimen. The new `state_links`
collection resolves two deposit projections and their source context. It rejects
foreign/mutant observation IDs, a different deposited canonical sequence and
incorrect source/deposit identities. The original source-row pointer and
parameter set also prevent replacing cleavage evidence with same-construct
synthesis results. Public queries reconstruct and verify the reviewed deposit
packets. The full scientific projection remains
subject to computational source review, not just hash equality.

## What matches, and what remains different

Both [5AOU](https://www.rcsb.org/structure/5AOU) and
[5AN7](https://www.rcsb.org/structure/5AN7) cite Obexer2017 and identify the
parent in their titles. Their full canonical sequences equal the printed
Figure S6a parent including initial methionine and positions251–258
`LEHHHHHH`. The actual polymer records encode S-oxymethionine (`MHO`) at
position237; canonical `M` does not erase this modification. Only its extra oxygenOD1 is partial occupancy (apo0.71, complex0.74); no
unoxidized population or functional consequence is inferred. The source mass
calculation excludes initiatorMet, while canonical strings include the
unmodeledMet1; exact mature N-terminus/specimen identity remains unestablished.
The5AOU reference difference table calls246–258 expression tag; preserve that
annotation separately from the source-reported251–258 terminal suffix.

The full residue-numbering tables and missing-coordinate records are retained.
5AOU changes author-number offset after label63: Tyr51 is author1051, while
Ser81/Lys83/Asn110/Tyr180 are2081/2083/2110/2180. In5AN7 these sites are
1051/1081/1083/1110/1180. Do not apply a global offset to5AOU or trim the
sequence to its observed atoms. The supplement says58–63 were unmodeled in
both structures, while the current5AN7 models62–63. Preserve this model-boundary
conflict; do not delete coordinates or infer why the records differ. Exact
sequence equality and same-study naming do not authenticate shared physical
assay/crystal preparations.

| Context | Source/deposit evidence | Limit |
| --- | --- | --- |
| 5AOU, source-named apo | Supplement and deposit pH4.6;100K diffraction; MHO237, phosphate, ethylene glycol and waters retained | Apo refers to the inhibitor comparison, not absence of other chemical species |
| 5AN7, inhibitor-derived instance | Supplement identifies the inhibitor3 complex; LLK is authorA5001/labelD, occupancy0.75;100K diffraction | Complex pH is7.5 in supplement but4.5 in deposit; normalized pH remains null |
| Parent cleavage assay | Existing source-bound(R)-methodol kinetic parameters at29°C/pH7.5 | No crystal-to-solution, parent-to-mutant or inhibition-to-turnover transfer |

## The exact chemical mapping stops short

The [retained supplement](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fnchem.2596/MediaObjects/41557_2017_BFnchem2596_MOESM342_ESM.pdf)
Materials p2 identifies inhibitor3 as a1,3-diketone. Methods p10 and
Figures S8–S9 describe derivatization and a Schiff-base complex, with a
comparison with the planar configuration expected for vinylogous amide4.
Table S2 assigns this complex to5AN7.

The deposit separately defines LLK as an enone, `(2E)-1-(6-methoxynaphthalen-2-yl)but-2-en-1-one`,
C15H14O2, with17 heavy atoms and no lysine nitrogen. Its entry prose calls the
1,3-diketone `CC1` covalently bonded to Lys2083, although actual5AN7 Lys83 is
author1083. Its complete `_struct_conn` table has two MHO peptide connections
and no LLK/Lys83 connection. These source facts support a source-linked,
inhibitor-derived coordinate instance; they do not provide a complete typed
protein-adduct graph. The original covalent assertion remains visible. Missing
structured connectivity is not evidence that the adduct was absent. The
component dictionary and coordinate hydrogen names also disagree: H13/H31A/H31B
are dictionary-only, while H112/H1B/H1C are coordinate-only. The dictionary
C12=C13/H13 description cannot silently become a complete adduct graph. No
atom-name repair, bond-order repair or protonation assignment is made.

The original two ligand-relevant atom pairs use the existing assembly
consumer. Lys83NZ to LLKC13 is1.274005/1.291032Å for alternativesA/B;
Tyr51OH to the deposited carbonyl oxygen LLKO1 is2.435342/1.776955Å.
These are separate coordinate pairs with unresolved coexistence, not jointly
observed ligand geometries. The second Tyr alternative's very short distance
is retained and must not be called a coexistent contact. None of these
distances creates a bond, assigns hydrogen positions, establishes a hydrogen
bond or selects a tautomer. LLK0.75, Lys83A/B0.57/0.43 and Tyr51A/B0.75/0.25
remain distinct occupancies with unresolved joint states. No occupancy averaging,
active-fraction estimate or kinetic population is inferred. The source also
describes secondary Ser81/water and Met182 packing contacts; the selected
pairs do not claim a complete contact inventory.

## The parent tyrosine pair has no single deposited separation

The two hydroxyl groups removed in the existing Y51F/Y180F functional square
now have an explicit coordinate relation in both parent deposits. This extends
the construct/state scope of CE-034; it adds no mutant structure or functional
observation.

```sh
python scripts/query_atlas_perturbations.py --state-link ra95_2017:RA95.5-8F-states --with-comparisons
```

| Parent deposit / Tyr51 alternative | Tyr51 OH to Tyr180 OH (Å) | Individual OH occupancies, Tyr51 / Tyr180 |
| --- | --- | --- |
| 5AOU, neither atom has an alternate label | 3.827 | 1.00 / 1.00 |
| 5AN7, Tyr51 A | 2.730 | 0.75 / 1.00 |
| 5AN7, Tyr51 B | 4.372 | 0.25 / 1.00 |

These distances are calculated from the retained model-1 coordinates through
assembly-1 identity operator1. The query preserves exact atom-site IDs
437/1507 in5AOU and944/945 versus3296 in5AN7, all Tyr51 alternatives and
the different Tyr180 author numbers2180/1180. It carries the
`tyr51-oh-to-tyr180-oh` pair in each deposit projection, beside the source
conditions, ligand-state conflicts and canonical parent association.

The inhibited deposit has one shorter and one longer Tyr51 alternative
relative to the apo separation. The local coordinate comparison therefore
does not supply one invariant Tyr-pair distance to transfer into a design.
This narrow negative audit does not refute the authors' broader network or
preorganization interpretation, which is not a claim of identical pair distances.
It does not identify a hydrogen bond or ligand-induced motion: crystal media
differ, complex pH is unresolved, and cross-residue alternate coexistence and
solution populations remain unestablished. No occupancy-weighted distance is
formed, and the shorter alternative is not selected as a productive state.

The same existing query also returns the four-cell kinetic comparison and
its retained thermal evidence. Its kcat observed/multiplicative-reference
ratio remains0.021, while reported melting temperatures remain76,71,74 and67°C
for parent, Y51F, Y180F and double mutant respectively. These functional and
thermal results do not assign the coordinate alternatives to mutants, isolate
a Tyr–Tyr interaction or establish a microscopic coupling energy. Only the
three parent kinetic observations are state-linked.
Co-retrieval of these same-study results is not independent corroboration of
a mechanism. The coordinate audit adds no causal constraint to the square.

The two new pair declarations reuse the existing deposit projector and
state/comparison query without a runtime or observation change. Source
selection and interpretation remain manual; this is a computable parent
coordinate audit, not evidence of generalization or measured curation-time
savings. The bounded comparison is complete. Additional nearby distances
would need a distinct scientific question.

## Evidence and reuse

The source context is `data/atlas/study_context/ra95_2017/chemical_state.json`.
Its acquisition appendix continues `designed-retroaldolase-ra95-giger2013`:
2 new requests/1,237,896 response-body bytes; cumulative26/16,591,234 of
100/31,457,280. Both public RCSB CIFs are retained in
`data/atlas/deposit_context/ra95_5aou` and `ra95_5an7`. The publisher supplement
is reused from the existing Git-common source cache and is not redistributed.
The old source packets and their evidence limits remain unchanged.

The tyrosine-pair extension required zero requests or new source bytes. The
later DERA access appendix is the latest ledger for the same named batch:
33 requests /17,556,517 response-body bytes cumulatively. The older26-request
figure above records the original chemical-state increment, not current use.

The generic deposit/assembly projector is reused. Three standard mmCIF
categories expose canonical polymer sequence, chemical modification and
diffraction conditions. One generic state-link operation joins exact sequences
and existing functional observations; chemistry, numbering and conflicts stay
in data. This is a usable connection and an explicit chemical-mapping limit,
not another kinetic-table migration. Manual source mapping/review remains a
cost; no measured speedup or superiority over competent incumbent use is claimed.

No project experiment, new protein admission, complete mechanism, productive
solution geometry, mutant structure, evidence-tier promotion or prospective
design capability follows. The missing evidence is an unambiguous complete
inhibitor/protein atom-and-bond mapping and a resolution of the crystal-pH
conflict. This result satisfies the bounded current question without making
those unresolved issues prerequisites for all future atlas coverage.
