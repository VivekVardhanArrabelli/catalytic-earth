---
name: catalytic-earth
description: Answer enzyme mechanism questions from Catalytic Earth's reviewed offline records and write a sourced brief. Use for a named variant, catalytic residue, endpoint (turnover, isotope exchange, structure), or a perturbation comparison between constructs — "does H297N racemization nondetection mean catalysis is lost", "did H473N improve target product accumulation", "what does the record actually support". Also use to attach a saved external structure or source-tool output to the case it answers. Not for new experiments, training runs, docking, literature search, or questions the packaged records do not cover.
---

# Catalytic Earth mechanism queries

A Catalytic Earth **project** skill. It orchestrates commands that already exist
in this repository. It is not a Rosalind suite plugin and running it is not
evidence of native tool use.

Every command here is offline, read-only and deterministic. None of them
computes new chemistry: they return reviewed records of published observations,
with the scope limits those records carry.

## 1. Resolve the question before running anything

Name the surface and the exact identifiers you will query, and say them to the
user **before** executing. Do not bend an unsupported question into one of the
examples below — if the records do not cover it, say so and stop.

| The question is about | Surface | Identifier you must state |
|---|---|---|
| a variant's measured endpoints in a reviewed mechanism case | `atlas-mechanism-evidence` | variant (e.g. `H297N`), endpoint (`turnover`, `isotope_exchange`, `structure`) |
| two constructs compared within one source study | `scripts/query_atlas_perturbations.py` | comparison id (e.g. `tk_2020:H473N:DHB_accumulation`) |
| changed source atoms and their catalytic residues | `atlas-transformation-sites` | M-CSA id |
| what the golden result does and does not claim | `claims` | — |

`catalytic-earth --help` lists every surface. Use it rather than guessing.

## 2. Run the real command and keep its output

```sh
# Installed wheel or source checkout. Works from any directory.
catalytic-earth atlas-mechanism-evidence --variant H297N --endpoint isotope_exchange \
  --output sessions/<UTC-timestamp>/evidence.json

# Source checkout only: derives its root from the script's location and shells
# out to git. It will not run from an installed wheel.
python scripts/query_atlas_perturbations.py \
  --comparison tk_2020:H473N:DHB_accumulation \
  --output sessions/<UTC-timestamp>/perturbation.json
```

Write into a new `sessions/<UTC-timestamp>/` directory (git-ignored) and save a
`provenance.json` beside the output recording the exact command, the source
commit (`git rev-parse HEAD`), and the output's sha256. `--output` never
overwrites an existing file.

## 3. Native structure or source inspection, only if the host really exposes it

If an authorized Rosalind component is available in this host, discover its
actual interface and call it. **Never** invent a tool name, viewer URL, receipt
or installation workaround, and never substitute a web search and credit it as
suite use.

If it is unavailable: finish the local query, deliver the brief, and mark
native inspection explicitly **pending**. That is a complete, honest result.

## 4. Attach a genuinely saved output

Only for a file a real tool actually produced:

```sh
python -m catalytic_earth.workbench.external_results \
  --provider-suite "<suite>" --provider-tool "<exact tool name>" \
  --action structure_view --query "<exact query sent>" \
  --case atlas10.mandelate-racemase-pputida.enolate \
  --publication paper:PMID:8292591 --site P11444:H297 --structure 1MNS \
  --artifact ./saved/1mns-view.png
```

Check what a case carries first with `--resolve-only`. Then respect what comes
back:

- a **confirmation** means the declared identifiers are in the case and one
  relation carries them together. It is not a review of the output's science.
- a functional-observation source and a deposited structure's primary citation
  are different roles. A structural citation under a structure the case carries
  is recorded as `external_context` — not confirmed, not contradicted. Leave it
  as declared; never swap it for a functional source that would match.
- `--context` values are recorded unverified and take no part in any check.
- open the returned artifact from its row in the workbench case card.

Never write into `work/workbench_external_sources.json` by hand.

## 5. Write the brief

Seven headings, in this order. `docs/briefs/` holds two worked examples.

1. **Question** — as asked.
2. **Source-scoped answer** — what the record supports, in one or two sentences.
3. **Decisive observations** — exact values, units and conditions; quote the
   source witness text.
4. **Structure context** — only where the record supports it, and only as
   reference context.
5. **Sources and artifacts** — exact publication ids and any artifact digests.
6. **Unresolved** — what this does not settle.
7. **Reproduce** — the exact command and the source commit.

## Boundaries that must survive into the brief

- A stored `adjudication` is a **previously reviewed conclusion**. Filters
  select observations; they never recompute it. Quote it as an existing curated
  conclusion tied to its case id, never as something this run derived.
- **Nondetection is not zero** and not absent flux. Where the source gives no
  detection limit, the limit stays unknown.
- Keep a functional paper and a structural paper apart. A reference structure is
  not an observation of the mutant.
- Concentrations are not rates and not selectivity.
- Do not invent error bars, significance, a mutant structure, or an assayed
  sequence.
- These curated cases are demonstrations, not held-out validation or a benchmark.
