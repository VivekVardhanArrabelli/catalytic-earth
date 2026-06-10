# Stage-1 Hole Sourcing Runbook

This runbook executes **Stage 1** of `docs/scaling_plan_to_10k.md` — closing the
governor's HOLE fingerprints toward the 100-label floor — for the two
**cofactor-defined** holes. It is meant for a session with **live UniProt egress**
(the cloud sandbox blocks it by default; run where the environment network policy is
`Full` or `Custom`-allowing `*.uniprot.org`).

## What it does

A single command runs the existing, tested pipeline end to end and writes a
non-destructive preview:

```
fetch_uniprot_query / fetch_uniprot_entry        (live UniProt REST)
  -> build_external_source_ingestion_pilot        (hole lane queries -> canonical rows)
  -> build_cofactor_ec_disambiguation             (cofactor+EC scope, _build_label,
                                                    dedup vs BOTH registries, multi-
                                                    fingerprint-signal rows held)
  -> evaluate_batch (novelty gate)                 (admit only new cluster/reaction/organism)
  -> preview artifact + report
  -> (--apply) apply_external_annotation_anchored_import_to_registry
```

Code: `src/catalytic_earth/stage1_hole_sourcing.py`; runner: `scripts/stage1_source_holes.py`;
offline test: `tests/test_stage1_hole_sourcing.py` (validates routing with synthetic
payloads — no network).

## Which holes

| Hole | combined (2026-06-10) | route |
| --- | --- | --- |
| `radical_sam_enzyme` | 10 | **this runner** — Fe-S + SAM cofactor/EC disambiguation |
| `cobalamin_radical_rearrangement` | 10 | **this runner** — adenosylcobalamin + mutase-EC disambiguation |
| `ser_his_acid_hydrolase` | 42 | **NOT this runner** — cofactorless; use `build-ser-his-triad-locator-scan` |

`ser_his` has no catalytic cofactor to corroborate, so the cofactor/EC engine
structurally cannot reach it. Source it with the dedicated triad locator, which
confirms the Ser/Cys-His-Asp triad against coordinates (the plan's Stage-1 route).

## Run it

```bash
# 0. confirm egress (expect 200)
curl -s -o /dev/null -w "%{http_code}\n" \
  "https://rest.uniprot.org/uniprotkb/search?query=ec:3.4.21.1&format=tsv&size=1"

# 1. preview only (non-destructive; writes artifact + report, no registry change)
PYTHONPATH=src python scripts/stage1_source_holes.py --max-records-per-lane 100

# 2. review the preview: floor_projection, novelty_gate decisions, fetch_failures
python -m json.tool artifacts/v3_stage1_hole_sourcing_preview_current702.json | less

# 3. when the preview looks right, append the novelty-admitted bronze labels
PYTHONPATH=src python scripts/stage1_source_holes.py --max-records-per-lane 100 --apply

# 4. (separately) the ser_his hole
PYTHONPATH=src python -m catalytic_earth.cli build-ser-his-triad-locator-scan --help
```

Scale `--max-records-per-lane` up (e.g. 200) to reach the floor; the novelty gate
throttles near-duplicate orthologs, so raw count and admitted count differ.

## Guardrails (asserted on the output)

- **Frozen current702 benchmark is never written.** Only the separate expansion
  registry `data/registries/external_bronze_labels.json` is appended (by `--apply`).
- **Leakage wall.** Scope is decided from reviewed Swiss-Prot/EC/Rhea/cofactor
  annotation only; EC / protein name / prose stay in `excluded_context`, never
  predictive features.
- `tier=bronze`, `review_status=automation_curated`.
- New labels are deduped vs **both** registries; **multi-fingerprint-signal rows stay
  held**; the novelty gate is seeded from both registries so existing orthologs are
  throttled, not re-imported.
- The runner without `--apply` writes nothing but `artifacts/` + `work/`.

## After applying

```bash
PYTHONPATH=src python -m catalytic_earth.cli validate
python -m unittest discover -s tests
git diff --check
# regenerate the governor to confirm the holes moved
PYTHONPATH=src python -m catalytic_earth.cli build-coverage-redundancy-audit \
  --out /tmp/gov.json --report /tmp/gov.md
```

Then commit the registry append + the preview/report, and refresh
`docs/project_state.md` / `docs/decision_log.md` with the new per-fingerprint counts.

## Notes / honest caveats

- Disambiguation is **conservative by design**: a row becomes bronze only when a
  single cofactor+EC rule fires. Genuine radical-SAM / cobalamin entries that lack a
  clear annotated cofactor stay held — that is correct, not a bug. Expect admitted <
  fetched.
- If a query returns few rows, **split into more EC/keyword subqueries** rather than
  increasing page depth (the 2026-06-09 page-depth saturation lesson).
- The cofactor evidence for radical-SAM needs both `[4Fe-4S]`/iron-sulfur AND a SAM
  signal (cofactor or binding-site ligand). Some reviewed entries annotate SAM only as
  a substrate; those will hold.
