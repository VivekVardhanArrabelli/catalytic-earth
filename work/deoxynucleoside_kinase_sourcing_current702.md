# Deoxynucleoside Kinase Sourcing - broadened evidence handles

Run: 2026-06-13T09:46:00Z

Sources fresh reviewed Swiss-Prot bronze for strict EC 2.7.1 dNK rows via
Rhea ATP/ADP deoxynucleoside phosphoryl-transfer text, dNK family text,
and active-/binding-site annotations. EC, keywords, names, UniProt prose,
and Rhea text are scope-admission only and never predictive.

## Result

- Families sourced: deoxynucleoside_kinase.
- Lanes queried: 1 (<= 240 rows each).
- Fetched candidate rows: 240.
- Target mechanism-corroborated bronze labels: 237 (off-target held 0; disambiguation holds 0; skipped 3).
- **Novelty-admitted labels: 150** (throttled/rejected 0; held@cap 87).
- Combined registry 6435 -> **6585** if merged.

## Floor projection (100-label floor; chemistry-confusable cap 150)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deoxynucleoside_kinase | atp_mg_deoxynucleoside_5_prime_phosphoryl_transfer_context | 0 | 150 | 150 | 150 | True | 87 |

## Novelty gate

- Decisions: {'admit': 237}.
- Reasons: {'adds_diversity': 137, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74}.

## Disambiguation holds

- Hold reasons: {}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- dNK handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Neighboring kinase subclass boundary guards: True.
- Per-family cap ceiling: {'deoxynucleoside_kinase': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
