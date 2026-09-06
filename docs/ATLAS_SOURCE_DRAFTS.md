# Reusable source-mechanism compilation

The source-draft path turns reviewed M-CSA chemistry into offline, queryable
atlas records. It addresses the gap between source review and usable chemical
content. The compiler accepts a bounded source selection and declared scopes;
its chemistry fields do not depend on enzyme-specific schema branches.

## What is represented

New mechanism-record v4 drafts carry source reaction context, competing
mechanism proposals, ordered source steps, available curved-arrow endpoints,
source residue assertions, and typed component/state context. They preserve
the source's inferred steps, unresolved fields and review abstentions. They
remain Tier 1 source-derived drafts. M-CSA participant context is not relabeled
as a balanced Rhea reaction or an exact reaction instance.

The initial batch covers M0106 pyruvate dehydrogenase E1, M0107 aerobic CODH,
M0212 nitrogenase, and M0753 HisF. Each has one record; alternative proposals
remain inside that record: five proposals contain 43 reaction steps, five
terminal states, and 148 preserved source arrow annotations. Source annotations are not duplicated into extra
records to increase the count. The existing Atlas-3/10 v2/v3 records and query
results remain unchanged. M0064 and M0970 remain subject to their existing
mechanism-draft objections.

The separate `aldolase-transketolase` batch adds M0052 class II aldolase,
M0222 class I aldolase, and M0219 transketolase: three records, four proposals,
26 reaction steps, four terminal states and 98 source arrow annotations. Its
successor review inherits the earlier six decisions unchanged and adds three
source-scoped decisions. Those first two batches contain seven Tier-1 records,
nine proposals, 69 reaction steps, nine terminal states and 246 source arrows.
These counts include source-marked inferred and extra-enzymatic steps; they
are not counts of experimentally observed active-site events.

The `plp-pyruvoyl` batch adds M0066 D-alanine transaminase, M0213 alanine
racemase, M0186 L-serine ammonia-lyase and M0049 pyruvoyl histidine
decarboxylase. Its four proposals contain 32 reaction steps, four terminal
states and 99 source arrows. Across all three batches there are eleven Tier-1
records, thirteen proposals, 101 reaction steps, thirteen terminal states and
345 source arrows. Three different PLP reaction branches and the non-PLP
pyruvoyl example remain separate records with explicit applicability limits.

The new source challenge retains these material conflicts:

- M0066's entry and scheme identifiers describe D-glutamate, while Step 1
  prose names L-glutamate.
- M0049's entry specifies L-histidine, while scheme panels 1–6 carry the
  identifier for D-histidinium. Precursor Ser83, prose Prv-82 and mature-chain
  Pyr1F numbering also remain distinct source assertions.
- M0213 retains an L-alanine scheme identifier even in its terminal panel,
  while the entry product is D-alanine and the drawing changes stereochemistry.
  Direction-dependent catalytic roles and the reference analogue are retained.
- M0186 explicitly infers its Step 4 phosphate-base assignment and assumes
  the corresponding acid assignment in Step 5. Panels 6 and 7 describe
  hydrolysis outside the active site and are retained as distinct source panels.

The records preserve these discrepancies rather than choosing an exact
stereochemical trajectory. The [source challenge](../data/atlas/source_drafts/batches/plp-pyruvoyl/review/challenge.json)
and [batch attribution](../data/atlas/source_drafts/batches/plp-pyruvoyl/SOURCE_ATTRIBUTION.md)
identify the evidence and reviewed scope. These four examples do not resolve
the entire PLP crosswalk row or establish conserved function in homologues.

The aldolases share source EC 4.1.2.13 and entry-level participant identifiers
while describing metal-assisted and covalent Schiff-base chemistry. M0222's
Step 1 prose and diagram disagree about the substrate, and its rabbit reference
identity coexists with archaeal mechanism statements. M0219 retains two
proposals with different reaction and protein contexts, a prose/diagram
participant conflict, and unresolved native-metal identity. These conflicts
remain explicit abstentions; entry-level matches do not resolve them.

In particular, the carrier owner/attachment gaps, unknown complete nitrogenase
cluster pathway, and conflicting HisF Asp11/Asp130 roles remain visible in the
query. Source transcription does not settle those questions or infer geometry,
atom mappings, balanced bond edits, or experimental validation.

