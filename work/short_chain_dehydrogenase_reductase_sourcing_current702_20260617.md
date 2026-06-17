# Short-Chain Dehydrogenase/Reductase Sourcing - broadened evidence handles

Run: 2026-06-17T20:05:58Z

Sources fresh reviewed Swiss-Prot bronze for EC 1.1.1 SDR-family
dehydrogenases/reductases through SDR family/name context, NAD(P)
cosubstrate or binding context, and Rhea/reviewed alcohol/ketone redox.
EC / keyword / reaction text are scope-admission only, never predictive;
AKR, MDR/zinc alcohol dehydrogenase, ALDH, flavin/metal redox,
oxygenase/oxidase, side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: short_chain_dehydrogenase_reductase.
- Lanes queried: 3 (<= 300 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 250.
- Target mechanism-corroborated bronze labels: 6 (off-target held 0; disambiguation holds 143; skipped 101).
- **Novelty-admitted labels: 3** (throttled/rejected 3; held@cap 0).
- Combined registry 8769 -> **8772** if merged.

## Floor projection

- `short_chain_dehydrogenase_reductase`: 100 -> 103 (added 3; cap 150; floor reached: True; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'short_chain_dehydrogenase_reductase': 150}.

## Novelty gate

- Decisions: {'admit': 3, 'throttle': 3}.
- Reasons: {'adds_diversity': 3, 'redundant_no_novelty_signal': 3}.

## Hold reasons

- {'no_mechanism_corroboration': 143}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
