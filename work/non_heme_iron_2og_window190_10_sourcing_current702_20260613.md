# Non-Heme Iron 2OG Dioxygenase Sourcing - broadened evidence handles

Run: 2026-06-14T00:04:27Z

Sources fresh reviewed Swiss-Prot bronze for non-heme Fe(II)/2-oxoglutarate
dioxygenases via iron/non-heme metal plus 2OG/succinate/CO2 Rhea participant or
Dioxygenase keyword evidence with EC 1.14.11 scope. EC / keyword / 2OG text are
scope-admission only, never predictive; heme/flavin/peroxide rows are guarded out.

## Result

- Families sourced: non_heme_iron_2og_dioxygenase.
- Lanes queried: 4 (<= 230 rows each).
- Per-lane record window: offset 190, limit 10.
- Fetched candidate rows: 10.
- Target mechanism-corroborated bronze labels: 6 (off-target held 0; disambiguation holds 3; skipped 1).
- **Novelty-admitted labels: 4** (throttled/rejected 1; held@cap 1).
- Combined registry 7657 -> **7661** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| non_heme_iron_2og_dioxygenase | fe_ii_2og_o2_cosubstrate | 246 | 4 | 250 | 250 | True | 1 |

## Novelty gate

- Decisions: {'admit': 5, 'reject': 1}.
- Reasons: {'adds_diversity': 5, 'fingerprint_over_cap_no_new_chemistry': 1}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 3}.
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
