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
8. Curated mechanism labels for 499 entries: all entries in the 475-entry
   source slice plus 24 accepted, factory-gated labels from the 500-entry
   candidate queue.
9. Auth-vs-label mmCIF residue-number fallback for cleaner structure mapping.
10. Retrieval evaluation, abstention threshold calibration, hard-negative
    selection, in-scope failure analysis, cofactor coverage analysis,
    label-expansion candidate ranking, geometry slice summaries, and a local
    performance suite.
11. Label-factory automation: explicit bronze/silver/gold label schema,
    mechanism ontology, deterministic promotion/demotion audit, active-learning
    review queue, adversarial negative mining, family-propagation guardrails,
    expert-review export/import, and a scaling gate.

The 20- through 500-entry evaluation slices are clean out-of-scope regression
slices: each has 0 out-of-scope false non-abstentions and 0 hard negatives
under calibrated abstention. The 125-entry slice has 38 in-scope positives, 87
out-of-scope controls, 124/125 evaluable active-site structures, threshold
`0.4115`, and a positive score separation gap of `0.0308`.

The current 500-entry countable stress slice has 499 geometry entries, 490
evaluable active-site structures, 131 local active-site in-scope positives, 367
evaluated out-of-scope controls, 1 remaining label-expansion candidate, 8
structure-mapping issues, 0 hard negatives, and 0 near misses. Its calibrated
threshold is `0.4115`; it retains 127/131 in-scope positives, abstains on all
evaluable out-of-scope controls, and leaves the same 4 evidence-limited
in-scope abstentions (`m_csa:132`, `m_csa:353`, `m_csa:372`, and `m_csa:430`).
The current actionable in-scope failure count is 0 after separating
selected-structure cofactor gaps from scorer failures. Cofactor policy sweeps
recommend audit-only handling rather than a score penalty because no tested
penalty reduces retained evidence-limited positives without losing retained
positives. Cofactor coverage artifacts explicitly identify retained
evidence-limited positives: `m_csa:41`, `m_csa:108`, `m_csa:160`,
`m_csa:446`, and `m_csa:486`.

The 500-entry candidate queue has been processed through the label factory.
`m_csa:482`, `m_csa:486`, `m_csa:495`, and `m_csa:497` were accepted as
countable positive seed labels; 20 out-of-scope controls were accepted;
`m_csa:494` remains the single uncounted review candidate because B12 evidence
is structure-wide only. The queue recognizes the `5PA` ligand as PLP context
and applies farnesyl/prenyl transfer counterevidence for `m_csa:484`; see
`work/label_queue_500_notes.md`.

Label scaling is now gated by the label factory rather than raw queue size. The
current factory audit proposes 63 bronze-to-silver promotions, flags 101
abstention/review rows, mines 100 adversarial negative controls from 367
out-of-scope candidates, exports 26 expert-review items including the remaining
unlabeled 500-slice candidate, and passes the 500-slice gate check.
`artifacts/v3_label_batch_acceptance_check_500.json` records that 1 additional
label was accepted for counting while 6 review-state decisions remain pending. See
`docs/label_factory.md`.

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

