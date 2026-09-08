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
```

The dependency-free wheel returns one case containing six published-observation
projections, two competing explanations, explicit discriminants and a reviewed
project adjudication. Filters select observations within each case while keeping
the **complete case, adjudication and abstentions** alongside the selected rows.
The two commands with filters match two observations each. An empty result
means no matching retained observation; it is not evidence of absent chemistry.
`--output` writes a new JSON file and refuses to overwrite an existing file.

The [evidence sidecar](../data/atlas/mechanism_evidence/m0187/evidence.json)
records results separately from source interpretation and project diagnosis.
`not_detected` has a null value, not zero. Numerical results here are reported
fold reductions, not absolute rates or new measurements. Only the H297N
S-exchange comparison explicitly identifies WT in the inspected abstract.

## Provenance and unresolved links

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
