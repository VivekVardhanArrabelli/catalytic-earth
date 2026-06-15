# Short-Chain Dehydrogenase/Reductase Sourcing - broadened evidence handles

Run: 2026-06-15T22:34:29Z

Sources fresh reviewed Swiss-Prot bronze for EC 1.1.1 SDR-family
dehydrogenases/reductases through SDR family/name context, NAD(P)
cosubstrate or binding context, and Rhea/reviewed alcohol/ketone redox.
EC / keyword / reaction text are scope-admission only, never predictive;
AKR, MDR/zinc alcohol dehydrogenase, ALDH, flavin/metal redox,
oxygenase/oxidase, side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: short_chain_dehydrogenase_reductase.
- Lanes queried: 1 (<= 150 rows each).
- Per-lane record window: offset 0, limit 150.
- Fetched candidate rows: 150.
- Target mechanism-corroborated bronze labels: 97 (off-target held 0; disambiguation holds 52; skipped 1).
- **Novelty-admitted labels: 94** (throttled/rejected 3; held@cap 0).
- Combined registry 8422 -> **8516** if merged.

## Floor projection

- `short_chain_dehydrogenase_reductase`: 0 -> 94 (added 94; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'short_chain_dehydrogenase_reductase': 150}.

## Novelty gate

- Decisions: {'admit': 94, 'throttle': 3}.
- Reasons: {'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 68, 'needed_fingerprint_but_redundant_ortholog': 3}.

## Hold reasons

- {'no_mechanism_corroboration': 52}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
