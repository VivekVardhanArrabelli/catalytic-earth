# Non-Heme Iron 2OG Dioxygenase Sourcing - broadened evidence handles

Run: 2026-06-13T00:27:47Z

Sources fresh reviewed Swiss-Prot bronze for non-heme Fe(II)/2-oxoglutarate
dioxygenases via iron/non-heme metal plus 2OG/succinate/CO2 Rhea participant or
Dioxygenase keyword evidence with EC 1.14.11 scope. EC / keyword / 2OG text are
scope-admission only, never predictive; heme/flavin/peroxide rows are guarded out.

## Result

- Families sourced: non_heme_iron_2og_dioxygenase.
- Lanes queried: 4 (<= 80 rows each).
- Fetched candidate rows: 212.
- Target mechanism-corroborated bronze labels: 198 (off-target held 0; disambiguation holds 12; skipped 2).
- **Novelty-admitted labels: 172** (throttled/rejected 26; held@cap 0).
- Combined registry 4402 -> **4574** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| non_heme_iron_2og_dioxygenase | fe_ii_2og_o2_cosubstrate | 0 | 172 | 172 | 250 | True | 0 |

## Novelty gate

- Decisions: {'admit': 172, 'throttle': 26}.
- Reasons: {'adds_diversity': 72, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'redundant_no_novelty_signal': 26}.

## Disambiguation holds

- Hold reasons: {'multi_fingerprint_signal_conflict': 5, 'no_mechanism_corroboration': 7}.
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
