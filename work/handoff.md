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
is `artifacts/v3_geometry_label_eval.json`; it shows top3 retrieval can recover
the small in-scope label set, while top1 ranking and out-of-scope abstention are
still weak.

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

- Treat each automation run as one 55-minute focused block.
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

Latest pushed state before this handoff rule: `1be523e`; later work added
geometry features, geometry retrieval, and curated labels. Run `git log -1` for
the exact latest commit.

Start commands:

```bash
git status -sb
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
```

Current state:

- V2 scaffold is complete.
- Geometry-aware active-site retrieval exists.
- Curated seed labels exist for the 20-entry geometry slice.
- Strengthened geometry scoring now recovers the small in-scope label set at
  top1, but there are only 4 in-scope positives, so this is not robust evidence.
- Abstention calibration exists at `artifacts/v3_abstention_calibration.json`.
- Local performance report exists at `artifacts/perf_report.json`.

Next concrete task:

Improve out-of-scope handling and mechanism coverage. A good next step is to add
ligand/cofactor context from PDB mmCIF non-polymer records, then use that to
penalize heme/flavin/PLP/radical-SAM fingerprints when the required cofactor is
not structurally or textually supported.

Known blockers:

- Current curated labels are provisional and small.
- Geometry retrieval still uses simple heuristics, not learned geometry.
- Ligand/cofactor context and substrate-pocket descriptors are not implemented.
