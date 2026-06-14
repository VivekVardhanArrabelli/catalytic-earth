# Non-Heme Iron 2OG Dioxygenase Sourcing - broadened evidence handles

Run: 2026-06-14T00:00:13Z

Sources fresh reviewed Swiss-Prot bronze for non-heme Fe(II)/2-oxoglutarate
dioxygenases via iron/non-heme metal plus 2OG/succinate/CO2 Rhea participant or
Dioxygenase keyword evidence with EC 1.14.11 scope. EC / keyword / 2OG text are
scope-admission only, never predictive; heme/flavin/peroxide rows are guarded out.

## Result

- Families sourced: non_heme_iron_2og_dioxygenase.
- Lanes queried: 4 (<= 180 rows each).
- Per-lane record window: offset 140, limit 10.
- Fetched candidate rows: 10.
- Target mechanism-corroborated bronze labels: 7 (off-target held 0; disambiguation holds 0; skipped 3).
- **Novelty-admitted labels: 6** (throttled/rejected 1; held@cap 0).
- Combined registry 7634 -> **7640** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| non_heme_iron_2og_dioxygenase | fe_ii_2og_o2_cosubstrate | 223 | 6 | 229 | 250 | True | 0 |

## Novelty gate

- Decisions: {'admit': 6, 'throttle': 1}.
- Reasons: {'adds_diversity': 6, 'redundant_no_novelty_signal': 1}.

## Disambiguation holds

- Hold reasons: {}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Iron/2OG/dioxygenase handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Heme/flavin/peroxide guard: True.
- Per-family cap ceiling: {'non_heme_iron_2og_dioxygenase': 250}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via `apply-external-annotation-anchored-import` with frozen current702 sha checks.
