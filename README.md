# Catalytic Earth

Catalytic Earth is a mechanism-first enzyme function atlas scaffold. The goal
is to make enzyme function searchable by catalytic mechanism, not only by EC
number, name, keyword, or sequence similarity.

## North Star

Build a computable map from protein evidence to chemical function:

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

This repository is a research scaffold and benchmark workspace. It is not a
wet-lab protocol, not a claim that computational candidates are validated
enzymes, and not a production biological design system.

## Quick Status

- Current benchmark surface: `current702`, with 702 curated labels, 562
  in-distribution rows, and 140 heldout rows.
- Current primary v1 targets: serine hydrolase, metal hydrolase, PLP enzyme,
  broad flavin dehydrogenase/reductase, and heme peroxidase/oxidase.
- Current secondary OOD probes: radical SAM, cobalamin radical rearrangement,
  and flavin monooxygenase.
- Current gate: geometry-first router. The Wave 1.2 audit re-exported geometry
  on the standardized heldout rows, joined 140/140 rows, and reported 45/45
  canonical primary accuracy with 0/92 pure-OOS false positives under the
  existing geometry abstention threshold.
- Learned representation results are diagnostic. ESM-C logistic versus ESM-C
  cosine shows decoder choice is confounded; ProtT5 and SaProt matched logistic
  reruns are blocked until raw local sidecars or weights exist.
- FMO remains secondary-only and review-only for now. No FMO primary promotion,
  registry edit, threshold change, production scoring change, or import is
  currently authorized.

## Start Here

Read these files in order before interpreting older reports or starting an
agent run:

| File | Use it for |
| --- | --- |
| `docs/project_state.md` | Current state, trusted results, blockers, and next gates |
| `docs/decision_log.md` | Dated decisions that override older artifact wording |
| `docs/artifact_index.md` | Which artifact answers which question, and what is deprecated |
| `docs/agent_runbook.md` | Safe edit boundaries, validation, and output locations |

## Key Commands

Install locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Validate the repo:

```bash
PYTHONPATH=src python -m catalytic_earth.cli validate
git diff --check
```

Run the test suite after code changes:

```bash
python -m unittest discover -s tests
```

Check JSON artifacts:

```bash
python -m json.tool artifacts/path.json >/dev/null
```

Check disk before heavy artifact work:

```bash
df -h .
```

## Artifact Map

The durable artifact map is in `docs/artifact_index.md`. Current high-signal
entry points are:

- `artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json`
- `work/wave1_2_decoder_join_confound_audit_702_20260528.md`
- `artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json`
- `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json`
- `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`
- `docs/label_factory.md`
- `docs/artifact_storage.md`

Older Wave 1 representation summaries are useful historical context, not the
current gate. Read them through the Wave 1.2 audit because geometry join policy
and decoder choice were confounded.

## Benchmark Caveats

- The 2026-05-25 current702 sequence manifest predates the later OOS revisions
  for `m_csa:497` and `m_csa:750`. Use the readthrough/addendum artifacts
  before interpreting old primary flavin metrics.
- Do not tune abstention thresholds on heldout/test rows.
- Do not use EC/name/source prose/mechanism text/expert notes/review reasons as
  predictive features.
- Review artifacts are not imports. A row counts only after explicit review,
  import preview, label-factory gates, batch acceptance, and registry summary
  refresh.
- Keep disk above 10 GiB free and avoid large downloads unless a task
  explicitly authorizes them.

## Contributing And Agent Work

Use `docs/agent_runbook.md` before starting an automated run. In routine
maintenance, prefer bounded artifacts and reports over broad regeneration.

Safe default output locations:

- Machine-readable audit: `artifacts/v3_<topic>_<scope>_<date>.json`
- Human-readable report: `work/<topic>_<date>.md`
- Durable project memory: `docs/*.md`

Do not edit labels, registries, ontologies, production scoring, imports, or
global thresholds unless the task explicitly says to do so and the required
gates are run.

## Repository Layout

```text
data/registries/        Source, fingerprint, ontology, and label registries
docs/                   Durable project memory and design references
src/catalytic_earth/    CLI and artifact-building code
tests/                  Unit and artifact regression tests
artifacts/              Generated machine-readable outputs
work/                   Human-readable run reports and handoffs
```

## Historical Context

Longer scientific and implementation history lives in the docs and artifact
reports instead of this front page:

- `docs/research_program.md`
- `docs/v2_report.md`
- `docs/v2_strengthening_report.md`
- `docs/geometry_features.md`
- `docs/label_factory.md`
- `docs/external_source_transfer.md`
- `docs/artifact_storage.md`
- `docs/wave1_representation_shootout.md`
