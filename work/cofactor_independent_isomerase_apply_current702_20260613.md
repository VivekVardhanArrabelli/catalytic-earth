# Cofactor-independent isomerase 19fp apply

Run: 2026-06-13T01:35:19Z

Applied gated external bronze rows for `cofactor_independent_isomerase` through
the existing mechanism-first admission pipeline. Growth went only to
`data/registries/external_bronze_labels.json`; frozen current702 stayed
byte-unchanged.

## Apply command

`PYTHONPATH=src python scripts/source_cofactor_independent_isomerase_family.py --max-records-per-lane 80 --apply`

## Counts

- Frozen current702 sha before/after apply:
  `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- External bronze: 4060 -> 4202 (+142).
- Combined label surface: 4762 -> 4904.
- `cofactor_independent_isomerase`: 0 -> 142 (cap 150; floor reached).
- Fetched candidate rows: 266.
- Target mechanism-corroborated bronze labels: 147.
- Novelty-admitted/applied labels: 142.
- Novelty throttled/rejected: 5.
- Held at cap: 0.
- Disambiguation holds: 70 (`no_mechanism_corroboration`).
- Off-target fingerprint matches held: 28 (`nad_p_dehydrogenase`).
- Duplicate skipped at apply: 0.

## Guardrails

- EC 5.3 is scope-only and never a counted corroborator.
- Rhea isomerization equation text, Isomerase keyword/domain, and active-/
  binding-site/base context are admission evidence only.
- Non-5.3 side-EC rows are held.
- `predictive_evidence` is `[]` on added rows.
- Added rows are `tier=bronze`, `review_status=automation_curated`, and use the
  `uniprot:*` namespace.
- Dedup ran against frozen current702 and the existing external bronze registry.
- Chemistry-confusable cap 150 was enforced; no fingerprint was pushed over cap.
- Row spot-check across 142 applied rows found 0 leakage/trust-tier problems;
  source-trust axes present across rows: domain/family 142, Rhea participant
  135, active-site/residue-role 134, cofactor/cosubstrate 69.

## Post-apply state

- Coverage audit:
  `artifacts/v3_coverage_redundancy_audit_current702_20260613_isomerase_applied.json` /
  `work/coverage_redundancy_audit_current702_20260613_isomerase_applied.md`.
- Novelty audit:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260613_isomerase_applied.json` /
  `work/novelty_admission_gate_audit_current702_20260613_isomerase_applied.md`.
- Combined labels: 4904 = 702 frozen + 4202 expansion.
- Fingerprint Gini: 0.1613.
- Holes: `[]`.
- Over-cap: `['metal_dependent_hydrolase']`.
- Next-batch floor deficit: 0.
- Honest counters: `positive_bronze=3191`, `oos_bronze=1696`,
  `silver_ready=0`, `silver_confirmed=17`, `projected=0`.
- Remaining positive-bronze gap to 10k: 6809.

## Follow-on scout

After the apply, a non-destructive next-lane scout wrote
`artifacts/v3_next_lane_source_supply_scout_after_isomerase_current702_20260613.json` /
`work/next_lane_source_supply_scout_after_isomerase_current702_20260613.md` and
recommended `molybdopterin_oxidoreductase` next over `copper_oxidoreductase`:
460 reviewed UniProt entries and 33 distinct full EC labels in a 200-row sample
versus 222 and 12 for copper. Both are reaction-poor, so the next agent should
run a mechanism-handle scout and design subclass guards before any preview/apply.
