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

This repository has moved past the initial v0 scaffold. The current public state
is a scaffold-level V2 research artifact plus post-V2 active-site geometry,
ligand/cofactor context, substrate-pocket descriptors, curated seed labels,
abstention calibration, cofactor coverage audits, and local performance checks.

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

## Current State

The repository currently contains:

1. A bounded catalytic knowledge graph slice linking M-CSA, Rhea, UniProt, PDB,
   and AlphaFold DB references.
2. A mechanism fingerprint registry and benchmark builder with leakage controls.
3. A baseline retrieval system, inconsistency detector, dark-hydrolase mining
   campaign, and candidate dossier writer.
4. PDB mmCIF active-site geometry extraction for catalytic residues.
5. Nearby ligand/cofactor context from non-polymer mmCIF records.
6. Structure-wide ligand inventory for cofactor coverage audits.
7. Substrate-pocket descriptor extraction from nearby protein residues.
8. Curated mechanism labels for 450 entries, including all entries in the
   current 450-entry source slice.
9. Auth-vs-label mmCIF residue-number fallback for cleaner structure mapping.
10. Retrieval evaluation, abstention threshold calibration, hard-negative
    selection, in-scope failure analysis, cofactor coverage analysis,
    label-expansion candidate ranking, geometry slice summaries, and a local
    performance suite.

The 20- through 450-entry evaluation slices are clean out-of-scope regression
slices: each has 0 out-of-scope false non-abstentions and 0 hard negatives
under calibrated abstention. The 125-entry slice has 38 in-scope positives, 87
out-of-scope controls, 124/125 evaluable active-site structures, threshold
`0.4115`, and a positive score separation gap of `0.0308`.

The current 450-label stress slice has 449 geometry entries, 442 evaluable
active-site structures, 124 local active-site in-scope positives, 325 evaluated
out-of-scope controls, 0 ready label-expansion candidates, 7 labeled
out-of-scope structure-mapping issues, 0 hard negatives, and 0 near misses. Its
calibrated threshold is `0.4115`; it retains 120/124 in-scope positives,
abstains on all evaluable out-of-scope controls, and leaves 4 evidence-limited
in-scope abstentions (`m_csa:132`, `m_csa:353`, `m_csa:372`, and `m_csa:430`).
The current actionable in-scope failure count is 0 after separating
selected-structure cofactor gaps from scorer failures. Cofactor policy sweeps
recommend audit-only handling rather than a score penalty because no tested
penalty reduces retained evidence-limited positives without losing retained
positives. Cofactor coverage artifacts explicitly identify retained
evidence-limited positives: `m_csa:41`, `m_csa:108`, `m_csa:160`, and
`m_csa:446`.

An unlabeled 475-entry candidate queue has also been generated for the next
curation pass. It contains 474 geometry entries, 25 unlabeled candidate rows,
and 23 entries ready for label review, but it is not yet part of the curated
cross-slice benchmark summary.

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

python -m catalytic_earth.cli label-summary --out artifacts/v3_label_summary.json