Step `is_inferred` is true when the text contains an explicit `inferred` tag,
`we infer`, or `we assume`; otherwise it is null (unspecified). The retained
text determines whether the inference qualifies a role within the step or
the whole step. Missing markers do not establish observation, and other source
hedging is retained without automatically assigning a boolean value.

## Use the atlas

The installed wheel includes the compiled drafts and attribution. Query it
without the repository, raw downloads, a model, or a network connection:

```bash
catalytic-earth atlas-drafts --mcsa-id M0107 --steps
catalytic-earth atlas-drafts --assembly cycle_coupled_association
catalytic-earth atlas-drafts --text lipoyl
catalytic-earth atlas-drafts --product CHEBI:16526
catalytic-earth atlas-drafts --reactant CHEBI:28938 --product CHEBI:58278
catalytic-earth atlas-drafts --batch aldolase-transketolase --reactant 57642 --reactant 59776 --product 49299
catalytic-earth atlas-drafts --batch aldolase-transketolase --mcsa-id M0219 --steps
catalytic-earth atlas-drafts --batch aldolase-transketolase --mcsa-id M0222 --text "DHAP-derived covalent moiety"
catalytic-earth atlas-drafts --batch all --mechanism-component "schiff base formed"
catalytic-earth atlas-drafts --batch all --mechanism-component decarboxylation --product 16526
catalytic-earth atlas-drafts --batch plp-pyruvoyl --mechanism-component decarboxylation --steps
catalytic-earth atlas-drafts --batch plp-pyruvoyl --mechanism-component dehydration --mechanism-component "schiff base formed"
catalytic-earth atlas-drafts --batch plp-pyruvoyl --mechanism-component "reaction occurs outside the enzyme"
catalytic-earth atlas-drafts --batch plp-pyruvoyl --reactant 57972 --product 57416
```

Compact results omit step bodies while retaining scope, residue evidence and
abstentions. `--steps` includes the ordered source steps and available electron
flows. An empty result means no matching record in this bounded batch; it is
not a claim that no such mechanism exists elsewhere. Every response identifies
the selected source IDs and requested operation, including empty results.
The default selects the original four records. `--batch aldolase-transketolase`
selects the additional three; it does not silently expand the default corpus.
`--batch plp-pyruvoyl` selects the next four. Its four examples above retrieve
M0049, M0066, M0186 and M0213 respectively. These are exact source-annotation
queries, not normalized reaction-class or cofactor classification. In
particular, text search for PLP can also match an abstention explaining why
pyruvoyl is not PLP.
The paired aldolase query above returns both source records and their separate
proposal, residue and uncertainty fields.

