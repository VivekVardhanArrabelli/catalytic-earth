# A mechanistic question with discriminating published evidence

Does reported nondetection of racemization mean that H297N mandelate racemase has lost all
catalytic capability? The reported S-mandelate proton exchange supports a
narrower, endpoint-specific impairment. The case connects those experiments
to the existing M0187 source transformation and P11444:H297 reference context.
It does not establish the complete molecular cause.

| Published observation | Source-scoped result |
| --- | --- |
| H297N racemization | Not detected; direction, assay conditions and detection floor unspecified in the inspected abstract |
| H297N S-mandelate alpha-proton exchange | Rate 3.3-fold lower than WT solvent-deuterium incorporation at pD 7.5 in D2O |
| H297N R-mandelate exchange | Not detected in that exchange context; detection floor unspecified |
| H297N structural comparison | Authors report no conformational alteration at 2.2 Å resolution |
| K166R R→S racemization | Nonzero turnover; kcat reduced 5000-fold |
| K166R S→R racemization | Nonzero turnover; kcat reduced 1000-fold |

The H297N observations come from the [1991 primary abstract](https://pubmed.ncbi.nlm.nih.gov/1909893/).
The [1995 K166R abstract](https://pubmed.ncbi.nlm.nih.gov/7893690/) provides
context from a different variant and publication. K166R is not a reciprocal
zero-activity knockout or a matched H297N control. Its abstract does not name
the fold-reduction reference, so the K166R comparator remains unspecified.

Both retained abstracts are truncated. Unknown conditions and detection floors
remain unknown; pD 7.5 belongs to exchange, not the separate racemase statement.
S-specific exchange does not establish S→R racemization. Stepwise overall
racemization does not settle whether proton transfers within one step are
concerted. Static structural similarity does not rule out subtle or dynamic
effects.

## Inspect the case offline

```sh
catalytic-earth atlas-mechanism-evidence
catalytic-earth atlas-mechanism-evidence --variant H297N --endpoint isotope_exchange
catalytic-earth atlas-mechanism-evidence --variant K166R --endpoint turnover
catalytic-earth atlas-mechanism-evidence --variant K166R --include-source-context
```

The dependency-free wheel returns one case containing six published-observation
projections, two competing explanations, explicit discriminants and a reviewed
project adjudication. Filters select observations within each case while keeping
the **complete case, adjudication and abstentions** alongside the selected rows.
The two commands with filters match two observations each. An empty result
means no matching retained observation; it is not evidence of absent chemistry.
`--output` writes a new JSON file and refuses to overwrite an existing file.

The optional `--include-source-context` adds a separately versioned
`source_context_query`. It currently returns one deposited K166R context,
linked through the exact primary PMID/DOI and reported substitution. The
complete six-observation case and its adjudication accompany the context.
The original observations, their count, and the default query stay unchanged.

`--variant` filters both planes. `--endpoint` filters **observations only**:
`--variant K166R --endpoint structure --include-source-context` returns zero
retained abstract observations and one deposited context. A context match
does not satisfy the observation filter. `H297N` returns no deposit context;
that means no matching retained context, not that an H297N structure cannot
exist. Related observation IDs identify same-citation/variant rows, not new
measurements or identical crystal and assay specimens.

The [evidence sidecar](../data/atlas/mechanism_evidence/m0187/evidence.json)
records results separately from source interpretation and project diagnosis.
`not_detected` has a null value, not zero. Numerical results here are reported
fold reductions, not absolute rates or new measurements. Only the H297N
S-exchange comparison explicitly identifies WT in the inspected abstract.

## A source fragment connects His297 to the existing functional discriminant

```sh
catalytic-earth atlas-mechanism-evidence --variant H297N --include-source-fragments
catalytic-earth atlas-mechanism-evidence --variant H297N --endpoint isotope_exchange --include-source-fragments
```

The optional `source_fragment_query` connects the retained M0187 proposal-1
step-1 arrow `o40`, atom `m1.a58`, through its seven-heavy-node covalent
fragment to the sole alias `His297A` on `a52`. The same selected source step
declares P11444:H297. Its existing numbering map retains author chain A
His297, UniProt H297 and 1MNS label residue 295 as distinct identifiers.
This resolves a source-fragment relation; it assigns no deposited atom name.

| Selected source endpoint | Fragment alias | Selected-step reference relation | Focal H297N evidence returned |
| --- | --- | --- | --- |
| Step 1, m1.a58, o40 | His297A on a52 | P11444:H297 | Existing focal H297N observations, subject to observation filters |
| Step 1, m1.a63, o39 | Glu317A on a59 | Unresolved: this step declares H297, not E317 | None |
| Step 2, m1.a19, o39 | Lys166A on a24 | P11444:K166 | None: existing K166R rows are contextual in the H297N case |

The H297 relation includes the exact reviewed transformation binding and its
changed-atom/edit/arrow witnesses. The Lys166 row demonstrates the same
fragment rule on another catalytic residue and step, but is explicitly
source-step context, not another reviewed transition. The Glu317 refusal says
nothing about whether glutamate participates chemically; it exposes the
narrower selected-step declaration. No source residue role is assigned to source atom a58.

The shared consumer follows heavy-atom covalent bonds, requires one residue
alias and no competing identity labels, and retains excluded H bonds and
opaque coordinate/stereo annotations. Hydrogen, aliased placeholder endpoints,
ambiguous labels, mixed ligand/residue components and unmatched step sites
cannot supply this relation. Raw schemes, qualified molecule/atom references,
source hashes, exact Atlas-10 context and the separate computational review
travel with the package. This source relation was computationally reviewed; topology alone does
not recognize a residue or establish a physical atom's identity.

The functional join requires the same source record/proposal, reference site,
UniProt context and focal variant of the already validated evidence case.
It copies existing observations with their conditions, source references and
limitations; it does not transcribe measurements or import another variant's
adjudication. Both filters apply only to the copied observations: all three
source relations remain visible and have a separate count. Empty evidence
means no matching retained focal observation, not absent activity.

H297N retains S-mandelate exchange at 3.3-fold below WT at pD 7.5 in D2O.
R-exchange and the separately reported racemase endpoint were not detected;
unknown detection floors remain null. This supports an endpoint-specific
functional discriminant alongside a source-proposed atom relation, without
experimentally validating `o40`, an intermediate, a proton trajectory or the
complete molecular cause. P11444 remains reference context; exact assayed
sequences and mutant geometry are not established by retained evidence. Exchange is not racemization.

The original direct-endpoint-label query and its frozen functional evidence
remain unchanged: they still report no explicit residue label on `a58`.
The supplemental fragment relation has a different evidence basis and status.
One consumer now recovers this additional relation without reinterpreting each
source panel. This is within-entry reuse, not demonstrated broad coverage,
measured curation-time savings, an experiment or validated enzyme design.
The [specification](../data/atlas/mechanism_evidence/source_fragment_spec.json)
and [review](../data/atlas/mechanism_evidence/source_fragment_review.json)
use retained sources only; acquisition was zero requests and zero bytes.

### Entry-level mutation annotations retain their narrower evidence basis

The same optional query now returns `reference_annotation_context` for the
His297 and Glu317 fragments. It resolves the entry-wide reference site using
the existing residue mapper, independently of the selected step's catalyst
list, and joins an exact UniProt point-mutagenesis feature. The retained
P11444 snapshot is bound to the original Atlas-10 protein evidence, accession,
natural-sequence position and wild-type residue. Its entry version is 141,
sequence version 1. Feature indices below are zero-based source locators.

| Reference site and feature | Retained UniProt statement | What the integrated relation adds |
| --- | --- | --- |
| P11444:E317, feature 9, E317Q; ECO:0000269 / PMID7893689 | “Reduces activity 10000-fold.” | The Glu317A fragment can carry a source-scoped variant-effect annotation even though step 1 does not declare E317 as a catalyst. |
| P11444:H297, feature 8, H297N; ECO:0000269 / PMID1909893 | “Loss of activity.” | This coarse annotation sits beside the existing endpoint-specific evidence, including retained S-mandelate exchange. It does not mean every catalytic endpoint is abolished. |

The Glu317 relation keeps author residue 317, UniProt E317 and 1MNS label
residue 315 distinct. `Glu317A` means the residue on author chain A, not an
E317A substitution. It remains unresolved in `source_record_residue_mapping`,
which answers the narrower selected-step question. Its existing primary-
observation match in `functional_evidence` remains empty. Entry-level source roles are not assigned
to atom a63 or to step 1 by this annotation, and the source's o39 arrow is not
experimentally validated. Absence from that step's list does not establish a
biologically unimportant or noncatalytic residue.

The original feature, alternatives, evidence code, citation metadata and
source version travel with the context. These are **two database annotations**,
not additional experimental observations. This database-annotation view was built without primary E317Q results.
The separate primary-factor query below does not add observations to this view. The UniProt feature text by itself supplies no identified endpoint, kinetic
parameter, comparator/denominator, reaction direction, assay conditions,
exact assayed construct or uncertainty. The consumer preserves the wording
without extracting a numeric ratio, assuming a wild-type denominator,
calculating an energy, or assigning a microscopic cause. These interpreted
quantities remain null. A citation title or UniProt crystallography reference
position does not supply a mutant geometry or assay result.

This reuses one source-feature rule for His and Glu, without enzyme-ID code or
retranscribed measurements. The useful constraint is that a step declaration
cannot exclude entry-level variant evidence, while a generic activity summary
cannot replace endpoint-specific observations. This is within-entry reuse;
broad coverage, measured effort savings and design performance are untested.
Observation filters still affect only the existing observation plane; both annotation
contexts remain visible with their own count and evidence basis. No new
acquisition, frozen-record change, evidence-tier promotion or claim is added.

### Primary E317Q factors retain the substrate enantiomer

A separately reviewed [Mitra1995 primary abstract](https://pubmed.ncbi.nlm.nih.gov/7893689/)
reports E317Q kcat reductions of 4,500-fold with R-mandelate and 29,000-fold
with S-mandelate. WT is the whole-abstract contextual reference; the factor
sentence does not explicitly name its denominator. The preserved final E317O
token is an apparent source/index typo, not an additional datum. Full methods,
absolute rates, uncertainty and exact matched preparation are unavailable.
R/S identifies the substrate; net reaction direction remains unassigned.

```sh
python scripts/query_atlas_perturbations.py --comparison mandelate_1995_e317q:E317Q:substrate-specific-context
```

This existing consumer returns both author-reported factors beside the original
UniProt feature 9 and its exact PMID/DOI citation. The database 10000-fold summary
is not projected as a primary observation. P11444:E317 remains reference context;
no selected-step role, assayed sequence, mutant geometry, residue energy or
validated arrow follows. The plural kcat/KM reduction is not split by enantiomer.
No new scalar comparison is computed, and the H297N evidence is unchanged.

The [source packet](../data/atlas/study_context/mandelate_1995_e317q/source_qualification.json)
binds a recovered, hash-verified archived PubMed tool excerpt. The full abstract
stays Git-common-local. This is tool-extracted text, not raw HTTP or publisher
full text. [Recovery provenance](../data/atlas/study_context/mandelate_1995_e317q/source_recovery.json)
records zero new requests; the earlier unmetered discovery still prevents a
claim of remaining source-budget headroom.

## Provenance and unresolved links

### New source followup: the K166R deposit

The [supplemental annotation](../data/atlas/mechanism_evidence/m0187/structure_followup/annotation.json)
now identifies [PDB 1MDL](https://www.rcsb.org/structure/1MDL) through its exact
primary citation, PMID 7893690 / DOI 10.1021/bi00009a007. The retained mmCIF
declares entity 1 as K166R, aligns chain A to P11444, and records an engineered
Arg166 against reference Lys166. This is deposited-specimen evidence; it does
not identify the exact protein preparation used in each reported assay.

The title names R-mandelate cocrystallization, but the model contains two
distinct components: RMN at author A398 / label chain C and SMN at author
A399 / label chain D. The depositor assigns SMN to the active site and RMN
to the approach region, and suggests that SMN arose by slow racemization.
That last statement is **depositor interpretation**, not a newly measured
turnover event or rate. Both modeled ligand instances have occupancy 1.00;
this is not a solution population or productive fraction. Neither ligand is
mapped to the M-CSA drawing or treated as an observed intermediate.

A source conflict remains explicit: the gene-source field says
*Pseudomonas aeruginosa* / taxid 287, while the sequence reference is
P11444 / MANR_PSEPU and the primary abstract names *Pseudomonas putida*.
No organism is chosen by majority vote. The current deposit is not asserted
byte-identical to the coordinates originally studied in 1995.

This followup did not obtain either paper's full methods. H297N structure
identity, assay conditions and detection limits remain unresolved. The
H297N text search's 9FI1 result belongs to a different enzyme and paper and
was rejected. The broader structure search inspected 100 of 306 returned
candidates, so it does not establish absence of an H297N deposit.

The [cumulative acquisition appendix](../data/atlas/mechanism_evidence/m0187/structure_followup/acquisition_appendix.json)
carries the original two captures forward. Ten further requests, including
two ACS 403 responses and two unsupported-query 400 responses, bring the
same source scope to **12 requests / 440,960 bytes**. Its inherited
12-request/2-MiB sublimit is reached; the batch was not renamed or reset.
Earlier unmetered discovery remains disclosed. The public PDB file is
retained losslessly as gzip; no paper body is redistributed.

The shared mmCIF parser now exposes standard citation, sequence-reference,
mutation, organism and entry-detail categories. The source rows are checked
against the retained file. This adds a source annotation to an existing
case, not another assay observation, mechanism draft, or evidence tier.
The default six-observation CLI output remains unchanged; the optional source
context interface exposes the accepted annotation beside it (CE-021). It
preserves each ligand instance, raw occupancy and alternate-conformation
tokens, source interpretation, organism conflict and unresolved identities.

The [source-context specification](../data/atlas/mechanism_evidence/source_context_spec.json)
pins the accepted annotation/review and existing evidence. A shared adapter
checks all reviewed source-file pins and rederives deposited citation,
entity/reference/alignment/substitution and ligand-instance facts from the
retained mmCIF. Runtime joins also check exact primary-projection hashes,
PMID/DOI, variant, reference accession and supporting observation IDs. The
wheel carries the reviewed factual context and provenance, without needing
the original checkout or network. No enzyme identifier branches or repeated
manual observation joins are added; only single-substitution deposit contexts
supported by this source format are currently handled.

The useful relation is a bounded bridge between published functional endpoints
and deposited specimen evidence. A competent PubMed/PDB workflow can find both
sources; this interface retains their exact relation and prevents a K166R
deposit or inferred product origin from becoming H297N or turnover evidence.
No measured curation-time reduction or comparative biological accuracy is
claimed.

### Dictionary stereochemistry does not transfer site context

A new optional comparison operation on the existing deposit projector checks
an explicit component-dictionary atom map and returns both instance contexts:

```sh
python scripts/build_atlas_deposit_context.py --packet data/atlas/deposit_context/mandelate_1mdl --comparison rmn-smn
```

For the source-named RMN/SMN enantiomers in 1MDL, the map covers all 19 dictionary
atoms, including eight hydrogens. Element/aromatic tokens and all 19 bond
endpoint/order/aromatic/stereo records match. The sole atom stereochemistry
change is C7 `R` to `S`; there are no unchanged assigned stereocenters. This is
a relation between deposited dictionary definitions, not a new assignment of
absolute configuration from coordinates or a normalized bound microstate.

| Separately retained instance | Modeled ligand atoms | Deposited site context | External connections in `struct_conn` |
| --- | --- | --- | --- |
| RMN, author A398 / label C | 11 heavy atoms; eight dictionary H lack coordinates | Software AC2, six members; depositor calls this the approach region | No RMN rows |
| SMN, author A399 / label D | 11 heavy atoms; eight dictionary H lack coordinates | Software AC3, thirteen members; depositor calls this the active site | Mg connections to O8 and O11, source distances 2.102 and 2.024 Å |

The query **refuses the same-deposited-environment request**: the anchored site
records, membership records and external-connection inventories differ. The
software shells cross-list the other ligand, which does not make their anchors
interchangeable. Missing RMN connection rows do not prove nonbinding or no
physical contacts; `struct_conn` is not a complete contact inventory. Model 1,
occupancy 1.00 and no alternate identifier remain raw model fields. Neither
equal ligand populations nor enantiopurity follows, and bound protonation stays unknown.

This extends CE-021 without revisiting its earlier title, source-origin or
organism review. The [packet](../data/atlas/deposit_context/mandelate_1mdl/spec.json)
and its [computational source review](../data/atlas/deposit_context/mandelate_1mdl/review.json)
reuse the retained gzip source and existing parser. The optional comparator
belongs to the existing deposit projector; chemistry and selectors remain in
data. It checks full declared maps without deleting H, normalizing stereo, or
introducing an enzyme-specific branch. It reports arbitrary explicit R/S
inversions and unchanged centers; it does not label every inversion an
enantiomer relation. Current scope is two components in **one deposit** with
complete heavy-atom coordinates and no alternate conformers. Comparisons
across deposits require a further source-bound relation. Membership and connection
equality compare literal deposited records, including order and metadata, not
normalized biological environments. The original installed six-observation query and all prior
deposit projections are unchanged.

The new value is executable graph correspondence coupled to a refusal of
instance-context transfer. No measured curation-time saving, superiority over
competent use of PDB, productive geometry or enzyme-design performance is
claimed. No new sources, experiments or evidence tiers are added.

The initially selected M0213 D/L-analogue comparison remains **unassessed**:
1L6F is not retained, and complete PLP acquisition headroom is unknown. The
retained 1L6G dictionary has PDD CA=`R`, N–C4A single bonding and two dictionary
H on C4A, but that does not supply the missing L-analogue graph or validate a
native imine intermediate. Separately scoped metered PLP subsets total at least 73
requests / 5,068,731 bytes; their explicit exclusions of other browsing prevent
treating the arithmetic remainder as usable headroom. No batch was reset or
new request issued. This missing counterpart does not weaken the closed PLP
source-drawing boundary or gain support from the mandelate result.

### The reaction-to-deposit join stops at protonation

The same deposit query now connects the reviewed M0187 input graph to the
RMN dictionary, with SMN as a separately scoped stereo comparison.

The retained source ligand still carries raw `chebi:17756`. R is the reviewed
computational graph/stereo correspondence to CHEBI:32382, not an upstream
relabeling; the query retains this conflict and its no-relabel abstention.

```sh
python scripts/build_atlas_deposit_context.py --packet data/atlas/deposit_context/mandelate_1mdl --comparison m0187-input-rmn
python scripts/build_atlas_deposit_context.py --packet data/atlas/deposit_context/mandelate_1mdl --comparison m0187-input-smn
```

**Exact chemical-state identity is refused.** The retained
[CHEBI:32382 MOL](../data/atlas/transformations/m0187/CHEBI_32382.mol)
encodes carboxylate atom 10 with charge −1, corresponding to source a11.
Both 1MDL dictionaries instead state formula `C8 H8 O3` and explicitly bond
the corresponding O12 to HO2. This is a canonical-representation
protonation difference, not evidence for the bound ligand's protonation.
The mmCIF dictionary omits atom charge fields and coordinate charge tokens are
unknown; neither is silently converted to a deposited charge of zero.

| Source locator | Dictionary locator | What the join retains |
| --- | --- | --- |
| a9 / canonical atom 8 | C7 | Source-computed R matches the RMN R token and differs from SMN S |
| a8 / canonical atom 7 | C10 | Carboxyl carbon |
| a10 / canonical atom 9 | O11 | Double-bonded carboxyl oxygen |
| a11 / canonical atom 10 | O12 | Source −1 charge; dictionary charge unavailable and O12–HO2 explicit |
| a12 / canonical atom 11 | O8 | Alpha-hydroxyl oxygen |
| a66 | H7 | Explicit source alpha H; dictionary H has no coordinate |

Each map covers the full 12-node depicted covalent component: 11 heavy atoms
and a66. Two phenyl topology maps remain. The literal alignment preserves all
12 mapped bond orders; the reflection changes six ring single/double tokens.
Dictionary aromatic flags are returned without normalizing the source graph,
which has no corresponding aromatic fields. Non-aromatic order differences
are rejected, so swapping the carboxyl oxygens cannot pass as another ring map.
No unique physical correspondence follows.
Source Mg coordinate bonds from a10/a11 lie outside this covalent graph join;
no source-to-deposit coordination or pose equality is established.

The query reports seven unmapped dictionary H and every bond touching them,
including O12–HO2. Other source H remain implicit; raw node-count inequality
alone would not establish a protonation difference. Runtime makes no implicit-H inference.
The chemical interpretation above is separately source-reviewed. Likewise,
the retained RDKit-2025.03.3 R assignment is computed provenance, whereas C7 R/S
is a deposited dictionary token. Source wedge conventions and dictionary bond
stereo tokens are not treated as equivalent representations.

Generic optional `reaction_state_comparisons` reference the unchanged,
[reviewed transformation](../data/atlas/transformations/m0187/transformations.json)
by exact file hash, transformation ID and before/after state. The projector
checks its review digest and all source bindings, requires one complete
depicted component, and returns canonical correspondence, both locator maps,
charge/stereo diagnostics and the full separate instance context. Case facts
remain data; the existing graph validator and component resolver are reused.
The comparison cannot establish full chemical identity, even if selected
tokens agree. This avoids a new MOL/stereo engine or a silent neutralization.

This extends CE-021 with a computable refusal that a name-only R-mandelate
join would miss. RMN's approach-region context cannot supply a reacting
R-mandelate pose, and SMN's distinct active-site context cannot repair that
missing identity. The source's product-origin interpretation remains separate.
No productive geometry, atom trajectory, new observation, assay specimen,
independent validation or evidence tier is added. Retained inputs and the
earlier RMN/SMN dictionary comparison are unchanged; no sources were acquired.

### Boundaries of the original abstract-only query

The sidecar pins the existing Atlas-10 payload, exact M0187 transformation,
proposal and source snapshot. P11444 is reference-site context: the H297N
abstract supplies no organism or UniProt identifier; the K166R abstract names
Pseudomonas putida and cites the H297N paper. Exact assayed construct sequences
were not inspected.

Neither inspected abstract supplies a mutant PDB accession. Existing Atlas
structure 1MNS is an inhibitor-bound, chemically modified Lys166 context;
it is not either mutant structure or a turnover observation. All seven changed
M0187 source atoms retain their unresolved direct-endpoint-label correspondence.
The separately reviewed fragment relation above does not rewrite that original
query or evidence record. This functional
evidence adds no residue label, physical atom map or observed intermediate.

The [source attribution](../data/atlas/mechanism_evidence/m0187/SOURCE_ATTRIBUTION.md)
and [acquisition ledger](../data/atlas/mechanism_evidence/m0187/acquisition_receipts.json)
record two official captures, totaling 16,968 bytes, within a predeclared
12-request/2-MiB limit. Raw XML is retained locally for analysis and excluded
from the repository and wheel. The wheel includes factual projections, short
source witnesses and their hashes.

```sh
python scripts/build_atlas_mechanism_evidence.py --check
```

The builder checks observation-to-projection equality and source/capture joins.
An optional `--raw-source-directory` containing the originally captured
`PMID_1909893.xml` and `PMID_7893690.xml` additionally checks exact response
hashes, source identities and witness substrings. It never accesses the network.
These are integrity checks; they do not prove an interpretation from prose.

Review uses informed same-model agents with potentially correlated errors,
not independent experts. The payload review pin is maintained manually after
source-to-conclusion review; the builder cannot silently refresh it. The work
is retrospective source analysis, not a prospective prediction, new laboratory
result or evidence-tier promotion. Review objections and resolutions are
recorded in `work/coordination_mechanism_case.md` in the full repository.
