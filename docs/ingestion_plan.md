# Ingestion Plan

## Principle

Ingestion starts from mechanism-centered sources, not the largest sequence
repositories. The first adapters should make reaction and catalytic-site evidence
usable before scaling to millions of proteins.

## Source Order

1. Rhea
   - Reason: expert-curated reactions, ChEBI participants, UniProt mapping.
   - First artifact: sampled reaction records with reaction identifiers and
     equations.

2. M-CSA
   - Reason: curated catalytic residues, residue roles, mechanism text, PDB and
     UniProt links.
   - First artifact: sampled entries normalized to enzyme, EC, reaction,
     catalytic residues, and mechanism snippets.

3. UniProt
   - Reason: sequence and cross-reference backbone.
   - First artifact: accession-centered records linked to Rhea and structures.

4. PDB and AlphaFold DB
   - Reason: experimental and predicted structural evidence.
   - First artifact: structure availability and confidence metadata for
     proteins already linked to Rhea/M-CSA.

## V0 Adapter Rules

- Fetch small samples first.
- Store normalized JSON artifacts, not raw database mirrors.
- Preserve source URLs and retrieval metadata.
- Do not redistribute restricted data without checking license terms.
- Treat all annotations as evidence, not truth.

## Current Commands

```bash
python -m catalytic_earth.cli fetch-rhea-sample --limit 25 --out artifacts/rhea_sample.json
python -m catalytic_earth.cli fetch-mcsa-sample --ids 1,2,3 --out artifacts/mcsa_sample.json
```
