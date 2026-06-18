# Aldo-Keto Reductase Sourcing - broadened evidence handles

Run: 2026-06-18T00:42:42Z

Sources fresh reviewed Swiss-Prot bronze for EC 1.1.1 aldo-keto reductase
(AKR) superfamily carbonyl reductases through AKR family/name context, NADP(H)
cosubstrate or binding context, and Rhea/reviewed carbonyl-reduction text.
EC / keyword / reaction text are scope-admission only, never predictive;
SDR/Rossmann, MDR/zinc alcohol dehydrogenase, ALDH, flavin/metal redox,
oxygenase/oxidase, side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: aldo_keto_reductase.
- Lanes queried: 3 (<= 300 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 141.
- Target mechanism-corroborated bronze labels: 28 (off-target held 1; disambiguation holds 89; skipped 23).
- **Novelty-admitted labels: 28** (throttled/rejected 0; held@cap 0).
- Combined registry 8842 -> **8870** if merged.

## Floor projection

- `aldo_keto_reductase`: 0 -> 28 (added 28; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'aldo_keto_reductase': 150}.

## Novelty gate

- Decisions: {'admit': 28}.
- Reasons: {'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 2}.

## Hold reasons

- {'no_mechanism_corroboration': 89}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
