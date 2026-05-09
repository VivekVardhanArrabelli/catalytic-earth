# Handoff

## Mission

Continue Catalytic Earth: an open mechanism-level atlas of enzyme function.

The central artifact is not a dashboard. It is a mechanism-first knowledge graph,
benchmark suite, and enzyme discovery pipeline that maps protein evidence to
catalytic hypotheses.

Current post-V2 direction: improve scientific quality by moving from text/motif
baselines to geometry-aware active-site retrieval. The first geometry artifact
is `artifacts/v3_geometry_features.json`.

Curated seed labels now live in
`data/registries/curated_mechanism_labels.json`. The latest evaluation artifact
is `artifacts/v3_geometry_label_eval.json`; the current 20-entry slice keeps
top1/top3 in-scope accuracy at 1.0, and abstention remains calibration-sensitive
because labels are still small and provisional.

## Repository

Local path:

```text
/Users/vivekvardhanarrabelli/Documents/Codex/2026-05-08/check-out-careflly-u-can-use-2/catalytic-earth
```

GitHub:

```text
https://github.com/VivekVardhanArrabelli/catalytic-earth
```

## Before Work

1. Read `README.md`.
2. Read `work/scope.md`.
3. Read `work/status.md` if it exists.
4. Run:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## During Work

- Treat each automation run as one 55-minute focused block measured from the
  real wall-clock start timestamp.
- If the assigned task finishes early, do not hand off immediately. Write a
  short plan for the remaining wall-clock time in the same 55-minute block and
  execute the highest-value bounded item toward project completion.
- At 50 minutes elapsed, stop starting new implementation work and begin
  wrap-up: finish tests/artifacts/docs, update this handoff, log measured time,
  regenerate status, commit, and push.
- Prefer durable code and data schemas over prose.
- Keep outputs reproducible.
- Add tests for new normalization logic.
- Do not make wet-lab or deployment claims.
- End every automation block by updating `Next Agent Start Here` below with:
  what changed, where to continue, known blockers, the next concrete task, and
  first commands to run.
- Log time and progress with:

```bash
PYTHONPATH=src python -m catalytic_earth.cli log-work --help
PYTHONPATH=src python -m catalytic_earth.cli progress-report --out work/status.md
```

Use measured time going forward:

```bash
PYTHONPATH=src python -m catalytic_earth.cli log-work \
  --stage post-v2 \
  --task "..." \
  --minutes 0 \
  --time-mode measured \
  --started-at "2026-05-09T00:00:00+00:00" \
  --ended-at "2026-05-09T00:55:00+00:00"
```

## Push Rule

Automation runs must commit and push every hour, even if progress is
incremental. Prefer meaningful progress such as:

- new source adapter
- graph schema or graph builder improvement
- benchmark machinery
- discovery pipeline component
- candidate dossier generation
- meaningful documentation that changes execution
- important bug fix with tests

Before handoff, git must be fully synced so the next agent starts from canonical
state:

1. `git fetch origin`
2. `git pull --ff-only origin main` (or verify already up to date)
3. `git push origin main`
4. Verify `git rev-parse HEAD` equals `git rev-parse origin/main`
5. Verify no merge is in progress (`test ! -f .git/MERGE_HEAD`)

## V2 Report Rule

Only report "v2 done" when every criterion in `work/scope.md` under `V2 Target`
is actually satisfied and reproducible from commands in the repository.

## UI Context Note

Computer Use was attempted against the Codex app for context inspection, but the
tool reported that it is not allowed to operate on `com.openai.codex` for safety
reasons. Treat repository state and this handoff file as the reliable recovery
surface.

## Next Agent Start Here

What changed in this run:

- Automation and scope rules were tightened: if the assigned handoff task
  finishes early, continue with a written remaining-time plan and implement
  bounded high-value work until the 50-minute wrap-up boundary; before handoff,
  verify `origin/main` sync, clean git status, and no pending merge.
- Added substrate-pocket descriptors in `src/catalytic_earth/structure.py`:
  - finds nearby non-catalytic protein residues in an 8A shell around resolved
    catalytic residues
  - records per-entry `pocket_context` with nearby residue sites, residue-code
    counts, and descriptor fractions (hydrophobic, polar, positive, negative,
    aromatic, sulfur) plus charge balance and mean active-site distance
  - adds geometry metadata counter `entries_with_pocket_context`
- Updated retrieval scoring in `src/catalytic_earth/geometry_retrieval.py`:
  - new `substrate_pocket_score` term added to final score
  - weighted scoring now combines residue/role overlap, cofactor context, pocket
    descriptors, and compactness
  - retrieval metadata string updated to reflect pocket-aware scoring
- Extended tests:
  - `tests/test_structure.py` now validates pocket-context extraction and
    metadata counts
  - `tests/test_geometry_retrieval.py` now validates pocket-scoring preference
    behavior and pocket-context ingestion in retrieval
- Regenerated artifacts:
  - `artifacts/v3_geometry_features.json`
  - `artifacts/v3_geometry_retrieval.json`
  - `artifacts/v3_geometry_label_eval.json`
  - `artifacts/v3_abstention_calibration.json`
  - `artifacts/perf_report.json`
- Updated docs: `README.md`, `docs/geometry_features.md`,
  `docs/v2_strengthening_report.md`, `work/scope.md`.

Start commands:

```bash
git fetch origin
git pull --ff-only origin main
git status -sb
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli build-geometry-features --graph artifacts/v1_graph.json --max-entries 20 --out artifacts/v3_geometry_features.json
PYTHONPATH=src python -m catalytic_earth.cli run-geometry-retrieval --geometry artifacts/v3_geometry_features.json --out artifacts/v3_geometry_retrieval.json
```

Current state:

- V2 scaffold is complete.
- Geometry-aware active-site retrieval exists.
- Curated seed labels exist for the 20-entry geometry slice.
- Ligand/cofactor context is now parsed from proximal mmCIF non-polymer atoms
  for the geometry slice (11/20 entries with proximal ligands; 5/20 with mapped
  cofactor families).
- Substrate-pocket context is now parsed from nearby protein residues for the
  geometry slice (15/20 entries with non-empty pocket context).
- Current label evaluation at threshold 0.7:
  - top1 in-scope accuracy: 1.0
  - top3 in-scope accuracy: 1.0
  - out-of-scope abstention: 0.75
- Current selected abstention threshold is 0.75 with out-of-scope abstention
  1.0 on this small provisional set.
- Local performance report exists at `artifacts/perf_report.json`.

Next concrete task:

Run targeted failure analysis on out-of-scope handling and pocket/cofactor
signals. Concrete path:
1) inspect per-entry top predictions vs labels for all out-of-scope entries,
2) categorize false non-abstentions by evidence pattern (residue overlap,
cofactor-only hits, pocket-only hits), 3) implement one bounded calibration or
scoring fix and re-evaluate threshold selection.

Known blockers:

- Current curated labels are provisional and small.
- Geometry retrieval still uses simple heuristics, not learned geometry.
- Ligand/cofactor evidence is currently nearest-ligand heuristic only; it does
  not model occupancy, alternate conformers, or biological assembly context.
- Substrate-pocket evidence is currently a residue-shell heuristic, not a
  physics-based or learned pocket model.