python -m catalytic_earth.cli build-v1-graph --max-mcsa 450 --page-size 100 --out artifacts/v1_graph_450.json
python -m catalytic_earth.cli graph-summary --graph artifacts/v1_graph_450.json --out artifacts/v1_graph_summary_450.json
python -m catalytic_earth.cli build-v2-benchmark --graph artifacts/v1_graph_450.json --out artifacts/v2_benchmark_450.json
python -m catalytic_earth.cli build-geometry-features --graph artifacts/v1_graph_450.json --max-entries 450 --out artifacts/v3_geometry_features_450.json
python -m catalytic_earth.cli run-geometry-retrieval --geometry artifacts/v3_geometry_features_450.json --out artifacts/v3_geometry_retrieval_450.json
python -m catalytic_earth.cli calibrate-abstention --retrieval artifacts/v3_geometry_retrieval_450.json --out artifacts/v3_abstention_calibration_450.json
python -m catalytic_earth.cli evaluate-geometry-labels --retrieval artifacts/v3_geometry_retrieval_450.json --abstain-threshold 0.4115 --out artifacts/v3_geometry_label_eval_450.json
python -m catalytic_earth.cli analyze-geometry-failures --retrieval artifacts/v3_geometry_retrieval_450.json --abstain-threshold 0.4115 --out artifacts/v3_geometry_failure_analysis_450.json
python -m catalytic_earth.cli analyze-in-scope-failures --retrieval artifacts/v3_geometry_retrieval_450.json --abstain-threshold 0.4115 --out artifacts/v3_in_scope_failure_analysis_450.json
python -m catalytic_earth.cli analyze-cofactor-coverage --retrieval artifacts/v3_geometry_retrieval_450.json --abstain-threshold 0.4115 --out artifacts/v3_cofactor_coverage_450.json
python -m catalytic_earth.cli analyze-cofactor-policy --retrieval artifacts/v3_geometry_retrieval_450.json --abstain-threshold 0.4115 --out artifacts/v3_cofactor_policy_450.json
python -m catalytic_earth.cli analyze-seed-family-performance --retrieval artifacts/v3_geometry_retrieval_450.json --abstain-threshold 0.4115 --out artifacts/v3_seed_family_performance_450.json
python -m catalytic_earth.cli analyze-geometry-score-margins --retrieval artifacts/v3_geometry_retrieval_450.json --out artifacts/v3_geometry_score_margins_450.json
python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_450.json --out artifacts/v3_hard_negative_controls_450.json
python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_450.json --retrieval artifacts/v3_geometry_retrieval_450.json --out artifacts/v3_label_expansion_candidates_450.json
python -m catalytic_earth.cli analyze-structure-mapping-issues --geometry artifacts/v3_geometry_features_450.json --out artifacts/v3_structure_mapping_issues_450.json
python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
python -m catalytic_earth.cli perf-suite --graph artifacts/v1_graph_450.json --geometry artifacts/v3_geometry_features_450.json --retrieval artifacts/v3_geometry_retrieval_450.json --iterations 5 --out artifacts/perf_report.json

python -m catalytic_earth.cli log-work --stage post-v2 --task "example work entry" --minutes 1
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
tests/                  Unit tests for graph, retrieval, labels, and structure code
artifacts/              Generated local outputs
work/                   Time ledger, scope calibration, and handoff state
```

## Roadmap And Timeline Calibration

The original "one year to v2" framing was too conservative for scaffold
construction. In practice, v0-v2 plus several post-V2 quality upgrades were
implemented quickly because they are bounded computational artifacts, not
expert-validated enzyme discoveries.

Current timeline judgment:

1. Done: public repo, graph slice, mechanism fingerprints, V2 benchmark,
   retrieval baseline, inconsistency detection, dark-enzyme candidate dossiers,
   active-site geometry, ligand/cofactor context, labels, calibration, and
   performance checks.
2. Next automation blocks: curate the generated 475-entry candidate queue while
   preserving 0 hard negatives, 0 near misses, and 0 out-of-scope false
   non-abstentions across the 20- through 450-entry slices.
3. Next serious milestone: expand beyond 450 labels or resolve the
   evidence-limited abstentions (`m_csa:132`, `m_csa:353`, `m_csa:372`, and
   `m_csa:430`) by improving structure/cofactor evidence, while preserving the
   current hard-negative guardrails.
4. Long-term impact path: expert-reviewed mechanism labels, learned
   geometry-aware retrieval, source-scale ingestion, and candidate dossiers that
   are credible enough for external labs to prioritize.

So the near-term scope is not "build a dashboard for a year." It is to keep
turning fast scaffold progress into increasingly hard, falsifiable mechanism
benchmarks. Real-world impact still requires expert review and wet-lab
validation outside this repository.
