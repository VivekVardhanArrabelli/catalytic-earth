# Molybdopterin Oxidoreductase Sourcing - broadened evidence handles

Run: 2026-06-13T22:17:54Z

Sources fresh reviewed Swiss-Prot bronze for molybdopterin/Mo-cofactor
oxidoreductases via Mo-cofactor/molybdopterin annotation, Mo-pterin feature
text, Rhea redox/oxo-transfer participants, Molybdenum keyword/domain, or
active-/binding-/metal-site context with oxidoreductase EC scope. EC / keyword
/ reaction text are scope-admission only, never predictive; boundary rows with
non-oxidoreductase side ECs, hydrolase, peroxide/peroxidase, or independent
off-target fingerprint signals are guarded or held.

## Result

- Families sourced: molybdopterin_oxidoreductase.
- Lanes queried: 4 (<= 500 rows each).
- Fetched candidate rows: 19.
- Target mechanism-corroborated bronze labels: 11 (off-target held 0; disambiguation holds 0; skipped 8).
- **Novelty-admitted labels: 4** (throttled/rejected 6; held@cap 1).
- Combined registry 7279 -> **7283** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| molybdopterin_oxidoreductase | molybdopterin_metal_center_redox_context | 246 | 4 | 250 | 250 | True | 1 |

## Novelty gate

- Decisions: {'admit': 5, 'reject': 6}.
- Reasons: {'adds_diversity': 5, 'fingerprint_over_cap_no_new_chemistry': 6}.

## Disambiguation holds

- Hold reasons: {}.
- Off-target held counts: {}.

## Guardrails

- Curated registry written: False.
- EC scope-only / never predictive: True.
- Molybdopterin handles scope-admission only, never predictive: True.
- EC never a counted corroborator: True.
- Boundary guards: True.
- Per-family cap ceiling: {'molybdopterin_oxidoreductase': 250}.
- All new labels bronze / automation_curated; novelty-gated vs both registries; heldout benchmark unchanged.

## Next action

- Review floor_projection + novelty_gate. If floor, novelty, dedup, trust-tier, and cap gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
