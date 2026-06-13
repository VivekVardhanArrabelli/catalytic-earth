# Non-Heme Iron 2OG Dioxygenase Apply - current702

Run: 2026-06-13T00:27:47Z

Applied gated external bronze rows for `non_heme_iron_2og_dioxygenase` through the
existing external annotation writer. The frozen current702 benchmark was not written.

## Apply Result

- Command: `PYTHONPATH=src python scripts/source_non_heme_iron_2og_family.py --max-records-per-lane 80 --apply`
- Fetched candidate rows: 212.
- Target mechanism-corroborated labels: 198.
- Novelty-admitted labels: 172.
- Appended bronze rows: 172.
- Duplicate skipped at apply: 0.
- External bronze registry: 3700 -> 3872.
- Combined label surface: 4402 -> 4574.
- `non_heme_iron_2og_dioxygenase`: 0 -> 172 (cap 250; floor reached; held at cap 0).
- Frozen current702 sha before and after:
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.

## Guardrails

- EC 1.14.11 was used for scope only and stayed non-counted as `ec_scope_hint`.
- Counted mechanism axes came from Fe/cosubstrate, 2OG/succinate/CO2 Rhea participant,
  Dioxygenase/domain keyword, and active/binding-site evidence.
- Heme, flavin, and peroxide rows were guarded out; multi-fingerprint signal rows were held.
- Added rows are `tier=bronze`, `review_status=automation_curated`, and `uniprot:*`.
- `predictive_evidence` stayed `[]`; broadened handles stayed in excluded/admission context.
- Dedup and novelty gates ran against both frozen current702 and the existing external bronze
  registry.

## Counters After Apply

- `positive_bronze=2861`
- `oos_bronze=1696`
- `silver_ready=0`
- `silver_confirmed=17`
- `projected=0`
- Remaining positive-bronze gap to 10k: 7139.

## Follow-On Scout

A non-destructive next-lane scout compared the remaining named candidates. It recommends
`coa_acyltransferase` next: 7728 reviewed UniProt rows and 82 distinct full ECs in a 200-row sample,
with no reaction-poor warning. See
`artifacts/v3_next_lane_source_supply_scout_after_p450_2og_current702_20260613.json`.
