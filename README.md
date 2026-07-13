# Catalytic Earth

Catalytic Earth is an open, computable catalytic-mechanism atlas. The goal is
to make enzyme function searchable by how catalysis happens — from net
reaction through elementary steps, catalytic residues and geometry, protein
evidence, uncertainty, and experimental outcomes — not only by EC number,
name, keyword, or sequence similarity.

## North Star

Build the world's computable catalytic-mechanism atlas: a continuously
expanding, provenance-grounded map from biochemical reaction and protein
evidence to explicit, testable chemical-function hypotheses.

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

The full atlas is the mission. A typed mechanism intermediate representation
and evidence compiler are the engine. Benchmarks, exposure ledgers, and fresh
external tests are quality-control systems inside the atlas; they are not the
product or the limit of its ambition. Search/API surfaces deliver the atlas to
users, and prospective experimental loops correct it against biological
reality.

The atlas is tiered so breadth can grow quickly without implying equal truth:

1. canonical reaction record;
2. explicit mechanism hypothesis;
3. protein/site-grounded hypothesis;
4. independently reviewed mechanism;
5. experimentally tested positive or negative outcome.

This repository remains a research scaffold. It is not a wet-lab protocol,
not a claim that computational candidates are validated enzymes, and not yet
a production biological design system.

## Quick Status — 2026-07-13 truth reset

- `current702` contains 702 project benchmark labels: 685 bronze, 17 silver,
  zero project-gold; 683 are automation-curated and 19 author-reviewed.
- The combined 10,001-row surface is **8,305 positive fingerprint assignments
  plus 1,696 out-of-scope protein-label records**, not 10,001 distinct
  mechanisms.
- The reported 76% chemistry result is a **cofactor-bucket consistency**
  endpoint. Exact fingerprint recovery was 65/210 (31%) on the featurizable,
  centroid-covered positive subset. The reported ID/OOS medians do not by
  themselves establish useful novelty separation.
- The 2026-06-28 M-CSA result is **retrospective analysis of an exhausted test
  surface**, not a never-touched independent validation: all 126 rows were
  already exposed by 2026-06-04 and the one-shot was explicitly declared spent.
- The 2026-06-29 Swiss-Prot/PDB-holo surface is an EC-proxy validation set, not
  mechanism gold. It recovered 45/64 overall, including 2/16 metal, with 2/72
  OOS false positives; its 40% preregistered OOS ceiling was too permissive for
  a deployment claim.
- A Python 3.13 full-suite audit ran 2,559 tests: 74 failures, 20 errors, and one
  skip. Some are dependency/Windows-path failures; many reflect stale hashes
  and checked-in state drift. Targeted green tests do not make the full suite
  green.
- New label/family expansion and new performance headlines are frozen until
  the claim ledger, exposure ledger, reproducible core environment, and live
  artifact manifest are in place.
- The active execution plan is `docs/RAPID_ATLAS_PLAN.md`: a 35-day
  computational atlas loop with a parallel 60–90-day experimental target when
  a ready assay and external execution route exist.

## Truth-governance gate

Before interpreting older reports, use the canonical truth surfaces:

- [`CLAIMS.md`](CLAIMS.md) — current Supported / Diagnostic / Superseded /
  Retracted claims;
- [`ERRATA.md`](ERRATA.md) — public corrections that preserve the historical
  artifacts;
- [`docs/ATLAS_TRUTH_POLICY.md`](docs/ATLAS_TRUTH_POLICY.md) — counted objects,
  evidence tiers, endpoint rules, and the expansion freeze;
- [`data/governance/exposure_ledger.jsonl`](data/governance/exposure_ledger.jsonl)
  — append-only history of frozen, exposed, and exhausted evaluation surfaces.
- [`data/governance/expansion_freeze.json`](data/governance/expansion_freeze.json)
  — machine-enforced registry-write freeze while CE-012 is active.

Historical artifacts are not silently rewritten. If an older document
conflicts with these files, the canonical claim ledger and errata control
current wording.

## Start Here

Read these files in order before interpreting older reports or starting an
agent run:

| File | Use it for |
| --- | --- |
| `CLAIMS.md` | Canonical current scientific and project claims |
| `ERRATA.md` | Corrections to invalid or misleading historical wording |
| `docs/ATLAS_TRUTH_POLICY.md` | Counted objects, evidence tiers, exposure rules, and admission freeze |
| `data/governance/exposure_ledger.jsonl` | Append-only evaluation exposure state |
| `docs/CURRENT_STATE.md` | Compact current state, trusted results, blockers, and next gates |
| `docs/CURRENT_DECISIONS.md` | Current durable decisions that govern historical records |
| `docs/RAPID_ATLAS_PLAN.md` | Current 35-day computational plan, parallel experimental clock, and atlas scale gates |
| `docs/reviews/catalytic-earth-full-review-2026-07-10.md` | Independent audit, evidence corrections, strategic amendment, and full rationale |
| `docs/reviews/catalytic-earth-90-day-map-2026-07-10.md` | Compact operating map derived from the full review |
| `docs/project_state.md` | Historical detailed state retained for provenance |
| `docs/decision_log.md` | Historical decision log retained for provenance |
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
PYTHONPATH=src python scripts/validate_truth_governance.py
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
- Clean M-CSA geometry and predicted-structure geometry are different
  benchmark surfaces. Use `artifacts/v3_predicted_geometry_robustness_audit_current702_20260529.json`
  before claiming sequence-to-structure deployment readiness.
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
