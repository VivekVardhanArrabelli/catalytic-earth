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
abstention calibration, and local performance checks.

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
6. Substrate-pocket descriptor extraction from nearby protein residues.
7. Curated mechanism labels for 100 entries, including all 100 entries in the
   current expanded geometry slice.
8. Auth-vs-label mmCIF residue-number fallback for cleaner structure mapping.
9. Retrieval evaluation, abstention threshold calibration, hard-negative
   selection, label-expansion candidate ranking, and a local
   performance suite.

The latest small-slice evaluation is intentionally modest: 100 geometry entries,
100 curated labels, 100 evaluable active-site structures, and 25 in-scope
seed-fingerprint positives. On the original 20-entry regression slice, adaptive
abstention finds a zero-false threshold that retains all 5 in-scope positives.
On the 100-entry slice, ligand/cofactor counterevidence plus the cobalamin seed
and a flavin-redox seed find a zero-false threshold that abstains on all 75
out-of-scope controls while retaining all 25 in-scope positives. There are
currently 0 hard negatives and 0 near misses in the 100-entry slice; the next
bottleneck is scale and label diversity, not more dashboard work.

A 125-entry staging slice has also been generated. It has 125 geometry entries,
25 currently unlabeled entries, 24 ready label-review candidates, and 1
unlabeled structure-mapping issue. Treat it as the next label-expansion work
queue, not as a fully audited benchmark yet.

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
python -m catalytic_earth.cli evaluate-geometry-labels --retrieval artifacts/v3_geometry_retrieval.json --abstain-threshold 0.565 --out artifacts/v3_geometry_label_eval.json
python -m catalytic_earth.cli calibrate-abstention --retrieval artifacts/v3_geometry_retrieval.json --out artifacts/v3_abstention_calibration.json
python -m catalytic_earth.cli analyze-geometry-failures --retrieval artifacts/v3_geometry_retrieval.json --abstain-threshold 0.565 --out artifacts/v3_geometry_failure_analysis.json
python -m catalytic_earth.cli analyze-geometry-score-margins --retrieval artifacts/v3_geometry_retrieval.json --out artifacts/v3_geometry_score_margins.json
python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval.json --out artifacts/v3_hard_negative_controls.json
python -m catalytic_earth.cli build-geometry-features --graph artifacts/v1_graph.json --max-entries 30 --out artifacts/v3_geometry_features_30.json
python -m catalytic_earth.cli run-geometry-retrieval --geometry artifacts/v3_geometry_features_30.json --out artifacts/v3_geometry_retrieval_30.json
python -m catalytic_earth.cli evaluate-geometry-labels --retrieval artifacts/v3_geometry_retrieval_30.json --abstain-threshold 0.565 --out artifacts/v3_geometry_label_eval_30.json
python -m catalytic_earth.cli calibrate-abstention --retrieval artifacts/v3_geometry_retrieval_30.json --out artifacts/v3_abstention_calibration_30.json
python -m catalytic_earth.cli analyze-geometry-score-margins --retrieval artifacts/v3_geometry_retrieval_30.json --out artifacts/v3_geometry_score_margins_30.json
python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_30.json --out artifacts/v3_hard_negative_controls_30.json
python -m catalytic_earth.cli build-geometry-features --graph artifacts/v1_graph.json --max-entries 40 --out artifacts/v3_geometry_features_40.json
python -m catalytic_earth.cli run-geometry-retrieval --geometry artifacts/v3_geometry_features_40.json --out artifacts/v3_geometry_retrieval_40.json
python -m catalytic_earth.cli evaluate-geometry-labels --retrieval artifacts/v3_geometry_retrieval_40.json --abstain-threshold 0.565 --out artifacts/v3_geometry_label_eval_40.json
python -m catalytic_earth.cli calibrate-abstention --retrieval artifacts/v3_geometry_retrieval_40.json --out artifacts/v3_abstention_calibration_40.json
python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_40.json --out artifacts/v3_hard_negative_controls_40.json
python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_40.json --retrieval artifacts/v3_geometry_retrieval_40.json --out artifacts/v3_label_expansion_candidates.json
python -m catalytic_earth.cli analyze-structure-mapping-issues --geometry artifacts/v3_geometry_features_40.json --out artifacts/v3_structure_mapping_issues_40.json
python -m catalytic_earth.cli build-geometry-features --graph artifacts/v1_graph.json --max-entries 50 --out artifacts/v3_geometry_features_50.json
python -m catalytic_earth.cli run-geometry-retrieval --geometry artifacts/v3_geometry_features_50.json --out artifacts/v3_geometry_retrieval_50.json
python -m catalytic_earth.cli evaluate-geometry-labels --retrieval artifacts/v3_geometry_retrieval_50.json --abstain-threshold 0.565 --out artifacts/v3_geometry_label_eval_50.json
python -m catalytic_earth.cli calibrate-abstention --retrieval artifacts/v3_geometry_retrieval_50.json --out artifacts/v3_abstention_calibration_50.json
python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_50.json --out artifacts/v3_hard_negative_controls_50.json
python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_50.json --retrieval artifacts/v3_geometry_retrieval_50.json --out artifacts/v3_label_expansion_candidates_50.json
python -m catalytic_earth.cli analyze-structure-mapping-issues --geometry artifacts/v3_geometry_features_50.json --out artifacts/v3_structure_mapping_issues_50.json
python -m catalytic_earth.cli build-v1-graph --max-mcsa 75 --page-size 75 --out artifacts/v1_graph_75.json
python -m catalytic_earth.cli graph-summary --graph artifacts/v1_graph_75.json --out artifacts/v1_graph_summary_75.json
python -m catalytic_earth.cli build-v2-benchmark --graph artifacts/v1_graph_75.json --out artifacts/v2_benchmark_75.json
python -m catalytic_earth.cli build-geometry-features --graph artifacts/v1_graph_75.json --max-entries 60 --out artifacts/v3_geometry_features_60.json
python -m catalytic_earth.cli run-geometry-retrieval --geometry artifacts/v3_geometry_features_60.json --out artifacts/v3_geometry_retrieval_60.json
python -m catalytic_earth.cli evaluate-geometry-labels --retrieval artifacts/v3_geometry_retrieval_60.json --abstain-threshold 0.5653 --out artifacts/v3_geometry_label_eval_60.json
python -m catalytic_earth.cli calibrate-abstention --retrieval artifacts/v3_geometry_retrieval_60.json --out artifacts/v3_abstention_calibration_60.json
python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_60.json --out artifacts/v3_hard_negative_controls_60.json
python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_60.json --retrieval artifacts/v3_geometry_retrieval_60.json --out artifacts/v3_label_expansion_candidates_60.json
python -m catalytic_earth.cli analyze-structure-mapping-issues --geometry artifacts/v3_geometry_features_60.json --out artifacts/v3_structure_mapping_issues_60.json
python -m catalytic_earth.cli build-geometry-features --graph artifacts/v1_graph_75.json --max-entries 75 --out artifacts/v3_geometry_features_75.json
python -m catalytic_earth.cli run-geometry-retrieval --geometry artifacts/v3_geometry_features_75.json --out artifacts/v3_geometry_retrieval_75.json
python -m catalytic_earth.cli evaluate-geometry-labels --retrieval artifacts/v3_geometry_retrieval_75.json --abstain-threshold 0.5653 --out artifacts/v3_geometry_label_eval_75.json
python -m catalytic_earth.cli calibrate-abstention --retrieval artifacts/v3_geometry_retrieval_75.json --out artifacts/v3_abstention_calibration_75.json
python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_75.json --out artifacts/v3_hard_negative_controls_75.json
python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_75.json --retrieval artifacts/v3_geometry_retrieval_75.json --out artifacts/v3_label_expansion_candidates_75.json
python -m catalytic_earth.cli analyze-structure-mapping-issues --geometry artifacts/v3_geometry_features_75.json --out artifacts/v3_structure_mapping_issues_75.json
python -m catalytic_earth.cli build-v1-graph --max-mcsa 100 --page-size 100 --out artifacts/v1_graph_100.json
python -m catalytic_earth.cli graph-summary --graph artifacts/v1_graph_100.json --out artifacts/v1_graph_summary_100.json
python -m catalytic_earth.cli build-v2-benchmark --graph artifacts/v1_graph_100.json --out artifacts/v2_benchmark_100.json
python -m catalytic_earth.cli build-geometry-features --graph artifacts/v1_graph_100.json --max-entries 100 --out artifacts/v3_geometry_features_100.json
python -m catalytic_earth.cli run-geometry-retrieval --geometry artifacts/v3_geometry_features_100.json --out artifacts/v3_geometry_retrieval_100.json
python -m catalytic_earth.cli evaluate-geometry-labels --retrieval artifacts/v3_geometry_retrieval_100.json --abstain-threshold 0.5653 --out artifacts/v3_geometry_label_eval_100.json
python -m catalytic_earth.cli calibrate-abstention --retrieval artifacts/v3_geometry_retrieval_100.json --out artifacts/v3_abstention_calibration_100.json
python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_100.json --out artifacts/v3_hard_negative_controls_100.json
python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_100.json --retrieval artifacts/v3_geometry_retrieval_100.json --out artifacts/v3_label_expansion_candidates_100.json
python -m catalytic_earth.cli analyze-structure-mapping-issues --geometry artifacts/v3_geometry_features_100.json --out artifacts/v3_structure_mapping_issues_100.json
python -m catalytic_earth.cli build-v1-graph --max-mcsa 125 --page-size 125 --out artifacts/v1_graph_125.json
python -m catalytic_earth.cli graph-summary --graph artifacts/v1_graph_125.json --out artifacts/v1_graph_summary_125.json
python -m catalytic_earth.cli build-v2-benchmark --graph artifacts/v1_graph_125.json --out artifacts/v2_benchmark_125.json
python -m catalytic_earth.cli build-geometry-features --graph artifacts/v1_graph_125.json --max-entries 125 --out artifacts/v3_geometry_features_125.json
python -m catalytic_earth.cli run-geometry-retrieval --geometry artifacts/v3_geometry_features_125.json --out artifacts/v3_geometry_retrieval_125.json
python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_125.json --retrieval artifacts/v3_geometry_retrieval_125.json --out artifacts/v3_label_expansion_candidates_125.json
python -m catalytic_earth.cli analyze-structure-mapping-issues --geometry artifacts/v3_geometry_features_125.json --out artifacts/v3_structure_mapping_issues_125.json
python -m catalytic_earth.cli perf-suite --iterations 5 --out artifacts/perf_report.json
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
2. Next automation blocks: label the 125-entry staging slice and resolve its
   one unlabeled structure-mapping issue.
3. Next serious milestone: scale from the 100-entry geometry slice to a larger
   audited benchmark where success cannot be explained by tiny-label effects.
4. Long-term impact path: expert-reviewed mechanism labels, learned
   geometry-aware retrieval, source-scale ingestion, and candidate dossiers that
   are credible enough for external labs to prioritize.

So the near-term scope is not "build a dashboard for a year." It is to keep
turning fast scaffold progress into increasingly hard, falsifiable mechanism
benchmarks. Real-world impact still requires expert review and wet-lab
validation outside this repository.
