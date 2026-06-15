# Short-Chain Dehydrogenase/Reductase Sourcing - broadened evidence handles

Run: 2026-06-15T22:31:22Z

Sources fresh reviewed Swiss-Prot bronze for EC 1.1.1 SDR-family
dehydrogenases/reductases through SDR family/name context, NAD(P)
cosubstrate or binding context, and Rhea/reviewed alcohol/ketone redox.
EC / keyword / reaction text are scope-admission only, never predictive;
AKR, MDR/zinc alcohol dehydrogenase, ALDH, flavin/metal redox,
oxygenase/oxidase, side-EC, EC-only, and off-target rows are guarded.

## Result

- Families sourced: short_chain_dehydrogenase_reductase.
- Lanes queried: 1 (<= 60 rows each).
- Per-lane record window: offset 0, limit 60.
- Fetched candidate rows: 60.
- Target mechanism-corroborated bronze labels: 53 (off-target held 0; disambiguation holds 7; skipped 0).
- **Novelty-admitted labels: 50** (throttled/rejected 3; held@cap 0).
- Combined registry 8422 -> **8472** if merged.

## Floor projection

- `short_chain_dehydrogenase_reductase`: 0 -> 50 (added 50; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'short_chain_dehydrogenase_reductase': 150}.

## Novelty gate

- Decisions: {'admit': 50, 'throttle': 3}.
- Reasons: {'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 24, 'needed_fingerprint_but_redundant_ortholog': 3}.

## Hold reasons

- {'no_mechanism_corroboration': 7}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
