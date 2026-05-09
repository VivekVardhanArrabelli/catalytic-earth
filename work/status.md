# Catalytic Earth Status

Generated from `work/progress_log.jsonl`.

## Time

- Entries: 7
- Total logged time: 315 minutes (5.25 hours)

## Time By Stage

- ops: 25 minutes (0.42 hours)
- post-v2: 110 minutes (1.83 hours)
- v0: 55 minutes (0.92 hours)
- v1: 55 minutes (0.92 hours)
- v2: 70 minutes (1.17 hours)

## Progress Counters

- Artifact references logged: 33
- Evidence references logged: 37

## Recent Entries

### 2026-05-09T13:40:20.355854+00:00 - v0

- Task: Initial scaffold, live source samples, seed graph, public GitHub publish
- Minutes: 55
- Artifacts: README.md, docs/research_program.md, data/registries/source_registry.json, data/registries/mechanism_fingerprints.json, artifacts/seed_graph.json
- Evidence: 12 source records, 6 mechanism fingerprints, 10 Rhea records, 3 M-CSA records, 26 graph nodes, 23 graph edges, 10 tests passed, public GitHub repo
- Commit: `9380641`
- Notes: Minutes are active-work estimate reconstructed from the session; future entries should be logged at session end.

### 2026-05-09T13:40:25.768544+00:00 - ops

- Task: Add durable work folder, time ledger, scope calibration, and progress report tooling
- Minutes: 25
- Artifacts: work/README.md, work/scope.md, work/handoff.md, src/catalytic_earth/progress.py, tests/test_progress.py
- Evidence: 12 tests passed, progress-report command, log-work command

### 2026-05-09T13:54:30.954964+00:00 - v1

- Task: Build persistent catalytic graph with M-CSA pages, Rhea EC mapping, UniProt links, and structure cross-references
- Minutes: 55
- Artifacts: docs/graph_schema.md, src/catalytic_earth/graph.py, artifacts/v1_graph.json, artifacts/v1_graph_summary.json
- Evidence: 50 M-CSA entries, 48 EC nodes, 53 Rhea reactions, 51 proteins, 918 structures, 1513 graph nodes, 1475 graph edges, 15 tests passed

### 2026-05-09T13:54:31.022704+00:00 - v2

- Task: Build first V2 benchmark, baseline retrieval, inconsistency detector, dark hydrolase mining campaign, dossiers, and report
- Minutes: 70
- Artifacts: src/catalytic_earth/v2.py, artifacts/v2_benchmark.json, artifacts/v2_baseline.json, artifacts/v2_inconsistencies.json, artifacts/v2_dark_hydrolase_candidates.json, artifacts/v2_dossiers, docs/v2_report.md
- Evidence: 50 benchmark records, 6 seed fingerprints, 10 inconsistency issues, 100 dark hydrolase candidates, 10 candidate dossiers, 18 tests passed

### 2026-05-09T14:01:49.012481+00:00 - post-v2

- Task: Add geometry-aware active-site feature extraction from PDB mmCIF files
- Minutes: 45
- Artifacts: src/catalytic_earth/structure.py, docs/geometry_features.md, artifacts/v3_geometry_features.json, tests/test_structure.py
- Evidence: 20 graph entries processed, 13 entries with pairwise active-site geometry, 21 tests passed

### 2026-05-09T14:03:45.516905+00:00 - post-v2

- Task: Add geometry-aware seed fingerprint retrieval baseline
- Minutes: 30
- Artifacts: src/catalytic_earth/geometry_retrieval.py, artifacts/v3_geometry_retrieval.json, tests/test_geometry_retrieval.py
- Evidence: 20 geometry entries ranked, 6 seed fingerprints scored, 25 tests passed

### 2026-05-09T14:10:40.717863+00:00 - post-v2

- Task: Add curated seed mechanism labels and geometry retrieval evaluation
- Minutes: 35
- Artifacts: data/registries/curated_mechanism_labels.json, src/catalytic_earth/labels.py, artifacts/v3_label_summary.json, artifacts/v3_geometry_label_eval.json, tests/test_labels.py
- Evidence: 20 curated labels, 4 in-scope seed-fingerprint labels, 16 out-of-scope labels, 28 tests passed, top3 in-scope accuracy 1.0, top1 in-scope accuracy 0.0

## Expectation Updates

- 2026-05-09T13:40:20.355854+00:00: v0 completed in one active session, so the previous one-year v0-v2 timeline is too conservative and must be recalibrated from logged progress
- 2026-05-09T13:40:25.768544+00:00: Use observed artifact-per-hour rate to revise v1 and v2 estimates after each material chunk.
- 2026-05-09T13:54:30.954964+00:00: V1 completed much faster than the earlier days-to-weeks estimate because paginated M-CSA and UniProt TSV APIs were straightforward.
- 2026-05-09T13:54:31.022704+00:00: The completed V2 is a scaffold-level research artifact, not the final high-impact enzyme atlas; time estimates must distinguish scaffold completion from scientific validation.
- 2026-05-09T14:01:49.012481+00:00: Geometry extraction was implementable quickly for PDB-linked M-CSA entries; the harder next step is label quality and retrieval evaluation.
- 2026-05-09T14:03:45.516905+00:00: Next quality bottleneck is curated mechanism labels and evaluation, not baseline implementation.
- 2026-05-09T14:10:40.717863+00:00: The next bottleneck is improving ranking and abstention, not adding labels machinery.

## Scope Adjustments

- 2026-05-09T13:40:25.768544+00:00: Project management is now repository state, not chat state; future scope changes must be recorded in the ledger.
- 2026-05-09T13:54:30.954964+00:00: V1 criteria are satisfied by a bounded 50-entry graph slice; broader scale is now an expansion problem, not a schema blocker.
- 2026-05-09T13:54:31.022704+00:00: V2 scaffold criteria are satisfied; next work should increase scientific quality rather than add more dashboard-like surface area.
- 2026-05-09T14:01:49.012481+00:00: Post-V2 quality work now targets geometry-aware retrieval rather than more text-only scaffolding.
- 2026-05-09T14:03:45.516905+00:00: Geometry now affects retrieval scores through residue signature matching and catalytic-cluster compactness.
- 2026-05-09T14:10:40.717863+00:00: Curated labels are now explicit for the 20-entry geometry slice; retrieval quality is measurable and currently weak at top1.
