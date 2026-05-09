# Catalytic Earth

Catalytic Earth is an open research scaffold for a mechanism-level atlas of enzyme
function. The goal is to make enzyme function searchable by catalytic mechanism,
not only by name, EC number, keyword, or sequence similarity.

## North Star

Build a computable map from protein sequence and structure to chemical function:

```text
protein sequence
+ predicted or experimental structure
+ active-site geometry
+ catalytic residue roles
+ cofactor and metal dependence
+ substrate-pocket constraints
+ reaction bond changes
+ evolutionary context
= mechanism-level function hypothesis
```

This repository starts the v0 foundation for that map.

## What This Is

- A research program for mechanism-first enzyme discovery.
- A schema for enzyme mechanism fingerprints.
- A registry of public data sources needed for a catalytic knowledge graph.
- A small executable validation and artifact-building pipeline.
- A base for later ingestion, benchmarking, model training, and discovery campaigns.

## What This Is Not

- It is not a wet-lab protocol.
- It is not a claim that computational candidates are validated enzymes.
- It is not a biological design system for harmful functions.
- It is not an EC-number classifier dressed up as mechanistic discovery.

## Quickstart

From this directory:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m catalytic_earth.cli validate
python -m catalytic_earth.cli build-ledger --out artifacts/source_ledger.json
python -m catalytic_earth.cli fingerprint-demo --out artifacts/mechanism_demo.json
python -m catalytic_earth.cli fetch-rhea-sample --limit 10 --out artifacts/rhea_sample.json
python -m catalytic_earth.cli fetch-mcsa-sample --ids 1,2,3 --out artifacts/mcsa_sample.json
python -m catalytic_earth.cli build-seed-graph --mcsa-ids 1,2,3 --out artifacts/seed_graph.json
python -m unittest discover -s tests
```

The commands currently operate on curated seed registries in `data/registries/`.
The first source-specific adapters fetch small Rhea and M-CSA samples and build
a seed graph linking M-CSA entries, EC numbers, catalytic residues, and Rhea
reactions.

## Repository Layout

```text
data/registries/        Seed source and mechanism registries
docs/                   Research protocol and design notes
src/catalytic_earth/    Validation and artifact-building code
tests/                  Unit tests for the v0 scaffold
artifacts/              Generated local outputs
```

## First-Year Research Shape

The year-one version should produce:

1. A catalytic knowledge graph.
2. A mechanism fingerprint language.
3. Benchmarks for mechanism prediction, substrate specificity, and misannotation.
4. A dark-enzyme mining pipeline.
5. One deep discovery campaign with lab-ready candidate dossiers.

The first campaign should target a hard but bounded chemistry where public data
exist and wet-lab validation would be plausible later, such as lignin
deconstruction or non-PET polyester/polyurethane transformation.