The additional batch now includes a reviewed primary-evidence annotation for
M0222. The preserved 2QUT structure supports a DHAP-derived covalent moiety at
author Lys229, mapped to P00883 Lys230. Its deposited description and primary
paper assign an enamine. This narrows the source's G3P/DHAP conflict at the
covalent-moiety scope. The engineered, chemically reduced 1J4E trap is separate
corroboration. [2QUT](https://www.rcsb.org/structure/2QUT),
[1J4E](https://www.rcsb.org/structure/1J4E).

Annotations do not rewrite the source record, remove its whole-step or
protein-applicability abstentions, assign a free-metabolite ChEBI identity to
the bound adduct, or change evidence tiers. Annotated responses use query
schema v2 and include `primary_evidence_annotations` in compact and full
results; text search includes those annotations. Calls without a sidecar,
including the default batch, retain query schema v1 unless a mechanism-component
filter is used.

### Search source mechanism events across batches

`--mechanism-component` matches a complete label from a proposal's
`components_summary`. Matching trims surrounding whitespace and ignores case;
it does not expand synonyms or match substrings. Repeat the flag to require
every label in **one proposal**. For example, M0107 proposal 2 names
`decoordination from a metal ion`, while proposal 3 names `decarboxylation`.
Searching for both returns no match instead of combining the two alternatives.

Each matching record retains all its proposals and gains
`mechanism_component_matches`: the proposal ID, source mechanism ID, original
summary and matched source labels. These filtered results use query schema v3;
compact and full results carry identical witnesses and uncertainty. Chemical
filters still apply to the entry-level reaction, so their intersection with an
event label does not assign the matched participant to that proposal or step.

`--batch all` applies the query separately to each available batch. Its catalog
response contains `batches`, each with `batch_id` and its complete `result`,
including selection and review metadata even when empty. It also reports the
searched batch IDs, searched record count, matching record count, and, for event
filters, matching proposal count. The default batch remains the original four
records. Existing single-batch responses are unchanged when event filters are
unused; this aggregation creates no combined scientific source bundle.

The Schiff-base label query finds M0753 HisF, M0222 class I aldolase, M0049
pyruvoyl decarboxylase, M0066 transaminase and M0213 racemase. The label is
shared across different chemistry and attachment contexts. M0186's proposal
does not contain that label even though its prose describes substrate–PLP
adduct chemistry; a missing annotation does not exclude that chemistry. Source labels do not
locate events to individual steps, establish conserved function, or validate
mechanisms. A missing label means no matching annotation in the selected
source summaries, not absence of that chemistry from the enzyme.

Chemical filters accept ChEBI identifiers or their numeric part. Repeat
`--participant` (either side), `--reactant` (left), or `--product` (right) to
require every specified participant within one source record. They intersect
with record ID, assembly and text filters. Left and right refer to the source
drawing, without establishing physiological direction or a balanced reaction.

The carbon-dioxide query (`CHEBI:16526`) returns both M0106 and M0107; adding
reactant pyruvate (`CHEBI:15361`) narrows it to M0106. Ammonium (`CHEBI:28938`)
is drawn on the right in M0212 and on the left in M0753. Results retain the
matching participant rows and source counts, all mechanism alternatives, and
the record's scope and abstentions. A participant match is entry-level context;
it does not assign that compound to every mechanism proposal or elementary step.

The dependency-free SQLite index uses exact source ChEBI identifiers. It does
not expand ontology classes, collapse protonation states, or infer equivalent
reactions from a shared participant. Records with unmapped participants remain
available through the other filters; an identifier query cannot match those
unmapped rows.

## Evidence for individual source steps

The PLP/pyruvoyl batch has an optional, reviewed context sidecar for all 32
nonterminal source steps. It binds each annotation to the exact record,
proposal, step and captured scheme hash. The original source bundles remain
unchanged. Opt in to the additional step fields with `--step-evidence` or any
step filter:

```bash
catalytic-earth atlas-drafts --batch plp-pyruvoyl --step-evidence
catalytic-earth atlas-drafts --batch all --step-cofactor PLP
catalytic-earth atlas-drafts --batch plp-pyruvoyl --step-cofactor pyruvoyl
catalytic-earth atlas-drafts --batch plp-pyruvoyl --step-enzyme-context extra_enzymatic
catalytic-earth atlas-drafts --batch plp-pyruvoyl --step-source-assertion explicitly_inferred
catalytic-earth atlas-drafts --batch plp-pyruvoyl --step-source-assertion explicitly_assumed
```

Cofactor filters match literal labels in a step's source text, with only
whitespace trimming and case folding. PLP retrieves witnessed steps from
M0066/M0186/M0213; pyruvoyl retrieves witnessed steps from M0049. These labels
are not normalized cofactor states, and their absence from a step annotation
does not mean that the chemistry lacks that cofactor.

The extra-enzymatic query returns M0186 Steps 6 and 7 with their distinct
scheme hashes. Combining it with `--step-cofactor PLP` returns no match:
the PLP and outside-enzyme descriptions belong to different steps. All step
filters must match one annotation; combining a step filter with a mechanism
component also requires the same proposal. Entry participant filters remain
entry-scoped and do not resolve the chemical identity of a matching step.

An inferred query preserves the difference between M0049's inferred Step 7
and the inferred phosphate role within M0186 Step 4. The assumed acid role
within M0186 Step 5 is separate. `source_silent` means no recognized explicit
infer/assume marker, never that a step was observed or established. Other
uncertainties and source conflicts remain visible in the witnesses and limits.

Compact and full results carry the same annotation witnesses, scope and
abstentions, plus complete step summaries and separately scoped proposal text.
This preserves qualifications that a selected actor/role fragment cannot
express, including M0186's conditional concerted model and uncertain water
identity. Linked primary observations retain their original record or
proposal scope; attaching one does not establish the exact step trajectory.
Unresolved native/analogue context remains unresolved. Neither source arrows
nor a source text annotation establishes atom mapping, bond edits, precise
protonation, a full catalytic trajectory or an exact reaction instance.

The [M0049 primary audit](../data/atlas/source_drafts/batches/plp-pyruvoyl/review/primary_sources/SOURCE_ATTRIBUTION.md)
adds a record-level observation of the deposited pyruvoyl component in 1PYA.
It distinguishes processed chain-F label position **1** from PDB author
residue **82**. Current and historical structure records preserve that
processed component. The separate audit crosswalk places the precursor
serine at current UniProt P00862 position **83**; the typed v1 annotation
leaves sequence mapping unasserted because its evidence types cannot express
the curated protein record honestly. The standard-residue alignment excludes
the modified label-1 component and is insufficient by itself for that mapping.

The structure supports a processed state. It does not establish the precursor
cleavage trajectory or settle the M-CSA substrate-identifier conflict.
Historical literature identifies the Ser81–Ser82 cleavage bond; that statement
is kept separate from M-CSA's Prv-82 label. The retained raw structures and
UniProt record, acquisition receipts, scoped projection and source inventory
are available in the audit directory; only the reviewed annotation and source
hashes enter the wheel.

## Query deposited structural contexts

Typed primary contexts distinguish a processed protein component, a
source-designated analogue, a source-described bound adduct, and a
deposit-described covalent intermediate. These are
record-level observations with explicit evidence paths; they do not establish
the identity or trajectory of any matching proposed step.

```bash
catalytic-earth atlas-drafts --batch all --observed-state-context
catalytic-earth atlas-drafts --batch all --observed-state bound_ligand_analogue --observed-component PDD
catalytic-earth atlas-drafts --batch plp-pyruvoyl --observed-component PYR
catalytic-earth atlas-drafts --batch plp-pyruvoyl --observed-state bound_ligand_adduct --step-enzyme-context extra_enzymatic
catalytic-earth atlas-drafts --batch all --observed-state protein_ligand_covalent_adduct --observed-component 13P
```

M0049's typed context separates the directly deposited PYR author82/label1
site from the curated correspondence to precursor Ser83. The older v1
observation remains unchanged; the additional context is not a second
independent observation. Standard alignment alone cannot establish that
modified-site correspondence.

M0213's 1L6G context retains the primary abstract's explicit analogue
designation for PDD, its two deposited instances, and their distinct numbering
namespaces. The second instance is atom-author B1390 but nonpolymer
source-author 390, with no polymer label sequence position. No deposited PDD
protein connection is listed. The structure's four other covalent connection
rows do not establish PDD attachment, and absence from that table does not
prove a physical noncovalency claim.

M0186's 1PWH context is a PLV bound adduct. The inspected primary abstract
describes an aldimine and says dehydration did not occur; deposited chemistry
assigns a single N–C4A bond. Both descriptions and their unresolved
disagreement remain visible. The abstract does not explicitly designate an
analogue, and the annotation does not establish a native intermediate,
protonation state, acid/base role or subsequent trajectory.

M0222's additive 2QUT context describes four deposited `13P` instances, each
with its exact Lys229 NZ–ligand C2 covalent connection. It preserves protein
and ligand author/label namespaces, connection IDs and distances. Deposited
bond order remains unknown (`source_bond_order_code=null`, raw token `?`).
The generic 13P component dictionary contains C2–O2 `doub`, while all four
modeled instances omit O2; the generic dictionary cannot supply the bound
moiety's topology. The deposit title/remark supplies its enamine description.
The inspected abstract's native-enzyme versus Lys146Met comparison remains
separately scoped, with detailed preparation conditions and exact
publication-era coordinate bytes unasserted.

This refines the existing 2QUT observation and does not add independent
experimental evidence. The original v1 annotation retains the separately
supported author Lys229 to UniProt Lys230 mapping. New typed attachment rows
leave canonical mapping unasserted. The separately reduced 1J4E trap remains
corroboration in the old annotation; M0219's computational template context
does not become an observed chemical state.

Observed-state filters match one typed annotation. Component matching only
trims whitespace and folds case: `PDD` does not match free PLP or a ChEBI
participant. Combining an observed-state filter with a step filter joins at
the record level and explicitly reports `observed_state_grounds_step=false`.
For example, the last query returns M0186's separately described outside-enzyme
Steps 6 and 7 alongside its structural context; the bound adduct does not
validate those steps.

Single-batch opt-in output uses query schema v5; catalog output uses v3.
Compact and full results preserve the same selected `observed_state_contexts`
and complete primary annotations. Projection excerpts retain evidence edges
and source locators; `primary_evidence.source_bindings` identifies captured
source files, curated references and reviewed factual article projections.
An article-projection hash does not claim to bind a retained full article.
`observed_state_context_count` counts typed
annotations, not independent observations. There are four typed contexts
across the eleven source records. Existing aldolase and transketolase
primary annotations keep their original record/proposal scope and are not
automatically reclassified into this new type. An empty typed result therefore
means no matching reviewed typed annotation, not an absence of evidence or
chemistry. Default queries keep their existing field layout.

## Rebuild and extend

```bash
python scripts/build_atlas_draft_sources.py --check
python scripts/build_atlas_drafts.py --check
python scripts/build_atlas50_state_probe.py --batch aldolase-transketolase --check
python scripts/build_atlas50_development_gate.py --batch aldolase-transketolase --check
python scripts/build_atlas_draft_sources.py --batch aldolase-transketolase --check
python scripts/build_atlas_drafts.py --batch aldolase-transketolase --check
python scripts/build_atlas50_state_probe.py --batch plp-pyruvoyl --check
python scripts/build_atlas50_development_gate.py --batch plp-pyruvoyl --check
python scripts/build_atlas_draft_sources.py --batch plp-pyruvoyl --check
python scripts/build_atlas_drafts.py --batch plp-pyruvoyl --check
python scripts/run_test_tier.py "core/unit"
python scripts/validate_repository_contracts.py
```

Source acquisition requires an explicit `--fetch`; checks and compilation are
offline. The downloader verifies authorizations, enforces request and byte
budgets before and during transfer, and retains source receipts, hashes,
unavailable-scheme status and attribution. The manifest specifies the selected
IDs; subsequent permitted batches use the same importer and compiler.
Batch paths are declared in `atlas_draft_batch.py`. Successor review inputs,
snapshots, manifests and compiled outputs live under their own batch directory;
inherited review decisions are pinned and checked. The additional batch used
31 recorded API/scheme requests and 569,327 bytes, plus three ancillary official
page inspections whose bytes are not represented as raw-source receipts.
The PLP/pyruvoyl batch inherits the nine prior decisions and adds four. Its
new identities absent from the frozen candidate list are checked against their
captured official snapshots; admission still requires the source challenge's
hash bindings and scoped adjudications. No frozen candidate list is extended.
The new source package used 37 API/scheme requests and 589,303 response bytes;
ancillary browser and source-label checks are disclosed separately from those
raw-package receipts.

The source API is the maintained M-CSA interface; its old flat files are no
longer updated. Upstream also warns that homologous residue matches do not
establish conserved catalytic function. [M-CSA API documentation](https://www.ebi.ac.uk/thornton-srv/m-csa/download/)

Source redistribution follows [the recorded attribution](../data/atlas/source_drafts/SOURCE_ATTRIBUTION.md)
and CC BY 4.0 terms. Only compiled projections and attribution enter the wheel.
The source snapshots remain in the repository source package.
The additional batch has [its own attribution](../data/atlas/source_drafts/batches/aldolase-transketolase/SOURCE_ATTRIBUTION.md).
The [primary-evidence audit package](../data/atlas/source_drafts/batches/aldolase-transketolase/review/primary_sources/SOURCE_ATTRIBUTION.md)
retains the exact 2QUT mmCIF and a project-authored field projection. Its inventory
explicitly records that the original research download had no saved HTTP
receipt. The wheel contains only the reviewed annotation and source hashes.
Changing annotation content or an audit input invalidates the manually reviewed
payload pin; ordinary compilation cannot refresh that scientific review pin.
The validator checks integrity and declared scope. It does not rederive free-form
scientific claims or residue mappings from coordinates; those require the
recorded source-to-claim review. Recomputing a pin is not scientific evidence.

## Priority rule

Choose the next batch or compiler improvement by the bottleneck it removes
from building the full computable atlas. A demonstration, benchmark, new
review layer or larger row count is not an automatic prerequisite. Add one
when its result will change what we build, admit, or spend effort on. The
current query layer makes the existing standardized participants usable across
records. Reassess the next coverage or mechanism-query improvement against the
remaining bottleneck, with source applicability handled at its affected scope.
