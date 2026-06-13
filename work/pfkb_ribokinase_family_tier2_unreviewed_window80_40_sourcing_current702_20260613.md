# PfkB Ribokinase-Family Sourcing - broadened evidence handles

Run: 2026-06-13T23:29:27Z

Sources fresh reviewed Swiss-Prot bronze for strict EC 2.7.1 PfkB/ribokinase-family rows via
Rhea ATP/ADP substrate-specific phosphoryl-transfer text, PfkB/ribokinase-family text,
and active-/binding-site annotations. EC, keywords, names, UniProt prose,
and Rhea text are scope-admission only and never predictive.

## Result

- Families sourced: pfkb_ribokinase_family.
- Lanes queried: 1 (<= 120 rows each).
- Per-lane record window: offset 80, limit 40.
- Source trust tier: source_tier_2.
- Unreviewed tier-2 lanes enabled: False (only: True).
- Fetched candidate rows: 40.
- Target mechanism-corroborated bronze labels: 40 (off-target held 0; disambiguation holds 0; skipped 0).
- **Novelty-admitted labels: 25** (throttled/rejected 1; held@cap 14).
- Combined registry 7558 -> **7583** if merged.

## Floor projection (100-label floor; chemistry-confusable cap 150)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pfkb_ribokinase_family | atp_mg_pfkb_ribokinase_family_phosphoryl_transfer_context | 125 | 25 | 150 | 150 | True | 14 |

## Novelty gate

- Decisions: {'admit': 39, 'throttle': 1}.
- Reasons: {'adds_diversity': 39, 'redundant_no_novelty_signal': 1}.

## Disambiguation holds

- Hold reasons: {}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- PfkB handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Source trust tier: source_tier_2; tier-2 three-axis gate: True.
- Neighboring kinase subclass boundary guards: True.
- Per-family cap ceiling: {'pfkb_ribokinase_family': 150}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks. If floor remains short, record the supply limit.
