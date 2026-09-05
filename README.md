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

## Quick Status — 2026-09-05

The compiled atlas remains the 2026-07-14 checkpoint built on the 2026-07-13
truth reset. The September update adds review intake and a
[computational correction review](docs/COMPUTATIONAL_REVIEW_20260905.md) of the
57-row crosswalk and 40-case proposal. It also withdraws the A0A177THN5
APX-specific transfer and retires the study based on it (CE-017). No benchmark
was rescored or independent human-review status upgraded.

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
- The preserved Python 3.13 audit ran 2,559 tests with 74 failures, 20 errors,
  and one skip. Root-cause review corrected an overstatement: 54 failed tests
  contained 179 CRLF-only hash comparisons, while exactly one genuine
  historical lineage mismatch remains quarantined. After bounded repairs, the
  pinned complete suite ran 2,586 tests with zero failures, zero errors, and
  one skip. This is software health, not biological validation.
- The P0 truth-reset implementation is complete and evidence-mapped in
  `docs/P0_COMPLETION.md`. The registry expansion latch remains intentionally
  active until a separate reviewed post-reset admission decision; cleanup does
  not silently authorize new labels or performance headlines.
- The active execution plan is `docs/RAPID_ATLAS_PLAN.md`: a 35-day
  computational atlas loop with a parallel 60–90-day experimental target when
  a ready assay and external execution route exist.
- The Atlas-3 first biological kernel is compiled: AdoCbl methylmalonyl-CoA
  mutase, E. coli MnSOD, and TEM-1 now have separate Tier-0 reaction, Tier-1
  source-mechanism, and Tier-2 protein/site-grounded hypothesis objects. The
  MnSOD source object explicitly abstains rather than importing the Cu/Zn
  same-EC mechanism. Thirteen source snapshots, five reference-only literature
  handles, the nine records, and a local truth-boundary query are content-bound
  and reproducible. This is useful Atlas knowledge, not biological validation
  or a coverage benchmark.
- Atlas-10 is computationally compiled as the immutable Atlas-3 plus seven v3
  follow-on packages: 10 cases, 30 typed truth objects, 45 source bindings, 3
  explicit Rhea gaps, 21 detailed source steps, 61 preserved source electron
  flows, and one mandatory zero-step cyclophilin abstention. Two relationship
  queries reproduce from package assets. The matched unintegrated-source
  comparator supports a structural usability result only; no human-time,
  accuracy, or discovery claim is made. A local Windows/Python 3.13 wheel
  passed fresh-directory Atlas-3 and Atlas-10 verification and excludes raw
  source snapshots. The published PR #27 Ubuntu/Windows Python 3.10/3.12
  matrix also passed, satisfying the high-level Atlas-10 scientific exit gate.
  Seven review packets are ready; a real external attempt remains a pending
  frozen review-contract deliverable and is not independent review.
- Atlas-50 Phase A and B provide a 57-row machine-draft crosswalk, 40 proposed
  follow-on cases, 97 unreviewed packets, and an unfrozen 47-case candidate.
  Only the inherited Atlas-10 cases are compiled. A local review-intake command
  now exports packets and intentionally incomplete templates, validates and
  append-only records supplied assertions, and reports unresolved decisions.
  No submission or reviewer was supplied in this update: all 97 packets remain
  without a valid submission, the selection remains unfrozen, and source
  acquisition remains prohibited.

## Truth-governance gate

Before interpreting older reports, use the canonical truth surfaces:

- [`CLAIMS.md`](CLAIMS.md) — current Supported / Diagnostic / Superseded /
  Retracted claims;
- [`ERRATA.md`](ERRATA.md) — public corrections that preserve the historical
  artifacts;
- [`docs/ATLAS_TRUTH_POLICY.md`](docs/ATLAS_TRUTH_POLICY.md) — counted objects,
  evidence tiers, endpoint rules, and the expansion freeze;
- [`data/governance/exposure_ledger.jsonl`](data/governance/exposure_ledger.jsonl)
  — append-only event history of frozen, exposed, and exhausted surfaces;
- [`data/governance/exposure_rows.jsonl`](data/governance/exposure_rows.jsonl)
  — one mechanical memory row per data item and evaluation surface;
- [`data/governance/expansion_freeze.json`](data/governance/expansion_freeze.json)
  — machine-enforced registry-write freeze while CE-012 is active;
