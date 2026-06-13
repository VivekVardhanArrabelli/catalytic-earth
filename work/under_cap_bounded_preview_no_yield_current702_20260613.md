# Under-Cap Bounded Preview No-Yield Report

Automation ID: `ce-nad-glyco-floor-expansion`

Created UTC: `2026-06-13T14:41:00Z`

## Result

The previous live-fetch blocker was cleared for bounded previews: the sourcing runners completed
and wrote preview artifacts at small `--max-records-per-lane` values. No registry rows were written
because every tested bounded window produced **0 novelty-admitted labels**.

Frozen current702 remained unchanged:
`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

Counts remain external bronze **6238**, combined label surface **6940**, `positive_bronze=5227`,
`oos_bronze=1696`, `silver_ready=0`, `silver_confirmed=17`, `projected=0`.

## Bounded Previews

| Lane | Max records/lane | Fetched | Mechanism-corroborated target | Novelty-admitted | Current count | Cap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cofactor_independent_isomerase` micro | 5 | 14 | 0 | 0 | 142 | 150 |
| `cofactor_independent_isomerase` bounded | 20 | 67 | 0 | 0 | 142 | 150 |
| `coa_acyltransferase` | 20 | 75 | 0 | 0 | 188 | 250 |
| `non_heme_iron_2og_dioxygenase` | 20 | 66 | 3 | 0 | 172 | 250 |
| `molybdopterin_oxidoreductase` | 20 | 67 | 2 | 0 | 207 | 250 |
| `zinc_lyase_hydratase` | 20 | 20 | 0 | 0 | 113 | 150 |
| `copper_oxidoreductase` | 20 | 40 | 1 | 0 | 140 | 250 |

The 2OG, molybdopterin, and copper target rows were novelty-throttled as
`redundant_no_novelty_signal`. The other lanes had no target mechanism-corroborated rows in the
bounded first windows.

## Guardrails

- No `--apply` was run.
- No rows were added to `data/registries/external_bronze_labels.json`.
- EC/name/keyword/Rhea/prose/feature handles remain excluded-context admission evidence only.
- EC is not a counted corroborator.
- `predictive_evidence` was not changed.

## Next Action

Do not repeat these same bounded first-window probes. The useful next move is one of:

1. Build a genuinely new PfkB or biotin source path with stronger mechanism corroboration.
2. Run a targeted deeper under-cap extension only when enough time remains for completion,
   inspection, validation, docs, push, and lock release.
3. Start a new-family mechanism/source-supply scout/spec if evidence is cleaner than further
   balanced-lane top-ups.
