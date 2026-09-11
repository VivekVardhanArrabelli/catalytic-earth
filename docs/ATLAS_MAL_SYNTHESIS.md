# A preparative methylaspartate ammonia-lyase outcome

Raj2012 reports **65% conversion after seven days** and **50% yield after purification**
when the L384A methylaspartate ammonia-lyase mutant adds ammonia to
2-(benzyloxy)-fumaric acid (1j), producing 3-benzyloxyaspartic acid (4j).
These are separate published preparative endpoints, not a kinetic rate or a
measured improvement over wild type. [CE-043](../CLAIMS.md) controls the scope;
[the truth policy](ATLAS_TRUTH_POLICY.md) and [errata](../ERRATA.md) remain in force.

The [source packet](../data/atlas/study_context/mal_2012/source_qualification.json)
binds the [publisher's primary supplement](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fnchem.1338/MediaObjects/41557_2012_BFnchem1338_MOESM144_ESM.pdf):
substrate 1j on p22, the preparative scheme and protocol on pp25–26, and the
product entry on pp29–30. The exact DOI, authors and publisher hyperlink bind
the source. The article body remains uninspected. Source bodies and rendered
pages are local reference material and are not redistributed.

| Relation | Source-supported scope |
| --- | --- |
| Construct | Source-named C. tetanomorphum MAL L384A, from the pBAD(MAL-His) lineage; no exact assayed sequence is reconstructed |
| Inputs | 3.1 mmol unsaturated acid, 31 mmol ammonium chloride and 20 mM MgCl2, prepared in 25 mL water at pH 9 |
| Preparation | 5 mg freshly purified enzyme initially, another 5 mg after two days, 22 °C, seven-day endpoint |
| Conversion | 65%, reported from proton NMR after seven days |
| Isolation | 50% yield after workup and cation-exchange purification |
| Product identity | Reported proton/carbon NMR and HRMS support the named 4j product at source scope |

The product entry labels the parameter “Yield.” Its classification as
`isolated_yield` in the shared consumer is an interpretation of the stated
purification workflow, not a verbatim source label. The supplement does not
name Q05514; that accession association comes from UniProt’s Raj2012 citation.

The source solution volume does not specify the volume of added pH titrant.
Ammonium chloride is the supplied material; the scheme names ammonia as the
nucleophile. No free-ammonia concentration, microscopic protonation state,
enzyme molarity or productivity is calculated. Replicates and statistical
uncertainty are not reported for these selected preparative endpoints.

## Selectivity and mutation limits travel with the result

The inspected 4j drawing has no stereobonds. Its HPLC entry gives a
`threo-DL-4j` retention pair of 5.0 and 6.9 minutes without assigning an
enzymatic product peak or absolute configuration to either time. The publisher
abstract describes a highly enantio- and diastereoselective threo example;
that qualitative author claim stays separate from the two quantified outcomes.
The query leaves numerical ee/de and absolute configuration null. It does not
borrow the Q73A product series' selectivity or interpret a single NMR signal
set as proof of an enantiopure product.

The supplement also reports that Q73A/L384A is almost completely inactive,
with data not shown (p40). It supplies no specific substrate pair, assay,
scalar or uncertainty for that statement. This cautions against combining the
two single mutants' substrate scopes by assumption, while supplying neither
a numerical epistasis estimate nor proof of a changed active-site geometry.
No wild-type or double-mutant comparison is computed for the 4j outcome.

M0468's catalytic-site declarations do not include L384A's reference position.
Neither that source mechanism nor a crystal or docking model is transferred
to this preparative reaction. Exact construct, reacted-state geometry and a
complete elementary mechanism remain unresolved.

## Reuse and evidence boundary

```sh
python scripts/query_atlas_perturbations.py --study mal_2012 --verify-witnesses --output /tmp/mal-outcome.json
```

The existing consumer projects the conversion and isolation records with their
shared source outcome context, reaction participants, assays and product limits.
It uses the same reaction and outcome representation as the prior RA95
synthesis, without a new enzyme-specific branch or parameter type. Previous
observations and comparisons retain their meaning. Two parameter records are
not two new experiments, proteins or mechanisms.

This extends reusable synthetic outcome evidence to another reaction class.
It does not establish measured curation savings, superior search performance,
prospective enzyme-design performance or independent validation. The current
batch `engineered-methylaspartate-raj2012` used six requests and 2,374,099
response-body bytes; its cumulative ceiling remains 100 requests and 30 MiB.
The [acquisition receipt](../data/atlas/study_context/mal_2012/acquisition_receipts.json)
records redirects and errors, and the
[computational review](../data/atlas/study_context/mal_2012/source_review.json)
preserves the source objections and scope decisions.
