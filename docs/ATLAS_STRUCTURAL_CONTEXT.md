# Catalytic arrangements need a chemical-state context

The atlas can now compare selected catalytic atoms from the retained trypsin
and subtilisin structures while preserving deposited covalent modifications,
alternate conformations, occupancy, residue numbering and source provenance.
This exposes a consequential limit on the existing subtilisin reference:
**1SUP has an unmutated protein sequence but a chemically modified catalytic
serine.** It must not be used as an unmodified productive arrangement.

## What the retained sources establish

The [1SUP deposition](https://www.rcsb.org/structure/1SUP) records
`_struct_conn.covale1` between Ser221 OG and PMS278 S. The separate
`_pdbx_modification_feature` category explicitly identifies a covalent chemical
modification. This connects P00782 Ser328 (natural sequence numbering) to
1SUP author/label Ser221, without altering the inherited residue mapping.
The deposited PMS atoms have occupancy 0.70. His64 (P00782 His171) has
alternatives A and B with occupancies 0.80 and 0.20.

Calculated from the retained coordinates:

| Protein/structure | Ser OG–His NE2 distance | Deposited His alternative / occupancy |
| --- | ---: | --- |
| Trypsin, 1PQ5 | 2.976 Å | No alternative identifier / 1.00 |
| Subtilisin, 1SUP | 7.347 Å | A / 0.80 |
| Subtilisin, 1SUP | 3.214 Å | B / 0.20 |

These are distances between deposited model coordinates, not new experimental
measurements or optimal catalytic restraints. The closer B conformation does
not identify an active fraction. No joint occupancy between PMS and either
histidine conformation is established. The [1PQ5 deposition](https://www.rcsb.org/structure/1PQ5)
is explicitly at pH 5 and includes ARG703 with atom-specific partial occupancies
(0.19–0.48 for the retained heavy atoms). The primary paper describes an
autoproteolytic arginine/peptide fragment and maps 1PQ5 to pH 5 in Table II.
This is not an intact substrate model or an assignment to an elementary step.

The primary structure papers are DOI
[10.1107/S0907444996007500](https://doi.org/10.1107/S0907444996007500) and
[10.1074/jbc.M306944200](https://doi.org/10.1074/jbc.M306944200).
This increment inspected both retained mmCIF records and official entry pages.
The source-review agent inspected the six-page trypsin paper; root checked its
relevant passages and rendered Table II. The subtilisin paper was inspected at
the official abstract/deposition depth. Diffraction data were not re-refined.
The subtilisin state conclusion rests on explicit deposited linkage and
modification records; coordinate distances alone do not establish chemical
bonds. The trypsin paper
[receipt](../data/atlas/structural_context/acquisition_receipts.json) records
one 318,096-byte local capture; the article PDF is not redistributed.

## Inspect and reuse

```sh
catalytic-earth atlas-structural-context
catalytic-earth atlas-structural-context --pdb-id 1SUP
catalytic-earth atlas-structural-context --site-id P35049:S204
python scripts/build_atlas_structural_context.py --check
```

The dependency-free package returns full matching contexts, including source
bindings, original site roles and mappings, deposited coordinates, all modeled
alternatives, selected-site connection records and the separately reviewed
interpretation. Site filtering retains the surrounding chemical context.
An empty query is absence from this bounded selection, not absence of a
catalytic arrangement. `--output` creates a new JSON file.

The shared extractor uses selections declared in
[the source specification](../data/atlas/structural_context/spec.json).
It has no enzyme-name or source-ID chemistry branches. The same fields select
Ser OG, both histidine nitrogens and both aspartate oxygens in both proteins.
All selected-residue atom rows are retained; the two Asp oxygen names are
never collapsed to a preferred contact. A connection inventory checks whole
selected residues so a modification on an atom outside a distance selection
is still exposed. Absent connections are scoped to the deposited table.
The current selection contract requires one unambiguous PDB mapping per site
and one context per PDB. Multiple-chain ambiguity, missing selected atoms,
or incomplete model coverage fail explicitly; this is not a universal
structural ingestion path.

Distances remain within one model. Distinct alternatives of the same residue
are mutually exclusive, while coexistence of alternatives on different
residues remains unresolved. Occupancy and B factors retain their deposited
meaning; neither becomes a kinetic population or a calibrated uncertainty on
the computed distance. Crystallographic symmetry transformations and an
occupancy-weighted mean arrangement are not constructed.

## Scientific contribution and boundary

The useful result is a corrected basis for comparing catalytic arrangements:
protein identity, chemical modification and conformer choice must travel
together. It prevents treating the inherited “unmutated target” annotation as
an unmodified catalytic state. The trypsin and subtilisin mechanisms still
illustrate a shared serine-protease strategy across different folds, without
transferring substrate specificity or a transition-state model.

A competent user of M-CSA, UniProt and a PDB viewer can retrieve these same
facts and calculate these distances. This work makes the exact joins and
state restrictions reusable by programs; it is not new biology, a demonstrated
accuracy or speed advantage, or proof of de novo design utility. It adds two
structural-context annotations to two existing cases, **zero additional
proteins, reactions or mechanism cases**. Atlas-3/10 snapshots remain intact.

The curation workflow now derives coordinates, alternatives, incident
connections and distances from one source selection, rather than copying those
facts into parallel manually maintained representations. Choosing chemically
meaningful atoms and interpreting the structure still requires source review.
No timing study was performed.

The next scientific bottleneck is a source-grounded substrate/intermediate
arrangement with compatible chemical state and functional evidence. That
would constrain reaction geometry beyond a catalytic triad. More triad
distances alone cannot provide a productive design template.

The verification protects source identity, dual residue numbering, distinct
alternate conformers, model separation, and retention of modifications outside
the chosen distance atoms. The core tier passed 465 tests (one skipped), and
repository contracts passed. The installed wheel reproduced the queries from
an empty directory with network connections blocked; the frozen Atlas-10
runtime result and protected historical sources remain unchanged. These checks
establish faithful computation and packaging, not experimental validation.
