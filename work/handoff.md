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

- Added mmCIF ligand/cofactor context extraction in
  `src/catalytic_earth/structure.py`:
  - parses nearby `HETATM` ligands around resolved catalytic residues
  - records `ligand_context` per geometry entry
  - infers cofactor families (heme, flavin, PLP, SAM, Fe-S, metal ions)
  - adds geometry metadata counters for proximal ligands and inferred cofactors
- Updated retrieval scoring in `src/catalytic_earth/geometry_retrieval.py` to
  use ligand-supported cofactor evidence and penalize unsupported cofactor-heavy
  fingerprints.
- Added tests in `tests/test_structure.py` and
  `tests/test_geometry_retrieval.py` for ligand parsing and cofactor-aware
  ranking behavior.
- Regenerated artifacts:
  - `artifacts/v3_geometry_features.json`
  - `artifacts/v3_geometry_retrieval.json`
  - `artifacts/v3_geometry_label_eval.json`
  - `artifacts/v3_abstention_calibration.json`
  - `artifacts/perf_report.json`
- Updated docs: `docs/geometry_features.md`, `docs/v2_strengthening_report.md`.

Start commands:

```bash
git status -sb
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli run-geometry-retrieval --geometry artifacts/v3_geometry_features.json --out artifacts/v3_geometry_retrieval.json
```

Current state:

- V2 scaffold is complete.
- Geometry-aware active-site retrieval exists.
- Curated seed labels exist for the 20-entry geometry slice.
- Ligand/cofactor context is now parsed from proximal mmCIF non-polymer atoms
  for the geometry slice (11/20 entries with proximal ligands; 5/20 with mapped
  cofactor families).
- Current label evaluation at threshold 0.7:
  - top1 in-scope accuracy: 1.0
  - top3 in-scope accuracy: 1.0
  - out-of-scope abstention: 0.75
- Current selected abstention threshold is 0.8 with out-of-scope abstention 1.0
  on this small provisional set.
- Local performance report exists at `artifacts/perf_report.json`.

Next concrete task:

Add substrate-pocket descriptors tied to the same resolved active-site geometry.
Concrete path:
1) collect nearby protein residues within a distance shell around catalytic
   residues, 2) summarize pocket polarity/charge/size proxies, 3) feed those
   descriptors into retrieval scoring and abstention calibration.

Known blockers:

- Current curated labels are provisional and small.
- Geometry retrieval still uses simple heuristics, not learned geometry.
- Ligand/cofactor evidence is currently nearest-ligand heuristic only; it does
  not model occupancy, alternate conformers, or biological assembly context.
- Substrate-pocket descriptors are not implemented yet.
