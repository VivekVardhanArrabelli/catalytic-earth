# Aldehyde Dehydrogenase Sourcing - broadened evidence handles

Run: 2026-06-14T20:20:48Z

Sources fresh reviewed Swiss-Prot bronze for EC 1.2.1 aldehyde
dehydrogenases through ALDH family context, NAD(P) cosubstrate or
binding context, catalytic Cys/Glu active-site evidence, and
Rhea/reviewed aldehyde oxidation where available. EC / keyword /
reaction text are scope-admission only, never predictive; molybdopterin
aldehyde oxidoreductases, flavin aldehyde oxidases, generic NAD(P)
dehydrogenases, SDR/AKR/MDR rows, side-EC, EC-only, and off-target
fingerprint rows are guarded or held.

## Result

- Families sourced: aldehyde_dehydrogenase.
- Lanes queried: 3 (<= 500 rows each).
- Per-lane record window: offset 260, limit 120.
- Fetched candidate rows: 134.
- Target mechanism-corroborated bronze labels: 4 (off-target held 0; disambiguation holds 130; skipped 0).
- **Novelty-admitted labels: 4** (throttled/rejected 0; held@cap 0).
- Combined registry 7710 -> **7714** if merged.

## Floor projection

- `aldehyde_dehydrogenase`: 0 -> 4 (added 4; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'aldehyde_dehydrogenase': 150}.

## Novelty gate

- Decisions: {'admit': 4}.
- Reasons: {'closes_hole_fingerprint': 4}.

## Hold reasons

- {'no_mechanism_corroboration': 130}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
