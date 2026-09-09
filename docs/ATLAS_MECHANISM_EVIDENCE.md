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

### Boundaries of the original abstract-only query

The sidecar pins the existing Atlas-10 payload, exact M0187 transformation,
proposal and source snapshot. P11444 is reference-site context: the H297N
abstract supplies no organism or UniProt identifier; the K166R abstract names
Pseudomonas putida and cites the H297N paper. Exact assayed construct sequences
were not inspected.

Neither inspected abstract supplies a mutant PDB accession. Existing Atlas
structure 1MNS is an inhibitor-bound, chemically modified Lys166 context;
it is not either mutant structure or a turnover observation. All seven changed
M0187 source atoms retain their unresolved site correspondence. This functional
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
