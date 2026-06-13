# PfkB Ribokinase-Family Sourcing - broadened evidence handles

Run: 2026-06-13T11:55:29Z

Sources fresh reviewed Swiss-Prot bronze for strict EC 2.7.1 PfkB/ribokinase-family rows via
Rhea ATP/ADP substrate-specific phosphoryl-transfer text, PfkB/ribokinase-family text,
and active-/binding-site annotations. EC, keywords, names, UniProt prose,
and Rhea text are scope-admission only and never predictive.

## Result

- Families sourced: pfkb_ribokinase_family.
- Lanes queried: 1 (<= 500 rows each).
- Fetched candidate rows: 88.
- Target mechanism-corroborated bronze labels: 0 (off-target held 4; disambiguation holds 36; skipped 48).
- **Novelty-admitted labels: 0** (throttled/rejected 0; held@cap 0).
- Combined registry 6781 -> **6781** if merged.

## Floor projection (100-label floor; chemistry-confusable cap 150)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pfkb_ribokinase_family | atp_mg_pfkb_ribokinase_family_phosphoryl_transfer_context | 46 | 0 | 46 | 150 | False | 0 |

## Novelty gate

- Decisions: {}.
- Reasons: {}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 36}.
- Off-target held counts: {'askha_sugar_acetate_kinase': 4}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- PfkB handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Neighboring kinase subclass boundary guards: True.
- Per-family cap ceiling: {'pfkb_ribokinase_family': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks. If floor remains short, record the supply limit.
