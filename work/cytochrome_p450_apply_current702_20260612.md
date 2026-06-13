# Cytochrome P450 Bronze Expansion Apply

Run: 2026-06-13T00:07:16Z

## Apply Summary

- Command: `PYTHONPATH=src python scripts/source_cytochrome_p450_family.py --max-records-per-lane 80 --apply`
- Added fingerprint: `cytochrome_p450_monooxygenase`.
- OOS preregistration re-freeze: `artifacts/v3_external_hard_negative_next_tranche_preregistration_16fp_1025.json`.
- Frozen current702 sha before/after apply:
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- External bronze registry: 3590 -> 3700 (+110).
- Combined label surface: 4292 -> 4402.
- Duplicate skipped at apply: 0.

## Source/Gate Counts

- Reviewed Swiss-Prot rows fetched: 142.
- Target mechanism-corroborated bronze labels: 128.
- Gate admitted before cap: 110.
- Appended labels: 110.
- `cytochrome_p450_monooxygenase`: 0 -> 110 (cap 250; floor reached).
- Held at cap: 0.
- Novelty throttled/rejected: 18.
- Disambiguation holds: 14 (`no_mechanism_corroboration`).
- Off-target fingerprint matches held: 0.
- Fetch failures: 0.

## Guardrails

- EC 1.14 is scope-only (`ec_scope_hint`) and was not counted as a corroborator.
- Counted mechanism axes came from heme/cofactor, O2/Rhea participant, P450/monooxygenase
  keyword/domain, active/binding-site, or heme-thiolate evidence.
- P450/O2/heme handles are admission/excluded-context evidence only.
- `predictive_evidence` is `[]` on every appended label.
- Every appended label is `tier=bronze`, `review_status=automation_curated`, and `uniprot:*`.
- Dedup ran against both frozen current702 and existing external bronze.
- Per-fingerprint cap held and no multi-signal row was forced into the family.

## Honest Counters After Apply

- `positive_bronze=2689`
- `oos_bronze=1696`
- `silver_ready=0`
- `silver_confirmed=17`
- `projected=0`
- Remaining positive-bronze gap to 10k: 7311.

## Post-Apply Audit

- `artifacts/v3_coverage_redundancy_audit_current702_20260612_p450_applied.json`
- `work/coverage_redundancy_audit_current702_20260612_p450_applied.md`
- Combined labels: 4402 = 702 frozen + 3700 external.
- Fingerprint Gini: 0.1657.
- Holes: `[]`.
- Over-cap: `['metal_dependent_hydrolase']`.
- Next-batch floor deficit: 0.

## Follow-On

The next non-destructive 10k-path action was a focused supply scout for
`non_heme_iron_2og_dioxygenase`: reviewed Swiss-Prot EC 1.14.11 + iron/dioxygenase handle has
870 rows and 36 distinct specific ECs in a 200-row sample. Next agent should wire it as a deliberate
17fp universe change, not as a generic preflight rerun.
