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
8. Curated mechanism labels for 630 entries: all entries in the 475-entry
   source slice plus accepted, factory-gated labels through the 725-entry
   candidate queue.
9. Auth-vs-label mmCIF residue-number fallback for cleaner structure mapping.
10. Retrieval evaluation, abstention threshold calibration, hard-negative
    selection, in-scope failure analysis, cofactor coverage analysis,
    label-expansion candidate ranking, geometry slice summaries, and a local
    performance suite.
11. Label-factory automation: explicit bronze/silver/gold label schema,
    mechanism ontology, deterministic promotion/demotion audit, active-learning
    review queue, adversarial negative mining, family-propagation guardrails
    including reaction/substrate mismatch blockers,
    expert-review export/import, review-debt triage, repair guardrail audits,
    ontology-gap and sequence-similarity failure controls, learned-retrieval
    manifest pathing, expert-reviewed ATP/phosphoryl-transfer family expansion,
    batch summary with scaling-quality audit attachment, and a scaling gate.

The 20- through 725-entry evaluation slices are clean out-of-scope regression
slices: each has 0 out-of-scope false non-abstentions and 0 hard negatives
under calibrated abstention. The 125-entry slice has 38 in-scope positives, 87
out-of-scope controls, 124/125 evaluable active-site structures, threshold
`0.4115`, and a positive score separation gap of `0.0308`.

The current 725-entry countable stress slice has 613 evaluable active-site
structures among 629 evaluated labeled rows, 163 in-scope labels, 466
evaluated out-of-scope controls, 21 structure-mapping issues, 0 hard negatives,
and 0 near misses. Its calibrated threshold is `0.4115`; it retains 159/163
in-scope positives, abstains on all
evaluable out-of-scope controls, and leaves the same 4 evidence-limited
in-scope abstentions (`m_csa:132`, `m_csa:353`, `m_csa:372`, and `m_csa:430`).
The current actionable in-scope failure count is 0 after separating
selected-structure cofactor gaps from scorer failures. Cofactor policy sweeps
recommend audit-only handling rather than a score penalty because no tested
penalty reduces retained evidence-limited positives without losing retained
positives. Cofactor coverage artifacts explicitly identify retained
evidence-limited positives: `m_csa:41`, `m_csa:108`, `m_csa:160`,
`m_csa:446`, and `m_csa:486`.

The 500-, 525-, 550-, 575-, 600-, 625-, 650-, 675-, 700-, and 725-entry candidate
queues have been processed through the label factory. `m_csa:494` is
intentionally preserved as a non-countable `needs_expert_review` cobalamin
evidence gap because B12 evidence is structure-wide only. The 675, 700, and
725 batches accepted 12 additional clean countable labels while preserving 0
hard negatives, 0 near misses, 0 out-of-scope false non-abstentions, and 0
actionable in-scope failures. See
`work/label_queue_500_notes.md`, `work/label_queue_525_notes.md`,
`work/label_queue_550_notes.md`, `work/label_factory_notes.md`, and
`work/label_preview_725_notes.md`.

