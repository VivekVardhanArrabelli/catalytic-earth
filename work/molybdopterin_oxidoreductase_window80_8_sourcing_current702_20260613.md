# Molybdopterin Oxidoreductase Sourcing - broadened evidence handles

Run: 2026-06-13T22:14:59Z

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
- Fetched candidate rows: 24.
- Target mechanism-corroborated bronze labels: 21 (off-target held 0; disambiguation holds 2; skipped 1).
- **Novelty-admitted labels: 20** (throttled/rejected 1; held@cap 0).
- Combined registry 7240 -> **7260** if merged.

## Floor projection (100-label floor; per-family cap)

| Family | missing-context | combined before | admitted | projected | cap | floor | held@cap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| molybdopterin_oxidoreductase | molybdopterin_metal_center_redox_context | 207 | 20 | 227 | 250 | True | 0 |

## Novelty gate

- Decisions: {'admit': 20, 'throttle': 1}.
- Reasons: {'adds_diversity': 20, 'redundant_no_novelty_signal': 1}.

## Disambiguation holds

- Hold reasons: {'no_mechanism_corroboration': 2}.
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
