# Mn/Fe Superoxide Dismutase Sourcing - broadened evidence handles

Run: 2026-06-13T15:35:43Z

Sources fresh reviewed Swiss-Prot bronze for Mn/Fe superoxide dismutases via
Rhea superoxide dismutation text, Mn/Fe metal or metal-site evidence, SOD
keyword/domain text, and active-/binding-/metal-site annotations. EC and
protein-name tokens are scope-admission only and never predictive.

## Result

- Families sourced: manganese_iron_superoxide_dismutase.
- Lanes queried: 1 (<= 320 rows each).
- Fetched candidate rows: 252.
- Target mechanism-corroborated bronze labels: 19 (off-target held 0; disambiguation holds 69; skipped 164).
- **Novelty-admitted labels: 2** (throttled/rejected 17; held@cap 0).
- Combined registry 7104 -> **7106** if merged.

## Floor projection (100-label floor; non-confusable cap 250)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| manganese_iron_superoxide_dismutase | mn_fe_superoxide_redox_dismutation_context | 164 | 2 | 166 | 250 | True | 0 |

## Novelty gate

- Decisions: {'admit': 2, 'throttle': 17}.
- Reasons: {'adds_diversity': 2, 'redundant_no_novelty_signal': 17}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 69}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- SOD handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Cu/Zn, heme/peroxidase, superoxide-reductase, and side-EC guards: True.
- Per-family cap ceiling: {'manganese_iron_superoxide_dismutase': 250}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
