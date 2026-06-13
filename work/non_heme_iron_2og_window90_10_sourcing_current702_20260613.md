# Non-Heme Iron 2OG Dioxygenase Sourcing - broadened evidence handles

Run: 2026-06-13T23:46:07Z

Sources fresh reviewed Swiss-Prot bronze for non-heme Fe(II)/2-oxoglutarate
dioxygenases via iron/non-heme metal plus 2OG/succinate/CO2 Rhea participant or
Dioxygenase keyword evidence with EC 1.14.11 scope. EC / keyword / 2OG text are
scope-admission only, never predictive; heme/flavin/peroxide rows are guarded out.

## Result

- Families sourced: non_heme_iron_2og_dioxygenase.
- Lanes queried: 4 (<= 130 rows each).
- Per-lane record window: offset 90, limit 10.
- Fetched candidate rows: 20.
- Target mechanism-corroborated bronze labels: 13 (off-target held 0; disambiguation holds 0; skipped 7).
- **Novelty-admitted labels: 13** (throttled/rejected 0; held@cap 0).
- Combined registry 7600 -> **7613** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| non_heme_iron_2og_dioxygenase | fe_ii_2og_o2_cosubstrate | 189 | 13 | 202 | 250 | True | 0 |

## Novelty gate

- Decisions: {'admit': 13}.
- Reasons: {'adds_diversity': 13}.

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
