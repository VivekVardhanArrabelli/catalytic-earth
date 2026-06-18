# Metallo-Beta-Lactamase Sourcing - broadened evidence handles

Run: 2026-06-18T12:36:31Z

Sources fresh reviewed Swiss-Prot bronze for EC 3.5.2.6 metallo-beta-lactamases
(MBL; Ambler class B) through metallo/zinc beta-lactamase family/name OR catalytic-zinc
context, plus Rhea/reviewed beta-lactam hydrolysis reaction text.
EC / keyword / reaction text are scope-admission only, never predictive;
serine beta-lactamases (Ser acyl-enzyme, zinc-excluded), penicillin-binding proteins /
DD-peptidases, non-beta-lactam zinc amidohydrolases, side-EC, EC-only, and off-target
rows are guarded.

## Result

- Families sourced: metallo_beta_lactamase.
- Lanes queried: 3 (<= 300 rows each).
- Per-lane record window: offset 0, limit None.
- Fetched candidate rows: 37.
- Target mechanism-corroborated bronze labels: 4 (off-target held 0; disambiguation holds 12; skipped 21).
- **Novelty-admitted labels: 4** (throttled/rejected 0; held@cap 0).
- Combined registry 8902 -> **8906** if merged.

## Floor projection

- `metallo_beta_lactamase`: 0 -> 4 (added 4; cap 150; floor reached: False; held@cap 0).

## Guardrails

- Registry written: False.
- Frozen current702 preserved: True.
- EC scope-only / never predictive: True.
- Predictive features from broadened handles: False.
- Boundary guards: True.
- Per-family caps: {'metallo_beta_lactamase': 150}.

## Novelty gate

- Decisions: {'admit': 4}.
- Reasons: {'closes_hole_fingerprint': 4}.

## Hold reasons

- {'no_mechanism_corroboration': 12}.

## Next action

- Review floor_projection + novelty_gate. If dedup, trust-tier, cap, leakage, and row guardrail gates pass, append `applied_labels` to data/registries/external_bronze_labels.json via the family script `--apply` with frozen current702 sha checks.