python -m catalytic_earth.cli build-v1-graph --max-mcsa 500 --page-size 100 --out artifacts/v1_graph_500.json
python -m catalytic_earth.cli graph-summary --graph artifacts/v1_graph_500.json --out artifacts/v1_graph_summary_500.json
python -m catalytic_earth.cli build-v2-benchmark --graph artifacts/v1_graph_500.json --out artifacts/v2_benchmark_500.json
python -m catalytic_earth.cli build-geometry-features --graph artifacts/v1_graph_500.json --max-entries 500 --out artifacts/v3_geometry_features_500.json
python -m catalytic_earth.cli run-geometry-retrieval --geometry artifacts/v3_geometry_features_500.json --out artifacts/v3_geometry_retrieval_500.json
python -m catalytic_earth.cli calibrate-abstention --retrieval artifacts/v3_geometry_retrieval_500.json --out artifacts/v3_abstention_calibration_500.json
python -m catalytic_earth.cli evaluate-geometry-labels --retrieval artifacts/v3_geometry_retrieval_500.json --abstain-threshold 0.4115 --out artifacts/v3_geometry_label_eval_500.json
python -m catalytic_earth.cli analyze-geometry-failures --retrieval artifacts/v3_geometry_retrieval_500.json --abstain-threshold 0.4115 --out artifacts/v3_geometry_failure_analysis_500.json
python -m catalytic_earth.cli analyze-in-scope-failures --retrieval artifacts/v3_geometry_retrieval_500.json --abstain-threshold 0.4115 --out artifacts/v3_in_scope_failure_analysis_500.json
python -m catalytic_earth.cli analyze-cofactor-coverage --retrieval artifacts/v3_geometry_retrieval_500.json --abstain-threshold 0.4115 --out artifacts/v3_cofactor_coverage_500.json
python -m catalytic_earth.cli analyze-cofactor-policy --retrieval artifacts/v3_geometry_retrieval_500.json --abstain-threshold 0.4115 --out artifacts/v3_cofactor_policy_500.json
python -m catalytic_earth.cli analyze-seed-family-performance --retrieval artifacts/v3_geometry_retrieval_500.json --abstain-threshold 0.4115 --out artifacts/v3_seed_family_performance_500.json
python -m catalytic_earth.cli analyze-geometry-score-margins --retrieval artifacts/v3_geometry_retrieval_500.json --out artifacts/v3_geometry_score_margins_500.json
python -m catalytic_earth.cli build-hard-negative-controls --retrieval artifacts/v3_geometry_retrieval_500.json --out artifacts/v3_hard_negative_controls_500.json
python -m catalytic_earth.cli build-label-expansion-candidates --geometry artifacts/v3_geometry_features_500.json --retrieval artifacts/v3_geometry_retrieval_500.json --out artifacts/v3_label_expansion_candidates_500.json
python -m catalytic_earth.cli build-adversarial-negatives --retrieval artifacts/v3_geometry_retrieval_500.json --abstain-threshold 0.4115 --out artifacts/v3_adversarial_negative_controls_500.json
python -m catalytic_earth.cli build-label-factory-audit --retrieval artifacts/v3_geometry_retrieval_500.json --hard-negatives artifacts/v3_hard_negative_controls_500.json --adversarial-negatives artifacts/v3_adversarial_negative_controls_500.json --abstain-threshold 0.4115 --out artifacts/v3_label_factory_audit_500.json
python -m catalytic_earth.cli apply-label-factory-actions --label-factory-audit artifacts/v3_label_factory_audit_500.json --out artifacts/v3_label_factory_applied_labels_500.json
python -m catalytic_earth.cli build-active-learning-queue --geometry artifacts/v3_geometry_features_500.json --retrieval artifacts/v3_geometry_retrieval_500.json --label-factory-audit artifacts/v3_label_factory_audit_500.json --abstain-threshold 0.4115 --max-rows 150 --out artifacts/v3_active_learning_review_queue_500.json
python -m catalytic_earth.cli export-label-review --queue artifacts/v3_active_learning_review_queue_500.json --out artifacts/v3_expert_review_export_500.json
python -m catalytic_earth.cli import-label-review --review artifacts/v3_expert_review_export_500.json --out artifacts/v3_expert_review_import_preview_500.json
python -m catalytic_earth.cli build-family-propagation-guardrails --geometry artifacts/v3_geometry_features_500.json --retrieval artifacts/v3_geometry_retrieval_500.json --out artifacts/v3_family_propagation_guardrails_500.json
python -m catalytic_earth.cli check-label-factory-gates --label-factory-audit artifacts/v3_label_factory_audit_500.json --applied-label-factory artifacts/v3_label_factory_applied_labels_500.json --active-learning-queue artifacts/v3_active_learning_review_queue_500.json --adversarial-negatives artifacts/v3_adversarial_negative_controls_500.json --expert-review-export artifacts/v3_expert_review_export_500.json --family-propagation-guardrails artifacts/v3_family_propagation_guardrails_500.json --out artifacts/v3_label_factory_gate_check_500.json
python -m catalytic_earth.cli analyze-structure-mapping-issues --geometry artifacts/v3_geometry_features_500.json --out artifacts/v3_structure_mapping_issues_500.json
python -m catalytic_earth.cli summarize-geometry-slices --artifact-dir artifacts --out artifacts/v3_geometry_slice_summary.json
python -m catalytic_earth.cli perf-suite --graph artifacts/v1_graph_500.json --geometry artifacts/v3_geometry_features_500.json --retrieval artifacts/v3_geometry_retrieval_500.json --iterations 5 --out artifacts/perf_report.json

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

Automation runs use the tested `automation-lock` CLI wrapper to acquire the
local run lock and to release it only after clean-tree, no-merge, and
`HEAD == origin/main` checks pass.

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
2. Current automation blocks: use the label factory to finish the remaining
   500-slice review candidate (`m_csa:494`) before opening a larger tranche.
   Each batch must pass promotion/demotion,
   adversarial-negative, active-learning, expert-review export/import,
   family-propagation, validation, and test gates before labels count toward
   the benchmark.
3. Next serious milestone: expand beyond 499 countable labels or resolve the
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
