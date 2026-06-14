# Aldehyde Dehydrogenase Sourcing - broadened evidence handles

Run: 2026-06-14T20:23:12Z

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
- Lanes queried: 3 (<= 260 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 264.
- Target mechanism-corroborated bronze labels: 250 (off-target held 3; disambiguation holds 10; skipped 1).
- **Novelty-admitted labels: 150** (throttled/rejected 8; held@cap 92).
- Combined registry 7710 -> **7860** if merged.

## Floor projection

- `aldehyde_dehydrogenase`: 0 -> 150 (added 150; cap 150; floor reached: True; held@cap 92).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'aldehyde_dehydrogenase': 150}.

## Novelty gate

- Decisions: {'admit': 242, 'throttle': 8}.
- Reasons: {'adds_diversity': 142, 'closes_hole_fingerprint': 26, 'closes_under_floor_fingerprint': 74, 'redundant_no_novelty_signal': 8}.

## Hold reasons

- {'no_mechanism_corroboration': 10}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
