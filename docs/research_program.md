# Catalytic Earth Research Program

## Problem

Protein biology now has massive sequence and structure coverage, but chemical
function remains poorly mapped. EC numbers, names, and broad annotations do not
capture the mechanism-level information that enzymologists actually need:
catalytic residues, residue roles, geometry, cofactors, substrate constraints,
reaction bond changes, promiscuity, and confidence.

The central research question is:

```text
Can uncharacterized proteins be mapped to catalytic mechanism hypotheses at
scale, with uncertainty and experimental testability?
```

## Core Claim

The missing foundation layer is not another protein classifier. It is a
mechanism coordinate system for catalysis.

## Year-One Objective

Build the first credible open scaffold for a catalytic atlas:

1. Curate a machine-readable source registry.
2. Define and test a mechanism fingerprint language.
3. Build a catalytic knowledge graph prototype.
4. Create mechanism-level prediction benchmarks.
5. Mine dark enzyme space for one valuable chemistry.
6. Produce candidate dossiers suitable for expert wet-lab review.

## V0: Foundation

V0 establishes the research grammar.

- Define the mechanism fingerprint schema.
- Build source registry and provenance model.
- Seed representative mechanism families.
- Create validation tools.
- Produce a first artifact ledger.

Success condition: the repo can represent enzyme evidence below EC-number level
without losing provenance or uncertainty.

## V1: Knowledge Graph and Benchmarks

V1 turns curated records into a graph and evaluation suite.

- Ingest Rhea reactions and UniProt mappings.
- Ingest M-CSA active-site and mechanism examples.
- Link PDB and AlphaFold structures where possible.
- Link chemistry through ChEBI/Rhea identifiers.
- Build held-out tests for mechanism prediction and misannotation.

Success condition: the system can ask and answer questions such as:

- Which proteins share an active-site architecture but differ in substrate class?
- Which annotations are inconsistent with catalytic residues or cofactors?
- Which reaction classes lack structural/mechanistic coverage?

## V2: Dark Enzyme Discovery Campaign

V2 performs one serious mining campaign.

Candidate target areas:

- Lignin deconstruction and aromatic compound transformation.
- Non-PET polyester or polyurethane transformation.
- Pollutant transformation where validated biology exists but coverage is thin.

The output is not validated enzyme function. The output is a ranked experimental
queue with mechanistic rationale.

Each top candidate dossier should include:

- sequence identifier
- predicted or experimental structure
- active-site evidence
- cofactor and metal evidence
- likely substrate class
- competing annotations
- nearest characterized homologs
- recommended assay family
- negative controls
- failure modes

## Scientific Risks

- Static structures may miss catalytic conformations.
- Annotation databases contain propagated errors.
- Sequence similarity can hide substrate changes.
- Metagenomic proteins may be fragments or assembly artifacts.
- Ligand docking scores can be overinterpreted.
- Mechanism hypotheses can sound convincing while being chemically wrong.

The project should treat every candidate as an experimental hypothesis, not a
discovery claim.

## Current Scaling Boundary

The M-CSA-only label-factory path is now a seed benchmark, not the whole atlas.
The accepted 1,000 state has 679 countable labels, and the 1,025 preview adds 0
new countable labels while exposing 1,003 observed M-CSA source records. Scaling
toward 10,000 labels now requires an external-source transfer method, starting
with review-only UniProtKB/Swiss-Prot candidate manifests, lane-balance audits,
evidence requests, active-site evidence queues, OOD calibration,
sequence-similarity failure controls, Rhea reaction context, and the existing
heuristic retrieval baseline as a control.
None of those external-source artifacts can count as benchmark labels until
they pass the label factory through an explicit decision artifact.