Label scaling is now gated by the label factory rather than raw queue size. The
current 725 factory audit proposes 83 bronze-to-silver promotions, flags 112
abstention/review rows, mines 100 adversarial negative controls from 466
out-of-scope candidates, exports 174 expert-review items from the post-725
review queue, exports all 95 active `expert_label_decision_needed` rows as
review-only no-decision items, generates a non-countable repair-candidate plan
and priority repair guardrail audit for those 95 rows, audits/exports the 25
priority local-evidence gap lanes as review-only items, emits a local-evidence
repair plan, exports 8 explicit alternate residue-position sourcing requests,
verifies review-only import safety, maps expert-reviewed
ATP/phosphoryl-transfer mismatch lanes to nine concrete fingerprint families,
and passes the 20-check 725-slice gate. The gate also
fails if unlabeled candidate rows are truncated by the queue limit, if
family-guardrail reaction/substrate mismatch lanes lack a dedicated review
export, if expert-label decision rows are not explicitly routed as non-countable
external-review items, or if those rows lack a complete non-countable repair
candidate summary, repair guardrail audit, local-evidence gap audit, and
local-evidence review export; it also requires alternate residue-position
sourcing requests and review-only import-safety audit to remain non-countable,
and requires the
ATP/phosphoryl-transfer family expansion artifact to be guardrail-clean when
attached.
`artifacts/v3_label_batch_acceptance_check_725.json` records that the latest
accepted batch added 6 labels for counting while 100 review-state decisions
remain pending. `artifacts/v3_label_factory_batch_summary.json` aggregates the
accepted batch history and confirms 10/10 accepted batches remain
guardrail-clean. `artifacts/v3_review_debt_summary_725_preview.json`
prioritizes 100 current evidence-gap rows for the accepted 725 state. The 675,
700, and 725 scaling-quality audits keep pending evidence gaps outside the
benchmark, classify new debt rows, and attach graph-derived sequence-cluster
proxy artifacts; all report 0 accepted labels with review debt and 0
near-duplicate hits among audited rows. See
`work/label_preview_675_notes.md`, `work/label_preview_700_notes.md`,
`work/label_preview_725_notes.md`, and
`work/expert_label_decision_review_700_notes.md` for the clean label profiles,
the top evidence gaps, the expert-decision review-only profile, and the
prioritized non-countable repair buckets.
`artifacts/v3_expert_label_decision_local_evidence_repair_plan_700.json`
prioritizes the current 21 local-evidence repair lanes as 4 reaction/substrate
expert-review lanes, 3 explicit alternate-residue-position sourcing lanes,
3 active-site mapping or structure-selection lanes, and 11 family-boundary
review lanes. `artifacts/v3_expert_label_decision_local_evidence_repair_resolution_700.json`
closes the 4 reaction/substrate lanes as reviewed out-of-scope repair debt
without adding countable labels; `artifacts/v3_explicit_alternate_residue_position_requests_700.json`
turns the 3 alternate-residue lanes into sourceable evidence requests across
34 alternate PDB structures; and
`artifacts/v3_review_only_import_safety_audit_700.json` confirms the
review-only decision artifacts add 0 countable labels.
The accepted-700 non-countable repair artifacts remain as historical
discovery-facing controls:
`artifacts/v3_mechanism_ontology_gap_audit_700.json` records 115 ontology
scope-pressure rows without creating new families,
`artifacts/v3_learned_retrieval_manifest_700.json` defines a future learned
representation interface with 562 eligible rows and heuristic retrieval as the
control, and `artifacts/v3_sequence_similarity_failure_sets_700.json` keeps the
2 exact-reference duplicate clusters as sequence-similarity failure controls.
The 700 review-debt repair pass now adds structure-aware remediation artifacts:
`artifacts/v3_review_debt_remediation_700.json`,
`artifacts/v3_review_debt_remediation_700_all.json`, and
`artifacts/v3_review_debt_alternate_structure_scan_700.json`. The focused
accepted-700 scan checks 152 candidate PDB structures for the 13 new-debt
structure-scan rows, conservatively remaps selected active-site residue
positions onto 63 alternate-PDB structures, finds 3 structure-wide
cofactor-family hits, and keeps them non-countable because 0 have local
active-site support. The all-debt bounded scan
`artifacts/v3_review_debt_alternate_structure_scan_700_all_bounded.json`
covers all 46 scan-candidate review-debt rows and all 739 candidate PDB
structures, remaps 362 alternate-PDB structures, and finds review-only local
expected-family hits for `m_csa:577`, `m_csa:592`, and `m_csa:641`.
`artifacts/v3_review_debt_remap_local_lead_audit_700.json` routes
`m_csa:577` and `m_csa:641` to expert family-boundary review and `m_csa:592`
to expert reaction/substrate review, while keeping all three under a strict
non-countable remap guardrail. `artifacts/v3_reaction_substrate_mismatch_audit_700.json`
flags 18 active-queue hydrolase-top1 rows with kinase or ATP phosphoryl-transfer
text for expert reaction/substrate review. The 700 family-propagation guardrail
retains all 24 hydrolase-top1 reaction/substrate mismatch blockers, split
between 17 labeled propagation blocks and 7 unlabeled pending-review blocks.
The accepted-725 repair preview adds a focused scan for 12 new review-debt
rows, covering 140 structures with 0 fetch failures. It finds structure-wide
expected-family hits for `m_csa:712`, `m_csa:718`, and `m_csa:724`; only
`m_csa:712` has local support from a conservative remap, so it is routed to
strict expert family-boundary review and remains non-countable. The 725
ontology-gap audit records 121 review-only scope-pressure rows, the learned
retrieval manifest exposes 568 eligible rows for future representation work,
and the sequence-similarity failure-set audit keeps 2 duplicate clusters as
non-countable propagation controls.
`artifacts/v3_reaction_substrate_mismatch_review_export_700.json` now carries
all 24 lanes together.
`artifacts/v3_atp_phosphoryl_transfer_family_expansion_700.json` implements the
expert-reviewed ontology expansion for ePK, ASKHA, ATP-grasp, GHKL, dNK, NDK,
PfkA, PfkB, and GHMP. It maps 20 expert-supported mismatch lanes to those
families, records 4 non-target hints for future work, and keeps
`countable_label_candidate_count=0`. The reviewed decision batch remains
review-only while routing the 7 unlabeled rows to reviewed out-of-scope repair
decisions and rejecting 17 controls. Countable import refuses
review-only artifacts even when they carry reviewed repair decisions, so these
lanes cannot enter the benchmark. With the 725 batch accepted, the next bounded
work item is repairing or explicitly deferring the accepted-725 review-debt
surface before blind 750 scaling.
See
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
python -m catalytic_earth.cli build-sequence-cluster-proxy --graph artifacts/v1_graph_500.json --out artifacts/v3_sequence_cluster_proxy_500.json
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
2. Current automation blocks: keep using the label factory for every new
   tranche. The 725 slice is accepted only for its clean countable labels; 100
   review-state rows remain outside the benchmark. Each batch must pass
   promotion/demotion, adversarial-negative, active-learning, expert-review
   export/import, family-propagation, ATP/phosphoryl-transfer family-boundary,
   validation, and test gates before labels count toward the benchmark.
3. Next serious milestone: repair and audit the new accepted-725 review-debt
   surface before opening a blind 750 tranche; then resume bounded
   factory-gated scaling toward 10k once the 725 warnings remain
   guardrail-clean. Stop count growth if the next
   gate exposes new review debt, ontology/family propagation drift, hard
   negatives, out-of-scope false non-abstentions, or actionable in-scope
   failures.
4. Long-term impact path: expert-reviewed mechanism labels, learned
   geometry-aware retrieval, source-scale ingestion, and candidate dossiers that
   are credible enough for external labs to prioritize.

So the near-term scope is not "build a dashboard for a year." It is to keep
turning fast scaffold progress into increasingly hard, falsifiable mechanism
benchmarks. Real-world impact still requires expert review and wet-lab
validation outside this repository.
