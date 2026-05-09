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
python -m catalytic_earth.cli build-v1-graph --max-mcsa 50 --page-size 50 --out artifacts/v1_graph.json
python -m catalytic_earth.cli graph-summary --graph artifacts/v1_graph.json --out artifacts/v1_graph_summary.json
python -m catalytic_earth.cli build-v2-benchmark --graph artifacts/v1_graph.json --out artifacts/v2_benchmark.json
python -m catalytic_earth.cli run-baseline --benchmark artifacts/v2_benchmark.json --out artifacts/v2_baseline.json
python -m catalytic_earth.cli detect-inconsistencies --graph artifacts/v1_graph.json --out artifacts/v2_inconsistencies.json
python -m catalytic_earth.cli mine-dark-hydrolases --limit 100 --out artifacts/v2_dark_hydrolase_candidates.json
python -m catalytic_earth.cli write-dossiers --candidates artifacts/v2_dark_hydrolase_candidates.json --out-dir artifacts/v2_dossiers --top 10
python -m catalytic_earth.cli write-v2-report --out docs/v2_report.md
python -m catalytic_earth.cli build-geometry-features --graph artifacts/v1_graph.json --max-entries 20 --out artifacts/v3_geometry_features.json
python -m catalytic_earth.cli run-geometry-retrieval --geometry artifacts/v3_geometry_features.json --out artifacts/v3_geometry_retrieval.json
python -m catalytic_earth.cli label-summary --out artifacts/v3_label_summary.json
python -m catalytic_earth.cli evaluate-geometry-labels --retrieval artifacts/v3_geometry_retrieval.json --out artifacts/v3_geometry_label_eval.json
python -m catalytic_earth.cli log-work --stage v0 --task "example work entry" --minutes 1
python -m catalytic_earth.cli progress-report --out work/status.md
python -m unittest discover -s tests
```

The commands currently operate on curated seed registries in `data/registries/`.
The first source-specific adapters fetch small Rhea and M-CSA samples and build
a seed graph linking M-CSA entries, EC numbers, catalytic residues, and Rhea
reactions.

The v1 graph command expands this into a persistent graph slice linking M-CSA,
Rhea, UniProt, PDB, and AlphaFold DB cross-references.

## Repository Layout

```text
data/registries/        Seed source and mechanism registries
docs/                   Research protocol and design notes
src/catalytic_earth/    Validation and artifact-building code
tests/                  Unit tests for the v0 scaffold
artifacts/              Generated local outputs
work/                   Time ledger, scope calibration, and handoff state
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
