# Under-Cap Extension Live Fetch Blocker

Automation ID: `ce-nad-glyco-floor-expansion`

Created UTC: `2026-06-13T14:21:19Z`

## Result

No registry rows were written in this run. The attempted live sourcing previews did not return
bounded preview artifacts quickly enough to support a safe preview -> inspect gates -> apply ->
validate -> push cycle.

Frozen current702 remained unchanged:
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Counts remain:

| Counter | Value |
| --- | ---: |
| frozen current702 | 702 |
| external bronze | 6238 |
| external seed-fingerprint bronze | 5014 |
| external OOS bronze | 1224 |
| combined label surface | 6940 |
| positive_bronze | 5227 |
| oos_bronze | 1696 |
| silver_ready | 0 |
| silver_confirmed | 17 |
| projected | 0 |
| remaining positive-bronze gap to 10k | 4773 |

## Attempts

1. CoA/acyl-CoA acyltransferase extension, deep preview:
   `PYTHONPATH=src python scripts/source_coa_acyltransferase_family.py --max-records-per-lane 500 --cap-ceiling 250 --out artifacts/v3_coa_acyltransferase_extension_sourcing_preview_current702_20260613.json --report work/coa_acyltransferase_extension_sourcing_current702_20260613.md`
   Result: terminated after no preview artifact was produced; no registry write.

2. CoA/acyl-CoA acyltransferase extension, smaller preview:
   `PYTHONPATH=src python scripts/source_coa_acyltransferase_family.py --max-records-per-lane 280 --cap-ceiling 250 --out artifacts/v3_coa_acyltransferase_extension_sourcing_preview_current702_20260613.json --report work/coa_acyltransferase_extension_sourcing_current702_20260613.md`
   Result: terminated after no preview artifact was produced; no registry write.

3. Cofactor-independent isomerase cap-fill preview:
   `PYTHONPATH=src python scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 120 --cap-ceiling 150 --out artifacts/v3_cofactor_independent_isomerase_capfill_sourcing_preview_current702_20260613.json --report work/cofactor_independent_isomerase_capfill_sourcing_current702_20260613.md`
   Result: terminated after no preview artifact was produced; no registry write.

## Current Lane State

The latest durable handoff remains scientifically correct: `pfkb_ribokinase_family` is 46/100 and
`biotin_dependent_carboxylase` is 84/100, but their current strict reviewed source paths are
exhausted under mechanism-first gates.

Under-cap approved lanes with possible bounded follow-up:

| Fingerprint | External count | Cap | Note |
| --- | ---: | ---: | --- |
| `cofactor_independent_isomerase` | 142 | 150 | Smallest safe cap-fill target; retry first with the 120-row preview above. |
| `coa_acyltransferase` | 188 | 250 | High-diversity approved lane; retry only with bounded preview, inspect gates before apply. |
| `non_heme_iron_2og_dioxygenase` | 172 | 250 | Approved lane; possible extension after CoA/isomerase if live fetch is healthy. |
| `molybdopterin_oxidoreductase` | 207 | 250 | Approved lane; possible extension but reaction-poor. |
| `copper_oxidoreductase` | 140 | 250 | Already extended this morning; another deep pass may have low yield. |
| `cytochrome_p450_monooxygenase` | 248 | 250 | Do not add more without explicit new reaction/organism justification. |

## Guardrails

- No added labels, no `predictive_evidence` changes, and no source-free feature changes.
- EC/name/keyword/Rhea/prose/feature handles remain excluded-context admission evidence only.
- EC is never a counted mechanism corroborator.
- Frozen current702 was not written.

## Next Exact Action

Retry the smallest cap-fill first:

`PYTHONPATH=src python scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 120 --cap-ceiling 150 --out artifacts/v3_cofactor_independent_isomerase_capfill_sourcing_preview_current702_20260613.json --report work/cofactor_independent_isomerase_capfill_sourcing_current702_20260613.md`

If it produces preview rows, inspect `floor_projection`, `novelty_gate`, held-at-cap, trust-tier,
and leakage fields before running the same command with `--apply`. If live fetch remains slow, do
not apply; preserve the blocker and choose an offline source-supply scout or a new-family design
artifact instead.
