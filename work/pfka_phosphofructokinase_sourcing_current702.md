# PfkA Phosphofructokinase Sourcing - broadened evidence handles

Run: 2026-06-13T10:51:53Z

Sources fresh reviewed Swiss-Prot bronze for strict EC 2.7.1 PfkA rows via
Rhea ATP/ADP fructose-6-phosphate phosphoryl-transfer text, PfkA family text,
and active-/binding-site annotations. EC, keywords, names, UniProt prose,
and Rhea text are scope-admission only and never predictive.

## Result

- Families sourced: pfka_phosphofructokinase.
- Lanes queried: 1 (<= 240 rows each).
- Fetched candidate rows: 240.
- Target mechanism-corroborated bronze labels: 233 (off-target held 0; disambiguation holds 5; skipped 2).
- **Novelty-admitted labels: 150** (throttled/rejected 0; held@cap 83).
- Combined registry 6585 -> **6735** if merged.

## Floor projection (100-label floor; chemistry-confusable cap 150)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pfka_phosphofructokinase | atp_mg_fructose_6_phosphate_phosphoryl_transfer_context | 0 | 150 | 150 | 150 | True | 83 |

## Novelty gate

- Decisions: {'admit': 233}.
- Reasons: {'adds_diversity': 133, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 5}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- PfkA handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Neighboring kinase subclass boundary guards: True.
- Per-family cap ceiling: {'pfka_phosphofructokinase': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
