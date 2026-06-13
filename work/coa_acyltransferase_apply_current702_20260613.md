# CoA acyltransferase 18fp apply

Run: 2026-06-13T01:13:10Z

Applied gated external bronze rows for `coa_acyltransferase` through the existing
mechanism-first admission pipeline. Growth went only to
`data/registries/external_bronze_labels.json`; frozen current702 stayed byte-unchanged.

## Apply command

`PYTHONPATH=src python scripts/source_coa_acyltransferase_family.py --max-records-per-lane 80 --apply`

## Counts

- Frozen current702 sha before/after apply:
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- External bronze: 3872 -> 4060 (+188).
- Combined label surface: 4574 -> 4762.
- `coa_acyltransferase`: 0 -> 188 (cap 250; floor reached).
- Fetched candidate rows: 218.
- Target mechanism-corroborated bronze labels: 204.
- Novelty-admitted/applied labels: 188.
- Novelty throttled/rejected: 16.
- Held at cap: 0.
- Disambiguation holds: 11 (`no_mechanism_corroboration`).
- Off-target fingerprint matches held: 1 (`metallo_amidohydrolase_deaminase`).
- Duplicate skipped at apply: 0.

## Guardrails

- EC 2.3.1 is scope-only and never a counted corroborator.
- CoA/acyl-CoA Rhea participant, CoA/acyl-CoA binding-site text,
  Acyltransferase keyword/domain, and active-/binding-site context are admission
  evidence only.
- Hydrolase side-EC rows are held.
- `predictive_evidence` is `[]` on added rows.
- Added rows are `tier=bronze`, `review_status=automation_curated`, and use the
  `uniprot:*` namespace.
- Dedup ran against frozen current702 and the existing external bronze registry.
- Per-fingerprint cap 250 was enforced; no fingerprint was pushed over cap.

## Post-apply state

- Coverage audit:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_coa_applied.json` /
  `work/coverage_redundancy_audit_current702_20260613_coa_applied.md`.
- Combined labels: 4762 = 702 frozen + 4060 expansion.
- Fingerprint Gini: 0.1652.
- Holes: `[]`.
- Over-cap: `['metal_dependent_hydrolase']`.
- Next-batch floor deficit: 0.
- Honest counters: `positive_bronze=3049`, `oos_bronze=1696`,
  `silver_ready=0`, `silver_confirmed=17`, `projected=0`.
- Remaining positive-bronze gap to 10k: 6951.

## Follow-on scout

After the apply, a non-destructive next-lane scout wrote
`artifacts/v3_next_lane_source_supply_scout_after_coa_current702_20260613.json` /
`work/next_lane_source_supply_scout_after_coa_current702_20260613.md` and recommended
`cofactor_independent_isomerase` next. A mechanism-handle scout wrote
`artifacts/v3_cofactor_independent_isomerase_mechanism_handle_scout_current702_20260613.json` /
`work/cofactor_independent_isomerase_mechanism_handle_scout_current702_20260613.md`:
80/80 entries had catalytic activity context, 62/80 had Rhea cross-references,
65/80 had active or binding-site context, and fetch failures were 0.