- [`docs/P0_COMPLETION.md`](docs/P0_COMPLETION.md) — every cleanup item, its
  evidence, its validation command, and the one deliberately deferred storage
  migration.

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
| `docs/ATLAS3_SELECTION.md` | Frozen first-kernel cases, authoritative handles, budgets, stop conditions, and build sequence |
| `docs/ATLAS3_KERNEL.md` | Compiled nine-object biological kernel, source checks, query, truth boundaries, and reproduction |
| `docs/ATLAS10_SELECTION.md` | Frozen seven-case extension, source gaps, relationship queries, applicability traps, baseline, review, and compute contracts |
| `docs/ATLAS10_KERNEL.md` | Compiled ten-case surface, v3 truth objects, source package, queries, comparator, review state, and remaining gate |
| `docs/ATLAS50_PHASE_A.md` | Deterministic 57-row machine draft, 40-case feasibility matrix, fail-closed 47-case proposal, blockers, and inherited-byte proof |
| `docs/ATLAS50_PHASE_B.md` | Deterministic 97-packet review queue, local append-only review intake, unfrozen 47-case candidate, post-freeze source plan, and explicit review/freeze blockers |
| `docs/P0_COMPLETION.md` | Auditable completion map for the truth-first review's P0 cleanup |
| `docs/reviews/catalytic-earth-full-review-2026-07-10.md` | Independent audit, evidence corrections, strategic amendment, and full rationale |
| `docs/reviews/catalytic-earth-90-day-map-2026-07-10.md` | Compact operating map derived from the full review |
| `docs/project_state.md` | Historical detailed state retained for provenance |
| `docs/decision_log.md` | Historical decision log retained for provenance |
| `docs/artifact_index.md` | Which artifact answers which question, and what is deprecated |
| `docs/agent_runbook.md` | Safe edit boundaries, validation, and output locations |

## Key Commands

Run the bounded canonical result from a release wheel:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --no-deps catalytic_earth-0.1.0-py3-none-any.whl
catalytic-earth reproduce
```

The expected `result_sha256` is
`a2374c6530dfd3b4681db5c3db691fdcdedbf645604c6e7dfe0b95ab7e89ea98`.
It validates packaging, typed schema behavior, determinism, and retention of a
synthetic negative record only; it is not a biological benchmark.

Reproduce the first biological kernel and its local query from the same wheel:

```bash
catalytic-earth atlas3
```

The expected Atlas-3 `runtime_result_sha256` is
`1c21a74b09b5812f27c18d49e891cbe9cad6030364a4b6a41a895cdccb1f1921`.
It reproduces three cases and nine typed biological objects with provenance,
counterevidence, and abstentions. It is not a claim of biological validation,
coverage, prospective discovery, or assay completion.

Reproduce the ten-case Atlas relationship surface:

```bash
catalytic-earth atlas10
```

The expected Atlas-10 `runtime_result_sha256` is
`57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.
It executes two frozen relationship queries with source gaps, applicability,
counterevidence, uncertainty, and provenance. It is not biological validation,
representative coverage, mechanism accuracy, prospective discovery, or a
speedup claim.

Validate the repo:

```bash
python scripts/validate_repository_contracts.py
python scripts/validate_atlas3_selection.py
python scripts/validate_atlas10_selection.py
python scripts/build_atlas3_sources.py
python scripts/build_atlas3_kernel.py --check
python scripts/build_atlas10_sources.py
python scripts/build_atlas10_kernel.py --check
python scripts/build_atlas10_runtime.py --check
python scripts/build_atlas10_baseline.py --check
python scripts/build_atlas10_comparator.py --check
python scripts/build_atlas10_review_packets.py --check
python scripts/build_atlas50_phase_a.py --check
python scripts/validate_atlas50_phase_a.py
python scripts/build_atlas50_phase_b.py --check
python scripts/validate_atlas50_phase_b.py
python scripts/atlas50_review.py status
python scripts/run_test_tier.py "core/unit"
git diff --check
```

Run the test suite after code changes:

```bash
python -m pip install -r requirements/ml.lock
python -m unittest discover -s tests -v
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

## Repository visibility

**Recommended visibility for the canonical repository: public.** Openness is
part of the project's credibility and usefulness: claims, corrections,
provenance, schemas, abstentions, and reproducible releases should be
inspectable without permission from the author.

Use a separate private or local lab workspace for secrets, credentials,
licensed non-redistributable data, blinded labels, embargoed collaborator
material, unpublished assay outcomes before their frozen reveal boundary, and
large disposable intermediates. Public records should contain redistributable
snapshots where permitted and otherwise stable source handles, rights notes,
hashes, and applicability metadata. Repository privacy must never be used to
hide corrections, failed results, or claim history.

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
data/atlas/             Real atlas proposal/release objects outside protected registries
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
